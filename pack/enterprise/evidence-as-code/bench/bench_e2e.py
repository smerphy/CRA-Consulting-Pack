"""End-to-end benchmark of the hard part: signing, timestamping, verification and object-lock storage.

Per synthetic version (inputs as in bench_scale.py: CycloneDX SBOM of
200-2,000 components, SARIF, matrix, documents, 64 KiB artefact) the timed
path is what a production pipeline does after the build:

  producer   sign provenance (ECDSA P-256) and VEX (Ed25519) through a
             KeyProvider, and get an RFC 3161 timestamp for each signature
             from the TSA over HTTP
  gate       build the record, verify both signatures and both timestamps
             against the trust policy, match the SBOM against a 50,000-record
             OSV feed, evaluate the gate, validate the schema
  record     sign the record (DSSE, ECDSA P-256) and timestamp it over HTTP
  store      PUT every input blob, the record, the signed record and the log
             entry to an S3 Object Lock bucket (moto server over HTTP,
             compliance mode, If-None-Match, checksum and lock read back)
  log        Merkle append; sign, timestamp and PUT a checkpoint
             (every version in mode "per-version"; every 100 in mode "batched")

Finally the whole store is verified as an auditor would: every entry,
record, signed bundle and checkpoint, and the Merkle root.

Not included: the build itself, artefact hashing for large binaries
(see bench_scale.py), and network latency to real cloud services (all
services here are local; see the extrapolation in the results).

Usage (module root): python bench/bench_e2e.py --n 1000
Results: bench/results/bench-e2e-<n>.json
"""

import argparse
import datetime as _dt
import json
import os
import platform
import random
import shutil
import socket
import statistics
import sys
import tempfile
import time

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(HERE)
sys.path.insert(0, ROOT)
sys.path.insert(0, HERE)
sys.path.insert(0, os.path.join(ROOT, "examples"))

import bench_scale as BS  # noqa: E402
import make_examples as MX  # noqa: E402
from cra_evidence import attest as A  # noqa: E402
from cra_evidence import evidence_store as ES  # noqa: E402
from cra_evidence import gate as G  # noqa: E402
from cra_evidence import keys as K  # noqa: E402
from cra_evidence import objectstore as O  # noqa: E402
from cra_evidence import schema as S  # noqa: E402
from cra_evidence import tsa as T  # noqa: E402
from cra_evidence.record import build_bundle  # noqa: E402


def pct(xs, p):
    xs = sorted(xs)
    return xs[min(len(xs) - 1, int(round(p / 100.0 * (len(xs) - 1))))]


def stats(xs):
    return {"mean_ms": round(1000 * statistics.mean(xs), 2), "p50_ms": round(1000 * pct(xs, 50), 2),
            "p95_ms": round(1000 * pct(xs, 95), 2), "p99_ms": round(1000 * pct(xs, 99), 2),
            "total_s": round(sum(xs), 2)}


class CountingClient:
    """Wrap a boto3 client to count PUT/HEAD calls."""

    def __init__(self, c):
        self._c, self.calls = c, {}

    def __getattr__(self, name):
        fn = getattr(self._c, name)

        def wrapped(*a, **kw):
            self.calls[name] = self.calls.get(name, 0) + 1
            return fn(*a, **kw)
        return wrapped


class CountingTSA:
    def __init__(self, client):
        self.client, self.n, self.name = client, 0, client.name

    def timestamp(self, m):
        self.n += 1
        return self.client.timestamp(m)


def run(n=1000, mode="per-version", seed=2027, min_c=200, max_c=2000, feed_size=50000, quiet=False):
    tmp = tempfile.mkdtemp(prefix="cra-e2e-")
    tsa = T.LocalTSA()
    url = tsa.serve()
    tsa_client = CountingTSA(T.TimestampClient(url))
    from moto.server import ThreadedMotoServer
    import boto3
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    moto = ThreadedMotoServer(ip_address="127.0.0.1", port=port, verbose=False)
    moto.start()
    s3 = CountingClient(boto3.client("s3", endpoint_url="http://127.0.0.1:%d" % port, region_name="eu-west-1",
                                     aws_access_key_id="b", aws_secret_access_key="b"))
    try:
        build = K.LocalFileKeyProvider(os.path.join(MX.KEYS, MX.BUILD_KEY + ".demo-private.pem"), MX.BUILD_KEY)
        psirt = K.LocalFileKeyProvider(os.path.join(MX.KEYS, MX.PSIRT_KEY + ".demo-private.pem"), MX.PSIRT_KEY)
        rec_key = K.LocalFileKeyProvider.generate(os.path.join(tmp, "rec.pem"), "bench-record")
        log_key = K.LocalFileKeyProvider.generate(os.path.join(tmp, "log.pem"), "bench-log", "ed25519")
        pol = BS.policy()
        tp = pol["attestation_trust"]
        tp["products"]["*"]["provenance"]["require_timestamp"] = True
        tp["products"]["*"]["vex"]["require_timestamp"] = True
        tp["products"]["*"]["evidence_record"] = {"keys": ["bench-record"], "require_timestamp": mode == "per-version"}
        tp["products"]["*"]["log_checkpoint"] = {"keys": ["bench-log"], "require_timestamp": True}
        tp["keys"]["bench-record"] = rec_key.trust_entry(["evidence_record"], "bench")
        tp["keys"]["bench-log"] = log_key.trust_entry(["log_checkpoint"], "bench")
        tp["timestamp_authorities"] = [{"name": "bench-tsa", "root_pem": T.pem_of(tsa.root)}]
        trust = A.TrustPolicy(tp, ROOT)
        backend = O.S3ObjectLockBackend("cra-bench-%s" % mode, client=s3)
        backend.ensure_bucket(create=True, region="eu-west-1")
        store = ES.EvidenceStore(backend, rec_key, log_key, tsa_client, log_id="bench-log",
                                 checkpoint_every=1 if mode == "per-version" else 100,
                                 timestamp_records=(mode == "per-version"))
        vulns, kev = BS.feed(feed_size, seed)
        by_name = {}
        for v in vulns:
            by_name.setdefault(v["affected"][0]["package"]["name"], []).append(v)
        rnd = random.Random(seed)
        st = {k: [] for k in ("producer_sign_timestamp", "gate_verify", "record_sign_timestamp", "object_lock_put",
                              "merkle_append", "checkpoint", "end_to_end")}
        decisions, ts_sources, put_bytes = {}, {}, 0
        d = os.path.join(tmp, "r")
        for i in range(n):
            BS.make_version(d, i, rnd, rnd.randint(min_c, max_c), by_name, kev)
            # --- producer signing and timestamping (build service and PSIRT service)
            t0 = time.perf_counter()
            pp = os.path.join(d, "evidence", "provenance.intoto.json")
            prov_st = A.load_attestation_file(pp)[0].unverified_statement()
            MX.write(pp, K.sign_and_timestamp(prov_st, build, tsa_client))
            vp = os.path.join(d, "evidence", "vex.openvex.intoto.json")
            vex_st = A.load_attestation_file(vp)[0].unverified_statement()
            MX.write(vp, K.sign_and_timestamp(vex_st, psirt, tsa_client))
            t1 = time.perf_counter()
            # --- gate with signature and timestamp verification
            b = build_bundle(d, osv_records=vulns, kev_ids=kev, generated_at="2028-01-11T10:15:00Z")
            res = G.evaluate(b, pol)
            b.record["gate"] = res
            errs = S.validate(b.record)
            if errs:
                raise RuntimeError(errs[:3])
            t2 = time.perf_counter()
            decisions[res["decision"]] = decisions.get(res["decision"], 0) + 1
            src = b.record["evidence"]["provenance"]["verification"]["signer"]["signing_time_source"]
            ts_sources[src] = ts_sources.get(src, 0) + 1
            files = []
            for sub in ("artefact", "evidence", "docs"):
                for fn in sorted(os.listdir(os.path.join(d, sub))):
                    files.append(sub + "/" + fn)
            files.append("release.json")
            put_bytes += sum(os.path.getsize(os.path.join(d, f)) for f in files)
            receipt = store.put_release(b.record, files, d)
            t3 = time.perf_counter()
            tm = receipt["timings"]
            st["producer_sign_timestamp"].append(t1 - t0)
            st["gate_verify"].append(t2 - t1)
            st["record_sign_timestamp"].append(tm["record_sign_and_timestamp"])
            st["object_lock_put"].append(tm["object_lock_put"])
            st["merkle_append"].append(tm["merkle_append"])
            st["checkpoint"].append(tm.get("checkpoint_sign_timestamp_put", 0.0))
            st["end_to_end"].append(t3 - t0)
            if not quiet and (i + 1) % 100 == 0:
                print("  %s: %d/%d, mean e2e %.1f ms" % (mode, i + 1, n, 1000 * statistics.mean(st["end_to_end"])),
                      flush=True)
        if store.tree.size % store.checkpoint_every:
            store.checkpoint()
        t0 = time.perf_counter()
        problems = store.verify(trust)
        t_verify = time.perf_counter() - t0
        objects = len(backend.list(""))
        e2e = statistics.mean(st["end_to_end"])
        out = {
            "mode": mode, "n": n, "decisions": decisions, "provenance_signing_time_source": ts_sources,
            "stages": {k: stats(v) for k, v in st.items()},
            "versions_per_second_single_thread": round(1 / e2e, 2),
            "calls_per_version": {"tsa": round(tsa_client.n / n, 2),
                                  "s3": {k: round(v / n, 2) for k, v in sorted(s3.calls.items())},
                                  "signatures": 3 + 1.0 / store.checkpoint_every},
            "objects": objects, "objects_per_version": round(objects / n, 2),
            "input_bytes_per_version": round(put_bytes / n),
            "store_verify": {"seconds": round(t_verify, 2), "ms_per_version": round(1000 * t_verify / n, 2),
                             "problems": problems[:5], "problem_count": len(problems)},
        }
        return out
    finally:
        tsa.stop()
        moto.stop()
        shutil.rmtree(tmp, ignore_errors=True)


def extrapolate(r):
    """Estimates, labelled: scale the measured single-thread cost to Aldermoor volumes."""
    e2e_s = r["stages"]["end_to_end"]["mean_ms"] / 1000
    weekly, yearly = 2000, 104000
    s3 = r["calls_per_version"]["s3"]
    # write path only: signatures (KMS), timestamps (TSA), PUT and lock read-back (object store);
    # get_object and list calls belong to the audit verification run after the loop
    calls = r["calls_per_version"]["signatures"] + r["calls_per_version"]["tsa"] + \
        s3.get("put_object", 0) + s3.get("head_object", 0)
    return {
        "basis": "measured single-thread end-to-end cost on local services; Aldermoor volumes are estimates "
                 "(2,000 EU versions a week, 104,000 a year)",
        "cpu_hours_per_week": round(weekly * e2e_s / 3600, 2),
        "cpu_hours_per_year": round(yearly * e2e_s / 3600, 1),
        "remote_calls_per_version_write_path": round(calls, 1),
        "assumed_remote_latency_ms": 50,
        "wall_clock_per_version_if_sequential_s_at_assumed_latency": round(e2e_s + calls * 0.05, 2),
        "note": "50 ms per remote call to a KMS, a TSA and an object store is an assumption, not a measurement; "
                "calls within a version can be parallelised and versions are independent.",
    }


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=1000)
    ap.add_argument("--modes", default="per-version,batched")
    a = ap.parse_args(argv)
    results = {"generated": _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat(),
               "host": {"python": platform.python_version(), "platform": platform.platform(),
                        "cpus": os.cpu_count()}, "runs": []}
    for mode in a.modes.split(","):
        r = run(a.n, mode)
        r["extrapolation"] = extrapolate(r)
        results["runs"].append(r)
        print(json.dumps({k: r[k] for k in ("mode", "decisions", "versions_per_second_single_thread",
                                             "objects_per_version")}), flush=True)
        print(json.dumps(r["stages"]), flush=True)
    os.makedirs(os.path.join(HERE, "results"), exist_ok=True)
    path = os.path.join(HERE, "results", "bench-e2e-%d.json" % a.n)
    with open(path, "w") as fh:
        json.dump(results, fh, indent=2)
    print("wrote", path)


if __name__ == "__main__":
    main()
