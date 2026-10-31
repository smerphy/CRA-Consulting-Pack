"""D11 — CRA Obligations Register and Programme Tracker, built from pack_data.json (openpyxl).

Layout and formulas follow the v1.0 workbook; client values come from pack_data through Ctx (context.py) and
table sizes follow the data (families, risks, issues, KPIs, tasks, milestones, decisions, stakeholders).
Obligation rows that depend on a notified body are held at Not started while none is available
(Ctx.nb_available, default False). Call build(pack_data_path, out_dir) -> [Path].
"""
import datetime as dt
import json
import re
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import LineChart, Reference
from openpyxl.chart import Series
from openpyxl.chart.series import SeriesLabel, StrRef
from openpyxl.styles import Alignment, Border, Font, Side
from openpyxl.worksheet.formula import ArrayFormula
from openpyxl.worksheet.pagebreak import Break as _Break

from . import common as _common
from .common import *  # noqa: F401,F403
from .context import FULL_APPLICATION, REPORTING_APPLIES, Ctx, Words, eur_m0, fdate, join, pdate, plan_class, words
from .obligations import held_ids, obligation_rows

TITLE = "CRA Obligations Register and Programme Tracker"

# National implementation status by main-establishment Member State (regulatory facts, not client data).
NATIONAL_LAW = {
    "Germany": ("Passed the Bundestag plenary on 15 Oct 2026; promulgation pending (F16).", dt.date(2026, 12, 31)),
}


def output_name(D):
    return f"{D['meta']['programme_codename']} - {TITLE}.xlsx"


def build(pack_data_path, out_dir):
    """Write the D11 workbook (formulas only, no cached values) and return [path]."""
    pack_data_path = Path(pack_data_path)
    D = json.loads(pack_data_path.read_text(encoding="utf-8"))
    out = Path(out_dir) / output_name(D)
    out.parent.mkdir(parents=True, exist_ok=True)
    _build(D, Ctx(D, pack_data_path), out)
    return [out]


def est_lines(text, width, size=9):
    if not text:
        return 1
    cpl = max(8, int(width * (1.32 if size <= 8 else 1.18)))
    words_, lines, cur = str(text).split(), 1, 0
    for w in words_:
        if cur + len(w) + (1 if cur else 0) > cpl:
            lines += 1
            cur = len(w)
        else:
            cur += len(w) + (1 if cur else 0)
    return lines


def _monday(d):
    return d - dt.timedelta(days=d.weekday())


def _span(ids):
    ids = list(ids)
    return f"{ids[0]}-{ids[-1]}" if len(ids) > 1 else (ids[0] if ids else "")


def _build(D, X, OUT):

    _common.set_footer(X)
    DG = D["diagnostic"]
    PG = D["programme"]
    HDR = f"{X.codename} · CRA Obligations Register and Programme Tracker {X.v}"
    LABEL = f"{X.CODENAME} · OBLIGATIONS REGISTER AND PROGRAMME TRACKER"
    S26, D27 = REPORTING_APPLIES, FULL_APPLICATION
    STATUS_COL = {"Not started": (C["heat0"], C["white"]), "Initial": (C["heat1"], C["ink900"]),
                  "Defined": (C["heat2"], C["ink900"]), "Implemented": (C["heat3"], C["ink900"]),
                  "Assured": (C["heat4"], C["white"]), "Not assessed": (C["grey"], C["white"]),
                  "Reference": (C["ink100"], C["ink700"])}
    STATUS_DATE = X.issue_date
    ROWS = obligation_rows(X)
    HOLD = held_ids(X, ROWS)

    # ---- derived narrative and sizes ----
    PROV = X.prov_fams
    NPROV = len(PROV)
    NB_N = len(X.nb_fams)
    PROV_LABELS = join(X.labels(PROV, sort=True))
    LEGAL_TASK = X.task_id(lambda s: "legal opinion" in s)
    CLASS_ISSUE = X.issue_id(lambda s: "classif" in s)
    LEGAL_DUE = X.task_end(LEGAL_TASK) or X.issues.get(CLASS_ISSUE, {}).get("due", "")
    STRICT_SD = X.decision_id(lambda s: "legal opinion" in s, prefix="SD")
    NQ = sum(len(dm["questions"]) for dm in DG["domains"])
    TGT = DG.get("targets", {})
    T1, T2 = TGT.get("by_jun_2027", 0.70), TGT.get("by_nov_2027", 0.90)
    TASKS = PG["mobilisation_plan"]
    TASK_LAST = 10 + len(TASKS) - 1
    T_START = min(pdate(t["start"]) for t in TASKS)
    # the 90-day window: latest task end within 90 days of the first start (falls back to the latest end)
    T_END = max([pdate(t["end"]) for t in TASKS if pdate(t["end"]) <= T_START + dt.timedelta(days=90)]
                or [pdate(t["end"]) for t in TASKS])
    GANTT0 = _monday(STATUS_DATE)
    BOARD_TASK = X.task_id(lambda s: s.startswith("board decision"))
    MS_SPAN = _span(m["id"] for m in PG["milestones"])
    TASK_SPAN = _span(t["id"] for t in TASKS)
    RISKS = D["risks"]
    NR = len(RISKS)
    RL = 7 + NR - 1
    TOP_I = max(range(NR), key=lambda i: RISKS[i]["score"])
    TOP = RISKS[TOP_I]
    TOP_PHRASE = X.t(f"d11.risk_short.{TOP['id']}", TOP["title"])
    KPIS = D["kpis"]
    NK = len(KPIS)
    KL = 6 + NK - 1
    SK_LAST = 6 + len(D["stakeholders"]) - 1
    BOARD_IDS = [d_["id"] for d_ in D["decisions"].get("board", [])]
    SC_IDS = [d_["id"] for d_ in D["decisions"].get("steerco_1", [])]
    ND = len(BOARD_IDS) + len(SC_IDS)
    wb = Workbook()
    ws_cover = wb.active
    ws_cover.title = "Cover"
    ws_reg = wb.create_sheet("Obligations register")
    ws_mx = wb.create_sheet("Product x obligation matrix")
    ws_plan = wb.create_sheet("90-day plan")
    ws_raid = wb.create_sheet("RAID log")
    ws_dec = wb.create_sheet("Decision log")
    ws_kpi = wb.create_sheet("KPI tracker")
    ws_raci = wb.create_sheet("RACI")
    ws_stk = wb.create_sheet("Stakeholder register")
    ws_db = wb.create_sheet("Diagnostic baseline")
    ws_ls = wb.create_sheet("Lists")

    # =====================================================================================
    # LISTS (validation lists and parameters)
    # =====================================================================================
    ws = ws_ls
    title_block(ws, LABEL + " · LISTS", "Validation lists and parameters used across the workbook",
                "Edit a list here to change every dropdown that uses it; parameters drive status bands and ratings",
                link_col="Q")
    lists = {
        "B": ("Applies to", ["Manufacturer", "Importer", "Distributor", "Importer / Distributor", "AR", "Steward", "All operators"]),
        "C": ("Level", ["Product", "Organisation", "Both"]),
        "D": ("Owner role (RACI)", ["Executive sponsor", "Compliance lead", "Product security officer", "PSIRT lead",
                                    "Engineering lead", "Legal", "Procurement", "Product management"]),
        "E": ("Diagnostic question", [q["id"] for dom in DG["domains"] for q in dom["questions"]] + ["Ref"]),
        "F": ("Register status", ["Not started", "Initial", "Defined", "Implemented", "Assured", "Not assessed", "Reference"]),
        "G": ("Task status", ["Not started", "In progress", "Complete", "At risk", "Blocked"]),
        "H": ("Milestone status", ["Complete", "Planned", "On track", "At risk", "Fixed", "Missed"]),
        "I": ("RAG", ["Green", "Amber", "Red", "Grey"]),
        "J": ("Trend", ["Rising", "Stable", "Falling", "New"]),
        "K": ("RAID item status", ["Open", "In progress", "Monitoring", "Planned", "Not started", "At risk", "Valid",
                                   "Invalidated", "Closed"]),
        "L": ("Decision status", ["Endorsed (illustrative)", "Proposed", "Approved", "Rejected", "Deferred"]),
        "M": ("RACI code", ["R", "A", "C", "I"]),
        "N": ("Status hold", ["No notified body"]),
    }
    LIST_REF = {}
    widths(ws, {"A": 2.5, **{c: 20 for c in "BCDEFGHIJKLMN"}, "O": 44, "P": 12, "Q": 12})
    for col, (name, items) in lists.items():
        header(ws, 5, [name], col, height=30)
        for i, it in enumerate(items):
            put(ws, f"{col}{6 + i}", it, kind="label", border=B_ROW)
        LIST_REF[name] = f"Lists!${col}$6:${col}${5 + len(items)}"
    header(ws, 5, ["Parameter", "Value"], "O", height=30)
    params = [
        ("b1", "Register status: Initial from diagnostic level (average rounded down; below = Not started)", 1, "0"),
        ("b2", "Register status: Defined from level", 2, "0"),
        ("b3", "Register status: Implemented from level", 3, "0"),
        ("b4", "Register status: Assured from level", 4, "0"),
        ("rh", "Risk rating: High if score (L x I) is at least", 12, "0"),
        ("rm", "Risk rating: Medium if score is at least (otherwise Low)", 5, "0"),
        ("pw", "Stakeholder: high power if at least", 4, "0"),
        ("it", "Stakeholder: high interest if at least", 4, "0"),
        ("cap", "Diagnostic target level (readiness caps scores here)", DG.get("target_level", 3), "0"),
        ("t1", "Readiness target, Jun 2027", T1, NF_PCT0),
        ("t2", "Readiness target, Nov 2027", T2, NF_PCT0),
    ]
    P = {}
    for i, (k, lab, v, fmt) in enumerate(params):
        rr = 6 + i
        put(ws, f"O{rr}", lab, kind="label", border=B_ROW, wrap=True)
        put(ws, f"P{rr}", v, kind="input", fmt=fmt, border=B_ROW)
        P[k] = f"Lists!$P${rr}"
        ws.row_dimensions[rr].height = 24
    source_line(ws, "O18", "Register status = diagnostic level rounded down (<1 Not started; 1 Initial; 2 Defined; 3 Implemented; "
                f"4 Assured). Rows with a Status hold read Not started. Risk bands reproduce the {X.v} ratings.")
    ws.freeze_panes = "A6"
    print_setup(ws, HDR, area="A1:P47")

    # =====================================================================================
    # DIAGNOSTIC BASELINE (question level)
    # =====================================================================================
    ws = ws_db
    FAMS = list(DG["baseline_scores"].keys())
    FAMCOL = {f: get_column_letter(7 + i) for i, f in enumerate(FAMS)}  # G..S for 13 families
    FL = FAMCOL[FAMS[-1]]
    TC, UC, VC = (get_column_letter(7 + len(FAMS) + k) for k in range(3))
    widths(ws, {"A": 2.5, "B": 7, "C": 6, "D": 18, "E": 62, "F": 26, **{FAMCOL[f]: 7.5 for f in FAMS}, TC: 10, UC: 10,
                VC: 13})
    title_block(ws, LABEL + " · DIAGNOSTIC BASELINE",
                f"Question-level baseline: {NQ} questions x {len(FAMS)} families drive the matrix and the register status",
                DG["baseline_label"] + " · Scale 0 Not started, 1 Initial, 2 Defined, 3 Implemented, 4 Assured", link_col=VC)
    header(ws, 5, ["Q", "Domain", "Domain name", "Question", "Basis"] + FAMS + ["Portfolio avg (0-4)",
                   "Readiness (capped)", "Status band"], "B", height=32)
    for c in list(FAMCOL.values()) + [TC, UC]:
        ws[f"{c}5"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    r = 6
    DBROW = {}
    for dom in DG["domains"]:
        for q in dom["questions"]:
            put(ws, f"B{r}", q["id"], kind="label", bold=True, border=B_ROW)
            put(ws, f"C{r}", dom["id"], kind="muted", border=B_ROW)
            put(ws, f"D{r}", dom["short"], kind="label", border=B_ROW, size=8)
            put(ws, f"E{r}", q["text"], kind="label", border=B_ROW, wrap=True, size=8)
            put(ws, f"F{r}", q["basis"], kind="muted", border=B_ROW, wrap=True, size=8)
            for f in FAMS:
                put(ws, f"{FAMCOL[f]}{r}", DG["baseline_scores"][f][q["id"]], kind="input", fmt="0", border=B_ROW,
                    align="center")
            put(ws, f"{TC}{r}", f"=AVERAGE(G{r}:{FL}{r})", fmt="0.00", border=B_ROW, bold=True, align="center")
            put(ws, f"{UC}{r}", f"=SUMPRODUCT((G{r}:{FL}{r}>{P['cap']})*{P['cap']}+(G{r}:{FL}{r}<={P['cap']})*G{r}:{FL}{r})/({P['cap']}*COUNT(G{r}:{FL}{r}))",
                fmt=NF_PCT0, border=B_ROW, align="center")
            put(ws, f"{VC}{r}", f'=IF({TC}{r}<{P["b1"]},"Not started",IF({TC}{r}<{P["b2"]},"Initial",IF({TC}{r}<{P["b3"]},"Defined",IF({TC}{r}<{P["b4"]},"Implemented","Assured"))))',
                border=B_ROW)
            ws.row_dimensions[r].height = max(24, 11.5 * max(est_lines(q["text"], 62, 8), est_lines(q["basis"], 26, 8)) + 3)
            DBROW[q["id"]] = r
            r += 1
    DB_LAST = r - 1  # 45
    add_table(ws, "tblDiagnostic", f"B5:{VC}{DB_LAST}")
    put(ws, f"E{r}", "Family readiness index (mean of min(score, 3) / 3)", kind="label", bold=True, border=B_TOTAL,
        align="right")
    for f in FAMS:
        c = FAMCOL[f]
        put(ws, f"{c}{r}", f"=SUMPRODUCT(({c}6:{c}{DB_LAST}>{P['cap']})*{P['cap']}+({c}6:{c}{DB_LAST}<={P['cap']})*{c}6:{c}{DB_LAST})/({P['cap']}*COUNT({c}6:{c}{DB_LAST}))",
            fmt=NF_PCT0, bold=True, border=B_TOTAL, align="center")
    put(ws, f"{TC}{r}", f"=AVERAGE(G{r}:{FL}{r})", fmt=NF_PCT1, kind="output", align="center")
    for c in ["B", "C", "D", "F", UC, VC]:
        ws[f"{c}{r}"].border = B_TOTAL
    DB_IDX_ROW = r  # 46
    # heatmap on scores
    HEAT = [(0, 1, C["heat0"], C["white"]), (1, 2, C["heat1"], C["ink900"]), (2, 3, C["heat2"], C["ink900"]),
            (3, 4, C["heat3"], C["ink900"]), (4, 99, C["heat4"], C["white"])]


    def heatmap(ws, rng, tl):
        for lo, hi, bg, fg in HEAT:
            cf_formula(ws, rng, f"AND(ISNUMBER({tl}),{tl}>={lo},{tl}<{hi})", bg=bg, fg=fg)


    heatmap(ws, f"G6:{FL}{DB_LAST}", "G6")
    heatmap(ws, f"{TC}6:{TC}{DB_LAST}", f"{TC}6")
    for st_ in ["Not started", "Initial", "Defined", "Implemented", "Assured"]:
        cf_text(ws, f"{VC}6:{VC}{DB_LAST}", st_, STATUS_COL[st_][0], fg=STATUS_COL[st_][1])
    add_whole_dv(ws, f"G6:{FL}{DB_LAST}", 0, 4)
    source_line(ws, f"B{r + 2}", f"Source: pack_data.json {X.v} (diagnostic.baseline_scores, domains). Scores are illustrative. "
                "The CRA Readiness Diagnostic (D08) is the live collection tool.")
    ws.freeze_panes = "G6"
    print_setup(ws, HDR, title_rows="5:5", area=f"A1:{VC}{r + 2}")

    # =====================================================================================
    # PRODUCT x OBLIGATION MATRIX
    # =====================================================================================
    ws = ws_mx
    DOMS = DG["domains"]
    if len(DOMS) != 10:
        raise ValueError("The matrix layout expects the 10 domains of the shared CRA readiness diagnostic")
    DCOL = {d["id"]: get_column_letter(7 + i) for i, d in enumerate(DOMS)}  # G..P
    widths(ws, {"A": 2.5, "B": 9, "C": 28, "D": 7, "E": 11, "F": 13, **{DCOL[d["id"]]: 13.5 for d in DOMS}, "Q": 11,
                "R": 19, "S": 11})
    MX_LAST = 6 + len(FAMS) - 1
    AV, DR, CT, CK = MX_LAST + 1, MX_LAST + 2, MX_LAST + 3, MX_LAST + 4
    title_block(ws, LABEL + " · PRODUCT X OBLIGATION MATRIX",
                f'="Portfolio readiness is "&TEXT(Q{AV},"0%")&": "&INDEX($G$5:$P$5,MATCH(MAX(G{DR}:P{DR}),G{DR}:P{DR},0))&" is strongest ("'
                f'&TEXT(MAX(G{DR}:P{DR}),"0%")&") and "&INDEX($G$5:$P$5,MATCH(MIN(G{DR}:P{DR}),G{DR}:P{DR},0))&" weakest ("&TEXT(MIN(G{DR}:P{DR}),"0%")&")"',
                f"Average diagnostic level (0-4, target {DG.get('target_level', 3)}) per family and domain · Illustrative baseline, {X.baseline} · "
                "Numbers print in every cell; colour repeats them", link_col="S")
    for d in DOMS:
        put(ws, f"{DCOL[d['id']]}4", d["id"], kind="muted", size=8, align="center", bold=True)
    header(ws, 5, ["ID", "Family", "BU", "Class (planning)", "Wave"] + [d["short"] for d in DOMS] +
           ["Readiness index", "Weakest domain", f"Gap to {T1:.0%} target (Jun 2027)"], "B", height=42)
    for c in list(DCOL.values()) + ["Q", "S"]:
        ws[f"{c}5"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    fams = {f["id"]: f for f in D["client"]["product_families"]}
    for i, fid in enumerate(FAMS):
        rr = 6 + i
        f = fams[fid]
        put(ws, f"B{rr}", fid, kind="label", bold=True, border=B_ROW)
        put(ws, f"C{rr}", f["name"], kind="label", border=B_ROW)
        put(ws, f"D{rr}", f["bu"], kind="label", border=B_ROW)
        put(ws, f"E{rr}", "Default" if f["cra_class"].startswith("Default") else f["cra_class"], kind="label", border=B_ROW)
        put(ws, f"F{rr}", f["wave"], kind="label", border=B_ROW)
        for d in DOMS:
            c = DCOL[d["id"]]
            put(ws, f"{c}{rr}",
                f"=AVERAGEIFS(INDEX('Diagnostic baseline'!$G$6:${FL}${DB_LAST},0,MATCH($B{rr},'Diagnostic baseline'!$G$5:${FL}$5,0)),"
                f"'Diagnostic baseline'!$C$6:$C${DB_LAST},{c}$4)", fmt="0.00", border=B_ROW, align="center")
        put(ws, f"Q{rr}", f"=INDEX('Diagnostic baseline'!$G${DB_IDX_ROW}:${FL}${DB_IDX_ROW},MATCH($B{rr},'Diagnostic baseline'!$G$5:${FL}$5,0))",
            fmt=NF_PCT0, border=B_ROW, bold=True, align="center")
        put(ws, f"R{rr}", f"=INDEX($G$5:$P$5,MATCH(MIN(G{rr}:P{rr}),G{rr}:P{rr},0))", border=B_ROW, size=8)
        put(ws, f"S{rr}", f"=Q{rr}-{P['t1']}", fmt='+0%;-0%;0%', border=B_ROW, align="center")
    ws.auto_filter.ref = f"B5:S{MX_LAST}"
    put(ws, f"C{AV}", "Portfolio average", kind="label", bold=True, border=B_TOTAL)
    for d in DOMS:
        c = DCOL[d["id"]]
        put(ws, f"{c}{AV}", f"=AVERAGE({c}6:{c}{MX_LAST})", fmt="0.00", bold=True, border=B_TOTAL, align="center")
    put(ws, f"Q{AV}", f"=AVERAGE(Q6:Q{MX_LAST})", kind="output", fmt=NF_PCT1, align="center")
    put(ws, f"S{AV}", f"=Q{AV}-{P['t1']}", fmt='+0%;-0%;0%', bold=True, border=B_TOTAL, align="center")
    for c in "BDEFR":
        ws[f"{c}{AV}"].border = B_TOTAL
    put(ws, f"C{DR}", "Domain readiness index", kind="label", bold=True, border=B_ROW)
    for d in DOMS:
        c = DCOL[d["id"]]
        put(ws, f"{c}{DR}",
            f"=SUMPRODUCT(('Diagnostic baseline'!$C$6:$C${DB_LAST}={c}$4)*(('Diagnostic baseline'!$G$6:${FL}${DB_LAST}>{P['cap']})*{P['cap']}"
            f"+('Diagnostic baseline'!$G$6:${FL}${DB_LAST}<={P['cap']})*'Diagnostic baseline'!$G$6:${FL}${DB_LAST}))/({P['cap']}*COUNTIF('Diagnostic baseline'!$C$6:$C${DB_LAST},{c}$4)*COUNTA('Diagnostic baseline'!$G$5:${FL}$5))",
            fmt=NF_PCT0, bold=True, border=B_ROW, align="center")
    put(ws, f"C{CT}", f"Control: pack_data.json {X.v}", kind="muted", border=B_ROW)
    for d in DOMS:
        put(ws, f"{DCOL[d['id']]}{CT}", DG["domain_readiness_index"][d["id"]], kind="input", fmt=NF_PCT1, border=B_ROW,
            align="center")
    put(ws, f"Q{CT}", DG["portfolio_readiness_index"], kind="input", fmt=NF_PCT1, border=B_ROW, align="center")
    put(ws, f"C{CK}", f"Check (within 0.1 pts of rounded {X.v} values)", kind="muted", border=B_ROW)
    for d in DOMS:
        c = DCOL[d["id"]]
        put(ws, f"{c}{CK}", f'=IF(ABS({c}{DR}-{c}{CT})<0.001,"OK","CHECK")', border=B_ROW, align="center", bold=True)
    put(ws, f"Q{CK}", f'=IF(ABS(Q{AV}-Q{CT})<0.001,"OK","CHECK")', border=B_ROW, align="center", bold=True)
    put(ws, f"R{CK}", f'=IF(COUNTIF(G{CK}:Q{CK},"OK")=11,"All OK","CHECK")', border=B_ROW, align="center", bold=True)
    cf_checks(ws, f"G{CK}:Q{CK}")
    cf_text(ws, f"R{CK}", "All OK", C["green"])
    cf_text(ws, f"R{CK}", "CHECK", C["red"])
    heatmap(ws, f"G6:P{AV}", "G6")
    # legend
    LG = CK + 2
    put(ws, f"C{LG}", "Heatmap legend (average level)", kind="label", bold=True)
    leg = [("0", "Not started", C["heat0"], C["white"]), ("1", "Initial", C["heat1"], C["ink900"]),
           ("2", "Defined", C["heat2"], C["ink900"]), ("3", "Implemented", C["heat3"], C["ink900"]),
           ("4", "Assured", C["heat4"], C["white"])]
    for i, (num, nm, bg, fg) in enumerate(leg):
        c = get_column_letter(7 + 2 * i)
        c2 = get_column_letter(8 + 2 * i)
        cell = ws[f"{c}{LG}"]
        cell.value = num
        cell.font = font(fg, bold=True)
        cell.fill = fill(bg)
        cell.alignment = Alignment(horizontal="center")
        put(ws, f"{c2}{LG}", nm, kind="label", size=8)
    put(ws, f"C{LG + 1}", "Colour = level rounded down, as in the diagnostic: below 1 = 0; 1 to below 2 = 1; 2 to below 3 = 2; "
        "3 to below 4 = 3; 4 = 4.", kind="muted", size=8)
    # by BU / class
    CB = LG + 3
    band(ws, CB, "Readiness index by business unit and by class", "B", "S")
    header(ws, CB + 1, ["Cut", "Group", "", "", "", "Families", "Readiness index", f"Control ({X.v})", "Check"], "B", height=20)


    def _ri_mean(ids):
        vals = [DG["family_readiness_index"][i] for i in ids if i in DG["family_readiness_index"]]
        return round(sum(vals) / len(vals), 3) if vals else 0


    cuts = [("BU", b, "D", DG["bu_readiness_index"].get(b, _ri_mean([f["id"] for f in X.fams if f["bu"] == b])))
            for b in X.bu_ids]
    cuts += [("Class", k, "E", DG["class_readiness_index"].get(k, _ri_mean([f["id"] for f in X.fams_by_class(k)])))
             for k in ("Default", "Class I", "Class II")]
    for i, (cut, grp, col, ctl) in enumerate(cuts):
        rr = CB + 2 + i
        put(ws, f"B{rr}", cut, kind="muted", border=B_ROW)
        put(ws, f"C{rr}", grp, kind="label", bold=True, border=B_ROW)
        put(ws, f"G{rr}", f'=COUNTIF(${col}$6:${col}${MX_LAST},C{rr})', fmt="0", border=B_ROW, align="center")
        fml = f'=AVERAGEIF(${col}$6:${col}${MX_LAST},C{rr},$Q$6:$Q${MX_LAST})'
        if not any((fams[fid]["bu"] if cut == "BU" else plan_class(fams[fid])) == grp for fid in FAMS):
            fml = f"=IFERROR({fml[1:]},0)"
        put(ws, f"H{rr}", fml, fmt=NF_PCT1, border=B_ROW,
            align="center", bold=True)
        put(ws, f"I{rr}", ctl, kind="input", fmt=NF_PCT1, border=B_ROW, align="center")
        put(ws, f"J{rr}", f'=IF(ABS(H{rr}-I{rr})<0.001,"OK","CHECK")', border=B_ROW, align="center", bold=True)
        for c in "DEF":
            ws[f"{c}{rr}"].border = B_ROW
    CUT_LAST = CB + 2 + len(cuts) - 1
    cf_checks(ws, f"J{CB + 2}:J{CUT_LAST}")
    source_line(ws, f"B{CUT_LAST + 2}", f"Source: Diagnostic baseline sheet (pack_data.json {X.v}, diagnostic). Readiness index = mean over "
                "questions of min(score, 3) / 3; level 4 does not offset gaps elsewhere. Classes on planning basis"
                + (f" ({PROV_LABELS} as Default)" if PROV else "") + ". Illustrative.")
    ws.freeze_panes = "D6"
    print_setup(ws, HDR, area=f"A1:S{CUT_LAST + 2}")
    MX_CHECK = f"'Product x obligation matrix'!$R${CK}"
    MX_AVG = f"'Product x obligation matrix'!$Q${AV}"

    # =====================================================================================
    # 90-DAY PLAN
    # =====================================================================================
    ws = ws_plan
    WKCOLS = [get_column_letter(12 + i) for i in range(14)]  # L..Y
    widths(ws, {"A": 2.5, "B": 7, "C": 26, "D": 46, "E": 22, "F": 11, "G": 11, "H": 6, "I": 12, "J": 12, "K": 1.5,
                **{c: 5.6 for c in WKCOLS}})
    title_block(ws, LABEL + " · 90-DAY PLAN",
                f'="Of "&COUNTA(B10:B{TASK_LAST})&" mobilisation tasks, "&COUNTIF(I10:I{TASK_LAST},"In progress")&" are in progress and "'
                + (f'&COUNTIF(I10:I{TASK_LAST},"Not started")&" not started; "&COUNTIF(J10:J{TASK_LAST},"*{BOARD_TASK}*")&" wait on the {X.board} board"'
                   if BOARD_TASK else f'&COUNTIF(I10:I{TASK_LAST},"Not started")&" not started"'),
                f"Mobilisation plan {TASK_SPAN}, {fdate(T_START)} to {fdate(T_END)}, with milestones {MS_SPAN} · Gantt bars are formulas on "
                "start and end dates; the orange column marks the status date · Illustrative", link_col="Y")
    put(ws, "B5", "Status date (today marker)", kind="label", bold=True)
    put(ws, "E5", STATUS_DATE, kind="input", fmt=NF_DATE, align="left", bold=True)
    put(ws, "B6", "Gantt start (week commencing)", kind="label", bold=True)
    put(ws, "E6", GANTT0, kind="input", fmt=NF_DATE, align="left")
    put(ws, "F6", f"Week of the status date; plan tasks start w/c {fdate(_monday(T_START))}", kind="muted", size=8)
    STATUS = "'90-day plan'!$E$5"
    # week headers
    for i, c in enumerate(WKCOLS):
        if i == 0:
            put(ws, f"{c}9", "=$E$6", fmt="d mmm", align="center", size=7, bold=True, color=C["white"], fill_hex=C["ink900"])
            put(ws, f"{c}8", f'=TEXT({c}9,"mmm yy")', kind="muted", size=7, bold=True)
        else:
            prev = WKCOLS[i - 1]
            put(ws, f"{c}9", f"={prev}9+7", fmt="d mmm", align="center", size=7, bold=True, color=C["white"],
                fill_hex=C["ink900"])
            put(ws, f"{c}8", f'=IF(MONTH({c}9)<>MONTH({prev}9),TEXT({c}9,"mmm yy"),"")', kind="muted", size=7, bold=True)
        put(ws, f"{c}7", f'=IF(AND($E$5>={c}9,$E$5<{c}9+7),"Today","")', size=7, bold=True, align="center",
            color=C["signal"])
        ws[f"{c}9"].alignment = Alignment(horizontal="center", vertical="center", text_rotation=90)
    ws.row_dimensions[9].height = 36
    header(ws, 9, ["ID", "Workstream", "Task", "Owner", "Start", "End", "Days", "Status", "Depends on"], "B", height=36)
    for c in "FG":
        ws[f"{c}9"].alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    for c in "HI":
        ws[f"{c}9"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    WSNAME = {w["id"]: w["name"] for w in PG["workstreams"]}
    for i, t in enumerate(PG["mobilisation_plan"]):
        rr = 10 + i
        put(ws, f"B{rr}", t["id"], kind="label", bold=True, border=B_ROW)
        put(ws, f"C{rr}", f"{t['workstream']} {WSNAME[t['workstream']]}", kind="label", border=B_ROW, size=8)
        put(ws, f"D{rr}", t["task"], kind="label", border=B_ROW, wrap=True)
        put(ws, f"E{rr}", t["owner"], kind="label", border=B_ROW, size=8, wrap=True)
        put(ws, f"F{rr}", pdate(t["start"]), kind="input", fmt=NF_DATE, border=B_ROW)
        put(ws, f"G{rr}", pdate(t["end"]), kind="input", fmt=NF_DATE, border=B_ROW)
        put(ws, f"H{rr}", f"=G{rr}-F{rr}+1", fmt="0", border=B_ROW, align="center")
        put(ws, f"I{rr}", t["status"], kind="input", border=B_ROW, align="center")
        put(ws, f"J{rr}", t["depends_on"].replace(",", ", "), kind="label", border=B_ROW, size=8)
        for c in WKCOLS:
            cell = put(ws, f"{c}{rr}", f"=IF(AND($F{rr}<={c}$9+6,$G{rr}>={c}$9),1,0)", fmt=";;;", border=B_ROW)
        ws.row_dimensions[rr].height = 24 if est_lines(t["task"], 46) > 1 else 16
    add_table(ws, "tblTasks", f"B9:J{TASK_LAST}")
    add_list_dv(ws, f"I10:I{TASK_LAST}", LIST_REF["Task status"])
    GR = f"L10:Y{TASK_LAST}"
    for st_, colr in [("Complete", C["green"]), ("In progress", C["acc600"]), ("At risk", C["amber"]),
                      ("Blocked", C["red"]), ("Not started", C["ink300"])]:
        cf_formula(ws, GR, f'AND(L10=1,$I10="{st_}")', bg=colr)
    today_border = Border(left=Side(style="thin", color=C["signal"]), right=Side(style="thin", color=C["signal"]))
    cf_formula(ws, f"L7:Y{TASK_LAST}", "AND(L$9<=$E$5,$E$5<L$9+7)", border=today_border)
    cf_formula(ws, "L9:Y9", "AND(L$9<=$E$5,$E$5<L$9+7)", bg=C["signal"])
    cf_text(ws, f"I10:I{TASK_LAST}", "Complete", C["green"])
    cf_text(ws, f"I10:I{TASK_LAST}", "In progress", C["acc600"])
    cf_text(ws, f"I10:I{TASK_LAST}", "At risk", C["amber"])
    cf_text(ws, f"I10:I{TASK_LAST}", "Blocked", C["red"])
    # legend
    put(ws, f"D{TASK_LAST + 1}", "Bars: teal = in progress, grey = not started, green = complete, amber = at risk, red = "
        "blocked. Orange outline = week of the status date.", kind="muted", size=8)
    # milestones
    MS0 = TASK_LAST + 3  # band row
    band(ws, MS0, f"Milestones {MS_SPAN} (diamonds fall in the week of the milestone date)", "B", "Y")
    header(ws, MS0 + 1, ["ID", "Date", "Milestone", "Status", "Days from status date"], "B", height=30)
    for c in "CF":
        ws[f"{c}{MS0 + 1}"].alignment = Alignment(horizontal="right", vertical="center", wrap_text=True)
    for c in WKCOLS:
        put(ws, f"{c}{MS0 + 1}", f"={c}$9", fmt="d mmm", align="center", size=7, bold=True, color=C["white"],
            fill_hex=C["ink900"])
        ws[f"{c}{MS0 + 1}"].alignment = Alignment(horizontal="center", vertical="center", text_rotation=90)
    ws.row_dimensions[MS0 + 1].height = 36
    for i, m in enumerate(PG["milestones"]):
        rr = MS0 + 2 + i
        put(ws, f"B{rr}", m["id"], kind="label", bold=True, border=B_ROW)
        put(ws, f"C{rr}", pdate(m["date"]), kind="input", fmt=NF_DATE, border=B_ROW)
        put(ws, f"D{rr}", m["name"], kind="label", border=B_ROW, wrap=True)
        put(ws, f"E{rr}", m["status"], kind="input", border=B_ROW)
        put(ws, f"F{rr}", f"=C{rr}-$E$5", fmt='0;-0;0', border=B_ROW)
        for c in "GHIJ":
            ws[f"{c}{rr}"].border = B_ROW
        for c in WKCOLS:
            put(ws, f"{c}{rr}", f'=IF(AND($C{rr}>={c}$9,$C{rr}<{c}$9+7),"◆","")', align="center", border=B_ROW,
                bold=True, size=10)
        ws.row_dimensions[rr].height = 24 if est_lines(m["name"], 46) > 1 else 16
    MS_LAST = MS0 + 2 + len(PG["milestones"]) - 1
    add_table(ws, "tblMilestones", f"B{MS0 + 1}:F{MS_LAST}")
    add_list_dv(ws, f"E{MS0 + 2}:E{MS_LAST}", LIST_REF["Milestone status"])
    cf_text(ws, f"E{MS0 + 2}:E{MS_LAST}", "Complete", C["green"])
    cf_text(ws, f"E{MS0 + 2}:E{MS_LAST}", "At risk", C["amber"])
    cf_text(ws, f"E{MS0 + 2}:E{MS_LAST}", "Missed", C["red"])
    cf_text(ws, f"E{MS0 + 2}:E{MS_LAST}", "Fixed", C["ink900"])
    cf_formula(ws, f"L{MS0 + 2}:Y{MS_LAST}", f'AND(L{MS0 + 2}="◆",$E{MS0 + 2}="At risk")', fg=C["amber"])
    cf_formula(ws, f"L{MS0 + 2}:Y{MS_LAST}", f'AND(L{MS0 + 2}="◆",$E{MS0 + 2}<>"At risk")', fg=C["acc600"])
    cf_formula(ws, f"L{MS0 + 1}:Y{MS_LAST}", "AND(L$9<=$E$5,$E$5<L$9+7)", border=today_border)
    source_line(ws, f"B{MS_LAST + 2}", f"Source: pack_data.json {X.v} (programme.mobilisation_plan, milestones). Week columns start "
                f"w/c {fdate(GANTT0)} so the status-date marker ({X.issue}) is visible; plan tasks run {fdate(T_START)} to {fdate(T_END)}. Illustrative.")
    ws.freeze_panes = "E10"
    print_setup(ws, HDR, title_rows="9:9", area=f"A1:Y{MS_LAST + 2}")

    # =====================================================================================
    # OBLIGATIONS REGISTER
    # =====================================================================================
    ws = ws_reg
    RW = {"B": 9, "C": 19, "D": 58, "E": 13, "F": 12, "G": 13, "H": 32, "I": 17, "J": 10, "K": 11, "L": 12, "M": 14,
          "N": 44, "O": 24}
    widths(ws, {"A": 2.5, **RW})
    FIRST = 10
    LAST = FIRST + len(ROWS) - 1
    # Rows that depend on a notified body are held at Not started while none is available (HOLD, above)
    HOLD_TEXT = "No notified body"
    title_block(ws, LABEL + " · OBLIGATIONS REGISTER",
                f'="{len(ROWS)} obligations mapped: "&COUNTIF(F{FIRST}:F{LAST},"<="&{STATUS})&" already apply, and "'
                f'&COUNTIF(M{FIRST}:M{LAST},"Not started")&" are not started at {X.client} (illustrative)"',
                "One row per obligation of Regulation (EU) 2024/2847 · Status = diagnostic level of the mapped question "
                "(portfolio average rounded down)" + ("; Module B and H rows held at Not started" if HOLD else "") + f" · Facts as at {X.facts} · "
                "Paraphrases, not legal text", link_col="O")
    band(ws, 5, "Register at a glance (Illustrative)", "B", "O")
    glance = [("B", "Rows", f"=COUNTA(B{FIRST}:B{LAST})", None),
              ("C", "Apply now (11 Sep 2026)", f'=COUNTIF(F{FIRST}:F{LAST},"<="&{STATUS})', None),
              ("D", "From 11 Dec 2027", f'=COUNTIF(F{FIRST}:F{LAST},">"&{STATUS})', None),
              ("E", "Not started", f'=COUNTIF(M{FIRST}:M{LAST},E6)', "Not started"),
              ("F", "Initial", f'=COUNTIF(M{FIRST}:M{LAST},F6)', "Initial"),
              ("G", "Defined", f'=COUNTIF(M{FIRST}:M{LAST},G6)', "Defined"),
              ("H", "Implemented", f'=COUNTIF(M{FIRST}:M{LAST},H6)', "Implemented"),
              ("I", "Assured", f'=COUNTIF(M{FIRST}:M{LAST},I6)', "Assured"),
              ("J", "Not assessed", f'=COUNTIF(M{FIRST}:M{LAST},J6)', "Not assessed"),
              ("K", "Reference", f'=COUNTIF(M{FIRST}:M{LAST},K6)', "Reference"),
              ("L", "Held: no notified body", f'=COUNTIF(L{FIRST}:L{LAST},"{HOLD_TEXT}")', None)]
    for c, lab, f, st_ in glance:
        put(ws, f"{c}6", lab, kind="label", bold=True, size=8, wrap=True, align="center", color=C["ink500"],
            fill_hex=C["ink100"])
        bg, fg = STATUS_COL[st_] if st_ else (C["ink100"], C["ink900"])
        put(ws, f"{c}7", f, fmt="0", bold=True, size=13, align="center", color=fg, fill_hex=bg)
    ws.row_dimensions[6].height = 24
    ws.row_dimensions[7].height = 22
    put(ws, "M6", "Status rule", kind="label", bold=True, size=8, color=C["ink500"])
    put(ws, "M7", "Diagnostic level rounded down: <1 Not started · 1 Initial · 2 Defined · 3 Implemented · 4 Assured."
        + (" Module B and H rows held at Not started while no CRA notified body exists (Lists)." if HOLD else ""), kind="muted", size=8)
    header(ws, 9, ["ID", "Source", "Obligation", "Applies to", "Effective from", "Product-level or organisation-level",
                   "Evidence artefact", "Owner role", "Diagnostic question", "Diagnostic average (0-4)", "Status hold",
                   f"{X.client} status (Illustrative)", "Notes/guidance reference", "Area"], "B", height=42)
    for c in "JKLM":
        ws[f"{c}9"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for i, row in enumerate(ROWS):
        oid, area, src, obl, app, eff, lvl, evid, owner, q, notes = row
        rr = FIRST + i
        put(ws, f"B{rr}", oid, kind="label", bold=True, border=B_ROW, valign="top")
        put(ws, f"C{rr}", src, kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"D{rr}", obl, kind="label", border=B_ROW, wrap=True, valign="top")
        put(ws, f"E{rr}", app, kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"F{rr}", S26 if eff == "S" else D27, kind="input", fmt=NF_DATE, border=B_ROW, valign="top", align="left")
        put(ws, f"G{rr}", lvl, kind="label", border=B_ROW, valign="top", size=8)
        put(ws, f"H{rr}", evid, kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"I{rr}", owner, kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"J{rr}", q if q else None, kind="label", border=B_ROW, valign="top", align="center")
        put(ws, f"K{rr}", f'=IF(OR(J{rr}="",J{rr}="Ref"),"",INDEX(\'Diagnostic baseline\'!${TC}$6:${TC}${DB_LAST},MATCH(J{rr},\'Diagnostic baseline\'!$B$6:$B${DB_LAST},0)))',
            fmt="0.00", border=B_ROW, valign="top", align="center")
        put(ws, f"L{rr}", HOLD_TEXT if oid in HOLD else None, kind="input", border=B_ROW, valign="top", size=8, wrap=True,
            align="center")
        put(ws, f"M{rr}", f'=IF(J{rr}="Ref","Reference",IF(L{rr}<>"","Not started",IF(J{rr}="","Not assessed",'
            f'IF(K{rr}<{P["b1"]},"Not started",IF(K{rr}<{P["b2"]},"Initial",IF(K{rr}<{P["b3"]},"Defined",'
            f'IF(K{rr}<{P["b4"]},"Implemented","Assured")))))))',
            border=B_ROW, valign="top", align="center", bold=True)
        nts = notes or ""
        if oid in HOLD:
            nts = (nts + " " if nts else "") + f"Held at Not started: no CRA notified body verifiably designated (checks to {X.nb_check})."
        put(ws, f"N{rr}", nts or None, kind="muted", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"O{rr}", area, kind="muted", border=B_ROW, wrap=True, valign="top", size=8)
        nl = max(est_lines(obl, RW["D"], 9), est_lines(evid, RW["H"], 8), est_lines(nts, RW["N"], 8),
                 est_lines(src, RW["C"], 8), est_lines(area, RW["O"], 8), est_lines(owner, RW["I"], 8))
        ws.row_dimensions[rr].height = max(15, 11.6 * nl + 3)
    add_table(ws, "tblObligations", f"B9:O{LAST}")
    add_list_dv(ws, f"E{FIRST}:E{LAST}", LIST_REF["Applies to"])
    add_list_dv(ws, f"G{FIRST}:G{LAST}", LIST_REF["Level"])
    add_list_dv(ws, f"I{FIRST}:I{LAST}", LIST_REF["Owner role (RACI)"])
    add_list_dv(ws, f"J{FIRST}:J{LAST}", LIST_REF["Diagnostic question"],
                prompt="Map to a diagnostic question (Q1.1-Q10.4), Ref for reference rows, or leave blank")
    add_list_dv(ws, f"L{FIRST}:L{LAST}", LIST_REF["Status hold"],
                prompt="Hold the status at Not started (e.g. no notified body yet); clear it once the dependency is met")
    dvd = DataValidation(type="date", operator="between", formula1="DATE(2024,12,10)", formula2="DATE(2030,12,31)",
                         allow_blank=True)
    dvd.error = "Enter a date between 10 Dec 2024 and 31 Dec 2030."
    dvd.showErrorMessage = True
    ws.add_data_validation(dvd)
    dvd.add(f"F{FIRST}:F{LAST}")
    SR = f"M{FIRST}:M{LAST}"
    for st_, (bg, fg) in STATUS_COL.items():
        cf_text(ws, SR, st_, bg, fg=fg, bold=(st_ != "Reference"))
    cf_formula(ws, f"F{FIRST}:F{LAST}", f"F{FIRST}<={STATUS}", fg=C["signal"], bold=True)
    put(ws, f"D{LAST + 2}", "Effective dates in orange already apply on the status date (90-day plan, cell E5).",
        kind="muted", size=8)
    source_line(ws, f"B{LAST + 3}", f"Source: knowledge base 'Requirement checklists' tab ({X.facts}) and sections on Annex I, "
                "reporting, conformity, open source and enforcement; corporate guide 02 RACI for owner roles; diagnostic "
                f"baseline {X.baseline} for status. Paraphrases only: verify against the OJ text before relying on wording. Illustrative.")
    ws.freeze_panes = f"C{FIRST}"
    print_setup(ws, HDR, title_rows="9:9", area=f"A1:O{LAST + 3}")
    REG_ROWS = len(ROWS)
    # =====================================================================================
    # RAID LOG
    # =====================================================================================
    ws = ws_raid
    widths(ws, {"A": 2.5, "B": 7, "C": 28, "D": 50, "E": 12, "F": 12, "G": 12, "H": 12, "I": 12, "J": 56, "K": 22,
                "L": 11})
    risks = RISKS
    title_block(ws, LABEL + " · RAID LOG",
                f'="{TOP_PHRASE} ({TOP["id"]}, score "&G{7 + TOP_I}&") is the top risk; "&COUNTIF(H7:H{RL},"High")&" of "&COUNTA(B7:B{RL})&" risks rate High"',
                f"Risks, issues, assumptions and dependencies as at SteerCo #1, {X.steerco} · Score = likelihood x impact "
                "(1-5 each) · Illustrative", link_col="L")
    band(ws, 5, "Risks", "B", "L")
    header(ws, 6, ["ID", "Risk", "Description", "Likelihood (1-5)", "Impact (1-5)", "Score", "Rating", "Trend",
                   "Mitigations", "Owner", "Status"], "B", height=32)
    for c in "EFGHI":
        ws[f"{c}6"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for i, rk in enumerate(risks):
        rr = 7 + i
        put(ws, f"B{rr}", rk["id"], kind="label", bold=True, border=B_ROW, valign="top")
        put(ws, f"C{rr}", rk["title"], kind="label", bold=True, border=B_ROW, wrap=True, valign="top")
        put(ws, f"D{rr}", rk["description"], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"E{rr}", rk["likelihood"], kind="input", border=B_ROW, align="center", valign="top")
        put(ws, f"F{rr}", rk["impact"], kind="input", border=B_ROW, align="center", valign="top")
        put(ws, f"G{rr}", f"=E{rr}*F{rr}", border=B_ROW, align="center", valign="top", bold=True)
        put(ws, f"H{rr}", f'=IF(G{rr}>={P["rh"]},"High",IF(G{rr}>={P["rm"]},"Medium","Low"))', border=B_ROW,
            align="center", valign="top", bold=True)
        put(ws, f"I{rr}", rk["trend"], kind="input", border=B_ROW, valign="top", align="center")
        put(ws, f"J{rr}", rk["mitigations"], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"K{rr}", rk["owner"], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"L{rr}", "Open", kind="input", border=B_ROW, valign="top")
        ws.row_dimensions[rr].height = max(26, 11.6 * max(est_lines(rk["description"], 50, 8),
                                                            est_lines(rk["mitigations"], 56, 8), est_lines(rk["title"], 28)) + 3)
    add_table(ws, "tblRisks", f"B6:L{RL}")
    add_whole_dv(ws, f"E7:F{RL}", 1, 5)
    add_list_dv(ws, f"I7:I{RL}", LIST_REF["Trend"])
    add_list_dv(ws, f"L7:L{RL}", LIST_REF["RAID item status"])
    cf_text(ws, f"H7:H{RL}", "High", C["red"])
    cf_text(ws, f"H7:H{RL}", "Medium", C["amber"])
    cf_text(ws, f"H7:H{RL}", "Low", C["green"])
    cf_text(ws, f"I7:I{RL}", "Rising", C["red"], bold=True)
    RC = RL + 1  # check row (17)
    put(ws, f"C{RC}", f"Check: scores and ratings reproduce the {X.v} register", kind="muted", size=8)
    ctl_scores = "{" + ";".join(str(r["score"]) for r in risks) + "}"
    ctl_ratings = "{" + ";".join(f'"{r["rating"]}"' for r in risks) + "}"
    put(ws, f"G{RC}", f'=IF(AND(SUMPRODUCT(--(G7:G{RL}={ctl_scores}))={NR},SUMPRODUCT(--(H7:H{RL}={ctl_ratings}))={NR}),"OK","CHECK")',
        align="center", bold=True)
    cf_checks(ws, f"G{RC}")
    RAID_CHECK = f"'RAID log'!$G${RC}"
    # heatmap on five uniform columns E..I
    O = RL - 16  # row offset versus the {X.v} layout (ten risks)
    band(ws, 19 + O, "Risk heatmap: likelihood (rows) x impact (columns); cells list risk IDs", "B", "L")
    put(ws, f"D{20 + O}", "Likelihood", kind="muted", size=8, bold=True, align="right")
    HM_ROWS = {5: 21 + O, 4: 22 + O, 3: 23 + O, 2: 24 + O, 1: 25 + O}
    HM_COLS = {1: "E", 2: "F", 3: "G", 4: "H", 5: "I"}
    IMP = 26 + O
    for lk, rr in HM_ROWS.items():
        put(ws, f"D{rr}", lk, kind="label", bold=True, align="right")
        for im, cc in HM_COLS.items():
            ws[f"{cc}{rr}"] = ArrayFormula(f"{cc}{rr}", f'=_xlfn.TEXTJOIN(", ",TRUE,IF(($E$7:$E${RL}=$D{rr})*($F$7:$F${RL}={cc}${IMP}),$B$7:$B${RL},""))')
            cell = ws[f"{cc}{rr}"]
            cell.font = font(C["ink900"], bold=True, size=9)
            cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
            cell.border = Border(left=side(C["white"], "medium"), right=side(C["white"], "medium"),
                                 top=side(C["white"], "medium"), bottom=side(C["white"], "medium"))
        ws.row_dimensions[rr].height = 30
    for im, cc in HM_COLS.items():
        put(ws, f"{cc}{IMP}", im, kind="label", bold=True, align="center")
    put(ws, f"G{27 + O}", "Impact", kind="muted", size=8, bold=True, align="center")
    HM = f"E{21 + O}:I{25 + O}"
    cf_formula(ws, HM, f"$D{21 + O}*E${IMP}>={P['rh']}", bg="F3C9C4", fg=C["red"])
    cf_formula(ws, HM, f"AND($D{21 + O}*E${IMP}>={P['rm']},$D{21 + O}*E${IMP}<{P['rh']})", bg="F6DDC5", fg=C["amber"])
    cf_formula(ws, HM, f"$D{21 + O}*E${IMP}<{P['rm']}", bg="CDEBDC", fg=C["green"])
    put(ws, f"J{21 + O}", "Red zone: score 12 or more (High). Amber: 5 to 11 (Medium). Green: below 5 (Low). Thresholds on Lists.",
        kind="muted", size=8, wrap=True)
    put(ws, f"J{22 + O}", f'="Risks plotted: "&COUNTA(B7:B{RL})&". Highest: "&INDEX(B7:B{RL},MATCH(MAX(G7:G{RL}),G7:G{RL},0))&" ("&INDEX(C7:C{RL},MATCH(MAX(G7:G{RL}),G7:G{RL},0))&")."',
        size=8, wrap=True)
    # issues
    IB = 29 + O
    band(ws, IB, "Issues", "B", "L")
    header(ws, IB + 1, ["ID", "Issue", "Description", "Due", "Status", "Linked risk", "Raised from", "Owner", "Next step"], "B",
           height=20)


    def _issue_default(iss):
        t = X.find_task(lambda t_: t_["end"] == iss["due"])
        nxt = f"{t['task']} ({t['id']})." if t else f"Resolve by {iss['due']}."
        return ["", "", nxt]


    for i, iss in enumerate(D["issues"]):
        rr = IB + 2 + i
        lr, src_, nxt = X.t(f"d11.issue.{iss['id']}", _issue_default(iss))
        put(ws, f"B{rr}", iss["id"], kind="label", bold=True, border=B_ROW, valign="top")
        put(ws, f"C{rr}", iss["title"], kind="label", bold=True, border=B_ROW, wrap=True, valign="top")
        put(ws, f"D{rr}", iss["description"], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"E{rr}", pdate(iss["due"]), kind="input", fmt=NF_DATE, border=B_ROW, valign="top", align="left")
        put(ws, f"F{rr}", "Open", kind="input", border=B_ROW, valign="top", align="center")
        put(ws, f"G{rr}", lr or None, kind="label", border=B_ROW, valign="top", size=8, align="center")
        put(ws, f"H{rr}", src_ or None, kind="label", border=B_ROW, valign="top", size=8, wrap=True)
        put(ws, f"I{rr}", iss["owner"], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"J{rr}", nxt, kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        ws.row_dimensions[rr].height = max(26, 11.6 * max(est_lines(iss["description"], 50, 8), est_lines(nxt, 56, 8),
                                                            est_lines(iss["owner"], 12, 8), est_lines(src_, 12, 8)) + 3)
    IS_LAST = IB + 1 + max(len(D["issues"]), 1)
    add_table(ws, "tblIssues", f"B{IB + 1}:J{IS_LAST}")
    add_list_dv(ws, f"F{IB + 2}:F{IS_LAST}", LIST_REF["RAID item status"])
    # assumptions
    AB = IS_LAST + 2
    band(ws, AB, "Assumptions", "B", "L")
    header(ws, AB + 1, ["ID", "Assumption", "Basis", "Validate by", "Status", "Linked risk", "Category", "Owner",
                    "Impact if wrong"], "B", height=20)
    assumptions = [
        ("AS01", "No harmonised standard for Class I products is cited in the OJ before Q3 2027.",
         f"None cited as at {X.facts} (F07); EN 40000-1-4 due 30 Oct 2027 per standards-tracking secondary sources.",
         dt.date(2027, 6, 30), "Valid", "R03", "Regulatory", "Compliance lead",
         "If one is cited earlier, Class I families could revert to Module A (closer to the Low scenario)."),
        ("AS02", "At least one CRA notified body with Module B and Module H scope is designated by Q1 2027.",
         "Art 35(2): Member States 'strive' for enough bodies by 11 Dec 2026; candidates in the pipeline per vendor statements (RD10).",
         dt.date(2027, 3, 31), "At risk", "R01", "Market", "Head of quality & regulatory",
         f"{Words(NB_N)} famil{'ies' if NB_N != 1 else 'y'} ({eur_m0(X.eu_nb_m)} of EU revenue) cannot be certified by 11 Dec 2027."),
        ("AS03", "Commission guidance C(2026) 5252 is adopted without material change to scope, remote data processing or support-period readings.",
         "Content approved 27 Jul 2026; formal adoption pending all language versions (F10).",
         dt.date(2027, 3, 31), "Valid", "R09", "Regulatory", "Compliance lead",
         "Scope and support-period decisions reopen; decision records must cite the new version."),
        ("AS04", f"{X.country}'s CRA implementation law is promulgated without changes to coordinator CSIRT reporting or market surveillance arrangements.",
         NATIONAL_LAW.get(X.country, ("National implementation status as tracked in F16.", None))[0],
         NATIONAL_LAW.get(X.country, (None, dt.date(2026, 12, 31)))[1], "Valid", "R06", "Regulatory", "General Counsel",
         "Update the reporting runbook and authority contacts."),
        ("AS05", f"{D['cost_model']['engineering_fte_years']} FTE-years of remediation can be ring-fenced in the 2027 engineering plan.",
         X.t("d11.as05.basis", "Cost model remediation drivers; R02 mitigation."),
         dt.date(2027, 1, 31), "Valid", "R02", "Internal", "CTO",
         "Remediation slips; cost moves towards the High scenario (+30% engineering)."),
        ("AS06", f"The legal opinion confirms {PROV_LABELS} as Default class.",
         "; ".join(x for x in ([f"Issue {CLASS_ISSUE}"] if CLASS_ISSUE else []) + ([f"SteerCo decision {STRICT_SD} plans notified-body capacity for {'both' if NPROV == 2 else ('it' if NPROV == 1 else 'all')} until the opinion lands."] if STRICT_SD else [])),
         pdate(LEGAL_DUE) if LEGAL_DUE else X.board_date, "Open", "R01", "Legal", "General Counsel",
         f"{eur_m0(sum(f['eu_revenue_m'] for f in PROV))} more EU revenue would need a notified body ("
         + " + ".join(f"{X.short(f)} EUR {f['eu_revenue_m']:,.1f}m" for f in sorted(PROV, key=lambda f: X.label(f).lower()))
         + f"); {'both move' if NPROV == 2 else ('it moves' if NPROV == 1 else 'all move')} to Wave 1."),
        ("AS07", "No implementing act on SBOM format (Art 13(24)) or notification format (Art 14(10)) departs from the current design.",
         f"None adopted or drafted as at {X.facts}; design to CycloneDX 1.6+ / SPDX 3.0.1+ and the ENISA SRP glossary.",
         dt.date(2027, 3, 31), "Valid", "R04", "Regulatory", "Head of platform engineering",
         "Rework of the SBOM pipeline or report templates."),
        ("AS08", "The Digital Omnibus does not change CRA application dates or Art 14 duties.",
         "COM(2025) 837 does not amend the CRA; Council mandate agreed 21 Oct 2026 (ST 14756/26), not adopted (F17).",
         dt.date(2027, 3, 31), "Valid", "R09", "Regulatory", "Compliance lead", "Re-plan if the CRA is reopened."),
    ]
    assumptions = [a for a in assumptions if a[0] != "AS06" or PROV]
    for i, a in enumerate(assumptions):
        rr = AB + 2 + i
        put(ws, f"B{rr}", a[0], kind="label", bold=True, border=B_ROW, valign="top")
        put(ws, f"C{rr}", a[1], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"D{rr}", a[2], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"E{rr}", a[3], kind="input", fmt=NF_DATE, border=B_ROW, valign="top", align="left")
        put(ws, f"F{rr}", a[4], kind="input", border=B_ROW, valign="top", align="center")
        put(ws, f"G{rr}", a[5], kind="label", border=B_ROW, valign="top", size=8, align="center")
        put(ws, f"H{rr}", a[6], kind="label", border=B_ROW, valign="top", size=8)
        put(ws, f"I{rr}", a[7], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"J{rr}", a[8], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        ws.row_dimensions[rr].height = max(26, 11.6 * max(est_lines(a[1], 28, 8), est_lines(a[2], 50, 8),
                                                            est_lines(a[8], 56, 8), est_lines(a[7], 12, 8)) + 3)
    AS_LAST = AB + 2 + len(assumptions) - 1
    add_table(ws, "tblAssumptionsRAID", f"B{AB + 1}:J{AS_LAST}")
    add_list_dv(ws, f"F{AB + 2}:F{AS_LAST}", LIST_REF["RAID item status"])
    cf_text(ws, f"F{AB + 2}:F{AS_LAST}", "At risk", C["amber"])
    # dependencies
    DP0 = AS_LAST + 2
    band(ws, DP0, "Dependencies", "B", "L")
    header(ws, DP0 + 1, ["ID", "Dependency", "Detail", "Needed by", "Status", "Type", "Workstream", "Affects",
                         "Owner / provider"], "B", height=20)
    ONCALL = X.find_task(lambda t_: "on-call" in t_["task"].lower())
    _m = re.search(r"top (\d+)", X.tasks.get("T20", {}).get("task", ""))
    TOPSUP = f"top {_m.group(1)}" if _m else "most"
    deps = [
        ("DP01", "CRA notified-body designation", f"A body notified for Module B and Module H in NANDO, with capacity for {words(NB_N)} famil{'ies' if NB_N != 1 else 'y'}.",
         pdate(X.ms_date("M7", "31 Mar 2027")), "At risk", "External", "WS7", "M5, M7, M12; T25", "Head of quality & regulatory / Member State notifying authorities"),
        ("DP02", f"Legal opinion on {PROV_LABELS}", f"Classification against Annex III Class I item{'s' if len(X.provisional_annex_items()) != 1 else ''} {join(X.provisional_annex_items())}.",
         pdate(LEGAL_DUE) if LEGAL_DUE else X.board_date, "In progress", "Internal", "WS2", "M4; T09", "General Counsel"),
        ("DP03", ONCALL["task"] if ONCALL else "", X.t("d11.dp03.detail", "Needed to sustain weekend filing (R08)."),
         pdate(ONCALL["end"]) if ONCALL else X.board_date, "In progress", "Internal", "WS3", ONCALL["id"] if ONCALL else "",
         (ONCALL["owner"] + (" / works council" if "works council" in ONCALL["task"].lower() else "")) if ONCALL else ""),
        ("DP04", f"Board decisions {_span(BOARD_IDS)}", X.t("d11.dp04.detail", "The board decisions in the decision log."),
         X.board_date, "Planned", "Internal", "WS1", "M3; T03, T25, T27", "Executive sponsor / board"),
        ("DP05", "System-of-record selection", "10-year evidence retention per version; reasoned-request export (SD4).",
         pdate(X.task_end("T05", X.board)), "In progress", "Internal", "WS6", "T05; M11", "Compliance lead"),
        ("DP06", "Harmonised standards cited in the OJ", f"EN 40000 series and EN 304 6xx verticals; none cited as at {X.facts}.",
         dt.date(2027, 6, 30), "Monitoring", "External", "WS7", "Class I route (R03)", "Compliance lead / CEN-CENELEC, ETSI, European Commission"),
        ("DP07", "Supplier SBOMs and vulnerability-notification commitments", f"Clause pack accepted by the {TOPSUP} security-relevant suppliers.",
         pdate(X.task_end("T20", "29 Jan 2027")), "Not started", "External", "WS5", "T20; M8; R04", "Head of procurement / suppliers"),
    ]
    deps = [d_ for d_ in deps if d_[1] and (d_[0] != "DP02" or PROV)]
    for i, d_ in enumerate(deps):
        rr = DP0 + 2 + i
        put(ws, f"B{rr}", d_[0], kind="label", bold=True, border=B_ROW, valign="top")
        put(ws, f"C{rr}", d_[1], kind="label", bold=True, border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"D{rr}", d_[2], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"E{rr}", d_[3], kind="input", fmt=NF_DATE, border=B_ROW, valign="top", align="left")
        put(ws, f"F{rr}", d_[4], kind="input", border=B_ROW, valign="top", align="center")
        put(ws, f"G{rr}", d_[5], kind="label", border=B_ROW, valign="top", size=8, align="center")
        put(ws, f"H{rr}", d_[6], kind="label", border=B_ROW, valign="top", size=8, align="center")
        put(ws, f"I{rr}", d_[7], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"J{rr}", d_[8], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        ws.row_dimensions[rr].height = max(26, 11.6 * max(est_lines(d_[2], 50, 8), est_lines(d_[8], 56, 8),
                                                            est_lines(d_[1], 28, 8), est_lines(d_[7], 12, 8)) + 3)
    DP_LAST = DP0 + 2 + len(deps) - 1
    add_table(ws, "tblDependencies", f"B{DP0 + 1}:J{DP_LAST}")
    add_list_dv(ws, f"F{DP0 + 2}:F{DP_LAST}", LIST_REF["RAID item status"])
    add_list_dv(ws, f"G{DP0 + 2}:G{DP_LAST}", '"Internal,External"')
    cf_text(ws, f"F{DP0 + 2}:F{DP_LAST}", "At risk", C["amber"])
    source_line(ws, f"B{DP_LAST + 2}", f"Source: pack_data.json {X.v} (risks, issues, decisions, programme); knowledge base facts as "
                f"at {X.facts}. Assumptions, dependencies, issue sources and next steps drafted from the same sources. Illustrative.")
    ws.freeze_panes = "A5"
    print_setup(ws, HDR, area=f"A1:L{DP_LAST + 2}")
    ws.row_breaks.append(_Break(id=28 + O))
    # =====================================================================================
    # DECISION LOG
    # =====================================================================================
    ws = ws_dec
    widths(ws, {"A": 2.5, "B": 7, "C": 12, "D": 13, "E": 40, "F": 40, "G": 46, "H": 22, "I": 18, "J": 20})
    title_block(ws, LABEL + " · DECISION LOG",
                f'="SteerCo #1 endorsed "&COUNTIF(I6:I{5 + ND},"Endorsed*")&" decisions; the board is asked for "&COUNTIF(I6:I{5 + ND},"Proposed")&" more on {X.board}"',
                f"SteerCo #1 ({X.steerco}) and board ({X.board}) decisions with rationale, owner and status · Illustrative",
                link_col="J")
    header(ws, 5, ["ID", "Date", "Forum", "Decision", "Detail / outcome", "Rationale", "Owner", "Status",
                   "Linked items"], "B", height=20)
    r = 6
    for d_ in D["decisions"]["steerco_1"]:
        own, rat, link = X.t(f"d11.decision.{d_['id']}", ["Programme director", "", ""])
        put(ws, f"B{r}", d_["id"], kind="label", bold=True, border=B_ROW, valign="top")
        put(ws, f"C{r}", X.steerco_date, kind="input", fmt=NF_DATE, border=B_ROW, valign="top", align="left")
        put(ws, f"D{r}", "SteerCo #1", kind="label", border=B_ROW, valign="top")
        put(ws, f"E{r}", d_["decision"], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"F{r}", X.t(f"d11.decision_detail.{d_['id']}", d_.get("detail", "")) or None, kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"G{r}", rat or None, kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"H{r}", own, kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"I{r}", d_.get("outcome") or "Endorsed (illustrative)", kind="input", border=B_ROW, valign="top", size=8)
        put(ws, f"J{r}", link or None, kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        ws.row_dimensions[r].height = 11.6 * max(est_lines(d_["decision"], 40, 8), est_lines(rat, 46, 8)) + 4
        r += 1
    for d_ in D["decisions"]["board"]:
        own, rat, link = X.t(f"d11.decision.{d_['id']}", ["Executive sponsor", "", ""])
        put(ws, f"B{r}", d_["id"], kind="label", bold=True, border=B_ROW, valign="top")
        put(ws, f"C{r}", X.board_date, kind="input", fmt=NF_DATE, border=B_ROW, valign="top", align="left")
        put(ws, f"D{r}", "Board", kind="label", border=B_ROW, valign="top")
        put(ws, f"E{r}", d_["decision"], kind="label", border=B_ROW, wrap=True, valign="top", size=8, bold=True)
        put(ws, f"F{r}", d_["detail"], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"G{r}", rat or None, kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"H{r}", own, kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"I{r}", "Proposed", kind="input", border=B_ROW, valign="top", size=8)
        put(ws, f"J{r}", link or None, kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        ws.row_dimensions[r].height = 11.6 * max(est_lines(d_["detail"], 40, 8), est_lines(rat, 46, 8)) + 4
        r += 1
    add_table(ws, "tblDecisions", f"B5:J{r - 1}")
    add_list_dv(ws, f"I6:I{r - 1}", LIST_REF["Decision status"])
    cf_text(ws, f"I6:I{r - 1}", "Endorsed (illustrative)", C["green"])
    cf_text(ws, f"I6:I{r - 1}", "Approved", C["green"])
    cf_text(ws, f"I6:I{r - 1}", "Proposed", C["acc100"], fg=C["acc700"])
    cf_text(ws, f"I6:I{r - 1}", "Rejected", C["red"])
    source_line(ws, f"B{r + 1}", f"Source: pack_data.json {X.v} (decisions.steerco_1, decisions.board). Rationale and owners drafted "
                f"from the programme data and knowledge base. Board decisions remain Proposed until {X.board}. Illustrative.")
    ws.freeze_panes = "C6"
    print_setup(ws, HDR, title_rows="5:5", area=f"A1:J{r + 1}")

    # =====================================================================================
    # KPI TRACKER
    # =====================================================================================
    ws = ws_kpi
    MONTHS = [dt.date(2026, 11, 1), dt.date(2026, 12, 1)] + [dt.date(2027, m, 1) for m in range(1, 13)]
    MCOLS = [get_column_letter(10 + i) for i in range(len(MONTHS))]  # J..W
    widths(ws, {"A": 2.5, "B": 6, "C": 34, "D": 18, "E": 10, "F": 28, "G": 9, "H": 9, "I": 9,
                **{c: 8.5 for c in MCOLS}})
    title_block(ws, LABEL + " · KPI TRACKER",
                f'="Of {NK} KPIs at SteerCo #1, "&COUNTIF(G6:G{KL},"Green")&" are Green, "&COUNTIF(G6:G{KL},"Amber")&" Amber and "&COUNTIF(G6:G{KL},"Red")&" Red{X.t("d11.kpi.red_note", "")}"',
                f"Values as at {X.steerco} (SteerCo #1) · Enter monthly actuals in the blue month columns · Plan "
                "trajectories below, aligned to the same months · Illustrative", link_col="W")
    header(ws, 5, ["ID", "KPI", "Oct 2026 actual", "Value", "Target", "RAG", "Trend", "Source"] +
           [m.strftime("%b %Y") for m in MONTHS], "B", height=32)
    for c in MCOLS + ["E", "G"]:
        ws[f"{c}5"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    kfmt = {"K01": NF_PCT1, "K05": '0.00" h"', "K07": NF_PCT0, "K11": NF_EUR}
    for i, k in enumerate(D["kpis"]):
        rr = 6 + i
        put(ws, f"B{rr}", k["id"], kind="label", bold=True, border=B_ROW, valign="top")
        put(ws, f"C{rr}", k["name"], kind="label", border=B_ROW, wrap=True, valign="top")
        put(ws, f"D{rr}", k["display"], kind="label", border=B_ROW, wrap=True, valign="top", bold=True)
        if k["id"] == "K01":
            put(ws, f"E{rr}", "=" + MX_AVG, fmt=NF_PCT1, border=B_ROW, valign="top")
        else:
            put(ws, f"E{rr}", k["value"], kind="input", fmt=kfmt.get(k["id"], "0"), border=B_ROW, valign="top")
        put(ws, f"F{rr}", k["target"], kind="label", border=B_ROW, wrap=True, valign="top", size=8, indent=1)
        put(ws, f"G{rr}", k["rag"], kind="input", border=B_ROW, valign="top", align="center")
        put(ws, f"H{rr}", k["trend"], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"I{rr}", k["source"], kind="muted", border=B_ROW, wrap=True, valign="top", size=7)
        for c in MCOLS:
            put(ws, f"{c}{rr}", None, kind="input", border=B_ROW)
        ws.row_dimensions[rr].height = max(26, 11.6 * max(est_lines(k["name"], 34), est_lines(k["target"], 28, 8),
                                                            est_lines(k["source"], 9, 7), est_lines(k["trend"], 9, 8)) + 3)
    add_table(ws, "tblKPIs", f"B5:{MCOLS[-1]}{KL}")
    add_list_dv(ws, f"G6:G{KL}", LIST_REF["RAG"])
    cf_rag(ws, f"G6:G{KL}")
    KO = KL - 17  # row offset versus the {X.v} layout (twelve KPIs)
    # trajectories: months aligned with the KPI month columns (Sep and Oct 2026 in H and I)
    band(ws, 19 + KO, "Plan trajectories (Oct 2026 values are illustrative actuals; later months are plan)", "B", MCOLS[-1])
    TM = [dt.date(2026, 9, 1), dt.date(2026, 10, 1)] + MONTHS  # Sep 2026..Dec 2027 (16)
    TCOLS = ["H", "I"] + MCOLS
    header(ws, 20 + KO, ["Ref", "Series", "", "", "", ""] + [m.strftime("%b %y") for m in TM], "B", height=20)
    ws.merge_cells(f"C{20 + KO}:G{20 + KO}")
    for c in TCOLS:
        ws[f"{c}{20 + KO}"].alignment = Alignment(horizontal="center", vertical="center")
    rp = D["kpi_trajectories"]["readiness_index_plan"]
    sb = D["kpi_trajectories"]["sbom_coverage_plan_and_actual"]
    series = [
        ("T1", "Readiness index: plan", {m: rp.get(m.strftime("%b %Y")) for m in TM}, "input"),
        ("T2", "Readiness index: actual", {}, "actual_r"),
        ("T3", "Readiness index: target", {dt.date(2027, 6, 1): f"={P['t1']}", dt.date(2027, 11, 1): f"={P['t2']}"}, "target"),
        ("T4", "Readiness variance vs plan (pts)", {}, "var_r"),
        ("T5", "Signed SBOM coverage: plan", {m: (sb.get(m.strftime("%b %Y")) if m >= dt.date(2026, 11, 1) else None) for m in TM}, "input"),
        ("T6", "Signed SBOM coverage: actual", {dt.date(2026, 9, 1): sb.get("Sep 2026"), dt.date(2026, 10, 1): sb.get("Oct 2026")}, "input_a"),
        ("T7", "Signed SBOM coverage: target", {dt.date(2027, 3, 1): 1.0}, "input"),
    ]
    for i, (ref, nm, vals, kind) in enumerate(series):
        rr = 21 + KO + i
        put(ws, f"B{rr}", ref, kind="muted", border=B_ROW)
        put(ws, f"C{rr}", nm, kind="label", border=B_ROW, bold=(kind == "input" and "plan" in nm))
        ws.merge_cells(f"C{rr}:G{rr}")
        for c in "DEFG":
            ws[f"{c}{rr}"].border = B_ROW
        for m, c in zip(TM, TCOLS):
            if kind == "actual_r":
                if m == dt.date(2026, 10, 1):
                    put(ws, f"{c}{rr}", "=" + MX_AVG, fmt=NF_PCT0, border=B_ROW, align="center")
                elif m > dt.date(2026, 10, 1):
                    put(ws, f"{c}{rr}", None, kind="input", fmt=NF_PCT0, border=B_ROW, align="center")
                else:
                    ws[f"{c}{rr}"].border = B_ROW
            elif kind == "var_r":
                put(ws, f"{c}{rr}", f'=IF(OR({c}{21 + KO}="",{c}{22 + KO}=""),"",{c}{22 + KO}-{c}{21 + KO})', fmt='+0.0%;-0.0%;0.0%', border=B_ROW,
                    align="center")
            elif kind == "target":
                put(ws, f"{c}{rr}", vals.get(m), fmt=NF_PCT0, border=B_ROW, align="center")
            else:
                v = vals.get(m)
                if v is None:
                    put(ws, f"{c}{rr}", None, kind="input" if (kind == "input_a" and m > dt.date(2026, 10, 1)) else "label",
                        fmt=NF_PCT0, border=B_ROW, align="center")
                else:
                    put(ws, f"{c}{rr}", v, kind="input", fmt=NF_PCT0, border=B_ROW, align="center")
    put(ws, f"C{28 + KO}", f"Check: the readiness plan starts at the {X.baseline} baseline (Oct 2026 plan = actual)", kind="muted", size=8)
    put(ws, f"I{28 + KO}", f'=IF(ABS(I{21 + KO}-I{22 + KO})<0.001,"OK","CHECK")', bold=True, align="center")
    cf_checks(ws, f"I{28 + KO}")
    KPI_CHECK = f"'KPI tracker'!$I${28 + KO}"
    # charts (series built explicitly so the merged label cells are not read as data)


    def traj_chart(title, rows, anchor):
        ch = LineChart()
        ch.title = chart_title(title)
        for row in rows:
            s = Series(Reference(ws, min_col=8, max_col=7 + len(TM), min_row=row))
            s.tx = SeriesLabel(strRef=StrRef(f"'KPI tracker'!$C${row}"))
            ch.series.append(s)
        ch.set_categories(Reference(ws, min_col=8, max_col=7 + len(TM), min_row=20 + KO))
        color_series(ch.series[0], C["acc600"], line=True)
        ch.series[0].marker.symbol = "none"
        ch.series[1].marker.symbol = "circle"
        ch.series[1].marker.size = 7
        ch.series[1].marker.graphicalProperties.solidFill = C["navy"]
        ch.series[1].marker.graphicalProperties.line.solidFill = C["navy"]
        ch.series[1].graphicalProperties.line.noFill = True
        ch.series[2].marker.symbol = "diamond"
        ch.series[2].marker.size = 9
        ch.series[2].marker.graphicalProperties.solidFill = C["signal"]
        ch.series[2].marker.graphicalProperties.line.solidFill = C["signal"]
        ch.series[2].graphicalProperties.line.noFill = True
        style_axes(ch, y_fmt="0%", gridlines=True)
        ch.y_axis.scaling.min = 0
        ch.y_axis.scaling.max = 1
        ch.legend.position = "b"
        ch.width = 16
        ch.height = 7
        ws.add_chart(ch, anchor)


    traj_chart("Readiness index: plan, actual and targets", [21 + KO, 22 + KO, 23 + KO], f"C{30 + KO}")
    traj_chart("Signed SBOM coverage: plan, actual and target", [25 + KO, 26 + KO, 27 + KO], f"J{30 + KO}")
    source_line(ws, f"B{45 + KO}", f"Source: pack_data.json {X.v} (kpis, kpi_trajectories). K01 and the Oct 2026 readiness actual link "
                "live to the Product x obligation matrix. SBOM Sep 2026 is the pre-programme measurement. Illustrative.")
    ws.freeze_panes = "D6"
    print_setup(ws, HDR, title_rows="5:5", area=f"A1:{MCOLS[-1]}{45 + KO}")
    # =====================================================================================
    # RACI
    # =====================================================================================
    ws = ws_raci
    _acct = X.find_decision(lambda d_: re.match(r"^(.+?) as accountable executive", d_.get("detail", "")))
    ACCT = (" In the illustrative engagement the " + re.match(r"^(.+?) as accountable executive", _acct["detail"]).group(1)
            + f" is the accountable executive ({_acct['id']}).") if _acct else ""
    ROLES = ["Executive sponsor", "Compliance lead", "Product security officer", "PSIRT lead", "Engineering lead", "Legal",
             "Procurement", "Product management"]
    RCOL = [get_column_letter(4 + i) for i in range(len(ROLES))]  # D..K
    widths(ws, {"A": 2.5, "B": 40, "C": 30, **{c: 12 for c in RCOL}, "L": 20, "M": 9})
    title_block(ws, LABEL + " · RACI",
                "Every CRA decision has exactly one accountable role; three cannot wait for a committee",
                "Decision RACI from the corporate implementation guide (section 2) · R responsible, A accountable, "
                "C consulted, I informed · One A per row, always a named individual", link_col="M")
    header(ws, 5, ["Decision", "Basis"] + ROLES + ["Accountable", "One A?"], "B", height=32)
    for c in RCOL + ["M"]:
        ws[f"{c}5"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    raci = [
        ("Scope and classification decision per product", "Arts 2-3, 7; IR 2025/2392", "IACIRCIR"),
        ("Risk assessment sign-off", "Art 13(2)-(4)", "ICACRIIC"),
        ("Release gate", "Annex I Part I(2)(a); guidance paras 230-237", "IIACRIIC"),
        ("Declaration of conformity signature", "Art 28; Annex V", "ARCICCII"),
        ("Art 14 awareness decision", "Guidance para 213", "IICARIII"),
        ("Notified-body relationship", "Art 32; Annex VIII", "CARICCRI"),
        ("Supplier terms", "Art 13(5); Art 23", "ICCICRAI"),
        ("Support period and end-of-support decision", "Art 13(8), (19)", "ICCCCCIA"),
        ("Steward determination for published FOSS", "Arts 3(14), 24", "ICCIRAIC"),
        ("Programme budget", "Corporate guide section 11", "ARCCCICC"),
    ]
    for i, (dec, basis, codes) in enumerate(raci):
        rr = 6 + i
        put(ws, f"B{rr}", dec, kind="label", bold=True, border=B_ROW, wrap=True)
        put(ws, f"C{rr}", basis, kind="muted", border=B_ROW, wrap=True, size=8)
        for c, code in zip(RCOL, codes):
            put(ws, f"{c}{rr}", code, kind="input", border=B_ROW, align="center", bold=True, fill_hex=C["white"])
        put(ws, f"L{rr}", f'=IF(COUNTIF(D{rr}:K{rr},"A")=1,INDEX($D$5:$K$5,MATCH("A",D{rr}:K{rr},0)),"Check")', border=B_ROW,
            bold=True)
        put(ws, f"M{rr}", f'=IF(COUNTIF(D{rr}:K{rr},"A")=1,"OK","CHECK")', border=B_ROW, align="center", bold=True)
        ws.row_dimensions[rr].height = 26
    add_table(ws, "tblRACI", "B5:M15")
    add_list_dv(ws, "D6:K15", LIST_REF["RACI code"])
    cf_text(ws, "D6:K15", "A", C["acc600"])
    cf_text(ws, "D6:K15", "R", C["acc100"], fg=C["acc700"])
    cf_text(ws, "D6:K15", "C", C["ink100"], fg=C["ink700"], bold=False)
    cf_checks(ws, "M6:M15")
    put(ws, "B16", "All rows have exactly one A", kind="muted", size=8)
    put(ws, "M16", '=IF(COUNTIF(M6:M15,"OK")=10,"OK","CHECK")', align="center", bold=True)
    cf_checks(ws, "M16")
    band(ws, 18, "Legend", "B", "M")
    legend = [("A", "Accountable: owns the outcome. Exactly one per row, always a named individual, never a team.", C["acc600"], C["white"]),
              ("R", "Responsible: does the work.", C["acc100"], C["acc700"]),
              ("C", "Consulted: asked before the decision.", C["ink100"], C["ink700"]),
              ("I", "Informed: told after the decision.", C["white"], C["ink900"])]
    for i, (code, desc, bg, fg) in enumerate(legend):
        rr = 19 + i
        cell = ws[f"B{rr}"]
        cell.value = code
        cell.font = font(fg, bold=True)
        cell.fill = fill(bg)
        cell.alignment = Alignment(horizontal="center")
        cell.border = B_BOX
        put(ws, f"C{rr}", desc, kind="label")
    band(ws, 24, "Decision rights that must sit with named individuals", "B", "M")
    header(ws, 25, ["Decision", "Holder", "Deputy chain", "", "", "Written rule"], "B", height=20)
    for c in "HIJKLM":
        ws[f"{c}25"].fill = fill(C["ink900"])
    rights = [
        ("Declaring awareness of an actively exploited vulnerability or severe incident, at any hour", "PSIRT lead",
         "Two named deputies on the on-call rota", "Awareness is a reasonable degree of certainty after an immediate assessment (guidance para 213); no approval step may precede it."),
        ("Submitting the 24-hour early warning", "On-call Primary or Secondary Assigned Representative",
         "Any other registered Assigned Representative", "Legal reviews the 72-hour and final reports, not the early warning."),
        ("Signing the EU declaration of conformity", "Executive sponsor, or a delegate named in a signed instrument",
         "One named alternate", "The signatory assumes responsibility for compliance (Art 28(4)); no delegation by email."),
        ("Accepting residual product risk", "Product security officer", "Executive sponsor on appeal",
         "Cost, risk appetite or commercial strategy are not relevant (guidance paras 156-163)."),
        ("Approving a non-applicable Annex I Part I(2) item", "Product security officer", "None",
         "Justification recorded in the risk assessment (Art 13(3)-(4); Recital 55)."),
        ("Blocking a release", "Product security officer", "Executive sponsor",
         "Release-blocking authority is written into the sponsor's mandate."),
        ("Choosing the main-establishment Member State and coordinator CSIRT", "Compliance lead with legal", "None",
         "Decided and recorded before any incident (Art 14(7))."),
    ]
    for i, (dec, holder, deputy, rule) in enumerate(rights):
        rr = 26 + i
        put(ws, f"B{rr}", dec, kind="label", bold=True, border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"C{rr}", holder, kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"D{rr}", deputy, kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        ws.merge_cells(f"D{rr}:F{rr}")
        put(ws, f"G{rr}", rule, kind="muted", border=B_ROW, wrap=True, valign="top", size=8)
        ws.merge_cells(f"G{rr}:M{rr}")
        ws.row_dimensions[rr].height = 11.6 * max(est_lines(dec, 40, 8), est_lines(rule, 90, 8), est_lines(holder, 30, 8)) + 4
    source_line(ws, "B34", "Source: knowledge base corporate implementation guide, section 2 (Governance: roles, decision rights and "
                "cadence)." + ACCT)
    ws.freeze_panes = "C6"
    print_setup(ws, HDR, area="A1:M34")

    # =====================================================================================
    # STAKEHOLDER REGISTER
    # =====================================================================================
    ws = ws_stk
    widths(ws, {"A": 2.5, "B": 7, "C": 30, "D": 20, "E": 8, "F": 8, "G": 15, "H": 13, "I": 13, "J": 7, "K": 28, "L": 44,
                "M": 24, "N": 22, "O": 14})
    title_block(ws, LABEL + " · STAKEHOLDER REGISTER",
                f'="Of "&COUNTA(B6:B{SK_LAST})&" stakeholder groups, "&COUNTIF(G6:G{SK_LAST},"Manage closely")&" need close management and "&COUNTIF(J6:J{SK_LAST},"Yes")&" must move stance before Dec 2027"',
                "Power and interest on a 1-5 scale · Engagement approach derived from power and interest (thresholds on "
                "Lists) · Stance now and target · Illustrative", link_col="O")
    header(ws, 5, ["ID", "Stakeholder", "Group", "Power (1-5)", "Interest (1-5)", "Engagement approach", "Stance now",
                   "Target stance", "Gap", "Key concern", "Key message", "Channel", "Owner", "Frequency"], "B", height=32)
    for c in "EFJ":
        ws[f"{c}5"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
    for i, s_ in enumerate(D["stakeholders"]):
        rr = 6 + i
        put(ws, f"B{rr}", s_["id"], kind="label", bold=True, border=B_ROW, valign="top")
        put(ws, f"C{rr}", s_["name"], kind="label", bold=True, border=B_ROW, wrap=True, valign="top")
        put(ws, f"D{rr}", s_["group"], kind="muted", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"E{rr}", s_["power"], kind="input", border=B_ROW, align="center", valign="top")
        put(ws, f"F{rr}", s_["interest"], kind="input", border=B_ROW, align="center", valign="top")
        put(ws, f"G{rr}", f'=IF(E{rr}>={P["pw"]},IF(F{rr}>={P["it"]},"Manage closely","Keep satisfied"),IF(F{rr}>={P["it"]},"Keep informed","Monitor"))',
            border=B_ROW, valign="top", bold=True, size=8)
        put(ws, f"H{rr}", s_["stance_now"], kind="input", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"I{rr}", s_["stance_target"], kind="input", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"J{rr}", f'=IF(H{rr}=I{rr},"No","Yes")', border=B_ROW, align="center", valign="top")
        put(ws, f"K{rr}", s_["key_concern"], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"L{rr}", s_["key_message"], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"M{rr}", s_["channel"], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"N{rr}", s_["owner"], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        put(ws, f"O{rr}", s_["frequency"], kind="label", border=B_ROW, wrap=True, valign="top", size=8)
        ws.row_dimensions[rr].height = max(26, 11.6 * max(est_lines(s_["key_message"], 44, 8), est_lines(s_["key_concern"], 28, 8),
                                                            est_lines(s_["channel"], 24, 8), est_lines(s_["name"], 30)) + 3)
    SK_LAST = 6 + len(D["stakeholders"]) - 1
    add_table(ws, "tblStakeholders", f"B5:O{SK_LAST}")
    add_whole_dv(ws, f"E6:F{SK_LAST}", 1, 5)
    cf_text(ws, f"G6:G{SK_LAST}", "Manage closely", C["acc600"])
    cf_text(ws, f"G6:G{SK_LAST}", "Keep satisfied", C["acc100"], fg=C["acc700"])
    cf_text(ws, f"G6:G{SK_LAST}", "Keep informed", C["ink100"], fg=C["ink700"])
    cf_text(ws, f"J6:J{SK_LAST}", "Yes", C["amber"])
    r = SK_LAST + 2
    band(ws, r, "Power-interest grid (count of stakeholder groups)", "B", "O")
    put(ws, f"C{r + 1}", "", kind="label")
    put(ws, f"D{r + 1}", "Interest below 4", kind="muted", bold=True, align="center")
    put(ws, f"G{r + 1}", "Interest 4 or more", kind="muted", bold=True, align="center")
    put(ws, f"C{r + 2}", "Power 4 or more", kind="muted", bold=True, align="right")
    put(ws, f"C{r + 3}", "Power below 4", kind="muted", bold=True, align="right")
    grid = [(r + 2, "D", "Keep satisfied"), (r + 2, "G", "Manage closely"), (r + 3, "D", "Monitor"), (r + 3, "G", "Keep informed")]
    for rr, c, nm in grid:
        put(ws, f"{c}{rr}", f'="{nm}: "&COUNTIF($G$6:$G${SK_LAST},"{nm}")', bold=True, align="center", border=B_BOX,
            fill_hex=C["acc600"] if nm == "Manage closely" else (C["acc100"] if nm == "Keep satisfied" else C["ink100"]),
            color=C["white"] if nm == "Manage closely" else C["ink900"])
        ws.row_dimensions[rr].height = 22
    source_line(ws, f"B{r + 5}", f"Source: pack_data.json {X.v} (stakeholders); engagement approach derived (power and interest "
                "thresholds on Lists). The Communication Pack (D05) carries the messages in full. Illustrative.")
    ws.freeze_panes = "D6"
    print_setup(ws, HDR, title_rows="5:5", area=f"A1:O{r + 5}")

    # =====================================================================================
    # COVER
    # =====================================================================================
    ws = ws_cover
    ws.sheet_view.showGridLines = False
    widths(ws, {"A": 3, "B": 3, "C": 30, "D": 84, "E": 18, "F": 3})
    for rr in range(1, 75):
        for c in "ABCDEF":
            ws[f"{c}{rr}"].fill = fill(C["white"])
    for rr in range(2, 9):
        for c in "BCDE":
            ws[f"{c}{rr}"].fill = fill(C["ink900"])
    put(ws, "C2", f"{X.CODENAME} · EU CYBER RESILIENCE ACT READINESS PROGRAMME", kind="label", bold=True, size=8,
        color=C["acc100"], fill_hex=C["ink900"])
    c = put(ws, "C3", "CRA Obligations Register and Programme Tracker", kind="label", fill_hex=C["ink900"])
    c.font = Font(name=DISPLAY, size=22, bold=True, color=C["white"])
    ws.row_dimensions[3].height = 34
    put(ws, "C4", f"What the CRA requires, who owns it, where {X.client} stands, and how the programme is tracked",
        kind="label", size=10, color=C["ink300"], fill_hex=C["ink900"])
    put(ws, "C6", f"Version {X.ver} · {X.issue}", kind="label", size=9, bold=True, color=C["white"], fill_hex=C["ink900"])
    put(ws, "C7", f"{X.engagement} · Prepared by {X.advisor}", kind="label", size=9,
        color=C["white"], fill_hex=C["ink900"])
    put(ws, "E2", "OBLIGATIONS", kind="label", bold=True, size=8, color=C["white"], fill_hex=C["acc600"], align="center")
    put(ws, "E3", f"=COUNTA('Obligations register'!B{FIRST}:B{LAST})", bold=True, size=16, align="center", color=C["white"],
        fill_hex=C["acc600"])
    put(ws, "E4", "rows in the register", kind="label", size=8, color=C["white"], fill_hex=C["acc600"], align="center")
    meta = [("Version", X.ver), ("Date", X.issue), ("Engagement", f"{X.engagement}"),
            ("Prepared by", f"{X.advisor}"), ("Client data", D["client"]["disclaimer"]),
            ("Regulatory facts", f"Regulation (EU) 2024/2847; verified to {X.facts} against the engagement knowledge base. "
                                 "Obligations are paraphrased; check the OJ text before relying on wording."),
            ("Status date", f"='90-day plan'!E5"),
            ("Model checks", f'=IF(AND({MX_CHECK}="All OK",RACI!$M$16="OK",{RAID_CHECK}="OK",{KPI_CHECK}="OK"),"OK","CHECK")')]
    r = 10
    band(ws, r, "About this workbook", "C", "E")
    r += 1
    for k, v in meta:
        put(ws, f"C{r}", k, kind="muted", bold=True, border=B_ROW)
        put(ws, f"D{r}", v, kind="label", border=B_ROW, wrap=True, fmt=NF_DATE if k == "Status date" else None,
            align="left", bold=(k == "Model checks"))
        ws[f"E{r}"].border = B_ROW
        if k == "Model checks":
            CHECK_ROW = r
        if len(str(v)) > 95:
            ws.row_dimensions[r].height = 26
        r += 1
    cf_checks(ws, f"D{CHECK_ROW}")
    r += 1
    band(ws, r, "Purpose", "C", "E")
    HOLD_NOTE = (f" {Words(len(HOLD))} conformity-assessment rows on notified-body routes are held at Not started until a CRA "
                 f"notified body is designated and contracted (none at checks to {X.nb_check}); clear the Status hold cell for a "
                 "row to release it.") if HOLD else ""
    r += 1
    put(ws, f"C{r}", f"The register lists {REG_ROWS} obligations of the Cyber Resilience Act in plain English, with the evidence "
        f"that proves each one, the accountable role and an illustrative {X.client} status derived from the {X.baseline} "
        f"readiness diagnostic. The tracker sheets run {X.codename}: product readiness heatmap, 90-day plan with Gantt and "
        "milestones, RAID log with risk heatmap, decision log, KPI tracker, RACI and stakeholder register." + HOLD_NOTE,
        kind="label", wrap=True, valign="top")
    ws.merge_cells(f"C{r}:E{r}")
    ws.row_dimensions[r].height = 84 if HOLD else 54
    r += 2
    band(ws, r, "How to use", "C", "E")
    r += 1
    steps = ["Filter the register by Area, Applies to, Owner role or status; each table has its own filter buttons.",
             "Update scores on Diagnostic baseline after each assessment round: the matrix, register status and KPI K01 follow.",
             "Move the status date on 90-day plan (cell E5) weekly; the Gantt marker and 'already apply' counts update.",
             "Log new risks, issues, assumptions, dependencies and decisions in their tables; ratings and the heatmap are formulas.",
             "Enter KPI actuals each month in the blue month columns; keep Model checks at OK."]
    for i, s_ in enumerate(steps):
        put(ws, f"C{r}", f"{i + 1}.  {s_}", kind="label", wrap=True, valign="top")
        ws.merge_cells(f"C{r}:E{r}")
        r += 1
    r += 1
    band(ws, r, "Contents", "C", "E")
    r += 1
    contents = [
        ("Obligations register", f"{REG_ROWS} obligations: source, plain-English duty, who it applies to, effective date, evidence, owner, status"),
        ("Product x obligation matrix", f"{len(FAMS)} families x {len(DOMS)} domains readiness heatmap; reproduces the {DG['portfolio_readiness_index']:.0%} portfolio index"),
        ("90-day plan", f"Tasks {TASK_SPAN} with formula-driven Gantt and status-date marker; milestones {MS_SPAN}"),
        ("RAID log", f"Risks {_span(r_['id'] for r_ in RISKS)} with score and rating formulas and a 5x5 heatmap; issues, assumptions, dependencies"),
        ("Decision log", f"SteerCo #1 decisions {_span(SC_IDS)} and board decisions {_span(BOARD_IDS)}"),
        ("KPI tracker", f"{_span(k_['id'] for k_ in KPIS)} at SteerCo #1, monthly actual columns, readiness and SBOM trajectories"),
        ("RACI", "Decision RACI and decision rights from the corporate guide"),
        ("Stakeholder register", f"{_span(s_['id'] for s_ in D['stakeholders'])} with power, interest, engagement approach, stance, owner and frequency"),
        ("Diagnostic baseline", f"Supporting data: {NQ} questions x {len(FAMS)} families (illustrative scores)"),
        ("Lists", "Supporting data: validation lists and parameters (status bands, rating thresholds)"),
    ]
    for name, desc in contents:
        link_cell(ws, f"C{r}", name, bold=True)
        ws[f"C{r}"].border = B_ROW
        put(ws, f"D{r}", desc, kind="label", border=B_ROW)
        ws[f"E{r}"].border = B_ROW
        r += 1
    r += 1
    band(ws, r, "Colour legend (standard modelling convention) and status colours", "C", "E")
    r += 1
    legend = [
        ("1,234", C["blue"], C["acc100"], "Input: hard-coded value, date or selection, blue font on a teal tint. Change these."),
        ("1,234", C["black"], None, "Formula: calculation, black font. Do not overwrite."),
        ("1,234", C["link"], None, "Link: direct reference to a cell on another sheet, green font."),
        ("Text", C["ink900"], None, "Register text and labels, ink. Edit text entries directly."),
        ("Not started", C["white"], C["heat0"], "Register status: level 0 (average below 1), or held: Module B/H rows while no notified body exists"),
        ("Initial", C["ink900"], C["heat1"], "Register status: level 1 (diagnostic average 1 to below 2)"),
        ("Defined", C["ink900"], C["heat2"], "Register status: level 2 (2 to below 3)"),
        ("Implemented", C["ink900"], C["heat3"], "Register status: level 3 (3 to below 4)"),
        ("Assured", C["white"], C["heat4"], "Register status: level 4"),
        ("Not assessed", C["white"], C["grey"], "No diagnostic question covers the obligation"),
        ("0  1  2  3  4", C["ink900"], C["heat2"], "Heatmap: level rounded down; red 0, coral 1, yellow 2, sage 3, teal 4; the number always prints"),
    ]
    for sample, fg, bg, desc in legend:
        cell = ws[f"C{r}"]
        cell.value = sample
        cell.font = font(fg, bold=bg is not None and bg != C["acc100"])
        if bg:
            cell.fill = fill(bg)
        cell.alignment = Alignment(horizontal="center", vertical="center")
        cell.border = B_BOX
        put(ws, f"D{r}", desc, kind="label")
        r += 1
    r += 1
    put(ws, f"C{r}", f"Illustrative engagement — fictional client data. Not legal advice. Facts as at {X.facts}.",
        kind="muted", size=8, italic=True)
    ws.merge_cells(f"C{r}:E{r}")
    print_setup(ws, HDR, area=f"A1:F{r}", landscape=False)
    ws.page_setup.fitToHeight = 1

    for w_, col in [(ws_cover, C["ink900"]), (ws_reg, C["acc600"]), (ws_mx, C["acc600"]), (ws_plan, C["ink700"]),
                    (ws_raid, C["ink700"]), (ws_dec, C["ink700"]), (ws_kpi, C["ink700"]), (ws_raci, C["ink700"]),
                    (ws_stk, C["ink700"]), (ws_db, C["ink500"]), (ws_ls, C["ink500"])]:
        w_.sheet_properties.tabColor = col
    wb.active = 0
    wb.properties.title = f"{X.codename} - CRA Obligations Register and Programme Tracker"
    wb.properties.subject = f"EU Cyber Resilience Act Readiness Programme · {X.engagement}"
    wb.properties.creator = f"{X.advisor}"
    wb.properties.lastModifiedBy = f"{X.advisor}"
    wb.properties.keywords = f"{X.codename}; CRA; obligations register; programme tracker; {X.v}"
    wb.save(str(OUT))
