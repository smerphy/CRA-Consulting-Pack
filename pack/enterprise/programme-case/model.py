#!/usr/bin/env python3
"""Aldermoor CRA integrated programme case (module E7). Standard library only; deterministic.

Reads the other Enterprise Edition modules' outputs where they exist and the explicit
assumptions in assumptions.yaml, then writes:

  outputs/inputs_resolved.csv     every input with the value used and its source
  outputs/budget.csv              one-off and run cost by line and workstream (low/base/high)
  outputs/headcount.csv           FTE by function and quarter, Q4 2026 to Q4 2028
  outputs/nb_schedule.csv         notified-body days by quarter against capacity scenarios
  outputs/critical_path.csv       CPM on base durations (ES/EF/LS/LF, float, dates)
  outputs/readiness_probability.csv  Monte Carlo P(ready by target) per product line and lever set
  outputs/sensitivity.csv         tornado: swing in total cost and end date per driver, low to high
  outputs/summary.json            headline figures used by paper.md and the reconciliation table
  v2 additions:
  outputs/remediation.csv         per-family remediation FTE-years and cost (low/base/high)
  outputs/support_periods.csv     per-family support-period gap and extension cost (low/base/high)
  outputs/correlated_mc.csv       joint Monte Carlo cost percentiles, correlated against independent
  outputs/readiness_scenarios.csv P(ready) by market scenario (A stated, B evidence-based, C Module B+C only), mode and lever set
  outputs/cost_of_delay.csv       EU revenue at risk per product line, scenario, mode and lever set
  outputs/lever_value.csv         expected value of each lever (cost against reduction in expected revenue at risk)

Own data files: assumptions.yaml (register, market scenarios, correlation loadings), families.csv (per-family
support policy, readiness line and revenue exposure class), market_evidence.csv (public notified-body evidence).

Module inputs read (paths relative to pack/enterprise/):
  art14-operations/volume_model_output.csv          (E2)
  portfolio-classification/nb_demand_summary.json   (E3)
  portfolio-classification/nb_demand.csv            (E3)
  portfolio-classification/classification_summary.json (E3)
  portfolio-classification/classification.csv, portfolio.yaml (E3; per-family class, revenue, types, complexity)
  evidence-as-code/aldermoor-additions.json         (E1)
  open-source-strategy/projects.yaml                (E4, project count only)
  global-control-set/controls.json                  (E5, control count only)
  oj-verification/claims.csv                        (E6, date claims F02 and F03)

All Aldermoor figures are estimates for a fictional client. Usage: python3 model.py
"""
from __future__ import annotations

import csv
import datetime as dt
import json
import math
import random
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENT = HERE.parent
OUT = HERE / "outputs"
START = dt.date(2026, 11, 2)
DEADLINE = dt.date(2027, 12, 11)
QUARTERS = ["2026Q4", "2027Q1", "2027Q2", "2027Q3", "2027Q4", "2028Q1", "2028Q2", "2028Q3", "2028Q4"]
SCEN = ("low", "base", "high")
N_RUNS = 5000
SEED = 20261101
LOG: list[str] = []

# Derived quantities: one template drives both the Python model and the Excel formulas.
DERIVED = [
    ("fte_cost_eur", "Loaded cost per FTE-year (EUR)", "fte_cost_usd*usd_to_eur"),
    ("e1_storage_eur_yr", "Evidence storage (EUR a year)", "e1_storage_usd_yr*e1_storage_tier_mult*usd_to_eur"),
    ("e2_localisation_eur_yr", "Art 14(8) notice localisation (EUR a year)", "e2_user_notices*e2_loc_langs*e2_loc_eur_per_variant"),
    ("nb_y1_eur", "Module H year-1 fees, 4 organisations (EUR)", "nb_y1_lumen+IF(lever_joinqs,nb_y1_platforms_joined,nb_y1_platforms)+nb_y1_devices+nb_y1_cloud_apps"),
    ("nb_pre_eur", "Pre-assessments (EUR)", "nb_pre_eur_per_org*nb_orgs"),
    ("nb_ss_eur_yr", "Module H surveillance and extensions (EUR a year)", "nb_ss_lumen+nb_ss_platforms+nb_ss_devices+nb_ss_cloud_apps"),
    ("qs_build_fte", "Quality-system staff, build (FTE)", "qs_build_fte_per_org*nb_orgs"),
    ("qs_run_fte", "Quality-system staff, run (FTE)", "qs_run_fte_per_org*nb_orgs"),
    ("legal_opinions_eur", "Borderline opinions (EUR)", "legal_opinions_n*legal_opinion_eur"),
    ("jcstar_unit_eur", "JC-STAR cost per model (EUR)", "jcstar_fee_jpy/jpy_per_eur+jcstar_eval_eur"),
    ("jcstar_initial_eur", "JC-STAR initial applications (EUR)", "jcstar_models*jcstar_unit_eur"),
    ("jcstar_run_eur_yr", "JC-STAR renewals (2-year validity) and new models (EUR a year)", "(jcstar_models/2+jcstar_new_models_yr)*jcstar_unit_eur"),
    ("us_ctm_eur", "US Cyber Trust Mark lab tests if pursued (EUR)", "us_ctm_pursued*jcstar_models*us_ctm_lab_usd*usd_to_eur"),
    ("annexvii_fteyrs", "Annex VII human parts (FTE-years; 46 working weeks)", "doc_units*annexvii_pw/46"),
    ("annexii_fteyrs", "Annex II drafting (FTE-years)", "doc_units*annexii_pw/46"),
    ("translation_eur", "Translations (EUR)", "doc_units*tr_words*tr_eur_per_word*tr_langs"),
    ("translation_run_eur_yr", "Translation refresh (EUR a year)", "translation_eur*tr_refresh_share"),
    ("train_delivery_eur", "Training delivery (EUR)", "train_core_staff*train_eur_per_learner"),
    ("train_run_eur_yr", "Training refresh (EUR a year)", "train_delivery_eur*train_refresh_share"),
    ("train_staff_hours_memo", "MEMO: staff hours in training (not in budget)", "train_core_staff*train_core_hours+engineers_total*train_awareness_hours"),
    ("train_staff_cost_memo", "MEMO: staff time cost of training (EUR, not in budget)", "train_staff_hours_memo*fte_cost_eur/productive_hours"),
    ("nb_assessors_eff", "Assessors per body working for Aldermoor", "IF(lever_precontract,nb_assessors_reserved,nb_assessors)"),
    ("nb_rate_body", "Body-days delivered per calendar day per body", "nb_assessors_eff*assessor_days_per_year/365"),
    ("div_lumen", "Share divisor, Lumen (1 = full body)", "IF(MAX(lever_seq,lever_joinqs),1,2)"),
    ("div_platforms", "Share divisor, Platforms", "IF(lever_seq,1,2)"),
    ("div_devices", "Share divisor, Devices", "IF(MAX(lever_seq,lever_thirdbody),1,2)"),
    ("div_cloud_apps", "Share divisor, Cloud and apps", "IF(MAX(lever_seq,lever_thirdbody),1,2)"),
    # v2: support-period extension and lever costs (rem_fteyrs and sp_fte_yr come from the per-family block)
    ("sp_eur_yr", "Support-period extension, accrued (EUR a year)", "sp_fte_yr*fte_cost_eur"),
    ("l1_bodies", "Bodies with reserved capacity (2, or 3 with L3)", "2+lever_thirdbody"),
    ("l1_reserved_days", "Reserved body-days (bodies x assessors x days x months/12)", "l1_bodies*l1_assessors_reserved*assessor_days_per_year*l1_reserve_months/12"),
    ("l1_used_days", "Module H year-1 body-days Aldermoor uses (already in fees)", "nbd_lumen+IF(lever_joinqs,nbd_platforms_joined,nbd_platforms)+nbd_devices+nbd_cloud_apps"),
    ("l1_cost_eur", "L1 reservation cost: unused reserved days plus premium (EUR)", "lever_precontract*(MAX(0,l1_reserved_days-l1_used_days)+l1_premium*l1_reserved_days)*nb_day_rate_eur"),
    ("l3_cost_eur", "L3 third-body onboarding (EUR)", "lever_thirdbody*(nb_pre_eur_per_org+l3_contract_eur)"),
]
EVAL_NS = {"MAX": max, "MIN": min, "IF": lambda c, a, b: a if c else b}
INPUT_SECTIONS = ("global", "cost", "nb", "lever", "cod")
FACTORS = ("wage", "shortage", "legal", "delivery")
MARKET_FACTORS = ("wage", "shortage", "legal")
LEVERS = ("lever_precontract", "lever_seq", "lever_thirdbody", "lever_joinqs", "lever_e1par")
ALL_ON = {k: 1 for k in LEVERS}
ALL_OFF = {k: 0 for k in LEVERS}
HORIZON = dt.date(2028, 12, 31)
COD_LINES = [("LUM", "R_LUM", "Lumen"), ("PLT", "R_PLT", "Platforms"), ("DEV", "R_DEV", "Devices Class I"),
             ("CLD", "R_CLD", "Cloud and apps Class I and II"), ("DEF", "R_DEF", "Default-class products")]


# ----------------------------------------------------------------------------- parsing
def _scalar(s: str):
    s = s.strip()
    if len(s) >= 2 and s[0] == s[-1] and s[0] in "\"'":
        return s[1:-1]
    try:
        return int(s)
    except ValueError:
        pass
    try:
        return float(s)
    except ValueError:
        return s


def parse_yaml_list(path: Path) -> list[dict]:
    """Parse the flat list-of-mappings subset of YAML used by assumptions.yaml."""
    items, cur = [], None
    for raw in path.read_text(encoding="utf-8").splitlines():
        line = raw.rstrip()
        if not line.strip() or line.strip().startswith("#"):
            continue
        if line.startswith("- "):
            cur = {}
            items.append(cur)
            line = line[2:]
        elif line.startswith("  ") and cur is not None:
            line = line.strip()
        else:
            raise ValueError(f"Unsupported YAML line: {raw!r}")
        k, _, v = line.partition(":")
        cur[k.strip()] = _scalar(v)
    return items


def load_module_inputs() -> dict:
    """Read other modules' outputs. Each value records the file it came from."""
    m: dict = {}
    p = ENT / "art14-operations/volume_model_output.csv"
    if p.exists():
        rows = []
        with p.open(newline="") as fh:
            for r in csv.DictReader(fh):
                if r.get("scenario") in SCEN:
                    rows.append(r)
        m["e2"] = {r["scenario"]: r for r in rows}
        LOG.append(f"read {p.relative_to(ENT)}")
    else:
        LOG.append(f"MISSING {p.relative_to(ENT)}: E2 fallbacks from assumptions.yaml used")
    p = ENT / "portfolio-classification/nb_demand_summary.json"
    if p.exists():
        m["e3"] = json.loads(p.read_text())
        LOG.append(f"read {p.relative_to(ENT)}")
    else:
        LOG.append(f"MISSING {p.relative_to(ENT)}: E3 fallbacks used")
    p = ENT / "portfolio-classification/nb_demand.csv"
    if p.exists():
        fams = [r for r in csv.DictReader(p.open(newline="")) if r["row_type"] == "family"]
        jc = [r for r in fams if r["classifier_id"] in ("I12", "I16", "I17", "I19")]
        m["e3_csv"] = {
            "jcstar_models": sum(float(r["initial_types"]) for r in jc),
            "jcstar_new_models_yr": sum(float(r["new_types_per_year"]) for r in jc),
            "jcstar_families": [r["id"] for r in jc],
            "nb_families": len([r for r in fams if r["note"] == ""]),
            "initial_types_nb": sum(float(r["initial_types"]) for r in fams if r["note"] == ""),
            "platforms_max_cx": max(float(r["complexity_factor_assumed"]) for r in fams if r["organisation"] == "platforms"),
        }
        LOG.append(f"read {p.relative_to(ENT)}")
    p = ENT / "portfolio-classification/classification_summary.json"
    if p.exists():
        m["e3_class"] = json.loads(p.read_text())
        LOG.append(f"read {p.relative_to(ENT)}")
    # v2: per-family data. E3 portfolio.yaml (types, complexity), classification.csv (class, revenue) and E7 families.csv.
    pc = ENT / "portfolio-classification/classification.csv"
    py = ENT / "portfolio-classification/portfolio.yaml"
    fam_rows = list(csv.DictReader((HERE / "families.csv").open(newline="")))
    rel = {}
    if py.exists():
        txt = py.read_text(encoding="utf-8")
        for blk in re.split(r"\n  - id: ", txt)[1:]:
            fid = blk.split("\n")[0].strip()
            mm = re.search(r"release: \{(.*)\}", blk)
            if mm:
                rel[fid] = {k: float(x) for k, x in re.findall(
                    r"(initial_types|new_types_per_year|complexity|substantial_mods_per_year): ([\d.]+)", mm.group(1))}
        LOG.append(f"read {py.relative_to(ENT)}")
    cls = {}
    if pc.exists():
        cls = {r["family_id"]: r for r in csv.DictReader(pc.open(newline=""))}
        LOG.append(f"read {pc.relative_to(ENT)}")
    fams = []
    for f in fam_rows:
        c, r = cls.get(f["family_id"], {}), rel.get(f["family_id"], {})
        f = dict(f)
        f["name"] = c.get("family", f["family_id"])
        f["business_line"] = c.get("business_line", "")
        f["class_bucket"] = c.get("class_bucket", "")
        f["eu_revenue_eur_m"] = float(c.get("eu_revenue_est_eur_m") or 0)
        f["complexity"] = r.get("complexity", 1.0)
        f["initial_types"] = r.get("initial_types", 0.0)
        for k in ("sp_policy_years", "sp_cohorts_per_year"):
            f[k] = float(f[k] or 0)
        fams.append(f)
    m["families"] = fams
    p = ENT / "evidence-as-code/aldermoor-additions.json"
    if p.exists():
        add = json.loads(p.read_text())["additions"]
        for a in add:
            if "product lines" in a["item"]:
                m["e1_product_lines"] = float(re.search(r"\d[\d,]*", a["value"]).group().replace(",", ""))
            if "Release volume" in a["item"]:
                m["e1_versions_week"] = float(re.search(r"\d[\d,]*", a["value"]).group().replace(",", ""))
        LOG.append(f"read {p.relative_to(ENT)}")
    p = ENT / "open-source-strategy/projects.yaml"
    if p.exists():
        m["e4_projects"] = len(re.findall(r"^  - id: ", p.read_text(), flags=re.M))
        LOG.append(f"read {p.relative_to(ENT)}")
    p = ENT / "global-control-set/controls.json"
    if p.exists():
        m["e5_controls"] = len(json.loads(p.read_text())["requirements"])
        LOG.append(f"read {p.relative_to(ENT)}")
    p = ENT / "oj-verification/claims.csv"
    if p.exists():
        rows = {r["id"]: r for r in csv.DictReader(p.open(newline=""))}
        m["e6"] = {k: rows[k]["status"] for k in ("F02", "F03", "F08", "K23") if k in rows}
        m["e6_total"] = len(rows)
        LOG.append(f"read {p.relative_to(ENT)}")
    return m


def resolve(items: list[dict], mod: dict) -> None:
    """Overwrite 'from:' inputs with module output values (in place)."""
    for it in items:
        src = it.get("from")
        if not src:
            continue
        vals = None
        if src.startswith("e2.") and "e2" in mod:
            col = src[3:]
            vals = [float(mod["e2"][s][col]) for s in SCEN]
        elif src.startswith("e3.") and "e3" in mod:
            parts = src[3:].split(".")
            e3 = mod["e3"]
            if parts[0] in ("lumen", "platforms", "devices", "cloud_apps"):
                o = e3["organisations"][parts[0]]
                lo, hi = o[parts[1] + "_low"], o[parts[1] + "_high"]
                vals = [lo, (lo + hi) / 2, hi]
            elif parts[0] == "h_ss_days":
                lo, hi = e3["totals_body_days"]["h_ss"]
                vals = [lo, (lo + hi) / 2, hi]
            elif parts[0] == "assessor_days_per_year":
                v = e3["assumptions"]["assessor_days_per_year"]
                vals = [v, v, v]
            elif parts[0] in ("platforms_joined_days", "platforms_joined_cost") and "e3_csv" in mod:
                ex = e3["assumptions"]["module_b_exam_eur"]
                f = e3["assumptions"]["h_model_review_factor"] * mod["e3_csv"]["platforms_max_cx"]
                cost = [ex[0] * f, (ex[0] + ex[1]) / 2 * f, ex[1] * f]
                vals = cost if parts[0].endswith("cost") else [c / e3["assumptions"]["day_rate_eur"] for c in cost]
            elif parts[0] in ("jcstar_models", "jcstar_new_models_yr") and "e3_csv" in mod:
                v = mod["e3_csv"][parts[0]]
                vals = [v, v, v]
        elif src == "e1.product_lines" and "e1_product_lines" in mod:
            b = mod["e1_product_lines"]
            vals = [it["low"], b, it["high"]]
        if vals is None:
            LOG.append(f"FALLBACK {it['key']}: {src} not available, assumptions.yaml values used")
            continue
        it["low"], it["base"], it["high"] = vals
        it["resolved_from_file"] = "yes"


# ----------------------------------------------------------------------------- core model
class Model:
    def __init__(self):
        self.items = parse_yaml_list(HERE / "assumptions.yaml")
        self.mod = load_module_inputs()
        resolve(self.items, self.mod)
        self.inputs = {i["key"]: i for i in self.items if i["section"] in INPUT_SECTIONS}
        self.lines = [i for i in self.items if i["section"] == "line"]
        self.acts = [i for i in self.items if i["section"] == "activity"]
        self.market = [i for i in self.items if i["section"] == "market"]
        self.corr = {i["key"]: {f: float(i.get(f, 0) or 0) for f in FACTORS} | {"why": i.get("why", "")}
                     for i in self.items if i["section"] == "corr"}
        for k, ld in self.corr.items():
            assert sum(ld[f] ** 2 for f in FACTORS) <= 1.0 + 1e-9, k
        self.families = self.mod["families"]
        self._code = {}
        for ln in self.lines:
            ln["prof"] = [float(x) for x in str(ln["profile"]).split(",")]
            assert len(ln["prof"]) == len(QUARTERS), ln["key"]
        for a in self.acts:
            a["pred_list"] = [p for p in str(a.get("preds", "")).split(";") if p]
            a["cond_list"] = []
            for c in str(a.get("cond_preds", "")).split(";"):
                if c.strip():
                    cond, _, pid = c.strip().rpartition(":")
                    a["cond_list"].append((cond.strip(), pid.strip()))
        self.act_by_id = {a["key"]: a for a in self.acts}
        self.order = self._topo()
        self.anc = self._ancestors("END")

    # -- values
    def pick(self, scen: str, overrides: dict | None = None, levers: dict | None = None) -> dict:
        v = {k: float(i[scen]) for k, i in self.inputs.items()}
        for k, i in self.inputs.items():
            if i["section"] == "lever":
                v[k] = float(i["base"])
        if overrides:
            v.update(overrides)
        if levers:
            v.update(levers)
        return v

    def cc(self, expr: str):
        """Compile an expression once (templates are module constants or assumptions.yaml fields)."""
        c = self._code.get(expr)
        if c is None:
            c = self._code[expr] = compile(expr, "<expr>", "eval")
        return c

    # -- v2 per-family remediation and support-period economics
    def family_calc(self, v: dict) -> list[dict]:
        out = []
        rate = {"default": v["rem_rate_default"], "class1": v["rem_rate_class1"], "class2": v["rem_rate_class2"]}
        for f in self.families:
            r = {"family_id": f["family_id"], "rem_fteyrs": 0.0, "sp_ext_years": 0.0, "sp_fte_yr": 0.0}
            if f["rem_scope"] == "yes":
                r["rem_fteyrs"] = (rate[f["rem_rate_class"]] * f["complexity"] * max(1.0, f["initial_types"]) ** v["rem_type_exp"]
                                   * v["rem_scale"] * v[f["severity_key"]])
            if f["sp_anchor"] == "launch":
                r["sp_ext_years"] = max(0.0, v["sp_floor_years"] + v["sp_sales_life_years"] - f["sp_policy_years"])
            elif f["sp_anchor"] == "last_sold":
                r["sp_ext_years"] = max(0.0, v["sp_floor_years"] - f["sp_policy_years"])
            r["sp_fte_yr"] = r["sp_ext_years"] * f["sp_cohorts_per_year"] * v["sp_fte_per_model_year"] * f["complexity"]
            out.append(r)
        return out

    def derive(self, v: dict) -> dict:
        fc = self.family_calc(v)
        v["rem_fteyrs"] = sum(r["rem_fteyrs"] for r in fc)
        v["sp_fte_yr"] = sum(r["sp_fte_yr"] for r in fc)
        ns = dict(EVAL_NS)
        ns.update(v)
        for key, _, tpl in DERIVED:
            ns[key] = eval(self.cc(tpl), {"__builtins__": {}}, ns)
            v[key] = ns[key]
        return v

    # -- cost
    def line_values(self, v: dict) -> list[dict]:
        out = []
        rate = v["fte_cost_eur"]
        for ln in self.lines:
            val = v[ln["value"]]
            prof = ln["prof"]
            s = sum(prof)
            if ln["type"] == "fte":
                fte = [val * f for f in prof]
            elif ln["type"] == "fteyrs":
                fte = [val * f / (s / 4) for f in prof]
            else:
                fte = [0.0] * len(prof)
            if ln["type"] in ("fte", "fteyrs"):
                cost = [x * rate / 4 for x in fte]
            elif ln["type"] == "eur_yr":
                cost = [val * f / 4 for f in prof]
            else:
                cost = [val * f / s for f in prof]
            out.append({"line": ln, "fte": fte, "cost": cost})
        return out

    def budget(self, v: dict) -> dict:
        lv = self.line_values(v)
        ws: dict = {}
        for r in lv:
            ln = r["line"]
            w = ws.setdefault(ln["workstream"], {"one_off": 0.0, "run_2027": 0.0, "run_2028": 0.0, "total": 0.0})
            c = r["cost"]
            if ln["category"] == "one-off":
                w["one_off"] += sum(c)
            else:
                w["run_2027"] += sum(c[:5])
                w["run_2028"] += sum(c[5:])
            w["total"] += sum(c)
        one = sum(w["one_off"] for w in ws.values())
        r27 = sum(w["run_2027"] for w in ws.values())
        r28 = sum(w["run_2028"] for w in ws.values())
        cont = {"one_off": one * v["contingency_rate"], "run_2027": r27 * v["contingency_run_rate"],
                "run_2028": r28 * v["contingency_run_rate"]}
        cont["total"] = cont["one_off"] + cont["run_2027"] + cont["run_2028"]
        ws["11 Contingency"] = cont
        tot = {k: sum(w[k] for w in ws.values()) for k in ("one_off", "run_2027", "run_2028", "total")}
        fte_q = [sum(r["fte"][q] for r in lv) for q in range(len(QUARTERS))]
        cost_q = [sum(r["cost"][q] for r in lv) for q in range(len(QUARTERS))]
        return {"lines": lv, "workstreams": ws, "total": tot, "fte_q": fte_q, "cost_q": cost_q}

    # -- schedule
    def _topo(self) -> list[str]:
        seen, order = set(), []

        def visit(n):
            if n in seen:
                return
            seen.add(n)
            a = self.act_by_id[n]
            for p in a["pred_list"] + [p for _, p in a["cond_list"]]:
                visit(p)
            order.append(n)
        for a in self.acts:
            visit(a["key"])
        return order

    def _ancestors(self, node: str) -> set:
        res, stack = set(), [node]
        while stack:
            n = stack.pop()
            if n in res:
                continue
            res.add(n)
            a = self.act_by_id[n]
            stack.extend(a["pred_list"] + [p for _, p in a["cond_list"]])
        return res

    def durations(self, v: dict, pickfn) -> dict:
        """pickfn(activity, prefix) returns a duration from low/base/high (prefix '' or 'pc_')."""
        ns = dict(EVAL_NS)
        ns.update(v)
        d = {}
        for a in self.acts:
            if a.get("dur_formula"):
                d[a["key"]] = eval(self.cc(a["dur_formula"]), {"__builtins__": {}}, ns)
            elif "pc_base" in a and v.get("lever_precontract"):
                d[a["key"]] = pickfn(a, "pc_")
            else:
                d[a["key"]] = pickfn(a, "")
        return d

    def active_preds(self, a: dict, v: dict, ns: dict | None = None) -> list[str]:
        if ns is None:
            ns = dict(EVAL_NS)
            ns.update(v)
        preds = list(a["pred_list"])
        for cond, pid in a["cond_list"]:
            if eval(self.cc(cond), {"__builtins__": {}}, ns):
                preds.append(pid)
        return preds

    def cpm(self, v: dict, d: dict, backward: bool = True) -> dict:
        es, ef, drv = {}, {}, {}
        ns = dict(EVAL_NS)
        ns.update(v)
        preds = {n: self.active_preds(self.act_by_id[n], v, ns) for n in self.order}
        for n in self.order:
            p = preds[n]
            es[n] = max([ef[x] for x in p], default=0.0)
            drv[n] = max(p, key=lambda x: ef[x]) if p else None
            ef[n] = es[n] + d[n]
        res = {"es": es, "ef": ef, "d": d, "driver": drv}
        if backward:
            end = ef["END"]
            succ = {n: [] for n in self.order}
            for n in self.order:
                for p in preds[n]:
                    succ[p].append(n)
            ls, lf = {}, {}
            for n in reversed(self.order):
                if n not in self.anc:
                    continue
                lf[n] = min([end] + [ls[s] for s in succ[n] if s in self.anc])
                ls[n] = lf[n] - d[n]
            res.update({"ls": ls, "lf": lf, "end": end})
        return res

    def chain(self, res: dict, node: str) -> list[str]:
        out, n = [], node
        while n:
            out.append(n)
            n = res["driver"][n]
        return list(reversed(out))


# ----------------------------------------------------------------------------- helpers
def day_to_date(day: float) -> dt.date:
    return START + dt.timedelta(days=int(math.ceil(day - 1e-9)))


def quarter_bounds() -> list[tuple[int, int]]:
    b = []
    for q in QUARTERS:
        y, n = int(q[:4]), int(q[-1])
        s = dt.date(y, 3 * n - 2, 1)
        e = dt.date(y + (n == 4), (3 * n) % 12 + 1, 1)
        s = max(s, START)
        b.append(((s - START).days, (e - START).days))
    return b


def pert(rng: random.Random, lo: float, mode: float, hi: float) -> float:
    a, b = min(lo, hi), max(lo, hi)
    if b - a < 1e-12:
        return a
    m = min(max(mode, a), b)
    al = 1 + 4 * (m - a) / (b - a)
    be = 1 + 4 * (b - m) / (b - a)
    return a + (b - a) * rng.betavariate(al, be)


def eur_m(x: float) -> float:
    return round(x / 1e6, 2)


# ----------------------------------------------------------------------------- runs
LEVER_SETS = [
    ("S0", "Base plan as the modules set it out (two bodies, shared capacity, E1 waves in sequence)", {}, None),
    ("S1", "L1 pre-contract both bodies and reserve 8 assessors each", {"lever_precontract": 1}, None),
    ("S2", "L2 priority sequencing (Lumen and Devices first)", {"lever_seq": 1}, None),
    ("S3", "L3 third body for Cloud and apps", {"lever_thirdbody": 1}, None),
    ("S4", "L4 Platforms joins the Lumen quality system", {"lever_joinqs": 1}, None),
    ("S5", "L5 default-product onboarding in parallel with E1 wave 1", {"lever_e1par": 1}, None),
    ("S6", "L1 + L2 + L3", {"lever_precontract": 1, "lever_seq": 1, "lever_thirdbody": 1}, None),
    ("S7", "L1-L5 (recommended)", {"lever_precontract": 1, "lever_seq": 1, "lever_thirdbody": 1, "lever_joinqs": 1, "lever_e1par": 1}, None),
    ("S8", "External: Module H body designated by 31 Jan 2027, base plan", {}, ("NB0", 90.0)),
    ("S9", "External: designation by 31 Jan 2027, with L1-L5", {"lever_precontract": 1, "lever_seq": 1, "lever_thirdbody": 1, "lever_joinqs": 1, "lever_e1par": 1}, ("NB0", 90.0)),
]
READY = ["R_LUM", "R_PLT", "R_DEV", "R_CLD", "R_DEF", "R_OSS", "R_A14", "G3"]

DRIVERS = [
    # name, keys (inputs or act:ID), kind
    ("Loaded cost per FTE-year (E1)", ["fte_cost_usd"], "cost"),
    ("E1 product onboarding effort", ["e1_onboarding_fteyrs"], "cost"),
    ("pt 110 review at release level instead of feature launch (E1)", ["e1_review_fte"], "cost"),
    ("PSIRT VEX operations (E1)", ["e1_vex_fte"], "cost"),
    ("Evidence platform build and run (E1)", ["e1_platform_fte", "e1_ci_fte", "e1_platform_run_fte", "e1_onboarding_run_fte", "e1_infra_eur_yr", "e1_storage_usd_yr", "e1_storage_tier_mult"], "cost"),
    ("Art 14 volume scenario (E2 low/base/high)", ["e2_cell_fte", "e2_legal_fte", "e2_comms_fte", "e2_user_notices"], "cost"),
    ("Art 14(8) notice localisation (languages, price)", ["e2_loc_langs", "e2_loc_eur_per_variant"], "cost"),
    ("Module H effort: E3 body-days and fees together", ["nb_y1_lumen", "nb_y1_platforms", "nb_y1_devices", "nb_y1_cloud_apps", "nb_ss_lumen", "nb_ss_platforms", "nb_ss_devices", "nb_ss_cloud_apps", "nbd_lumen", "nbd_platforms", "nbd_devices", "nbd_cloud_apps"], "both"),
    ("Quality-system staffing", ["qs_build_fte_per_org", "qs_run_fte_per_org"], "cost"),
    ("Foundation and LTS funding (E4)", ["oss_kite_eur_yr", "oss_mooring_eur_yr", "oss_lts_eur_yr", "oss_setup_eur"], "cost"),
    ("OSPO staffing (E4)", ["oss_build_fte", "oss_run_fte"], "cost"),
    ("Labelling team and generator (E5)", ["lab_generator_fteyrs", "lab_ops_fte", "lab_screening_fte", "lab_pos_fteyrs"], "cost"),
    ("US Cyber Trust Mark pursued (E5)", ["us_ctm_pursued", "us_ctm_lab_usd"], "cost"),
    ("Documentation effort per product line", ["annexvii_pw", "annexii_pw", "doc_run_fte"], "cost"),
    ("Translation volume and price", ["tr_words", "tr_eur_per_word", "tr_refresh_share"], "cost"),
    ("Portfolio size (product lines, E1)", ["doc_units"], "cost"),
    ("Legal and classification", ["legal_opinion_eur", "legal_build_fte", "legal_run_fte"], "cost"),
    ("Training", ["train_core_staff", "train_eur_per_learner", "train_content_eur", "train_build_fte", "train_run_fte", "train_refresh_share"], "cost"),
    ("Programme office and advisory", ["pmo_build_fte", "pmo_run_fte", "advisory_eur"], "cost"),
    ("Contingency rates", ["contingency_rate", "contingency_run_rate"], "cost"),
    ("Product remediation scale (Aldermoor family against base-pack family)", ["rem_scale"], "cost"),
    ("Remediation gap severity, all business lines", ["sev_arc", "sev_halo", "sev_apps", "sev_lumen", "sev_hearth", "sev_pulse", "sev_keystone", "sev_cloud", "sev_oss"], "cost"),
    ("Support-period extension (sales life, sustaining effort)", ["sp_sales_life_years", "sp_fte_per_model_year"], "cost"),
    ("L1 reservation terms (months, premium, day rate)", ["l1_reserve_months", "l1_premium", "nb_day_rate_eur"], "cost"),
    ("Module H body designation date (external)", ["act:NB0"], "schedule"),
    ("Assessors per body working for Aldermoor", ["nb_assessors"], "schedule"),
    ("Contracting time after designation", ["act:K_SW", "act:K_HW", "act:K_CL"], "schedule"),
    ("Second body designation lag", ["act:NB2"], "schedule"),
    ("Minimum Module H approval time", ["nb_hmin"], "schedule"),
    ("Quality-system gap assessment and documentation", ["act:C2", "act:QSD"], "schedule"),
    ("Risk assessments (all families)", ["act:RA"], "schedule"),
    ("Evidence pipeline waves (E1)", ["act:E1P", "act:E1W1", "act:E1W2", "act:E1W3"], "schedule"),
    ("Classification opinions (E3)", ["act:C1"], "schedule"),
    ("Annex II drafting and translation", ["act:AII", "act:TR"], "schedule"),
    ("Annex VII file assembly", ["act:TDN", "act:TDD"], "schedule"),
    ("Mobilisation and funding decision", ["act:M0"], "schedule"),
]


# ----------------------------------------------------------------------------- v2 joint Monte Carlo
SCHED_DERIVED = ("nb_assessors_eff", "nb_rate_body", "div_lumen", "div_platforms", "div_devices", "div_cloud_apps")
LOO_SETS = [(f"S7-{lab}", f"L1-L5 without {lab}", {**ALL_ON, key: 0}, None)
            for lab, key in zip(("L1", "L2", "L3", "L4", "L5"), LEVERS)]
MARKET_SCEN = {"A": "Stated capacity assumptions (as v1: Module H body designated Jan-Oct 2027, 5 assessors per body)",
               "B": "Evidence-based Module H (first Module H body Apr 2027 to Apr 2028, base end Sep 2027; 3 assessors per body)",
               "C": "Module B and C only through 2027 (no Module H; first Module B body Jan-Jun 2027; E3 B+C body-days)"}


def phi(z: float) -> float:
    return 0.5 * (1.0 + math.erf(z / math.sqrt(2.0)))


def cod_exposure(M) -> dict:
    """Annual EU revenue (EUR m) per cost-of-delay line and exposure class (E3 classification.csv; families.csv)."""
    ex = {c: {"hardware": 0.0, "sw_product": 0.0, "sw_enabled": 0.0} for c, _, _ in COD_LINES}
    for f in M.families:
        if f["cod_node"] in ex and f["exposure_class"] in ex[f["cod_node"]]:
            ex[f["cod_node"]][f["exposure_class"]] += f["eu_revenue_eur_m"]
    return ex


def revenue_at_risk(late_days: float, ex: dict, p: dict) -> float:
    """EUR m of EU revenue lost for one line, given days late (capped at the horizon) and exposure parameters."""
    w = late_days / 7.0
    return (ex["hardware"] / 52.0 * p["cod_exp_hardware"] * max(0.0, w - p["cod_buffer_weeks"])
            + (ex["sw_product"] * p["cod_exp_swproduct"] + ex["sw_enabled"] * p["cod_exp_swenabled"]) / 52.0 * w)


def joint_mc(M, deadline_day: int, n_runs: int) -> dict:
    """One simulation of cost and schedule together, run twice on the same noise: inputs independent, and inputs
    loaded on three shared factors (wage, shortage, legal). Schedule is run under market scenarios A, B and C."""
    e3 = M.mod.get("e3", {})

    def bc(org):
        o = e3["organisations"][org]
        lo, hi = float(o["bc_year1_body_days_low"]), float(o["bc_year1_body_days_high"])
        return (lo, (lo + hi) / 2, hi)

    base_p = {k: (float(i["low"]), float(i["base"]), float(i["high"])) for k, i in M.inputs.items()
              if i["section"] in ("cost", "nb", "cod") and k != "us_ctm_pursued"}
    for a in M.acts:
        if a.get("dur_formula"):
            continue
        base_p["act:" + a["key"]] = (float(a["low"]), float(a["base"]), float(a["high"]))
        if "pc_base" in a:
            base_p["pc:" + a["key"]] = (float(a["pc_low"]), float(a["pc_base"]), float(a["pc_high"]))
    scen_p = {sc: dict(base_p) for sc in MARKET_SCEN}
    for it in M.market:
        sc, tgt = it["key"].split(".", 1)
        vals = bc(str(it["low"])[3:]) if str(it["low"]).startswith("bc:") else (float(it["low"]), float(it["base"]), float(it["high"]))
        scen_p[sc][("act:" + tgt) if tgt in M.act_by_id else tgt] = vals
    keys = sorted(base_p)
    loads, loads_mkt = [], []
    for k in keys:
        lk = ("act:" + k[3:]) if k.startswith("pc:") else k
        ld = M.corr.get(lk)
        a = [ld[f] for f in FACTORS] if ld else [0.0] * len(FACTORS)
        loads.append((a, math.sqrt(max(0.0, 1.0 - sum(x * x for x in a)))))
        am = [x if f in MARKET_FACTORS else 0.0 for x, f in zip(a, FACTORS)]
        loads_mkt.append((am, math.sqrt(max(0.0, 1.0 - sum(x * x for x in am)))))
    # quantile tables of each PERT distribution (inverse CDF by sorted sample)
    rq, NQ, tables = random.Random(SEED + 7), 2000, {}

    def table(p):
        if p not in tables:
            tables[p] = [p[1]] if abs(p[2] - p[0]) < 1e-12 else sorted(pert(rq, *p) for _ in range(NQ))
        return tables[p]
    for sc in scen_p:
        for k in keys:
            table(scen_p[sc][k])

    def look(p, u):
        t = tables[p]
        return t[0] if len(t) == 1 else t[min(len(t) - 1, int(u * len(t)))]

    sets_ = {"A": LEVER_SETS + LOO_SETS, "B": LEVER_SETS[:8] + LOO_SETS, "C": LEVER_SETS[:8] + LOO_SETS}
    gates = {"LUM": "D_LUM", "PLT": "D_PLT", "DEV": "D_DEV", "CLD": "D_CLD"}
    rec = {"cost": {}, "ready": {}, "gate": {}, "codp": {"independent": [], "correlated": []}}
    rng = random.Random(SEED + 3)
    base_v = M.pick("base")
    for _ in range(n_runs):
        F = [rng.gauss(0, 1) for _ in FACTORS]
        e = [rng.gauss(0, 1) for _ in keys]
        for mode in ("independent", "correlated", "market_only"):
            u = {}
            for idx, k in enumerate(keys):
                a, sd = (loads_mkt if mode == "market_only" else loads)[idx]
                z = e[idx] if mode == "independent" else sum(ai * fi for ai, fi in zip(a, F)) + sd * e[idx]
                u[k] = phi(z)
            for sc in MARKET_SCEN:
                if mode == "market_only" and sc != "A":
                    continue
                P = scen_p[sc]
                vals = {k: look(P[k], u[k]) for k in keys}
                over = {k: x for k, x in vals.items() if not k.startswith(("act:", "pc:"))}
                if sc == "A" and mode != "market_only":
                    rec["codp"][mode].append({k: over[k] for k in ("cod_exp_hardware", "cod_buffer_weeks", "cod_exp_swproduct", "cod_exp_swenabled", "cod_margin")})
                    for plan, lev in (("recommended", ALL_ON), ("as_written", ALL_OFF)):
                        t = M.budget(M.derive(M.pick("base", over, lev)))["total"]
                        for m_ in ("one_off", "run_2028", "total"):
                            rec["cost"].setdefault((plan, mode, m_), []).append(t[m_])
                if mode == "market_only":
                    continue  # cost-only variant: the three market factors without the delivery factor
                sm = {(k[4:] if k.startswith("act:") else k): x for k, x in vals.items() if k.startswith(("act:", "pc:"))}
                v0 = dict(base_v)
                v0.update(over)
                ns = dict(EVAL_NS)
                for sid, _, lev, fix in sets_[sc]:
                    if mode == "independent" and sid.startswith("S7-"):
                        continue
                    v = dict(v0)
                    v.update(ALL_OFF)
                    v.update(lev)
                    ns.update(v)
                    for key, _, tpl in DERIVED:
                        if key in SCHED_DERIVED:
                            ns[key] = v[key] = eval(M.cc(tpl), {"__builtins__": {}}, ns)
                    smx = sm if not fix else {**sm, fix[0]: fix[1]}
                    d = M.durations(v, lambda a_, pre: smx[(pre[:2] + ":" if pre else "") + a_["key"]])
                    res = M.cpm(v, d, backward=False)
                    ef = res["ef"]
                    kk = (sc, mode, sid)
                    rr = rec["ready"].setdefault(kk, {r: [] for r in READY + ["END"]})
                    for r in READY + ["END"]:
                        rr[r].append(ef[r])
                    gg = rec["gate"].setdefault(kk, {c: [] for c, _, _ in COD_LINES})
                    for c, node in gates.items():
                        gg[c].append(ef[node])
                    gg["DEF"].append(max(ef["TDD"], ef["TR"], ef["E1W2"]) + d["D_DEF"])
    return rec


def main() -> None:
    OUT.mkdir(exist_ok=True)
    M = Model()
    qb = quarter_bounds()
    deadline_day = (DEADLINE - START).days

    def scen_pick(scen):
        return lambda a, pre: float(a[pre + scen])

    # ---- deterministic scenarios: det = plan as the modules set it out (levers off; drives the base-plan schedule
    # exhibits); detR = recommended plan with levers L1-L5 on (drives the budget headline, since lever costs are real)
    det, detR = {}, {}
    for s in SCEN:
        v = M.derive(M.pick(s))
        b = M.budget(v)
        d = M.durations(v, scen_pick(s))
        det[s] = {"v": v, "b": b, "d": d, "cpm": M.cpm(v, d)}
        vr = M.derive(M.pick(s, levers=ALL_ON))
        detR[s] = {"v": vr, "b": M.budget(vr)}

    # inputs_resolved.csv
    with (OUT / "inputs_resolved.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["section", "key", "description", "low", "base", "high", "unit", "label", "source", "read_from_module_file"])
        for i in M.items:
            if i["section"] in INPUT_SECTIONS:
                w.writerow([i["section"], i["key"], i["desc"], i["low"], i["base"], i["high"], i.get("unit", ""),
                            i.get("label", ""), i.get("source", ""), i.get("resolved_from_file", "")])
        for key, desc in (("rem_fteyrs", "Product remediation, all families (FTE-years; families.csv)"),
                          ("sp_fte_yr", "Support-period extension, steady state (FTE; families.csv)")):
            w.writerow(["derived", key, desc] + [round(det[s]["v"][key], 4) for s in SCEN] + ["", "derived", "per-family block in model.py", ""])
        for key, desc, tpl in DERIVED:
            w.writerow(["derived", key, desc] + [round(det[s]["v"][key], 4) for s in SCEN] + ["", "derived", tpl, ""])
        for key, desc, tpl in DERIVED:
            if key.startswith("l1_") or key.startswith("l3_"):
                w.writerow(["derived (levers L1-L5 on)", key, desc] + [round(detR[s]["v"][key], 4) for s in SCEN] + ["", "derived", tpl, ""])

    # budget.csv
    with (OUT / "budget.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        hdr = ["level", "id", "workstream", "description", "category", "value_input", "source"]
        for m in ("one_off", "run_2027", "run_2028", "total_q4_2026_to_q4_2028"):
            hdr += [f"{m}_eur_m_{s}" for s in SCEN]
        w.writerow(hdr)
        for idx, ln in enumerate(M.lines):
            row = ["line", ln["key"], ln["workstream"], ln["desc"], ln["category"], ln["value"],
                   M.inputs.get(ln["value"], {}).get("source", "derived: see inputs_resolved.csv")]
            for m in ("one_off", "run_2027", "run_2028", "total"):
                for s in SCEN:
                    c = detR[s]["b"]["lines"][idx]["cost"]
                    if m == "one_off":
                        x = sum(c) if ln["category"] == "one-off" else 0
                    elif m == "run_2027":
                        x = sum(c[:5]) if ln["category"] == "run" else 0
                    elif m == "run_2028":
                        x = sum(c[5:]) if ln["category"] == "run" else 0
                    else:
                        x = sum(c)
                    row.append(eur_m(x))
            w.writerow(row)
        for wsn in sorted(detR["base"]["b"]["workstreams"], key=lambda x: int(x.split()[0])):
            row = ["workstream", "", wsn, "", "", "", ""]
            for m in ("one_off", "run_2027", "run_2028", "total"):
                row += [eur_m(detR[s]["b"]["workstreams"][wsn][m]) for s in SCEN]
            w.writerow(row)
        row = ["total", "", "All workstreams incl. contingency (recommended plan, levers L1-L5)", "", "", "", ""]
        for m in ("one_off", "run_2027", "run_2028", "total"):
            row += [eur_m(detR[s]["b"]["total"][m]) for s in SCEN]
        w.writerow(row)
        row = ["total_as_written", "", "All workstreams incl. contingency (plan as the modules set it out, levers off)", "", "", "", ""]
        for m in ("one_off", "run_2027", "run_2028", "total"):
            row += [eur_m(det[s]["b"]["total"][m]) for s in SCEN]
        w.writerow(row)

    # headcount.csv
    funcs = sorted({ln["function"] for ln in M.lines if ln["function"] != "none"})
    with (OUT / "headcount.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["scenario", "function"] + QUARTERS + ["peak"])
        for s in SCEN:
            lv = det[s]["b"]["lines"]
            for f in funcs:
                q = [sum(r["fte"][i] for r in lv if r["line"]["function"] == f) for i in range(len(QUARTERS))]
                if s == "base":
                    w.writerow([s, f] + [round(x, 1) for x in q] + [round(max(q), 1)])
            tq = det[s]["b"]["fte_q"]
            w.writerow([s, "TOTAL"] + [round(x, 1) for x in tq] + [round(max(tq), 1)])

    # critical_path.csv (base)
    base_cpm = det["base"]["cpm"]
    with (OUT / "critical_path.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["id", "activity", "module", "predecessors_active", "dur_low", "dur_base", "dur_high", "dur_used_base",
                    "es_day", "ef_day", "ls_day", "lf_day", "total_float_days", "critical", "start_date", "finish_date",
                    "target_date", "slack_to_target_days", "source"])
        v = det["base"]["v"]
        for n in M.order:
            a = M.act_by_id[n]
            lo = det["low"]["d"][n]
            hi = det["high"]["d"][n]
            es, ef = base_cpm["es"][n], base_cpm["ef"][n]
            fl = base_cpm["ls"][n] - es if n in M.anc else None
            tgt = a.get("target")
            w.writerow([n, a["desc"], a["module"], ";".join(M.active_preds(a, v)), round(lo, 1), round(det["base"]["d"][n], 1),
                        round(hi, 1), round(base_cpm["d"][n], 1), round(es, 1), round(ef, 1),
                        round(base_cpm["ls"][n], 1) if n in M.anc else "", round(base_cpm["lf"][n], 1) if n in M.anc else "",
                        round(fl, 1) if fl is not None else "not CRA-gating",
                        "yes" if fl is not None and fl < 0.5 else "no",
                        day_to_date(es).isoformat(), day_to_date(ef).isoformat(),
                        day_to_date(tgt).isoformat() if tgt else "", round(tgt - ef, 1) if tgt else "", a.get("source", "")])

    # ---- Monte Carlo (schedule): common random numbers across lever sets
    rng = random.Random(SEED)
    nb_keys = ["nbd_lumen", "nbd_platforms", "nbd_platforms_joined", "nbd_devices", "nbd_cloud_apps", "nb_assessors", "nb_assessors_reserved", "nb_hmin"]
    finish = {sid: {r: [] for r in READY} for sid, *_ in LEVER_SETS}
    finish_end = {sid: [] for sid, *_ in LEVER_SETS}
    base_v = det["base"]["v"]
    for _ in range(N_RUNS):
        samp = {}
        for a in M.acts:
            if a.get("dur_formula"):
                continue
            samp[a["key"]] = pert(rng, a["low"], a["base"], a["high"])
            if "pc_base" in a:
                samp["pc:" + a["key"]] = pert(rng, a["pc_low"], a["pc_base"], a["pc_high"])
        nbs = {k: pert(rng, M.inputs[k]["low"], M.inputs[k]["base"], M.inputs[k]["high"]) for k in nb_keys}
        for sid, _, lev, fix in LEVER_SETS:
            v = dict(base_v)
            v.update(nbs)
            v.update({"lever_precontract": 0, "lever_seq": 0, "lever_thirdbody": 0, "lever_joinqs": 0, "lever_e1par": 0})
            v.update(lev)
            M.derive(v)
            sm = dict(samp)
            if fix:
                sm[fix[0]] = fix[1]
            d = M.durations(v, lambda a, pre: sm[("pc:" if pre else "") + a["key"]])
            res = M.cpm(v, d, backward=False)
            for r in READY:
                finish[sid][r].append(res["ef"][r])
            finish_end[sid].append(res["ef"]["END"])

    def pct(xs, p):
        s = sorted(xs)
        return s[min(len(s) - 1, int(p * len(s)))]

    prob_rows = []
    for sid, sname, _, _ in LEVER_SETS:
        for r in READY:
            a = M.act_by_id[r]
            tgt = a["target"]
            xs = finish[sid][r]
            p_tgt = sum(1 for x in xs if x <= tgt) / len(xs)
            p_dl = sum(1 for x in xs if x <= deadline_day) / len(xs)
            prob_rows.append({"lever_set": sid, "lever_description": sname, "node": r, "product_line": a["desc"],
                              "target_date": day_to_date(tgt).isoformat(), "p_ready_by_target": round(p_tgt, 3),
                              "p_ready_by_11_dec_2027": round(p_dl, 3),
                              "p50_date": day_to_date(pct(xs, 0.5)).isoformat(), "p80_date": day_to_date(pct(xs, 0.8)).isoformat()})
        xs = finish_end[sid]
        prob_rows.append({"lever_set": sid, "lever_description": sname, "node": "END", "product_line": "All CRA product lines",
                          "target_date": DEADLINE.isoformat(), "p_ready_by_target": round(sum(1 for x in xs if x <= deadline_day) / len(xs), 3),
                          "p_ready_by_11_dec_2027": round(sum(1 for x in xs if x <= deadline_day) / len(xs), 3),
                          "p50_date": day_to_date(pct(xs, 0.5)).isoformat(), "p80_date": day_to_date(pct(xs, 0.8)).isoformat()})
    with (OUT / "readiness_probability.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(prob_rows[0].keys()))
        w.writeheader()
        w.writerows(prob_rows)

    # ---- v2 joint Monte Carlo (cost and schedule; independent against correlated; market scenarios A, B, C)
    J = joint_mc(M, deadline_day, N_RUNS)

    def pstats(xs):
        return {"p10": eur_m(pct(xs, 0.1)), "p50": eur_m(pct(xs, 0.5)), "p80": eur_m(pct(xs, 0.8)),
                "p90": eur_m(pct(xs, 0.9)), "mean": eur_m(sum(xs) / len(xs))}
    cost_j = {f"{plan}|{mode}|{m_}": pstats(xs) for (plan, mode, m_), xs in J["cost"].items()}
    cost_mc = {m_: cost_j[f"recommended|independent|{m_ if m_ != 'total_q4_2026_to_q4_2028' else 'total'}"]
               for m_ in ("one_off", "run_2028", "total_q4_2026_to_q4_2028")}
    with (OUT / "correlated_mc.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["plan", "mode", "measure", "p10_eur_m", "p50_eur_m", "p80_eur_m", "p90_eur_m", "mean_eur_m"])
        for plan in ("recommended", "as_written"):
            for m_ in ("one_off", "run_2028", "total"):
                for mode in ("independent", "market_only", "correlated"):
                    st = cost_j[f"{plan}|{mode}|{m_}"]
                    w.writerow([plan, mode, m_, st["p10"], st["p50"], st["p80"], st["p90"], st["mean"]])

    # readiness by scenario, mode and lever set
    set_desc = {sid: dsc for sid, dsc, _, _ in LEVER_SETS + LOO_SETS}
    rs_rows = []
    for (sc, mode, sid), rr in sorted(J["ready"].items()):
        for r in READY + ["END"]:
            xs = rr[r]
            tgt = M.act_by_id[r].get("target", deadline_day) if r != "END" else deadline_day
            rs_rows.append({"scenario": sc, "mode": mode, "lever_set": sid, "lever_description": set_desc[sid], "node": r,
                            "product_line": M.act_by_id[r]["desc"] if r != "END" else "All CRA product lines",
                            "p_ready_by_target": round(sum(1 for x in xs if x <= tgt) / len(xs), 3),
                            "p50_date": day_to_date(pct(xs, 0.5)).isoformat(), "p80_date": day_to_date(pct(xs, 0.8)).isoformat()})
    with (OUT / "readiness_scenarios.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rs_rows[0].keys()))
        w.writeheader()
        w.writerows(rs_rows)
    rdy = {(r["scenario"], r["mode"], r["lever_set"], r["node"]): r["p_ready_by_target"] for r in rs_rows}

    # cost of delay
    EX = cod_exposure(M)
    cap = (HORIZON - DEADLINE).days
    cod_rows, rar_tot = [], {}
    for (sc, mode, sid), gg in sorted(J["gate"].items()):
        cps = J["codp"][mode]
        tot = [0.0] * len(cps)
        for c, _, lname in COD_LINES:
            xs = gg[c]
            lates = [min(max(0.0, x - deadline_day), cap) for x in xs]
            rar = [revenue_at_risk(lt, EX[c], cps[i]) for i, lt in enumerate(lates)]
            for i, x in enumerate(rar):
                tot[i] += x
            pb = {"cod_exp_hardware": M.inputs["cod_exp_hardware"]["base"], "cod_buffer_weeks": 0,
                  "cod_exp_swproduct": M.inputs["cod_exp_swproduct"]["base"], "cod_exp_swenabled": M.inputs["cod_exp_swenabled"]["base"]}
            cod_rows.append({"scenario": sc, "mode": mode, "lever_set": sid, "line": lname,
                             "eu_revenue_eur_m_yr": round(sum(EX[c].values()), 1),
                             "weekly_revenue_at_risk_base_eur_m": round(revenue_at_risk(7.0, EX[c], pb), 2),
                             "p_late": round(sum(1 for x in lates if x > 0) / len(lates), 3),
                             "mean_weeks_late": round(sum(lates) / len(lates) / 7, 2),
                             "p80_weeks_late": round(pct(lates, 0.8) / 7, 1),
                             "expected_rar_eur_m": round(sum(rar) / len(rar), 1),
                             "p90_rar_eur_m": round(pct(rar, 0.9), 1)})
        rar_tot[(sc, mode, sid)] = tot
        cod_rows.append({"scenario": sc, "mode": mode, "lever_set": sid, "line": "All lines",
                         "eu_revenue_eur_m_yr": round(sum(sum(EX[c].values()) for c, _, _ in COD_LINES), 1),
                         "weekly_revenue_at_risk_base_eur_m": "", "p_late": "", "mean_weeks_late": "", "p80_weeks_late": "",
                         "expected_rar_eur_m": round(sum(tot) / len(tot), 1), "p90_rar_eur_m": round(pct(tot, 0.9), 1)})
    with (OUT / "cost_of_delay.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(cod_rows[0].keys()))
        w.writeheader()
        w.writerows(cod_rows)
    erar = {k: sum(x) / len(x) for k, x in rar_tot.items()}

    # lever value: budget effect (total Q4 2026-Q4 2028, base inputs) against reduction in expected revenue at risk
    def btot(lev):
        return M.budget(M.derive(M.pick("base", levers={**ALL_OFF, **lev})))["total"]["total"]
    b_none, b_all = btot({}), btot(ALL_ON)
    margin = float(M.inputs["cod_margin"]["base"])
    lv_rows = []
    for k, (lab, key) in enumerate(zip(("L1", "L2", "L3", "L4", "L5"), LEVERS)):
        c_single = btot({key: 1}) - b_none
        c_loo = b_all - btot({**ALL_ON, key: 0})
        for sc in MARKET_SCEN:
            d_single = erar[(sc, "correlated", "S0")] - erar[(sc, "correlated", f"S{k + 1}")]
            d_loo = erar[(sc, "correlated", f"S7-{lab}")] - erar[(sc, "correlated", "S7")]
            lv_rows.append({"lever": lab, "description": LEVER_SETS[k + 1][1], "scenario": sc,
                            "cost_alone_eur_m": eur_m(c_single), "rar_reduction_alone_eur_m": round(d_single, 1),
                            "ev_alone_eur_m": round(d_single * margin - c_single / 1e6, 1),
                            "cost_in_set_eur_m": eur_m(c_loo), "rar_reduction_in_set_eur_m": round(d_loo, 1),
                            "ev_in_set_eur_m": round(d_loo * margin - c_loo / 1e6, 1)})
    for sc in MARKET_SCEN:
        d_all = erar[(sc, "correlated", "S0")] - erar[(sc, "correlated", "S7")]
        lv_rows.append({"lever": "L1-L5", "description": "All five levers", "scenario": sc,
                        "cost_alone_eur_m": eur_m(b_all - b_none), "rar_reduction_alone_eur_m": round(d_all, 1),
                        "ev_alone_eur_m": round(d_all * margin - (b_all - b_none) / 1e6, 1),
                        "cost_in_set_eur_m": eur_m(b_all - b_none), "rar_reduction_in_set_eur_m": round(d_all, 1),
                        "ev_in_set_eur_m": round(d_all * margin - (b_all - b_none) / 1e6, 1)})
    with (OUT / "lever_value.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(lv_rows[0].keys()))
        w.writeheader()
        w.writerows(lv_rows)

    # remediation.csv and support_periods.csv (deterministic low/base/high)
    fcs = {s_: M.family_calc(det[s_]["v"]) for s_ in SCEN}
    with (OUT / "remediation.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["family_id", "family", "business_line", "class_bucket", "rate_class", "severity_key", "e3_complexity",
                    "initial_types", "fte_years_low", "fte_years_base", "fte_years_high", "eur_m_low", "eur_m_base", "eur_m_high"])
        for i, f in enumerate(M.families):
            if f["rem_scope"] != "yes":
                continue
            w.writerow([f["family_id"], f["name"], f["business_line"], f["class_bucket"], f["rem_rate_class"], f["severity_key"],
                        f["complexity"], f["initial_types"]] + [round(fcs[s_][i]["rem_fteyrs"], 2) for s_ in SCEN]
                       + [eur_m(fcs[s_][i]["rem_fteyrs"] * det[s_]["v"]["fte_cost_eur"]) for s_ in SCEN])
    with (OUT / "support_periods.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["family_id", "family", "policy_years", "anchor", "cohorts_per_year", "e3_complexity",
                    "extra_years_low", "extra_years_base", "extra_years_high", "fte_yr_low", "fte_yr_base", "fte_yr_high",
                    "eur_m_yr_low", "eur_m_yr_base", "eur_m_yr_high", "source"])
        for i, f in enumerate(M.families):
            if f["sp_anchor"] not in ("launch", "last_sold", "not_updatable"):
                continue
            w.writerow([f["family_id"], f["name"], f["sp_policy_years"], f["sp_anchor"], f["sp_cohorts_per_year"], f["complexity"]]
                       + [round(fcs[s_][i]["sp_ext_years"], 2) for s_ in SCEN] + [round(fcs[s_][i]["sp_fte_yr"], 2) for s_ in SCEN]
                       + [eur_m(fcs[s_][i]["sp_fte_yr"] * det[s_]["v"]["fte_cost_eur"]) for s_ in SCEN] + [f["sp_policy_source"]])

    # ---- sensitivity (tornado)
    def eval_case(over: dict, act_over: dict):
        v = M.derive(M.pick("base", over))
        b = M.budget(M.derive(M.pick("base", over, ALL_ON)))  # cost of the recommended plan; schedule of the base plan
        d = M.durations(v, lambda a, pre: act_over.get(a["key"], float(a[pre + "base"])))
        r = M.cpm(v, d, backward=False)
        return b["total"]["total"], r["ef"]["END"], r["ef"]["R_LUM"], r["ef"]["R_DEF"]

    base_case = eval_case({}, {})
    sens = []
    for name, keys, kind in DRIVERS:
        res = {}
        for s in ("low", "high"):
            over, aover = {}, {}
            for k in keys:
                if k.startswith("act:"):
                    aover[k[4:]] = float(M.act_by_id[k[4:]][s])
                else:
                    over[k] = float(M.inputs[k][s])
            res[s] = eval_case(over, aover)
        desc_lo = "; ".join(f"{k}={M.inputs[k]['low'] if not k.startswith('act:') else M.act_by_id[k[4:]]['low']}" for k in keys[:4])
        desc_hi = "; ".join(f"{k}={M.inputs[k]['high'] if not k.startswith('act:') else M.act_by_id[k[4:]]['high']}" for k in keys[:4])
        sens.append({
            "driver": name, "kind": kind, "inputs": ";".join(keys), "low_setting": desc_lo, "high_setting": desc_hi,
            "total_cost_low_eur_m": eur_m(res["low"][0]), "total_cost_high_eur_m": eur_m(res["high"][0]),
            "cost_swing_eur_m": eur_m(res["high"][0] - res["low"][0]),
            "end_date_low": day_to_date(res["low"][1]).isoformat(), "end_date_high": day_to_date(res["high"][1]).isoformat(),
            "end_swing_days": round(res["high"][1] - res["low"][1], 1),
            "lumen_ready_low": day_to_date(res["low"][2]).isoformat(), "lumen_ready_high": day_to_date(res["high"][2]).isoformat(),
            "lumen_swing_days": round(res["high"][2] - res["low"][2], 1),
            "default_ready_low": day_to_date(res["low"][3]).isoformat(), "default_ready_high": day_to_date(res["high"][3]).isoformat(),
            "default_swing_days": round(res["high"][3] - res["low"][3], 1),
        })
    for key, field in (("rank_cost", "cost_swing_eur_m"), ("rank_schedule", "end_swing_days")):
        for rank, row in enumerate(sorted(sens, key=lambda r: -abs(r[field])), 1):
            row[key] = rank if abs(row[field]) > 1e-9 else ""
    sens.sort(key=lambda r: (-abs(r["cost_swing_eur_m"]), -abs(r["end_swing_days"])))
    with (OUT / "sensitivity.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(sens[0].keys()))
        w.writeheader()
        w.writerows(sens)

    # ---- notified-body schedule by quarter
    vb = det["base"]["v"]
    E3 = M.mod.get("e3", {})

    def overlap(q, a, b):
        s, e = qb[q]
        return max(0.0, min(e, b) - max(s, a))

    internal_ready = max(base_cpm["ef"][x] for x in ("QSD", "E1W1", "RA"))

    def demand(scen):
        tot = sum(float(M.inputs[k][scen]) for k in ("nbd_lumen", "nbd_platforms", "nbd_devices", "nbd_cloud_apps"))
        ss = float(M.inputs["nbd_ss_total"][scen])
        span = deadline_day - internal_ready
        return [tot * overlap(q, internal_ready, deadline_day) / span + ss / 365 * overlap(q, deadline_day, 10 ** 6)
                for q in range(len(QUARTERS))], tot

    dem = {s: demand(s) for s in SCEN}
    # capacity scenarios: bodies available from contract day; assessors x 180/365 body-days per calendar day
    lev5 = {"lever_precontract": 1, "lever_seq": 1, "lever_thirdbody": 1, "lever_joinqs": 1, "lever_e1par": 1}
    v5 = M.derive(M.pick("base", levers=lev5))
    c5 = M.cpm(v5, M.durations(v5, scen_pick("base")), backward=False)
    vh = M.derive(M.pick("high"))
    ch = M.cpm(vh, M.durations(vh, scen_pick("high")), backward=False)
    rate = M.inputs["assessor_days_per_year"]["base"] / 365
    cap_scen = {
        "base": ([base_cpm["ef"]["K_SW"], base_cpm["ef"]["K_HW"]], vb["nb_assessors"]),
        "constrained": ([ch["ef"]["K_SW"], ch["ef"]["K_HW"]], M.inputs["nb_assessors"]["high"]),
        "levers": ([c5["ef"]["K_SW"], c5["ef"]["K_HW"], c5["ef"]["K_CL"]], M.inputs["nb_assessors_reserved"]["base"]),
    }
    nb_rows, clear = [], {}
    for cs, (avail, ass) in cap_scen.items():
        backlog, cum_dem, cum_proc = 0.0, 0.0, 0.0
        wave1 = dem["base"][1]
        for q in range(len(QUARTERS)):
            cap = sum(ass * rate * overlap(q, a, 10 ** 6) for a in avail)
            arrivals = dem["base"][0][q]
            proc = min(cap, backlog + arrivals)
            backlog = backlog + arrivals - proc
            cum_proc += proc
            if cs not in clear and cum_proc >= wave1 - 1e-6:
                clear[cs] = QUARTERS[q]
            if cs == "base":
                nb_rows.append({"quarter": QUARTERS[q], "start": (START + dt.timedelta(days=qb[q][0])).isoformat(),
                                "end": (START + dt.timedelta(days=qb[q][1] - 1)).isoformat()})
            row = nb_rows[q]
            row[f"capacity_{cs}"] = round(cap, 1)
            row[f"processed_{cs}"] = round(proc, 1)
            row[f"backlog_{cs}"] = round(backlog, 1)
        clear.setdefault(cs, "after 2028Q4")
    thin_q = M.inputs["eu_capacity_thin"]["base"] / 4
    mod_q = M.inputs["eu_capacity_moderate"]["base"] / 4
    for q, row in enumerate(nb_rows):
        row["demand_needed_low"] = round(dem["low"][0][q], 1)
        row["demand_needed_base"] = round(dem["base"][0][q], 1)
        row["demand_needed_high"] = round(dem["high"][0][q], 1)
        row["eu_capacity_thin_market"] = thin_q
        row["eu_capacity_moderate_market"] = mod_q
        row["aldermoor_share_of_thin_market_base"] = round(dem["base"][0][q] / thin_q, 3)
    order_cols = ["quarter", "start", "end", "demand_needed_low", "demand_needed_base", "demand_needed_high",
                  "capacity_base", "processed_base", "backlog_base", "capacity_constrained", "processed_constrained",
                  "backlog_constrained", "capacity_levers", "processed_levers", "backlog_levers",
                  "eu_capacity_thin_market", "eu_capacity_moderate_market", "aldermoor_share_of_thin_market_base"]
    with (OUT / "nb_schedule.csv").open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=order_cols)
        w.writeheader()
        for r in nb_rows:
            w.writerow({k: r[k] for k in order_cols})

    # ---- summary.json
    hc = {s: det[s]["b"]["fte_q"] for s in SCEN}
    peak_q = {s: QUARTERS[max(range(len(QUARTERS)), key=lambda i: hc[s][i])] for s in SCEN}
    chains = {r: M.chain(base_cpm, r) for r in READY + ["END"]}
    lv_base = det["base"]["b"]["lines"]
    summary = {
        "as_at": "2026-11-01", "start_date": START.isoformat(), "deadline": DEADLINE.isoformat(), "runs": N_RUNS, "seed": SEED,
        "log": LOG,
        "budget_eur_m": {s: {k: eur_m(x) for k, x in detR[s]["b"]["total"].items()} for s in SCEN},
        "budget_as_written_eur_m": {s: {k: eur_m(x) for k, x in det[s]["b"]["total"].items()} for s in SCEN},
        "budget_by_workstream_eur_m": {s: {w_: {k: eur_m(x) for k, x in vals.items()} for w_, vals in detR[s]["b"]["workstreams"].items()} for s in SCEN},
        "cost_monte_carlo_eur_m": cost_mc,
        "joint_mc_cost_eur_m": cost_j,
        "readiness_scenarios": {f"{sc}:{mode}:{sid}:{n}": p_ for (sc, mode, sid, n), p_ in rdy.items() if n in ("END", "R_LUM", "R_PLT", "R_DEV", "R_CLD", "R_DEF")},
        "expected_rar_total_eur_m": {f"{sc}:{mode}:{sid}": round(x, 1) for (sc, mode, sid), x in erar.items()},
        "cod_exposure_eur_m_yr": EX,
        "lever_value": lv_rows,
        "remediation": {s: {"fte_years": round(det[s]["v"]["rem_fteyrs"], 1), "eur_m": eur_m(det[s]["v"]["rem_fteyrs"] * det[s]["v"]["fte_cost_eur"])} for s in SCEN},
        "support_extension": {s: {"fte_yr": round(det[s]["v"]["sp_fte_yr"], 1), "eur_m_yr": eur_m(det[s]["v"]["sp_eur_yr"])} for s in SCEN},
        "lever_costs_eur_m": {s: {"l1": eur_m(detR[s]["v"]["l1_cost_eur"]), "l1_reserved_days": round(detR[s]["v"]["l1_reserved_days"]),
                                  "l1_used_days": round(detR[s]["v"]["l1_used_days"]), "l3": eur_m(detR[s]["v"]["l3_cost_eur"])} for s in SCEN},
        "headcount": {s: {"by_quarter": dict(zip(QUARTERS, [round(x, 1) for x in hc[s]])), "peak": round(max(hc[s]), 1),
                          "peak_quarter": peak_q[s], "q4_2028": round(hc[s][-1], 1)} for s in SCEN},
        "critical_path_base": {"end_day": round(base_cpm["end"], 1), "end_date": day_to_date(base_cpm["end"]).isoformat(),
                               "critical_activities": [n for n in M.order if n in M.anc and base_cpm["ls"][n] - base_cpm["es"][n] < 0.5],
                               "driving_chains": chains,
                               "ready_dates": {r: day_to_date(base_cpm["ef"][r]).isoformat() for r in READY},
                               "h_durations_days": {k: round(base_cpm["d"][k], 1) for k in ("H_LUM", "H_PLT", "H_DEV", "H_CLD")}},
        "critical_path_levers_base": {"ready_dates": {r: day_to_date(c5["ef"][r]).isoformat() for r in READY},
                                      "h_durations_days": {k: round(c5["d"][k], 1) for k in ("H_LUM", "H_PLT", "H_DEV", "H_CLD")}},
        "readiness": {f"{r['lever_set']}:{r['node']}": r["p_ready_by_target"] for r in prob_rows},
        "nb_schedule": {"wave1_days_base": round(dem["base"][1], 1), "wave1_cleared_quarter": clear,
                        "internal_ready_day": round(internal_ready, 1), "internal_ready_date": day_to_date(internal_ready).isoformat(),
                        "peak_quarter_share_of_thin_market": max(r["aldermoor_share_of_thin_market_base"] for r in nb_rows)},
        "memo_training_staff_time": {s: {"hours": round(det[s]["v"]["train_staff_hours_memo"]), "eur_m": eur_m(det[s]["v"]["train_staff_cost_memo"])} for s in SCEN},
        "e5_labelling_share_of_total_base": round(det["base"]["b"]["workstreams"]["6 Multi-jurisdiction labelling (E5)"]["total"] / det["base"]["b"]["total"]["total"], 3),
        "e1_fte_years_2027_base": round(sum(sum(r["fte"][1:5]) / 4 for r in lv_base if r["line"]["key"] in ("L01", "L02", "L03", "L04", "L05", "L06")), 1),
        "e1_fte_years_2027_low": round(sum(sum(r["fte"][1:5]) / 4 for r in det["low"]["b"]["lines"] if r["line"]["key"] in ("L01", "L02", "L03", "L04", "L05", "L06")), 1),
        "e1_fte_years_2027_high": round(sum(sum(r["fte"][1:5]) / 4 for r in det["high"]["b"]["lines"] if r["line"]["key"] in ("L01", "L02", "L03", "L04", "L05", "L06")), 1),
        "module_facts": {k: v for k, v in M.mod.items() if k not in ("e2", "e3", "e3_class")},
        "e2_incremental_fte": {s: float(M.mod["e2"][s]["fte_incremental_total"]) for s in SCEN} if "e2" in M.mod else None,
        "e3_totals": M.mod.get("e3", {}).get("totals"), "e3_totals_body_days": M.mod.get("e3", {}).get("totals_body_days"),
        "e3_nb_route_families": M.mod.get("e3_class", {}).get("nb_route_families"),
        "derived_base": {k: round(det["base"]["v"][k], 2) for k, _, _ in DERIVED},
    }
    (OUT / "summary.json").write_text(json.dumps(summary, indent=2))

    # ---- reconciliation.csv: every module figure the case uses, against its source file
    e2, e3 = M.mod.get("e2", {}), M.mod.get("e3", {})
    fx = det["base"]["v"]["usd_to_eur"]
    rate = {s: det[s]["v"]["fte_cost_eur"] for s in SCEN}
    e1y = {s: summary[f"e1_fte_years_2027_{s}"] for s in SCEN}
    rec = [
        ("E1 evidence effort, 2027 (FTE-years)", f"{e1y['low']} / {e1y['base']} / {e1y['high']}", "24-40",
         "evidence-as-code/paper.md (effort table)", "Agrees at low and base. E7 high adds release-level pt 110 review (12 FTE, E1 review paragraph) and a 25% build overrun"),
        ("E1 evidence cost, 2027 (EUR m)", " / ".join(f"{e1y[s] * rate[s] / 1e6:.1f}" for s in SCEN),
         f"USD 6-14m = EUR {6 * fx:.1f}-{14 * fx:.1f}m", "evidence-as-code/paper.md; BRIEF.md (USD 310bn = EUR 285bn)", "Agrees within the range at low and base"),
        ("E1 EU product lines to onboard", f"{M.inputs['doc_units']['base']:.0f}", f"{M.mod.get('e1_product_lines', 'n/a'):.0f}" if M.mod.get('e1_product_lines') else "n/a",
         "evidence-as-code/aldermoor-additions.json", "Agrees. E3 counts 40 families; E1 counts about 200 onboarding units. Both used, for different purposes"),
        ("E1 evidence storage, central (USD a year)", f"{M.inputs['e1_storage_usd_yr']['base']:.0f} x {M.inputs['e1_storage_tier_mult']['base']:.0f} tier multiple",
         "about 340", "evidence-as-code/paper.md (storage table)", "Agrees; E7 adds a warmer-tier multiple (assumption)"),
        ("E2 incremental Art 14 FTE", " / ".join(f"{det[s]['v']['e2_cell_fte'] + det[s]['v']['e2_legal_fte'] + det[s]['v']['e2_comms_fte']:.2f}" for s in SCEN),
         " / ".join(e2[s]["fte_incremental_total"] for s in SCEN) if e2 else "n/a", "art14-operations/volume_model_output.csv",
         "Agrees to 0.01 FTE (E7 sums the rounded components)"),
        ("E2 user notices a year", " / ".join(f"{det[s]['v']['e2_user_notices']:.0f}" for s in SCEN),
         " / ".join(e2[s]["user_notices"] for s in SCEN) if e2 else "n/a", "art14-operations/volume_model_output.csv", "Agrees"),
        ("E2 duty-officer rota (FTE-equivalent, existing PSIRT)", "not budgeted", e2["base"]["fte_duty_rota_existing"] if e2 else "n/a",
         "art14-operations/volume_model_output.csv", "Agrees: E2 says absorbed in the existing PSIRT, so E7 excludes it"),
        ("E3 Module H year-1 fees (EUR m)", " / ".join(f"{det[s]['v']['nb_y1_eur'] / 1e6:.2f}" for s in SCEN),
         f"{e3['totals']['h_y1'][0] / 1e6:.2f}-{e3['totals']['h_y1'][1] / 1e6:.2f}" if e3 else "n/a",
         "portfolio-classification/nb_demand_summary.json (totals.h_y1)", "Agrees; E7 base is the midpoint"),
        ("E3 Module H run fees (EUR m a year)", " / ".join(f"{det[s]['v']['nb_ss_eur_yr'] / 1e6:.2f}" for s in SCEN),
         f"{e3['totals']['h_ss'][0] / 1e6:.2f}-{e3['totals']['h_ss'][1] / 1e6:.2f}" if e3 else "n/a",
         "portfolio-classification/nb_demand_summary.json (totals.h_ss)", "Agrees"),
        ("E3 Module H year-1 body-days", f"{sum(float(M.inputs[k]['low']) for k in ('nbd_lumen','nbd_platforms','nbd_devices','nbd_cloud_apps')):.0f} / {dem['base'][1]:.0f} / {sum(float(M.inputs[k]['high']) for k in ('nbd_lumen','nbd_platforms','nbd_devices','nbd_cloud_apps')):.0f}",
         f"{e3['totals_body_days']['h_y1'][0]}-{e3['totals_body_days']['h_y1'][1]}" if e3 else "n/a",
         "portfolio-classification/nb_demand_summary.json (totals_body_days.h_y1)", "Agrees"),
        ("E3 share of a thin EU market", f"peak quarter {summary['nb_schedule']['peak_quarter_share_of_thin_market']:.0%} (Q3-Q4 2027)",
         "10.0-20.3% of a year", "portfolio-classification/nb_demand_summary.json (capacity_scenarios)",
         "Differs in framing, not data: E3 spreads the first wave over a year; E7 places it in the 5.5 months between internal readiness and 11 Dec 2027. E7 uses its own figure for timing"),
        ("E3 notified-body route families", str(M.mod.get("e3_csv", {}).get("nb_families", "n/a")), str(summary["e3_nb_route_families"]),
         "portfolio-classification/classification_summary.json; nb_demand.csv", "Agrees"),
        ("E3 models for JC-STAR (Hearth, Pulse Class I)", f"{M.inputs['jcstar_models']['base']:.0f}", "sum of initial_types for I.12, I.16, I.17, I.19",
         "portfolio-classification/nb_demand.csv", "Derived by E7 from E3 data"),
        ("E3 Platforms inside the Lumen QS (body-days)", f"{M.inputs['nbd_platforms_joined']['low']:.0f} / {M.inputs['nbd_platforms_joined']['base']:.0f} / {M.inputs['nbd_platforms_joined']['high']:.0f}",
         "0.5 x complexity 4 x EUR 20,000-60,000 / EUR 1,800", "portfolio-classification/nb_demand_summary.json (assumptions); nb_demand.csv (F14 complexity)",
         "Derived by E7 from E3 parameters for lever L4"),
        ("E4 projects led by Aldermoor", str(M.mod.get("e4_projects", "n/a")), "5", "open-source-strategy/projects.yaml", "Agrees; E4 gives no costs, so E7 funding lines are assumptions"),
        ("E5 controls in the global set", str(M.mod.get("e5_controls", "n/a")), "43", "global-control-set/controls.json", "Agrees"),
        ("E5 marginal labelling share of programme", f"{summary['e5_labelling_share_of_total_base']:.1%} of Q4 2026-Q4 2028 cost", "under 10% of effort",
         "global-control-set/paper.md", "Agrees"),
        ("E6 Art 14 applies from 11 Sep 2026", M.mod.get("e6", {}).get("F02", "n/a"), "Verified", "oj-verification/claims.csv (F02)", "Agrees; the Art 14 desk is a legal requirement now, not a project"),
        ("E6 Chapter IV from 11 Jun 2026; other provisions 11 Dec 2027", M.mod.get("e6", {}).get("F03", "n/a"), "Verified", "oj-verification/claims.csv (F03)", "Agrees; 11 Dec 2027 is the readiness date"),
        ("E6 Member States 'strive' for notified bodies by 11 Dec 2026", M.mod.get("e6", {}).get("K23", "n/a"), "Verified", "oj-verification/claims.csv (K23)", "Agrees; designation timing is still an assumption"),
        ("Loaded cost per FTE-year (EUR)", " / ".join(f"{rate[s]:,.0f}" for s in SCEN), "USD 250,000-350,000", "evidence-as-code/paper.md; BRIEF.md FX", "Agrees"),
        ("JC-STAR STAR-1 fee", f"JPY {M.inputs['jcstar_fee_jpy']['base']:,.0f}", "JPY 198,000 incl. tax per application", "https://www.ipa.go.jp/security/jc-star/shinsei/index.html", "External; one application per model assumed"),
    ]
    with (OUT / "reconciliation.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["figure", "value_used_in_E7 (low / base / high)", "module_value", "source_file", "status"])
        w.writerows(rec)

    # ---- console report
    t = {s: det[s]["b"]["total"] for s in SCEN}
    print("Inputs:", "; ".join(LOG))
    print("\n| Measure (EUR m) | Low | Base | High |\n|---|---|---|---|")
    for k, lab in (("one_off", "One-off (incl. contingency)"), ("run_2027", "Run cost Q4 2026-Q4 2027"),
                   ("run_2028", "Run cost 2028 (annual steady state)"), ("total", "Total Q4 2026-Q4 2028")):
        print(f"| {lab} | {eur_m(t['low'][k])} | {eur_m(t['base'][k])} | {eur_m(t['high'][k])} |")
    tR = {s: detR[s]["b"]["total"] for s in SCEN}
    print("Recommended plan (L1-L5):", {s: {k: eur_m(x) for k, x in tR[s].items()} for s in SCEN})
    print("Remediation:", summary["remediation"], "Support:", summary["support_extension"], "Lever costs:", summary["lever_costs_eur_m"])
    for plan in ("recommended",):
        for m_ in ("one_off", "run_2028", "total"):
            print(plan, m_, "indep", cost_j[f"{plan}|independent|{m_}"], "mkt", cost_j[f"{plan}|market_only|{m_}"], "corr", cost_j[f"{plan}|correlated|{m_}"])
    for sc in MARKET_SCEN:
        print(sc, "END", {f"{mode}:{sid}": rdy[(sc, mode, sid, "END")] for mode in ("independent", "correlated") for sid in ("S0", "S6", "S7", "S9") if (sc, mode, sid, "END") in rdy})
        print(sc, "E[RaR]", {sid: round(erar[(sc, "correlated", sid)]) for sid in ("S0", "S1", "S2", "S3", "S4", "S5", "S6", "S7")})
    for r in lv_rows:
        print(r)
    print(f"Peak headcount: " + ", ".join(f"{s} {max(hc[s]):.0f} ({peak_q[s]})" for s in SCEN))
    print(f"Base critical path ends {day_to_date(base_cpm['end'])}; chain {' > '.join(chains['END'])}")
    print("\n| Product line | " + " | ".join(sid for sid, *_ in LEVER_SETS) + " |")
    print("|---|" + "---|" * len(LEVER_SETS))
    for r in READY + ["END"]:
        cells = [next(x for x in prob_rows if x["lever_set"] == sid and x["node"] == r)["p_ready_by_target"] for sid, *_ in LEVER_SETS]
        name = M.act_by_id[r]["desc"] if r != "END" else "All CRA product lines"
        print(f"| {name} | " + " | ".join(f"{c:.0%}" for c in cells) + " |")
    print("\nTop schedule drivers:", [(r["driver"], r["end_swing_days"]) for r in sorted(sens, key=lambda r: -abs(r["end_swing_days"]))[:5]])
    print("Top cost drivers:", [(r["driver"], r["cost_swing_eur_m"]) for r in sens[:5]])
    print("NB wave-1 cleared:", clear)
    print("Wrote outputs/*.csv and outputs/summary.json")


if __name__ == "__main__":
    main()
