"""Annex VII index generator.

Emits, per version, a JSON and a Markdown index pointing to each evidence
item with its digest, organised by Annex VII point (structure from
reports/guides/application/11-documentation-set.md and
reports/sections/10-conformity.md). Items the pipeline cannot generate
(architecture drawings, production-process description) are listed as
'maintained outside the pipeline' so the gap is explicit.
"""


def _d(item):
    if not item:
        return None
    return {"uri": item["uri"], "ref": item.get("ref"), "sha256": item["digests"]["sha256"],
            "sha512": item["digests"].get("sha512")}


def _vlabel(v):
    if not v:
        return "signature not evaluated"
    if not v.get("verified"):
        return "signature NOT verified"
    s = v.get("signer") or {}
    who = s.get("key") or s.get("san") or "?"
    lvl = " ; SLSA Build L%d" % v["slsa_build_level"] if v.get("slsa_build_level") is not None else ""
    log = " ; Rekor index %s" % (v.get("tlog") or {}).get("log_index") if (v.get("tlog") or {}).get("log_index") else ""
    return "verified %s by %s%s%s" % (v.get("method"), who, lvl, log)


def build_index(record):
    ev = record.get("evidence", {})
    c = record.get("classification", {})
    sp = record.get("support_period", {})
    dec = record.get("declaration", {})
    gate = record.get("gate") or {}
    pts = []

    def add(point, title, items, note=None):
        pts.append({"point": point, "title": title, "items": [i for i in items if i], "note": note})

    art = record["version"].get("artefact")
    add("1", "General description: intended purpose, versions affecting compliance, Annex II information", [
        dict(_d(art), label="Shipped artefact") if art else None,
        dict(_d(ev.get("annex_ii_user_information")), label="Annex II user information")
        if ev.get("annex_ii_user_information") else None,
    ], "Product %s version %s; previous %s" % (record["product"]["product_id"], record["version"]["version"],
                                              record["version"].get("previous_version")))
    add("2(a)", "Design and development; system architecture", [],
        "Maintained outside the pipeline in the product technical file; linked by product id")
    add("2(b)", "Vulnerability handling: SBOM, CVD policy, reporting contact, secure update distribution", [
        dict(_d(ev.get("sbom")), label="SBOM (%s %s)" % (ev["sbom"]["format"], ev["sbom"]["spec_version"]))
        if ev.get("sbom") else None,
        dict(_d(ev.get("vulnerability_status")), label="VEX (%s)" % ev["vulnerability_status"]["format"])
        if ev.get("vulnerability_status") else None,
        dict(_d(ev["vulnerability_status"]["attestation"]), label="Signed VEX attestation (%s)" % _vlabel(
            ev["vulnerability_status"].get("verification")))
        if (ev.get("vulnerability_status") or {}).get("attestation") else None,
        dict(_d(ev.get("cvd_policy")), label="CVD policy") if ev.get("cvd_policy") else None,
        dict(_d(ev.get("update_design_note")), label="Update design note") if ev.get("update_design_note") else None,
    ])
    add("2(c)", "Production and monitoring processes with validation evidence", [
        dict(_d(ev.get("provenance")), label="Build provenance (%s; builder %s; %s)" % (
            ev["provenance"]["predicate_type"], ev["provenance"]["builder_id"],
            _vlabel(ev["provenance"].get("verification")))) if ev.get("provenance") else None,
    ], "Release gate decision: %s under %s" % (gate.get("decision", "not evaluated"), gate.get("policy_id", "-")))
    add("3", "Cybersecurity risk assessment and Annex I Part I applicability", [
        dict(_d(ev.get("risk_assessment")), label="Risk assessment") if ev.get("risk_assessment") else None,
        dict(_d(ev.get("applicability_matrix")), label="Applicability matrix (not applied: %s)" % (
            ", ".join(ev["applicability_matrix"].get("items_not_applied") or []) or "none"))
        if ev.get("applicability_matrix") else None,
    ])
    add("4", "Support period", [], "End %s (%.2f years); justification: %s; latest-version rule (Art 13(10)): %s" % (
        sp.get("end_date"), sp.get("years", 0), sp.get("justification") or "none recorded",
        "yes" if sp.get("latest_version_rule") else "no"))
    add("5", "Harmonised standards, common specifications, certification schemes", [],
        "Route %s; applied in full: %s; certificate %s" % (
            c.get("conformity_route"), ", ".join(c.get("harmonised_standards_applied_in_full") or []) or "none",
            c.get("certificate_ref") or "n/a"))
    add("6", "Test reports against Annex I Parts I and II", [
        dict(_d(t), label="%s (%s; %s)" % (t["test_type"], t.get("tool", ""), ", ".join(
            "%s=%d" % kv for kv in sorted(t["summary"].items())))) for t in ev.get("tests", [])
    ])
    add("7", "EU declaration of conformity", [], "Declaration %s (%s%s) at %s" % (
        dec.get("declaration_id"), dec.get("status"),
        ", from %s" % dec["reused_from_version"] if dec.get("reused_from_version") else "", dec.get("uri")))
    add("8", "SBOM for market surveillance authority on reasoned request", [
        dict(_d(ev.get("sbom")), label="SBOM") if ev.get("sbom") else None])
    return {
        "record_id": record["record_id"],
        "product_id": record["product"]["product_id"],
        "version": record["version"]["version"],
        "placing_date": record["placing_on_market"]["date"],
        "placing_event": record["placing_on_market"].get("event"),
        "inherited_placing_date": record["placing_on_market"].get("inherited_placing_date"),
        "inherited_from_version": record["placing_on_market"].get("inherited_from_version"),
        "retain_until": (record.get("retention") or {}).get("retain_until"),
        "substantial_modification": (record.get("substantial_modification") or {}).get("decision"),
        "points": pts,
    }


def _placing_sentence(idx):
    if idx.get("inherited_placing_date") and idx.get("placing_event") == "update_to_placed_product":
        return ("Version first offered %s; not a new placing, so it keeps placing date %s from version %s "
                "(guidance para 15, Example 2)." % (idx["placing_date"], idx["inherited_placing_date"],
                                                    idx.get("inherited_from_version") or "(not recorded)"))
    if idx.get("placing_event") == "update_to_placed_product":
        return "Version first offered %s as an update to a placed product." % idx["placing_date"]
    return "Placed %s (%s)." % (idx["placing_date"], idx.get("placing_event") or "event not recorded")


def render_markdown(idx):
    lines = [
        "# Annex VII index: %s %s" % (idx["product_id"], idx["version"]),
        "",
        "Record `%s`. %s Retain until %s. Substantial-modification decision: %s." % (
            idx["record_id"], _placing_sentence(idx), idx["retain_until"], idx["substantial_modification"]),
        "",
        "| Annex VII point | Evidence | SHA-256 (first 16) | Location |",
        "|---|---|---|---|",
    ]
    for p in idx["points"]:
        if not p["items"]:
            lines.append("| %s %s | %s | | |" % (p["point"], p["title"], p["note"] or "-"))
        for i, it in enumerate(p["items"]):
            label = it["label"] + (" ; %s" % p["note"] if p["note"] and i == 0 else "")
            lines.append("| %s | %s | `%s` | %s |" % (
                p["point"] if i else "%s %s" % (p["point"], p["title"]), label, it["sha256"][:16], it["uri"]))
    lines.append("")
    return "\n".join(lines)
