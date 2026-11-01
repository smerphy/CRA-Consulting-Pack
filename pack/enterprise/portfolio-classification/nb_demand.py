#!/usr/bin/env python3
"""Notified-body demand model for Aldermoor's CRA portfolio (module E3).

Inputs:  portfolio.yaml (types, cadence, complexity) and classification.csv
         (class and whether a notified body is needed today; run classify.py first).
Outputs: nb_demand.csv (per family, per organisation, totals and capacity
         scenarios) and nb_demand_summary.json.

Every figure is an ESTIMATE. Cost anchors are vendor commentary reported in the
knowledge base and marked unverified there (reports/sections/10-conformity.md:
EUR 20,000-60,000 per Module B examination; EUR 80,000-150,000 for a first
Module H engagement; CRA Decoded, commentary). All other parameters are the
writer's assumptions and are labelled as such below. Market capacity is
unknown: no CRA notified body was listed in NANDO at the last verified check
(8 Sep 2026), and no official estimate of capacity exists (KB 10-conformity.md;
research notes KQ7 gaps). Capacity rows are hypothetical scenarios.

Modelling rules (legal basis in the KB):
- Module B+C: one EU-type examination per type; a substantial modification is a
  new placing on the market, re-assessed with focus on the modified parts
  (guidance pts 116, 122-123); the body must be told of modifications that may
  affect conformity (Annex VIII Module B pt 7) and audits vulnerability handling
  periodically (pt 8).
- Module H: the body approves the quality system and examines one model's
  technical documentation per product category (pt 3.1(b), 3.3); periodic
  surveillance audits (pt 4); new or substantially modified products are scope
  extensions with the same body, "a more streamlined process" (FAQ 6.3).
- Security updates are generally not substantial modifications (pt 108), so
  ordinary versions do not trigger new examinations. A software version that is
  not a substantial modification keeps the original placing date (guidance
  paras 13-15, Example 2), so the demand driver is substantial modifications and
  new types, not version count. Version count drives only the small Module B
  change-notice allowance below and the labelled "naive" sensitivity.
"""
from __future__ import annotations

import csv
import json
import sys
from collections import defaultdict
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent

A = {
    # --- KB anchors (vendor commentary, unverified; 10-conformity.md) ---
    "module_b_exam_eur": (20_000, 60_000),
    "module_h_first_eur": (80_000, 150_000),
    # --- writer's assumptions (not from the KB) ---
    "day_rate_eur": 1_800,                     # notified-body day, blended
    "assessor_days_per_year": 180,             # productive CRA assessment days per assessor
    "submod_first_type_factor": 0.40,          # share of a full exam for a focused re-assessment
    "submod_extra_type_factor": 0.10,          # each further certificate hit by the same change
    "b_periodic_audit_days": (2, 4),           # per live certificate per year (Module B pt 8)
    "b_change_notice_days": (0.05, 0.15),      # per version notified under Module B pt 7
    "h_org_scale": {"lumen": 4, "platforms": 3, "devices": 4, "cloud_apps": 3},  # x first-H cost
    "h_model_review_factor": 0.5,              # x exam x complexity, one model per category
    "h_surveillance_share": (0.25, 0.50),      # of QS approval cost per year (audits every 1-2 years)
    "h_scope_extension_factor": 0.15,          # x exam x complexity per new type or substantial change
    "horizon_years": 5,                        # 2027-2031 comparison window
    "capacity_scenarios": [                    # hypothetical EU-wide CRA notified-body capacity
        {"name": "Thin (late 2027)", "bodies": 5, "assessors_per_body": 8},
        {"name": "Moderate (2028)", "bodies": 15, "assessors_per_body": 12},
        {"name": "Mature (2029+)", "bodies": 30, "assessors_per_body": 20},
    ],
}


def lohi(x, f=1.0):
    return (x[0] * f, x[1] * f)


def add(a, b):
    return (a[0] + b[0], a[1] + b[1])


def days(cost):
    return (cost[0] / A["day_rate_eur"], cost[1] / A["day_rate_eur"])


def main() -> int:
    port = yaml.safe_load((HERE / "portfolio.yaml").read_text())
    fam = {f["id"]: f for f in port["families"]}
    cls = {r["family_id"]: r for r in csv.DictReader(open(HERE / "classification.csv"))}

    nb_ids = [i for i, r in cls.items() if r["class_bucket"] in ("class1", "class2", "critical")]
    # The Hearth app sits inside device certificates: it adds modification load, not types.
    linked = [i for i, r in cls.items() if r["notified_body_needed_today"].startswith("Via host cert")]

    exam = A["module_b_exam_eur"]
    rows, org_bc_y1, org_bc_ss, org_h_inc, org_cats = [], defaultdict(lambda: (0, 0)), defaultdict(lambda: (0, 0)), defaultdict(lambda: (0, 0)), defaultdict(dict)

    for fid in nb_ids + linked:
        f, c = fam[fid], cls[fid]
        rel = f["release"]
        cx = float(rel["complexity"])
        n0 = float(rel["initial_types"])
        new = float(rel["new_types_per_year"])
        sm = float(rel["substantial_mods_per_year"])
        ver = float(rel["versions_per_year"])
        hit = float(rel.get("affects_types", n0)) or 1.0
        org = f["org"]

        exam_f = lohi(exam, cx)
        # B+C year 1: examine every live type once
        bc_y1 = lohi(exam_f, n0)
        # B+C steady state per year
        new_cost = lohi(exam_f, new)
        sm_mult = A["submod_first_type_factor"] + A["submod_extra_type_factor"] * max(hit - 1, 0)
        sm_cost = lohi(exam_f, sm * sm_mult)
        live = max(n0, 1.0) if fid not in linked else 0.0
        audit = lohi(A["b_periodic_audit_days"], live * A["day_rate_eur"])
        notice = lohi(A["b_change_notice_days"], ver * A["day_rate_eur"]) if fid not in linked else (0, 0)
        bc_ss = add(add(add(new_cost, sm_cost), audit), notice)
        bc_y1 = add(bc_y1, add(audit, notice))
        # Module H incremental per family (scope extensions); QS and model reviews at org level
        h_inc = lohi(exam_f, (new + sm) * A["h_scope_extension_factor"])
        cid = c["classifier_id"]
        if fid not in linked:
            org_cats[org][cid] = max(org_cats[org].get(cid, 0), cx)

        # naive sensitivity (not the guidance reading): every version treated as a new type
        naive = lohi(exam_f, ver) if ver and fid not in linked else (0, 0)

        org_bc_y1[org] = add(org_bc_y1[org], bc_y1)
        org_bc_ss[org] = add(org_bc_ss[org], bc_ss)
        org_h_inc[org] = add(org_h_inc[org], h_inc)
        rows.append({
            "row_type": "family", "id": fid, "name": f["name"], "organisation": org,
            "classifier_id": cid, "class": c["class_label"],
            "initial_types": n0, "new_types_per_year": new, "substantial_mods_per_year_assumed": sm,
            "versions_per_year": ver, "complexity_factor_assumed": cx,
            "bc_year1_cost_eur_low": round(bc_y1[0]), "bc_year1_cost_eur_high": round(bc_y1[1]),
            "bc_year1_body_days_low": round(days(bc_y1)[0]), "bc_year1_body_days_high": round(days(bc_y1)[1]),
            "bc_steady_cost_eur_per_year_low": round(bc_ss[0]), "bc_steady_cost_eur_per_year_high": round(bc_ss[1]),
            "bc_steady_body_days_per_year_low": round(days(bc_ss)[0]), "bc_steady_body_days_per_year_high": round(days(bc_ss)[1]),
            "h_scope_ext_cost_eur_per_year_low": round(h_inc[0]), "h_scope_ext_cost_eur_per_year_high": round(h_inc[1]),
            "naive_every_version_new_type_cost_eur_per_year_high": round(naive[1]),
            "note": "Linked: inside Hearth device certificates" if fid in linked else "",
        })

    # Organisation level: compare routes over the horizon
    org_rows, totals = [], defaultdict(lambda: (0, 0))
    H = A["horizon_years"]
    for org in sorted(org_bc_y1):
        qs = lohi(A["module_h_first_eur"], A["h_org_scale"][org])
        reviews = (0, 0)
        for cid, cx in org_cats[org].items():
            reviews = add(reviews, lohi(exam, A["h_model_review_factor"] * cx))
        h_y1 = add(qs, reviews)
        surv = (qs[0] * A["h_surveillance_share"][0], qs[1] * A["h_surveillance_share"][1])
        h_ss = add(surv, org_h_inc[org])
        bc_total = add(org_bc_y1[org], lohi(org_bc_ss[org], H - 1))
        h_total = add(h_y1, lohi(h_ss, H - 1))
        rec = "Module H" if (h_total[0] + h_total[1]) < (bc_total[0] + bc_total[1]) else "Module B+C"
        org_rows.append({
            "row_type": "organisation", "id": org, "name": port["organisations"][org]["name"], "organisation": org,
            "classifier_id": ", ".join(sorted(org_cats[org])), "class": "",
            "bc_year1_cost_eur_low": round(org_bc_y1[org][0]), "bc_year1_cost_eur_high": round(org_bc_y1[org][1]),
            "bc_year1_body_days_low": round(days(org_bc_y1[org])[0]), "bc_year1_body_days_high": round(days(org_bc_y1[org])[1]),
            "bc_steady_cost_eur_per_year_low": round(org_bc_ss[org][0]), "bc_steady_cost_eur_per_year_high": round(org_bc_ss[org][1]),
            "bc_steady_body_days_per_year_low": round(days(org_bc_ss[org])[0]), "bc_steady_body_days_per_year_high": round(days(org_bc_ss[org])[1]),
            "h_year1_cost_eur_low": round(h_y1[0]), "h_year1_cost_eur_high": round(h_y1[1]),
            "h_year1_body_days_low": round(days(h_y1)[0]), "h_year1_body_days_high": round(days(h_y1)[1]),
            "h_steady_cost_eur_per_year_low": round(h_ss[0]), "h_steady_cost_eur_per_year_high": round(h_ss[1]),
            "h_steady_body_days_per_year_low": round(days(h_ss)[0]), "h_steady_body_days_per_year_high": round(days(h_ss)[1]),
            "bc_5yr_cost_eur_low": round(bc_total[0]), "bc_5yr_cost_eur_high": round(bc_total[1]),
            "h_5yr_cost_eur_low": round(h_total[0]), "h_5yr_cost_eur_high": round(h_total[1]),
            "recommended_route": rec,
            "note": f"{len(org_cats[org])} product categories under one quality system",
        })
        for k, v in (("bc_y1", org_bc_y1[org]), ("bc_ss", org_bc_ss[org]), ("h_y1", h_y1), ("h_ss", h_ss),
                     ("bc_5y", bc_total), ("h_5y", h_total)):
            totals[k] = add(totals[k], v)
        totals["rec_y1"] = add(totals["rec_y1"], h_y1 if rec == "Module H" else org_bc_y1[org])
        totals["rec_ss"] = add(totals["rec_ss"], h_ss if rec == "Module H" else org_bc_ss[org])

    total_row = {"row_type": "total", "id": "TOTAL", "name": "Portfolio total", "organisation": "all"}
    for k, label in (("bc_y1", "bc_year1"), ("bc_ss", "bc_steady"), ("h_y1", "h_year1"), ("h_ss", "h_steady")):
        suffix = "" if "year1" in label else "_per_year"
        total_row[f"{label}_cost_eur{suffix}_low"] = round(totals[k][0])
        total_row[f"{label}_cost_eur{suffix}_high"] = round(totals[k][1])
        total_row[f"{label}_body_days{suffix}_low"] = round(days(totals[k])[0])
        total_row[f"{label}_body_days{suffix}_high"] = round(days(totals[k])[1])
    total_row.update({"bc_5yr_cost_eur_low": round(totals["bc_5y"][0]), "bc_5yr_cost_eur_high": round(totals["bc_5y"][1]),
                      "h_5yr_cost_eur_low": round(totals["h_5y"][0]), "h_5yr_cost_eur_high": round(totals["h_5y"][1]),
                      "recommended_route": "Module H in every organisation" if all(r["recommended_route"] == "Module H" for r in org_rows) else "Mixed"})

    cap_rows = []
    rec_y1_days = days(totals["rec_y1"])
    bc_y1_days = days(totals["bc_y1"])
    rec_ss_days = days(totals["rec_ss"])
    for sc in A["capacity_scenarios"]:
        cap = sc["bodies"] * sc["assessors_per_body"] * A["assessor_days_per_year"]
        cap_rows.append({
            "row_type": "capacity_scenario (hypothetical)", "id": sc["name"], "name": sc["name"], "organisation": "EU market",
            "note": (f"{sc['bodies']} bodies x {sc['assessors_per_body']} CRA assessors x {A['assessor_days_per_year']} days = {cap:,} body-days/yr; "
                     f"Aldermoor recommended-route year-1 demand = {rec_y1_days[0]/cap:.1%}-{rec_y1_days[1]/cap:.1%}; "
                     f"steady state = {rec_ss_days[0]/cap:.1%}-{rec_ss_days[1]/cap:.1%}; "
                     f"all-B+C year-1 = {bc_y1_days[0]/cap:.1%}-{bc_y1_days[1]/cap:.1%}"),
        })

    allrows = rows + org_rows + [total_row] + cap_rows
    fields = []
    for r in allrows:
        for k in r:
            if k not in fields:
                fields.append(k)
    with open(HERE / "nb_demand.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=fields)
        w.writeheader()
        w.writerows(allrows)

    browser = [r for r in rows if r["classifier_id"] == "I2"]
    summary = {
        "assumptions": {k: v for k, v in A.items()},
        "nb_route_families": len(nb_ids),
        "types_to_certify_year1_bc": sum(r["initial_types"] for r in rows if r["note"] == ""),
        "organisations": {r["id"]: {k: r[k] for k in r if k.startswith(("bc_", "h_", "recommended"))} for r in org_rows},
        "totals": {k: [round(v[0]), round(v[1])] for k, v in totals.items()},
        "totals_body_days": {k: [round(days(v)[0]), round(days(v)[1])] for k, v in totals.items()},
        "browser_naive_every_version_cost_eur_per_year_high": sum(r["naive_every_version_new_type_cost_eur_per_year_high"] for r in browser),
        "capacity_scenarios": [r["note"] for r in cap_rows],
    }
    (HERE / "nb_demand_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
