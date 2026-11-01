"""Generate the sample releases deterministically.

Aldermoor Platforms is fictional. Component names are real open-source
projects; component versions, digests and URLs are synthetic. Signatures
are REAL cryptographic signatures made with demonstration keys generated
by this script (examples/keys/*.demo-private.pem). The private keys are
committed only so the examples and tests are reproducible; a production
signing key never leaves its KMS/HSM.
Vulnerability identifiers (CVE-2022-37434 zlib, CVE-2023-4863 libwebp) are
real public identifiers used on synthetic component versions for
illustration. Feed files are illustrative excerpts with simplified ranges.

Run: python examples/make_examples.py   (from the module root)
"""

import base64
import hashlib
import json
import os
import sys

from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from cra_evidence import attest as A  # noqa: E402

KEYS = os.path.join(HERE, "keys")
BUILD_KEY = "aldermoor-build-provenance-2027"     # ECDSA P-256, held by the hermetic builder's signing service
PSIRT_KEY = "aldermoor-psirt-vex-2027"            # Ed25519, held by the PSIRT VEX publishing service
OPENVEX_PT = "https://openvex.dev/ns/v0.2.0"
CSAF_PT = "https://aldermoor.example/attestation/csaf-vex/v2.0"
REL = os.path.join(HERE, "releases")
BUILDER = "https://build.aldermoor.example/hermetic/v2"
STORE = "s3://aldermoor-cra-evidence-eu/v1"


def blob(label, size=32768):
    out, seed = b"", label.encode()
    while len(out) < size:
        seed = hashlib.sha256(seed).digest()
        out += seed
    return out[:size]


def sha256(b):
    return hashlib.sha256(b).hexdigest()


def sha512(b):
    return hashlib.sha512(b).hexdigest()


def write(path, data):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    mode = "wb" if isinstance(data, bytes) else "w"
    with open(path, mode, **({} if mode == "wb" else {"encoding": "utf-8"})) as fh:
        if isinstance(data, (dict, list)):
            fh.write(json.dumps(data, indent=2) + "\n")
        else:
            fh.write(data)


# --------------------------------------------------------------- feeds

def feeds():
    osv = {"vulns": [
        {"schema_version": "1.6.0", "id": "CVE-2022-37434", "aliases": [],
         "summary": "zlib inflateGetHeader heap-based buffer over-read or overflow via large gzip header extra field",
         "affected": [{"package": {"ecosystem": "GIT", "name": "zlib", "purl": "pkg:generic/zlib"},
                       "ranges": [{"type": "ECOSYSTEM", "events": [{"introduced": "0"}, {"fixed": "1.2.13"}]}]}],
         "database_specific": {"severity": "CRITICAL", "note": "illustrative excerpt; ranges simplified"}},
        {"schema_version": "1.6.0", "id": "CVE-2023-4863", "aliases": [],
         "summary": "libwebp heap buffer overflow in lossless decoding (Huffman table construction)",
         "affected": [{"package": {"ecosystem": "GIT", "name": "libwebp", "purl": "pkg:generic/libwebp"},
                       "ranges": [{"type": "ECOSYSTEM", "events": [{"introduced": "0"}, {"fixed": "1.3.2"}]}]}],
         "database_specific": {"severity": "HIGH", "note": "illustrative excerpt; ranges simplified"}},
        {"schema_version": "1.6.0", "id": "CVE-2024-23170", "aliases": [],
         "summary": "Mbed TLS timing side channel in RSA private operation",
         "affected": [{"package": {"ecosystem": "GIT", "name": "mbedtls", "purl": "pkg:generic/mbedtls"},
                       "ranges": [{"type": "ECOSYSTEM", "events": [{"introduced": "3.0.0"}, {"fixed": "3.5.2"}]}]}],
         "database_specific": {"severity": "MEDIUM", "note": "illustrative excerpt; ranges simplified"}},
    ]}
    kev = {"title": "CISA Catalog of Known Exploited Vulnerabilities (illustrative excerpt)",
           "catalogVersion": "2026.10.30", "dateReleased": "2026-10-30T00:00:00.000Z", "count": 1,
           "vulnerabilities": [{"cveID": "CVE-2023-4863", "vendorProject": "Google", "product": "Chromium WebP",
                                "vulnerabilityName": "Google Chromium WebP Heap-Based Buffer Overflow Vulnerability",
                                "dateAdded": "2023-09-13", "requiredAction": "Apply mitigations per vendor instructions.",
                                "knownRansomwareCampaignUse": "Unknown"}]}
    write(os.path.join(HERE, "feeds", "osv-snapshot.json"), osv)
    write(os.path.join(HERE, "feeds", "kev-snapshot.json"), kev)


# ---------------------------------------------------------------- keys

def private_key(name):
    """Load or create a demonstration signing key (persisted for reproducibility)."""
    path = os.path.join(KEYS, name + ".demo-private.pem")
    if not os.path.exists(path):
        key = ec.generate_private_key(ec.SECP256R1()) if name == BUILD_KEY else ed25519.Ed25519PrivateKey.generate()
        write(path, key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                      serialization.NoEncryption()))
    with open(path, "rb") as fh:
        return serialization.load_pem_private_key(fh.read(), password=None)


def public_pem(name):
    return private_key(name).public_key().public_bytes(
        serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode("ascii")


def sign(statement, key_name):
    k = private_key(key_name)
    return A.sign_envelope(statement, k, keyid=A.keyid_for(k.public_key()))


def key_entry(name, algorithm, purposes, owner):
    pub = private_key(name).public_key()
    return {"algorithm": algorithm, "keyid": A.keyid_for(pub), "public_key_pem": public_pem(name),
            "owner": owner, "purposes": purposes, "status": "active",
            "not_before": "2026-01-01T00:00:00Z", "not_after": "2030-12-31T23:59:59Z",
            "custody": "Cloud KMS/HSM, non-exportable; this demonstration key is file-based (examples/keys)"}


def trust_policy():
    lock_ext = {"target": {"pattern": r"//firmware/hearth/lock3:signed_image"},
                "source": {"pattern": r"git\+https://monorepo\.aldermoor\.example/monorepo@refs/tags/hearth-lock-3/.+"}}
    lb_ext = {"target": {"pattern": r"//lumen/browser:release_linux_x64"},
              "source": {"pattern": r"git\+https://monorepo\.aldermoor\.example/monorepo@refs/tags/lumen-browser/.+"}}

    def product(ext):
        return {"provenance": {"keys": [BUILD_KEY], "builder_ids": [BUILDER], "min_slsa_build_level": 3,
                               "build_types": ["https://build.aldermoor.example/buildtypes/hermetic-bazel/v1"],
                               "external_parameters": ext},
                "vex": {"keys": [PSIRT_KEY]}}
    return {
        "trust_policy_id": "aldermoor-attestation-trust/1.0.0",
        "description": "Who may sign what. SLSA levels are the verifier's assessment of each builder, "
                       "not claims read from provenance (SLSA v1.0 'Verifying artifacts' step 1).",
        "require_signed_provenance": True,
        "require_signed_vex": True,
        "min_slsa_build_level": 3,
        "keys": {
            BUILD_KEY: key_entry(BUILD_KEY, "ecdsa-p256-sha256", ["provenance"], "Developer Infrastructure (build platform)"),
            PSIRT_KEY: key_entry(PSIRT_KEY, "ed25519", ["vex"], "Product Security Incident Response Team"),
        },
        "revoked_keyids": [],
        "builders": {
            BUILDER: {"slsa_build_level": 3, "hosted": True, "isolated": True, "signing_key_isolated": True,
                      "signers": ["key:" + BUILD_KEY],
                      "basis": "Internal assessment against SLSA v1.0 Build L3 requirements (illustrative ref "
                               "SLSA-ASSESS-2027-04); re-assessed annually"},
        },
        "sigstore": {"trusted_root": "trust/sigstore-public-good.trusted_root.json"},
        "products": {"hearth-lock-3": product(lock_ext), "lumen-browser": product(lb_ext)},
    }


def policy():
    write(os.path.join(HERE, "policy", "aldermoor-gate-policy.json"), {
        "policy_id": "aldermoor-cra-gate/1.1.0",
        "description": "Release gate policy for EU-placed Aldermoor products (illustrative).",
        "trusted_builders": [BUILDER],
        "accepted_predicate_types": ["https://slsa.dev/provenance/v1"],
        "min_support_years": 5,
        "fail_untriaged_severities": ["critical", "high"],
        "required_tests": {"default": ["sast"],
                           "products": {"hearth-lock-3": ["sast", "fuzz"], "lumen-browser": ["sast", "fuzz"]}},
        "pentest_required_on": ["first_placing", "substantial"],
        "sarif_fail_level": "error",
        "harmonised_standards_cited": [],
        "required_matrix_items": ["1"] + ["2" + c for c in "abcdefghijklm"],
        "accepted_vex_predicate_types": [OPENVEX_PT, "https://openvex.dev/ns", CSAF_PT],
        "attestation_trust": trust_policy(),
    })


# ----------------------------------------------------------- artefacts

def cyclonedx(name, version, art, comps, root_deps, extra_deps):
    ref = "pkg:generic/aldermoor/%s@%s" % (name, version)
    components = []
    for n, v, purl, supplier in comps:
        b = blob("%s-%s" % (n, v), 256)
        components.append({
            "type": "library", "bom-ref": "%s@%s" % (n, v), "supplier": {"name": supplier},
            "name": n, "version": v, "purl": purl,
            "hashes": [{"alg": "SHA-512", "content": sha512(b)}],
            "properties": [{"name": "bsi:dependencies:complete", "value": "true"}],
        })
    byname = {c["name"]: c["bom-ref"] for c in components}
    deps = [{"ref": ref, "dependsOn": [byname[d] for d in root_deps]}]
    for parent, children in extra_deps.items():
        deps.append({"ref": byname[parent], "dependsOn": [byname[c] for c in children]})
    return {
        "bomFormat": "CycloneDX", "specVersion": "1.5", "version": 1,
        "serialNumber": "urn:uuid:%s" % _uuid(name + version),
        "metadata": {
            "timestamp": "2028-01-11T09:14:02Z",
            "tools": {"components": [{"type": "application", "name": "aldermoor-sbomgen", "version": "3.2.0"}]},
            "authors": [{"name": "Aldermoor Build Engineering", "email": "sbom@aldermoor.example"}],
            "component": {"type": "firmware", "bom-ref": ref, "name": name, "version": version,
                          "supplier": {"name": "Aldermoor Platforms"},
                          "hashes": [{"alg": "SHA-256", "content": sha256(art)}]},
        },
        "components": components,
        "dependencies": deps,
    }


def spdx(name, version, art, pkgs, root_deps):
    root = "SPDXRef-Package-%s" % name
    packages = [{
        "SPDXID": root, "name": name, "versionInfo": version, "supplier": "Organization: Aldermoor Platforms",
        "downloadLocation": "NOASSERTION", "filesAnalyzed": False,
        "checksums": [{"algorithm": "SHA256", "checksumValue": sha256(art)}],
        "externalRefs": [{"referenceCategory": "PACKAGE-MANAGER", "referenceType": "purl",
                          "referenceLocator": "pkg:generic/aldermoor/%s@%s" % (name, version)}],
    }]
    rels = [{"spdxElementId": "SPDXRef-DOCUMENT", "relationshipType": "DESCRIBES", "relatedSpdxElement": root}]
    for n, v, lic in pkgs:
        sid = "SPDXRef-Package-%s" % n
        packages.append({
            "SPDXID": sid, "name": n, "versionInfo": v, "downloadLocation": "NOASSERTION",
            "filesAnalyzed": False, "licenseConcluded": lic,
            "checksums": [{"algorithm": "SHA512", "checksumValue": sha512(blob(n + v, 256))}],
            "externalRefs": [{"referenceCategory": "PACKAGE-MANAGER", "referenceType": "purl",
                              "referenceLocator": "pkg:generic/%s@%s" % (n, v)}],
        })
        if n in root_deps:
            rels.append({"spdxElementId": root, "relationshipType": "DEPENDS_ON", "relatedSpdxElement": sid})
    return {
        "spdxVersion": "SPDX-2.3", "dataLicense": "CC0-1.0", "SPDXID": "SPDXRef-DOCUMENT",
        "name": "%s-%s" % (name, version),
        "documentNamespace": "https://sbom.aldermoor.example/spdx/%s/%s" % (name, version),
        "creationInfo": {"created": "2028-01-30T06:02:11Z",
                         "creators": ["Organization: Aldermoor Platforms", "Tool: aldermoor-sbomgen-3.2.0"]},
        "packages": packages, "relationships": rels,
    }


def _uuid(s):
    h = sha256(s.encode())
    return "%s-%s-%s-%s-%s" % (h[:8], h[8:12], h[12:16], h[16:20], h[20:32])


def provenance(target, artname, art, tag, builder=BUILDER):
    st = {
        "_type": "https://in-toto.io/Statement/v1",
        "subject": [{"name": artname, "digest": {"sha256": sha256(art)}}],
        "predicateType": "https://slsa.dev/provenance/v1",
        "predicate": {
            "buildDefinition": {
                "buildType": "https://build.aldermoor.example/buildtypes/hermetic-bazel/v1",
                "externalParameters": {"target": target,
                                       "source": "git+https://monorepo.aldermoor.example/monorepo@refs/tags/%s" % tag},
                "internalParameters": {"remote_execution_pool": "eu-hermetic-prod", "sandbox": "hermetic"},
                "resolvedDependencies": [{"uri": "git+https://monorepo.aldermoor.example/monorepo@refs/tags/%s" % tag,
                                          "digest": {"gitCommit": sha256(tag.encode())[:40]}}],
            },
            "runDetails": {
                "builder": {"id": builder, "version": {"hermetic-bazel": "8.1.0-ald.4"}},
                "metadata": {"invocationId": "inv-%s" % sha256(tag.encode())[:16],
                             "startedOn": "2028-01-11T08:51:40Z", "finishedOn": "2028-01-11T09:13:55Z"},
            },
        },
    }
    return sign(st, BUILD_KEY)


def vex_attestation(vex_doc, artname, art, predicate_type):
    st = {"_type": "https://in-toto.io/Statement/v1",
          "subject": [{"name": artname, "digest": {"sha256": sha256(art)}}],
          "predicateType": predicate_type, "predicate": vex_doc}
    return sign(st, PSIRT_KEY)


def sign_release(d):
    """Re-sign a release directory's attestations after its evidence changed.

    Used by tests that mutate VEX or provenance content to exercise gate
    logic on correctly signed evidence. Subjects are kept as they were, so a
    tampered artefact still fails the digest binding.
    """
    m = json.load(open(os.path.join(d, "release.json")))
    ev = m.get("evidence") or {}
    p = os.path.join(d, ev.get("provenance") or "-")
    if os.path.isfile(p):
        atts = A.load_attestation_file(p)
        if atts:
            write(p, sign(atts[0].unverified_statement(), BUILD_KEY))
    v, va = os.path.join(d, ev.get("vex") or "-"), os.path.join(d, ev.get("vex_attestation") or "-")
    if os.path.isfile(v) and os.path.isfile(va):
        old = A.load_attestation_file(va)[0].unverified_statement()
        old["predicate"] = json.load(open(v))
        write(va, sign(old, PSIRT_KEY))


def sarif(tool, results):
    return {"$schema": "https://json.schemastore.org/sarif-2.1.0.json", "version": "2.1.0",
            "runs": [{"tool": {"driver": {"name": tool, "rules": [{"id": r[0]} for r in results]}},
                      "results": [dict({"ruleId": r[0], "level": r[1], "message": {"text": r[2]},
                                        "locations": [{"physicalLocation": {"artifactLocation": {"uri": r[3]}}}]},
                                       **({"suppressions": [{"kind": "external", "status": "accepted",
                                                             "justification": r[4]}]} if len(r) > 4 else {}))
                                  for r in results]}]}


def matrix(product, overrides=None):
    titles = {"1": "Appropriate level of cybersecurity based on the risks", "2a": "No known exploitable vulnerabilities",
              "2b": "Secure by default; reset", "2c": "Security updates; automatic by default",
              "2d": "Protection from unauthorised access", "2e": "Confidentiality", "2f": "Integrity",
              "2g": "Data minimisation", "2h": "Availability of essential functions", "2i": "Minimise impact on other networks",
              "2j": "Limit attack surface", "2k": "Exploitation mitigation", "2l": "Logging and monitoring, user opt-out",
              "2m": "Secure data removal and transfer"}
    rows = []
    for k, t in titles.items():
        row = {"item": k, "title": t, "applies": True, "implementation": "See risk assessment section %s" % k}
        row.update((overrides or {}).get(k, {}))
        rows.append(row)
    return {"product_id": product, "basis": "Art 13(3)-(4); Annex I Part I", "items": rows}


def common_docs(d, product, version, extra=""):
    write(os.path.join(d, "docs", "risk-assessment.md"),
          "# Cybersecurity risk assessment: %s %s\n\nArt 13(2)-(4) assessment (sample stub). Threat model, data flows, "
          "evaluated and accepted risks, residual-risk treatment.%s\n" % (product, version, extra))
    write(os.path.join(d, "docs", "annex-ii-user-information.md"),
          "# Security information for %s %s\n\nAnnex II points 1-9 (sample stub). Manufacturer: Aldermoor Platforms "
          "(fictional). Vulnerability contact: security@aldermoor.example. Declaration: see release.json uri.\n"
          % (product, version))
    write(os.path.join(d, "docs", "update-design-note.md"),
          "# Update design note: %s\n\nSigned images, anti-rollback counter, A/B slots, staged rollout (sample stub).\n"
          % product)
    write(os.path.join(d, "docs", "cvd-policy.md"),
          "# Coordinated vulnerability disclosure policy (sample stub)\n\nSee https://www.aldermoor.example/.well-known/security.txt\n")


def manifest(product, version, prev, release_date, placing, classification, artefact, direct, evidence,
             support, sm, decl, tests):
    ev = {"sbom": evidence[0], "provenance": evidence[1], "vex": evidence[2],
          "vex_attestation": evidence[2].replace(".json", ".intoto.json"),
          "tests": [{"type": t, "path": p} for t, p in tests],
          "risk_assessment": {"path": "docs/risk-assessment.md", "ref": "RA-%s-%s" % (product["product_id"], version)},
          "applicability_matrix": {"path": "docs/applicability-matrix.json",
                                   "ref": "AM-%s-%s" % (product["product_id"], version)},
          "annex_ii": {"path": "docs/annex-ii-user-information.md",
                       "uri": "https://www.aldermoor.example/security/%s/%s/" % (product["product_id"], version)},
          "update_design_note": {"path": "docs/update-design-note.md", "ref": "UDN-%s" % product["product_id"]},
          "cvd_policy": {"path": "docs/cvd-policy.md", "ref": "https://www.aldermoor.example/security/cvd"}}
    return {
        "manifest_version": "1.0", "org": "aldermoor", "product": product, "version": version,
        "previous_version": prev, "release_date": release_date, "placing": placing,
        "classification": classification, "artefact": artefact,
        "build_graph": {"direct_dependencies": direct,
                        "source": "hermetic build graph query: direct deps of the release target"},
        "evidence": ev, "support_period": support, "substantial_modification": sm, "declaration": decl,
        "signer": {"identity": "spiffe://aldermoor.example/release-pipeline/%s" % product["product_id"],
                   "role": "Release manager (accountable); pipeline identity signs",
                   "signature_ref": "DSSE envelopes: provenance key %s, VEX key %s" % (BUILD_KEY, PSIRT_KEY)},
        "store": {"uri_prefix": STORE, "object_lock_mode": "compliance"},
        "feeds": {"osv": "OSV snapshot 2026-10-30 (excerpt)", "kev": "CISA KEV 2026.10.30 (excerpt)"},
    }


LOCK = {"product_id": "hearth-lock-3", "name": "Hearth Lock 3 smart door lock (firmware)",
        "manufacturer": "Aldermoor Platforms (fictional)", "product_type": "hardware_with_software",
        "family": "Hearth Lock 3", "variants": ["HL3-STD", "HL3-PRO"]}
LOCK_CLASS = {"class": "important_class_i",
              "annex_category": "Annex III Class I, 17: smart home products with security functionalities (smart door locks)",
              "conformity_route": "module_h", "harmonised_standards_applied_in_full": [],
              "notified_body": "Illustrative notified body (no CRA body designated at 8 Sep 2026)",
              "certificate_ref": "QS-APPROVAL-ILLUSTRATIVE-0142"}
LOCK_SUPPORT = {"end_date": "2039-12-31", "latest_version_rule": False,
                "justification": "Expected time in use of door-lock hardware exceeds 10 years; reasonable user expectations for a building fixture."}


def lock_release(version, prev, release_date, placing_date, comps, root_deps, vex_statements, sm, tests_extra=None,
                 decl_status="reused"):
    d = os.path.join(REL, "hearth-lock-3_%s" % version)
    art = blob("hearth-lock-3-fw-%s" % version)
    artname = "hearth-lock-3-fw-%s.bin" % version
    write(os.path.join(d, "artefact", artname), art)
    write(os.path.join(d, "evidence", "sbom.cdx.json"),
          cyclonedx("hearth-lock-3-firmware", version, art, comps, root_deps,
                    {"connectedhomeip": ["mbedtls", "openthread"]}))
    write(os.path.join(d, "evidence", "provenance.intoto.json"),
          provenance("//firmware/hearth/lock3:signed_image", artname, art, "hearth-lock-3/%s" % version))
    vex = {"@context": "https://openvex.dev/ns/v0.2.0",
           "@id": "https://vex.aldermoor.example/hearth-lock-3/%s" % version,
           "author": "Aldermoor PSIRT", "role": "manufacturer", "timestamp": "2028-01-11T10:02:00Z", "version": 1,
           "statements": vex_statements}
    write(os.path.join(d, "evidence", "vex.openvex.json"), vex)
    write(os.path.join(d, "evidence", "vex.openvex.intoto.json"), vex_attestation(vex, artname, art, OPENVEX_PT))
    write(os.path.join(d, "evidence", "sast.sarif"), sarif("CodeQL", [
        ("cpp/uncontrolled-allocation-size", "warning", "Allocation size from BLE frame length", "src/ble/frame.c"),
        ("cpp/unused-local-variable", "note", "Unused variable", "src/ui/led.c"),
        ("cpp/path-injection", "error", "Path built from input", "tools/factory/flash.c",
         "Factory tool not shipped in image; PSIRT-2027-118"),
    ]))
    write(os.path.join(d, "evidence", "fuzz.sarif"), sarif("libFuzzer (aldermoor-fuzz-farm)", []))
    tests = [("sast", "evidence/sast.sarif"), ("fuzz", "evidence/fuzz.sarif")] + (tests_extra or [])
    common_docs(d, "Hearth Lock 3", version)
    write(os.path.join(d, "docs", "applicability-matrix.json"), matrix("hearth-lock-3"))
    m = manifest(LOCK, version, prev, release_date,
                 {"date": placing_date, "event": "update_to_placed_product", "member_states": ["IE", "DE", "FR", "NL"]},
                 LOCK_CLASS, "artefact/" + artname, root_deps,
                 ("evidence/sbom.cdx.json", "evidence/provenance.intoto.json", "evidence/vex.openvex.json"),
                 LOCK_SUPPORT, sm,
                 {"declaration_id": "AP-DoC-HL3-2027-001", "status": decl_status, "reused_from_version": "4.0.0",
                  "uri": "https://www.aldermoor.example/compliance/doc/hearth-lock-3",
                  "signatory_function": "SVP Devices (delegated signatory)"}, tests)
    write(os.path.join(d, "release.json"), m)
    return d


def lock_comps(zlib="1.2.12", extra=()):
    base = [("hearth-lock-app", None, "pkg:generic/aldermoor/hearth-lock-app", "Aldermoor Platforms"),
            ("zephyr", "3.7.0", "pkg:github/zephyrproject-rtos/zephyr@v3.7.0", "Zephyr Project"),
            ("mbedtls", "3.6.2", "pkg:generic/mbedtls@3.6.2", "Trusted Firmware project"),
            ("zlib", zlib, "pkg:generic/zlib@%s" % zlib, "zlib project"),
            ("openthread", "2024.06", "pkg:github/openthread/openthread@thread-reference-20240612", "OpenThread"),
            ("connectedhomeip", "1.3.0.0", "pkg:github/project-chip/connectedhomeip@v1.3.0.0", "CSA")]
    return base + list(extra)


BROWSER_141_PLACED = "2028-01-06"  # illustrative: first offering of 141.0.7390.40, assessed as a new placing


def browser_release(version, prev, placing_date, pkgs, root_deps, direct, csaf_status, fuzz_results, sm):
    d = os.path.join(REL, "lumen-browser_%s" % version)
    art = blob("lumen-browser-%s" % version)
    artname = "lumen-browser-%s-linux-x64.tar.zst" % version
    write(os.path.join(d, "artefact", artname), art)
    write(os.path.join(d, "evidence", "sbom.spdx.json"), spdx("lumen-browser", version, art, pkgs, root_deps))
    write(os.path.join(d, "evidence", "provenance.intoto.json"),
          provenance("//lumen/browser:release_linux_x64", artname, art, "lumen-browser/%s" % version))
    pid = "LB-%s" % version
    status = {csaf_status: [pid]}
    vuln = {"cve": "CVE-2023-4863", "notes": [{"category": "description", "text": "Heap buffer overflow in libwebp lossless decoder."}],
            "product_status": status}
    if csaf_status == "fixed":
        vuln["remediations"] = [{"category": "vendor_fix", "details": "Vendored libwebp updated to 1.3.2.", "product_ids": [pid]}]
    csaf = {
        "document": {"category": "csaf_vex", "csaf_version": "2.0", "title": "Lumen Browser %s VEX" % version,
                     "publisher": {"category": "vendor", "name": "Aldermoor Platforms (fictional)",
                                   "namespace": "https://www.aldermoor.example"},
                     "tracking": {"id": "ALD-VEX-LB-%s" % version, "status": "final", "version": "1",
                                  "initial_release_date": placing_date + "T06:00:00Z",
                                  "current_release_date": placing_date + "T06:00:00Z",
                                  "revision_history": [{"date": placing_date + "T06:00:00Z", "number": "1", "summary": "Initial"}]}},
        "product_tree": {"branches": [{"category": "vendor", "name": "Aldermoor Platforms", "branches": [
            {"category": "product_name", "name": "Lumen Browser", "branches": [
                {"category": "product_version", "name": version,
                 "product": {"product_id": pid, "name": "Lumen Browser %s" % version,
                             "product_identification_helper": {"purl": "pkg:generic/aldermoor/lumen-browser@%s" % version}}}]}]}]},
        "vulnerabilities": [vuln]}
    write(os.path.join(d, "evidence", "vex.csaf.json"), csaf)
    write(os.path.join(d, "evidence", "vex.csaf.intoto.json"), vex_attestation(csaf, artname, art, CSAF_PT))
    write(os.path.join(d, "evidence", "sast.sarif"), sarif("CodeQL", [
        ("cpp/integer-overflow-tainted", "warning", "Tainted multiplication", "engine/net/http_parser.cc")]))
    write(os.path.join(d, "evidence", "fuzz.sarif"), sarif("libFuzzer (aldermoor-fuzz-farm)", fuzz_results))
    common_docs(d, "Lumen Browser", version)
    write(os.path.join(d, "docs", "applicability-matrix.json"), matrix("lumen-browser", {
        "2m": {"implementation": "Clear browsing data; profile deletion; sync data deletion via account"}}))
    m = manifest({"product_id": "lumen-browser", "name": "Lumen Browser (desktop)",
                  "manufacturer": "Aldermoor Platforms (fictional)", "product_type": "software",
                  "family": "Lumen Browser"}, version, prev, placing_date,
                 # A weekly security update on the 141 branch is not a new placing: it keeps
                 # the placing date of 141.0.7390.40 (guidance para 15, Example 2).
                 {"date": placing_date, "event": "update_to_placed_product",
                  "member_states": ["IE", "DE", "FR", "ES", "IT", "PL"],
                  "inherited_placing_date": BROWSER_141_PLACED, "inherited_from_version": "141.0.7390.40"},
                 {"class": "important_class_i",
                  "annex_category": "Annex III Class I, 2: standalone and embedded browsers",
                  "conformity_route": "module_h", "harmonised_standards_applied_in_full": [],
                  "notified_body": "Illustrative notified body (no CRA body designated at 8 Sep 2026)",
                  "certificate_ref": "QS-APPROVAL-ILLUSTRATIVE-0142"},
                 "artefact/" + artname, direct,
                 ("evidence/sbom.spdx.json", "evidence/provenance.intoto.json", "evidence/vex.csaf.json"),
                 {"end_date": "2033-02-28", "latest_version_rule": True,
                  "justification": "Product support period for Lumen Browser; Art 13(10) latest-version rule with free upgrade."},
                 sm,
                 {"declaration_id": "AP-DoC-LB-141", "status": "reused", "reused_from_version": "141.0.7390.40",
                  "uri": "https://www.aldermoor.example/compliance/doc/lumen-browser",
                  "signatory_function": "SVP Browser (delegated signatory)"},
                 [("sast", "evidence/sast.sarif"), ("fuzz", "evidence/fuzz.sarif")])
    write(os.path.join(d, "release.json"), m)
    return d


def main():
    feeds()
    policy()
    lock_deps = ["hearth-lock-app", "zephyr", "mbedtls", "zlib", "openthread", "connectedhomeip"]

    def fix_app(comps, v):
        return [(n, v if n == "hearth-lock-app" else ver, (p + "@" + v) if n == "hearth-lock-app" else p, s)
                for n, ver, p, s in comps]

    # PASS: security update
    lock_release("4.2.0", "4.1.3", "2028-01-11", "2028-01-18", fix_app(lock_comps(), "4.2.0"), lock_deps,
                 [{"vulnerability": {"name": "CVE-2022-37434"},
                   "products": [{"@id": "pkg:generic/aldermoor/hearth-lock-3-firmware@4.2.0",
                                 "subcomponents": [{"@id": "pkg:generic/zlib@1.2.12"}]}],
                   "status": "not_affected", "justification": "vulnerable_code_not_in_execute_path",
                   "impact_statement": "Firmware calls deflate only (diagnostic bundles); inflateGetHeader() is never linked."}],
                 {"change_type": "security_update",
                  "questions": {"new_threat_vectors": False, "new_attack_scenarios": False,
                                "changed_likelihood": False, "changed_impact": False},
                  "rationale": "Fixes BLE pairing timing weakness; no new interfaces, data flows or dependencies.",
                  "assessed_by": None, "decision": "not_substantial"})
    # REVIEW: functionality change with pt 110 'yes' answers
    lock_release("4.3.0", "4.2.0", "2028-02-27", "2028-03-06",
                 fix_app(lock_comps("1.3.1", [("hearth-voice-unlock", "1.0.0", "pkg:generic/aldermoor/hearth-voice-unlock@1.0.0",
                                               "Aldermoor Platforms")]), "4.3.0"),
                 lock_deps + ["hearth-voice-unlock"],
                 [{"vulnerability": {"name": "CVE-2022-37434"},
                   "products": [{"@id": "pkg:generic/aldermoor/hearth-lock-3-firmware@4.3.0"}],
                   "status": "fixed"}],
                 {"change_type": "functionality",
                  "questions": {"new_threat_vectors": True, "new_attack_scenarios": True,
                                "changed_likelihood": False, "changed_impact": False},
                  "rationale": "Adds voice-assistant unlock through the Hearth cloud: a new remote unlock path.",
                  "assessed_by": None, "decision": "pending_review"},
                 tests_extra=[("pentest", "evidence/pentest-summary.json")])
    write(os.path.join(REL, "hearth-lock-3_4.3.0", "evidence", "pentest-summary.json"),
          {"format": "test-summary/v1", "tool": "Aldermoor Red Team (internal)", "report_uri": "pentest-HL3-4.3.0.pdf",
           "scope": "Voice unlock path, cloud boundary, BLE", "findings": {"critical": 0, "high": 0, "medium": 2, "low": 3}})

    browser_pkgs = [("lumen-engine", None, "BSD-3-Clause"), ("skia", "m141", "BSD-3-Clause"),
                    ("libwebp", None, "BSD-3-Clause"), ("harfbuzz", "10.1.0", "MIT"), ("icu", "76.1", "Unicode-3.0"),
                    ("boringssl", "0.20250114.0", "Apache-2.0"), ("zlib", "1.3.1", "Zlib"), ("freetype", "2.13.3", "FTL")]
    direct = ["lumen-engine", "skia", "libwebp", "harfbuzz", "icu", "boringssl", "zlib", "freetype"]

    def pk(engine, webp):
        return [(n, engine if n == "lumen-engine" else webp if n == "libwebp" else v, lic) for n, v, lic in browser_pkgs]

    # FAIL: KEV vulnerability unresolved, SBOM missing a top-level dependency, open fuzz crash
    browser_release("141.0.7390.54", "141.0.7390.40", "2028-02-03", pk("141.0.7390.54", "1.3.1"),
                    [d for d in direct if d != "harfbuzz"], direct, "under_investigation",
                    [("heap-buffer-overflow", "error", "ASan: heap-buffer-overflow READ 4 in ImageDecoder",
                      "engine/image/webp_decoder.cc")],
                    {"change_type": "security_update",
                     "questions": {"new_threat_vectors": False, "new_attack_scenarios": False,
                                   "changed_likelihood": False, "changed_impact": False},
                     "rationale": "Weekly security update on the 141 branch.", "assessed_by": None,
                     "decision": "not_substantial"})
    # PASS: fixed security update
    browser_release("141.0.7390.65", "141.0.7390.40", "2028-02-10", pk("141.0.7390.65", "1.3.2"), direct, direct,
                    "fixed", [],
                    {"change_type": "security_update",
                     "questions": {"new_threat_vectors": False, "new_attack_scenarios": False,
                                   "changed_likelihood": False, "changed_impact": False},
                     "rationale": "Weekly security update; vendored libwebp updated; harfbuzz edge restored in SBOM.",
                     "assessed_by": None, "decision": "not_substantial"})
    print("examples written under", REL)


if __name__ == "__main__":
    main()
