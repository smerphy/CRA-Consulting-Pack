"""Multi-product fan-out: one upstream bug, several Aldermoor products.

What the KB says (and does not say):
  - ENISA SRP FAQ 8: "Only one notification is required for any given actively
    exploited vulnerability (AEV) or severe incident (SI)" -- stated for a
    manufacturer with several EU branches or subsidiaries (research notes KQ4;
    FAQ page updated 15 Oct 2026).
  - Guidance C(2026) 5252 para 218 / Commission FAQ 5.4: a component
    vulnerability that is not reachable or not exploited in a product is not an
    AEV for that product's manufacturer (KB 09-reporting.md "Triggers").
  - The SRP glossary lists a single "Product name and version" field per
    notification, a final report that freezes the record, and an AEV final
    deadline that runs from when a measure is available (KB 09-reporting.md).
  - The KB is SILENT on whether one SRP notification should cover several
    distinct products of the same manufacturer that share a vulnerable engine.

Pack rule (conservative design, labelled "PACK RULE FO-1"):
  Tier A  exploited      reliable evidence of exploitation in this product -> reportable.
  Tier B  reachable      same vulnerable code, reachable by the same exploit path,
                         no product-specific evidence yet -> treated as reportable
                         (conservative; the evidence of exploitation is evidence
                         about the vulnerability in Aldermoor's own code).
  Tier C  not_reachable  code absent or unreachable -> not reportable; record a
                         VEX "not_affected" justification (FAQ 5.4; para 218).
  Mode per_product (default): one SRP notification per Tier A/B product,
      cross-referenced by a shared case ID in title and summary. Reasons: one
      product field per record; each product's fix date drives its own 14-day
      final report; Member State sets differ; the record freezes at final report.
  Mode grouped: one notification listing all Tier A/B products. Use only after
      the coordinator CSIRT confirms in writing that it accepts grouped
      notifications for a shared-engine vulnerability; its final report is due
      14 days after the EARLIEST product's measure is available (conservative).
"""
from __future__ import annotations

EVIDENCE_TIERS = {"exploited": "A", "reachable": "B", "not_reachable": "C"}
FANOUT_MODES = ("per_product", "grouped")
PACK_RULE_ID = "FO-1"


class FanoutError(ValueError):
    pass


def member_states_for(product: dict, eu27: list[str]) -> list[str]:
    ms = product.get("member_states")
    if ms == "EU27":
        return list(eu27)
    if not isinstance(ms, list) or not ms:
        raise FanoutError(f"distribution map missing for product {product.get('id')}")
    unknown = [m for m in ms if m not in eu27]
    if unknown:
        raise FanoutError(f"product {product['id']}: not EU Member States: {unknown}")
    return sorted(ms, key=eu27.index)


def products_with_component(registry: dict, component_id: str) -> list[str]:
    return [p["id"] for p in registry["products"] if component_id in p.get("components", [])]


def classify(evidence: dict[str, str]) -> dict[str, str]:
    """Map product id -> tier letter. Raises on unknown evidence labels."""
    out = {}
    for pid, ev in evidence.items():
        if ev not in EVIDENCE_TIERS:
            raise FanoutError(f"evidence for {pid} must be one of {sorted(EVIDENCE_TIERS)}, got {ev!r}")
        out[pid] = EVIDENCE_TIERS[ev]
    return out


def plan(registry: dict, evidence: dict[str, str], mode: str = "per_product") -> dict:
    """Return the fan-out plan: notifications to open and the non-reportable record."""
    if mode not in FANOUT_MODES:
        raise FanoutError(f"mode must be one of {FANOUT_MODES}")
    by_id = {p["id"]: p for p in registry["products"]}
    unknown = [pid for pid in evidence if pid not in by_id]
    if unknown:
        raise FanoutError(f"unknown products: {unknown}")
    tiers = classify(evidence)
    reportable = [pid for pid, t in tiers.items() if t in ("A", "B")]
    not_reportable = [pid for pid, t in tiers.items() if t == "C"]
    eu27 = registry["eu27"]
    groups = [[pid] for pid in reportable] if mode == "per_product" else ([reportable] if reportable else [])
    notifications = []
    for i, group in enumerate(groups, start=1):
        ms = set()
        for pid in group:
            ms.update(member_states_for(by_id[pid], eu27))
        notifications.append({
            "id": f"N{i}",
            "products": group,
            "member_states": sorted(ms, key=eu27.index),
        })
    return {
        "rule": PACK_RULE_ID,
        "mode": mode,
        "tiers": tiers,
        "reportable": reportable,
        "not_reportable": not_reportable,
        "notifications": notifications,
    }
