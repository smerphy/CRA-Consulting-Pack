"""Scale benchmark: generate N synthetic signed versions and run record + gate + index on each.

Every version gets a CycloneDX SBOM of 200-2,000 components (uniform), a
DSSE-signed SLSA v1 provenance (ECDSA P-256), a DSSE-signed OpenVEX
attestation (Ed25519), SAST and fuzz SARIF, an applicability matrix and
document stubs. The gate verifies both signatures, matches the SBOM against
a synthetic OSV feed (default 50,000 records) and a KEV set, validates the
record against the JSON Schema and builds the Annex VII index.

Timed (per version, single process): build_bundle (parse, digest, OSV
match) + gate.evaluate (incl. signature verification) + schema validation +
index build and Markdown render + record serialisation. Not timed:
generating the synthetic inputs. Artefact hashing is measured separately
because real artefacts (MB to GB) dominate it.

Usage (from the module root):
  python bench/bench_scale.py --n 10000 --workers 2
Results go to bench/results/bench-<n>.json.
"""

import argparse
import datetime as _dt
import gzip
import hashlib
import json
import multiprocessing as mp
import os
import platform
import random
import shutil
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, os.path.join(ROOT, "examples"))

import make_examples as MX  # noqa: E402
from cra_evidence import gate as G  # noqa: E402
from cra_evidence import index as I  # noqa: E402
from cra_evidence import schema as S  # noqa: E402
from cra_evidence.record import build_bundle  # noqa: E402

UNIVERSE = 1000000        # distinct package names; with a 50,000-record feed this gives about 25 matches per 1,000-component SBOM
LICENSES = ["Apache-2.0", "MIT", "BSD-3-Clause", "ISC", "MPL-2.0", "LGPL-2.1-only"]


def feed(size, seed):
    rnd = random.Random(seed)
    vulns = []
    for i in range(size):
        name = "pkg-%07d" % rnd.randrange(UNIVERSE)
        fixed = "%d.%d.%d" % (rnd.randint(1, 9), rnd.randint(0, 20), rnd.randint(0, 30))
        vulns.append({"id": "SYN-%06d" % i, "aliases": ["CVE-2099-%06d" % i],
                      "affected": [{"package": {"ecosystem": "npm", "name": name, "purl": "pkg:npm/" + name},
                                    "ranges": [{"type": "ECOSYSTEM", "events": [{"introduced": "0"}, {"fixed": fixed}]}]}],
                      "database_specific": {"severity": rnd.choice(["LOW", "MEDIUM", "HIGH", "CRITICAL"])}})
    kev = {"CVE-2099-%06d" % i for i in rnd.sample(range(size), max(1, size // 500))}
    return vulns, kev


def policy():
    p = json.load(open(os.path.join(ROOT, "examples", "policy", "aldermoor-gate-policy.json")))
    tp = p["attestation_trust"]
    tp["products"]["*"] = {
        "provenance": {"keys": [MX.BUILD_KEY], "builder_ids": [MX.BUILDER], "min_slsa_build_level": 3,
                       "build_types": ["https://build.aldermoor.example/buildtypes/hermetic-bazel/v1"],
                       "external_parameters": {"target": {"pattern": r"//bench/.+"},
                                               "source": {"pattern": r"git\+https://monorepo\.aldermoor\.example/.+"}}},
        "vex": {"keys": [MX.PSIRT_KEY]}}
    p["required_tests"]["products"] = {}
    return p


def make_version(d, i, rnd, ncomp, osv_by_name, kev):
    """Write one synthetic release directory (overwrites d)."""
    if os.path.exists(d):
        shutil.rmtree(d)
    pid, ver = "bench-product-%03d" % (i % 200), "1.%d.%d" % (i // 200, i % 200)
    art = hashlib.sha256(b"art%d" % i).digest() * 2048          # 64 KiB stand-in artefact
    artname = "%s-%s.bin" % (pid, ver)
    MX.write(os.path.join(d, "artefact", artname), art)
    names = rnd.sample(range(UNIVERSE), ncomp)
    comps = []
    for n in names:
        name = "pkg-%07d" % n
        v = "%d.%d.%d" % (rnd.randint(1, 9), rnd.randint(0, 20), rnd.randint(0, 30))
        comps.append({"type": "library", "bom-ref": "%s@%s" % (name, v), "name": name, "version": v,
                      "purl": "pkg:npm/%s@%s" % (name, v), "supplier": {"name": "Supplier %d" % (n % 997)},
                      "licenses": [{"license": {"id": LICENSES[n % len(LICENSES)]}}],
                      "hashes": [{"alg": "SHA-512", "content": hashlib.sha512(b"%d%s" % (n, v.encode())).hexdigest()}],
                      "properties": [{"name": "bsi:dependencies:complete", "value": "true"}]})
    top = comps[:max(5, ncomp // 10)]
    direct = [c["name"] for c in top]
    fail_case = rnd.random() < 0.02                                   # SBOM misses a direct dependency
    review_case = rnd.random() < 0.05                                 # one medium vulnerability left untriaged
    root = "pkg:generic/aldermoor/%s@%s" % (pid, ver)
    deps = [{"ref": root, "dependsOn": [c["bom-ref"] for c in (top[1:] if fail_case else top)]}]
    rest = comps[len(top):]
    for k, c in enumerate(top):
        deps.append({"ref": c["bom-ref"], "dependsOn": [x["bom-ref"] for x in rest[k::len(top)]]})
    sbom = {"bomFormat": "CycloneDX", "specVersion": "1.5", "version": 1,
            "metadata": {"timestamp": "2028-01-11T09:14:02Z",
                         "component": {"type": "application", "bom-ref": root, "name": pid, "version": ver,
                                       "hashes": [{"alg": "SHA-256", "content": hashlib.sha256(art).hexdigest()}]}},
            "components": comps, "dependencies": deps}
    MX.write(os.path.join(d, "evidence", "sbom.cdx.json"), sbom)
    # VEX: every feed match gets a justified not_affected, except the review case
    statements, left = [], review_case
    for c in comps:
        for rec in osv_by_name.get(c["name"], ()):
            ev = rec["affected"][0]["ranges"][0]["events"]
            from cra_evidence.collectors import version_in_range
            if version_in_range(c["version"], ev):
                cve = rec["aliases"][0]
                if left and cve not in kev and rec["database_specific"]["severity"] in ("LOW", "MEDIUM"):
                    left = False
                    continue
                statements.append({"vulnerability": {"name": cve}, "status": "not_affected",
                                   "justification": "vulnerable_code_not_in_execute_path",
                                   "products": [{"@id": root, "subcomponents": [{"@id": c["purl"]}]}]})
    vex = {"@context": "https://openvex.dev/ns/v0.2.0", "@id": "https://vex.aldermoor.example/%s/%s" % (pid, ver),
           "author": "Aldermoor PSIRT", "timestamp": "2028-01-11T10:02:00Z", "version": 1, "statements": statements}
    MX.write(os.path.join(d, "evidence", "vex.openvex.json"), vex)
    MX.write(os.path.join(d, "evidence", "vex.openvex.intoto.json"), MX.vex_attestation(vex, artname, art, MX.OPENVEX_PT))
    st = {"_type": "https://in-toto.io/Statement/v1",
          "subject": [{"name": artname, "digest": {"sha256": hashlib.sha256(art).hexdigest()}}],
          "predicateType": "https://slsa.dev/provenance/v1",
          "predicate": {"buildDefinition": {
              "buildType": "https://build.aldermoor.example/buildtypes/hermetic-bazel/v1",
              "externalParameters": {"target": "//bench/%s:release" % pid,
                                     "source": "git+https://monorepo.aldermoor.example/monorepo@refs/tags/%s/%s" % (pid, ver)},
              "resolvedDependencies": [{"uri": "git+https://monorepo.aldermoor.example/monorepo",
                                        "digest": {"gitCommit": hashlib.sha1(b"%d" % i).hexdigest()}}]},
              "runDetails": {"builder": {"id": MX.BUILDER}, "metadata": {"invocationId": "inv-%d" % i}}}}
    MX.write(os.path.join(d, "evidence", "provenance.intoto.json"), MX.sign(st, MX.BUILD_KEY))
    MX.write(os.path.join(d, "evidence", "sast.sarif"), MX.sarif("CodeQL", [
        ("js/prototype-pollution", "warning", "Possible prototype pollution", "src/a.js"),
        ("js/unused-local-variable", "note", "Unused variable", "src/b.js")]))
    MX.write(os.path.join(d, "evidence", "fuzz.sarif"), MX.sarif("libFuzzer", []))
    MX.common_docs(d, pid, ver)
    MX.write(os.path.join(d, "docs", "applicability-matrix.json"), MX.matrix(pid))
    m = MX.manifest({"product_id": pid, "name": pid, "manufacturer": "Aldermoor Platforms (fictional)",
                     "product_type": "software", "family": "bench"}, ver, None, "2028-01-11",
                    {"date": "2028-01-18", "event": "new_version_placing", "member_states": ["IE"]},
                    {"class": "default", "conformity_route": "module_a", "harmonised_standards_applied_in_full": []},
                    "artefact/" + artname, direct,
                    ("evidence/sbom.cdx.json", "evidence/provenance.intoto.json", "evidence/vex.openvex.json"),
                    {"end_date": "2033-01-31", "latest_version_rule": True, "justification": "bench"},
                    {"change_type": "security_update",
                     "questions": {"new_threat_vectors": False, "new_attack_scenarios": False,
                                   "changed_likelihood": False, "changed_impact": False},
                     "rationale": "bench", "assessed_by": None, "decision": "not_substantial"},
                    {"declaration_id": "AP-DoC-BENCH", "status": "reused", "reused_from_version": "1.0.0",
                     "uri": "https://www.aldermoor.example/compliance/doc/bench", "signatory_function": "bench"},
                    [("sast", "evidence/sast.sarif"), ("fuzz", "evidence/fuzz.sarif")])
    MX.write(os.path.join(d, "release.json"), m)
    return ncomp


def _sizes(d, record_bytes, index_bytes):
    raw, gz = record_bytes + index_bytes, 0
    blob = b""
    for sub in ("evidence", "docs"):
        for fn in sorted(os.listdir(os.path.join(d, sub))):
            with open(os.path.join(d, sub, fn), "rb") as fh:
                b = fh.read()
            raw += len(b)
            blob += b
    with open(os.path.join(d, "release.json"), "rb") as fh:
        b = fh.read()
    raw += len(b)
    blob += b
    return raw, len(gzip.compress(blob, 6))


def worker(args):
    start, stop, cfg = args
    rnd = random.Random(cfg["seed"] * 1000003 + start)
    vulns, kev = feed(cfg["feed_size"], cfg["seed"])
    by_name = {}
    for v in vulns:
        by_name.setdefault(v["affected"][0]["package"]["name"], []).append(v)
    pol = policy()
    tmp = tempfile.mkdtemp(prefix="cra-bench-")
    out = {"gate_seconds": 0.0, "gen_seconds": 0.0, "decisions": {}, "components": 0, "raw_bytes": 0,
           "gz_bytes": 0, "max_ms": 0.0, "signature_failures": 0, "verified": 0, "codes": {}}
    lat = []
    try:
        for i in range(start, stop):
            d = os.path.join(tmp, "r")
            t0 = time.perf_counter()
            ncomp = make_version(d, i, rnd, rnd.randint(cfg["min_components"], cfg["max_components"]), by_name, kev)
            t1 = time.perf_counter()
            b = build_bundle(d, osv_records=vulns, kev_ids=kev, generated_at="2028-01-11T10:15:00Z")
            res = G.evaluate(b, pol)
            b.record["gate"] = res
            errs = S.validate(b.record)
            idx = I.build_index(b.record)
            md = I.render_markdown(idx)
            rec_bytes = json.dumps(b.record).encode()
            t2 = time.perf_counter()
            if errs:
                raise RuntimeError("schema errors: %s" % errs[:3])
            out["gen_seconds"] += t1 - t0
            out["gate_seconds"] += t2 - t1
            lat.append((t2 - t1) * 1000)
            out["decisions"][res["decision"]] = out["decisions"].get(res["decision"], 0) + 1
            for r in res["reasons"]:
                if r["severity"] != "info":
                    out["codes"][r["code"]] = out["codes"].get(r["code"], 0) + 1
                if "SIGNATURE_INVALID" in r["code"]:
                    out["signature_failures"] += 1
            if (b.record["evidence"]["provenance"].get("verification") or {}).get("verified") and \
                    (b.record["evidence"]["vulnerability_status"].get("verification") or {}).get("verified"):
                out["verified"] += 1
            out["components"] += ncomp
            raw, gz = _sizes(d, len(rec_bytes), len(json.dumps(idx)) + len(md))
            out["raw_bytes"] += raw
            out["gz_bytes"] += gz
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    out["latencies_ms"] = lat
    return out


def hash_throughput(mib=256):
    buf = os.urandom(1 << 20)
    h256, h512 = hashlib.sha256(), hashlib.sha512()
    t = time.perf_counter()
    for _ in range(mib):
        h256.update(buf)
        h512.update(buf)
    return mib / (time.perf_counter() - t)


def keyless_verify_ms(k=50):
    try:
        sys.path.insert(0, os.path.join(ROOT, "tests"))
        from cra_evidence import attest as A
        path = os.path.join(ROOT, "examples", "real", "policy", "real-artefact-gate-policy.json")
        tp = A.TrustPolicy(json.load(open(path))["attestation_trust"])
        att_path = os.path.join(ROOT, "examples", "real", "releases", "npm-sigstore_5.0.0", "evidence",
                                "npm-attestations.json")
        t = time.perf_counter()
        for _ in range(k):
            att = A.select(A.load_attestation_file(att_path), ("https://slsa.dev/provenance/v1",))
            assert A.verify(att, tp, "npm-sigstore", "provenance")["verified"]
        return (time.perf_counter() - t) * 1000 / k
    except Exception as e:  # noqa: BLE001
        return "unavailable: %s" % e


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(p / 100.0 * (len(xs) - 1))))] if xs else 0.0


def run(n=10000, workers=None, min_components=200, max_components=2000, feed_size=50000, seed=2027, quiet=False):
    workers = workers or os.cpu_count() or 1
    cfg = {"seed": seed, "feed_size": feed_size, "min_components": min_components, "max_components": max_components}
    chunks = [(k * n // workers, (k + 1) * n // workers, cfg) for k in range(workers)]
    t0 = time.perf_counter()
    if workers == 1:
        parts = [worker(chunks[0])]
    else:
        with mp.get_context("fork").Pool(workers) as pool:
            parts = pool.map(worker, chunks)
    wall = time.perf_counter() - t0
    tot = {"decisions": {}, "codes": {}}
    lat = []
    for p in parts:
        for k in ("gate_seconds", "gen_seconds", "components", "raw_bytes", "gz_bytes", "signature_failures", "verified"):
            tot[k] = tot.get(k, 0) + p[k]
        for k, v in p["decisions"].items():
            tot["decisions"][k] = tot["decisions"].get(k, 0) + v
        for k, v in p["codes"].items():
            tot["codes"][k] = tot["codes"].get(k, 0) + v
        lat += p["latencies_ms"]
    per_core = n / tot["gate_seconds"]
    weekly_per_core = per_core * 3600 * 24 * 7
    gz_mean = tot["gz_bytes"] / n
    res = {
        "benchmark": "cra_evidence scale benchmark",
        "run_at": _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z"),
        "host": {"cpus": os.cpu_count(), "python": platform.python_version(), "machine": platform.machine(),
                 "processor": platform.processor() or "unknown"},
        "versions": n, "workers": workers, "feed_records": feed_size,
        "components": {"min": min_components, "max": max_components, "mean": round(tot["components"] / n, 1)},
        "decisions": tot["decisions"], "non_info_reason_codes": tot["codes"],
        "both_signatures_verified": tot["verified"], "signature_failures": tot["signature_failures"],
        "gate_cpu_seconds": round(tot["gate_seconds"], 2), "generation_cpu_seconds": round(tot["gen_seconds"], 2),
        "wall_seconds": round(wall, 2),
        "per_core_versions_per_second": round(per_core, 2),
        "latency_ms": {"p50": round(pct(lat, 50), 2), "p95": round(pct(lat, 95), 2), "p99": round(pct(lat, 99), 2),
                       "max": round(max(lat), 2) if lat else 0},
        "extrapolation": {
            "per_core_versions_per_week": int(weekly_per_core),
            "cores_for_2000_per_week_at_10x_peak": round(2000 * 10 / weekly_per_core, 4),
            "cores_for_20000_per_week_in_one_8h_window": round(20000 / (per_core * 8 * 3600), 3),
        },
        "storage": {
            "mean_raw_kib_per_version": round(tot["raw_bytes"] / n / 1024, 1),
            "mean_gzip_kib_per_version": round(gz_mean / 1024, 1),
            "tb_per_year_at_104000_versions": round(gz_mean * 104000 / 1e12, 4),
            "note": "evidence excluding the release binary: SBOM, signed provenance, VEX and signed VEX, two small "
                    "SARIF files, document stubs, record and Annex VII index; gzip level 6",
        },
        "artefact_hashing_mib_per_second_sha256_plus_sha512": round(hash_throughput(64 if quiet else 256), 1),
        "keyless_sigstore_verify_ms": keyless_verify_ms(3 if quiet else 50),
    }
    if not quiet:
        os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
        with open(os.path.join(HERE, "results", "bench-%d.json" % n), "w") as fh:
            json.dump(res, fh, indent=2)
        print(json.dumps(res, indent=2))
    return res


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=10000)
    ap.add_argument("--workers", type=int, default=None)
    ap.add_argument("--min-components", type=int, default=200)
    ap.add_argument("--max-components", type=int, default=2000)
    ap.add_argument("--feed-size", type=int, default=50000)
    ap.add_argument("--seed", type=int, default=2027)
    a = ap.parse_args(argv)
    run(a.n, a.workers, a.min_components, a.max_components, a.feed_size, a.seed)


if __name__ == "__main__":
    main()
