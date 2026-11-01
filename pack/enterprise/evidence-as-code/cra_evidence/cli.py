"""Command line: python -m cra_evidence <command> ...

Commands
  record     build the evidence record for a release directory
  gate       build the record, run the release gate, print the decision
             (exit 0 PASS, 1 FAIL, 3 REVIEW)
  index      write the Annex VII index (JSON and Markdown) for a release
  validate   validate a record JSON file (or a release directory) against the schema
  retention  compute the Art 13(13) retain-until date
  store      gate a release and write it to an append-only evidence store
  verify-store  recompute the store's hash chain
  verify-attestation  verify one DSSE envelope or Sigstore bundle against the
             trust policy (exit 0 verified, 1 not verified)
"""

import argparse
import datetime as _dt
import json
import os
import sys

from . import attest as A
from . import collectors as C
from . import gate as G
from . import index as I
from . import retention as R
from . import schema as S
from . import store as ST
from .record import build_bundle

EXIT = {"PASS": 0, "FAIL": 1, "REVIEW": 3}


def _feeds(args):
    osv_path = args.osv or (os.path.join(args.feeds, "osv-snapshot.json") if args.feeds else None)
    kev_path = args.kev or (os.path.join(args.feeds, "kev-snapshot.json") if args.feeds else None)
    osv = C.load_json(osv_path) if osv_path else None
    if isinstance(osv, dict):
        osv = osv.get("vulns") or []
    kev = C.load_kev(C.load_json(kev_path)) if kev_path else set()
    return osv, kev


def _policy(args):
    if not getattr(args, "policy", None):
        return None
    pol = C.load_json(args.policy)
    pol["_base_dir"] = os.path.dirname(os.path.abspath(args.policy))
    return pol


def _now(args):
    v = getattr(args, "now", None)
    return _dt.datetime.fromisoformat(v.replace("Z", "+00:00")) if v else None


def _gated(args):
    osv, kev = _feeds(args)
    bundle = build_bundle(args.release, osv_records=osv, kev_ids=kev, generated_at=args.generated_at)
    result = G.evaluate(bundle, _policy(args), now=_now(args))
    bundle.record["gate"] = result
    return bundle, result


def _dump(obj, path):
    text = json.dumps(obj, indent=2, sort_keys=False) + "\n"
    if path:
        os.makedirs(os.path.dirname(os.path.abspath(path)), exist_ok=True)
        with open(path, "w", encoding="utf-8") as fh:
            fh.write(text)
    else:
        sys.stdout.write(text)


def cmd_record(args):
    osv, kev = _feeds(args)
    bundle = build_bundle(args.release, osv_records=osv, kev_ids=kev, generated_at=args.generated_at)
    _dump(bundle.record, args.out)
    return 0


def cmd_gate(args):
    bundle, result = _gated(args)
    errs = S.validate(bundle.record)
    if errs:
        result["reasons"].append({"code": "RECORD_SCHEMA_INVALID", "severity": "fail",
                                  "message": "; ".join(errs[:5]), "basis": "spec/ schema 1.0.0"})
        result["decision"] = "FAIL"
    if args.out:
        _dump(bundle.record, args.out)
    if args.json:
        _dump(result, None)
    else:
        rec = bundle.record
        print("%s %s -> %s  (policy %s)" % (rec["product"]["product_id"], rec["version"]["version"],
                                            result["decision"], result["policy_id"]))
        for r in result["reasons"]:
            if r["severity"] != "info" or args.verbose:
                print("  [%s] %s: %s" % (r["severity"].upper(), r["code"], r["message"]))
    return EXIT[result["decision"]]


def cmd_index(args):
    bundle, _ = _gated(args)
    idx = I.build_index(bundle.record)
    os.makedirs(args.out, exist_ok=True)
    stem = "%s_%s" % (idx["product_id"], idx["version"])
    _dump(idx, os.path.join(args.out, stem + ".annex-vii-index.json"))
    with open(os.path.join(args.out, stem + ".annex-vii-index.md"), "w", encoding="utf-8") as fh:
        fh.write(I.render_markdown(idx))
    print("wrote %s/%s.annex-vii-index.{json,md}" % (args.out, stem))
    return 0


def cmd_validate(args):
    if os.path.isdir(args.target):
        osv, kev = _feeds(args)
        record = build_bundle(args.target, osv_records=osv, kev_ids=kev).record
    else:
        record = C.load_json(args.target)
    errs = S.validate(record, force_fallback=args.fallback)
    engine = "built-in validator" if args.fallback or not S.have_jsonschema() else "jsonschema"
    if errs:
        print("INVALID (%s): %d error(s)" % (engine, len(errs)))
        for e in errs:
            print("  " + e)
        return 1
    print("VALID (%s): %s" % (engine, record.get("record_id")))
    return 0


def cmd_retention(args):
    _dump(R.explain(args.placing, args.support_end, args.buffer_days), None)
    return 0


def cmd_store(args):
    bundle, result = _gated(args)
    m = bundle.context["manifest"]
    ev = m.get("evidence", {})
    files = [m["artefact"]] if m.get("artefact") else []
    files += [ev[k] for k in ("sbom", "provenance", "vex", "vex_attestation") if ev.get(k)]
    files += [t["path"] for t in ev.get("tests", [])]
    files += [ev[k]["path"] for k in ("risk_assessment", "applicability_matrix", "annex_ii",
                                       "update_design_note", "cvd_policy") if ev.get(k)]
    entry = ST.put_record(args.store, bundle.record, os.path.abspath(args.release),
                          [f for f in files if f not in bundle.context["missing"]])
    print(json.dumps(entry))
    return 0


def cmd_verify_store(args):
    problems = ST.verify(args.store)
    print("OK" if not problems else "\n".join(problems))
    return 0 if not problems else 1


def cmd_verify_attestation(args):
    pol = _policy(args) or {}
    trust = A.TrustPolicy(pol.get("attestation_trust") or {}, pol.get("_base_dir"))
    atts = A.load_attestation_file(args.attestation)
    if args.predicate_type:
        atts = [a for a in atts if (a.unverified_statement() or {}).get("predicateType") == args.predicate_type]
    att = atts[0] if atts else None
    res = A.verify(att, trust, args.product, args.purpose, _now(args))
    out = A.summary(res, trust)
    st = res["statement"] or {}
    out["predicate_type"] = st.get("predicateType")
    out["subjects"] = st.get("subject")
    if args.artefact:
        from .digests import file_digests
        digs, _ = file_digests(args.artefact)
        alg = A.subject_matches(st, digs)
        out["artefact"] = {"path": args.artefact, "sha256": digs["sha256"], "subject_match": alg}
        if not alg:
            out["verified"] = False
            out["problems"].append("SUBJECT_MISMATCH: no verified subject matches the artefact digest")
    _dump(out, None)
    return 0 if out["verified"] else 1


def main(argv=None):
    p = argparse.ArgumentParser(prog="python -m cra_evidence", description=__doc__,
                                formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = p.add_subparsers(dest="cmd", required=True)

    def feeds(sp):
        sp.add_argument("--feeds", help="directory holding osv-snapshot.json and kev-snapshot.json")
        sp.add_argument("--osv", help="OSV records JSON (list or {'vulns': [...]})")
        sp.add_argument("--kev", help="CISA KEV catalogue JSON")
        sp.add_argument("--generated-at", help="fix the record timestamp (reproducible output)")
        sp.add_argument("--now", help="evaluation time for key validity checks (ISO 8601; default: now)")

    sp = sub.add_parser("record"); sp.add_argument("release"); feeds(sp)
    sp.add_argument("-o", "--out"); sp.set_defaults(fn=cmd_record)

    sp = sub.add_parser("gate"); sp.add_argument("release"); feeds(sp)
    sp.add_argument("--policy"); sp.add_argument("-o", "--out", help="write gated record JSON")
    sp.add_argument("--json", action="store_true"); sp.add_argument("-v", "--verbose", action="store_true")
    sp.set_defaults(fn=cmd_gate)

    sp = sub.add_parser("index"); sp.add_argument("release"); feeds(sp)
    sp.add_argument("--policy"); sp.add_argument("-o", "--out", required=True); sp.set_defaults(fn=cmd_index)

    sp = sub.add_parser("validate"); sp.add_argument("target"); feeds(sp)
    sp.add_argument("--fallback", action="store_true", help="force the built-in validator")
    sp.set_defaults(fn=cmd_validate)

    sp = sub.add_parser("retention"); sp.add_argument("--placing", required=True)
    sp.add_argument("--support-end", required=True); sp.add_argument("--buffer-days", type=int, default=0)
    sp.set_defaults(fn=cmd_retention)

    sp = sub.add_parser("store"); sp.add_argument("release"); feeds(sp)
    sp.add_argument("--policy"); sp.add_argument("--store", required=True); sp.set_defaults(fn=cmd_store)

    sp = sub.add_parser("verify-store"); sp.add_argument("--store", required=True)
    sp.set_defaults(fn=cmd_verify_store)

    sp = sub.add_parser("verify-attestation"); sp.add_argument("attestation")
    sp.add_argument("--policy", required=True); sp.add_argument("--product", required=True)
    sp.add_argument("--purpose", required=True, help="provenance | vex | publish | ...")
    sp.add_argument("--artefact", help="check the verified subject digest against this file")
    sp.add_argument("--predicate-type", help="select this predicate type from a multi-attestation file")
    sp.add_argument("--now", help="evaluation time (ISO 8601)")
    sp.set_defaults(fn=cmd_verify_attestation)

    args = p.parse_args(argv)
    return args.fn(args)
