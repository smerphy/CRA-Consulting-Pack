"""Article 14 volume and staffing model for Aldermoor (module E2). Standard library only.

Reads volume_model.csv (inputs with low/base/high values and source labels) and
writes volume_model_output.csv plus a printed summary table. All Aldermoor
figures are estimates; public counts (GTIG, CISA KEV, Chrome) are benchmarks
for calibration only and are not Aldermoor data.

Usage: python3 volume_model.py
"""
from __future__ import annotations

import csv
import math
from pathlib import Path

HERE = Path(__file__).resolve().parent
SCENARIOS = ("low", "base", "high")


def load(path: Path = HERE / "volume_model.csv") -> dict:
    data = {"aev": {}, "fanout": {}, "param": {}}
    with path.open(newline="") as fh:
        for row in csv.DictReader(fh):
            data[row["section"]][row["key"]] = {s: float(row[s]) for s in SCENARIOS}
    return data


def run(data: dict, s: str) -> dict:
    P = {k: v[s] for k, v in data["param"].items()}
    aev_cases = sum(v[s] for v in data["aev"].values())
    aev_notifs = sum(data["aev"][k][s] * data["fanout"][k][s] for k in data["aev"])
    si_cases = P["si_cases"]
    si_notifs = si_cases * P["si_fanout"]
    cases = aev_cases + si_cases
    notifs_pp = aev_notifs + si_notifs            # pack rule FO-1, per product
    notifs_grouped = cases                         # one record per AEV/SI
    upd = P["updates_per_notification"]
    subs_pp = notifs_pp * (3 + upd)
    subs_grouped = notifs_grouped * (3 + upd)
    filing_min = (P["ew_filer_min"] + P["ew_checker_min"] + P["n72_filer_min"] + P["n72_checker_min"]
                  + P["final_filer_min"] + P["final_checker_min"] + upd * P["update_min"])
    filing_h = notifs_pp * filing_min / 60
    legal_h = notifs_pp * 2 * P["legal_min_per_stage"] / 60
    notices = notifs_pp * P["notices_per_notification"]
    notice_h = notices * P["notice_hours"]
    triage_h = cases * P["triage_ratio"] * P["triage_hours"]
    coord_h = aev_cases * P["coord_hours_aev"] + si_cases * P["coord_hours_si"]
    upstream_h = aev_cases * P["oss_share"] * P["upstream_hours"]
    drill_h = P["drills_per_year"] * P["drill_hours"]
    cell_h = filing_h + triage_h + coord_h + upstream_h + drill_h   # PSIRT reporting cell
    fte_workload = cell_h / P["productive_hours_fte"]
    seat_fte = 8760 / P["productive_hours_fte"]          # one seat staffed every hour of the year
    fte_filing_seat = P["filing_seats"] * seat_fte
    fte_duty_rota = P["duty_seats_existing"] * seat_fte
    fte_legal = legal_h / P["productive_hours_fte"]
    fte_comms = notice_h / P["productive_hours_fte"]
    # Probability that another reportable case starts within a 72 h window of any given case
    overlap = 1 - math.exp(-cases * 3 / 365)
    return {
        "scenario": s, "aev_cases": aev_cases, "si_cases": si_cases, "srp_notifications_per_product": notifs_pp,
        "srp_notifications_grouped": notifs_grouped, "srp_submissions_per_product": subs_pp,
        "srp_submissions_grouped": subs_grouped, "user_notices": notices, "filing_hours": filing_h,
        "triage_hours": triage_h, "coordination_hours": coord_h, "cell_hours": cell_h,
        "fte_cell_workload": fte_workload, "fte_filing_seat_24x7": fte_filing_seat,
        "fte_cell_recommended": max(fte_workload, fte_filing_seat), "fte_legal": fte_legal, "fte_comms": fte_comms,
        "fte_incremental_total": max(fte_workload, fte_filing_seat) + fte_legal + fte_comms,
        "fte_duty_rota_existing": fte_duty_rota,
        "p_overlap_72h": overlap,
    }


def peak(data: dict) -> list[dict]:
    """One Lumen Engine bug, 6 products, 27 Member States: load in the first 72 hours."""
    P = {k: v["base"] for k, v in data["param"].items()}
    n = int(P["peak_products"])
    rows = []
    for mode, records in (("per_product (FO-1)", n), ("grouped", 1)):
        ew_h = records * (P["ew_filer_min"] + P["ew_checker_min"]) / 60
        n72_h = records * (P["n72_filer_min"] + P["n72_checker_min"]) / 60
        legal_h = records * P["legal_min_per_stage"] / 60
        notices = n * 2   # impacted-user notice and all-user advisory per product, regardless of SRP mode
        rows.append({
            "mode": mode, "srp_records": records, "submissions_first_72h": records * 2,
            "ar_hours_24h": ew_h, "ar_hours_72h": ew_h + n72_h, "legal_hours_72h": legal_h,
            "user_notices": notices, "localised_notice_variants": notices * int(P["languages_eu"]),
            # AR pairs needed to finish all early warnings within 4 hours of a ready data pack
            "ar_pairs_for_4h_ew": max(1, math.ceil(records * P["ew_filer_min"] / 60 / 4)),
            "member_states": int(P["peak_member_states"]),
        })
    return rows


def fmt(v):
    if isinstance(v, float):
        return f"{v:.2f}" if v < 1 else f"{v:,.1f}"
    return str(v)


def main() -> None:
    data = load()
    results = [run(data, s) for s in SCENARIOS]
    out = HERE / "volume_model_output.csv"
    with out.open("w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(results[0].keys()))
        w.writeheader()
        for r in results:
            w.writerow({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})
        fh.write("\n")
        pk = peak(data)
        w2 = csv.DictWriter(fh, fieldnames=list(pk[0].keys()))
        w2.writeheader()
        for r in pk:
            w2.writerow({k: (round(v, 2) if isinstance(v, float) else v) for k, v in r.items()})
    cols = [("aev_cases", "AEV cases/yr"), ("si_cases", "SI cases/yr"),
            ("srp_notifications_per_product", "SRP records/yr (FO-1)"),
            ("srp_notifications_grouped", "SRP records/yr (grouped)"),
            ("srp_submissions_per_product", "SRP submissions/yr (FO-1)"),
            ("user_notices", "User notices/yr"), ("cell_hours", "Cell hours/yr"),
            ("fte_cell_workload", "Cell FTE, workload"), ("fte_filing_seat_24x7", "Cell FTE, 24/7 filing seat floor"),
            ("fte_cell_recommended", "Cell FTE, recommended"), ("fte_legal", "Legal FTE"),
            ("fte_comms", "Comms FTE"), ("fte_incremental_total", "Incremental FTE, total"),
            ("fte_duty_rota_existing", "Duty-officer rota FTE (existing PSIRT)"),
            ("p_overlap_72h", "P(another case within 72 h)")]
    print("| Measure | Low | Base | High |\n|---|---|---|---|")
    for key, label in cols:
        print(f"| {label} | " + " | ".join(fmt(r[key]) for r in results) + " |")
    print("\n| Peak: one engine bug, 6 products, 27 Member States | Per product (FO-1) | Grouped |\n|---|---|---|")
    pk = peak(data)
    for key, label in (("srp_records", "SRP records"), ("submissions_first_72h", "Submissions in first 72 h"),
                       ("ar_hours_24h", "AR hours to file early warnings"),
                       ("ar_hours_72h", "AR hours to 72 h (cumulative)"), ("legal_hours_72h", "Legal hours at 72 h"),
                       ("user_notices", "User notices (impacted + all users)"),
                       ("localised_notice_variants", "Localised notice variants (24 languages, assumption)"),
                       ("ar_pairs_for_4h_ew", "AR pairs to file all early warnings in 4 h")):
        print(f"| {label} | {fmt(pk[0][key])} | {fmt(pk[1][key])} |")
    print(f"\nWrote {out.name}")


if __name__ == "__main__":
    main()
