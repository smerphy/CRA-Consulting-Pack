"""Append-only local evidence store (reference for the design).

Production design: object storage with compliance-mode object lock, a
retention date per object version and a hash-chained ledger (see paper.md).
This local implementation demonstrates the same contract:
- blobs are content-addressed (blobs/sha256/<digest>) and never overwritten;
- records are write-once and content-addressed
  (records/<product>/<version>/<sha256>.json); a re-gated version (for
  example after a REVIEW decision is recorded) adds a new record, never
  replaces the earlier one;
- every write appends a ledger entry whose chain hash covers the previous
  entry, so deletion or edit of any record is detectable by verify().
"""

import hashlib
import json
import os
import shutil
import stat


class StoreError(RuntimeError):
    pass


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _readonly(path):
    os.chmod(path, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)


def put_blob(store, src):
    h = hashlib.sha256()
    with open(src, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    dig = h.hexdigest()
    dst = os.path.join(store, "blobs", "sha256", dig)
    if not os.path.exists(dst):
        os.makedirs(os.path.dirname(dst), exist_ok=True)
        shutil.copyfile(src, dst)
        _readonly(dst)
    return dig


def _ledger_tail(store):
    path = os.path.join(store, "ledger.jsonl")
    if not os.path.exists(path):
        return "0" * 64, 0
    last, n = None, 0
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if line.strip():
                last, n = json.loads(line), n + 1
    return last["chain"], n


def put_record(store, record, release_dir, files):
    """Store evidence files and the record; refuse to overwrite."""
    pid, ver = record["product"]["product_id"], record["version"]["version"]
    rdir = os.path.join(store, "records", pid, ver)
    body = _canon(record)
    rpath = os.path.join(rdir, hashlib.sha256(body).hexdigest() + ".json")
    if os.path.exists(rpath):
        raise StoreError("identical record for %s %s already stored; records are write-once" % (pid, ver))
    for rel in files:
        put_blob(store, os.path.join(release_dir, rel))
    os.makedirs(rdir, exist_ok=True)
    with open(rpath, "wb") as fh:
        fh.write(body)
    _readonly(rpath)
    prev, seq = _ledger_tail(store)
    rec_hash = hashlib.sha256(body).hexdigest()
    entry = {"seq": seq + 1, "record_id": record["record_id"], "record_sha256": rec_hash,
             "retain_until": (record.get("retention") or {}).get("retain_until"),
             "decision": (record.get("gate") or {}).get("decision"), "prev": prev}
    entry["chain"] = hashlib.sha256((prev + rec_hash).encode()).hexdigest()
    with open(os.path.join(store, "ledger.jsonl"), "a", encoding="utf-8") as fh:
        fh.write(json.dumps(entry, sort_keys=True) + "\n")
    return entry


def verify(store):
    """Recompute the chain and every record hash. Returns list of problems."""
    problems = []
    path = os.path.join(store, "ledger.jsonl")
    if not os.path.exists(path):
        return ["no ledger"]
    prev = "0" * 64
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            if not line.strip():
                continue
            e = json.loads(line)
            if e["prev"] != prev:
                problems.append("seq %d: chain break" % e["seq"])
            if hashlib.sha256((e["prev"] + e["record_sha256"]).encode()).hexdigest() != e["chain"]:
                problems.append("seq %d: chain hash mismatch" % e["seq"])
            _, pid, ver = e["record_id"].rsplit(":", 2)
            rpath = os.path.join(store, "records", pid, ver, e["record_sha256"] + ".json")
            if not os.path.exists(rpath):
                problems.append("seq %d: record missing" % e["seq"])
            else:
                with open(rpath, "rb") as rf:
                    if hashlib.sha256(rf.read()).hexdigest() != e["record_sha256"]:
                        problems.append("seq %d: record altered" % e["seq"])
            prev = e["chain"]
    return problems
