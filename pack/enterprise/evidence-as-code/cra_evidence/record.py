"""Build a per-version CRA evidence record from a release directory.

A release directory holds ``release.json`` (the release manifest the pipeline
writes from build metadata) and the evidence artefacts it references. The
builder collects and normalises each artefact, computes digests and returns a
bundle: the schema-conformant record plus the normalised context the gate
needs (build-graph dependencies, provenance subjects, matrix rows).
"""

import datetime as _dt
import os

from . import SCHEMA_VERSION
from . import attest as A
from . import collectors as C
from .digests import digested_item
from .retention import effective_placing_date, retain_until, support_years

PART_I_ITEMS = ["1"] + ["2" + c for c in "abcdefghijklm"]


def _now():
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class Bundle:
    def __init__(self, record, context):
        self.record = record
        self.context = context


def _uri(manifest, rel):
    prefix = (manifest.get("store") or {}).get("uri_prefix")
    pid = manifest["product"]["product_id"]
    ver = manifest["version"]
    if prefix:
        return "%s/%s/%s/%s" % (prefix.rstrip("/"), pid, ver, rel)
    return rel


def build_bundle(release_dir, osv_records=None, kev_ids=None, generated_at=None):
    release_dir = os.path.abspath(release_dir)
    manifest = C.load_json(os.path.join(release_dir, "release.json"))
    ev = manifest.get("evidence") or {}
    ctx = {"errors": [], "missing": [], "manifest": manifest}

    def path_of(rel):
        p = os.path.join(release_dir, rel)
        if not os.path.isfile(p):
            ctx["missing"].append(rel)
            return None
        return p

    def item(rel, ref=None):
        p = path_of(rel) if rel else None
        return digested_item(p, uri=_uri(manifest, rel), ref=ref) if p else None

    # artefact
    art_rel = manifest.get("artefact")
    art = item(art_rel) if art_rel else None
    ctx["artefact_sha256"] = art["digests"]["sha256"] if art else None
    ctx["artefact_digests"] = dict(art["digests"]) if art else {}

    # SBOM
    sbom_rec, sbom_norm = None, None
    if ev.get("sbom") and path_of(ev["sbom"]):
        try:
            sbom_norm = C.normalise_sbom(C.load_json(path_of(ev["sbom"])))
            sbom_rec = item(ev["sbom"])
            sbom_rec.update({
                "format": sbom_norm["format"],
                "spec_version": sbom_norm["spec_version"],
                "component_count": len(sbom_norm["components"]),
                "top_level_dependencies": sbom_norm["top_level_dependencies"],
                "top_level_complete": False,
                "contains_vulnerability_data": sbom_norm["contains_vulnerability_data"],
            })
        except (C.CollectorError, ValueError) as e:
            ctx["errors"].append(("SBOM_UNPARSEABLE", str(e)))
    ctx["sbom"] = sbom_norm
    direct = (manifest.get("build_graph") or {}).get("direct_dependencies") or []
    ctx["build_graph_direct"] = direct
    if sbom_rec is not None:
        have = {n.lower() for n in sbom_norm["top_level_dependencies"]}
        ctx["sbom_missing_top_level"] = sorted(d for d in direct if d.lower() not in have)
        sbom_rec["top_level_complete"] = sbom_norm["top_level_recorded"] and not ctx["sbom_missing_top_level"]

    # provenance (claims only; the gate verifies signatures and re-reads the
    # claims from the verified payload)
    prov_rec, prov_norm = None, None
    ctx["provenance_attestations"] = []
    if ev.get("provenance") and path_of(ev["provenance"]):
        try:
            with open(path_of(ev["provenance"]), "r", encoding="utf-8") as fh:
                text = fh.read()
            prov_norm = C.normalise_provenance(text)
            ctx["provenance_attestations"] = A.load_attestations(text)
            prov_rec = item(ev["provenance"])
            digs = ctx["artefact_digests"]
            match = any((s.get("sha256") and s["sha256"] == digs.get("sha256")) or
                        (s.get("sha512") and s["sha512"] == digs.get("sha512")) for s in prov_norm["subjects"])
            prov_rec.update({
                "format": prov_norm["format"],
                "predicate_type": prov_norm["predicate_type"] or "",
                "builder_id": prov_norm["builder_id"] or "",
                "build_type": prov_norm["build_type"] or "",
                "invocation_id": prov_norm["invocation_id"] or "",
                "subject_digest_match": bool(digs) and match,
            })
        except (C.CollectorError, ValueError) as e:
            ctx["errors"].append(("PROVENANCE_UNPARSEABLE", str(e)))
    ctx["provenance"] = prov_norm

    # VEX + known-vulnerability correlation
    vex_rec, vex_norm = None, None
    ctx["vex_attestations"], ctx["vex_document"] = [], None
    if ev.get("vex") and path_of(ev["vex"]):
        try:
            vdoc = C.load_json(path_of(ev["vex"]))
            embedded = [a for a in A.load_attestations(vdoc) if a.kind != "statement"]
            if embedded:                       # the VEX file is itself a signed attestation
                ctx["vex_attestations"] = embedded
                vdoc = (embedded[0].unverified_statement() or {}).get("predicate") or {}
            ctx["vex_document"] = vdoc
            vex_norm = C.normalise_vex(vdoc)
            vex_rec = item(ev["vex"])
            vex_rec.update({
                "format": vex_norm["format"],
                "statements": [{k: s[k] for k in ("vulnerability", "status", "justification",
                                                  "impact_statement", "action_statement", "components")}
                               for s in vex_norm["statements"]],
            })
        except (C.CollectorError, ValueError) as e:
            ctx["errors"].append(("VEX_UNPARSEABLE", str(e)))
    matches = []
    if sbom_norm is not None and osv_records is not None:
        comps = sbom_norm["components"]
        root = sbom_norm.get("root") or {}
        # The product's own advisories: match the SBOM root (the shipped artefact) as well.
        if root.get("name") and root.get("version") and not any(
                c.get("name") == root["name"] and c.get("version") == root["version"] for c in comps):
            comps = comps + [{"name": root["name"], "version": root["version"], "purl": root.get("purl")}]
        matches = C.match_osv(comps, osv_records, kev_ids or set())
        status_by_vuln = {}
        for s in (vex_norm or {}).get("statements", []):
            status_by_vuln.setdefault(s["vulnerability"], s)
        for m in matches:
            st = None
            for vid in [m["vulnerability"]] + m["aliases"]:
                st = st or status_by_vuln.get(vid)
            m["vex_status"] = st["status"] if st else None
    ctx["vex"] = vex_norm
    ctx["matches"] = matches
    if ev.get("vex_attestation") and path_of(ev["vex_attestation"]):
        try:
            ctx["vex_attestations"] = A.load_attestation_file(path_of(ev["vex_attestation"]))
            if vex_rec is not None:
                vex_rec["attestation"] = item(ev["vex_attestation"])
        except ValueError as e:
            ctx["errors"].append(("VEX_ATTESTATION_UNPARSEABLE", str(e)))
    if vex_rec is not None:
        vex_rec["known_vulnerability_matches"] = matches
        vex_rec["feeds"] = list((manifest.get("feeds") or {}).values()) or ["OSV snapshot", "CISA KEV snapshot"]

    # tests
    tests = []
    for t in ev.get("tests") or []:
        p = path_of(t["path"])
        if not p:
            continue
        try:
            doc = C.load_json(p)
            norm = C.normalise_sarif(doc) if "runs" in doc else C.normalise_test_summary(doc)
            rec = item(t["path"])
            rec.update({"test_type": t["type"], "format": norm["format"],
                        "tool": norm["tool"], "summary": norm["summary"]})
            tests.append(rec)
        except (C.CollectorError, ValueError) as e:
            ctx["errors"].append(("TEST_UNPARSEABLE", "%s: %s" % (t["path"], e)))

    # risk assessment, matrix, Annex II, design note, CVD policy
    def ref_item(key):
        spec = ev.get(key)
        if not spec:
            return None
        return item(spec.get("path"), ref=spec.get("ref") or spec.get("uri"))

    risk = ref_item("risk_assessment")
    matrix = ref_item("applicability_matrix")
    ctx["matrix_rows"] = None
    if matrix:
        try:
            rows = C.load_json(path_of(ev["applicability_matrix"]["path"])).get("items") or []
            ctx["matrix_rows"] = rows
            matrix["items_covered"] = [r.get("item") for r in rows]
            matrix["items_not_applied"] = [r.get("item") for r in rows if r.get("applies") is False]
        except ValueError as e:
            ctx["errors"].append(("MATRIX_UNPARSEABLE", str(e)))
    annex2 = ref_item("annex_ii")
    if annex2 and ev["annex_ii"].get("uri"):
        annex2["ref"] = ev["annex_ii"]["uri"]

    evidence = {
        "sbom": sbom_rec, "provenance": prov_rec, "vulnerability_status": vex_rec,
        "tests": tests, "risk_assessment": risk, "applicability_matrix": matrix,
        "annex_ii_user_information": annex2,
    }
    for opt_key, man_key in (("update_design_note", "update_design_note"), ("cvd_policy", "cvd_policy")):
        it = ref_item(man_key)
        if it:
            evidence[opt_key] = it
    evidence = {k: v for k, v in evidence.items() if v is not None}

    placing = manifest.get("placing") or {}
    sp = manifest.get("support_period") or {}
    sm = manifest.get("substantial_modification") or {}
    ret = None
    eff = effective_placing_date(placing)
    if eff and sp.get("end_date"):
        rule = "Art 13(13): max(placing + 10 years, support period end)"
        if placing.get("date") and eff < effective_placing_date({"date": placing["date"]}):
            rule += "; placing date %s inherited from version %s (guidance para 15, Example 2)" % (
                eff.isoformat(), placing.get("inherited_from_version") or "previously placed")
        ret = {
            "retain_until": retain_until(eff, sp["end_date"]).isoformat(),
            "rule": rule,
            "store_uri": _uri(manifest, ""),
            "object_lock_mode": (manifest.get("store") or {}).get("object_lock_mode", "compliance"),
        }
    record = {
        "schema_version": SCHEMA_VERSION,
        "record_id": "urn:%s:cra-evidence:%s:%s" % (manifest.get("org", "aldermoor"),
                                                   manifest["product"]["product_id"], manifest["version"]),
        "generated_at": generated_at or _now(),
        "product": manifest["product"],
        "version": {
            "version": manifest["version"],
            "release_date": manifest.get("release_date") or placing.get("date"),
            "previous_version": manifest.get("previous_version"),
            "artefact": art,
        },
        "placing_on_market": placing,
        "classification": manifest.get("classification") or {},
        "evidence": evidence,
        "support_period": {
            "end_date": sp.get("end_date"),
            "years": support_years(placing["date"], sp["end_date"]) if placing.get("date") and sp.get("end_date") else 0,
            "justification": sp.get("justification"),
            "latest_version_rule": bool(sp.get("latest_version_rule", False)),
        },
        "substantial_modification": sm,
        "declaration": manifest.get("declaration") or {},
        "signer": manifest.get("signer") or {},
        "retention": ret,
    }
    record = {k: v for k, v in record.items() if v is not None}
    if record["version"]["artefact"] is None:
        del record["version"]["artefact"]
    return Bundle(record, ctx)
