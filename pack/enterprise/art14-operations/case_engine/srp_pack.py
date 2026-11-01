"""SRP submission pack: field-by-field content for manual web-form entry.

The ENISA SRP is a web form with no API (ENISA SRP FAQ 15: "no Application
Programming Interface (API) will be provided at the initial release of the
SRP"; FAQ page updated 15 Oct 2026). It is English only (FAQ 24). So the pack
produces (1) a copy-ready text sheet in the glossary's field order with
requirement levels, character counts and gaps, and (2) a JSON export in an
internal schema that can be mapped to an API if ENISA ever publishes one.
The JSON schema name is Aldermoor's own; it is not an ENISA format.
"""
from __future__ import annotations

import json

from . import engine
from .clocks import fmt_utc, parse_utc

EXPORT_SCHEMA = "aldermoor.cra.srp-submission/0.1 (internal; not an ENISA format)"


def _product_lines(case: dict, registry: dict, n: dict) -> tuple[str, str, str, str]:
    by_id = {p["id"]: p for p in registry["products"]}
    names = "; ".join(f"{by_id[p]['name']} - {by_id[p]['affected_versions']}" for p in n["products"])
    classes = "; ".join(f"{by_id[p]['name']}: {by_id[p]['class']}" for p in n["products"])
    eos = "Yes" if any(by_id[p].get("support_status") == "end_of_support" for p in n["products"]) else "No"
    comp = registry["components"].get(case.get("component") or "", {}).get("name", "")
    return names, classes, eos, comp


def build(case: dict, registry: dict, nid: str, stage: str, fields_def: dict | None = None) -> dict:
    if stage not in engine.STAGES:
        raise engine.CaseError(f"stage must be one of {engine.STAGES}")
    if not case.get("aware_at"):
        raise engine.CaseError("no awareness declared; nothing to file")
    fields_def = fields_def or engine.load_fields()
    n = engine._notification(case, nid)
    c = case["content"]
    names, classes, eos, comp = _product_lines(case, registry, n)
    total = len(case["notifications"])
    xref = f"[{case['id']} {n['id']}/{total}]"
    fix = engine.fix_available_at(case, n)
    is_aev = case["type"] == "aev"
    values = {
        "notification_type": "Actively exploited vulnerability" if is_aev else "Severe incident having an impact on the security of the product",
        "title": f"{xref} {case['title']}",
        "summary": (case["summary"] or "") + (
            f" This vulnerability affects {total} Aldermoor products notified as separate records under "
            f"case {case['id']} (records N1-N{total})." if total > 1 else ""),
        "manufacturer_name": registry["manufacturer"]["eu_manufacturer_entity"] + " (system-generated from association)",
        "member_states": ", ".join(n["member_states"]),
        "product_name_version": names,
        "product_class": classes,
        "end_of_support": eos,
        "component_name": comp,
        "aware_at": fmt_utc(parse_utc(case["aware_at"])),
        "occurred_at": fmt_utc(parse_utc(case["occurred_at"])) + " (estimate)" if case.get("occurred_at") else "",
        "suspected_malicious": case.get("suspected_malicious") or "",
        "cve_id": case.get("cve_id") or "",
        "euvd_id": case.get("euvd_id") or "",
        "general_information": c.get("general_information", ""),
        "general_information_incident": c.get("general_information", ""),
        "initial_assessment": c.get("initial_assessment", ""),
        "mitigation_expected_shortly": c.get("mitigation_expected_shortly", ""),
        "user_action": c.get("user_action", ""),
        "measures_taken": c.get("measures_taken", ""),
        "measures_users": c.get("measures_users", ""),
        "sensitivity": c.get("sensitivity", ""),
        "attack_vector": c.get("attack_vector", ""),
        "pec_indicator": c.get("pec_indicator", "No"),
        "pec_reason": c.get("pec_reason", ""),
        "fix_available_at": fmt_utc(fix) if fix else "",
        "security_update_details": c.get("security_update_details", ""),
        "severity_impact": c.get("severity_impact", ""),
        "severity_impact_incident": c.get("severity_impact", ""),
        "malicious_actor": c.get("malicious_actor", "unknown") or "unknown",
        "applied_mitigation": c.get("applied_mitigation", ""),
        "root_cause": c.get("root_cause", ""),
        "ar_note": f"Internal case {case['id']} record {n['id']}; coordinator CSIRT {case['coordinator']['member_state']}.",
    }
    rows, gaps, errors = [], [], []
    for f in fields_def["fields"]:
        if f["applies"] not in ("both", case["type"]):
            continue
        level = f["levels"].get(stage, "-")
        if level == "-":
            continue
        v = values.get(f["key"], "")
        if f["key"] == "pec_indicator" and not (is_aev and stage == "notification"):
            continue
        if f.get("allowed") and v and v not in f["allowed"]:
            errors.append(f"{f['label']}: value {v!r} not in {f['allowed']}")
        if f.get("max_len") and len(v) > f["max_len"]:
            errors.append(f"{f['label']}: {len(v)} characters exceeds {f['max_len']}")
        if level in ("M", "R") and not v:
            gaps.append(f["label"])
        rows.append({"key": f["key"], "label": f["label"], "level": level, "value": v, "chars": len(v),
                     "max_len": f.get("max_len")})
    d = engine.deadlines(case, n)[stage]
    return {
        "schema": EXPORT_SCHEMA,
        "case_id": case["id"],
        "notification": n["id"],
        "srp_id": n.get("srp_id"),
        "stage": stage,
        "coordinator_csirt": case["coordinator"],
        "statutory_due": fmt_utc(d[0]) if d[0] else None,
        "statutory_basis": d[1],
        "fields": rows,
        "gaps": gaps,
        "errors": errors,
        "ready": not gaps and not errors,
        "checklist": [
            "Filer logs in with personal EU Login and MFA (no shared or corporate account).",
            "Correct manufacturer association and coordinator CSIRT selected (wrong CSIRT may invalidate; FAQ 18).",
            "Enter fields in order; paste from this sheet only; English only.",
            "Checker (second person) compares every field on screen against this sheet before submit.",
            "Capture evidence: full-page screenshot or PDF of the submitted tab and the confirmation; store under the case.",
            "Record the SRP notification ID and the submission time (UTC) in the case engine immediately.",
            "Do not wait for the SRP counter; the statutory clock runs from awareness (FAQ 26 quirk).",
        ],
    }


def render_text(pack: dict) -> str:
    out = [f"SRP SUBMISSION PACK  {pack['case_id']} / {pack['notification']}  stage: {pack['stage']}",
           f"Coordinator CSIRT: {pack['coordinator_csirt']['member_state']} - {pack['coordinator_csirt']['csirt_name']}",
           f"Statutory due: {pack['statutory_due'] or 'not yet triggered'}  ({pack['statutory_basis']})",
           f"SRP record: {pack['srp_id'] or 'new record'}",
           f"Status: {'READY' if pack['ready'] else 'NOT READY'}", ""]
    for i, r in enumerate(pack["fields"], 1):
        lim = f"/{r['max_len']}" if r["max_len"] else ""
        out.append(f"{i:>2}. [{r['level']}] {r['label']}  ({r['chars']}{lim} chars)")
        out.append("    " + (r["value"] if r["value"] else "<<EMPTY>>"))
    if pack["gaps"]:
        out += ["", "GAPS (required, empty): " + "; ".join(pack["gaps"])]
    if pack["errors"]:
        out += ["", "ERRORS: " + "; ".join(pack["errors"])]
    out += ["", "Filing checklist:"] + [f"  [ ] {c}" for c in pack["checklist"]]
    return "\n".join(out)


def render_json(pack: dict) -> str:
    return json.dumps(pack, indent=2)
