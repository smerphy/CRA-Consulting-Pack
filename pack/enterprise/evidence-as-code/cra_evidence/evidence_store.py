"""Signed, append-only evidence store over any ``StorageBackend``.

Layout (keys under the backend):
  blobs/sha256/<hex>                         evidence inputs, content-addressed
  records/<product>/<version>/<rsha>.record.json      canonical record JSON
  records/<product>/<version>/<rsha>.bundle.json      signed record (Sigstore v0.3 bundle,
                                                      DSSE + RFC 3161 timestamp)
  log/entries/<seq:012d>.json                one entry per stored record
  log/checkpoints/<size:012d>.json           signed tree head (bundle over a checkpoint statement)

Each entry carries the record digest, the signed-bundle digest, the
artefact digest, the gate decision, the retain-until date and a hash chain
(prev, chain = SHA-256(prev || record_sha256)). Entries are leaves of an RFC
9162 Merkle tree. After every ``checkpoint_every`` entries the store signs a
checkpoint statement (log id, tree size, root hash) with the log key and
time-stamps it. A checkpoint is small and can be handed to an auditor or a
notified body, or logged publicly; with it, inclusion and consistency proofs
detect deletion, reordering or edit of any entry, whatever the storage layer
did.

Every object is written once with a compliance-mode retain-until date:
blobs, record and bundle to the record's Art 13(13) retain-until date; log
entries and checkpoints to the latest retain-until date seen so far, because
proofs for later records depend on earlier leaves.
"""

import datetime as _dt
import hashlib
import json
import time

from . import attest as A
from . import keys as K
from . import merkle as M
from . import record_signing as RS
from .objectstore import WriteOnceError

CHECKPOINT_PREDICATE = "https://aldermoor.example/attestations/cra-evidence-log-checkpoint/v1"
CHECKPOINT_PURPOSE = "log_checkpoint"


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _sha(b):
    return hashlib.sha256(b).hexdigest()


def _now():
    return _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat().replace("+00:00", "Z")


class EvidenceStore:
    def __init__(self, backend, record_signer=None, log_signer=None, tsa=None, log_id="cra-evidence-log",
                 checkpoint_every=1, timestamp_records=True):
        self.backend = backend
        self.record_signer = record_signer
        self.log_signer = log_signer or record_signer
        self.tsa = tsa
        self.log_id = log_id
        self.checkpoint_every = max(1, int(checkpoint_every))
        self.timestamp_records = timestamp_records
        self.tree = M.CompactTree()
        self.chain = "0" * 64
        self.max_retain = "1970-01-01"
        self.entries = []
        self._load()

    # ------------------------------------------------------------ state
    def _load(self):
        for key in self.backend.list("log/entries/"):
            raw = self.backend.get(key)
            e = json.loads(raw)
            self.entries.append(e)
            self.tree.append(M.leaf_hash(_canon(e)))
            self.chain = e["chain"]
            self.max_retain = max(self.max_retain, e.get("retain_until") or "1970-01-01")

    # ------------------------------------------------------------ write
    def put_release(self, record, files=(), release_dir=None):
        """Store inputs, the signed record, a log entry and (if due) a signed checkpoint.

        ``files``: list of (relative path, bytes) or paths under ``release_dir``.
        Returns a receipt with keys, timings (seconds per step) and an
        inclusion proof when a checkpoint covers the entry.
        """
        import os
        t = {}
        retain = (record.get("retention") or {}).get("retain_until")
        if not retain:
            raise ValueError("record has no retention.retain_until; refuse to store without a lock date")
        self.max_retain = max(self.max_retain, retain)
        pid, ver = record["product"]["product_id"], record["version"]["version"]

        t0 = time.perf_counter()
        blobs = []
        for f in files:
            if isinstance(f, tuple):
                rel, data = f
            else:
                rel = f
                with open(os.path.join(release_dir, f), "rb") as fh:
                    data = fh.read()
            dig = _sha(data)
            self.backend.put_dedup("blobs/sha256/" + dig, data, retain)
            blobs.append({"path": rel, "sha256": dig})
        t["blobs_put"] = time.perf_counter() - t0

        body = _canon(record)
        rsha = _sha(body)
        t0 = time.perf_counter()
        bundle = RS.sign_record(record, self.record_signer, self.tsa if self.timestamp_records else None)
        t["record_sign_and_timestamp"] = time.perf_counter() - t0
        bbytes = _canon(bundle)

        t0 = time.perf_counter()
        base = "records/%s/%s/%s" % (pid, ver, rsha)
        r1 = self.backend.put(base + ".record.json", body, retain, "application/json")
        r2 = self.backend.put(base + ".bundle.json", bbytes, retain, "application/json")
        seq = len(self.entries)
        entry = {"seq": seq, "log_id": self.log_id, "record_id": record["record_id"], "record_sha256": rsha,
                 "bundle_sha256": _sha(bbytes),
                 "artefact_sha256": (((record.get("version") or {}).get("artefact") or {}).get("digests") or {})
                 .get("sha256"),
                 "decision": (record.get("gate") or {}).get("decision"), "retain_until": retain,
                 "record_key": base + ".record.json", "bundle_key": base + ".bundle.json",
                 "blobs": blobs, "stored_at": _now(), "prev": self.chain}
        entry["chain"] = _sha((self.chain + rsha).encode())
        self.backend.put("log/entries/%012d.json" % seq, _canon(entry), self.max_retain, "application/json")
        t["object_lock_put"] = time.perf_counter() - t0 + t["blobs_put"]
        self.entries.append(entry)
        self.chain = entry["chain"]
        t0 = time.perf_counter()
        self.tree.append(M.leaf_hash(_canon(entry)))
        t["merkle_append"] = time.perf_counter() - t0

        receipt = {"seq": seq, "record_sha256": rsha, "record_key": entry["record_key"],
                   "bundle_key": entry["bundle_key"], "versions": [r1.get("version_id"), r2.get("version_id")],
                   "retain_until": retain, "timings": t}
        if self.tree.size % self.checkpoint_every == 0:
            t0 = time.perf_counter()
            cp = self.checkpoint()
            t["checkpoint_sign_timestamp_put"] = time.perf_counter() - t0
            receipt["checkpoint_key"] = cp["key"]
            receipt["inclusion_proof"] = self.inclusion_proof(seq)
        return receipt

    def checkpoint(self):
        """Sign and store a checkpoint for the current tree."""
        size, root = self.tree.size, self.tree.root().hex()
        st = {"_type": "https://in-toto.io/Statement/v1",
              "subject": [{"name": "%s@%d" % (self.log_id, size), "digest": {"sha256": root}}],
              "predicateType": CHECKPOINT_PREDICATE,
              "predicate": {"log_id": self.log_id, "tree_size": size, "root_hash": root,
                            "hash": "RFC 9162 SHA-256", "issued_at": _now()}}
        bundle = K.sign_and_timestamp(st, self.log_signer, self.tsa)
        key = "log/checkpoints/%012d.json" % size
        try:
            self.backend.put(key, _canon(bundle), self.max_retain, "application/json")
        except WriteOnceError:
            pass
        return {"key": key, "tree_size": size, "root_hash": root, "bundle": bundle}

    def inclusion_proof(self, seq, size=None):
        size = size or self.tree.size
        return {"log_id": self.log_id, "leaf_index": seq, "tree_size": size,
                "root_hash": M.mth(self.tree.leaves[:size]).hex(),
                "audit_path": [h.hex() for h in self.tree.inclusion_proof(seq, size)],
                "checkpoint_key": "log/checkpoints/%012d.json" % size}

    # ------------------------------------------------------------- read
    def latest_checkpoint(self):
        keys = self.backend.list("log/checkpoints/")
        return (keys[-1], json.loads(self.backend.get(keys[-1]))) if keys else (None, None)

    def get_record(self, record_id, trust, now=None):
        """Verify-on-read: newest stored record for ``record_id`` whose signature verifies."""
        for e in reversed(self.entries):
            if e["record_id"] != record_id:
                continue
            bundle = json.loads(self.backend.get(e["bundle_key"]))
            pid = record_id.rsplit(":", 2)[-2]
            rec, res = RS.verify_record_bundle(bundle, trust, pid, e["record_sha256"], now)
            stored = self.backend.get(e["record_key"])
            if rec is not None and _sha(stored) != e["record_sha256"]:
                res["verified"], rec = False, None
                res["problems"].append("RECORD_ALTERED: stored record bytes differ from the logged digest")
            return rec, res
        return None, {"verified": False, "problems": ["RECORD_NOT_FOUND: %s" % record_id]}

    def verify(self, trust, now=None, deep=False):
        """Recompute chain, leaves and root; verify every record bundle and the checkpoints."""
        problems = []
        prev, leaves = "0" * 64, []
        entries = [json.loads(self.backend.get(k)) for k in self.backend.list("log/entries/")]
        for i, e in enumerate(entries):
            if e.get("seq") != i:
                problems.append("entry %d: sequence gap or reorder (seq %s)" % (i, e.get("seq")))
            if e["prev"] != prev or _sha((prev + e["record_sha256"]).encode()) != e["chain"]:
                problems.append("entry %d: hash chain broken" % i)
            prev = e["chain"]
            leaves.append(M.leaf_hash(_canon(e)))
            try:
                rec_bytes = self.backend.get(e["record_key"])
                bundle_bytes = self.backend.get(e["bundle_key"])
            except Exception as ex:  # noqa: BLE001
                problems.append("entry %d: record or bundle missing (%s)" % (i, ex))
                continue
            if _sha(rec_bytes) != e["record_sha256"]:
                problems.append("entry %d: record bytes altered" % i)
            if _sha(bundle_bytes) != e["bundle_sha256"]:
                problems.append("entry %d: signed bundle altered" % i)
            pid = e["record_id"].rsplit(":", 2)[-2]
            rec, res = RS.verify_record_bundle(json.loads(bundle_bytes), trust, pid, e["record_sha256"], now)
            if rec is None:
                problems.append("entry %d: record signature: %s" % (i, "; ".join(res["problems"])))
            if deep:
                for b in e.get("blobs") or []:
                    try:
                        if _sha(self.backend.get("blobs/sha256/" + b["sha256"])) != b["sha256"]:
                            problems.append("entry %d: blob %s altered" % (i, b["path"]))
                    except Exception:  # noqa: BLE001
                        problems.append("entry %d: blob %s missing" % (i, b["path"]))
        cps = self.backend.list("log/checkpoints/")
        if entries and not cps:
            problems.append("no signed checkpoint")
        for k in cps:
            ok, info = verify_checkpoint(json.loads(self.backend.get(k)), trust, now)
            if not ok:
                problems.append("%s: %s" % (k, info))
                continue
            n = info["tree_size"]
            if n > len(leaves):
                problems.append("%s: checkpoint size %d exceeds log size %d (entries deleted)" % (k, n, len(leaves)))
            elif M.mth(leaves[:n]).hex() != info["root_hash"]:
                problems.append("%s: root hash does not match the stored entries (log rewritten)" % k)
        return problems


def verify_checkpoint(bundle, trust, now=None):
    """Verify a signed checkpoint bundle. Returns (ok, predicate or reason)."""
    atts = A.load_attestations(bundle)
    res = A.verify(atts[0] if atts else None, trust, "*", CHECKPOINT_PURPOSE, now)
    if not res["verified"]:
        return False, "; ".join("%s: %s" % p for p in res["problems"])
    st = res["statement"]
    if st.get("predicateType") != CHECKPOINT_PREDICATE:
        return False, "not a checkpoint statement"
    pred = dict(st["predicate"])
    pred["signer"] = res["signer"]
    return True, pred


def verify_inclusion(entry, proof, checkpoint_bundle, trust, now=None):
    """Storage-independent check: ``entry`` is in the log the signed checkpoint commits to."""
    ok, info = verify_checkpoint(checkpoint_bundle, trust, now)
    if not ok:
        return False, "checkpoint: %s" % info
    if info["tree_size"] != proof["tree_size"] or info["root_hash"] != proof["root_hash"]:
        return False, "proof is for a different tree than the checkpoint"
    try:
        good = M.verify_inclusion(proof["leaf_index"], proof["tree_size"], M.leaf_hash(_canon(entry)),
                                  [bytes.fromhex(h) for h in proof["audit_path"]], bytes.fromhex(info["root_hash"]))
    except M.TlogError as e:
        return False, str(e)
    return (True, info) if good else (False, "inclusion proof does not reach the checkpoint root")
