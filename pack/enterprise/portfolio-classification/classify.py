#!/usr/bin/env python3
"""Apply the knowledge-base CRA classification rules to Aldermoor's portfolio.

Reads portfolio.yaml, writes classification.csv and classification_summary.json.

The analyst records each family's facts and its single core functionality
(guidance pt 144) in portfolio.yaml, with the category the core matches. This
script applies the deterministic rules on top of that judgement:

  1. Scope gates     browser-only software is not a product (guidance paras 20-21,
                     Examples 5-6); hosted services are NIS2 territory unless they are
                     remote data processing of a product (recital 12; Art 3(2)).
  2. Placement       unmonetised FOSS is not placed on the market; its publisher is a
                     steward at most (Art 3(14), (22); recitals 15-20; guidance s.3).
  3. Integration     a component not sold separately has no class of its own and does
                     not reclassify the host (Art 7(1); Example 58); software inside a
                     product boundary takes the host's class and certificate (Example 9).
  4. Class           the category id maps to Annex III Class I / II or Annex IV.
  5. Route           Art 32 routes today (no OJ-cited harmonised standard, no Art 27(9)
                     act, no designated notified body at the KB date) and later; the
                     Art 32(5) FOSS overlay.
  6. QA              keyword hints flag possible category matches that the analyst
                     must have dismissed as ancillary (IR 2025/2392 recitals).

Category ids reuse the CRA Product Classifier (pack/out/classifier/index.html).
Sources: reports/sections/03-scope.md, 06-classification.md, 10-conformity.md,
12-open-source.md; reports/verification.md (claims 9, 10, 11).
"""
from __future__ import annotations

import csv
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

HERE = Path(__file__).resolve().parent

# id, class, Annex reference, short name (same ids as the CRA Product Classifier)
CATS = {
    "I1": ("class1", "Annex III Class I item 1", "Identity and privileged access management"),
    "I2": ("class1", "Annex III Class I item 2", "Standalone and embedded browsers"),
    "I3": ("class1", "Annex III Class I item 3", "Password managers"),
    "I4": ("class1", "Annex III Class I item 4", "Anti-malware"),
    "I5": ("class1", "Annex III Class I item 5", "VPN products"),
    "I6": ("class1", "Annex III Class I item 6", "Network management systems"),
    "I7": ("class1", "Annex III Class I item 7", "SIEM systems"),
    "I8": ("class1", "Annex III Class I item 8", "Boot managers"),
    "I9": ("class1", "Annex III Class I item 9", "PKI and certificate issuance software"),
    "I10": ("class1", "Annex III Class I item 10", "Physical and virtual network interfaces"),
    "I11": ("class1", "Annex III Class I item 11", "Operating systems"),
    "I12": ("class1", "Annex III Class I item 12", "Routers, internet modems and switches"),
    "I13": ("class1", "Annex III Class I item 13", "Microprocessors with security functions"),
    "I14": ("class1", "Annex III Class I item 14", "Microcontrollers with security functions"),
    "I15": ("class1", "Annex III Class I item 15", "ASICs and FPGAs with security functions"),
    "I16": ("class1", "Annex III Class I item 16", "Smart home virtual assistants"),
    "I17": ("class1", "Annex III Class I item 17", "Smart home products with security functions"),
    "I18": ("class1", "Annex III Class I item 18", "Connected toys"),
    "I19": ("class1", "Annex III Class I item 19", "Health-monitoring and children's wearables"),
    "II1": ("class2", "Annex III Class II item 1", "Hypervisors and container runtimes"),
    "II2": ("class2", "Annex III Class II item 2", "Firewalls, IDS and IPS"),
    "II3": ("class2", "Annex III Class II item 3", "Tamper-resistant microprocessors"),
    "II4": ("class2", "Annex III Class II item 4", "Tamper-resistant microcontrollers"),
    "IV1": ("critical", "Annex IV item 1", "Hardware devices with security boxes"),
    "IV2": ("critical", "Annex IV item 2", "Smart meter gateways and secure cryptoprocessing devices"),
    "IV3": ("critical", "Annex IV item 3", "Smartcards and secure elements"),
}

CLASS_LABEL = {
    "default": "Default",
    "class1": "Important Class I",
    "class2": "Important Class II",
    "critical": "Critical (Annex IV)",
}

# QA keyword hints: words in a family's description that suggest a category.
# A hit on a category other than the assigned one is not an error; it records
# that the ancillary/integration rules were applied (or should be checked).
HINTS = {
    "I1": r"\b(authenticat\w*|MFA|OTP|FIDO|passkey|sign-in|identity)\b",
    "I2": r"\b(browser|webview|web content|rendering)\b",
    "I3": r"\bpassword (manager|autofill)\b",
    "I5": r"\b(VPN|encrypted tunnel\w*)\b",
    "I6": r"\bnetwork management\b",
    "I8": r"\b(boot manager|boot firmware|verified boot|UEFI)\b",
    "I9": r"\b(KMS|key management|certificate issuance)\b",
    "I10": r"\b(Bluetooth radio|network interface)\b",
    "I11": r"\b(operating system|Halo OS|Lumen OS|Halo Wear OS)\b",
    "I12": r"\b(router|access point|modem|switch|border router)\b",
    "I16": r"\b(assistant|natural-language)\b",
    "I17": r"\b(camera\w*|locks?|doorbells?|alarm\w*|baby monitor\w*)\b",
    "I19": r"\b(health|heart rate|heart-rate|fitness)\b",
    "II1": r"\b(hypervisor|container runtime)\b",
    "II2": r"\b(firewall|intrusion)\b",
    "IV3": r"\b(secure element|smart-card|smartcard|TPM|eUICC)\b",
}

NB_NONE_NOTE = "none designated in NANDO at the last verified check (8 Sep 2026)"


def revenue_band(value: float, bands: list[dict]) -> str:
    for band in bands:
        if value <= band["max"]:
            return band["label"]
    return bands[-1]["label"]


def routes(cls: str, foss: bool) -> tuple[str, str, str, str]:
    """Return (route_today, route_later, notified_body_needed_today, art32_5)."""
    if cls == "default":
        return ("Module A (internal control); stricter routes optional (guidance pt 137)",
                "Module A; a cited harmonised standard adds presumption of conformity",
                "No", "Not needed")
    if foss:
        a325 = "Yes: any Art 32(1) route incl. Module A if Annex VII documentation is public at placing"
        return ("Module A with public technical documentation (Art 32(5)), or B+C / H",
                "As today", "No, if documentation is published", a325)
    if cls == "class1":
        return ("Module B+C or Module H (Art 32(2)): no OJ-cited harmonised standard, common "
                "specification or Art 27(9) scheme exists",
                "Module A once an OJ-cited harmonised standard is applied in full and covers all "
                "core-functionality risks (guidance pt 149; 2027 at the earliest); or an EUCC "
                "'substantial' certificate once the Art 27(9) act exists",
                "Yes (" + NB_NONE_NOTE + ")", "No: shipped build does not qualify as FOSS")
    if cls == "class2":
        return ("Module B+C or Module H (Art 32(3))",
                "Also an EUCC certificate at 'substantial' or higher once the Art 27(9) act "
                "exists (planned Q4 2026, not adopted); Module A never, unless FOSS",
                "Yes (" + NB_NONE_NOTE + ")", "No: shipped build does not qualify as FOSS")
    if cls == "critical":
        return ("Module B+C or Module H (Art 32(4)(b), as Class II)",
                "An Art 8(1) mandatory certification scheme if adopted (none adopted or "
                "consulted; at least 6 months' transition)",
                "Yes (" + NB_NONE_NOTE + ")", "No")
    raise ValueError(cls)


def classify(f: dict, bands: list[dict]) -> dict:
    placement = f["placement"]
    cat = f.get("category", "default")
    foss = bool(f.get("foss_qualifying"))
    cat_cls = CATS[cat][0] if cat in CATS else ("default" if cat == "default" else None)

    row = {
        "family_id": f["id"],
        "family": f["name"],
        "business_line": f["line"],
        "organisation": f["org"],
        "core_functionality": f["core_functionality"],
    }

    potential = ""
    if placement == "browser_only":
        status, bucket = "Not a product: browser-only software (guidance paras 20-21, Examples 5-6)", "out"
        annex, cid = "n/a", ""
        today = later = "n/a"; nb = "No"; a325 = "n/a"
    elif placement == "service":
        status, bucket = ("Not a product: hosted service under NIS2 (recital 12); remote data "
                          "processing only where an installed product needs it (Art 3(2))"), "out"
        annex, cid = "n/a", ""
        today = later = "n/a"; nb = "No"; a325 = "n/a"
    elif placement == "not_placed_foss":
        status = ("Not placed on the market: unmonetised FOSS; Aldermoor is open-source software "
                  "steward (Art 3(14); Art 24; guidance pts 67-68)")
        bucket = "not_placed"
        annex, cid = "n/a (steward)", ""
        today = "No conformity assessment; Art 24 policy, cooperation and reporting duties from 11 Dec 2027"
        later = "If monetised: manufacturer from that date (guidance pt 84)"
        nb = "No"
        a325 = "Would apply if monetised and in Annex III" if cat_cls in ("class1", "class2") else "n/a"
        potential = (CATS[cat][1] if cat in CATS else "Default") + " if monetised"
    elif placement in ("integrated_only", "part_of_product"):
        host = f.get("host", "")
        if placement == "integrated_only":
            status = (f"Not placed separately: integrated in {host}; no class of its own and the host is "
                      "not reclassified (Art 7(1); Example 58)")
            today = "Covered by the host product's route and risk assessment"
            nb = "Via host" if cat_cls else "No"
        else:
            status = (f"Within the product boundary of {host} (guidance para 25, Example 9); "
                      "takes the host class and certificate")
            today = "Assessed inside each host product's conformity assessment"
            nb = "Via host certificates"
        bucket = "within_other_product"
        annex = CATS[cat][1] + " function (not separately classified)" if cat in CATS else "n/a"
        cid = cat if cat in CATS else ""
        later = "Re-classify if ever supplied or sold separately"
        a325 = "n/a"
        if placement == "integrated_only" and cat in CATS:
            potential = CATS[cat][1] + " if supplied separately"
    elif placement == "placed":
        if cat == "default":
            bucket, annex, cid = "default", "None (default)", ""
        elif cat in CATS:
            bucket, annex, cid = CATS[cat][0], CATS[cat][1] + ": " + CATS[cat][2], cat
        else:
            raise ValueError(f"{f['id']}: unknown category {cat}")
        status = "Product placed on the EU market; Aldermoor is manufacturer (Art 3(13))"
        today, later, nb, a325 = routes(bucket, foss)
    else:
        raise ValueError(f"{f['id']}: unknown placement {placement}")

    # QA keyword hints
    text = " ".join([f["name"], f["core_functionality"], " ".join(f.get("ancillary", [])),
                     " ".join(f.get("integrated_components", []))])
    hits = sorted({k for k, rx in HINTS.items() if re.search(rx, text, re.I)} - {cat})
    hit_note = ""
    if hits:
        hit_note = ("Keyword match with " + ", ".join(hits) + ": assessed and not adopted as the core "
                    "functionality (ancillary, integrated or falls short; IR 2025/2392 recitals; guidance "
                    "pts 140-144); see rationale" if bucket != "out" else "")

    b = f.get("borderline", {}) or {}
    rev = float(f["eu_revenue"]["est_eur_m"])
    row.update({
        "scope_status": status,
        "class_bucket": bucket,
        "class_label": {**CLASS_LABEL, "out": "Out of scope as a product",
                        "not_placed": "Not placed (steward)",
                        "within_other_product": "Within another product"}[bucket],
        "annex_item": annex,
        "classifier_id": cid,
        "potential_if_supply_changes": potential,
        "route_today": today,
        "route_later": later,
        "notified_body_needed_today": nb,
        "art32_5_FOSS_route": a325,
        "eu_revenue_est_eur_m": int(rev),
        "eu_revenue_band": revenue_band(rev, bands),
        "eu_revenue_basis": f["eu_revenue"]["basis"],
        "release_cadence": f["release"]["cadence"],
        "versions_placed_per_year": f["release"]["versions_per_year"],
        "rdps": "; ".join(f.get("rdps", [])),
        "separately_sold_modules": "; ".join(f.get("separately_sold_modules", [])),
        "rationale": " ".join(f["rationale"].split()),
        "citations": "; ".join(f.get("citations", [])),
        "borderline_level": b.get("level", "none"),
        "borderline_note": b.get("note", ""),
        "alternative_classification": b.get("alternative", ""),
        "auto_check_hits": hit_note,
    })
    return row


def main() -> int:
    data = yaml.safe_load((HERE / "portfolio.yaml").read_text())
    bands = data["meta"]["revenue_bands_eur_m"]
    rows = [classify(f, bands) for f in data["families"]]

    ids = [r["family_id"] for r in rows]
    assert len(ids) == len(set(ids)), "duplicate family ids"

    with open(HERE / "classification.csv", "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    # Summary
    by_bucket = Counter(r["class_bucket"] for r in rows)
    rev_by_bucket = defaultdict(float)
    for r in rows:
        rev_by_bucket[r["class_bucket"]] += r["eu_revenue_est_eur_m"]
    nb_buckets = {"class1", "class2", "critical"}
    product_buckets = {"default", "class1", "class2", "critical"}
    rev_products = sum(v for k, v in rev_by_bucket.items() if k in product_buckets)
    rev_nb = sum(v for k, v in rev_by_bucket.items() if k in nb_buckets)
    # Hearth app subscription sits inside Class I device certificates
    rev_within_nb = sum(r["eu_revenue_est_eur_m"] for r in rows
                        if r["class_bucket"] == "within_other_product" and r["notified_body_needed_today"].startswith("Via host cert"))
    total_eu = data["meta"]["eu_revenue_total_eur_m"]

    matrix = defaultdict(Counter)
    for r in rows:
        matrix[r["business_line"]][r["class_bucket"]] += 1
    by_cat = Counter(r["classifier_id"] for r in rows if r["class_bucket"] in nb_buckets)

    summary = {
        "families": len(rows),
        "families_by_bucket": dict(by_bucket),
        "nb_route_families": sum(by_bucket[b] for b in nb_buckets),
        "nb_route_by_category": dict(by_cat),
        "eu_revenue_by_bucket_eur_m": {k: round(v) for k, v in rev_by_bucket.items()},
        "product_revenue_eur_m": round(rev_products),
        "nb_route_revenue_eur_m": round(rev_nb + rev_within_nb),
        "nb_route_share_of_product_revenue": round((rev_nb + rev_within_nb) / rev_products, 3),
        "nb_route_share_of_total_eu_revenue": round((rev_nb + rev_within_nb) / total_eu, 3),
        "browser_share_of_nb_route_revenue": round(
            sum(r["eu_revenue_est_eur_m"] for r in rows if r["classifier_id"] == "I2" and r["class_bucket"] == "class1")
            / (rev_nb + rev_within_nb), 3),
        "borderline_high": [f'{r["family_id"]} {r["family"]}' for r in rows if r["borderline_level"] == "high"],
        "line_by_bucket_matrix": {k: dict(v) for k, v in matrix.items()},
    }
    (HERE / "classification_summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
