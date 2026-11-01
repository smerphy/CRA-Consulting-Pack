"""Offline verification of Rekor v1 transparency-log entries carried in a Sigstore bundle.

Used for key-signed bundles (for example the npm registry's publish
attestation) and as an independent second check on keyless bundles that
``sigstore-python`` has already verified. Everything here runs offline
against a trusted root (the Sigstore ``trusted_root.json`` format):

1. Merkle inclusion proof: the entry's leaf hash, SHA-256(0x00 || body),
   hashes up the audit path to the proof's root hash (RFC 9162 section
   2.1.3.2 algorithm; Rekor v1 uses RFC 6962 hashing).
2. Checkpoint: the signed note commits to the same tree size and root hash
   and is signed by the log key named by the entry's log id.
3. Signed entry timestamp (inclusion promise): the log's signature over
   canonical JSON {body, integratedTime, logID, logIndex}.
4. Body binding: for ``dsse`` 0.0.1 entries the logged payload hash equals
   SHA-256 of the envelope payload, the logged signature equals the
   envelope signature and the logged verifier equals the key or certificate
   that verified it.
5. Log-key validity: the integrated time falls inside the key's validFor window.

What this cannot do offline: prove the checkpoint is the same one other
parties see (split-view protection needs witnessing or online gossip), or
prove the entry was not later removed from a log that was rotated. Both are
recorded as residual risks in paper.md.
"""

import base64
import datetime as _dt
import hashlib
import json

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519
from cryptography import x509


class TlogError(ValueError):
    """Raised when a transparency-log entry fails verification."""


def b64d(s):
    s = s.strip()
    pad = "=" * (-len(s) % 4)
    try:
        return base64.b64decode(s + pad, validate=False)
    except Exception:
        return base64.urlsafe_b64decode(s + pad)


def _h(b):
    return hashlib.sha256(b).digest()


def root_from_inclusion_proof(index, size, leaf_hash, proof):
    """RFC 9162 2.1.3.2: recompute the tree root from an inclusion proof."""
    if index < 0 or index >= size:
        raise TlogError("leaf index %d outside tree of size %d" % (index, size))
    fn, sn, r = index, size - 1, leaf_hash
    for p in proof:
        if sn == 0:
            raise TlogError("inclusion proof longer than the tree height")
        if fn & 1 or fn == sn:
            r = _h(b"\x01" + p + r)
            if not fn & 1:
                while True:
                    fn >>= 1
                    sn >>= 1
                    if fn & 1 or fn == 0:
                        break
        else:
            r = _h(b"\x01" + r + p)
        fn >>= 1
        sn >>= 1
    if sn != 0:
        raise TlogError("inclusion proof shorter than the tree height")
    return r


def _parse_time(s):
    return _dt.datetime.fromisoformat(s.replace("Z", "+00:00")) if s else None


def log_keys(trusted_root):
    """Map base64 log id -> {key, start, end, url} from a trusted_root.json dict."""
    out = {}
    for t in trusted_root.get("tlogs") or []:
        pk = t.get("publicKey") or {}
        raw = pk.get("rawBytes")
        if not raw:
            continue
        key = serialization.load_der_public_key(b64d(raw))
        vf = pk.get("validFor") or {}
        out[(t.get("logId") or {}).get("keyId")] = {
            "key": key, "url": t.get("baseUrl"),
            "start": _parse_time(vf.get("start")), "end": _parse_time(vf.get("end")),
        }
    return out


def _verify_sig(key, sig, data):
    if isinstance(key, ec.EllipticCurvePublicKey):
        key.verify(sig, data, ec.ECDSA(hashes.SHA256()))
    elif isinstance(key, ed25519.Ed25519PublicKey):
        key.verify(sig, data)
    else:
        raise TlogError("unsupported log key type %s" % type(key).__name__)


def verify_checkpoint(note, key, size, root_hash):
    """Verify a signed-note checkpoint and that it commits to (size, root)."""
    if "\n\n" not in note:
        raise TlogError("checkpoint is not a signed note")
    body, sigs = note.split("\n\n", 1)
    body += "\n"
    lines = body.split("\n")
    if len(lines) < 3:
        raise TlogError("checkpoint body too short")
    origin, csize, croot = lines[0], int(lines[1]), b64d(lines[2])
    if csize != size or croot != root_hash:
        raise TlogError("checkpoint does not commit to the proof's tree size and root")
    ok = False
    for line in sigs.strip().split("\n"):
        parts = line.split(" ")
        if len(parts) < 3 or not parts[0].startswith("—"):
            continue
        blob = b64d(parts[-1])
        try:
            _verify_sig(key, blob[4:], body.encode("utf-8"))
            ok = True
            break
        except InvalidSignature:
            continue
    if not ok:
        raise TlogError("checkpoint signature does not verify under the log key")
    return origin


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def _public_key_from_verifier(blob):
    """Rekor 'verifier' fields hold a base64 PEM public key or certificate."""
    pem = b64d(blob)
    if b"BEGIN CERTIFICATE" in pem:
        return x509.load_pem_x509_certificate(pem).public_key()
    return serialization.load_pem_public_key(pem)


def _same_key(a, b):
    f = serialization.PublicFormat.SubjectPublicKeyInfo
    e = serialization.Encoding.DER
    return a.public_bytes(e, f) == b.public_bytes(e, f)


def verify_entry(entry, payload, signatures, signer_key, trusted_root):
    """Verify one Rekor v1 tlog entry from a Sigstore bundle.

    entry: the bundle's tlogEntries[i] dict.
    payload: DSSE payload bytes; signatures: list of raw signature bytes.
    signer_key: the public key that verified the envelope.
    Returns a summary dict; raises TlogError on any failure.
    """
    kv = entry.get("kindVersion") or {}
    if (kv.get("kind"), kv.get("version")) != ("dsse", "0.0.1"):
        raise TlogError("unsupported entry kind %s/%s for offline check" % (kv.get("kind"), kv.get("version")))
    body_b64 = entry.get("canonicalizedBody")
    if not body_b64:
        raise TlogError("entry has no canonicalized body")
    body = b64d(body_b64)
    keys = log_keys(trusted_root)
    log_id = (entry.get("logId") or {}).get("keyId")
    lk = keys.get(log_id)
    if not lk:
        raise TlogError("log id %s is not in the trusted root" % log_id)
    itime = int(entry.get("integratedTime", 0))
    t = _dt.datetime.fromtimestamp(itime, _dt.timezone.utc)
    if (lk["start"] and t < lk["start"]) or (lk["end"] and t > lk["end"]):
        raise TlogError("integrated time outside the log key's validity window")

    # 4. body binding
    spec = json.loads(body).get("spec") or {}
    if (spec.get("payloadHash") or {}).get("value") != hashlib.sha256(payload).hexdigest():
        raise TlogError("logged payload hash does not match the envelope payload")
    logged = spec.get("signatures") or []
    if not any(b64d(s.get("signature", "")) in signatures for s in logged):
        raise TlogError("logged signature does not match the envelope signature")
    if not any(_same_key(_public_key_from_verifier(s["verifier"]), signer_key) for s in logged if s.get("verifier")):
        raise TlogError("logged verifier is not the key that verified the envelope")

    # 1. + 2. inclusion proof and checkpoint
    proof = entry.get("inclusionProof")
    checked = {"inclusion_proof": False, "checkpoint": False, "signed_entry_timestamp": False}
    if proof:
        idx, size = int(proof["logIndex"]), int(proof["treeSize"])
        root = root_from_inclusion_proof(idx, size, _h(b"\x00" + body), [b64d(h) for h in proof.get("hashes") or []])
        if root != b64d(proof["rootHash"]):
            raise TlogError("inclusion proof does not reproduce the root hash")
        checked["inclusion_proof"] = True
        cp = (proof.get("checkpoint") or {}).get("envelope")
        if cp:
            verify_checkpoint(cp, lk["key"], size, root)
            checked["checkpoint"] = True
    # 3. signed entry timestamp
    set_b64 = (entry.get("inclusionPromise") or {}).get("signedEntryTimestamp")
    if set_b64:
        payload_set = _canon({"body": body_b64, "integratedTime": itime,
                              "logID": b64d(log_id).hex(), "logIndex": int(entry["logIndex"])})
        try:
            _verify_sig(lk["key"], b64d(set_b64), payload_set)
        except InvalidSignature:
            raise TlogError("signed entry timestamp does not verify under the log key")
        checked["signed_entry_timestamp"] = True
    if not (checked["inclusion_proof"] and checked["checkpoint"]) and not checked["signed_entry_timestamp"]:
        raise TlogError("entry has neither a verifiable inclusion proof nor a signed entry timestamp")
    return {"log_url": lk["url"], "log_index": int(entry.get("logIndex", -1)), "integrated_time":
            t.isoformat().replace("+00:00", "Z"), **checked}
