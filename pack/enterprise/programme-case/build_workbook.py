#!/usr/bin/env python3
"""Build 'Aldermoor CRA Integrated Programme Case.xlsx' (module E7) with live formulas.

Run model.py first. The workbook re-implements the cost model and the critical path as Excel
formulas driven by one scenario switch (1 Low, 2 Base, 3 High), per-input overrides and five
lever switches. Monte Carlo, tornado and notified-body queue results are pasted as values from
model.py outputs and labelled as such. A check cell compares the live total with model.py.
"""
from __future__ import annotations

import csv
import json
import re
from pathlib import Path

from openpyxl import Workbook
from openpyxl.chart import BarChart, LineChart, Reference
from openpyxl.comments import Comment
from openpyxl.styles import Alignment, Border, Font, PatternFill, Side
from openpyxl.utils import get_column_letter as L
from openpyxl.workbook.defined_name import DefinedName

import model as mdl

HERE = Path(__file__).resolve().parent
OUT = HERE / "outputs"
XLSX = HERE / "Aldermoor CRA Integrated Programme Case.xlsx"

F = "Arial"
BLUE = Font(name=F, size=10, color="0000FF")
BLACK = Font(name=F, size=10)
GREEN = Font(name=F, size=10, color="008000")
BOLD = Font(name=F, size=10, bold=True)
TITLE = Font(name=F, size=14, bold=True)
HDR = Font(name=F, size=10, bold=True, color="FFFFFF")
HFILL = PatternFill("solid", fgColor="1F3864")
YELLOW = PatternFill("solid", fgColor="FFFF00")
GREY = PatternFill("solid", fgColor="F2F2F2")
THIN = Border(bottom=Side(style="thin", color="BFBFBF"))
EURM = '#,##0.00;(#,##0.00);"-"'
EUR = '#,##0;(#,##0);"-"'
NUM1 = '#,##0.0;(#,##0.0);"-"'
NUM2 = '#,##0.00;(#,##0.00);"-"'
PCT = '0%;(0%);"-"'
DATE = "dd mmm yyyy"


def header(ws, row, cols, widths=None):
    for i, c in enumerate(cols, 1):
        cell = ws.cell(row=row, column=i, value=c)
        cell.font, cell.fill = HDR, HFILL
        cell.alignment = Alignment(wrap_text=True, vertical="center")
    if widths:
        for i, w in enumerate(widths, 1):
            ws.column_dimensions[L(i)].width = w


def name(wb, nm, sheet, ref):
    wb.defined_names[nm] = DefinedName(nm, attr_text=f"'{sheet}'!{ref}")


def xl(tpl: str) -> str:
    return "=" + tpl


def main() -> None:
    M = mdl.Model()
    summ = json.loads((OUT / "summary.json").read_text())
    wb = Workbook()

    # ------------------------------------------------------------------ Read me
    ws = wb.active
    ws.title = "Read me"
    ws.column_dimensions["A"].width = 120
    rows = [
        ("Aldermoor CRA Integrated Programme Case (module E7, v2)", TITLE),
        ("Fictional client. All Aldermoor figures are estimates. Facts as at 1 Nov 2026; notified-body market evidence to 12 Sep 2026 (register) and vendor pages opened 1 Nov 2026.", BLACK),
        ("", BLACK),
        ("How to use", BOLD),
        ("1. Assumptions!C3 is the scenario switch: 1 = Low (cheap and fast), 2 = Base, 3 = High (costly and slow). For schedule inputs Low is the favourable end.", BLACK),
        ("2. Assumptions column G overrides the scenario for one input (enter 1, 2 or 3). Leave blank to follow C3.", BLACK),
        ("3. Assumptions!C6:C10 are the decision levers L1-L5 (0 = off, 1 = on). They change the critical path and the budget (L1 reservation cost, L3 onboarding, L4 fee saving). Set all to 1 for the recommended plan.", BLACK),
        ("4. Budget, Headcount, Critical path, Remediation and the weekly revenue on Cost of delay recalculate live. The Budget check cell compares the live total with model.py: against the recommended plan when all levers are 1, the plan as written when all are 0.", BLACK),
        ("5. Readiness, Scenarios, Correlated MC, Cost of delay (expected values), Lever value, Sensitivity, NB schedule and Reconciliation are values pasted from model.py outputs; rerun model.py and this builder to refresh them.", BLACK),
        ("6. Market evidence lists the public notified-body sources behind scenarios B and C; vendor statements are labelled as such.", BLACK),
        ("", BLACK),
        ("Colour code", BOLD),
        ("Blue text: hard-coded inputs. Black text: formulas. Green text: links to another sheet. Yellow fill: the switches a reader should change.", BLACK),
        ("", BLACK),
        ("Sources", BOLD),
        ("Every input row on Assumptions names its source: a module output file under pack/enterprise/, a KB section, a web page, or 'assumption'.", BLACK),
        ("Module files read: art14-operations/volume_model_output.csv; portfolio-classification/nb_demand_summary.json, nb_demand.csv, classification_summary.json, classification.csv, portfolio.yaml;", BLACK),
        ("evidence-as-code/aldermoor-additions.json and paper.md; open-source-strategy/projects.yaml; global-control-set/controls.json; oj-verification/claims.csv. Remediation calibration: pack/clients/example-group/client.yaml cost_model.", BLACK),
        ("", BLACK),
        ("Units: EUR unless stated; USD converted at 0.919 (BRIEF.md: USD 310bn = EUR 285bn). Days are calendar days from 2 Nov 2026. Q4 2026 covers Nov-Dec.", BLACK),
    ]
    for i, (t, f) in enumerate(rows, 1):
        c = ws.cell(row=i, column=1, value=t)
        c.font = f

    # ------------------------------------------------------------------ Assumptions
    wa = wb.create_sheet("Assumptions")
    wa["A1"] = "Assumptions register"
    wa["A1"].font = TITLE
    wa["A3"] = "Scenario switch"
    wa["B3"] = "1 = Low, 2 = Base, 3 = High"
    wa["C3"] = 2
    wa["C3"].font, wa["C3"].fill = BLUE, YELLOW
    name(wb, "scenario", "Assumptions", "$C$3")
    wa["A5"] = "Decision levers (0 = off, 1 = on)"
    wa["A5"].font = BOLD
    levers = [i for i in M.items if i["section"] == "lever"]
    for k, it in enumerate(levers):
        r = 6 + k
        wa.cell(row=r, column=1, value=it["key"]).font = BLACK
        wa.cell(row=r, column=2, value=it["desc"]).font = BLACK
        c = wa.cell(row=r, column=3, value=int(it["base"]))
        c.font, c.fill = BLUE, YELLOW
        name(wb, it["key"], "Assumptions", f"$C${r}")
    r0 = 6 + len(levers) + 2
    header(wa, r0, ["Key", "Section", "Description", "Low", "Base", "High", "Override (1/2/3)", "Selected", "Unit", "Label", "Source"],
           [26, 9, 60, 12, 12, 12, 10, 14, 18, 22, 70])
    wa.freeze_panes = wa.cell(row=r0 + 1, column=1)
    row = r0 + 1
    for it in M.items:
        if it["section"] not in ("global", "cost", "nb", "cod"):
            continue
        wa.cell(row=row, column=1, value=it["key"]).font = BLACK
        wa.cell(row=row, column=2, value=it["section"]).font = BLACK
        wa.cell(row=row, column=3, value=it["desc"]).font = BLACK
        for j, s in enumerate(mdl.SCEN):
            c = wa.cell(row=row, column=4 + j, value=float(it[s]))
            c.font = BLUE
            c.number_format = "#,##0.00" if abs(float(it[s])) < 100 else "#,##0"
        wa.cell(row=row, column=7).font = BLUE
        c = wa.cell(row=row, column=8, value=f'=CHOOSE(IF(G{row}="",scenario,G{row}),D{row},E{row},F{row})')
        c.font = BLACK
        c.number_format = "#,##0.00" if abs(float(it["base"])) < 100 else "#,##0"
        wa.cell(row=row, column=9, value=it.get("unit", "")).font = BLACK
        wa.cell(row=row, column=10, value=it.get("label", "")).font = BLACK
        src = it.get("source", "") + (" [value read from module file by model.py]" if it.get("resolved_from_file") else "")
        wa.cell(row=row, column=11, value=src).font = BLACK
        name(wb, it["key"], "Assumptions", f"$H${row}")
        row += 1

    # ------------------------------------------------------------------ Derived
    wd = wb.create_sheet("Derived")
    wd["A1"] = "Derived quantities (formulas over Assumptions; same templates as model.py)"
    wd["A1"].font = TITLE
    header(wd, 3, ["Key", "Description", "Value", "Formula template"], [26, 60, 16, 80])
    for k, (key, desc, tpl) in enumerate(mdl.DERIVED):
        r = 4 + k
        wd.cell(row=r, column=1, value=key).font = BLACK
        wd.cell(row=r, column=2, value=desc).font = BLACK
        c = wd.cell(row=r, column=3, value=xl(tpl))
        c.font = BLACK
        c.number_format = "#,##0.00"
        wd.cell(row=r, column=4, value=tpl).font = BLACK
        name(wb, key, "Derived", f"$C${r}")

    # ------------------------------------------------------------------ Remediation and support periods (live)
    wm = wb.create_sheet("Remediation")
    wm["A1"] = "Product remediation and support-period extension by family (live formulas over Assumptions)"
    wm["A1"].font = TITLE
    wm["A2"] = ("Remediation FTE-years = base-pack rate for the class x E3 complexity x MAX(1, types)^rem_type_exp x rem_scale x severity. "
                "Support extension: launch-anchored policies need floor + sales life years; last-sold policies need the floor. "
                "FTE a year = extra years x model cohorts a year x sp_fte_per_model_year x complexity.")
    header(wm, 4, ["ID", "Family", "Business line", "Class", "Rate class", "Severity key", "E3 complexity", "Types",
                   "Remediation FTE-years", "Remediation EUR m", "Support policy (years)", "Anchor", "Cohorts a year",
                   "Extra years needed", "Support FTE a year", "Support EUR m a year", "Policy source"],
           [6, 44, 20, 12, 10, 12, 10, 8, 12, 12, 10, 12, 10, 10, 10, 12, 70])
    rate_nm = {"default": "rem_rate_default", "class1": "rem_rate_class1", "class2": "rem_rate_class2"}
    r = 5
    for f in M.families:
        vals = [f["family_id"], f["name"], f["business_line"], f["class_bucket"], f["rem_rate_class"], f["severity_key"]]
        for j, v_ in enumerate(vals):
            wm.cell(row=r, column=1 + j, value=v_).font = BLACK
        wm.cell(row=r, column=7, value=f["complexity"]).font = BLUE
        wm.cell(row=r, column=8, value=f["initial_types"]).font = BLUE
        if f["rem_scope"] == "yes":
            fx = f"={rate_nm[f['rem_rate_class']]}*G{r}*MAX(1,H{r})^rem_type_exp*rem_scale*{f['severity_key']}"
        else:
            fx = 0
        c = wm.cell(row=r, column=9, value=fx)
        c.number_format = NUM2
        c = wm.cell(row=r, column=10, value=f"=I{r}*fte_cost_eur/1000000")
        c.number_format = EURM
        wm.cell(row=r, column=11, value=f["sp_policy_years"]).font = BLUE
        wm.cell(row=r, column=12, value=f["sp_anchor"]).font = BLUE
        wm.cell(row=r, column=13, value=f["sp_cohorts_per_year"]).font = BLUE
        c = wm.cell(row=r, column=14, value=f'=IF(L{r}="launch",MAX(0,sp_floor_years+sp_sales_life_years-K{r}),IF(L{r}="last_sold",MAX(0,sp_floor_years-K{r}),0))')
        c.number_format = NUM2
        c = wm.cell(row=r, column=15, value=f"=N{r}*M{r}*sp_fte_per_model_year*G{r}")
        c.number_format = NUM2
        c = wm.cell(row=r, column=16, value=f"=O{r}*fte_cost_eur/1000000")
        c.number_format = EURM
        wm.cell(row=r, column=17, value=f["sp_policy_source"]).font = BLACK
        r += 1
    wm.cell(row=r, column=1, value="Total").font = BOLD
    for col in (9, 10, 15, 16):
        c = wm.cell(row=r, column=col, value=f"=SUM({L(col)}5:{L(col)}{r - 1})")
        c.font, c.number_format = BOLD, (EURM if col in (10, 16) else NUM2)
    name(wb, "rem_fteyrs", "Remediation", f"$I${r}")
    name(wb, "sp_fte_yr", "Remediation", f"$O${r}")
    wm.freeze_panes = "C5"

    # ------------------------------------------------------------------ Lines
    wl = wb.create_sheet("Lines")
    wl["A1"] = "Cost lines by quarter (FTE and EUR)"
    wl["A1"].font = TITLE
    Q = mdl.QUARTERS
    nq = len(Q)
    cols = ["ID", "Workstream", "Function", "Category", "Type", "Value", "Description"] + [f"Profile {q}" for q in Q] + \
           [f"FTE {q}" for q in Q] + [f"EUR {q}" for q in Q] + ["One-off EUR", "Run Q4 2026-Q4 2027 EUR", "Run 2028 EUR", "Total EUR"]
    header(wl, 3, cols, [6, 34, 30, 9, 8, 14, 44] + [8] * nq + [8] * nq + [12] * nq + [14, 14, 14, 14])
    wl.freeze_panes = "H4"
    pc0, fc0, cc0 = 8, 8 + nq, 8 + 2 * nq
    tc0 = 8 + 3 * nq
    first = 4
    for k, ln in enumerate(M.lines):
        r = first + k
        for j, v in enumerate([ln["key"], ln["workstream"], ln["function"], ln["category"], ln["type"]]):
            wl.cell(row=r, column=1 + j, value=v).font = BLACK
        c = wl.cell(row=r, column=6, value=f"={ln['value']}")
        c.font, c.number_format = GREEN, "#,##0.00"
        wl.cell(row=r, column=7, value=ln["desc"]).font = BLACK
        prange = f"${L(pc0)}{r}:${L(pc0 + nq - 1)}{r}"
        for q in range(nq):
            c = wl.cell(row=r, column=pc0 + q, value=ln["prof"][q])
            c.font = BLUE
            p = f"{L(pc0 + q)}{r}"
            c = wl.cell(row=r, column=fc0 + q, value=f'=IF($E{r}="fte",$F{r}*{p},IF($E{r}="fteyrs",$F{r}*{p}/(SUM({prange})/4),0))')
            c.font, c.number_format = BLACK, NUM1
            fcell = f"{L(fc0 + q)}{r}"
            c = wl.cell(row=r, column=cc0 + q,
                        value=f'=IF(OR($E{r}="fte",$E{r}="fteyrs"),{fcell}*fte_cost_eur/4,IF($E{r}="eur_yr",$F{r}*{p}/4,$F{r}*{p}/SUM({prange})))')
            c.font, c.number_format = BLACK, EUR
        crange = f"{L(cc0)}{r}:{L(cc0 + nq - 1)}{r}"
        c27 = f"{L(cc0)}{r}:{L(cc0 + 4)}{r}"
        c28 = f"{L(cc0 + 5)}{r}:{L(cc0 + nq - 1)}{r}"
        for j, f_ in enumerate([f'=IF($D{r}="one-off",SUM({crange}),0)', f'=IF($D{r}="run",SUM({c27}),0)',
                                f'=IF($D{r}="run",SUM({c28}),0)', f"=SUM({crange})"]):
            c = wl.cell(row=r, column=tc0 + j, value=f_)
            c.font, c.number_format = BLACK, EUR
    last = first + len(M.lines) - 1
    tr = last + 1
    wl.cell(row=tr, column=1, value="Total").font = BOLD
    for col in range(fc0, tc0 + 4):
        c = wl.cell(row=tr, column=col, value=f"=SUM({L(col)}{first}:{L(col)}{last})")
        c.font, c.number_format = BOLD, (NUM1 if col < cc0 else EUR)
    LR = f"${first}:${last}"  # noqa

    def rng(col):
        return f"Lines!${L(col)}${first}:${L(col)}${last}"

    # ------------------------------------------------------------------ Budget
    wbud = wb.create_sheet("Budget")
    wbud["A1"] = "Budget by workstream, live (EUR m; selected scenario)"
    wbud["A1"].font = TITLE
    wbud["A2"] = "Selected scenario:"
    wbud["B2"] = '=CHOOSE(scenario,"Low","Base","High")'
    wbud["B2"].font = GREEN
    header(wbud, 4, ["Workstream", "One-off", "Run Q4 2026-Q4 2027", "Run 2028 (annual)", "Total Q4 2026-Q4 2028"], [46, 16, 20, 18, 22])
    wsn = sorted({ln["workstream"] for ln in M.lines}, key=lambda x: int(x.split()[0]))
    for k, w in enumerate(wsn):
        r = 5 + k
        wbud.cell(row=r, column=1, value=w).font = BLACK
        for j in range(4):
            c = wbud.cell(row=r, column=2 + j, value=f'=SUMIFS({rng(tc0 + j)},{rng(2)},$A{r})/1000000')
            c.font, c.number_format = GREEN, EURM
    rc = 5 + len(wsn)
    wbud.cell(row=rc, column=1, value="11 Contingency").font = BLACK
    wbud.cell(row=rc, column=2, value=f"=contingency_rate*SUM(B5:B{rc - 1})").number_format = EURM
    wbud.cell(row=rc, column=3, value=f"=contingency_run_rate*SUM(C5:C{rc - 1})").number_format = EURM
    wbud.cell(row=rc, column=4, value=f"=contingency_run_rate*SUM(D5:D{rc - 1})").number_format = EURM
    wbud.cell(row=rc, column=5, value=f"=B{rc}+C{rc}+D{rc}").number_format = EURM
    rt = rc + 1
    wbud.cell(row=rt, column=1, value="Total").font = BOLD
    for j in range(4):
        c = wbud.cell(row=rt, column=2 + j, value=f"=SUM({L(2 + j)}5:{L(2 + j)}{rc})")
        c.font, c.number_format = BOLD, EURM
    # static model.py results and check
    rs = rt + 3
    wbud.cell(row=rs - 1, column=1, value="model.py results (values) for comparison, EUR m").font = BOLD
    header(wbud, rs, ["Plan and scenario", "One-off", "Run Q4 2026-Q4 2027", "Run 2028 (annual)", "Total Q4 2026-Q4 2028"])
    for k, (lab, key) in enumerate((("Recommended plan, levers L1-L5", "budget_eur_m"), ("Plan as written, levers off", "budget_as_written_eur_m"))):
        for kk, s_ in enumerate(mdl.SCEN):
            r = rs + 1 + 3 * k + kk
            wbud.cell(row=r, column=1, value=f"{lab}: {s_}").font = BLACK
            for j, m in enumerate(("one_off", "run_2027", "run_2028", "total")):
                c = wbud.cell(row=r, column=2 + j, value=summ[key][s_][m])
                c.font, c.number_format = BLUE, EURM
    chk = rs + 8
    lev_sum = "+".join(mdl.LEVERS)
    wbud.cell(row=chk, column=1, value="Check: live total less model.py total for the selected scenario (0 when no overrides; levers all 1 or all 0)").font = BOLD
    c = wbud.cell(row=chk, column=2, value=f'=IF({lev_sum}=5,ROUND(E{rt}-INDEX(E{rs + 1}:E{rs + 3},scenario),2),IF({lev_sum}=0,ROUND(E{rt}-INDEX(E{rs + 4}:E{rs + 6},scenario),2),"mixed levers"))')
    c.font, c.number_format = BOLD, EURM
    wbud.cell(row=chk + 2, column=1, value="Joint Monte Carlo, recommended plan (model.py, 5,000 runs; EUR m). Funding level = correlated P90").font = BOLD
    header(wbud, chk + 3, ["Measure and sampling", "P10", "P50", "P80", "P90", "Mean"])
    rr = chk + 4
    for m, lab in (("one_off", "One-off"), ("run_2028", "Run 2028"), ("total", "Total Q4 2026-Q4 2028")):
        for mode, mlab in (("independent", "independent inputs"), ("market_only", "correlated, three market factors"), ("correlated", "correlated, four factors")):
            wbud.cell(row=rr, column=1, value=f"{lab}: {mlab}").font = BLACK
            st = summ["joint_mc_cost_eur_m"][f"recommended|{mode}|{m}"]
            for j, p in enumerate(("p10", "p50", "p80", "p90", "mean")):
                c = wbud.cell(row=rr, column=2 + j, value=st[p])
                c.font, c.number_format = BLUE, EURM
            rr += 1
    rq = rr + 1
    wbud.cell(row=rq, column=1, value="Spend by quarter, live (EUR m, before contingency)").font = BOLD
    for q in range(nq):
        wbud.cell(row=rq + 1, column=2 + q, value=Q[q]).font = BOLD
        c = wbud.cell(row=rq + 2, column=2 + q, value=f"=Lines!{L(cc0 + q)}{tr}/1000000")
        c.font, c.number_format = GREEN, EURM
    wbud.cell(row=rq + 2, column=1, value="Spend").font = BLACK
    memo = rq + 4
    wbud.cell(row=memo, column=1, value="Memo, not in budget: staff time spent in training (EUR m)").font = BLACK
    c = wbud.cell(row=memo, column=2, value="=train_staff_cost_memo/1000000")
    c.font, c.number_format = GREEN, EURM
    ch = BarChart()
    ch.type = "col"
    ch.grouping = "stacked"
    ch.overlap = 100
    ch.title = "One-off and run cost by workstream (selected scenario, EUR m)"
    ch.add_data(Reference(wbud, min_col=2, max_col=4, min_row=4, max_row=rc), titles_from_data=True)
    ch.set_categories(Reference(wbud, min_col=1, min_row=5, max_row=rc))
    ch.height, ch.width = 9, 22
    wbud.add_chart(ch, "G4")

    # ------------------------------------------------------------------ Headcount
    wh = wb.create_sheet("Headcount")
    wh["A1"] = "Headcount by function and quarter, live (FTE; selected scenario)"
    wh["A1"].font = TITLE
    header(wh, 3, ["Function"] + Q + ["Peak"], [36] + [10] * (nq + 1))
    funcs = sorted({ln["function"] for ln in M.lines if ln["function"] != "none"})
    for k, f_ in enumerate(funcs):
        r = 4 + k
        wh.cell(row=r, column=1, value=f_).font = BLACK
        for q in range(nq):
            c = wh.cell(row=r, column=2 + q, value=f"=SUMIFS({rng(fc0 + q)},{rng(3)},$A{r})")
            c.font, c.number_format = GREEN, NUM1
        c = wh.cell(row=r, column=2 + nq, value=f"=MAX(B{r}:{L(1 + nq)}{r})")
        c.number_format = NUM1
    ht = 4 + len(funcs)
    wh.cell(row=ht, column=1, value="Total").font = BOLD
    for q in range(nq + 1):
        c = wh.cell(row=ht, column=2 + q, value=f"=SUM({L(2 + q)}4:{L(2 + q)}{ht - 1})" if q < nq else f"=MAX(B{ht}:{L(1 + nq)}{ht})")
        c.font, c.number_format = BOLD, NUM1
    wh.cell(row=ht + 1, column=1, value="Peak quarter").font = BOLD
    wh.cell(row=ht + 1, column=2, value=f"=INDEX(B3:{L(1 + nq)}3,MATCH({L(2 + nq)}{ht},B{ht}:{L(1 + nq)}{ht},0))")
    lc = LineChart()
    lc.title = "Total headcount (FTE)"
    lc.add_data(Reference(wh, min_col=2, max_col=1 + nq, min_row=ht), from_rows=True, titles_from_data=False)
    lc.set_categories(Reference(wh, min_col=2, max_col=1 + nq, min_row=3))
    lc.height, lc.width = 8, 18
    wh.add_chart(lc, f"A{ht + 4}")

    # ------------------------------------------------------------------ Critical path
    wc = wb.create_sheet("Critical path")
    wc["A1"] = "Critical path (CPM, live; durations in calendar days)"
    wc["A1"].font = TITLE
    wc["A2"] = "Start"
    wc["B2"] = mdl.START
    wc["B2"].number_format, wc["B2"].font = DATE, BLUE
    name(wb, "start_date", "Critical path", "$B$2")
    wc["C2"] = "Deadline"
    wc["D2"] = mdl.DEADLINE
    wc["D2"].number_format, wc["D2"].font = DATE, BLUE
    name(wb, "deadline_date", "Critical path", "$D$2")
    wc["E2"] = "Project end"
    cols = ["ID", "Activity", "Module", "Predecessors", "Low", "Base", "High", "Pre-contract low", "Pre-contract base",
            "Pre-contract high", "Duration", "ES", "EF", "LS", "LF", "Float", "Critical", "Start", "Finish", "Target", "Slack to target", "Source"]
    header(wc, 4, cols, [7, 58, 7, 22, 7, 7, 7, 9, 9, 9, 10, 8, 8, 8, 8, 8, 8, 12, 12, 12, 9, 60])
    wc.freeze_panes = "C5"
    rowof = {n: 5 + k for k, n in enumerate(M.order)}
    succ = {n: [] for n in M.order}
    for n in M.order:
        a = M.act_by_id[n]
        for p in a["pred_list"]:
            succ[p].append((None, n))
        for cond, p in a["cond_list"]:
            succ[p].append((cond, n))
    endr = rowof["END"]
    for n in M.order:
        a, r = M.act_by_id[n], rowof[n]
        wc.cell(row=r, column=1, value=n).font = BLACK
        wc.cell(row=r, column=2, value=a["desc"]).font = BLACK
        wc.cell(row=r, column=3, value=a["module"]).font = BLACK
        pt = ";".join(a["pred_list"] + [f"[{c}] {p}" for c, p in a["cond_list"]])
        wc.cell(row=r, column=4, value=pt).font = BLACK
        if a.get("dur_formula"):
            wc.cell(row=r, column=11, value=xl(a["dur_formula"])).font = BLACK
        else:
            for j, s in enumerate(mdl.SCEN):
                wc.cell(row=r, column=5 + j, value=float(a[s])).font = BLUE
            base = f"CHOOSE(scenario,E{r},F{r},G{r})"
            if "pc_base" in a:
                for j, s in enumerate(mdl.SCEN):
                    wc.cell(row=r, column=8 + j, value=float(a["pc_" + s])).font = BLUE
                wc.cell(row=r, column=11, value=f"=IF(lever_precontract,CHOOSE(scenario,H{r},I{r},J{r}),{base})").font = BLACK
            else:
                wc.cell(row=r, column=11, value="=" + base).font = BLACK
        terms = [f"M{rowof[p]}" for p in a["pred_list"]] + [f"IF({c},M{rowof[p]},0)" for c, p in a["cond_list"]]
        wc.cell(row=r, column=12, value="=MAX(0," + ",".join(terms) + ")" if terms else 0).font = BLACK
        wc.cell(row=r, column=13, value=f"=L{r}+K{r}").font = BLACK
        if n in M.anc:
            st = [f"N{rowof[s]}" if c is None else f"IF({c},N{rowof[s]},1E9)" for c, s in succ[n] if s in M.anc]
            wc.cell(row=r, column=15, value=f"=MIN($M${endr}," + ",".join(st) + ")" if st else f"=$M${endr}").font = BLACK
            wc.cell(row=r, column=14, value=f"=O{r}-K{r}").font = BLACK
            wc.cell(row=r, column=16, value=f"=N{r}-L{r}").font = BLACK
            wc.cell(row=r, column=17, value=f'=IF(P{r}<0.5,"yes","no")').font = BLACK
        else:
            wc.cell(row=r, column=16, value="not CRA-gating").font = BLACK
        wc.cell(row=r, column=18, value=f"=start_date+ROUNDUP(L{r},0)").number_format = DATE
        wc.cell(row=r, column=19, value=f"=start_date+ROUNDUP(M{r},0)").number_format = DATE
        if a.get("target"):
            c = wc.cell(row=r, column=20, value=f"=start_date+{int(a['target'])}")
            c.number_format = DATE
            wc.cell(row=r, column=21, value=f"={int(a['target'])}-M{r}").number_format = NUM1
        wc.cell(row=r, column=22, value=a.get("source", "")).font = BLACK
        for col in range(11, 17):
            wc.cell(row=r, column=col).number_format = NUM1
    wc["F2"] = f"=S{endr}"
    wc["F2"].number_format = DATE
    wc["G2"] = "Slack to 11 Dec 2027 (days)"
    wc["H2"] = f"=D2-F2"

    # ------------------------------------------------------------------ Readiness (MC values)
    wr = wb.create_sheet("Readiness")
    wr["A1"] = "Probability of readiness by target date: scenario A (stated capacity assumptions), inputs independent (Monte Carlo, 5,000 runs, PERT; values from model.py). CONDITIONAL on the stated capacity assumptions; see Scenarios"
    wr["A1"].font = TITLE
    prob = list(csv.DictReader((OUT / "readiness_probability.csv").open()))
    sets = []
    for p in prob:
        if p["lever_set"] not in [s for s, _ in sets]:
            sets.append((p["lever_set"], p["lever_description"]))
    header(wr, 3, ["Product line", "Target"] + [s for s, _ in sets], [60, 12] + [9] * len(sets))
    nodes = []
    for p in prob:
        if p["node"] not in nodes:
            nodes.append(p["node"])
    for k, n in enumerate(nodes):
        r = 4 + k
        pr = [p for p in prob if p["node"] == n]
        wr.cell(row=r, column=1, value=pr[0]["product_line"]).font = BLACK
        wr.cell(row=r, column=2, value=pr[0]["target_date"]).font = BLACK
        for j, (sid, _) in enumerate(sets):
            v = next(float(p["p_ready_by_target"]) for p in pr if p["lever_set"] == sid)
            c = wr.cell(row=r, column=3 + j, value=v)
            c.font, c.number_format = BLUE, PCT
    r = 6 + len(nodes)
    wr.cell(row=r, column=1, value="Lever sets").font = BOLD
    for k, (sid, d) in enumerate(sets):
        wr.cell(row=r + 1 + k, column=1, value=f"{sid}: {d}").font = BLACK
    r2 = r + len(sets) + 3
    wr.cell(row=r2, column=1, value="P50 and P80 ready dates").font = BOLD
    header(wr, r2 + 1, ["Product line", "S0 P50", "S0 P80", "S7 P50", "S7 P80"])
    for k, n in enumerate(nodes):
        rr = r2 + 2 + k
        pr = {p["lever_set"]: p for p in prob if p["node"] == n}
        wr.cell(row=rr, column=1, value=pr["S0"]["product_line"]).font = BLACK
        for j, (sid, f_) in enumerate((("S0", "p50_date"), ("S0", "p80_date"), ("S7", "p50_date"), ("S7", "p80_date"))):
            wr.cell(row=rr, column=2 + j, value=pr[sid][f_]).font = BLUE

    # ------------------------------------------------------------------ Sensitivity
    wsn_ = wb.create_sheet("Sensitivity")
    wsn_["A1"] = "Tornado: each driver from low to high, others at base (values from model.py)"
    wsn_["A1"].font = TITLE
    sens = list(csv.DictReader((OUT / "sensitivity.csv").open()))
    cols = ["driver", "kind", "total_cost_low_eur_m", "total_cost_high_eur_m", "cost_swing_eur_m", "end_date_low", "end_date_high",
            "end_swing_days", "lumen_swing_days", "default_swing_days", "rank_cost", "rank_schedule", "inputs"]
    header(wsn_, 3, cols, [52, 9, 12, 12, 12, 12, 12, 10, 10, 10, 8, 8, 80])
    for k, s in enumerate(sens):
        for j, c_ in enumerate(cols):
            v = s[c_]
            try:
                v = float(v) if c_ not in ("driver", "kind", "inputs", "end_date_low", "end_date_high") and v != "" else v
            except ValueError:
                pass
            c = wsn_.cell(row=4 + k, column=1 + j, value=v)
            c.font = BLUE if j > 1 else BLACK

    # ------------------------------------------------------------------ NB schedule
    wn = wb.create_sheet("NB schedule")
    wn["A1"] = "Notified-body body-days by quarter: demand needed for 11 Dec 2027 against capacity (values from model.py; totals live)"
    wn["A1"].font = TITLE
    nbs = list(csv.DictReader((OUT / "nb_schedule.csv").open()))
    cols = list(nbs[0].keys())
    header(wn, 3, cols, [10, 11, 11] + [12] * (len(cols) - 3))
    for k, rrow in enumerate(nbs):
        for j, c_ in enumerate(cols):
            v = rrow[c_]
            c = wn.cell(row=4 + k, column=1 + j, value=float(v) if j >= 3 else v)
            c.font = BLUE
            if j >= 3:
                c.number_format = PCT if c_.startswith("aldermoor_share") else NUM1
    tr_ = 4 + len(nbs)
    wn.cell(row=tr_, column=1, value="Total").font = BOLD
    for j in range(3, len(cols)):
        if cols[j].startswith(("demand", "capacity", "processed")):
            c = wn.cell(row=tr_, column=1 + j, value=f"=SUM({L(1 + j)}4:{L(1 + j)}{tr_ - 1})")
            c.font, c.number_format = BOLD, NUM1
    wn.cell(row=tr_ + 2, column=1, value="Capacity scenarios: base = two bodies from contract dates in the base plan, 5 assessors each; constrained = high-case designation and contracting, 3 assessors; levers = L1-L3 (three bodies, 8 reserved assessors). Demand is spread from internal readiness (30 Jun 2027) to 11 Dec 2027, then steady state. Queue aggregated across bodies.").font = BLACK
    bc = BarChart()
    bc.title = "Body-days needed vs Aldermoor capacity (base)"
    bc.add_data(Reference(wn, min_col=5, max_col=5, min_row=3, max_row=tr_ - 1), titles_from_data=True)
    bc.add_data(Reference(wn, min_col=7, max_col=7, min_row=3, max_row=tr_ - 1), titles_from_data=True)
    bc.add_data(Reference(wn, min_col=13, max_col=13, min_row=3, max_row=tr_ - 1), titles_from_data=True)
    bc.set_categories(Reference(wn, min_col=1, min_row=4, max_row=tr_ - 1))
    bc.height, bc.width = 8, 20
    wn.add_chart(bc, f"A{tr_ + 4}")

    # ------------------------------------------------------------------ Scenarios (values)
    wsc = wb.create_sheet("Scenarios")
    wsc["A1"] = "P(ready by target) by notified-body market scenario, sampling mode and lever set (values from model.py)"
    wsc["A1"].font = TITLE
    for k, (sc, d_) in enumerate(mdl.MARKET_SCEN.items()):
        wsc.cell(row=2 + k, column=1, value=f"{sc}: {d_}").font = BLACK
    rsc = list(csv.DictReader((OUT / "readiness_scenarios.csv").open()))
    nodes_s = ["R_LUM", "R_PLT", "R_DEV", "R_CLD", "R_DEF", "END"]
    header(wsc, 6, ["Scenario", "Mode", "Lever set", "Lumen", "Platforms", "Devices", "Cloud and apps", "Default", "All lines", "All lines P50 date", "All lines P80 date"],
           [9, 12, 10, 9, 9, 9, 9, 9, 9, 14, 14])
    keyd = {(x["scenario"], x["mode"], x["lever_set"], x["node"]): x for x in rsc}
    combos = sorted({(x["scenario"], x["mode"], x["lever_set"]) for x in rsc})
    for k, (sc, mode, sid) in enumerate(combos):
        r = 7 + k
        for j, v_ in enumerate((sc, mode, sid)):
            wsc.cell(row=r, column=1 + j, value=v_).font = BLACK
        for j, n in enumerate(nodes_s):
            c = wsc.cell(row=r, column=4 + j, value=float(keyd[(sc, mode, sid, n)]["p_ready_by_target"]))
            c.font, c.number_format = BLUE, PCT
        wsc.cell(row=r, column=10, value=keyd[(sc, mode, sid, "END")]["p50_date"]).font = BLUE
        wsc.cell(row=r, column=11, value=keyd[(sc, mode, sid, "END")]["p80_date"]).font = BLUE
    wsc.freeze_panes = "D7"

    # ------------------------------------------------------------------ Cost of delay (live weekly exposure; expected values pasted)
    wcd = wb.create_sheet("Cost of delay")
    wcd["A1"] = "EU revenue at risk if a line cannot place new units or versions after 11 Dec 2027 (estimates; units already placed may continue)"
    wcd["A1"].font = TITLE
    header(wcd, 3, ["Line", "Hardware revenue (EUR m a year)", "Paid software revenue", "Enabled revenue", "Weekly revenue at risk, live (EUR m)", "Note"],
           [34, 16, 16, 16, 18, 90])
    EXd = summ["cod_exposure_eur_m_yr"]
    for k, (cid, _, lname) in enumerate(mdl.COD_LINES):
        r = 4 + k
        wcd.cell(row=r, column=1, value=lname).font = BLACK
        for j, cls in enumerate(("hardware", "sw_product", "sw_enabled")):
            c = wcd.cell(row=r, column=2 + j, value=EXd[cid][cls])
            c.font, c.number_format = BLUE, NUM1
        c = wcd.cell(row=r, column=5, value=f"=(B{r}*cod_exp_hardware+C{r}*cod_exp_swproduct+D{r}*cod_exp_swenabled)/52")
        c.number_format = NUM2
    rT = 4 + len(mdl.COD_LINES)
    wcd.cell(row=rT, column=1, value="Total").font = BOLD
    for col in range(2, 6):
        c = wcd.cell(row=rT, column=col, value=f"=SUM({L(col)}4:{L(col)}{rT - 1})")
        c.font, c.number_format = BOLD, (NUM2 if col == 5 else NUM1)
    wcd.cell(row=4, column=6, value="Revenue from portfolio-classification/classification.csv (illustrative); mapping in families.csv. Hardware loses revenue after the channel-stock buffer (cod_buffer_weeks)").font = BLACK
    wcd.cell(row=5, column=6, value="Free clients keep current users and security updates (Art 69(2); guidance paras 15, 108); only a feature freeze bites").font = BLACK
    cod = list(csv.DictReader((OUT / "cost_of_delay.csv").open()))
    r0 = rT + 3
    wcd.cell(row=r0 - 1, column=1, value="Monte Carlo cost of delay (values from model.py; correlated four-factor mode unless stated; lateness capped at 31 Dec 2028)").font = BOLD
    cols = ["scenario", "mode", "lever_set", "line", "p_late", "mean_weeks_late", "p80_weeks_late", "expected_rar_eur_m", "p90_rar_eur_m"]
    header(wcd, r0, cols)
    rr = r0 + 1
    for x in cod:
        if x["lever_set"] not in ("S0", "S1", "S6", "S7", "S7-L4", "S9"):
            continue
        for j, c_ in enumerate(cols):
            v_ = x[c_]
            try:
                v_ = float(v_) if j >= 4 and v_ != "" else v_
            except ValueError:
                pass
            c = wcd.cell(row=rr, column=1 + j, value=v_)
            c.font = BLUE if j >= 4 else BLACK
            if c_ == "p_late" and v_ != "":
                c.number_format = PCT
        rr += 1

    # ------------------------------------------------------------------ Lever value (values)
    wlv = wb.create_sheet("Lever value")
    wlv["A1"] = "Expected value of each lever: reduction in expected EU revenue at risk x contribution margin, less budget cost (values from model.py; correlated mode)"
    wlv["A1"].font = TITLE
    lv = list(csv.DictReader((OUT / "lever_value.csv").open()))
    cols = list(lv[0].keys())
    header(wlv, 3, cols, [8, 50, 9, 12, 14, 12, 12, 14, 12])
    for k, x in enumerate(lv):
        for j, c_ in enumerate(cols):
            v_ = x[c_]
            c = wlv.cell(row=4 + k, column=1 + j, value=float(v_) if j >= 3 else v_)
            c.font = BLUE if j >= 3 else BLACK
            if j >= 3:
                c.number_format = EURM
    wlv.cell(row=6 + len(lv), column=1, value="'Alone' compares the lever with the base plan; 'in set' removes it from L1-L5. Costs are the change in total budget Q4 2026-Q4 2028 at base inputs. Margin: cod_margin base.").font = BLACK

    # ------------------------------------------------------------------ Correlation (values)
    wco = wb.create_sheet("Correlation")
    wco["A1"] = "Factor loadings for the correlated Monte Carlo (from assumptions.yaml). Positive loading moves an input towards its costly or slow end."
    wco["A1"].font = TITLE
    header(wco, 3, ["Input"] + list(mdl.FACTORS) + ["Own noise share", "Why"], [30, 10, 10, 10, 10, 14, 80])
    for k, (key, ld) in enumerate(M.corr.items()):
        r = 4 + k
        wco.cell(row=r, column=1, value=key).font = BLACK
        for j, f_ in enumerate(mdl.FACTORS):
            c = wco.cell(row=r, column=2 + j, value=ld[f_])
            c.font, c.number_format = BLUE, NUM2
        c = wco.cell(row=r, column=2 + len(mdl.FACTORS), value=f"=SQRT(MAX(0,1-SUMSQ(B{r}:{L(1 + len(mdl.FACTORS))}{r})))")
        c.number_format = NUM2
        wco.cell(row=r, column=3 + len(mdl.FACTORS), value=ld["why"]).font = BLACK

    # ------------------------------------------------------------------ Market evidence (values)
    wme = wb.create_sheet("Market evidence")
    wme["A1"] = "Public evidence on CRA notified-body capacity (pages opened 1 Nov 2026; vendor statements labelled)"
    wme["A1"].font = TITLE
    me = list(csv.reader((HERE / "market_evidence.csv").open()))
    header(wme, 3, me[0], [6, 30, 12, 80, 16, 14, 26, 60, 60])
    for k, rrow in enumerate(me[1:]):
        for j, v_ in enumerate(rrow):
            c = wme.cell(row=4 + k, column=1 + j, value=v_)
            c.font = BLACK
            c.alignment = Alignment(wrap_text=True, vertical="top")

    # ------------------------------------------------------------------ Reconciliation
    wrc = wb.create_sheet("Reconciliation")
    wrc["A1"] = "Reconciliation of every module figure used (from model.py)"
    wrc["A1"].font = TITLE
    rec = list(csv.reader((OUT / "reconciliation.csv").open()))
    header(wrc, 3, rec[0], [46, 30, 30, 60, 80])
    for k, rrow in enumerate(rec[1:]):
        for j, v in enumerate(rrow):
            wrc.cell(row=4 + k, column=1 + j, value=v).font = BLACK

    for sh in wb.worksheets:
        for rowc in sh.iter_rows():
            for c in rowc:
                if c.font is None or c.font.name != F:
                    c.font = Font(name=F, size=c.font.size if c.font else 10, bold=c.font.bold if c.font else False,
                                  color=c.font.color if c.font else None)
    wb.save(XLSX)
    print(f"Wrote {XLSX.name}")


if __name__ == "__main__":
    main()
