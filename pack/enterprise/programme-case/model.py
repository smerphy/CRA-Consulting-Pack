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

Module inputs read (paths relative to pack/enterprise/):
  art14-operations/volume_model_output.csv          (E2)
  portfolio-classification/nb_demand_summary.json   (E3)
  portfolio-classification/nb_demand.csv            (E3)
  portfolio-classification/classification_summary.json (E3)
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
    ("nb_y1_eur", "Module H year-1 fees, 4 organisations (EUR)", "nb_y1_lumen+nb_y1_platforms+nb_y1_devices+nb_y1_cloud_apps"),
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
    ("div_lumen", "Share divisor, Lumen (1 = full body)", "IF(lever_seq,1,2)"),
    ("div_platforms", "Share divisor, Platforms", "IF(lever_seq,1,2)"),
    ("div_devices", "Share divisor, Devices", "IF(MAX(lever_seq,lever_thirdbody),1,2)"),
    ("div_cloud_apps", "Share divisor, Cloud and apps", "IF(MAX(lever_seq,lever_thirdbody),1,2)"),
]
EVAL_NS = {"MAX": max, "MIN": min, "IF": lambda c, a, b: a if c else b}


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
        }
        LOG.append(f"read {p.relative_to(ENT)}")
    p = ENT / "portfolio-classification/classification_summary.json"
    if p.exists():
        m["e3_class"] = json.loads(p.read_text())
        LOG.append(f"read {p.relative_to(ENT)}")
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
        self.inputs = {i["key"]: i for i in self.items if i["section"] in ("global", "cost", "nb", "lever")}
        self.lines = [i for i in self.items if i["section"] == "line"]
        self.acts = [i for i in self.items if i["section"] == "activity"]
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

    @staticmethod
    def derive(v: dict) -> dict:
        ns = dict(EVAL_NS)
        ns.update(v)
        for key, _, tpl in DERIVED:
            ns[key] = eval(tpl, {"__builtins__": {}}, ns)  # templates are module constants
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
        ws["10 Contingency"] = cont
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
                d[a["key"]] = eval(a["dur_formula"], {"__builtins__": {}}, ns)
            elif "pc_base" in a and v.get("lever_precontract"):
                d[a["key"]] = pickfn(a, "pc_")
            else:
                d[a["key"]] = pickfn(a, "")
        return d

    def active_preds(self, a: dict, v: dict) -> list[str]:
        ns = dict(EVAL_NS)
        ns.update(v)
        preds = list(a["pred_list"])
        for cond, pid in a["cond_list"]:
            if eval(cond, {"__builtins__": {}}, ns):
                preds.append(pid)
        return preds

    def cpm(self, v: dict, d: dict, backward: bool = True) -> dict:
        es, ef, drv = {}, {}, {}
        preds = {n: self.active_preds(self.act_by_id[n], v) for n in self.order}
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
    ("S0", "Base plan as the modules set it out (two bodies, shared capacity)", {}, None),
    ("S1", "L1 pre-contract both bodies and reserve 8 assessors each", {"lever_precontract": 1}, None),
    ("S2", "L2 priority sequencing (Lumen and Devices first)", {"lever_seq": 1}, None),
    ("S3", "L3 third body for Cloud and apps", {"lever_thirdbody": 1}, None),
    ("S4", "L1 + L2", {"lever_precontract": 1, "lever_seq": 1}, None),
    ("S5", "L1 + L2 + L3 (recommended)", {"lever_precontract": 1, "lever_seq": 1, "lever_thirdbody": 1}, None),
    ("S6", "External: Module H body designated by 31 Jan 2027, base plan", {}, ("NB0", 90.0)),
    ("S7", "External: designation by 31 Jan 2027, with L1 + L2 + L3", {"lever_precontract": 1, "lever_seq": 1, "lever_thirdbody": 1}, ("NB0", 90.0)),
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


def main() -> None:
    OUT.mkdir(exist_ok=True)
    M = Model()
    qb = quarter_bounds()
    deadline_day = (DEADLINE - START).days

    def scen_pick(scen):
        return lambda a, pre: float(a[pre + scen])

    # ---- deterministic scenarios
    det = {}
    for s in SCEN:
        v = M.derive(M.pick(s))
        b = M.budget(v)
        d = M.durations(v, scen_pick(s))
        det[s] = {"v": v, "b": b, "d": d, "cpm": M.cpm(v, d)}

    # inputs_resolved.csv
    with (OUT / "inputs_resolved.csv").open("w", newline="") as fh:
        w = csv.writer(fh)
        w.writerow(["section", "key", "description", "low", "base", "high", "unit", "label", "source", "read_from_module_file"])
        for i in M.items:
            if i["section"] in ("global", "cost", "nb", "lever"):
                w.writerow([i["section"], i["key"], i["desc"], i["low"], i["base"], i["high"], i.get("unit", ""),
                            i.get("label", ""), i.get("source", ""), i.get("resolved_from_file", "")])
        for key, desc, tpl in DERIVED:
            w.writerow(["derived", key, desc] + [round(det[s]["v"][key], 4) for s in SCEN] + ["", "derived", tpl, ""])

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
                    c = det[s]["b"]["lines"][idx]["cost"]
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
        for wsn in sorted(det["base"]["b"]["workstreams"]):
            row = ["workstream", "", wsn, "", "", "", ""]
            for m in ("one_off", "run_2027", "run_2028", "total"):
                row += [eur_m(det[s]["b"]["workstreams"][wsn][m]) for s in SCEN]
            w.writerow(row)
        row = ["total", "", "All workstreams incl. contingency", "", "", "", ""]
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
    nb_keys = ["nbd_lumen", "nbd_platforms", "nbd_devices", "nbd_cloud_apps", "nb_assessors", "nb_assessors_reserved", "nb_hmin"]
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
            v.update({"lever_precontract": 0, "lever_seq": 0, "lever_thirdbody": 0})
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

    # ---- Monte Carlo (cost)
    rng2 = random.Random(SEED + 1)
    cost_keys = [k for k, i in M.inputs.items() if i["section"] == "cost" and k != "us_ctm_pursued"]
    tot_one, tot_run28, tot_all = [], [], []
    for _ in range(N_RUNS):
        ov = {k: pert(rng2, M.inputs[k]["low"], M.inputs[k]["base"], M.inputs[k]["high"]) for k in cost_keys}
        v = M.derive(M.pick("base", ov))
        t = M.budget(v)["total"]
        tot_one.append(t["one_off"])
        tot_run28.append(t["run_2028"])
        tot_all.append(t["total"])
    cost_mc = {k: {"p10": eur_m(pct(xs, 0.1)), "p50": eur_m(pct(xs, 0.5)), "p90": eur_m(pct(xs, 0.9))}
               for k, xs in (("one_off", tot_one), ("run_2028", tot_run28), ("total_q4_2026_to_q4_2028", tot_all))}

    # ---- sensitivity (tornado)
    def eval_case(over: dict, act_over: dict):
        v = M.derive(M.pick("base", over))
        b = M.budget(v)
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
    lev5 = {"lever_precontract": 1, "lever_seq": 1, "lever_thirdbody": 1}
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
        "budget_eur_m": {s: {k: eur_m(x) for k, x in det[s]["b"]["total"].items()} for s in SCEN},
        "budget_by_workstream_eur_m": {s: {w_: {k: eur_m(x) for k, x in vals.items()} for w_, vals in det[s]["b"]["workstreams"].items()} for s in SCEN},
        "cost_monte_carlo_eur_m": cost_mc,
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

    # ---- console report
    t = {s: det[s]["b"]["total"] for s in SCEN}
    print("Inputs:", "; ".join(LOG))
    print("\n| Measure (EUR m) | Low | Base | High |\n|---|---|---|---|")
    for k, lab in (("one_off", "One-off (incl. contingency)"), ("run_2027", "Run cost Q4 2026-Q4 2027"),
                   ("run_2028", "Run cost 2028 (annual steady state)"), ("total", "Total Q4 2026-Q4 2028")):
        print(f"| {lab} | {eur_m(t['low'][k])} | {eur_m(t['base'][k])} | {eur_m(t['high'][k])} |")
    print(f"\nCost Monte Carlo: {cost_mc}")
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
