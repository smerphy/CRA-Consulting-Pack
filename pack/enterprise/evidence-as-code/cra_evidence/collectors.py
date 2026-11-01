"""Collectors: ingest real-format artefacts and normalise them.

Supported inputs
- SBOM: CycloneDX 1.4-1.6 JSON, SPDX 2.2-2.3 JSON
- Build provenance: in-toto Statement v1 with SLSA Provenance v1 predicate,
  bare, in a DSSE envelope, in a Sigstore bundle, or as JSON Lines
  (.intoto.jsonl). This module only parses claims; the gate verifies the
  signature and re-reads the claims from the verified bytes (attest.py)
- Vulnerability status: OpenVEX v0.2.0, CSAF 2.0 with category csaf_vex
- Tests: SARIF 2.1.0; a small JSON summary for reports that are not SARIF
  (for example a penetration-test PDF)
- Feeds: OSV-format vulnerability records; CISA KEV catalogue JSON
"""

import base64
import json
import re


class CollectorError(ValueError):
    """Raised when an artefact is not in the expected format."""


def load_json(path):
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


# ---------------------------------------------------------------- SBOM

def _purl_name(purl):
    """Return the package name from a purl (without namespace/version)."""
    if not purl or not purl.startswith("pkg:"):
        return None
    body = purl[4:].split("?")[0].split("#")[0]
    body = body.split("@")[0]
    return body.split("/")[-1].lower()


def normalise_sbom(doc):
    """Detect CycloneDX or SPDX JSON and return a normalised dict.

    Returns keys: format, spec_version, root (name, version, sha256),
    components (list of name, version, purl, hashes), top_level_dependencies
    (component names), top_level_recorded (bool: root has dependency edges),
    contains_vulnerability_data (bool).
    """
    if doc.get("bomFormat") == "CycloneDX":
        return _normalise_cyclonedx(doc)
    if str(doc.get("spdxVersion", "")).startswith("SPDX-"):
        return _normalise_spdx(doc)
    raise CollectorError("not a CycloneDX or SPDX JSON document")


def _normalise_cyclonedx(doc):
    spec = str(doc.get("specVersion", ""))
    if spec not in ("1.4", "1.5", "1.6", "1.7"):
        raise CollectorError("unsupported CycloneDX specVersion %r" % spec)
    meta_comp = (doc.get("metadata") or {}).get("component") or {}
    root_ref = meta_comp.get("bom-ref")
    by_ref = {}
    components = []
    for comp in doc.get("components") or []:
        hashes = {h.get("alg", "").upper().replace("-", ""): h.get("content")
                  for h in comp.get("hashes") or []}
        item = {
            "ref": comp.get("bom-ref"),
            "name": comp.get("name"),
            "version": comp.get("version"),
            "purl": comp.get("purl"),
            "hashes": hashes,
        }
        components.append(item)
        if item["ref"]:
            by_ref[item["ref"]] = item
    top = []
    recorded = False
    for dep in doc.get("dependencies") or []:
        if root_ref and dep.get("ref") == root_ref:
            recorded = True
            for r in dep.get("dependsOn") or []:
                top.append(by_ref.get(r, {}).get("name") or r)
    root_hashes = {h.get("alg", "").upper().replace("-", ""): h.get("content")
                   for h in meta_comp.get("hashes") or []}
    return {
        "format": "CycloneDX",
        "spec_version": spec,
        "root": {"name": meta_comp.get("name"), "version": meta_comp.get("version"),
                 "purl": meta_comp.get("purl"), "sha256": root_hashes.get("SHA256")},
        "components": components,
        "top_level_dependencies": sorted(set(top)),
        "top_level_recorded": recorded and bool(top),
        "contains_vulnerability_data": bool(doc.get("vulnerabilities")),
    }


_SPDX_FORWARD = {"DEPENDS_ON", "CONTAINS", "STATIC_LINK", "DYNAMIC_LINK", "HAS_PREREQUISITE"}
_SPDX_REVERSE = {"DEPENDENCY_OF", "CONTAINED_BY", "PREREQUISITE_FOR"}


def _normalise_spdx(doc):
    spec = doc["spdxVersion"].split("-", 1)[1]
    if spec not in ("2.2", "2.3"):
        raise CollectorError("unsupported SPDX version %r (2.2/2.3 JSON supported)" % spec)
    pkgs = {}
    components = []
    for p in doc.get("packages") or []:
        purl = None
        for ref in p.get("externalRefs") or []:
            if ref.get("referenceType") == "purl":
                purl = ref.get("referenceLocator")
        hashes = {c.get("algorithm", "").upper().replace("-", ""): c.get("checksumValue")
                  for c in p.get("checksums") or []}
        item = {"ref": p.get("SPDXID"), "name": p.get("name"),
                "version": p.get("versionInfo"), "purl": purl, "hashes": hashes}
        pkgs[item["ref"]] = item
    rels = doc.get("relationships") or []
    described = list(doc.get("documentDescribes") or [])
    for r in rels:
        if r.get("spdxElementId") == "SPDXRef-DOCUMENT" and r.get("relationshipType") == "DESCRIBES":
            described.append(r.get("relatedSpdxElement"))
    root_id = described[0] if described else None
    for ref, item in pkgs.items():
        if ref != root_id:
            components.append(item)
    top = []
    for r in rels:
        rt = r.get("relationshipType")
        if rt in _SPDX_FORWARD and r.get("spdxElementId") == root_id:
            top.append(pkgs.get(r.get("relatedSpdxElement"), {}).get("name") or r.get("relatedSpdxElement"))
        elif rt in _SPDX_REVERSE and r.get("relatedSpdxElement") == root_id:
            top.append(pkgs.get(r.get("spdxElementId"), {}).get("name") or r.get("spdxElementId"))
    root = pkgs.get(root_id, {})
    return {
        "format": "SPDX",
        "spec_version": spec,
        "root": {"name": root.get("name"), "version": root.get("version"),
                 "sha256": (root.get("hashes") or {}).get("SHA256")},
        "components": components,
        "top_level_dependencies": sorted(set(top)),
        "top_level_recorded": bool(top),
        "contains_vulnerability_data": False,
    }


# ---------------------------------------------------------- provenance

STATEMENT_TYPES = ("https://in-toto.io/Statement/v1", "https://in-toto.io/Statement/v0.1")
SLSA_V1 = "https://slsa.dev/provenance/v1"


def normalise_provenance(doc):
    """Normalise an in-toto Statement carrying SLSA v1 provenance.

    Accepts a bare Statement, a DSSE envelope, a Sigstore bundle, an npm
    attestations response, JSON text or JSON Lines. Does NOT verify
    signatures: the values returned are claims until attest.verify() has
    checked them, and the gate uses only the verified statement.
    """
    from . import attest as A
    if isinstance(doc, dict) and "payloadType" in doc and doc.get("payloadType") != A.INTOTO:
        raise CollectorError("DSSE payloadType is not in-toto")
    try:
        atts = A.load_attestations(doc)
    except ValueError as e:
        raise CollectorError("provenance is not parseable JSON or JSON Lines: %s" % e)
    if not atts:
        raise CollectorError("not an in-toto Statement, DSSE envelope or Sigstore bundle")
    att = A.select(atts, (SLSA_V1,))
    if att.kind != "statement" and att.payload_type != A.INTOTO:
        raise CollectorError("DSSE payloadType is not in-toto")
    return _statement_claims(att.unverified_statement() or {}, att.kind != "statement", att.kind)


def _statement_claims(doc, signed=False, envelope="statement"):
    if doc.get("_type") not in STATEMENT_TYPES:
        raise CollectorError("not an in-toto Statement")
    pred = doc.get("predicate") or {}
    run = pred.get("runDetails") or {}
    bdef = pred.get("buildDefinition") or {}
    meta = run.get("metadata") or {}
    subjects = [{"name": s.get("name"), "sha256": (s.get("digest") or {}).get("sha256"),
                 "sha512": (s.get("digest") or {}).get("sha512")}
                for s in doc.get("subject") or []]
    return {
        "format": "in-toto Statement v1 / SLSA Provenance v1" if doc.get("predicateType") == SLSA_V1
                  else "in-toto Statement",
        "predicate_type": doc.get("predicateType"),
        "builder_id": (run.get("builder") or {}).get("id"),
        "build_type": bdef.get("buildType"),
        "external_parameters": bdef.get("externalParameters") or {},
        "invocation_id": meta.get("invocationId"),
        "started_on": meta.get("startedOn"),
        "finished_on": meta.get("finishedOn"),
        "subjects": subjects,
        "resolved_dependencies": [d.get("uri") for d in bdef.get("resolvedDependencies") or []],
        "dsse_envelope": signed,
        "envelope": envelope,
    }


# ----------------------------------------------------------------- VEX

OPENVEX_STATUSES = {"not_affected", "affected", "fixed", "under_investigation"}


def normalise_vex(doc):
    """OpenVEX or CSAF VEX. An in-toto Statement wrapping one (predicate) is unwrapped."""
    if doc.get("_type") in STATEMENT_TYPES and isinstance(doc.get("predicate"), dict):
        doc = doc["predicate"]
    ctx = str(doc.get("@context", ""))
    if ctx.startswith("https://openvex.dev/ns"):
        return _normalise_openvex(doc)
    if (doc.get("document") or {}).get("category") == "csaf_vex":
        return _normalise_csaf(doc)
    raise CollectorError("not an OpenVEX or CSAF VEX document")


def _normalise_openvex(doc):
    out = []
    for st in doc.get("statements") or []:
        status = st.get("status")
        if status not in OPENVEX_STATUSES:
            raise CollectorError("invalid OpenVEX status %r" % status)
        vuln = st.get("vulnerability")
        if isinstance(vuln, dict):
            vuln = vuln.get("name") or vuln.get("@id")
        comps, prods = [], []
        for p in st.get("products") or []:
            pid = p.get("@id") if isinstance(p, dict) else p
            prods.append(pid)
            for sc in (p.get("subcomponents") if isinstance(p, dict) else None) or []:
                comps.append(sc.get("@id") if isinstance(sc, dict) else sc)
        out.append({
            "vulnerability": vuln,
            "status": status,
            "justification": st.get("justification"),
            "impact_statement": st.get("impact_statement"),
            "action_statement": st.get("action_statement"),
            "components": comps,
            "products": prods,
        })
    return {"format": "OpenVEX", "statements": out}


_CSAF_STATUS = {
    "known_not_affected": "not_affected",
    "known_affected": "affected",
    "fixed": "fixed",
    "first_fixed": "fixed",
    "under_investigation": "under_investigation",
}


def _csaf_products(tree):
    names = {}

    def walk(node):
        for fpn in node.get("full_product_names") or []:
            names[fpn.get("product_id")] = fpn.get("name")
        if "product" in node:
            p = node["product"]
            names[p.get("product_id")] = p.get("name")
        for b in node.get("branches") or []:
            walk(b)
    walk(tree or {})
    for rel in (tree or {}).get("relationships") or []:
        fpn = rel.get("full_product_name") or {}
        names[fpn.get("product_id")] = fpn.get("name")
    return names


def _normalise_csaf(doc):
    names = _csaf_products(doc.get("product_tree"))
    out = []
    for v in doc.get("vulnerabilities") or []:
        vid = v.get("cve") or ((v.get("ids") or [{}])[0].get("text"))
        flags = {}
        for f in v.get("flags") or []:
            for pid in f.get("product_ids") or []:
                flags[pid] = f.get("label")
        threats = {}
        for t in v.get("threats") or []:
            if t.get("category") == "impact":
                for pid in t.get("product_ids") or []:
                    threats[pid] = t.get("details")
        actions = {}
        for r in v.get("remediations") or []:
            for pid in r.get("product_ids") or []:
                actions[pid] = r.get("details")
        for key, status in _CSAF_STATUS.items():
            for pid in (v.get("product_status") or {}).get(key) or []:
                out.append({
                    "vulnerability": vid,
                    "status": status,
                    "justification": flags.get(pid),
                    "impact_statement": threats.get(pid),
                    "action_statement": actions.get(pid),
                    "components": [],
                    "products": [names.get(pid, pid)],
                })
    return {"format": "CSAF-VEX", "statements": out}


# --------------------------------------------------------------- tests

def normalise_sarif(doc):
    if str(doc.get("version")) != "2.1.0":
        raise CollectorError("SARIF version must be 2.1.0")
    counts = {"error": 0, "warning": 0, "note": 0, "suppressed": 0}
    tools = []
    for run in doc.get("runs") or []:
        driver = ((run.get("tool") or {}).get("driver") or {})
        tools.append(driver.get("name"))
        for res in run.get("results") or []:
            sups = res.get("suppressions") or []
            if any(s.get("status", "accepted") == "accepted" for s in sups):
                counts["suppressed"] += 1
                continue
            level = res.get("level", "warning")
            if level == "none":
                level = "note"
            counts[level] = counts.get(level, 0) + 1
    return {"format": "SARIF", "tool": ", ".join(t for t in tools if t), "summary": counts}


def normalise_test_summary(doc):
    """Non-SARIF report summary (for example a penetration-test PDF)."""
    if doc.get("format") != "test-summary/v1":
        raise CollectorError("unknown test summary format")
    f = doc.get("findings") or {}
    return {"format": "summary", "tool": doc.get("tool", ""),
            "summary": {"critical": int(f.get("critical", 0)), "high": int(f.get("high", 0))}}


# --------------------------------------------------------------- feeds

def load_kev(doc):
    """CISA KEV catalogue JSON -> set of CVE ids."""
    return {v.get("cveID") for v in doc.get("vulnerabilities") or [] if v.get("cveID")}


def _vkey(v):
    parts = re.split(r"[.\-+_]", str(v).lstrip("vV"))
    key = []
    for p in parts:
        key.append((0, int(p), "") if p.isdigit() else (1, 0, p))
    return tuple(key)


def version_in_range(version, events):
    """OSV ECOSYSTEM/SEMVER range events -> True if version is affected."""
    v = _vkey(version)
    affected = False

    def order(ev):
        val = next(iter(ev.values()))
        return () if val == "0" else _vkey(val)

    for ev in sorted(events, key=order):
        if "introduced" in ev:
            if ev["introduced"] == "0" or v >= _vkey(ev["introduced"]):
                affected = True
        if "fixed" in ev and v >= _vkey(ev["fixed"]):
            affected = False
        if "last_affected" in ev and v > _vkey(ev["last_affected"]):
            affected = False
    return affected


_OSV_INDEX = {"records": None, "index": None}


def index_osv(osv_records):
    """Index OSV records by lower-case package name and purl name (built once per feed)."""
    if _OSV_INDEX["records"] is osv_records:
        return _OSV_INDEX["index"]
    idx = {}
    for ri, rec in enumerate(osv_records):
        for aff in rec.get("affected") or []:
            pkg = aff.get("package") or {}
            for n in {(pkg.get("name") or "").lower(), _purl_name(pkg.get("purl"))}:
                if n:
                    idx.setdefault(n, []).append((ri, rec, aff))
    _OSV_INDEX.update(records=osv_records, index=idx)
    return idx


def match_osv(components, osv_records, kev_ids):
    """Match SBOM components against OSV records by package name and version.

    Uses a name index so cost grows with SBOM size, not feed size; output
    order is feed order, then component order (same as a nested scan).
    """
    idx = index_osv(osv_records)
    found = {}
    for ci, comp in enumerate(components):
        if not comp.get("version"):
            continue
        names = {(comp.get("name") or "").lower(), _purl_name(comp.get("purl"))}
        seen = set()
        for n in names:
            for ri, rec, aff in idx.get(n, ()):
                key = (ri, id(aff))
                if key in seen:
                    continue
                seen.add(key)
                for rng in aff.get("ranges") or []:
                    if version_in_range(comp["version"], rng.get("events") or []):
                        ids = [rec.get("id")] + list(rec.get("aliases") or [])
                        cve = next((i for i in ids if i and i.startswith("CVE-")), rec.get("id"))
                        sev = (rec.get("database_specific") or {}).get("severity")
                        found[(ri, ci, id(aff))] = {
                            "vulnerability": cve,
                            "aliases": [i for i in ids if i and i != cve],
                            "component": "%s@%s" % (comp["name"], comp["version"]),
                            "severity": sev.lower() if sev else None,
                            "known_exploited": any(i in kev_ids for i in ids),
                        }
                        break
    return [found[k] for k in sorted(found, key=lambda k: (k[0], k[1]))]
