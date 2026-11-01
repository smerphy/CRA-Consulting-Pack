"""Sign the evidence record itself as an in-toto attestation, and verify it on read.

The record is the predicate of an in-toto Statement v1 whose subject is the
shipped artefact (its SHA-256 and SHA-512 digests), so the signature binds
the CRA evidence to exactly one artefact. The predicate type is

    https://aldermoor.example/attestations/cra-evidence-record/v1

(an organisation-defined type: in-toto lets any producer define a predicate
type by URI; there is no standard CRA predicate). The statement is wrapped in
a DSSE envelope signed through a ``KeyProvider`` (KMS, HSM or, for tests,
a local file) and carried in a Sigstore bundle v0.3 whose
``timestampVerificationData`` holds an RFC 3161 token over the signature
bytes. A transparency-log entry (Rekor) is optional and, when present, is
verified offline like any other bundle.

``verify_record_bundle`` is the read path: a stored record is returned to a
caller only if the signature verifies against the trust policy (purpose
``evidence_record``), the signing time comes from a verified timestamp or
log entry where the policy requires it, the predicate type is right, and the
canonical predicate digest equals the digest the log recorded.
"""

import hashlib
import json

from . import attest as A
from . import keys as K

PREDICATE_TYPE = "https://aldermoor.example/attestations/cra-evidence-record/v1"
PURPOSE = "evidence_record"


def canonical(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":")).encode("utf-8")


def record_digest(record):
    return hashlib.sha256(canonical(record)).hexdigest()


def record_statement(record):
    art = (record.get("version") or {}).get("artefact") or {}
    digs = {k: v for k, v in (art.get("digests") or {}).items() if k in ("sha256", "sha512")}
    if digs:
        name = (art.get("uri") or "").rsplit("/", 1)[-1] or record["record_id"]
        subject = [{"name": name, "digest": digs}]
    else:   # no artefact (should not pass the gate): bind to the record itself
        subject = [{"name": record["record_id"], "digest": {"sha256": record_digest(record)}}]
    return {"_type": "https://in-toto.io/Statement/v1", "subject": subject,
            "predicateType": PREDICATE_TYPE, "predicate": record}


def sign_record(record, provider, tsa=None):
    """Return a Sigstore v0.3 bundle (dict) attesting ``record``."""
    return K.sign_and_timestamp(record_statement(record), provider, tsa)


def verify_record_bundle(bundle, trust, product_id, expected_sha256=None, now=None):
    """Verify a signed record bundle. Returns (record or None, result dict).

    ``result`` has ``verified``, ``signer`` (with signing time and its
    source), ``record_sha256`` and ``problems`` (codes as in attest.py plus
    RECORD_PREDICATE_TYPE, RECORD_DIGEST_MISMATCH, RECORD_SUBJECT_MISMATCH).
    """
    atts = A.load_attestations(bundle)
    att = atts[0] if atts else None
    res = A.verify(att, trust, product_id, PURPOSE, now)
    out = {"verified": res["verified"], "method": res["method"], "signer": res["signer"], "tlog": res["tlog"],
           "problems": ["%s: %s" % p for p in res["problems"]], "record_sha256": None}
    if not res["verified"]:
        return None, out
    st = res["statement"]
    if st.get("predicateType") != PREDICATE_TYPE:
        out["verified"] = False
        out["problems"].append("RECORD_PREDICATE_TYPE: %r is not %s" % (st.get("predicateType"), PREDICATE_TYPE))
        return None, out
    record = st.get("predicate") or {}
    dig = record_digest(record)
    out["record_sha256"] = dig
    if expected_sha256 and dig != expected_sha256:
        out["verified"] = False
        out["problems"].append("RECORD_DIGEST_MISMATCH: signed record digest %s differs from logged %s"
                               % (dig, expected_sha256))
        return None, out
    art = ((record.get("version") or {}).get("artefact") or {}).get("digests") or {}
    if art and not A.subject_matches(st, art):
        out["verified"] = False
        out["problems"].append("RECORD_SUBJECT_MISMATCH: statement subject is not the record's artefact")
        return None, out
    return record, out
