"""Article 14 case model and state machine.

States (case level):
    triage -> aware -> early_warning_filed -> notification_filed -> final_filed -> closed
    triage -> not_reportable
The case state is the least-advanced state across its SRP notifications, so a
fan-out case is only "final_filed" when every notification has its final report.

Governance rules enforced (KB: corporate guide 07-reporting-governance.md):
  - Awareness is declared by the awareness authority (PSIRT lead, deputy or duty
    officer) alone. There is no approval step before the early warning.
  - Legal review is recorded before the 72-hour notification and the final
    report, never required for the early warning.
  - Every SRP submission records a filer and a different checker (four-eyes,
    pack design for a web form with no API).
  - A "not reportable" decision is logged with criterion and rationale.
"""
from __future__ import annotations

import json
import uuid
from datetime import datetime, timedelta
from pathlib import Path

from . import clocks, fanout, routing
from .clocks import UTC, fmt_utc, iso, parse_utc

DATA_DIR = Path(__file__).resolve().parent / "data"
CASE_TYPES = ("aev", "severe_incident")
STAGES = ("early_warning", "notification", "final_report")
STATE_ORDER = ("triage", "aware", "early_warning_filed", "notification_filed", "final_filed", "closed")
STAGE_TO_STATE = {"early_warning": "early_warning_filed", "notification": "notification_filed",
                  "final_report": "final_filed"}
DETECTION_SOURCES = ("vrp_bug_bounty", "threat_intel", "in_house_research", "partner_report",
                     "telemetry", "csirt_or_enisa", "customer_report", "media")
NOT_REPORTABLE_CRITERIA = {
    "no_exploitation_evidence": "Research or bug-bounty finding without exploitation evidence (Commission FAQ 5.2; guidance para 218)",
    "component_not_exploitable": "Component vulnerability not present, not reachable or not exploited in the product (FAQ 5.4; para 218)",
    "no_product_security_effect": "Incident with no effect on product security (Art 14(5)(a)-(b); BSI SRP page)",
    "known_before_application": "Exploitation already known before 11 Sep 2026 (guidance para 217)",
}
# Pack targets (internal SLAs, not law), in hours from awareness unless noted.
PACK_TARGETS = {
    "early_warning_filed_h": 12,
    "legal_review_72h_h": 60,
    "affected_user_notice_h": 72,
    "upstream_report_h": 72,
    "nis2_assessment_h": 12,
    "all_users_notice_after_fix_h": 24,
    "legal_review_final_before_due_h": 48,
}


class CaseError(ValueError):
    pass


def load_registry(path: str | Path | None = None) -> dict:
    p = Path(path) if path else DATA_DIR / "aldermoor_registry.json"
    return json.loads(p.read_text())


def load_fields(path: str | Path | None = None) -> dict:
    p = Path(path) if path else DATA_DIR / "srp_fields.json"
    return json.loads(p.read_text())


def _log(case: dict, at: datetime, actor: str, role: str, action: str, detail: str, **extra) -> None:
    entry = {"at": iso(at), "actor": actor, "role": role, "action": action, "detail": detail}
    entry.update({k: v for k, v in extra.items() if v is not None})
    case["decision_log"].append(entry)


def _require_state(case: dict, *allowed: str) -> None:
    if case["state"] not in allowed:
        raise CaseError(f"case {case['id']} is in state '{case['state']}', expected one of {allowed}")


def _recompute_state(case: dict) -> None:
    if case["state"] in ("triage", "not_reportable", "closed"):
        return
    levels = []
    for n in case["notifications"]:
        level = "aware"
        for stage in STAGES:
            if n["submissions"].get(stage):
                level = STAGE_TO_STATE[stage]
        levels.append(STATE_ORDER.index(level))
    case["state"] = STATE_ORDER[min(levels)] if levels else "aware"


# --------------------------------------------------------------------------- create / triage

def create_case(registry: dict, case_type: str, title: str, first_signal_at: str, detection_source: str,
                evidence: dict[str, str], component: str | None = None, summary: str = "",
                fanout_mode: str = "per_product", actor: str = "PSIRT intake", cve_id: str | None = None,
                case_id: str | None = None, entity_incident: bool = False) -> dict:
    if case_type not in CASE_TYPES:
        raise CaseError(f"type must be one of {CASE_TYPES}")
    if detection_source not in DETECTION_SOURCES:
        raise CaseError(f"detection_source must be one of {DETECTION_SOURCES}")
    if not evidence:
        raise CaseError("at least one product with an evidence tier is required")
    if component and component not in registry["components"]:
        raise CaseError(f"unknown component {component!r}")
    first = parse_utc(first_signal_at)
    plan = fanout.plan(registry, evidence, fanout_mode)  # validates products and tiers
    case = {
        "schema": "aldermoor.cra.art14-case/0.1",
        "id": case_id or "ART14-" + uuid.uuid4().hex[:8].upper(),
        "type": case_type,
        "title": title,
        "summary": summary,
        "component": component,
        "cve_id": cve_id,
        "euvd_id": None,
        "detection_source": detection_source,
        "first_signal_at": iso(first),
        "aware_at": None,
        "occurred_at": None,
        "suspected_malicious": None,
        "entity_incident": entity_incident,
        "state": "triage",
        "evidence": dict(evidence),
        "fanout": plan,
        "coordinator": routing.derive_coordinator(registry["manufacturer"], registry["coordinator_csirts"]).as_dict(),
        "notifications": [],
        "fixes": {},
        "user_notices": [],
        "upstream": [],
        "csirt_requests": [],
        "content": {},
        "decision_log": [],
    }
    _log(case, first, actor, "intake", "case_opened",
         f"First signal via {detection_source}; triage started (suspicion starts triage, not the clock; guidance para 213)")
    return case


def update_evidence(case: dict, registry: dict, evidence: dict[str, str], at: str, actor: str, role: str) -> dict:
    """Change product evidence tiers. Before awareness this re-plans; after, it can only add notifications."""
    t = parse_utc(at)
    merged = dict(case["evidence"])
    merged.update(evidence)
    plan = fanout.plan(registry, merged, case["fanout"]["mode"])
    if case["state"] != "triage":
        existing = {p for n in case["notifications"] for p in n["products"]}
        new_products = [p for p in plan["reportable"] if p not in existing]
        removed = [p for p in existing if p not in plan["reportable"]]
        if removed:
            raise CaseError(f"cannot withdraw products already notified: {removed}; file an update instead")
        if case["fanout"]["mode"] == "grouped" and new_products:
            raise CaseError("grouped notification: add products through an SRP update, not a new record")
        for pid in new_products:
            n = _new_notification(registry, f"N{len(case['notifications']) + 1}", [pid])
            case["notifications"].append(n)
        _recompute_state(case)
    case["evidence"] = merged
    case["fanout"] = plan if case["state"] == "triage" else {**plan, "notifications": [
        {"id": n["id"], "products": n["products"], "member_states": n["member_states"]} for n in case["notifications"]]}
    _log(case, t, actor, role, "evidence_updated", json.dumps(evidence, sort_keys=True))
    return case


def _new_notification(registry: dict, nid: str, products: list[str]) -> dict:
    by_id = {p["id"]: p for p in registry["products"]}
    ms = set()
    for pid in products:
        ms.update(fanout.member_states_for(by_id[pid], registry["eu27"]))
    return {"id": nid, "products": products, "member_states": sorted(ms, key=registry["eu27"].index),
            "srp_id": None, "submissions": {}, "updates": [], "legal_reviews": {}}


def declare_not_reportable(case: dict, registry: dict, at: str, actor: str, role: str, criterion: str,
                           rationale: str) -> dict:
    _require_state(case, "triage")
    if role not in registry["awareness_authority_roles"]:
        raise CaseError(f"role {role!r} cannot decide reportability; allowed: {registry['awareness_authority_roles']}")
    if criterion not in NOT_REPORTABLE_CRITERIA:
        raise CaseError(f"criterion must be one of {sorted(NOT_REPORTABLE_CRITERIA)}")
    if not rationale.strip():
        raise CaseError("a not-reportable decision needs a written rationale")
    t = parse_utc(at)
    case["state"] = "not_reportable"
    _log(case, t, actor, role, "not_reportable", rationale, criterion=NOT_REPORTABLE_CRITERIA[criterion])
    return case


def declare_awareness(case: dict, registry: dict, at: str, actor: str, role: str, rationale: str,
                      suspected_malicious: str | None = None, occurred_at: str | None = None) -> dict:
    """Start the statutory clocks. No approval step (corporate guide 07)."""
    _require_state(case, "triage")
    if role not in registry["awareness_authority_roles"]:
        raise CaseError(f"role {role!r} does not hold the awareness authority; allowed: "
                        f"{registry['awareness_authority_roles']}")
    t = parse_utc(at)
    if t < parse_utc(case["first_signal_at"]):
        raise CaseError("awareness cannot precede the first signal")
    if case["type"] == "severe_incident":
        if suspected_malicious not in ("Yes", "No", "Unknown"):
            raise CaseError("severe incident: suspected_malicious must be Yes, No or Unknown (Art 14(4)(a))")
    if not case["fanout"]["reportable"]:
        raise CaseError("no product is in Tier A or B; record a not-reportable decision instead")
    case["aware_at"] = iso(t)
    case["suspected_malicious"] = suspected_malicious
    case["occurred_at"] = iso(parse_utc(occurred_at)) if occurred_at else None
    case["notifications"] = [_new_notification(registry, n["id"], n["products"])
                             for n in case["fanout"]["notifications"]]
    comp = registry["components"].get(case["component"] or "", {})
    if comp.get("open_source"):
        case["upstream"].append({"component": case["component"], "maintainer": comp["maintainer"],
                                 "channel": comp.get("upstream_channel"), "done_at": None})
    case["state"] = "aware"
    _log(case, t, actor, role, "awareness_declared",
         f"{rationale} | Reasonable degree of certainty reached (guidance para 213). "
         f"Fan-out rule {case['fanout']['rule']} ({case['fanout']['mode']}): "
         f"{len(case['notifications'])} SRP notification(s) for {len(case['fanout']['reportable'])} product(s); "
         f"coordinator CSIRT {case['coordinator']['member_state']}.")
    return case


# --------------------------------------------------------------------------- filing

def _notification(case: dict, nid: str) -> dict:
    for n in case["notifications"]:
        if n["id"] == nid:
            return n
    raise CaseError(f"case {case['id']} has no notification {nid}")


def record_legal_review(case: dict, registry: dict, nid: str, stage: str, at: str, reviewer: str, role: str) -> dict:
    if stage not in ("notification", "final_report"):
        raise CaseError("legal review applies to the 72-hour notification and the final report only")
    if role not in registry["legal_reviewer_roles"]:
        raise CaseError(f"role {role!r} is not a legal reviewer role")
    n = _notification(case, nid)
    t = parse_utc(at)
    n["legal_reviews"][stage] = {"at": iso(t), "reviewer": reviewer}
    _log(case, t, reviewer, role, "legal_review", f"{nid} {stage} content reviewed")
    return case


def record_submission(case: dict, nid: str, stage: str, at: str, filed_by: str, checked_by: str,
                      srp_id: str | None = None, evidence_ref: str | None = None) -> dict:
    """Record a manual SRP web-form submission for one notification and stage."""
    if stage not in STAGES:
        raise CaseError(f"stage must be one of {STAGES}")
    if case["state"] in ("triage", "not_reportable", "closed"):
        raise CaseError(f"cannot file while case is '{case['state']}'")
    if not filed_by or not checked_by or filed_by.strip().lower() == checked_by.strip().lower():
        raise CaseError("four-eyes check: filer and checker must be two different named people")
    n = _notification(case, nid)
    if n["submissions"].get(stage):
        raise CaseError(f"{nid} {stage} already submitted; use an update")
    idx = STAGES.index(stage)
    if idx > 0 and not n["submissions"].get(STAGES[idx - 1]):
        raise CaseError(f"{nid}: {STAGES[idx - 1]} must be submitted before {stage} (one SRP record, tabs in order)")
    if stage in ("notification", "final_report") and stage not in n["legal_reviews"]:
        raise CaseError(f"{nid}: legal review of the {stage} is required before submission")
    if stage == "final_report" and case["type"] == "aev" and fix_available_at(case, n) is None:
        raise CaseError(f"{nid}: AEV final report needs the date a corrective or mitigating measure became available")
    if stage == "early_warning" and not srp_id:
        raise CaseError("record the SRP notification ID shown after the early warning is submitted")
    t = parse_utc(at)
    if t < parse_utc(case["aware_at"]):
        raise CaseError("submission cannot precede awareness")
    if srp_id:
        n["srp_id"] = srp_id
    n["submissions"][stage] = {"at": iso(t), "filed_by": filed_by, "checked_by": checked_by,
                               "evidence_ref": evidence_ref}
    _log(case, t, filed_by, "assigned_representative", f"srp_{stage}_submitted",
         f"{nid} ({', '.join(n['products'])}) SRP {n['srp_id']}; checked by {checked_by}", evidence=evidence_ref)
    _recompute_state(case)
    return case


def record_update(case: dict, nid: str, at: str, filed_by: str, checked_by: str, reason: str) -> dict:
    """Art 14(6) intermediate update (on CSIRT request) or a manufacturer-initiated update."""
    n = _notification(case, nid)
    if not n["submissions"].get("early_warning"):
        raise CaseError("an update needs an existing SRP record (early warning first)")
    if n["submissions"].get("final_report"):
        raise CaseError("the SRP record is frozen after the final report")
    if filed_by.strip().lower() == checked_by.strip().lower():
        raise CaseError("four-eyes check: filer and checker must differ")
    t = parse_utc(at)
    n["updates"].append({"at": iso(t), "filed_by": filed_by, "checked_by": checked_by, "reason": reason})
    for req in case["csirt_requests"]:
        if req["notification"] == nid and req["done_at"] is None:
            req["done_at"] = iso(t)
    _log(case, t, filed_by, "assigned_representative", "srp_update_submitted", f"{nid}: {reason}")
    return case


def record_csirt_request(case: dict, nid: str, at: str, respond_by: str, request: str) -> dict:
    _notification(case, nid)
    t = parse_utc(at)
    case["csirt_requests"].append({"notification": nid, "at": iso(t), "respond_by": iso(parse_utc(respond_by)),
                                   "request": request, "done_at": None})
    _log(case, t, "coordinator CSIRT", "csirt", "intermediate_update_requested", f"{nid}: {request} (Art 14(6))")
    return case


def record_fix(case: dict, product_id: str, at: str, description: str, actor: str = "Remediation lead") -> dict:
    if case["type"] != "aev":
        raise CaseError("fix dates drive the AEV final report; for incidents record mitigation in content")
    if product_id not in case["fanout"]["reportable"]:
        raise CaseError(f"{product_id} is not a reportable product in this case")
    t = parse_utc(at)
    case["fixes"][product_id] = {"at": iso(t), "description": description}
    _log(case, t, actor, "remediation_lead", "measure_available",
         f"{product_id}: {description} (AEV final report due 14 days after; Art 14(2)(c))")
    return case


def record_user_notice(case: dict, product_id: str, kind: str, at: str, channel: str, actor: str = "Communications") -> dict:
    if kind not in ("affected_users", "all_users", "machine_readable"):
        raise CaseError("kind must be affected_users, all_users or machine_readable")
    t = parse_utc(at)
    case["user_notices"].append({"product": product_id, "kind": kind, "at": iso(t), "channel": channel})
    _log(case, t, actor, "communications", "user_notice", f"{product_id}: {kind} via {channel} (Art 14(8))")
    return case


def record_upstream(case: dict, at: str, actor: str = "OSPO") -> dict:
    t = parse_utc(at)
    for u in case["upstream"]:
        u["done_at"] = iso(t)
    _log(case, t, actor, "ospo", "upstream_reported", "Reported to component maintainer and shared fix (Art 13(6))")
    return case


def set_content(case: dict, **fields) -> dict:
    case["content"].update({k: v for k, v in fields.items() if v is not None})
    return case


def close_case(case: dict, at: str, actor: str, role: str, review_ref: str) -> dict:
    _require_state(case, "final_filed")
    t = parse_utc(at)
    case["state"] = "closed"
    _log(case, t, actor, role, "case_closed", f"Post-incident review {review_ref}")
    return case


# --------------------------------------------------------------------------- deadlines and due items

def fix_available_at(case: dict, n: dict) -> datetime | None:
    """Per notification: the EARLIEST measure among its products (conservative for grouped records)."""
    dates = [parse_utc(case["fixes"][p]["at"]) for p in n["products"] if p in case["fixes"]]
    return min(dates) if dates else None


def deadlines(case: dict, n: dict) -> dict:
    if not case.get("aware_at"):
        return {}
    aware = parse_utc(case["aware_at"])
    sub = {s: parse_utc(v["at"]) for s, v in n["submissions"].items()}
    if case["type"] == "aev":
        final = clocks.aev_final_due(fix_available_at(case, n))
        final_basis = "Art 14(2)(c): 14 days after a corrective or mitigating measure is available"
    else:
        final = clocks.si_final_due(sub.get("notification"))
        final_basis = "Art 14(4)(c): one month after submission of the incident notification"
    return {
        "early_warning": (clocks.early_warning_due(aware), "Art 14(2)(a)/(4)(a): 24 h from awareness"),
        "notification": (clocks.notification_due(aware), "Art 14(2)(b)/(4)(b): 72 h from awareness"),
        "final_report": (final, final_basis),
        "srp_72h_counter": clocks.srp_72h_counter(sub.get("early_warning")),
    }


def due_items(case: dict, registry: dict, now: datetime) -> list[dict]:
    items: list[dict] = []
    if case["state"] in ("triage",):
        first = parse_utc(case["first_signal_at"])
        items.append(_item(case, "-", "Awareness decision (immediate assessment)", None, None, now,
                           "Guidance para 213: assess immediately; clock starts at reasonable certainty",
                           note=f"open {round((now - first).total_seconds() / 3600, 1)} h since first signal"))
        return items
    if case["state"] in ("not_reportable", "closed"):
        return items
    aware = parse_utc(case["aware_at"])
    by_id = {p["id"]: p for p in registry["products"]}
    for n in case["notifications"]:
        d = deadlines(case, n)
        for stage in STAGES:
            due, basis = d[stage]
            done = n["submissions"].get(stage, {}).get("at")
            note = None
            if stage == "notification" and d["srp_72h_counter"] and not done:
                note = f"SRP counter will show {fmt_utc(d['srp_72h_counter'])} (FAQ 26 quirk; statute governs)"
            if stage == "final_report" and due is None:
                note = ("awaiting corrective or mitigating measure" if case["type"] == "aev"
                        else "starts when the 72 h notification is submitted")
            items.append(_item(case, n["id"], f"SRP {stage.replace('_', ' ')}", due,
                               parse_utc(done) if done else None, now, basis, note=note, statutory=True))
        if "notification" not in n["legal_reviews"]:
            items.append(_item(case, n["id"], "Legal review of 72 h content",
                               aware + timedelta(hours=PACK_TARGETS["legal_review_72h_h"]), None, now,
                               "Pack target (corporate guide 07: legal reviews 72 h and final only)"))
        final_due = d["final_report"][0]
        if final_due and "final_report" not in n["legal_reviews"]:
            items.append(_item(case, n["id"], "Legal review of final report",
                               final_due - timedelta(hours=PACK_TARGETS["legal_review_final_before_due_h"]), None,
                               now, "Pack target"))
        for pid in n["products"]:
            notices = {u["kind"] for u in case["user_notices"] if u["product"] == pid}
            if "affected_users" not in notices:
                items.append(_item(case, n["id"], f"User notice, impacted users: {by_id[pid]['name']}",
                                   aware + timedelta(hours=PACK_TARGETS["affected_user_notice_h"]), None, now,
                                   "Art 14(8) 'without undue delay'; time is a pack target"))
            fix = case["fixes"].get(pid)
            if fix and "all_users" not in notices:
                items.append(_item(case, n["id"], f"User notice, all users and CSAF: {by_id[pid]['name']}",
                                   parse_utc(fix["at"]) + timedelta(hours=PACK_TARGETS["all_users_notice_after_fix_h"]),
                                   None, now, "Art 14(8) 'where appropriate, all users'; guidance paras 219-221; time is a pack target"))
    for u in case["upstream"]:
        if not u["done_at"]:
            items.append(_item(case, "-", f"Upstream report and fix sharing: {u['maintainer']}",
                               aware + timedelta(hours=PACK_TARGETS["upstream_report_h"]), None, now,
                               "Art 13(6); guidance section 9.2.1; time is a pack target"))
    nis2 = case["type"] == "severe_incident" and (case.get("entity_incident") or any(
        by_id[p].get("rdps_on_aldermoor_cloud") for p in case["fanout"]["reportable"]))
    if nis2 and not any(e["action"] == "nis2_assessed" for e in case["decision_log"]):
        items.append(_item(case, "-", "Multi-regime cell: NIS2 Art 23 assessment for Aldermoor Cloud",
                           aware + timedelta(hours=PACK_TARGETS["nis2_assessment_h"]), None, now,
                           "Separate NIS2 filing today (KB 09-reporting.md 'Multiple regimes'); time is a pack target"))
    for r in case["csirt_requests"]:
        if not r["done_at"]:
            items.append(_item(case, r["notification"], f"Intermediate update requested: {r['request']}",
                               parse_utc(r["respond_by"]), None, now, "Art 14(6)", statutory=True))
    return items


def _item(case, nid, what, due, done, now, basis, note=None, statutory=False):
    st = clocks.status(due, done, now)
    if st == "overdue" and not statutory:
        st = "past-target"  # pack targets are internal SLAs, not legal deadlines
    return {"case": case["id"], "notification": nid, "item": what, "due_at": due, "done_at": done,
            "status": st, "basis": basis, "note": note, "statutory": statutory}


def log_nis2_assessment(case: dict, at: str, actor: str, outcome: str) -> dict:
    _log(case, parse_utc(at), actor, "nis2_owner", "nis2_assessed", outcome)
    return case


def timeline(case: dict) -> list[dict]:
    return sorted(case["decision_log"], key=lambda e: e["at"])
