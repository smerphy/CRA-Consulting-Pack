"""D10 — CRA Business Case and Cost Model, built from pack_data.json (openpyxl).

Generated layout and formulas follow the v1.0 workbook; every client-specific value is read from pack_data
through Ctx (context.py). Call build(pack_data_path, out_dir) -> [Path].
"""
import datetime as dt
import json
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.styles import Alignment, Border, Font
from openpyxl.worksheet.pagebreak import Break

from . import common as _common
from .common import *  # noqa: F401,F403
from .context import Ctx, Words, eur_m0, join, pdate, plan_class, words

TITLE = "CRA Business Case and Cost Model"


def output_name(D):
    return f"{D['meta']['programme_codename']} - {TITLE}.xlsx"


def build(pack_data_path, out_dir):
    """Write the D10 workbook (formulas only, no cached values) and return [path]."""
    pack_data_path = Path(pack_data_path)
    D = json.loads(pack_data_path.read_text(encoding="utf-8"))
    out = Path(out_dir) / output_name(D)
    out.parent.mkdir(parents=True, exist_ok=True)
    _build(D, Ctx(D, pack_data_path), out)
    return [out]


def _build(D, X, OUT):

    _common.set_footer(X)
    CM = D["cost_model"]
    A = CM["assumptions"]
    CL = D["client"]
    HDR = f"{X.codename} · CRA Business Case and Cost Model {X.v}"
    LABEL = f"{X.CODENAME} · CRA BUSINESS CASE AND COST MODEL"

    # ---- client narrative derived from pack_data (no client strings in code) ----
    PROV = X.prov_fams
    NPROV = len(PROV)
    NB_N = len(X.nb_fams)
    LEGAL_TASK = X.task_id(lambda s: "legal opinion" in s)
    CLASS_ISSUE = X.issue_id(lambda s: "classif" in s)
    LEGAL_DUE = X.task_end(LEGAL_TASK) or X.issues.get(CLASS_ISSUE, {}).get("due", "")
    STRICT_SD = X.decision_id(lambda s: "legal opinion" in s, prefix="SD")
    NB_BD = X.decision_id(lambda s: "notified-body" in s or "notified body" in s, prefix="BD")
    INVEST_BD = X.decision_id(lambda s: "investment" in s or "budget" in s, prefix="BD")
    LEG_BD = (X.decision_id(lambda s: any(X.label(l).lower() in s for l in X.legacy_sold), prefix="BD")
              if X.legacy_sold else "")
    PILOT = X.short(X.pilot_fams[0]) if X.pilot_fams else "pilot"
    P3, P4 = X.phase("P3") or {}, X.phase("P4") or {}
    REV_TXT = f"{round(CL['revenue_m']):,}"
    NBPRE = A["nb_pre_assessments"]
    NBB = A["nb_module_b_examinations"]
    NBB_NOTE = NBB.get("note") or join(X.shorts(X.fams_by_route("Module B")))
    NBB_SHORT = NBB_NOTE.replace(" types", "").replace(" type", "")
    MODH = X.module_h_scope()
    MODH_BU = X.module_h_bu()
    LVL = {"cont": (0.10, 0.15, 0.20), "pfte": (5, 5, 6)}
    CLASS2 = X.fams_by_class("Class II")
    CRIT = X.fams_by_class("Critical")
    NB_CLASSES = sorted({plan_class(f) for f in X.nb_fams})
    NB_CLASS_TXT = "Class I and II" if NB_CLASSES == ["Class I", "Class II"] else join(NB_CLASSES)
    DEF_RI = [D["diagnostic"]["family_readiness_index"].get(f["id"]) for f in X.fams_by_class("Default")]
    DEF_RI = [v for v in DEF_RI if v is not None] or [0]
    PROV_SHORTS = join(X.shorts(PROV))
    PROV_LABELS = join(X.labels(PROV, sort=True))
    PROV_LABELS_C = ", ".join(X.labels(PROV, sort=True))
    if NPROV == 0:
        PORT_NOTE = ("EU revenue = revenue x BU EU share. Switch a family's planning class to test the cost and "
                     "exposure impact. Illustrative.")
    else:
        PORT_NOTE = (f"EU revenue = revenue x BU EU share. {PROV_SHORTS} {'are' if NPROV > 1 else 'is'} costed as Default "
                     f"pending the legal opinion (due {LEGAL_DUE}); switch {'their' if NPROV > 1 else 'its'} planning class "
                     f"to test the cost and exposure impact. Illustrative.")
    BOTH = "both are" if NPROV == 2 else ("it is" if NPROV == 1 else "all are")
    SENS_REFS = "; ".join(x for x in ([f"issue {CLASS_ISSUE}"] if CLASS_ISSUE else []) +
                          ([f"SteerCo decision {STRICT_SD}"] if STRICT_SD else []))
    SENS_TXT = f"Derived sensitivity: legal opinion due {LEGAL_DUE}" + (f" ({SENS_REFS})" if SENS_REFS else "")
    LEG = X.legacy_sold
    NLEG = len(LEG)
    LEG_REC = D["exposure"]["legacy_decision"]
    LEG_VERB = (LEG_REC.get("recommendation", "").split() or ["decide"])[0].lower()
    wb = Workbook()
    ws_cover = wb.active
    ws_cover.title = "Cover"
    ws_sum = wb.create_sheet("Summary")
    ws_in = wb.create_sheet("Inputs")
    ws_cb = wb.create_sheet("Cost build")
    ws_sc = wb.create_sheet("Scenarios")
    ws_ex = wb.create_sheet("Exposure")
    ws_mp = wb.create_sheet("Monthly plan")
    ws_bm = wb.create_sheet("Benchmarks")
    ws_al = wb.create_sheet("Assumptions log")

    IN = {}      # key -> absolute reference on Inputs
    INROW = {}   # key -> row on Inputs
    REFID = {}   # key -> assumption ref code (A01...)

    # =====================================================================================
    # INPUTS
    # =====================================================================================
    ws = ws_in
    widths(ws, {"A": 2.5, "B": 8, "C": 50, "D": 14, "E": 16, "F": 14, "G": 14, "H": 13, "I": 11, "J": 13,
                "K": 13, "L": 11, "M": 13, "N": 15})
    title_block(ws, LABEL + " · INPUTS",
                "Every assumption sits in one labelled blue cell: change these, never the calculations",
                f"EUR, real 2026 terms, excl. VAT · {X.engagement} · "
                f"Source: pack_data.json {X.v} (cost_model, client) unless stated", link_col="N")

    band(ws, 5, "Scenario selector", "B", "N")
    put(ws, "B6", "SEL", kind="muted")
    put(ws, "C6", "Active scenario (drives Cost build, Summary and Monthly plan)", kind="label", bold=True)
    put(ws, "D6", "Base", kind="input", bold=True, align="center", border=B_BOX)
    add_list_dv(ws, "D6", '"Low,Base,High"', prompt="Choose Low, Base or High")
    put(ws, "E6", "Low, Base or High. The Scenarios sheet always computes all three, whatever is selected here.",
        kind="muted")
    IN["sel"] = "Inputs!$D$6"

    band(ws, 8, "1. Scenario levers", "B", "N")
    header(ws, 9, ["Ref", "Lever", "Low", "Base", "High", "Active", "Unit", "Source / comment"], "B", height=20)
    for c in "DEFG":
        ws[f"{c}9"].alignment = Alignment(horizontal="right", vertical="center")
    ws["I9"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=False)
    LEV_ROWS = {}
    levers = [
        ("eng", "S1", "Engineering remediation multiplier", (0.8, 1.0, 1.3), "x", NF_X,
         "Low: less remediation than assessed. High: remediation 30% above estimate."),
        ("nb", "S2", "Notified-body fee multiplier", (0.6, 1.0, 1.6), "x", NF_X,
         "Low: fewer notified-body days. High: scarcity forces a second body and premium fees."),
        ("test", "S3", "Security testing multiplier", (0.9, 1.0, 1.0), "x", NF_X, "Low only: lighter re-testing."),
        ("legal", "S4", "Legal, representation and translation multiplier", (1.0, 1.0, 1.5), "x", NF_X,
         "High only: premium legal support."),
        ("pfte", "S5", "Programme team FTE (build, Q4 2026 to Dec 2027)", (5, 5, 6), "FTE", '0.0',
         "High adds one programme FTE; run stays at the run FTE input."),
        ("cont", "S6", "Contingency on one-off costs", (0.10, 0.15, 0.20), "%", NF_PCT0,
         "Applied to Q4 2026 and 2027 subtotals; no contingency on the run-rate."),
    ]
    r = 10
    for key, ref, lab, vals, unit, fmt, com in levers:
        put(ws, f"B{r}", ref, kind="muted", border=B_ROW)
        put(ws, f"C{r}", lab, kind="label", border=B_ROW)
        for c, v in zip("DEF", vals):
            put(ws, f"{c}{r}", v, kind="input", fmt=fmt, border=B_ROW)
        put(ws, f"G{r}", f"=INDEX(D{r}:F{r},MATCH($D$6,$D$9:$F$9,0))", fmt=fmt, border=B_ROW, bold=True)
        put(ws, f"H{r}", unit, kind="muted", border=B_ROW, indent=1)
        put(ws, f"I{r}", com, kind="muted", border=B_ROW)
        for c in "JKLMN":
            ws[f"{c}{r}"].border = B_ROW
        LEV_ROWS[key] = r
        r += 1


    def LEV(name, col):
        return f"Inputs!${col}${LEV_ROWS[name]}"


    sections = [
        ("2. People and run-rate", [
            ("fte_prog", "Loaded cost per FTE: programme team", A["fte_cost_programme"], "EUR per FTE-year", NF_EUR,
             "cost_model.assumptions.fte_cost_programme (illustrative loaded rate)"),
            ("fte_psirt", "Loaded cost per FTE: PSIRT", A["fte_cost_psirt"], "EUR per FTE-year", NF_EUR,
             "cost_model.assumptions.fte_cost_psirt"),
            ("fte_eng", "Loaded cost per FTE: engineering", A["fte_cost_engineering"], "EUR per FTE-year", NF_EUR,
             "cost_model.assumptions.fte_cost_engineering"),
            ("prog_run_fte", "Programme team FTE in run (from 2028)", A["programme_team_run_fte"], "FTE", "0.0",
             "cost_model.assumptions.programme_team_run_fte"),
            ("psirt_fte", "Incremental PSIRT FTE (lead + analyst)", A["psirt_incremental_fte"], "FTE", "0.0",
             "cost_model.assumptions.psirt_incremental_fte"),
            ("oncall", "PSIRT 24/7 on-call allowance", A["psirt_oncall_allowance"], "EUR per year", NF_EUR,
             "cost_model.assumptions.psirt_oncall_allowance"),
            ("q4_share", "Share of a full year falling in Q4 2026 (Oct to Dec)", 0.25, "% of a year", NF_PCT0,
             "Derived: 3 of 12 months; applied to programme team and PSIRT annual cost"),
        ]),
        ("3. Engineering remediation of Annex I gaps", [
            ("rem_def", "Remediation effort per Default family", A["remediation_fte_years"]["default"],
             "FTE-years per family", "0.0", "cost_model.assumptions.remediation_fte_years.default"),
            ("rem_i", "Remediation effort per Class I family", A["remediation_fte_years"]["class_i"],
             "FTE-years per family", "0.0", "cost_model.assumptions.remediation_fte_years.class_i"),
            ("rem_ii", "Remediation effort per Class II family", A["remediation_fte_years"]["class_ii"],
             "FTE-years per family", "0.0", "cost_model.assumptions.remediation_fte_years.class_ii"),
            ("rem_q4", "Share of remediation in Q4 2026 (balance in 2027)", A["remediation_phasing"]["q4_2026"],
             "%", NF_PCT0, f"cost_model.assumptions.remediation_phasing ({A['remediation_phasing']['q4_2026']:.0%} / {A['remediation_phasing']['y2027']:.0%})"),
        ]),
        ("4. Shared platforms (build once, use for every family)", [
            ("plat_sbom", "SBOM, VEX and CSAF tooling (build)", A["platforms_build_detail"]["sbom_vex_csaf_tooling"],
             "EUR", NF_EUR, "cost_model.assumptions.platforms_build_detail"),
            ("plat_hsm", "Signing HSM and update infrastructure (build)",
             A["platforms_build_detail"]["signing_hsm_update_infrastructure"], "EUR", NF_EUR,
             "cost_model.assumptions.platforms_build_detail"),
            ("plat_sor", "System of record (build)", A["platforms_build_detail"]["system_of_record"], "EUR", NF_EUR,
             "cost_model.assumptions.platforms_build_detail"),
            ("plat_psirt", "PSIRT tooling and advisory portal (build)",
             A["platforms_build_detail"]["psirt_tooling_advisory_portal"], "EUR", NF_EUR,
             "cost_model.assumptions.platforms_build_detail"),
            ("plat_q4", "Share of platform build in Q4 2026 (balance in 2027)", A["platforms_phasing"]["q4_2026"], "%",
             NF_PCT0, f"cost_model.assumptions.platforms_phasing ({A['platforms_phasing']['q4_2026']:.0%} / {A['platforms_phasing']['y2027']:.0%})"),
            ("plat_run", "Platform run cost", A["platforms_run"], "EUR per year", NF_EUR,
             "cost_model.assumptions.platforms_run"),
            ("plat_run27", "Share of a year of platform run cost incurred in 2027", 0.5, "% of a year", NF_PCT0,
             f"Derived from the driver 'EUR {A['platforms_run'] / 1000:,.0f}k a year run from mid-2027'"),
        ]),
        ("5. Risk assessment, security testing and documentation", [
            ("ra_cost", "Risk assessment and threat model per family", A["risk_assessment_per_family"],
             "EUR per family", NF_EUR, "cost_model.assumptions.risk_assessment_per_family"),
            ("ra_q4", "Share of risk assessments in Q4 2026 (balance in 2027)", A["risk_assessment_phasing"]["q4_2026"],
             "%", NF_PCT0, f"cost_model.assumptions.risk_assessment_phasing ({A['risk_assessment_phasing']['q4_2026']:.0%} / {A['risk_assessment_phasing']['y2027']:.0%})"),
            ("test_def", "Security testing per Default family", A["testing_per_family_per_year"]["default"],
             "EUR per family-year", NF_EUR, "cost_model.assumptions.testing_per_family_per_year"),
            ("test_i", "Security testing per Class I family", A["testing_per_family_per_year"]["class_i"],
             "EUR per family-year", NF_EUR, "cost_model.assumptions.testing_per_family_per_year"),
            ("test_ii", "Security testing per Class II family", A["testing_per_family_per_year"]["class_ii"],
             "EUR per family-year", NF_EUR, "cost_model.assumptions.testing_per_family_per_year"),
            ("test_q4", "Share of a year of testing in Q4 2026", 0.0, "% of a year", NF_PCT0,
             f"Derived: base lines show no Q4 2026 testing; testing starts with remediation (P3, {P3.get('start', '')})"),
            ("doc_cost", "Technical file and Annex II information per family", A["documentation_per_family"],
             "EUR per family", NF_EUR, "cost_model.assumptions.documentation_per_family"),
            ("doc_q4", "Share of documentation build in Q4 2026 (balance in 2027)", 0.0, "%", NF_PCT0,
             f"Derived: base lines show documentation in 2027 (P4, {pdate(P4['start']):%b} to {pdate(P4['end']):%b %Y})" if P4 else "Derived: base lines show documentation in 2027"),
            ("doc_run", "Documentation upkeep per family (run)", A["documentation_run_per_family"],
             "EUR per family-year", NF_EUR, "cost_model.assumptions.documentation_run_per_family"),
        ]),
        (f"6. Notified bodies: vendor estimates, unverified. {X.nb_status}", [
            ("nb_pre_n", "Notified-body pre-assessments", A["nb_pre_assessments"]["count"], "number", "0",
             f"{Words(NBPRE['count'])} candidate bodies" + (f" (board decision {NB_BD})" if NB_BD else "")),
            ("nb_pre_unit", "Cost per pre-assessment", A["nb_pre_assessments"]["unit"], "EUR", NF_EUR,
             "cost_model.assumptions.nb_pre_assessments.unit"),
            ("nb_pre_q4", "Pre-assessments contracted in Q4 2026", round(NBPRE.get("q4_2026", 0) / NBPRE["unit"]) if NBPRE["unit"] else 0, "number", "0",
             f"Derived: pack_data shows EUR {NBPRE.get('q4_2026', 0) / 1000:,.0f}k in Q4 2026 and EUR {NBPRE.get('y2027', 0) / 1000:,.0f}k in 2027"),
            ("nb_b_n", f"Module B examinations ({NBB_NOTE})", A["nb_module_b_examinations"]["count"],
             "number", "0", "cost_model.assumptions.nb_module_b_examinations"),
            ("nb_b_unit", "Cost per Module B examination", A["nb_module_b_examinations"]["unit"], "EUR", NF_EUR,
             "Benchmark EUR 20k to 60k (CRA Decoded, commentary); see Benchmarks"),
            ("nb_h_init", f"Module H initial approval ({MODH})", A["nb_module_h"]["initial"], "EUR",
             NF_EUR, "Benchmark EUR 80k to 150k for a first engagement (commentary); see Benchmarks"),
            ("nb_h_extra_n", "Additional Module H product categories", A["nb_module_h"]["extra_categories"], "number",
             "0", "cost_model.assumptions.nb_module_h.extra_categories"),
            ("nb_h_extra_unit", "Cost per additional Module H category", A["nb_module_h"]["per_extra_category"], "EUR",
             NF_EUR, "cost_model.assumptions.nb_module_h.per_extra_category"),
            ("nb_h_surv", "Module H surveillance (run)", A["nb_surveillance_run"]["module_h"], "EUR per year", NF_EUR,
             "Surveillance every 1 to 2 years (commentary)"),
            ("nb_b_audit", "Module B periodic audits (run)", A["nb_surveillance_run"]["module_b_audits"], "EUR per year",
             NF_EUR, "cost_model.assumptions.nb_surveillance_run.module_b_audits"),
        ]),
        ("7. Training, legal and supply chain", [
            ("train_q4", "Training and awareness, Q4 2026", A["training"]["q4_2026"], "EUR", NF_EUR,
             "cost_model.assumptions.training"),
            ("train_27", "Training and awareness, 2027", A["training"]["y2027"], "EUR", NF_EUR,
             "cost_model.assumptions.training"),
            ("train_run", "Training and awareness (run)", A["training"]["run"], "EUR per year", NF_EUR,
             "cost_model.assumptions.training"),
            ("legal_q4", "External legal, Q4 2026", A["legal"]["external_q4_2026"], "EUR", NF_EUR,
             "cost_model.assumptions.legal"),
            ("legal_27", "External legal, 2027", A["legal"]["external_2027"], "EUR", NF_EUR,
             "cost_model.assumptions.legal"),
            ("transl", "DoC and Annex II translations per family (2027)", A["legal"]["translations_per_family"],
             "EUR per family", NF_EUR, "cost_model.assumptions.legal.translations_per_family"),
            ("legal_run", "Legal and EU representation (run)", A["legal"]["run"], "EUR per year", NF_EUR,
             "cost_model.assumptions.legal.run"),
            ("supp_q4", "Supplier programme, Q4 2026", 0, "EUR", NF_EUR,
             "Derived: base lines show no Q4 2026 supplier spend"),
            ("supp_27", "Supplier programme, 2027", A["supplier_programme"]["y2027"], "EUR", NF_EUR,
             "cost_model.assumptions.supplier_programme"),
            ("supp_run", "Supplier programme (run)", A["supplier_programme"]["run"], "EUR per year", NF_EUR,
             "cost_model.assumptions.supplier_programme"),
            ("suppliers", "In-scope suppliers (used in the driver text)", CL["suppliers_in_scope"], "number", "0",
             "client.suppliers_in_scope"),
        ]),
    ]
    r = 17
    n = 1
    for title, rows in sections:
        band(ws, r, title, "B", "N")
        r += 1
        header(ws, r, ["Ref", "Assumption", "Value", "Unit", "Source / comment"], "B", height=20)
        ws[f"D{r}"].alignment = Alignment(horizontal="right", vertical="center")
        ws[f"E{r}"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws[f"F{r}"].alignment = Alignment(horizontal="left", vertical="center", wrap_text=False)
        for c in "GHIJKLMN":
            ws[f"{c}{r}"].fill = fill(C["ink900"])
        r += 1
        for key, lab, val, unit, fmt, com in rows:
            ref = f"A{n:02d}"
            put(ws, f"B{r}", ref, kind="muted", border=B_ROW)
            put(ws, f"C{r}", lab, kind="label", border=B_ROW)
            put(ws, f"D{r}", val, kind="input", fmt=fmt, border=B_ROW)
            put(ws, f"E{r}", unit, kind="muted", border=B_ROW, indent=1)
            put(ws, f"F{r}", com, kind="muted", border=B_ROW)
            for c in "GHIJKLMN":
                ws[f"{c}{r}"].border = B_ROW
            IN[key] = f"Inputs!$D${r}"
            INROW[key] = r
            REFID[key] = ref
            n += 1
            r += 1
        r += 1

    # --- 8. Revenue by business unit
    band(ws, r, "8. Revenue by business unit (EUR m)", "B", "N")
    r += 1
    header(ws, r, ["BU", "Business unit", "Revenue (EUR m)", "EU share", "EU revenue (EUR m)", "Source / comment"], "B",
           height=30)
    for c in "DEF":
        ws[f"{c}{r}"].alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    for c in "HIJKLMN":
        ws[f"{c}{r}"].fill = fill(C["ink900"])
    r += 1
    BU_FIRST = r
    for bu in CL["business_units"]:
        put(ws, f"B{r}", bu["id"], kind="label", border=B_ROW, bold=True)
        put(ws, f"C{r}", bu["name"], kind="label", border=B_ROW)
        put(ws, f"D{r}", bu["revenue_m"], kind="input", fmt=NF_EUR1, border=B_ROW)
        put(ws, f"E{r}", bu["eu_share"], kind="input", fmt=NF_PCT0, border=B_ROW)
        put(ws, f"F{r}", f"=D{r}*E{r}", fmt=NF_EUR1, border=B_ROW)
        put(ws, f"G{r}", "client.business_units", kind="muted", border=B_ROW)
        for c in "HIJKLMN":
            ws[f"{c}{r}"].border = B_ROW
        r += 1
    BU_LAST = r - 1
    put(ws, f"B{r}", "Group", kind="label", bold=True, border=B_TOTAL)
    put(ws, f"C{r}", f"{X.client} total (worldwide revenue)", kind="label", bold=True, border=B_TOTAL)
    put(ws, f"D{r}", f"=SUM(D{BU_FIRST}:D{BU_LAST})", fmt=NF_EUR1, bold=True, border=B_TOTAL)
    put(ws, f"E{r}", f"=F{r}/D{r}", fmt=NF_PCT1, bold=True, border=B_TOTAL)
    put(ws, f"F{r}", f"=SUM(F{BU_FIRST}:F{BU_LAST})", fmt=NF_EUR1, bold=True, border=B_TOTAL)
    put(ws, f"G{r}", f"Group revenue EUR {REV_TXT}m; EU revenue EUR {CL['eu_revenue_m']:,.1f}m ({CL['eu_share']:.0%})", kind="muted", border=B_TOTAL)
    for c in "HIJKLMN":
        ws[f"{c}{r}"].border = B_TOTAL
    IN["rev_total"] = f"Inputs!$D${r}"
    IN["eu_rev_total"] = f"Inputs!$F${r}"
    BU_TOTAL_ROW = r
    r += 2

    # --- 9. Product portfolio
    band(ws, r, f"9. Product portfolio in scope ({X.nfam} families)", "B", "N")
    r += 1
    PH = r
    header(ws, r, ["ID", "Family", "BU", "Class (planning basis)", "CRA class as recorded", "Conformity route", "Wave",
                   "SKUs", "Support period (years)", "Revenue (EUR m)", "EU share", "EU revenue (EUR m)",
                   "Needs a notified body"], "B", height=32)
    for c in "IJKLM":
        ws[f"{c}{r}"].alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    r += 1
    FAM_FIRST = r
    for fam in CL["product_families"]:
        planning = "Default" if fam["cra_class"].startswith("Default") else fam["cra_class"]
        put(ws, f"B{r}", fam["id"], kind="label", bold=True, border=B_ROW)
        put(ws, f"C{r}", fam["name"], kind="label", border=B_ROW)
        put(ws, f"D{r}", fam["bu"], kind="input", border=B_ROW, fill_hex=C["acc100"])
        put(ws, f"E{r}", planning, kind="input", border=B_ROW)
        put(ws, f"F{r}", fam["cra_class"], kind="label", border=B_ROW, wrap=True)
        put(ws, f"G{r}", fam["route"], kind="label", border=B_ROW, wrap=True)
        put(ws, f"H{r}", fam["wave"], kind="label", border=B_ROW, wrap=True)
        put(ws, f"I{r}", fam["skus"], kind="input", fmt="0", border=B_ROW)
        put(ws, f"J{r}", fam["support_period_years"], kind="input", fmt="0", border=B_ROW)
        put(ws, f"K{r}", fam["revenue_m"], kind="input", fmt=NF_EUR1, border=B_ROW)
        put(ws, f"L{r}", f"=INDEX($E${BU_FIRST}:$E${BU_LAST},MATCH(D{r},$B${BU_FIRST}:$B${BU_LAST},0))", fmt=NF_PCT0,
            border=B_ROW)
        put(ws, f"M{r}", f"=K{r}*L{r}", fmt=NF_EUR1, border=B_ROW)
        put(ws, f"N{r}", f'=IF(OR(E{r}="Class I",E{r}="Class II"),"Yes","No")', border=B_ROW, align="center")
        ws.row_dimensions[r].height = 24
        r += 1
    FAM_LAST = r - 1
    add_table(ws, "tblPortfolio", f"B{PH}:N{FAM_LAST}")
    add_list_dv(ws, f"E{FAM_FIRST}:E{FAM_LAST}", '"Default,Class I,Class II"',
                prompt="Class used for costing and exposure: Default, Class I or Class II")
    add_list_dv(ws, f"D{FAM_FIRST}:D{FAM_LAST}", '"' + ','.join(X.bu_ids) + '"')
    # Other revenue line (not a family)
    put(ws, f"B{r}", "SaaS", kind="label", bold=True, border=B_ROW)
    put(ws, f"C{r}", "Cloud platform revenue (remote data processing for several products; not a family)", kind="label",
        border=B_ROW, wrap=True)
    put(ws, f"D{r}", X.saas_bu, kind="input", border=B_ROW)
    put(ws, f"K{r}", X.saas_revenue_m, kind="input", fmt=NF_EUR1, border=B_ROW)
    put(ws, f"L{r}", f"=INDEX($E${BU_FIRST}:$E${BU_LAST},MATCH(D{r},$B${BU_FIRST}:$B${BU_LAST},0))", fmt=NF_PCT0,
        border=B_ROW)
    put(ws, f"M{r}", f"=K{r}*L{r}", fmt=NF_EUR1, border=B_ROW)
    for c in "EFGHIJN":
        ws[f"{c}{r}"].border = B_ROW
    ws.row_dimensions[r].height = 24
    SAAS_ROW = r
    r += 1
    put(ws, f"C{r}", "Total revenue (families + other)", kind="label", bold=True, border=B_TOTAL)
    put(ws, f"K{r}", f"=SUM(K{FAM_FIRST}:K{SAAS_ROW})", fmt=NF_EUR1, bold=True, border=B_TOTAL)
    put(ws, f"M{r}", f"=SUM(M{FAM_FIRST}:M{SAAS_ROW})", fmt=NF_EUR1, bold=True, border=B_TOTAL)
    for c in "BDEFGHIJLN":
        ws[f"{c}{r}"].border = B_TOTAL
    PORT_TOTAL_ROW = r
    r += 1
    source_line(ws, f"B{r+1}", f"Source: pack_data.json {X.v} (client.product_families, client.business_units); "
                + PORT_NOTE)
    ws.freeze_panes = "A5"
    print_setup(ws, HDR, area=f"A1:N{r+1}")

    FAM = dict(id=f"Inputs!$B${FAM_FIRST}:$B${FAM_LAST}", cls=f"Inputs!$E${FAM_FIRST}:$E${FAM_LAST}",
               rec=f"Inputs!$F${FAM_FIRST}:$F${FAM_LAST}", rev=f"Inputs!$K${FAM_FIRST}:$K${FAM_LAST}",
               eu=f"Inputs!$M${FAM_FIRST}:$M${FAM_LAST}", nb=f"Inputs!$N${FAM_FIRST}:$N${FAM_LAST}")

    # =====================================================================================
    # COST BUILD
    # =====================================================================================
    ws = ws_cb
    widths(ws, {"A": 2.5, "B": 5, "C": 25, "D": 46, "E": 56, "F": 14, "G": 14, "H": 15, "I": 15, "J": 13, "K": 13,
                "L": 10})
    title_block(ws, LABEL + " · COST BUILD",
                f'="With the "&Inputs!$D$6&" scenario, {X.codename} costs EUR "&TEXT(H31/1000000,"0.0")&"m one-off to '
                'Dec 2027 and EUR "&TEXT(I31/1000000,"0.0")&"m a year from 2028"',
                "EUR, real 2026 terms, excl. VAT · Every cost line is a formula on Inputs and the active scenario · "
                "Illustrative", link_col="L")
    # check indicators (filled later)
    put(ws, "J2", f"Reconciles to {X.v} control totals", kind="muted", size=8, align="right")
    put(ws, "J3", "All model checks", kind="muted", size=8, align="right")

    band(ws, 5, "Volume drivers (scenario-neutral, read from the Inputs portfolio)", "B", "L")
    header(ws, 6, ["Ref", "Driver", "", "", "Value", "Unit"], "B", height=18)
    ws["F6"].alignment = Alignment(horizontal="right", vertical="center")
    drivers = [
        ("nfam", "D1", "Families in scope", f"=COUNTA({FAM['id']})", "families", "0"),
        ("n_def", "D2", "of which Default (planning basis)", f'=COUNTIF({FAM["cls"]},"Default")', "families", "0"),
        ("n_i", "D3", "of which Class I", f'=COUNTIF({FAM["cls"]},"Class I")', "families", "0"),
        ("n_ii", "D4", "of which Class II", f'=COUNTIF({FAM["cls"]},"Class II")', "families", "0"),
        ("fteyrs", "D5", "Engineering remediation effort (Default, Class I, Class II rates x families)",
         f"=F8*{IN['rem_def']}+F9*{IN['rem_i']}+F10*{IN['rem_ii']}", "FTE-years", "0.0"),
        ("test_yr", "D6", "Security testing per year, before scenario lever",
         f"=F8*{IN['test_def']}+F9*{IN['test_i']}+F10*{IN['test_ii']}", "EUR per year", NF_EUR),
        ("build", "D7", "Shared-platform build (four components)",
         f"={IN['plat_sbom']}+{IN['plat_hsm']}+{IN['plat_sor']}+{IN['plat_psirt']}", "EUR", NF_EUR),
    ]
    DRV = {}
    r = 7
    for key, ref, lab, f, unit, fmt in drivers:
        put(ws, f"B{r}", ref, kind="muted", border=B_ROW)
        put(ws, f"C{r}", lab, kind="label", border=B_ROW)
        put(ws, f"F{r}", f, fmt=fmt, border=B_ROW)
        put(ws, f"G{r}", unit, kind="muted", border=B_ROW)
        for c in "DEHIJKL":
            ws[f"{c}{r}"].border = B_ROW
        DRV[key] = r
        r += 1
    put(ws, f"B{r}", "D8", kind="muted", border=B_ROW)
    put(ws, f"C{r}", "Active scenario", kind="label", border=B_ROW)
    put(ws, f"F{r}", "=Inputs!$D$6", border=B_ROW, align="right", bold=True)
    for c in "DEGHIJKL":
        ws[f"{c}{r}"].border = B_ROW


    def drv_local(k):
        return f"$F${DRV[k]}"


    def drv_cb(k):
        return f"'Cost build'!$F${DRV[k]}"


    LINES = [
        (1, "Programme & governance", "Programme team (director, compliance lead, product security officer, PMO)", "Programme FTE"),
        (2, "Reporting & PSIRT", "Incremental PSIRT (lead + analyst) and 24/7 on-call allowance", "-"),
        (3, "Secure engineering", "Engineering remediation of Annex I gaps", "Engineering"),
        (4, "Shared platforms", "SBOM/VEX/CSAF tooling, signing HSM and update infrastructure, system of record, PSIRT tooling", "-"),
        (5, "Secure engineering", "Risk assessments and threat models", "-"),
        (6, "Secure engineering", "Security testing (penetration tests, fuzzing, re-tests)", "Testing"),
        (7, "Documentation & evidence", "Technical files and Annex II user information", "-"),
        (8, "Conformity & market access", "Notified bodies: pre-assessments, Module B examinations, Module H approval", "Notified body"),
        (9, "People & change", "Training and awareness", "-"),
        (10, "Conformity & market access", "Legal, EU representation and translations", "Legal"),
        (11, "Supply chain", "Supplier contract remediation and questionnaire programme", "-"),
    ]


    def line_formulas(c, drv):
        I = IN
        lev = lambda n: LEV(n, c)
        f = {}
        f[1] = (f"={lev('pfte')}*{I['fte_prog']}*{I['q4_share']}", f"={lev('pfte')}*{I['fte_prog']}",
                f"={I['prog_run_fte']}*{I['fte_prog']}")
        f[2] = (f"=({I['psirt_fte']}*{I['fte_psirt']}+{I['oncall']})*{I['q4_share']}",
                f"={I['psirt_fte']}*{I['fte_psirt']}+{I['oncall']}", f"={I['psirt_fte']}*{I['fte_psirt']}+{I['oncall']}")
        f[3] = (f"={drv('fteyrs')}*{I['fte_eng']}*{lev('eng')}*{I['rem_q4']}",
                f"={drv('fteyrs')}*{I['fte_eng']}*{lev('eng')}*(1-{I['rem_q4']})", None)
        f[4] = (f"={drv('build')}*{I['plat_q4']}", f"={drv('build')}*(1-{I['plat_q4']})+{I['plat_run']}*{I['plat_run27']}",
                f"={I['plat_run']}")
        f[5] = (f"={drv('nfam')}*{I['ra_cost']}*{I['ra_q4']}", f"={drv('nfam')}*{I['ra_cost']}*(1-{I['ra_q4']})", None)
        f[6] = (f"={drv('test_yr')}*{lev('test')}*{I['test_q4']}", f"={drv('test_yr')}*{lev('test')}",
                f"={drv('test_yr')}*{lev('test')}")
        f[7] = (f"={drv('nfam')}*{I['doc_cost']}*{I['doc_q4']}", f"={drv('nfam')}*{I['doc_cost']}*(1-{I['doc_q4']})",
                f"={drv('nfam')}*{I['doc_run']}")
        f[8] = (f"={I['nb_pre_q4']}*{I['nb_pre_unit']}*{lev('nb')}",
                f"=(({I['nb_pre_n']}-{I['nb_pre_q4']})*{I['nb_pre_unit']}+{I['nb_b_n']}*{I['nb_b_unit']}+{I['nb_h_init']}"
                f"+{I['nb_h_extra_n']}*{I['nb_h_extra_unit']})*{lev('nb')}",
                f"=({I['nb_h_surv']}+{I['nb_b_audit']})*{lev('nb')}")
        f[9] = (f"={I['train_q4']}", f"={I['train_27']}", f"={I['train_run']}")
        f[10] = (f"={I['legal_q4']}*{lev('legal')}", f"=({I['legal_27']}+{drv('nfam')}*{I['transl']})*{lev('legal')}",
                 f"={I['legal_run']}*{lev('legal')}")
        f[11] = (f"={I['supp_q4']}", f"={I['supp_27']}", f"={I['supp_run']}")
        return f


    def drivers_text():
        I = IN
        g = lambda n: LEV(n, "G")
        return {
            1: f'=TEXT({g("pfte")},"General")&" FTE x EUR "&TEXT({I["fte_prog"]},"#,##0")&" loaded; Q4 2026 = "&TEXT({I["q4_share"]},"0%")&" of a year; run "&TEXT({I["prog_run_fte"]},"General")&" FTE"',
            2: f'=TEXT({I["psirt_fte"]},"General")&" FTE x EUR "&TEXT({I["fte_psirt"]},"#,##0")&" + EUR "&TEXT({I["oncall"]},"#,##0")&" on-call a year"',
            3: f'=TEXT($F${DRV["fteyrs"]},"0.0")&" FTE-years (Default "&TEXT({I["rem_def"]},"0.0")&", Class I "&TEXT({I["rem_i"]},"0.0")&", Class II "&TEXT({I["rem_ii"]},"0.0")&" per family) x EUR "&TEXT({I["fte_eng"]},"#,##0")&" x "&TEXT({g("eng")},"0.0")&"; "&TEXT({I["rem_q4"]},"0%")&" in Q4 2026"',
            4: f'="EUR "&TEXT($F${DRV["build"]}/1000,"#,##0")&"k build ("&TEXT({I["plat_q4"]},"0%")&" Q4 2026, "&TEXT(1-{I["plat_q4"]},"0%")&" 2027); EUR "&TEXT({I["plat_run"]}/1000,"#,##0")&"k a year run from mid-2027"',
            5: f'=TEXT($F${DRV["nfam"]},"0")&" families x EUR "&TEXT({I["ra_cost"]},"#,##0")&" ("&TEXT({I["ra_q4"]},"0%")&" in Q4 2026)"',
            6: f'="Per family per year: Default EUR "&TEXT({I["test_def"]}/1000,"0")&"k, Class I EUR "&TEXT({I["test_i"]}/1000,"0")&"k, Class II EUR "&TEXT({I["test_ii"]}/1000,"0")&"k x "&TEXT({g("test")},"0.0")',
            7: f'=TEXT($F${DRV["nfam"]},"0")&" families x EUR "&TEXT({I["doc_cost"]},"#,##0")&"; run EUR "&TEXT({I["doc_run"]},"#,##0")&" per family"',
            8: f'=TEXT({I["nb_pre_n"]},"0")&" pre-assessments x EUR "&TEXT({I["nb_pre_unit"]}/1000,"0")&"k; "&TEXT({I["nb_b_n"]},"0")&" Module B examinations x EUR "&TEXT({I["nb_b_unit"]}/1000,"0")&"k; Module H EUR "&TEXT({I["nb_h_init"]}/1000,"0")&"k + "&TEXT({I["nb_h_extra_n"]},"0")&" categories x EUR "&TEXT({I["nb_h_extra_unit"]}/1000,"0")&"k (vendor estimates) x "&TEXT({g("nb")},"0.0")',
            9: "Role-based training, drills, e-learning",
            10: f'="External legal EUR "&TEXT(({I["legal_q4"]}+{I["legal_27"]})/1000,"0")&"k; DoC/Annex II translations "&TEXT($F${DRV["nfam"]},"0")&" x EUR "&TEXT({I["transl"]}/1000,"0")&"k x "&TEXT({g("legal")},"0.0")',
            11: f'=TEXT({I["suppliers"]},"0")&" in-scope suppliers: clause pack and questionnaire"',
        }


    band(ws, 16, "Cost lines (active scenario)", "B", "L")
    header(ws, 17, ["#", "Workstream", "Line", "Driver (updates with Inputs)", "Q4 2026 (EUR)", "2027 (EUR)",
                    "One-off to Dec 2027 (EUR)", "Run 2028 (EUR a year)", "Scenario lever"], "B", height=30)
    for c in "FGHI":
        ws[f"{c}17"].alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    FL = line_formulas("G", drv_local)
    DT = drivers_text()
    LINE_FIRST = 18
    for i, (num, wsn, line, lever) in enumerate(LINES):
        rr = LINE_FIRST + i
        q4, y27, run = FL[num]
        put(ws, f"B{rr}", num, kind="muted", border=B_ROW, align="center")
        put(ws, f"C{rr}", wsn, kind="label", border=B_ROW, wrap=True)
        put(ws, f"D{rr}", line, kind="label", border=B_ROW, wrap=True)
        put(ws, f"E{rr}", DT[num], size=8, border=B_ROW, wrap=True)
        put(ws, f"F{rr}", q4, fmt=NF_EUR, border=B_ROW)
        put(ws, f"G{rr}", y27, fmt=NF_EUR, border=B_ROW)
        put(ws, f"H{rr}", f"=SUM(F{rr}:G{rr})", fmt=NF_EUR, border=B_ROW)
        if run is None:
            put(ws, f"I{rr}", "-", kind="muted", border=B_ROW, align="right")
        else:
            put(ws, f"I{rr}", run, fmt=NF_EUR, border=B_ROW)
        put(ws, f"J{rr}", lever, kind="muted", border=B_ROW, align="center")
        ws.row_dimensions[rr].height = 30
    LINE_LAST = LINE_FIRST + len(LINES) - 1  # 28
    rs = LINE_LAST + 1  # 29 subtotal
    put(ws, f"D{rs}", "Subtotal excl. contingency", kind="label", bold=True, border=B_SUB)
    for c in "FGHI":
        put(ws, f"{c}{rs}", f"=SUM({c}{LINE_FIRST}:{c}{LINE_LAST})", fmt=NF_EUR, bold=True, border=B_SUB)
    for c in "BCEJ":
        ws[f"{c}{rs}"].border = B_SUB
    rc = rs + 1  # 30 contingency
    put(ws, f"D{rc}", "Contingency", kind="label", border=B_ROW)
    put(ws, f"E{rc}", f'="At "&TEXT({LEV("cont", "G")},"0%")&" of one-off costs; none on the run-rate"', kind="muted",
        size=8, border=B_ROW)
    put(ws, f"F{rc}", f"=F{rs}*{LEV('cont', 'G')}", fmt=NF_EUR, border=B_ROW)
    put(ws, f"G{rc}", f"=G{rs}*{LEV('cont', 'G')}", fmt=NF_EUR, border=B_ROW)
    put(ws, f"H{rc}", f"=SUM(F{rc}:G{rc})", fmt=NF_EUR, border=B_ROW)
    put(ws, f"I{rc}", "-", kind="muted", border=B_ROW, align="right")
    put(ws, f"J{rc}", "Contingency", kind="muted", border=B_ROW, align="center")
    for c in "BC":
        ws[f"{c}{rc}"].border = B_ROW
    rt = rc + 1  # 31 total
    put(ws, f"D{rt}", "Total incl. contingency", kind="label", bold=True, border=B_TOTAL)
    put(ws, f"F{rt}", f"=F{rs}+F{rc}", fmt=NF_EUR, bold=True, border=B_TOTAL)
    put(ws, f"G{rt}", f"=G{rs}+G{rc}", fmt=NF_EUR, bold=True, border=B_TOTAL)
    put(ws, f"H{rt}", f"=F{rt}+G{rt}", kind="output", fmt=NF_EUR)
    put(ws, f"I{rt}", f"=I{rs}", kind="output", fmt=NF_EUR)
    for c in "BCEJ":
        ws[f"{c}{rt}"].border = B_TOTAL
    assert (rs, rc, rt) == (29, 30, 31)
    put(ws, "D33", f"Share of group revenue (EUR {REV_TXT}m)", kind="label")
    put(ws, "E33", "One-off total and run-rate as a share of one year's worldwide revenue", kind="muted", size=8)
    put(ws, "H33", f"=H31/({IN['rev_total']}*1000000)", fmt=NF_PCT2, bold=True)
    put(ws, "I33", f"=I31/({IN['rev_total']}*1000000)", fmt=NF_PCT2, bold=True)

    # --- Reconciliation checks
    band(ws, 35, f"Checks: reconciliation to pack_data.json {X.v} control totals (all inputs at {X.v} values)", "B", "L")
    header(ws, 36, ["Ref", "Metric", "", "", "Low", "Base", "High", "Active control", "Model (active)", "Difference",
                    "Check"], "B", height=20)
    for c in "FGHIJKL":
        ws[f"{c}36"].alignment = Alignment(horizontal="right", vertical="center")
    SC = CM["scenarios"]
    ctl = [
        ("Q4 2026 subtotal excl. contingency", "q4_2026", f"F{rs}"),
        ("2027 subtotal excl. contingency", "y2027", f"G{rs}"),
        ("Contingency, Q4 2026", "contingency_q4_2026", f"F{rc}"),
        ("Contingency, 2027", "contingency_2027", f"G{rc}"),
        ("Q4 2026 incl. contingency", "q4_2026_incl_contingency", f"F{rt}"),
        ("2027 incl. contingency", "y2027_incl_contingency", f"G{rt}"),
        ("One-off total incl. contingency", "one_off_total_incl_contingency", f"H{rt}"),
        ("Run 2028 (a year)", "run_2028", f"I{rt}"),
    ]
    CTL_ROW = {}
    r = 37
    for i, (lab, key, model) in enumerate(ctl):
        put(ws, f"B{r}", f"C{i + 1}", kind="muted", border=B_ROW)
        put(ws, f"C{r}", lab, kind="label", border=B_ROW)
        for c, s in zip("FGH", ["low", "base", "high"]):
            put(ws, f"{c}{r}", SC[s]["totals"][key], kind="input", fmt=NF_EUR, border=B_ROW)
        put(ws, f"I{r}", f"=INDEX(F{r}:H{r},MATCH(Inputs!$D$6,$F$36:$H$36,0))", fmt=NF_EUR, border=B_ROW)
        put(ws, f"J{r}", f"={model}", fmt=NF_EUR, border=B_ROW)
        put(ws, f"K{r}", f"=J{r}-I{r}", fmt=NF_EUR2, border=B_ROW)
        put(ws, f"L{r}", f'=IF(ABS(K{r})<0.5,"OK","CHECK")', border=B_ROW, align="center", bold=True)
        for c in "DE":
            ws[f"{c}{r}"].border = B_ROW
        CTL_ROW[key] = r
        r += 1
    # r = 45
    put(ws, "C45", f"Active scenario reproduces its {X.v} control totals", kind="label", bold=True)
    put(ws, "L45", '=IF(COUNTIF(L37:L44,"OK")=8,"OK","CHECK")', align="center", bold=True)
    put(ws, "C46", f"All three scenarios reproduce their {X.v} control totals (Scenarios sheet)", kind="label", bold=True)
    # L46 set after scenarios sheet exists
    source_line(ws, "C47", f"Control totals are the {X.v} values in pack_data.json (cost_model.scenarios.*.totals). "
                "After you change an input on purpose, these reconciliation checks will (correctly) read CHECK.")

    band(ws, 49, "Checks: model integrity (should always read OK)", "B", "L")
    header(ws, 50, ["Ref", "Check", "", "", "", "", "", "Value A", "Value B", "Difference", "Check"], "B", height=20)
    for c in "IJKL":
        ws[f"{c}50"].alignment = Alignment(horizontal="right", vertical="center")
    # rows 51-56 filled after other sheets are defined
    put(ws, "C58", "All checks (reconciliation and integrity)", kind="label", bold=True)

    # =====================================================================================
    # SCENARIOS (independent of the selector)
    # =====================================================================================
    ws = ws_sc
    widths(ws, {"A": 2.5, "B": 5, "C": 24, "D": 46, "E": 13, "F": 13, "G": 13, "H": 2, "I": 13, "J": 13, "K": 13,
                "L": 2, "M": 13, "N": 13, "O": 13})
    title_block(ws, LABEL + " · SCENARIOS",
                '="One-off spend ranges from EUR "&TEXT(E27/1000000,"0.0")&"m (Low) to EUR "&TEXT(G27/1000000,"0.0")&"m '
                '(High); the base case needs EUR "&TEXT(F27/1000000,"0.0")&"m"',
                "All three scenarios are computed side by side from the Inputs scenario table, whatever the selector shows · "
                "EUR · Illustrative", link_col="O")
    blocks = [("Low", "E", "D"), ("Base", "I", "E"), ("High", "M", "F")]  # name, first col, lever col
    for name, c0, lc in blocks:
        cols = col_range(c0, get_column_letter(column_index_from_string(c0) + 2))
        ws.merge_cells(f"{cols[0]}5:{cols[2]}5")
        put(ws, f"{cols[0]}5", name, kind="label", bold=True, align="center", color=C["white"], fill_hex=C["ink900"], size=10)
        ws.merge_cells(f"{cols[0]}6:{cols[2]}6")
        desc = SC[name.lower()]["description"]
        put(ws, f"{cols[0]}6", desc, kind="label", wrap=True, fill_hex=C["ink100"], size=8, valign="top")
        ws.merge_cells(f"{cols[0]}7:{cols[2]}7")
        put(ws, f"{cols[0]}7",
            f'="Eng x"&TEXT(Inputs!${lc}$10,"0.0")&" · NB x"&TEXT(Inputs!${lc}$11,"0.0")&" · Test x"&TEXT(Inputs!${lc}$12,"0.0")'
            f'&" · Legal x"&TEXT(Inputs!${lc}$13,"0.0")&" · "&TEXT(Inputs!${lc}$14,"General")&" FTE · Cont. "&TEXT(Inputs!${lc}$15,"0%")',
            kind="muted", size=8, wrap=True, fill_hex=C["ink100"], valign="top")
        for cc in cols:
            ws[f"{cc}6"].fill = fill(C["ink100"])
            ws[f"{cc}7"].fill = fill(C["ink100"])
    ws.row_dimensions[6].height = 48
    ws.row_dimensions[7].height = 26
    put(ws, "D6", "Scenario description", kind="muted", size=8, align="right", valign="top")
    put(ws, "D7", "Levers (from Inputs)", kind="muted", size=8, align="right", valign="top")
    header(ws, 8, ["#", "Workstream", "Line", "Q4 2026", "2027", "Run 2028", "", "Q4 2026", "2027", "Run 2028", "",
                   "Q4 2026", "2027", "Run 2028"], "B", height=20)
    for c in "EFGIJKMNO":
        ws[f"{c}8"].alignment = Alignment(horizontal="right", vertical="center")
    for c in "HL":
        ws[f"{c}8"].fill = fill(C["white"])
    for i, (num, wsn, line, lever) in enumerate(LINES):
        rr = 9 + i
        put(ws, f"B{rr}", num, kind="muted", border=B_ROW, align="center")
        put(ws, f"C{rr}", wsn, kind="label", border=B_ROW)
        put(ws, f"D{rr}", line, kind="label", border=B_ROW, size=8)
        for name, c0, lc in blocks:
            fl = line_formulas(lc, drv_cb)[num]
            cols = col_range(c0, get_column_letter(column_index_from_string(c0) + 2))
            for cc, f in zip(cols, fl):
                if f is None:
                    put(ws, f"{cc}{rr}", "-", kind="muted", border=B_ROW, align="right")
                else:
                    put(ws, f"{cc}{rr}", f, fmt=NF_EUR, border=B_ROW)
    for name, c0, lc in blocks:
        cols = col_range(c0, get_column_letter(column_index_from_string(c0) + 2))
        for cc in cols:
            put(ws, f"{cc}20", f"=SUM({cc}9:{cc}19)", fmt=NF_EUR, bold=True, border=B_SUB)
        put(ws, f"{cols[0]}21", f"={cols[0]}20*Inputs!${lc}$15", fmt=NF_EUR, border=B_ROW)
        put(ws, f"{cols[1]}21", f"={cols[1]}20*Inputs!${lc}$15", fmt=NF_EUR, border=B_ROW)
        put(ws, f"{cols[2]}21", "-", kind="muted", border=B_ROW, align="right")
        put(ws, f"{cols[0]}22", f"={cols[0]}20+{cols[0]}21", fmt=NF_EUR, bold=True, border=B_TOTAL)
        put(ws, f"{cols[1]}22", f"={cols[1]}20+{cols[1]}21", fmt=NF_EUR, bold=True, border=B_TOTAL)
        put(ws, f"{cols[2]}22", f"={cols[2]}20", fmt=NF_EUR, bold=True, border=B_TOTAL)
    put(ws, "D20", "Subtotal excl. contingency", kind="label", bold=True, border=B_SUB)
    put(ws, "D21", "Contingency", kind="label", border=B_ROW)
    put(ws, "D22", "Total incl. contingency", kind="label", bold=True, border=B_TOTAL)
    for c in "BC":
        ws[f"{c}20"].border = B_SUB
        ws[f"{c}21"].border = B_ROW
        ws[f"{c}22"].border = B_TOTAL

    band(ws, 25, "Scenario comparison", "B", "I")
    header(ws, 26, ["Ref", "Metric", "", "Low", "Base", "High", "", "Unit"], "B", height=20)
    for c in "EFG":
        ws[f"{c}26"].alignment = Alignment(horizontal="right", vertical="center")
    ws["H26"].fill = fill(C["ink900"])
    comp = [
        ("SC1", "One-off to Dec 2027 incl. contingency", ("=E22+F22", "=I22+J22", "=M22+N22"), NF_EUR, "EUR", True),
        ("SC2", "of which Q4 2026", ("=E22", "=I22", "=M22"), NF_EUR, "EUR", False),
        ("SC3", "of which 2027", ("=F22", "=J22", "=N22"), NF_EUR, "EUR", False),
        ("SC4", "Contingency rate", ("=Inputs!$D$15", "=Inputs!$E$15", "=Inputs!$F$15"), NF_PCT0, "%", False),
        ("SC5", "Run-rate from 2028", ("=G22", "=K22", "=O22"), NF_EUR, "EUR a year", True),
        ("SC6", "One-off vs Base", ("=E27-$F$27", "=F27-$F$27", "=G27-$F$27"), NF_EUR, "EUR", False),
        ("SC7", "One-off vs Base (%)", ("=E32/$F$27", "=F32/$F$27", "=G32/$F$27"), NF_PCT1, "%", False),
        ("SC8", "One-off as % of group revenue", tuple(f"={c}27/({IN['rev_total']}*1000000)" for c in "EFG"), NF_PCT2,
         "%", False),
        ("SC9", "Run-rate as % of group revenue", tuple(f"={c}31/({IN['rev_total']}*1000000)" for c in "EFG"), NF_PCT2,
         "%", False),
        ("SC10", "Engineering remediation (one-off)", ("=E11+F11", "=I11+J11", "=M11+N11"), NF_EUR, "EUR", False),
        ("SC11", "Notified-body fees (one-off)", ("=E16+F16", "=I16+J16", "=M16+N16"), NF_EUR, "EUR", False),
        ("SC12", f"Control: one-off ({X.v})", tuple(f"='Cost build'!${c}${CTL_ROW['one_off_total_incl_contingency']}" for c in "FGH"),
         NF_EUR, "EUR", False),
        ("SC13", f"Check: one-off reproduces {X.v}", tuple(f'=IF(ABS({c}27-{c}38)<0.5,"OK","CHECK")' for c in "EFG"), None,
         "", False),
        ("SC14", f"Control: run-rate ({X.v})", tuple(f"='Cost build'!${c}${CTL_ROW['run_2028']}" for c in "FGH"), NF_EUR,
         "EUR a year", False),
        ("SC15", f"Check: run-rate reproduces {X.v}", tuple(f'=IF(ABS({c}31-{c}40)<0.5,"OK","CHECK")' for c in "EFG"), None,
         "", False),
    ]
    for i, (ref, lab, fs, fmt, unit, bold) in enumerate(comp):
        rr = 27 + i
        put(ws, f"B{rr}", ref, kind="muted", border=B_ROW)
        put(ws, f"C{rr}", lab, kind="label", border=B_ROW, bold=bold)
        for c, f in zip("EFG", fs):
            put(ws, f"{c}{rr}", f, fmt=fmt, border=B_ROW, bold=bold, align="center" if fmt is None else None)
        put(ws, f"I{rr}", unit, kind="muted", border=B_ROW)
        for c in "DH":
            ws[f"{c}{rr}"].border = B_ROW
    assert 27 + len(comp) - 1 == 41
    put(ws, "C42", f"All three scenarios reproduce their {X.v} control totals", kind="label", bold=True)
    put(ws, "G42", '=IF(COUNTIF(E39:G39,"OK")+COUNTIF(E41:G41,"OK")=6,"OK","CHECK")', bold=True, align="center")
    cf_checks(ws, "E39:G39")
    cf_checks(ws, "E41:G41")
    cf_checks(ws, "G42")
    source_line(ws, "C44", f"Source: pack_data.json {X.v} (cost_model.scenarios); levers on Inputs rows 10-15. "
                "Vendor estimates for notified-body fees are unverified. Illustrative.")
    ws.freeze_panes = "E9"
    print_setup(ws, HDR, area="A1:O44")

    # =====================================================================================
    # MONTHLY PLAN
    # =====================================================================================
    ws = ws_mp
    widths(ws, {"A": 2.5, "B": 12, "C": 11, "D": 11, "E": 14, "F": 15, "G": 14, "H": 15, "I": 13, "J": 11, "K": 17,
                "L": 16, "M": 9, "N": 3, "O": 10, "P": 13, "Q": 13})
    title_block(ws, LABEL + " · MONTHLY PLAN",
                '="Spend to date is EUR "&TEXT(G27/1000,"#,##0")&"k against a plan of EUR "&TEXT(E27/1000,"#,##0")&"k ('
                '"&TEXT(J27,"+0.0%;-0.0%")&"), "&IF(ABS(J27)<=E6,"inside","outside")&" the ±"&TEXT(E6,"0%")&" tolerance"',
                "Monthly phasing of the one-off budget (incl. contingency) for the active scenario · Actuals from Finance · "
                "EUR · Illustrative", link_col="Q")
    band(ws, 5, "Parameters", "B", "M")
    put(ws, "B6", "Variance tolerance (KPI K11)", kind="label")
    put(ws, "E6", 0.10, kind="input", fmt=NF_PCT0)
    put(ws, "B7", "Plan follows the active scenario", kind="label")
    put(ws, "E7", "=Inputs!$D$6", align="right", bold=True)
    band(ws, 9, "Monthly phasing, plan and actuals", "B", "M")
    header(ws, 10, ["Month", "Period", "Phasing weight", "Plan (EUR)", "Cumulative plan (EUR)", "Actual (EUR)",
                    "Cumulative actual (EUR)", "Variance (EUR)", "Variance (%)", "Tolerance status",
                    f"Control: cumulative plan {X.v}", "Check"], "B", height=32)
    for c in "DEFGHIJLM":
        ws[f"{c}10"].alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    q4w = [0.27, 0.33, 0.40]
    y27w = [0.055, 0.065, 0.075, 0.085, 0.09, 0.095, 0.095, 0.09, 0.09, 0.09, 0.09, 0.08]
    months = [dt.date(2026, 10, 1), dt.date(2026, 11, 1), dt.date(2026, 12, 1)] + [dt.date(2027, m, 1) for m in range(1, 13)]
    weights = q4w + y27w
    for i, (mo, w) in enumerate(zip(months, weights)):
        rr = 11 + i
        put(ws, f"B{rr}", mo, kind="label", fmt=NF_MONTH, border=B_ROW, align="left")
        put(ws, f"C{rr}", f'=IF(YEAR(B{rr})=2026,"Q4 2026","2027")', border=B_ROW)
        put(ws, f"D{rr}", w, kind="input", fmt=NF_PCT1, border=B_ROW)
        put(ws, f"E{rr}", f'=D{rr}*IF(C{rr}="Q4 2026",\'Cost build\'!$F$31,\'Cost build\'!$G$31)', fmt=NF_EUR, border=B_ROW)
        put(ws, f"F{rr}", f"=SUM($E$11:E{rr})", fmt=NF_EUR, border=B_ROW)
        if i == 0:
            put(ws, f"G{rr}", CM["actual_to_date"]["actual"], kind="input", fmt=NF_EUR, border=B_ROW)
        else:
            put(ws, f"G{rr}", None, kind="input", fmt=NF_EUR, border=B_ROW)
        put(ws, f"H{rr}", f'=IF(G{rr}="","",SUM($G$11:G{rr}))', fmt=NF_EUR, border=B_ROW)
        put(ws, f"I{rr}", f'=IF(G{rr}="","",G{rr}-E{rr})', fmt=NF_EUR, border=B_ROW)
        put(ws, f"J{rr}", f'=IF(G{rr}="","",I{rr}/E{rr})', fmt='+0.0%;-0.0%;0.0%', border=B_ROW)
        put(ws, f"K{rr}", f'=IF(G{rr}="","",IF(ABS(J{rr})<=$E$6,"Within tolerance","Outside tolerance"))', border=B_ROW)
        put(ws, f"L{rr}", CM["monthly_plan"][i]["cumulative_plan"], kind="input", fmt=NF_EUR, border=B_ROW)
        put(ws, f"M{rr}", f'=IF(Inputs!$D$6<>"Base","n/a",IF(ABS(F{rr}-L{rr})<1,"OK","CHECK"))', border=B_ROW,
            align="center")
        # chart helpers (EUR m)
        put(ws, f"O{rr}", f'=TEXT(B{rr},"mmm yy")', kind="muted", size=8)
        put(ws, f"P{rr}", f"=F{rr}/1000000", fmt="0.0", kind="muted", size=8)
        put(ws, f"Q{rr}", f'=IF(H{rr}="","",H{rr}/1000000)', fmt="0.0", kind="muted", size=8)
    add_table(ws, "tblMonthlyPlan", "B10:M25")
    cf_checks(ws, "M11:M25")
    cf_text(ws, "K11:K25", "Within tolerance", C["green"])
    cf_text(ws, "K11:K25", "Outside tolerance", C["red"])
    put(ws, "B26", "Total", kind="label", bold=True, border=B_TOTAL)
    put(ws, "E26", "=SUM(E11:E25)", fmt=NF_EUR, bold=True, border=B_TOTAL)
    put(ws, "G26", "=SUM(G11:G25)", fmt=NF_EUR, bold=True, border=B_TOTAL)
    for c in "CDFHIJKLM":
        ws[f"{c}26"].border = B_TOTAL
    put(ws, "B27", "To date (months with actuals)", kind="label", bold=True)
    put(ws, "E27", '=SUMPRODUCT((G11:G25<>"")*E11:E25)', fmt=NF_EUR, bold=True)
    put(ws, "G27", "=G26", fmt=NF_EUR, bold=True)
    put(ws, "I27", "=G27-E27", fmt=NF_EUR, bold=True)
    put(ws, "J27", "=IF(E27=0,0,I27/E27)", fmt='+0.0%;-0.0%;0.0%', bold=True)
    put(ws, "K27", '=IF(ABS(J27)<=$E$6,"Within tolerance","Outside tolerance")', bold=True)
    cf_text(ws, "K27", "Within tolerance", C["green"])
    cf_text(ws, "K27", "Outside tolerance", C["red"])
    band(ws, 29, "Checks", "B", "M")
    mchecks = [
        ("Q4 2026 phasing weights sum to 100%", '=SUMIF(C11:C25,"Q4 2026",D11:D25)', NF_PCT1,
         '=IF(ABS(E30-1)<0.000001,"OK","CHECK")'),
        ("2027 phasing weights sum to 100%", '=SUMIF(C11:C25,"2027",D11:D25)', NF_PCT1,
         '=IF(ABS(E31-1)<0.000001,"OK","CHECK")'),
        ("Plan total equals the one-off total incl. contingency (Cost build)", "=E26-'Cost build'!$H$31", NF_EUR2,
         '=IF(ABS(E32)<0.5,"OK","CHECK")'),
        (f"Cumulative plan reproduces {X.v} phasing (Base only)", '=COUNTIF(M11:M25,"OK")', "0",
         '=IF(Inputs!$D$6<>"Base","n/a",IF(E33=15,"OK","CHECK"))'),
    ]
    for i, (lab, f, fmt, chk) in enumerate(mchecks):
        rr = 30 + i
        put(ws, f"B{rr}", lab, kind="label", border=B_ROW)
        put(ws, f"L{rr}", f, fmt=fmt, border=B_ROW)
        put(ws, f"M{rr}", chk.replace("E3", "L3"), border=B_ROW, align="center", bold=True)
        for c in "CDEFGHIJK":
            ws[f"{c}{rr}"].border = B_ROW
    cf_checks(ws, "M30:M33")
    put(ws, "O10", "Chart data (EUR m)", kind="muted", size=8, bold=True)
    put(ws, "P10", "Cumulative plan", kind="muted", size=8, bold=True, wrap=True)
    put(ws, "Q10", "Cumulative actual", kind="muted", size=8, bold=True, wrap=True)
    source_line(ws, "B35", f"Source: pack_data.json {X.v} (cost_model.monthly_plan, actual_to_date). Phasing weights "
                f"reproduce the {X.v} monthly plan exactly for Base. Enter each month's actual in column G. Illustrative.")
    ws.freeze_panes = "C11"
    print_setup(ws, HDR, title_rows="10:10", area="A1:M35")

    # =====================================================================================
    # EXPOSURE
    # =====================================================================================
    ws = ws_ex
    widths(ws, {"A": 2.5, "B": 52, "C": 14, "D": 14, "E": 14, "F": 14, "G": 14, "H": 16, "I": 56})
    title_block(ws, LABEL + " · EXPOSURE",
                '="EUR "&TEXT(C24,"#,##0")&"m of EU revenue needs a notified body; maximum fines reach EUR "&TEXT(G7,"0")&"m"',
                '="Illustrative · Worldwide turnover EUR "&TEXT(' + IN["rev_total"] + ',"#,##0")&"m (Inputs) · '
                f'Regulation (EU) 2024/2847 · Facts as at {X.facts}"', link_col="I")
    band(ws, 5, f"1. Maximum administrative fines (Art 64), applied to {X.client} turnover", "B", "I")
    header(ws, 6, ["Tier", "Basis", "Fixed cap (EUR m)", "% of worldwide turnover", "% x turnover (EUR m)",
                   "Maximum fine (EUR m)", "Turnover above which % applies (EUR m)", "Breaches covered"], "B", height=32)
    for c in "DEFGH":
        ws[f"{c}6"].alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    tiers = D["exposure"]["fine_tiers"]
    covers = ["Annex I essential requirements; manufacturer obligations in Arts 13 and 14",
              "Arts 18-23, 28, 30(1)-(4), 31(1)-(4), 32(1)-(3), 33(5), 39, 41, 47, 49 and 53",
              "Incorrect, incomplete or misleading information to notified bodies or market surveillance authorities"]
    for i, t in enumerate(tiers):
        rr = 7 + i
        put(ws, f"B{rr}", t["tier"], kind="label", border=B_ROW, wrap=True, bold=True)
        put(ws, f"C{rr}", t["basis"], kind="label", border=B_ROW)
        put(ws, f"D{rr}", t["fixed_m"], kind="input", fmt=NF_EUR1, border=B_ROW)
        put(ws, f"E{rr}", t["pct"] / 100, kind="input", fmt=NF_PCT1, border=B_ROW)
        put(ws, f"F{rr}", f"=E{rr}*{IN['rev_total']}", fmt=NF_EUR1, border=B_ROW)
        put(ws, f"G{rr}", f"=MAX(D{rr},F{rr})", kind="output", fmt=NF_EUR1)
        put(ws, f"H{rr}", f"=D{rr}/E{rr}", fmt=NF_EUR, border=B_ROW)
        put(ws, f"I{rr}", covers[i], kind="muted", border=B_ROW, wrap=True, size=8)
        ws.row_dimensions[rr].height = 28
    put(ws, "B10", D["exposure"]["note"], kind="muted", size=8, wrap=True)
    ws.merge_cells("B10:I10")
    ws.row_dimensions[10].height = 26

    band(ws, 12, "2. EU revenue by CRA class (planning basis)", "B", "I")
    header(ws, 13, ["Class", "Families", "Revenue (EUR m)", "EU revenue (EUR m)", "Share of EU revenue",
                    "Needs a notified body", "", "Notes"], "B", height=32)
    for c in "CDEF":
        ws[f"{c}13"].alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    classes = [("Default", "No", f"Includes {PROV_LABELS}, provisional pending the legal opinion (due {LEGAL_DUE})" if PROV else ""),
               ("Class I", "Yes", f"Module A only once a harmonised standard is cited and applied in full; none cited as at {X.facts}"),
               ("Class II", "Yes", "Module B+C, Module H or an EU scheme at 'substantial' or higher"),
               ("Critical", "Yes", f"None in the {X.client} portfolio" if not CRIT else join(X.labels(CRIT)))]
    for i, (cl, nbq, note) in enumerate(classes):
        rr = 14 + i
        put(ws, f"B{rr}", cl, kind="label", border=B_ROW)
        put(ws, f"C{rr}", f'=COUNTIF({FAM["cls"]},B{rr})', fmt=NF_INT, border=B_ROW)
        put(ws, f"D{rr}", f'=SUMIF({FAM["cls"]},B{rr},{FAM["rev"]})', fmt=NF_EUR1, border=B_ROW)
        put(ws, f"E{rr}", f'=SUMIF({FAM["cls"]},B{rr},{FAM["eu"]})', fmt=NF_EUR1, border=B_ROW)
        put(ws, f"F{rr}", f"=E{rr}/$E$20", fmt=NF_PCT1, border=B_ROW)
        put(ws, f"G{rr}", nbq, kind="label", border=B_ROW, align="center")
        put(ws, f"I{rr}", note, kind="muted", size=8, border=B_ROW, wrap=True)
        ws["H%d" % rr].border = B_ROW
        ws.row_dimensions[rr].height = 24
    put(ws, "B18", "Families in scope", kind="label", bold=True, border=B_SUB)
    for c in "CDE":
        put(ws, f"{c}18", f"=SUM({c}14:{c}17)", fmt=NF_EUR1 if c != "C" else NF_INT, bold=True, border=B_SUB)
    put(ws, "F18", "=E18/$E$20", fmt=NF_PCT1, bold=True, border=B_SUB)
    for c in "GHI":
        ws[f"{c}18"].border = B_SUB
    put(ws, "B19", "Other revenue: cloud platform (remote data processing, not a family)", kind="label", border=B_ROW)
    put(ws, "D19", f"=Inputs!$K${SAAS_ROW}", fmt=NF_EUR1, border=B_ROW)
    put(ws, "E19", f"=Inputs!$M${SAAS_ROW}", fmt=NF_EUR1, border=B_ROW)
    put(ws, "F19", "=E19/$E$20", fmt=NF_PCT1, border=B_ROW)
    for c in "CGHI":
        ws[f"{c}19"].border = B_ROW
    put(ws, "B20", f"{X.client} total", kind="label", bold=True, border=B_TOTAL)
    put(ws, "D20", "=D18+D19", fmt=NF_EUR1, bold=True, border=B_TOTAL)
    put(ws, "E20", "=E18+E19", fmt=NF_EUR1, bold=True, border=B_TOTAL)
    put(ws, "F20", "=E20/$E$20", fmt=NF_PCT1, bold=True, border=B_TOTAL)
    put(ws, "I20", f'=IF(ABS(D20-{IN["rev_total"]})+ABS(E20-{IN["eu_rev_total"]})<0.001,"Reconciles to Inputs","Check against Inputs")',
        kind="muted", size=8, border=B_TOTAL)
    for c in "CGH":
        ws[f"{c}20"].border = B_TOTAL

    band(ws, 22, "3. Market access exposure", "B", "I")
    header(ws, 23, ["Measure", "Value", "Unit", "Basis"], "B", height=20)
    ws["C23"].alignment = Alignment(horizontal="right", vertical="center")
    for c in "FGHI":
        ws[f"{c}23"].fill = fill(C["ink900"])
    mae = [
        ("EU revenue needing a notified body (Class I, II, critical)", "=E15+E16+E17", NF_EUR1, "EUR m",
         f"Headline '{eur_m0(X.eu_nb_m)}': {words(NB_N)} famil{'ies' if NB_N != 1 else 'y'} cannot be placed on the EU market from 11 Dec 2027 without third-party assessment"),
        ("as % of group revenue", f"=C24/{IN['rev_total']}", NF_PCT1, "%", f"Headline '{X.eu_nb_share:.0%} of group revenue'"),
        ("as % of EU revenue", "=C24/E20", NF_PCT1, "%", "Derived"),
        ("Families needing a notified body", "=C15+C16+C17", NF_INT, "families", ", ".join(X.labels(X.nb_fams))),
        (f"EU revenue of provisional families ({PROV_LABELS_C or 'none'})",
         f'=SUMIF({FAM["rec"]},"Default (provisional)",{FAM["eu"]})', NF_EUR1, "EUR m",
         SENS_TXT),
        (f"EU revenue needing a notified body if {BOTH} Class I", "=C24+C28", NF_EUR1, "EUR m", "Derived sensitivity"),
        (f"as % of group revenue (if {BOTH} Class I)", f"=C29/{IN['rev_total']}", NF_PCT1, "%", "Derived sensitivity"),
        (f"Days from {X.issue} to full application on 11 Dec 2027", f"=DATE(2027,12,11)-DATE({X.issue_date.year},{X.issue_date.month},{X.issue_date.day})",
         "0", "days", f"Art 71(2); {X.days_board} days from the {X.board} board"),
    ]
    for i, (lab, f, fmt, unit, basis) in enumerate(mae):
        rr = 24 + i
        put(ws, f"B{rr}", lab, kind="label", border=B_ROW, bold=(i == 0))
        put(ws, f"C{rr}", f, fmt=fmt, border=B_ROW, bold=(i == 0))
        put(ws, f"D{rr}", unit, kind="muted", border=B_ROW, indent=1)
        put(ws, f"E{rr}", basis, kind="muted", size=8, border=B_ROW)
        for c in "FGHI":
            ws[f"{c}{rr}"].border = B_ROW
    assert 24 + len(mae) - 1 == 31
    ws["C24"].fill = fill(C["acc100"])

    band(ws, 33, "4. Legacy lines still sold in the EU after 11 Dec 2027" + (f" (board decision {LEG_BD})" if LEG_BD else ""), "B", "I")
    header(ws, 34, ["Line", "BU", "Units in field (k)", "EU revenue (EUR m)", "Still sold after 11 Dec 2027", "", "",
                    "Status"], "B", height=32)
    for c in "DE":
        ws[f"{c}34"].alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    leg = LEG
    if not leg:
        put(ws, "B35", "None: no legacy line is still sold in the EU after 11 Dec 2027", kind="muted", border=B_ROW)
        put(ws, "E35", 0, kind="input", fmt=NF_EUR1, border=B_ROW)
        for c in "CDFGHI":
            ws[f"{c}35"].border = B_ROW
    LT = 35 + max(NLEG, 1)
    EXP_LEG = f"E{LT}"
    for i, l in enumerate(leg):
        rr = 35 + i
        put(ws, f"B{rr}", l["name"], kind="label", border=B_ROW)
        put(ws, f"C{rr}", l["bu"], kind="label", border=B_ROW)
        put(ws, f"D{rr}", l["units_in_field_k"], kind="input", fmt=NF_EUR, border=B_ROW)
        put(ws, f"E{rr}", l["eu_revenue_m"], kind="input", fmt=NF_EUR1, border=B_ROW)
        put(ws, f"F{rr}", "Yes", kind="label", border=B_ROW, align="center")
        put(ws, f"I{rr}", l["status"], kind="muted", size=8, border=B_ROW)
        for c in "GH":
            ws[f"{c}{rr}"].border = B_ROW
    LINES_TXT = f"{words(NLEG)} line{'s' if NLEG != 1 else ''}"
    put(ws, f"B{LT}", f"EU revenue at stake ({LINES_TXT}, a year)", kind="label", bold=True, border=B_SUB)
    put(ws, f"E{LT}", f"=SUM(E35:E{LT - 1})", fmt=NF_EUR1, bold=True, border=B_SUB)
    put(ws, f"B{LT + 1}", "Remediation estimate, plus notified-body fees (EUR m)", kind="label", border=B_ROW)
    put(ws, f"E{LT + 1}", LEG_REC.get("remediation_cost_estimate_m", 0), kind="input", fmt=NF_EUR1, border=B_ROW)
    put(ws, f"B{LT + 2}", f"Remediation as % of the {LINES_TXT}' annual EU revenue" if NLEG != 1 else
        "Remediation as % of the line's annual EU revenue", kind="label", border=B_ROW)
    put(ws, f"E{LT + 2}", f"=E{LT + 1}/E{LT}" if NLEG else f"=IF(E{LT}=0,0,E{LT + 1}/E{LT})", fmt=NF_PCT1, border=B_ROW)
    for rr in (LT, LT + 1, LT + 2):
        for c in "CDFGHI":
            ws[f"{c}{rr}"].border = B_SUB if rr == LT else B_ROW
    put(ws, f"B{LT + 3}", "Recommendation: " + LEG_REC.get("recommendation", "none recorded"), kind="label", wrap=True, size=8)
    ws.merge_cells(f"B{LT + 3}:I{LT + 3}")
    ws.row_dimensions[LT + 3].height = 26
    put(ws, f"B{LT + 4}", f"All {words(len(X.legacy))} legacy lines stay in the Art 14 reportable inventory (Art 69(3)); reporting continues after "
        "support ends (guidance para 210).", kind="muted", size=8)

    band(ws, LT + 6, "5. Product liability (Directive (EU) 2024/2853)", "B", "I")
    put(ws, f"B{LT + 7}", D["exposure"]["product_liability"], kind="label", wrap=True, size=8, valign="top")
    ws.merge_cells(f"B{LT + 7}:I{LT + 7}")
    ws.row_dimensions[LT + 7].height = 30
    source_line(ws, f"B{LT + 9}", f"Source: pack_data.json {X.v} (exposure, client); Regulation (EU) 2024/2847 Arts 64, 69, 71; "
                f"knowledge base (Enforcement; Conformity), facts as at {X.facts}. Derived sensitivities labelled. Illustrative.")
    ws.freeze_panes = "A5"
    print_setup(ws, HDR, area=f"A1:I{LT + 9}")

    # =====================================================================================
    # SUMMARY
    # =====================================================================================
    ws = ws_sum
    for c in col_range("B", "Q"):
        ws.column_dimensions[c].width = 11.5
    ws.column_dimensions["A"].width = 2.5
    ws.column_dimensions["R"].width = 3
    for c in "STU":
        ws.column_dimensions[c].width = 16
    title_block(ws, LABEL + " · SUMMARY",
                f'="{X.codename} needs EUR "&TEXT(\'Cost build\'!H31/1000000,"0.0")&"m to Dec 2027 and EUR "&TEXT('
                '\'Cost build\'!I31/1000000,"0.0")&"m a year to run: "&TEXT(\'Cost build\'!H33,"0.00%")&" of one year\'s revenue"',
                f'="Scenario shown: "&Inputs!$D$6&" · EUR, real 2026 terms, excl. VAT · {X.engagement}"', link_col="Q")
    tiles = [
        ("ONE-OFF TO DEC 2027", "='Cost build'!H31", NF_EURM_SCALED,
         f'="incl. "&TEXT({LEV("cont", "G")},"0%")&" contingency"'),
        ("Q4 2026", "='Cost build'!F31", NF_EURM_SCALED, "Oct to Dec 2026, incl. contingency"),
        ("2027", "='Cost build'!G31", NF_EURM_SCALED, "Jan to Dec 2027, incl. contingency"),
        ("RUN-RATE FROM 2028", "='Cost build'!I31", NF_EURM_SCALED, "a year; no contingency"),
        ("SHARE OF REVENUE", "='Cost build'!H33", NF_PCT2, '="one-off; run-rate "&TEXT(\'Cost build\'!I33,"0.00%")'),
        ("EU REVENUE NEEDING A NOTIFIED BODY", "=Exposure!C24", '"EUR "#,##0"m"',
         f'=TEXT(Exposure!C25,"0%")&" of group revenue; {NB_N} families"'),
        ("MODEL CHECKS", "='Cost build'!L58", None, f"integrity and {X.v} reconciliation"),
    ]
    white_sep = Border(right=Side(style="thick", color=C["white"]))
    for i, (lab, val, fmt, sub) in enumerate(tiles):
        c1 = get_column_letter(2 + 2 * i)
        c2 = get_column_letter(3 + 2 * i)
        for rr in (5, 6, 7):
            ws.merge_cells(f"{c1}{rr}:{c2}{rr}")
            for cc in (c1, c2):
                ws[f"{cc}{rr}"].fill = fill(C["ink100"])
                ws[f"{cc}{rr}"].border = white_sep if cc == c2 else Border()
        put(ws, f"{c1}5", lab, kind="label", bold=True, size=7, color=C["ink500"], wrap=True, fill_hex=C["ink100"],
            valign="bottom")
        put(ws, f"{c1}6", val, fmt=fmt, bold=True, size=16, color=C["acc600"], fill_hex=C["ink100"], align="left")
        put(ws, f"{c1}7", sub, kind="muted", size=7, wrap=True, fill_hex=C["ink100"], valign="top", color=C["ink500"])
        ws[f"{c2}5"].border = white_sep
        ws[f"{c2}6"].border = white_sep
        ws[f"{c2}7"].border = white_sep
    ws.row_dimensions[5].height = 24
    ws.row_dimensions[6].height = 30
    ws.row_dimensions[7].height = 24
    cf_checks(ws, "N6")

    # workstream table
    band(ws, 9, "Investment by workstream (EUR, active scenario)", "B", "I")
    header(ws, 10, ["Workstream", "", "", "Q4 2026", "2027", "One-off", "Share", "Run 2028"], "B", height=20)
    ws.merge_cells("B10:D10")
    for c in "EFGHI":
        ws[f"{c}10"].alignment = Alignment(horizontal="right", vertical="center")
    WSN = ["Programme & governance", "Reporting & PSIRT", "Secure engineering", "Shared platforms",
           "Documentation & evidence", "Conformity & market access", "People & change", "Supply chain"]
    for i, w in enumerate(WSN):
        rr = 11 + i
        ws.merge_cells(f"B{rr}:D{rr}")
        put(ws, f"B{rr}", w, kind="label", border=B_ROW)
        put(ws, f"E{rr}", f"=SUMIF('Cost build'!$C$18:$C$28,$B{rr},'Cost build'!F$18:F$28)", fmt=NF_EUR, border=B_ROW)
        put(ws, f"F{rr}", f"=SUMIF('Cost build'!$C$18:$C$28,$B{rr},'Cost build'!G$18:G$28)", fmt=NF_EUR, border=B_ROW)
        put(ws, f"G{rr}", f"=E{rr}+F{rr}", fmt=NF_EUR, border=B_ROW)
        put(ws, f"H{rr}", f"=G{rr}/$G$19", fmt=NF_PCT0, border=B_ROW)
        put(ws, f"I{rr}", f"=SUMIF('Cost build'!$C$18:$C$28,$B{rr},'Cost build'!I$18:I$28)", fmt=NF_EUR, border=B_ROW)
        for c in "CD":
            ws[f"{c}{rr}"].border = B_ROW
    ws.merge_cells("B19:D19")
    put(ws, "B19", "Subtotal excl. contingency", kind="label", bold=True, border=B_SUB)
    for c in "EFGI":
        put(ws, f"{c}19", f"=SUM({c}11:{c}18)", fmt=NF_EUR, bold=True, border=B_SUB)
    put(ws, "H19", "=SUM(H11:H18)", fmt=NF_PCT0, bold=True, border=B_SUB)
    ws.merge_cells("B20:D20")
    put(ws, "B20", "Contingency", kind="label", border=B_ROW)
    put(ws, "E20", "='Cost build'!F30", fmt=NF_EUR, border=B_ROW)
    put(ws, "F20", "='Cost build'!G30", fmt=NF_EUR, border=B_ROW)
    put(ws, "G20", "=E20+F20", fmt=NF_EUR, border=B_ROW)
    put(ws, "I20", "-", kind="muted", border=B_ROW, align="right")
    ws.merge_cells("B21:D21")
    put(ws, "B21", "Total incl. contingency", kind="label", bold=True, border=B_TOTAL)
    put(ws, "E21", "=E19+E20", fmt=NF_EUR, bold=True, border=B_TOTAL)
    put(ws, "F21", "=F19+F20", fmt=NF_EUR, bold=True, border=B_TOTAL)
    put(ws, "G21", "=E21+F21", kind="output", fmt=NF_EUR)
    put(ws, "I21", "=I19", kind="output", fmt=NF_EUR)
    for c in "CDH":
        ws[f"{c}21"].border = B_TOTAL
    source_line(ws, "B22", f"Source: Cost build (11 lines), pack_data.json {X.v}. Illustrative.")

    # scenario table
    band(ws, 24, "Scenarios (EUR; computed independently of the selector)", "B", "I")
    header(ws, 25, ["Measure", "", "", "Low", "Base", "High", "", ""], "B", height=20)
    ws.merge_cells("B25:D25")
    for c in "EFG":
        ws[f"{c}25"].alignment = Alignment(horizontal="right", vertical="center")
    scen_rows = [("One-off to Dec 2027 incl. contingency", 27, NF_EUR, True),
                 ("of which Q4 2026", 28, NF_EUR, False), ("of which 2027", 29, NF_EUR, False),
                 ("Run-rate from 2028 (a year)", 31, NF_EUR, True), ("One-off vs Base", 32, NF_EUR, False),
                 ("Contingency rate", 30, NF_PCT0, False)]
    for i, (lab, srow, fmt, bold) in enumerate(scen_rows):
        rr = 26 + i
        ws.merge_cells(f"B{rr}:D{rr}")
        put(ws, f"B{rr}", lab, kind="label", border=B_ROW, bold=bold)
        for c in "EFG":
            put(ws, f"{c}{rr}", f"=Scenarios!{c}{srow}", fmt=fmt, border=B_ROW, bold=bold)
        for c in "CDHI":
            ws[f"{c}{rr}"].border = B_ROW
    for i, (k, nm) in enumerate([("low", "Low"), ("base", "Base"), ("high", "High")]):
        rr = 32 + i
        ws.merge_cells(f"B{rr}:I{rr}")
        put(ws, f"B{rr}", f"{nm}: {SC[k]['description']}", kind="muted", size=8, wrap=True)
        ws.row_dimensions[rr].height = 22
    source_line(ws, "B35", "Source: Scenarios sheet; levers on Inputs. Notified-body fees are vendor estimates, unverified. Illustrative.")

    # exposure table
    band(ws, 37, "Exposure (Illustrative)", "B", "I")
    header(ws, 38, ["Measure", "", "", "Value", "Unit", "Basis", "", ""], "B", height=20)
    ws.merge_cells("B38:D38")
    ws["F38"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws["E38"].alignment = Alignment(horizontal="right", vertical="center")
    exr = [
        ("Maximum fine, Tier 1 (Annex I; Arts 13-14)", "=Exposure!G7", NF_EUR1, "EUR m", "Art 64(2): EUR 15m or 2.5% of turnover"),
        ("Maximum fine, Tier 2 (other obligations)", "=Exposure!G8", NF_EUR1, "EUR m", "Art 64(3): EUR 10m or 2%"),
        ("Maximum fine, Tier 3 (misleading information)", "=Exposure!G9", NF_EUR1, "EUR m", "Art 64(4): EUR 5m or 1%"),
        ("EU revenue needing a notified body", "=Exposure!C24", NF_EUR1, "EUR m", f"{Words(NB_N)} {NB_CLASS_TXT} famil{'ies' if NB_N != 1 else 'y'}"),
        ("as % of group revenue", "=Exposure!C25", NF_PCT0, "%", f"{X.nb_status}"),
        (f"Legacy {join([X.label(l) for l in LEG]) or 'lines'}: EU revenue", f"=Exposure!{EXP_LEG}", NF_EUR1, "EUR m",
         f"vs about EUR {LEG_REC.get('remediation_cost_estimate_m', 0):,.1f}m remediation: {LEG_VERB}" + (f" ({LEG_BD})" if LEG_BD else "")),
        (f"Days from {X.issue} to 11 Dec 2027", "=Exposure!C31", "0", "days", f"{X.days_board} days from the {X.board} board"),
    ]
    for i, (lab, f, fmt, unit, basis) in enumerate(exr):
        rr = 39 + i
        ws.merge_cells(f"B{rr}:D{rr}")
        put(ws, f"B{rr}", lab, kind="label", border=B_ROW)
        put(ws, f"E{rr}", f, fmt=fmt, border=B_ROW)
        put(ws, f"F{rr}", unit, kind="muted", border=B_ROW, indent=1)
        put(ws, f"G{rr}", basis, kind="muted", size=8, border=B_ROW)
        for c in "CDHI":
            ws[f"{c}{rr}"].border = B_ROW
    source_line(ws, "B46", f"Source: Exposure sheet; Regulation (EU) 2024/2847 Art 64; pack_data.json {X.v}. Illustrative.")

    # chart data (outside print area)
    put(ws, "S9", "Chart data (EUR m)", kind="muted", bold=True, size=8)
    put(ws, "S10", "Workstream (sorted)", kind="muted", bold=True, size=8)
    put(ws, "T10", "One-off excl. contingency", kind="muted", bold=True, size=8, wrap=True)
    put(ws, "V10", "Sort key (hidden helper)", kind="muted", bold=True, size=8)
    for i in range(8):
        rr = 11 + i
        put(ws, f"V{rr}", f"=G{rr}+ROW()/1000000000", kind="muted", size=8, fmt="0.000")
    ws.column_dimensions["V"].hidden = True
    for i in range(8):
        rr = 11 + i
        put(ws, f"T{rr}", f"=INDEX($G$11:$G$18,MATCH(LARGE($V$11:$V$18,{i + 1}),$V$11:$V$18,0))/1000000", kind="muted", size=8, fmt="0.0")
        put(ws, f"S{rr}", f"=INDEX($B$11:$B$18,MATCH(LARGE($V$11:$V$18,{i + 1}),$V$11:$V$18,0))", kind="muted", size=8)
    put(ws, "S25", "Scenario", kind="muted", bold=True, size=8)
    put(ws, "T25", "One-off to Dec 2027", kind="muted", bold=True, size=8, wrap=True)
    put(ws, "U25", "Run-rate from 2028", kind="muted", bold=True, size=8, wrap=True)
    for i, c in enumerate("EFG"):
        rr = 26 + i
        put(ws, f"S{rr}", ["Low", "Base", "High"][i], kind="muted", size=8)
        put(ws, f"T{rr}", f"={c}26/1000000", kind="muted", size=8, fmt="0.0")
        put(ws, f"U{rr}", f"={c}29/1000000", kind="muted", size=8, fmt="0.0")

    # Chart 1: one-off by workstream (sorted, horizontal bars)
    ch1 = BarChart()
    ch1.type = "bar"
    ch1.grouping = "clustered"
    ch1.title = chart_title("One-off by workstream, excl. contingency (EUR m)")
    d1 = Reference(ws, min_col=20, min_row=10, max_row=18)
    c1r = Reference(ws, min_col=19, min_row=11, max_row=18)
    ch1.add_data(d1, titles_from_data=True)
    ch1.set_categories(c1r)
    color_series(ch1.series[0], C["acc600"])
    ch1.dataLabels = data_labels(fmt="0.0", pos="outEnd")
    style_axes(ch1, y_fmt="0.0", gridlines=False)
    ch1.x_axis.scaling.orientation = "maxMin"
    ch1.y_axis.delete = True
    ch1.legend = None
    ch1.gapWidth = 60
    ch1.width = 15.5
    ch1.height = 7.2
    ws.add_chart(ch1, "K9")

    # Chart 2: scenario comparison
    ch2 = BarChart()
    ch2.type = "col"
    ch2.grouping = "clustered"
    ch2.title = chart_title("Scenarios: one-off to Dec 2027 vs annual run-rate (EUR m)")
    d2 = Reference(ws, min_col=20, max_col=21, min_row=25, max_row=28)
    c2r = Reference(ws, min_col=19, min_row=26, max_row=28)
    ch2.add_data(d2, titles_from_data=True)
    ch2.set_categories(c2r)
    color_series(ch2.series[0], C["acc600"])
    color_series(ch2.series[1], C["navy"])
    ch2.dataLabels = data_labels(fmt="0.0", pos="outEnd")
    style_axes(ch2, y_fmt="0", gridlines=True)
    ch2.legend.position = "b"
    ch2.gapWidth = 80
    ch2.width = 15.5
    ch2.height = 7.2
    ws.add_chart(ch2, "K24")

    # Chart 3: cumulative plan (line) vs actual (columns)
    ch3 = BarChart()
    ch3.type = "col"
    ch3.title = chart_title("Cumulative spend: plan vs actual (EUR m)")
    d3a = Reference(ws_mp, min_col=17, min_row=10, max_row=25)
    cats = Reference(ws_mp, min_col=15, min_row=11, max_row=25)
    ch3.add_data(d3a, titles_from_data=True)
    ch3.set_categories(cats)
    color_series(ch3.series[0], C["navy"])
    ln = LineChart()
    d3b = Reference(ws_mp, min_col=16, min_row=10, max_row=25)
    ln.add_data(d3b, titles_from_data=True)
    ln.set_categories(cats)
    color_series(ln.series[0], C["acc600"], line=True)
    ln.series[0].marker.symbol = "none"
    style_axes(ch3, y_fmt="0", gridlines=True)
    ch3.gapWidth = 50
    ch3 += ln
    ch3.legend.position = "b"
    ch3.width = 15.5
    ch3.height = 7.2
    ws.add_chart(ch3, "K37")
    ws.freeze_panes = "A4"
    print_setup(ws, HDR, area="A1:Q51", fit_height=1)

    # =====================================================================================
    # BENCHMARKS
    # =====================================================================================
    ws = ws_bm
    widths(ws, {"A": 2.5, "B": 6, "C": 30, "D": 30, "E": 11, "F": 11, "G": 34, "H": 20, "I": 10, "J": 14, "K": 30,
                "L": 46})
    title_block(ws, LABEL + " · BENCHMARKS",
                "The model's notified-body unit costs sit inside the published ranges, but every benchmark is thin and unverified",
                "External reference points, labelled by type (commentary, vendor estimate, independent model, survey). "
                "None is a quote · Illustrative", link_col="L")
    header(ws, 5, ["ID", "Item", "Benchmark value", "Low (EUR)", "High (EUR)", "Source", "Type", "Date",
                   "Model value (EUR)", "Model vs benchmark", "Notes / URL"], "B", height=32)
    for c in "EFJ":
        ws[f"{c}5"].alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    bms = [
        ("B01", "Module B examination (per type)", "EUR 20,000-60,000", 20000, 60000, "CRA Decoded",
         "Commentary (unverified)", "2026", f"={IN['nb_b_unit']}", "range",
         "https://cra-decoded.com/blog/posts/cra-notified-body-capacity-crisis/"),
        ("B02", "Module B examination (alternative range)", "EUR 15,000-80,000", 15000, 80000, "sota.io",
         "Vendor estimate (unsourced)", "2026", f"={IN['nb_b_unit']}", "range", "Cited in the knowledge base (Programme budget guide)"),
        ("B03", "First Module H engagement", "EUR 80,000-150,000; surveillance every 1-2 years", 80000, 150000, "CRA Decoded",
         "Commentary (unverified)", "2026", f"={IN['nb_h_init']}", "range",
         "https://cra-decoded.com/blog/posts/cra-notified-body-capacity-crisis/"),
        ("B04", "Three default products, medium readiness", "EUR 78,300 one-off; EUR 13,500 a year", None, None,
         "cyberresilienceact.eu cost calculator", "Independent model (illustrative)", "2026", None,
         "Not comparable: SME planning model at EUR 45 per hour; excludes programme, PSIRT and platform costs",
         "https://www.cyberresilienceact.eu/cra-compliance-cost-calculator/"),
        ("B05", "Expected cost increase", "50% of 12 companies expect <20% cost increase", None, None,
         "KONE-authored industrial study (arXiv 2505.14325)", "Survey (small sample)", "2024", None, "Context only",
         "https://arxiv.org/pdf/2505.14325"),
        ("B06", "CRA team size", "28% up to 10 people; 22% larger; 16% up to 3", None, None,
         "ONEKEY IoT/OT Cybersecurity Report 2026 (200 German industrial firms)", "Vendor survey", "Sep 2026",
         f"={LEV('pfte', 'G')}+{IN['psirt_fte']}", "team",
         "https://www.onekey.com/press-release/onkey-iot-ot-cybersecurity-report-2026-half-of-all-companies-have-formed-cra-teams"),
        ("B07", "Notified-body lead times", "12-18 months to designate a body; 2-4 months to contract; 3-6 months per Module B+C engagement",
         None, None, "CRA Decoded", "Commentary (unverified)", "2026", None,
         "Drives the Q1 2027 contracting milestones (M5, M7)", "https://cra-decoded.com/blog/posts/cra-notified-body-capacity-crisis/"),
    ]
    for i, (bid, item, val, lo, hi, src, typ, date, model, cmp_, notes) in enumerate(bms):
        rr = 6 + i
        put(ws, f"B{rr}", bid, kind="muted", border=B_ROW)
        put(ws, f"C{rr}", item, kind="label", border=B_ROW, wrap=True, bold=True)
        put(ws, f"D{rr}", val, kind="label", border=B_ROW, wrap=True)
        put(ws, f"E{rr}", lo, kind="input" if lo else "label", fmt=NF_EUR, border=B_ROW)
        put(ws, f"F{rr}", hi, kind="input" if hi else "label", fmt=NF_EUR, border=B_ROW)
        put(ws, f"G{rr}", src, kind="label", border=B_ROW, wrap=True)
        put(ws, f"H{rr}", typ, kind="label", border=B_ROW, wrap=True)
        put(ws, f"I{rr}", date, kind="label", border=B_ROW)
        if model:
            put(ws, f"J{rr}", model, fmt=NF_EUR if cmp_ == "range" else '0.0" FTE"', border=B_ROW)
        else:
            put(ws, f"J{rr}", "-", kind="muted", border=B_ROW, align="right")
        if cmp_ == "range":
            put(ws, f"K{rr}", f'=IF(AND(J{rr}>=E{rr},J{rr}<=F{rr}),"Within range","Outside range")', border=B_ROW)
        elif cmp_ == "team":
            put(ws, f"K{rr}", f'="Core team "&TEXT(J{rr},"General")&" FTE: "&IF(J{rr}<=10,"inside the \'up to 10\' band","above 10 people")',
                border=B_ROW, wrap=True)
        else:
            put(ws, f"K{rr}", cmp_, kind="muted", border=B_ROW, wrap=True, size=8)
        put(ws, f"L{rr}", notes, kind="muted", border=B_ROW, wrap=True, size=8)
        ws.row_dimensions[rr].height = 36
    BM_LAST = 6 + len(bms) - 1
    add_table(ws, "tblBenchmarks", f"B5:L{BM_LAST}")
    cf_text(ws, f"K6:K{BM_LAST}", "Within range", C["green"])
    cf_text(ws, f"K6:K{BM_LAST}", "Outside range", C["red"])
    source_line(ws, f"B{BM_LAST + 2}", f"Source: pack_data.json {X.v} (cost_model.benchmarks, research_datapoints RD06, RD08, "
                "RD09, RD12); knowledge base Programme budget guide. Labels as given; none verified. Illustrative.")
    ws.freeze_panes = "C6"
    print_setup(ws, HDR, title_rows="5:5", area=f"A1:L{BM_LAST + 2}")

    # =====================================================================================
    # ASSUMPTIONS LOG
    # =====================================================================================
    ws = ws_al
    widths(ws, {"A": 2.5, "B": 7, "C": 40, "D": 16, "E": 16, "F": 56, "G": 26, "H": 12, "I": 13, "J": 46})
    title_block(ws, LABEL + " · ASSUMPTIONS LOG",
                "Notified-body fees and remediation effort carry the least confidence and the most money",
                "Each assumption with its rationale, owner, confidence and date. Values link live to Inputs · Illustrative",
                link_col="J")
    header(ws, 5, ["ID", "Assumption", "Value (live)", "Unit", "Rationale", "Owner", "Confidence (H/M/L)", "Date logged",
                   "What would change it"], "B", height=32)
    ws["D5"].alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    LOGDATE = dt.date(2026, 10, 31)
    alog = [
        ("Loaded cost per programme FTE", "fte_prog", NF_EUR, "EUR per FTE-year",
         "Fully loaded internal rate (salary, social charges, overhead) for director, compliance lead, product security officer and PMO.",
         "CFO office", "H", "HR rate card update; external hires instead of internal moves."),
        ("Loaded cost per PSIRT FTE", "fte_psirt", NF_EUR, "EUR per FTE-year",
         X.t("d10.alog.psirt_rate", "Loaded rate for the incremental PSIRT roles (lead and analyst)."), "PSIRT lead", "H",
         "Market rate for the PSIRT lead hire."),
        ("Loaded cost per engineering FTE", "fte_eng", NF_EUR, "EUR per FTE-year",
         "Blended internal engineering rate applied to remediation effort.", "CTO", "H",
         "Use of contractors for documentation and testing (R02 mitigation)."),
        ("Programme team size (build)", None, None, "FTE",
         f"Director, compliance lead, product security officer and PMO ({words(LVL['pfte'][1])} FTE); {words(LVL['pfte'][2])} in the High scenario.",
         "Programme director", "M", (f"Wave 2 scope growth if {PROV_SHORTS} {'become' if NPROV > 1 else 'becomes'} Class I." if PROV else "Wave 2 scope growth if a family is reclassified upwards.")),
        ("Programme team size (run)", "prog_run_fte", "0.0", "FTE",
         "Compliance lead, product security officer and part-time PMO to run the evidence system from 2028.",
         "Programme director", "M", "Degree of automation achieved in the system of record."),
        ("PSIRT incremental capacity and on-call", "psirt_fte", "0.0", "FTE",
         X.t("d10.alog.psirt_capacity", f"Lead plus analyst on top of the existing PSIRT capacity; 24/7 on-call allowance of EUR {A['psirt_oncall_allowance'] / 1000:,.0f}k a year."), "PSIRT lead", "M",
         X.t("d10.alog.psirt_capacity_change", "Agreement on 24/7 on-call with employee representatives; case volumes after 11 Dec 2027.")),
        ("Remediation effort per Default family", "rem_def", "0.0", "FTE-years per family",
         f"Baseline gap analysis on the {PILOT} pilot extrapolated to default families (readiness {min(DEF_RI) * 100:.0f}-{max(DEF_RI) * 100:.0f}%).",
         "Product security officer", "M", "Signed Wave 2 risk assessments (P2) and applicability matrices."),
        ("Remediation effort per Class I family", "rem_i", "0.0", "FTE-years per family",
         "Higher assurance expectation and third-party assessment for Class I families.", "Product security officer", "M",
         f"Wave 1 gap lists from signed risk assessments (M6, {X.ms_date('M6')})."),
        ("Remediation effort per Class II family", "rem_ii", "0.0", "FTE-years per family",
         X.t("d10.alog.class_ii", f"{join(X.labels(CLASS2))} (Class II) carries the deepest Annex I scope." if CLASS2 else "Class II families carry the deepest Annex I scope."), "Product security officer", "M",
         "Module H pre-assessment findings."),
        ("Remediation phasing (Q4 2026 share)", "rem_q4", NF_PCT0, "%",
         f"Remediation starts in earnest with Phase P3 on {P3.get('start', '')}; Q4 2026 covers the {PILOT} pilot.", "CTO", "M",
         "Speed of release-gate enforcement (T16)."),
        ("Shared-platform build", None, None, "EUR",
         "SBOM/VEX/CSAF tooling EUR {sbom_vex_csaf_tooling}k, signing HSM and update infrastructure EUR {signing_hsm_update_infrastructure}k, system of record EUR {system_of_record}k, PSIRT tooling EUR {psirt_tooling_advisory_portal}k.".format(**{k: f"{v / 1000:,.0f}" for k, v in A["platforms_build_detail"].items()}),
         "Head of platform engineering", "M", f"Vendor quotes after system-of-record selection (T05, {X.task_end('T05')})."),
        ("Platform run cost and start", "plat_run", NF_EUR, "EUR per year",
         "Licences, hosting and support from mid-2027 (half a year in 2027).", "Head of platform engineering", "M",
         "Choice of open-source versus commercial tooling."),
        ("Risk assessment per family", "ra_cost", NF_EUR, "EUR per family",
         "TR-03183-1-style assessment with threat model and applicability matrix per family.", "Product security officer",
         "M", f"Reuse of templates from the {PILOT} pilot."),
        ("Security testing rates", "test_i", NF_EUR, "EUR per family-year (Class I shown)",
         "Penetration tests, fuzzing and re-tests: Default EUR {default}k, Class I EUR {class_i}k, Class II EUR {class_ii}k a year.".format(**{k: f"{v / 1000:,.0f}" for k, v in A["testing_per_family_per_year"].items()}),
         "Product security officer", "M", "Notified-body test expectations for Module B specimens."),
        ("Technical file and Annex II per family", "doc_cost", NF_EUR, "EUR per family",
         f"Annex VII file and Annex II information assembled from pipeline evidence; EUR {A['documentation_run_per_family'] / 1000:,.0f}k a year upkeep.",
         "Compliance lead", "M", "One file per family where guidance paras 174-177 allow."),
        ("Notified-body pre-assessments", "nb_pre_unit", NF_EUR, "EUR each",
         f"{Words(NBPRE['count'])} candidates at EUR {NBPRE['unit'] / 1000:,.0f}k (board authority up to EUR {NBPRE['count'] * NBPRE['unit'] / 1000:,.0f}k" + (f", {NB_BD})." if NB_BD else ")."), "Head of quality & regulatory", "L",
         f"{X.nb_status}; fees not yet quoted."),
        ("Module B examination fee", "nb_b_unit", NF_EUR, "EUR per type",
         f"Mid-point of the EUR 20k-60k commentary range; {words(NBB['count'])} types ({NBB_SHORT}).", "Head of quality & regulatory",
         "L", "First designated bodies' price lists; scarcity premium (High scenario x1.6)."),
        ("Module H approval fee", "nb_h_init", NF_EUR, "EUR",
         f"Within the EUR 80k-150k range for a first engagement, plus EUR {A['nb_module_h']['per_extra_category'] / 1000:,.0f}k per extra category.",
         "Head of quality & regulatory", "L", f"Scope of the {MODH_BU + ' ' if MODH_BU else ''}quality system (T26) and body capacity."),
        ("Training and awareness", "train_27", NF_EUR, "EUR (2027)",
         f"Role-based training, drills and e-learning for {CL['engineers']:,} engineers and named roles.", "Head of engineering enablement",
         "H", "LMS licence model; works council position on training time."),
        ("External legal and translations", "legal_27", NF_EUR, "EUR (2027)",
         f"Classification opinions, signing instrument, supplier clauses; DoC and Annex II translations at EUR {A['legal']['translations_per_family'] / 1000:,.0f}k per family.",
         "General Counsel", "M", "Number of Member State languages required per family."),
        ("Supplier programme", "supp_27", NF_EUR, "EUR (2027)",
         f"Clause pack and questionnaire for {CL['suppliers_in_scope']:,} in-scope suppliers.", "Head of procurement", "M",
         "Supplier refusals needing exit plans (R04)."),
        ("Contingency rate (Base)", None, None, "%",
         "15% on one-off costs reflects early-stage estimates and external dependencies; 10% Low, 20% High.",
         "CFO office", "M", "Notified-body designation and harmonised-standard citations."),
        ("Q4 2026 share of a year", "q4_share", NF_PCT0, "% of a year",
         f"Programme mobilised {X.kickoff}; Q4 2026 carries three months of run-rate costs.", "CFO office", "H", "None expected."),
        ("Monthly phasing of the one-off budget", None, None, "%",
         "Q4 2026 27/33/40%; 2027 rising to a 9.5% mid-year peak, then 8% in December (Monthly plan).",
         "Programme director", "M", "Notified-body slot dates; remediation velocity."),
    ]
    for i, (lab, key, fmt, unit, rat, owner, conf, change) in enumerate(alog):
        rr = 6 + i
        put(ws, f"B{rr}", f"L{i + 1:02d}", kind="muted", border=B_ROW)
        put(ws, f"C{rr}", lab, kind="label", border=B_ROW, wrap=True, bold=True)
        if key:
            put(ws, f"D{rr}", f"={IN[key]}", fmt=fmt, border=B_ROW)
        elif lab.startswith("Programme team size (build)"):
            put(ws, f"D{rr}", f"={LEV('pfte', 'G')}", fmt="0.0", border=B_ROW)
        elif lab.startswith("Shared-platform"):
            put(ws, f"D{rr}", f"='Cost build'!$F${DRV['build']}", fmt=NF_EUR, border=B_ROW)
        elif lab.startswith("Contingency"):
            put(ws, f"D{rr}", "=Inputs!$E$15", fmt=NF_PCT0, border=B_ROW)
        else:
            put(ws, f"D{rr}", "See Monthly plan", kind="muted", border=B_ROW, align="right")
        put(ws, f"E{rr}", unit, kind="muted", border=B_ROW, wrap=True, indent=1)
        put(ws, f"F{rr}", rat, kind="label", border=B_ROW, wrap=True)
        put(ws, f"G{rr}", owner, kind="label", border=B_ROW, wrap=True)
        put(ws, f"H{rr}", conf, kind="input", border=B_ROW, align="center", bold=True)
        put(ws, f"I{rr}", LOGDATE, kind="input", fmt=NF_DATE, border=B_ROW, align="left")
        put(ws, f"J{rr}", change, kind="muted", border=B_ROW, wrap=True, size=8)
        ws.row_dimensions[rr].height = 34
    AL_LAST = 6 + len(alog) - 1
    add_table(ws, "tblAssumptions", f"B5:J{AL_LAST}")
    add_list_dv(ws, f"H6:H{AL_LAST}", '"H,M,L"')
    cf_text(ws, f"H6:H{AL_LAST}", "H", C["green"])
    cf_text(ws, f"H6:H{AL_LAST}", "M", C["amber"])
    cf_text(ws, f"H6:H{AL_LAST}", "L", C["red"])
    source_line(ws, f"B{AL_LAST + 2}", "Confidence: H = rate or quote in hand; M = estimate from baseline evidence; "
                f"L = external dependency or vendor estimate. Source: pack_data.json {X.v} cost_model; programme data. Illustrative.")
    ws.freeze_panes = "C6"
    print_setup(ws, HDR, title_rows="5:5", area=f"A1:J{AL_LAST + 2}")

    # =====================================================================================
    # COST BUILD — integrity checks (need other sheets)
    # =====================================================================================
    ws = ws_cb
    integ = [
        ("I1", "Workstream table cross-foots to the cost lines (one-off excl. contingency)", "=Summary!G19", "=H29",
         '=IF(ABS(K{r})<0.5,"OK","CHECK")'),
        ("I2", "Monthly plan sums to the one-off total incl. contingency", "='Monthly plan'!E26", "=H31",
         '=IF(ABS(K{r})<0.5,"OK","CHECK")'),
        ("I3", "Scenarios sheet (active scenario) equals the Cost build one-off total",
         "=INDEX(Scenarios!$E$27:$G$27,MATCH(Inputs!$D$6,Scenarios!$E$26:$G$26,0))", "=H31",
         '=IF(ABS(K{r})<0.5,"OK","CHECK")'),
        ("I4", "Scenarios sheet (active scenario) equals the Cost build run-rate",
         "=INDEX(Scenarios!$E$31:$G$31,MATCH(Inputs!$D$6,Scenarios!$E$26:$G$26,0))", "=I31",
         '=IF(ABS(K{r})<0.5,"OK","CHECK")'),
        ("I5", "Monthly phasing weights sum to 100% in Q4 2026 and in 2027", "='Monthly plan'!L30", "='Monthly plan'!L31",
         '=IF(AND(ABS(I{r}-1)<0.000001,ABS(J{r}-1)<0.000001),"OK","CHECK")'),
        ("I6", "Portfolio revenue (families + other) reconciles to business-unit revenue",
         f"=Inputs!$K${PORT_TOTAL_ROW}", f"={IN['rev_total']}", '=IF(ABS(K{r})<0.001,"OK","CHECK")'),
    ]
    for i, (ref, lab, a, b, chk) in enumerate(integ):
        rr = 51 + i
        put(ws, f"B{rr}", ref, kind="muted", border=B_ROW)
        put(ws, f"C{rr}", lab, kind="label", border=B_ROW)
        fmt = NF_PCT1 if ref == "I5" else (NF_EUR1 if ref == "I6" else NF_EUR)
        put(ws, f"I{rr}", a, fmt=fmt, border=B_ROW)
        put(ws, f"J{rr}", b, fmt=fmt, border=B_ROW)
        if ref == "I5":
            put(ws, f"K{rr}", f"=ABS(I{rr}-1)+ABS(J{rr}-1)", fmt="0.000000", border=B_ROW)
        else:
            put(ws, f"K{rr}", f"=I{rr}-J{rr}", fmt=NF_EUR2, border=B_ROW)
        put(ws, f"L{rr}", chk.format(r=rr), border=B_ROW, align="center", bold=True)
        for c in "DEFGH":
            ws[f"{c}{rr}"].border = B_ROW
    put(ws, "L46", "=Scenarios!G42", align="center", bold=True)
    put(ws, "L58", '=IF(AND(L45="OK",L46="OK",COUNTIF(L51:L56,"OK")=6),"OK","CHECK")', align="center", bold=True)
    put(ws, "L2", "=L45", align="center", bold=True)
    put(ws, "L3", "=L58", align="center", bold=True)
    cf_checks(ws, "L37:L46")
    cf_checks(ws, "L51:L58")
    cf_checks(ws, "L2:L3")
    ws.freeze_panes = "A5"
    print_setup(ws, HDR, area="A1:L58")
    ws.row_breaks.append(Break(id=34))

    # =====================================================================================
    # COVER
    # =====================================================================================
    ws = ws_cover
    ws.sheet_view.showGridLines = False
    widths(ws, {"A": 3, "B": 3, "C": 30, "D": 82, "E": 18, "F": 3})
    for rr in range(1, 60):
        for c in "ABCDEF":
            ws[f"{c}{rr}"].fill = fill(C["white"])
    for rr in range(2, 9):
        for c in "BCDE":
            ws[f"{c}{rr}"].fill = fill(C["ink900"])
    put(ws, "C2", f"{X.CODENAME} · EU CYBER RESILIENCE ACT READINESS PROGRAMME", kind="label", bold=True, size=8,
        color=C["acc100"], fill_hex=C["ink900"])
    c = put(ws, "C3", "CRA Business Case and Cost Model", kind="label", fill_hex=C["ink900"])
    c.font = Font(name=DISPLAY, size=24, bold=True, color=C["white"])
    ws.row_dimensions[3].height = 36
    put(ws, "C4", f"Investment case, cost build, scenarios, exposure and monthly plan for the board decision of {X.board}",
        kind="label", size=10, color=C["ink300"], fill_hex=C["ink900"])
    put(ws, "C6", f"Version {X.ver} · {X.issue}", kind="label", size=9, bold=True, color=C["white"], fill_hex=C["ink900"])
    put(ws, "C7", f"{X.engagement} · Prepared by {X.advisor}", kind="label", size=9,
        color=C["white"], fill_hex=C["ink900"])
    ws["E2"].fill = fill(C["acc600"])
    ws["E3"].fill = fill(C["acc600"])
    put(ws, "E2", "MODEL CHECKS", kind="label", bold=True, size=8, color=C["white"], fill_hex=C["acc600"], align="center")
    put(ws, "E3", "='Cost build'!L58", bold=True, size=14, align="center", color=C["white"], fill_hex=C["acc600"])
    cf_checks(ws, "E3")

    meta = [("Version", X.ver), ("Date", X.issue), ("Engagement", f"{X.engagement}"),
            ("Prepared by", f"{X.advisor}"), ("Client data", CL["disclaimer"]),
            ("Regulatory facts", f"Verified to {X.facts} against the engagement knowledge base (Regulation (EU) 2024/2847)"),
            ("Currency and basis", "EUR, real 2026 terms, excl. VAT"),
            ("Source of numbers", f"pack_data.json {X.v} (cost_model, client, exposure); every derived number is a live formula")]
    r = 10
    band(ws, r, "About this workbook", "C", "E")
    r += 1
    for k, v in meta:
        put(ws, f"C{r}", k, kind="muted", bold=True, border=B_ROW)
        put(ws, f"D{r}", v, kind="label", border=B_ROW, wrap=True)
        ws[f"E{r}"].border = B_ROW
        r += 1
    r += 1
    band(ws, r, "Purpose", "C", "E")
    r += 1
    put(ws, f"C{r}", f"This model sizes the {X.codename} investment that keeps {X.client_pos} products on the EU market "
        "after 11 Dec 2027. It builds the one-off cost to Dec 2027 and the run-rate from 2028 from labelled drivers, tests "
        f"three scenarios, sets the cost against regulatory exposure (fines and {eur_m0(X.eu_nb_m)} of EU revenue that needs a notified "
        f"body) and phases the budget by month so Finance can track actuals. It supports board decision {INVEST_BD + ' ' if INVEST_BD else ''}on {X.board}.",
        kind="label", wrap=True, valign="top")
    ws.merge_cells(f"C{r}:E{r}")
    ws.row_dimensions[r].height = 54
    r += 2
    band(ws, r, "How to use", "C", "E")
    r += 1
    steps = ["Pick a scenario on Inputs (cell D6: Low, Base or High). Summary, Cost build and Monthly plan follow it; "
             "Scenarios always shows all three.",
             "Change assumptions only in blue cells on Inputs. Every cost line, total and chart recalculates.",
             f"Read the answer on Summary; trace any number back through Cost build to its Inputs row (refs A01 to {max(REFID.values())}, S1 to S6).",
             "Enter monthly actuals in Monthly plan column G; variance and tolerance status update.",
             f"Keep Model checks at OK. The {X.v} reconciliation checks read CHECK by design once inputs move away from {X.v}."]
    for i, s_ in enumerate(steps):
        put(ws, f"C{r}", f"{i + 1}.  {s_}", kind="label", wrap=True, valign="top")
        ws.merge_cells(f"C{r}:E{r}")
        ws.row_dimensions[r].height = 15
        r += 1
    r += 1
    band(ws, r, "Contents", "C", "E")
    r += 1
    contents = [
        ("Summary", "Headline outputs, workstream and scenario tables, exposure box and three charts"),
        ("Inputs", f"Scenario selector and levers; every cost assumption; revenue and the {X.nfam}-family portfolio"),
        ("Cost build", "Eleven cost lines as formulas on Inputs; subtotal, contingency, total; all model checks"),
        ("Scenarios", "Low, Base and High computed side by side, independent of the selector"),
        ("Exposure", "Fine tiers, EU revenue by class and needing a notified body, legacy decision, product liability"),
        ("Monthly plan", "Oct 2026 to Dec 2027 phasing weights, plan, cumulative, actuals and variance"),
        ("Benchmarks", "External cost reference points with source and type labels"),
        ("Assumptions log", "Rationale, owner, confidence and date for each assumption"),
    ]
    for name, desc in contents:
        link_cell(ws, f"C{r}", name, bold=True)
        ws[f"C{r}"].border = B_ROW
        put(ws, f"D{r}", desc, kind="label", border=B_ROW)
        ws[f"E{r}"].border = B_ROW
        r += 1
    r += 1
    band(ws, r, "Colour legend (standard modelling convention)", "C", "E")
    r += 1
    legend = [
        ("1,234", "input", "Input: hard-coded assumption or selector, blue font on a teal tint. Change these."),
        ("1,234", "formula", "Formula: calculation on the same or another sheet, black font. Do not overwrite."),
        ("1,234", "link", "Link: direct reference to a cell on another sheet, green font."),
        ("1,234", "output", "Key output: white on teal."),
        ("OK", "ok", "Check passes (green fill). CHECK on a red fill means a check fails."),
        ("Text", "text", "Labels and descriptive text, ink."),
    ]
    for sample, k, desc in legend:
        cell = ws[f"C{r}"]
        cell.value = sample
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = B_BOX
        if k == "input":
            cell.font = font(C["blue"])
            cell.fill = fill(C["acc100"])
        elif k == "formula":
            cell.font = font(C["black"])
        elif k == "link":
            cell.font = font(C["link"])
        elif k == "output":
            cell.font = font(C["white"], bold=True)
            cell.fill = fill(C["acc600"])
        elif k == "ok":
            cell.font = font(C["white"], bold=True)
            cell.fill = fill(C["green"])
        else:
            cell.font = font(C["ink900"])
        put(ws, f"D{r}", desc, kind="label")
        r += 1
    r += 1
    put(ws, f"C{r}", "Illustrative engagement — fictional client data. Not a quote, an audit opinion or legal advice. "
        f"Facts as at {X.facts}.", kind="muted", size=8, italic=True)
    ws.merge_cells(f"C{r}:E{r}")
    print_setup(ws, HDR, area=f"A1:F{r}", landscape=False)
    ws.page_setup.fitToHeight = 1

    # sheet tab colours
    for w_, col in [(ws_cover, C["ink900"]), (ws_sum, C["acc600"]), (ws_in, C["blue"]), (ws_cb, C["ink700"]),
                    (ws_sc, C["ink700"]), (ws_ex, C["ink700"]), (ws_mp, C["ink700"]), (ws_bm, C["ink500"]),
                    (ws_al, C["ink500"])]:
        w_.sheet_properties.tabColor = col

    wb.active = 0
    wb.properties.title = f"{X.codename} - CRA Business Case and Cost Model"
    wb.properties.subject = f"EU Cyber Resilience Act Readiness Programme · {X.engagement}"
    wb.properties.creator = f"{X.advisor}"
    wb.properties.lastModifiedBy = f"{X.advisor}"
    wb.properties.keywords = f"{X.codename}; CRA; business case; cost model; {X.v}"
    wb.save(str(OUT))
