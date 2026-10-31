"""Client intake validation for the re-skin pipeline.

validate(intake) -> (errors, warnings). Errors stop the build; warnings are printed.
"""
import datetime as dt
import re

VALID_CLASSES = ("Default", "Default (provisional)", "Class I", "Class II", "Critical")
NB_CLASSES = ("Class I", "Class II", "Critical")
DATE_FMT = "%d %b %Y"  # e.g. 11 Dec 2027
QUESTIONS_PER_DOMAIN = 4
DOMAINS = ["D%d" % i for i in range(1, 11)]
QIDS = [f"Q{i}.{j}" for i in range(1, 11) for j in range(1, 5)]
REQUIRED = {
    "engagement": ["client_name", "programme_codename", "advisor", "classification_label", "pack_date", "facts_as_at",
                   "board_date", "steerco_1", "kickoff", "knowledge_base_url"],
    "storyline": ["governing_thought", "scqa", "pillars"],
    "client": ["disclaimer", "hq", "employees", "engineers", "suppliers_in_scope", "installed_base_m", "existing_assurance",
               "saas", "business_units", "product_families", "legacy_lines"],
    "exposure": ["legacy_decision"],
    "diagnostic": ["baseline_date", "baseline_label", "targets"],
    "cost_model": ["assumptions", "scenarios", "phasing", "actual_to_date"],
    "programme": ["overall_rag", "overall_status", "phases", "waves", "milestones", "workstreams", "mobilisation_plan",
                  "kpis", "trajectories", "risks", "issues", "decisions", "stakeholders"],
}
FAMILY_KEYS = ["id", "name", "bu", "cra_class", "annex_item", "revenue_m", "skus", "wave", "route",
               "support_period_years", "rdps", "description"]
ASSUMPTION_KEYS = ["fte_cost_programme", "fte_cost_psirt", "fte_cost_engineering", "programme_team_fte", "programme_team_run_fte",
                   "psirt_incremental_fte", "psirt_oncall_allowance", "remediation_fte_years", "remediation_phasing",
                   "platforms_build", "platforms_phasing", "platforms_run", "risk_assessment_per_family",
                   "testing_per_family_per_year", "documentation_per_family", "documentation_run_per_family",
                   "nb_pre_assessments", "nb_module_b_examinations", "nb_module_h", "nb_surveillance_run", "training",
                   "legal", "supplier_programme", "contingency_rate"]


class IntakeError(ValueError):
    def __init__(self, path, errors):
        self.errors = errors
        super().__init__(f"Intake {path} has {len(errors)} problem(s):\n" + "\n".join(f"  - {e}" for e in errors))


def _num(x):
    return isinstance(x, (int, float)) and not isinstance(x, bool)


def _date_ok(s):
    if isinstance(s, dt.date):
        return True
    try:
        dt.datetime.strptime(str(s), DATE_FMT)
        return True
    except ValueError:
        return False


def validate(I):
    E, W = [], []
    if not isinstance(I, dict):
        return ["the intake is not a YAML mapping"], W
    for sec, keys in REQUIRED.items():
        if not isinstance(I.get(sec), dict):
            E.append(f"missing section '{sec}'")
            continue
        for k in keys:
            if k not in I[sec] or I[sec][k] is None:
                E.append(f"{sec}.{k} is required")
    if E:
        return E, W  # structure is broken; deeper checks would only add noise

    eng, cl, dg, cm, pg = I["engagement"], I["client"], I["diagnostic"], I["cost_model"], I["programme"]
    for k in ("pack_date", "facts_as_at", "board_date", "steerco_1"):
        if not isinstance(eng[k], dt.date):
            E.append(f"engagement.{k} must be an ISO date (YYYY-MM-DD), got {eng[k]!r}")
    if not _date_ok(eng["kickoff"]):
        E.append(f"engagement.kickoff must look like '5 Oct 2026', got {eng['kickoff']!r}")
    if isinstance(eng.get("pack_date"), dt.date) and eng["pack_date"] >= dt.date(2027, 12, 11):
        E.append("engagement.pack_date must be before full application (11 Dec 2027)")
    if not isinstance(dg["baseline_date"], dt.date):
        E.append(f"diagnostic.baseline_date must be an ISO date (YYYY-MM-DD), got {dg['baseline_date']!r}")

    # business units
    bus = cl["business_units"] or []
    bu_ids = []
    for i, b in enumerate(bus):
        for k in ("id", "name", "revenue_m", "eu_share", "profile"):
            if k not in b:
                E.append(f"client.business_units[{i}] is missing '{k}'")
        bu_ids.append(b.get("id"))
        if "revenue_m" in b and (not _num(b["revenue_m"]) or b["revenue_m"] <= 0):
            E.append(f"business unit {b.get('id')}: revenue_m must be a positive number (EUR m), got {b['revenue_m']!r}")
        if "eu_share" in b and (not _num(b["eu_share"]) or not 0 <= b["eu_share"] <= 1):
            E.append(f"business unit {b.get('id')}: eu_share must be a fraction between 0 and 1, got {b['eu_share']!r}")
    if not bus:
        E.append("client.business_units must list at least one business unit")
    _dups(bu_ids, "business unit id", E)

    # families
    fams = cl["product_families"] or []
    if not fams:
        E.append("client.product_families must list at least one family")
    fam_ids = []
    for i, f in enumerate(fams):
        fid = f.get("id", f"#{i}")
        fam_ids.append(fid)
        for k in FAMILY_KEYS:
            if k not in f:
                E.append(f"family {fid}: missing '{k}'")
        if f.get("bu") not in bu_ids:
            E.append(f"family {fid}: business unit {f.get('bu')!r} is not in client.business_units ({', '.join(map(str, bu_ids))})")
        cls = f.get("cra_class")
        if cls not in VALID_CLASSES:
            E.append(f"family {fid}: cra_class {cls!r} is not one of {', '.join(VALID_CLASSES)}")
        if "revenue_m" in f and (not _num(f["revenue_m"]) or f["revenue_m"] < 0):
            E.append(f"family {fid}: revenue_m must be a number >= 0 (EUR m)")
        if "skus" in f and (not isinstance(f["skus"], int) or f["skus"] < 1):
            E.append(f"family {fid}: skus must be a whole number >= 1")
        sp = f.get("support_period_years")
        if sp is not None and (not _num(sp) or not 1 <= sp <= 30):
            E.append(f"family {fid}: support_period_years must be between 1 and 30")
        elif _num(sp) and sp < 5:
            W.append(f"family {fid}: support period {sp} years is under the five-year floor of Art 13(8); record why")
        route = str(f.get("route", ""))
        if cls in NB_CLASSES and route.startswith("Module A"):
            W.append(f"family {fid}: {cls} on {route!r}; Module A needs a cited harmonised standard (none cited at 30 Oct 2026)")
        if not route.startswith(("Module A", "Module B+C", "Module H")):
            E.append(f"family {fid}: route {route!r} must start with 'Module A', 'Module B+C' or 'Module H'")
        if cls in NB_CLASSES and not re.search(r"Annex\s+(III|IV)", str(f.get("annex_item", ""))):
            W.append(f"family {fid}: {cls} family without an 'Annex III ... item N' / 'Annex IV item N' reference; the classifier cannot map it")
        if not str(f.get("wave", "")).startswith(("Wave 1", "Wave 2")):
            W.append(f"family {fid}: wave {f.get('wave')!r} does not start with 'Wave 1' or 'Wave 2'; the diagnostic groups it as 'Not assigned'")
    _dups(fam_ids, "product family id", E)
    rev_by_bu = {}
    for f in fams:
        if _num(f.get("revenue_m")):
            rev_by_bu[f.get("bu")] = rev_by_bu.get(f.get("bu"), 0) + f["revenue_m"]
    for b in bus:
        if _num(b.get("revenue_m")) and rev_by_bu.get(b.get("id"), 0) > b["revenue_m"] + 1e-9:
            E.append(f"business unit {b.get('id')}: family revenue ({rev_by_bu[b['id']]}) exceeds BU revenue ({b['revenue_m']})")

    leg_ids = []
    for i, l in enumerate(cl["legacy_lines"] or []):
        leg_ids.append(l.get("id", f"#{i}"))
        for k in ("id", "name", "bu", "status", "units_in_field_k", "still_sold_after_dec_2027", "eu_revenue_m"):
            if k not in l:
                E.append(f"legacy line {l.get('id', i)}: missing '{k}'")
        if l.get("bu") not in bu_ids:
            E.append(f"legacy line {l.get('id')}: business unit {l.get('bu')!r} is not in client.business_units")
    _dups(fam_ids + leg_ids, "family/legacy id", E)
    saas = cl["saas"] or {}
    if not _num(saas.get("revenue_m")) or saas.get("revenue_m", 0) < 0:
        E.append("client.saas.revenue_m must be a number >= 0 (use 0 when the client has no SaaS)")
    elif saas.get("revenue_m") and saas.get("bu") not in bu_ids:
        E.append(f"client.saas.bu {saas.get('bu')!r} is not in client.business_units")
    for k in ("employees", "engineers", "suppliers_in_scope", "installed_base_m"):
        if not _num(cl[k]) or cl[k] < 0:
            E.append(f"client.{k} must be a number >= 0")
    if _num(cl["employees"]) and _num(cl["engineers"]) and cl["engineers"] > cl["employees"]:
        E.append("client.engineers cannot exceed client.employees")

    ld = I["exposure"]["legacy_decision"] or {}
    for lid in ld.get("lines") or []:
        if lid not in leg_ids:
            E.append(f"exposure.legacy_decision.lines: {lid!r} is not a legacy line id")
    for k in ("eu_revenue_m", "remediation_cost_estimate_m", "recommendation"):
        if k not in ld:
            E.append(f"exposure.legacy_decision.{k} is required")

    # diagnostic
    t = dg["targets"] or {}
    for k in ("by_jun_2027", "by_nov_2027"):
        if not _num(t.get(k)) or not 0 < t[k] <= 1:
            E.append(f"diagnostic.targets.{k} must be a fraction between 0 and 1")
    scores, gen = dg.get("scores") or {}, dg.get("generator")
    for fid, sc in scores.items():
        if fid not in fam_ids:
            E.append(f"diagnostic.scores: {fid!r} is not a product family id")
            continue
        missing = [q for q in QIDS if q not in (sc or {})]
        if missing:
            E.append(f"diagnostic.scores.{fid}: missing {len(missing)} question(s), e.g. {', '.join(missing[:4])}")
        bad = [q for q, v in (sc or {}).items() if not isinstance(v, int) or not 0 <= v <= 4]
        if bad:
            E.append(f"diagnostic.scores.{fid}: scores must be whole numbers 0-4 ({', '.join(bad[:4])})")
    unscored = [f for f in fam_ids if f not in scores]
    if unscored and not gen:
        E.append(f"diagnostic: families {', '.join(map(str, unscored))} have no explicit scores and there is no diagnostic.generator")
    if gen:
        for b in (gen.get("bu_base") or {}):
            if b not in bu_ids:
                E.append(f"diagnostic.generator.bu_base: {b!r} is not a business unit id")
        for b, row in (gen.get("bu_base") or {}).items():
            for d, v in (row or {}).items():
                if d not in DOMAINS or not _num(v) or not 0 <= v <= 4:
                    E.append(f"diagnostic.generator.bu_base.{b}.{d}: domain must be D1-D10 and level 0-4")
        for f in (gen.get("family_adjust") or {}):
            if f not in fam_ids:
                E.append(f"diagnostic.generator.family_adjust: {f!r} is not a product family id")
        for d, offs in (gen.get("question_offset") or {}).items():
            if d not in DOMAINS or not isinstance(offs, list) or len(offs) != QUESTIONS_PER_DOMAIN:
                E.append(f"diagnostic.generator.question_offset.{d}: needs a list of 4 offsets")
        for d, vals in (gen.get("fixed") or {}).items():
            if d not in DOMAINS or not isinstance(vals, list) or len(vals) != QUESTIONS_PER_DOMAIN:
                E.append(f"diagnostic.generator.fixed.{d}: needs a list of 4 levels (null = take d8_q4_by_bu)")
        for b in (gen.get("d8_q4_by_bu") or {}):
            if b not in bu_ids:
                E.append(f"diagnostic.generator.d8_q4_by_bu: {b!r} is not a business unit id")

    # cost model
    A = cm["assumptions"] or {}
    for k in ASSUMPTION_KEYS:
        if k not in A:
            E.append(f"cost_model.assumptions.{k} is required")
    if _num(A.get("contingency_rate")) and not 0 <= A["contingency_rate"] <= 0.5:
        E.append("cost_model.assumptions.contingency_rate must be between 0 and 0.5")
    for k in ("remediation_phasing", "platforms_phasing", "risk_assessment_phasing"):
        ph = A.get(k)
        if isinstance(ph, dict) and _num(ph.get("q4_2026")) and _num(ph.get("y2027")) and abs(ph["q4_2026"] + ph["y2027"] - 1) > 0.001:
            E.append(f"cost_model.assumptions.{k}: q4_2026 + y2027 must equal 1")
    for k, v in A.items():
        if _num(v) and v < 0:
            E.append(f"cost_model.assumptions.{k} must not be negative")
    if "base" not in (cm["scenarios"] or {}):
        E.append("cost_model.scenarios.base is required")
    for k, s in (cm["scenarios"] or {}).items():
        for kk in ("label", "description", "multipliers", "contingency"):
            if kk not in (s or {}):
                E.append(f"cost_model.scenarios.{k}.{kk} is required (multipliers may be {{}})")
    ph = cm["phasing"] or {}
    if len(ph.get("q4_2026_monthly_weights") or []) != 3:
        E.append("cost_model.phasing.q4_2026_monthly_weights needs 3 weights (Oct, Nov, Dec 2026)")
    elif abs(sum(ph["q4_2026_monthly_weights"]) - 1) > 0.001:
        E.append("cost_model.phasing.q4_2026_monthly_weights must sum to 1")
    if len(ph.get("y2027_monthly_weights") or []) != 12:
        E.append("cost_model.phasing.y2027_monthly_weights needs 12 weights (Jan-Dec 2027)")
    if not _num((cm["actual_to_date"] or {}).get("actual")):
        E.append("cost_model.actual_to_date.actual must be a number (EUR)")

    # programme
    ws_ids = [w.get("id") for w in pg["workstreams"] or []]
    _dups(ws_ids, "workstream id", E)
    for p in pg["phases"] or []:
        for k in ("id", "name", "start", "end", "status", "gate"):
            if k not in p:
                E.append(f"phase {p.get('id')}: missing '{k}'")
        if not _date_ok(p.get("start")):
            E.append(f"phase {p.get('id')}: start {p.get('start')!r} must look like '2 Nov 2026'")
    wave_members = []
    for w in pg["waves"] or []:
        for m in w.get("families") or []:
            wave_members.append(m)
            if m not in fam_ids and m not in leg_ids:
                E.append(f"wave {w.get('id')}: {m!r} is neither a product family nor a legacy line id")
    for f in fam_ids:
        if f not in wave_members:
            W.append(f"family {f} is not in any programme wave")
    _dups(wave_members, "wave member", E)
    for m in pg["milestones"] or []:
        if not _date_ok(m.get("date")):
            E.append(f"milestone {m.get('id')}: date {m.get('date')!r} must look like '19 Nov 2026'")
    task_ids = [t.get("id") for t in pg["mobilisation_plan"] or []]
    _dups(task_ids, "task id", E)
    for t in pg["mobilisation_plan"] or []:
        if t.get("workstream") not in ws_ids:
            E.append(f"task {t.get('id')}: workstream {t.get('workstream')!r} is not a workstream id")
        for d in [x.strip() for x in str(t.get("depends_on") or "").split(",") if x.strip()]:
            if d not in task_ids:
                E.append(f"task {t.get('id')}: depends_on {d!r} is not a task id")
        for k in ("start", "end"):
            if not _date_ok(t.get(k)):
                E.append(f"task {t.get('id')}: {k} {t.get(k)!r} must look like '2 Nov 2026'")
        if _date_ok(t.get("start")) and _date_ok(t.get("end")) and \
                dt.datetime.strptime(str(t["end"]), DATE_FMT) < dt.datetime.strptime(str(t["start"]), DATE_FMT):
            E.append(f"task {t.get('id')}: ends before it starts")
    for k in pg["kpis"] or []:
        for kk in ("id", "name", "value", "display", "target", "rag", "trend", "source"):
            if kk not in k:
                E.append(f"kpi {k.get('id')}: missing '{kk}'")
        v = k.get("value")
        if isinstance(v, str) and v.startswith("auto:") and v not in ("auto:readiness_index", "auto:spend_vs_plan"):
            E.append(f"kpi {k.get('id')}: unknown auto value {v!r} (use auto:readiness_index or auto:spend_vs_plan)")
    tr = pg["trajectories"] or {}
    if len(tr.get("readiness_months") or []) != len(tr.get("readiness_weights") or []):
        E.append("programme.trajectories: readiness_months and readiness_weights must have the same length")
    if not _num(tr.get("readiness_end")) or not 0 < tr["readiness_end"] <= 1:
        E.append("programme.trajectories.readiness_end must be a fraction between 0 and 1")
    for k in ("sbom_coverage", "note"):
        if k not in tr:
            E.append(f"programme.trajectories.{k} is required")
    for r in pg["risks"] or []:
        for kk in ("likelihood", "impact"):
            if not isinstance(r.get(kk), int) or not 1 <= r[kk] <= 5:
                E.append(f"risk {r.get('id')}: {kk} must be a whole number 1-5")
    dec = pg["decisions"] or {}
    for k in ("steerco_1", "board"):
        if not isinstance(dec.get(k), list):
            E.append(f"programme.decisions.{k} must be a list")
    for s in pg["stakeholders"] or []:
        for kk in ("power", "interest"):
            if not isinstance(s.get(kk), int) or not 1 <= s[kk] <= 5:
                E.append(f"stakeholder {s.get('id')}: {kk} must be a whole number 1-5")

    # flow-style YAML pitfall: an unquoted comma inside {a: b, c} silently creates extra keys with no value
    for sec in ("phases", "milestones", "workstreams", "mobilisation_plan", "kpis", "risks", "issues", "stakeholders"):
        for x in pg.get(sec) or []:
            stray = [k for k, v in (x or {}).items() if v is None and k not in ("depends_on",)]
            if stray:
                E.append(f"programme.{sec} {x.get('id')}: keys with no value {stray} — quote any text that contains a comma or ': '")
    for f in fams:
        stray = [k for k, v in f.items() if v is None]
        if stray:
            E.append(f"family {f.get('id')}: keys with no value {stray} — quote text that contains a comma or ': '")

    # classifier presets (optional)
    for p in ((I.get("classifier") or {}).get("presets") or []):
        fid = p if isinstance(p, str) else (p or {}).get("family")
        if fid not in fam_ids:
            E.append(f"classifier.presets: {fid!r} is not a product family id")
    return E, W


def _dups(ids, what, E):
    seen = set()
    for i in ids:
        if i in seen:
            E.append(f"duplicate {what} {i!r}")
        seen.add(i)
