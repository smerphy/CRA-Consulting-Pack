"""Signed attestations: DSSE envelopes and Sigstore bundles, verified against a trust policy.

Two signing modes are supported.

Key-based. A DSSE envelope (or a Sigstore bundle whose verification
material is a public-key hint) signed with ECDSA P-256/SHA-256 or Ed25519.
The trust policy lists each key with its validity window, status, purposes
and the products it may sign for. Signatures are computed over the DSSE
pre-authentication encoding PAE(payloadType, payload).

Keyless (Sigstore). A Sigstore bundle carrying a short-lived Fulcio
certificate, a Rekor transparency-log entry with inclusion proof and a DSSE
envelope. Verification is delegated to ``sigstore-python`` against a pinned
trusted root (offline), with an identity policy from the trust policy:
OIDC issuer, subject alternative name (exact or regular expression) and
optional Fulcio certificate extensions such as source repository URI.

The verifier fails closed. Every outcome other than "a trusted key or
identity verified this exact payload" yields a problem code:

  UNSIGNED                  statement supplied without any envelope
  PAYLOAD_TYPE_UNSUPPORTED  DSSE payloadType is not application/vnd.in-toto+json
  NO_TRUSTED_SIGNER         the trust policy configures no key or identity for this product and purpose
  SIGNATURE_INVALID         no configured key verifies the signature (tampered payload or wrong key)
  SIGNER_NOT_AUTHORISED     a key known to the policy verifies, but it is not authorised for this product or purpose
  KEY_REVOKED / KEY_EXPIRED / KEY_NOT_YET_VALID   key status or validity window at signing time
  IDENTITY_MISMATCH         keyless certificate identity does not satisfy the identity policy
  TLOG_MISSING / TLOG_INVALID   transparency-log entry required but absent, or fails offline verification
  SIGSTORE_UNAVAILABLE      keyless bundle but sigstore-python is not installed
  BUNDLE_INVALID            bundle cannot be parsed
  TIMESTAMP_INVALID         an RFC 3161 timestamp in the bundle fails verification against the trusted TSAs
  TIMESTAMP_MISSING         policy requires an independent signing time (log entry or RFC 3161 timestamp) and none verified

Signing time. A key-based signature has no time of its own. The verifier
takes it, in order of preference, from a verified transparency-log entry
(integrated time), from a verified RFC 3161 timestamp over the signature
bytes (``verificationMaterial.timestampVerificationData`` in a Sigstore v0.3
bundle; see ``tsa.py``), or from the gate's clock, and records which source
it used. Key status and validity windows are checked at that time.
  STATEMENT_INVALID         verified payload is not an in-toto Statement
"""

import base64
import datetime as _dt
import hashlib
import json
import os
import re

from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519

from . import transparency as T

INTOTO = "application/vnd.in-toto+json"
STATEMENT_TYPES = ("https://in-toto.io/Statement/v1", "https://in-toto.io/Statement/v0.1")
BUNDLE_MEDIA_PREFIX = "application/vnd.dev.sigstore.bundle"
MODULE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_TRUSTED_ROOT = os.path.join(MODULE_ROOT, "trust", "sigstore-public-good.trusted_root.json")

# Fulcio certificate extension OIDs (Sigstore Fulcio OID registry). V2 values
# are DER UTF8String; 57264.1.1 (issuer, V1) is a raw string.
FULCIO_OIDS = {
    "issuer_v1": "1.3.6.1.4.1.57264.1.1",
    "issuer": "1.3.6.1.4.1.57264.1.8",
    "build_signer_uri": "1.3.6.1.4.1.57264.1.9",
    "build_signer_digest": "1.3.6.1.4.1.57264.1.10",
    "runner_environment": "1.3.6.1.4.1.57264.1.11",
    "source_repository_uri": "1.3.6.1.4.1.57264.1.12",
    "source_repository_digest": "1.3.6.1.4.1.57264.1.13",
    "source_repository_ref": "1.3.6.1.4.1.57264.1.14",
    "source_repository_owner_uri": "1.3.6.1.4.1.57264.1.16",
    "build_config_uri": "1.3.6.1.4.1.57264.1.18",
    "build_trigger": "1.3.6.1.4.1.57264.1.20",
    "run_invocation_uri": "1.3.6.1.4.1.57264.1.21",
    "source_repository_visibility": "1.3.6.1.4.1.57264.1.22",
}


def b64d(s):
    return T.b64d(s)


def b64e(b):
    return base64.b64encode(b).decode("ascii")


def pae(payload_type, payload):
    """DSSE v1 pre-authentication encoding."""
    t = payload_type.encode("utf-8")
    return b"DSSEv1 %d %s %d %s" % (len(t), t, len(payload), payload)


def keyid_for(public_key):
    der = public_key.public_bytes(serialization.Encoding.DER, serialization.PublicFormat.SubjectPublicKeyInfo)
    return "SHA256:" + base64.b64encode(hashlib.sha256(der).digest()).decode().rstrip("=")


# ------------------------------------------------------------- parsing

class Attestation:
    """One signed (or unsigned) attestation as found on disk."""

    def __init__(self, kind, raw, payload_type=None, payload=None, signatures=None, statement=None):
        self.kind = kind                    # "dsse" | "sigstore_bundle" | "statement"
        self.raw = raw
        self.payload_type = payload_type
        self.payload = payload              # bytes
        self.signatures = signatures or []  # [{"keyid":..., "sig": bytes}]
        self._statement = statement

    @property
    def keyless(self):
        vm = (self.raw or {}).get("verificationMaterial") or {}
        return self.kind == "sigstore_bundle" and ("certificate" in vm or "x509CertificateChain" in vm)

    @property
    def tlog_entries(self):
        return ((self.raw or {}).get("verificationMaterial") or {}).get("tlogEntries") or []

    @property
    def rfc3161_timestamps(self):
        """DER TimeStampResp tokens from a Sigstore v0.3 bundle (empty for a bare DSSE envelope)."""
        vm = (self.raw or {}).get("verificationMaterial") or {} if self.kind == "sigstore_bundle" else {}
        tvd = vm.get("timestampVerificationData") or {}
        return [b64d(t["signedTimestamp"]) for t in tvd.get("rfc3161Timestamps") or [] if t.get("signedTimestamp")]

    def unverified_statement(self):
        """Parse the statement WITHOUT verification (selection and display only)."""
        if self._statement is not None:
            return self._statement
        try:
            return json.loads(self.payload)
        except (TypeError, ValueError):
            return None


def _from_obj(obj):
    if not isinstance(obj, dict):
        return []
    if "attestations" in obj and isinstance(obj["attestations"], list):     # npm registry API response
        out = []
        for a in obj["attestations"]:
            out += _from_obj(a.get("bundle") if isinstance(a, dict) and "bundle" in a else a)
        return out
    if str(obj.get("mediaType", "")).startswith(BUNDLE_MEDIA_PREFIX):
        env = obj.get("dsseEnvelope")
        if not env:
            return [Attestation("sigstore_bundle", obj)]                    # message-signature bundle
        return [Attestation("sigstore_bundle", obj, env.get("payloadType"), b64d(env.get("payload", "")),
                            [{"keyid": s.get("keyid"), "sig": b64d(s.get("sig", ""))}
                             for s in env.get("signatures") or []])]
    if "payloadType" in obj and "payload" in obj:
        return [Attestation("dsse", obj, obj.get("payloadType"), b64d(obj["payload"]),
                            [{"keyid": s.get("keyid"), "sig": b64d(s.get("sig", ""))}
                             for s in obj.get("signatures") or []])]
    if obj.get("_type") in STATEMENT_TYPES:
        return [Attestation("statement", obj, statement=obj)]
    return []


def load_attestations(doc_or_text):
    """Accept a parsed JSON object, a JSON string, or JSON Lines (.intoto.jsonl)."""
    if isinstance(doc_or_text, (dict, list)):
        items = doc_or_text if isinstance(doc_or_text, list) else [doc_or_text]
        out = []
        for i in items:
            out += _from_obj(i)
        return out
    text = doc_or_text.decode("utf-8") if isinstance(doc_or_text, bytes) else doc_or_text
    try:
        return load_attestations(json.loads(text))
    except ValueError:
        out = []
        for line in text.splitlines():
            if line.strip():
                out += _from_obj(json.loads(line))
        return out


def load_attestation_file(path):
    with open(path, "r", encoding="utf-8") as fh:
        return load_attestations(fh.read())


def select(atts, predicate_types):
    """Pick the first attestation whose (unverified) predicateType is acceptable."""
    for a in atts:
        st = a.unverified_statement() or {}
        if st.get("predicateType") in predicate_types:
            return a
    return atts[0] if atts else None


# --------------------------------------------------------- trust policy

def _parse_dt(s):
    if not s:
        return None
    return _dt.datetime.fromisoformat(str(s).replace("Z", "+00:00"))


def load_public_key(spec):
    pem = spec.get("public_key_pem")
    if pem:
        return serialization.load_pem_public_key(pem.encode("ascii"))
    der = spec.get("public_key_der_b64")
    if der:
        return serialization.load_der_public_key(b64d(der))
    raise ValueError("key has no public_key_pem or public_key_der_b64")


class TrustPolicy:
    """Accessor over the ``attestation_trust`` block of the gate policy."""

    def __init__(self, cfg, base_dir=None):
        self.cfg = cfg or {}
        self.base_dir = base_dir or os.getcwd()
        self.policy_id = self.cfg.get("trust_policy_id", "unspecified")
        self.keys = self.cfg.get("keys") or {}
        self.revoked = set(self.cfg.get("revoked_keyids") or [])
        self._tr = None

    def rules(self, product_id, purpose):
        p = ((self.cfg.get("products") or {}).get(product_id) or {}).get(purpose)
        if p is None:
            p = ((self.cfg.get("products") or {}).get("*") or {}).get(purpose) or {}
        return p

    def builder(self, builder_id):
        return (self.cfg.get("builders") or {}).get(builder_id)

    def trusted_root(self):
        if self._tr is None:
            path = (self.cfg.get("sigstore") or {}).get("trusted_root") or DEFAULT_TRUSTED_ROOT
            if not os.path.isabs(path):
                cand = os.path.join(self.base_dir, path)
                path = cand if os.path.exists(cand) else os.path.join(MODULE_ROOT, path)
            self._tr_path = path
            with open(path, "r", encoding="utf-8") as fh:
                self._tr = json.load(fh)
        return self._tr

    def trusted_root_path(self):
        self.trusted_root()
        return self._tr_path

    def timestamp_authorities(self):
        """RFC 3161 authorities trusted for signing time (``timestamp_authorities`` block)."""
        if not hasattr(self, "_tsas"):
            from . import tsa as _tsa
            self._tsas = _tsa.authorities_from_policy(self.cfg, self.base_dir)
        return self._tsas


# --------------------------------------------------------- verification

def _result(att, purpose):
    return {"purpose": purpose, "envelope": att.kind if att else None, "verified": False, "method": "none",
            "signer": None, "tlog": None, "problems": [], "statement": None, "payload_type": att.payload_type
            if att else None}


def _verify_raw(key, sig, data):
    if isinstance(key, ec.EllipticCurvePublicKey):
        if key.curve.name not in ("secp256r1", "secp384r1"):
            raise InvalidSignature("unsupported curve")
        h = hashes.SHA256() if key.curve.name == "secp256r1" else hashes.SHA384()
        key.verify(sig, data, ec.ECDSA(h))
    elif isinstance(key, ed25519.Ed25519PublicKey):
        key.verify(sig, data)
    else:
        raise InvalidSignature("unsupported key type")


def _key_status(name, spec, keyid, when):
    if spec.get("status") == "revoked" or keyid in spec.get("_revoked_set", ()):
        return "KEY_REVOKED", "key %s is revoked (%s)" % (name, spec.get("revocation_reason", "no reason recorded"))
    nb, na = _parse_dt(spec.get("not_before")), _parse_dt(spec.get("not_after"))
    if nb and when < nb:
        return "KEY_NOT_YET_VALID", "key %s not valid before %s (signing time %s)" % (name, spec["not_before"], when.isoformat())
    if na and when > na:
        return "KEY_EXPIRED", "key %s expired %s (signing time %s)" % (name, spec["not_after"], when.isoformat())
    return None


def _verify_key(att, trust, rules, purpose, product_id, now, res):
    allowed = list(rules.get("keys") or [])
    if not allowed:
        res["problems"].append(("NO_TRUSTED_SIGNER", "trust policy configures no signing key for %s %s" % (
            product_id, purpose)))
        return
    if not att.signatures:
        res["problems"].append(("SIGNATURE_INVALID", "envelope carries no signatures"))
        return
    data = pae(att.payload_type, att.payload)
    hit = None
    for s in att.signatures:
        for name in allowed:
            spec = trust.keys.get(name)
            if not spec:
                continue
            try:
                _verify_raw(load_public_key(spec), s["sig"], data)
                hit = (name, spec, s)
                break
            except (InvalidSignature, ValueError):
                continue
        if hit:
            break
    if not hit:
        # Does a key the policy knows, but has not authorised here, verify it?
        for s in att.signatures:
            for name, spec in trust.keys.items():
                if name in allowed:
                    continue
                try:
                    _verify_raw(load_public_key(spec), s["sig"], data)
                    res["problems"].append(("SIGNER_NOT_AUTHORISED", "signed by key %s, which is not authorised "
                                            "for %s %s" % (name, product_id, purpose)))
                    return
                except (InvalidSignature, ValueError):
                    continue
        res["problems"].append(("SIGNATURE_INVALID", "no trusted key verifies the envelope signature over "
                                "PAE(payloadType, payload)"))
        return
    name, spec, s = hit
    pub = load_public_key(spec)
    kid = keyid_for(pub)
    res["method"] = "key"
    res["signer"] = {"key": name, "keyid": spec.get("keyid") or kid, "algorithm": spec.get("algorithm"),
                     "owner": spec.get("owner")}
    signing_time = now
    if att.tlog_entries:
        try:
            tl = T.verify_entry(att.tlog_entries[0], att.payload, [x["sig"] for x in att.signatures], pub,
                                trust.trusted_root())
            res["tlog"] = tl
            signing_time = _parse_dt(tl["integrated_time"])
        except (T.TlogError, KeyError, ValueError) as e:
            res["problems"].append(("TLOG_INVALID", "transparency-log entry failed offline verification: %s" % e))
            return
    elif rules.get("require_tlog"):
        res["problems"].append(("TLOG_MISSING", "policy requires a transparency-log entry for this signer"))
        return
    source = "transparency log integrated time" if res["tlog"] else "gate evaluation time"
    tokens = att.rfc3161_timestamps
    if tokens:
        from . import tsa as _tsa
        stamps = []
        for tok in tokens:
            try:
                stamps.append(_tsa.verify_response(tok, s["sig"], trust.timestamp_authorities()))
            except _tsa.TimestampError as e:
                res["problems"].append(("TIMESTAMP_INVALID", "RFC 3161 timestamp over the signature failed "
                                        "verification: %s" % e))
                return
        res["signer"]["timestamps"] = stamps
        if not res["tlog"]:
            signing_time = min(_parse_dt(t["gen_time"]) for t in stamps)
            source = "RFC 3161 timestamp (%s)" % ", ".join(sorted({t["tsa"] for t in stamps}))
    if rules.get("require_timestamp") and not res["tlog"] and not tokens:
        res["problems"].append(("TIMESTAMP_MISSING", "policy requires an independent signing time (transparency-log "
                                "entry or RFC 3161 timestamp) for this signer; none present"))
        return
    res["signer"]["signing_time"] = signing_time.isoformat().replace("+00:00", "Z")
    res["signer"]["signing_time_source"] = source
    spec = dict(spec, _revoked_set=trust.revoked)
    st = _key_status(name, spec, spec.get("keyid") or kid, signing_time)
    if st:
        res["problems"].append(st)
        return
    if spec.get("purposes") and purpose not in spec["purposes"]:
        res["problems"].append(("SIGNER_NOT_AUTHORISED", "key %s is not authorised for purpose %s" % (name, purpose)))
        return
    res["verified"] = True


def _der_utf8(raw):
    if raw[:1] == b"\x0c":
        n = raw[1]
        off = 2
        if n & 0x80:
            ln = n & 0x7F
            n = int.from_bytes(raw[2:2 + ln], "big")
            off = 2 + ln
        return raw[off:off + n].decode("utf-8")
    return raw.decode("utf-8")


def cert_identity(cert):
    from cryptography import x509
    out = {"san": None, "issuer": None, "extensions": {}}
    try:
        san = cert.extensions.get_extension_for_class(x509.SubjectAlternativeName).value
        vals = san.get_values_for_type(x509.UniformResourceIdentifier) or san.get_values_for_type(x509.RFC822Name)
        out["san"] = vals[0] if vals else None
    except x509.ExtensionNotFound:
        pass
    by_oid = {e.oid.dotted_string: e for e in cert.extensions}
    for name, oid in FULCIO_OIDS.items():
        e = by_oid.get(oid)
        if e is None:
            continue
        raw = e.value.value
        out["extensions"][name] = raw.decode("utf-8") if name == "issuer_v1" else _der_utf8(raw)
    out["issuer"] = out["extensions"].get("issuer") or out["extensions"].get("issuer_v1")
    out["not_before"] = cert.not_valid_before_utc.isoformat().replace("+00:00", "Z")
    out["not_after"] = cert.not_valid_after_utc.isoformat().replace("+00:00", "Z")
    out["serial"] = format(cert.serial_number, "x")
    return out


def identity_matches(ident, rule):
    """Return None when the certificate identity satisfies one rule, else a reason."""
    if rule.get("issuer") and ident.get("issuer") != rule["issuer"]:
        return "issuer %r is not %r" % (ident.get("issuer"), rule["issuer"])
    if rule.get("san") and ident.get("san") != rule["san"]:
        return "SAN %r is not %r" % (ident.get("san"), rule["san"])
    if rule.get("san_regex") and not re.fullmatch(rule["san_regex"], ident.get("san") or ""):
        return "SAN %r does not match %r" % (ident.get("san"), rule["san_regex"])
    for k, v in (rule.get("extensions") or {}).items():
        if ident["extensions"].get(k) != v:
            return "certificate extension %s=%r, expected %r" % (k, ident["extensions"].get(k), v)
    return None


class _IdentityPolicy:
    """sigstore-python VerificationPolicy: any configured identity rule matches."""

    def __init__(self, rules):
        self.rules = rules
        self.failed = None
        self.matched = None

    def verify(self, cert):
        from sigstore.errors import VerificationError
        ident = cert_identity(cert)
        reasons = []
        for r in self.rules:
            why = identity_matches(ident, r)
            if why is None:
                self.matched = r
                return
            reasons.append(why)
        self.failed = "; ".join(reasons) or "no identity rules"
        raise VerificationError("certificate identity rejected: %s" % self.failed)


def _verify_sigstore(att, trust, rules, purpose, product_id, res):
    idents = list(rules.get("identities") or [])
    if not idents:
        res["problems"].append(("NO_TRUSTED_SIGNER", "trust policy configures no keyless identity for %s %s" % (
            product_id, purpose)))
        return
    try:
        from sigstore.errors import Error as SigstoreError
        from sigstore.models import Bundle, TrustedRoot
        from sigstore.verify import Verifier
    except ImportError:
        res["problems"].append(("SIGSTORE_UNAVAILABLE", "keyless bundle but sigstore-python is not installed"))
        return
    try:
        bundle = Bundle.from_json(json.dumps(att.raw))
    except Exception as e:  # noqa: BLE001 (any parse failure is a fail-closed bundle error)
        res["problems"].append(("BUNDLE_INVALID", "Sigstore bundle cannot be parsed: %s" % e))
        return
    policy = _IdentityPolicy(idents)
    try:
        verifier = Verifier(trusted_root=TrustedRoot.from_file(trust.trusted_root_path()))
        ptype, payload = verifier.verify_dsse(bundle, policy)
    except SigstoreError as e:
        if policy.failed:
            res["problems"].append(("IDENTITY_MISMATCH", "keyless certificate %s" % policy.failed))
        else:
            res["problems"].append(("SIGNATURE_INVALID", "Sigstore verification failed: %s" % e))
        return
    except Exception as e:  # noqa: BLE001
        res["problems"].append(("SIGNATURE_INVALID", "Sigstore verification error: %s" % e))
        return
    ident = cert_identity(bundle.signing_certificate)
    res["method"] = "sigstore-keyless"
    res["signer"] = {"identity_rule": (policy.matched or {}).get("name"), "san": ident["san"], "issuer": ident["issuer"], "certificate_serial": ident["serial"],
                     "certificate_not_before": ident["not_before"], "certificate_not_after": ident["not_after"],
                     "extensions": {k: v for k, v in ident["extensions"].items()
                                    if k in ("source_repository_uri", "source_repository_digest",
                                             "source_repository_ref", "runner_environment", "build_signer_uri",
                                             "run_invocation_uri", "build_trigger")},
                     "trusted_root_sha256": hashlib.sha256(open(trust.trusted_root_path(), "rb").read()).hexdigest()}
    # Independent offline re-check of the log entry with this module's own code.
    tl = {"verified_by": "sigstore-python"}
    if att.tlog_entries:
        try:
            tl.update(T.verify_entry(att.tlog_entries[0], payload, [s["sig"] for s in att.signatures],
                                     bundle.signing_certificate.public_key(), trust.trusted_root()))
            tl["verified_by"] = "sigstore-python and cra_evidence.transparency"
        except (T.TlogError, KeyError, ValueError) as e:
            res["problems"].append(("TLOG_INVALID", "independent transparency-log check failed: %s" % e))
            return
    res["tlog"] = tl
    att.payload_type, att.payload = ptype, payload
    res["verified"] = True


def verify(att, trust, product_id, purpose, now=None):
    """Verify one attestation for (product, purpose). Returns a result dict.

    ``statement`` is set only from bytes whose signature verified.
    """
    now = now or _dt.datetime.now(_dt.timezone.utc)
    res = _result(att, purpose)
    if att is None:
        res["problems"].append(("UNSIGNED", "no attestation supplied"))
        return res
    if att.kind == "statement":
        res["problems"].append(("UNSIGNED", "bare in-toto Statement without a DSSE envelope or Sigstore bundle"))
        return res
    if att.payload is None:
        res["problems"].append(("BUNDLE_INVALID", "bundle carries no DSSE envelope"))
        return res
    if att.payload_type != INTOTO:
        res["problems"].append(("PAYLOAD_TYPE_UNSUPPORTED", "payloadType %r is not %s" % (att.payload_type, INTOTO)))
        return res
    rules = trust.rules(product_id, purpose)
    if att.keyless:
        _verify_sigstore(att, trust, rules, purpose, product_id, res)
    else:
        _verify_key(att, trust, rules, purpose, product_id, now, res)
    if res["verified"]:
        try:
            st = json.loads(att.payload)
        except ValueError:
            st = None
        if not isinstance(st, dict) or st.get("_type") not in STATEMENT_TYPES:
            res["verified"] = False
            res["problems"].append(("STATEMENT_INVALID", "verified payload is not an in-toto Statement"))
        else:
            res["statement"] = st
    return res


def subject_matches(statement, digests):
    """True if any subject digest equals the artefact digest for a shared algorithm."""
    for s in (statement or {}).get("subject") or []:
        d = s.get("digest") or {}
        for alg in ("sha256", "sha512"):
            if d.get(alg) and digests.get(alg) and d[alg].lower() == digests[alg].lower():
                return alg
    return None


def summary(res, trust, slsa_level=None):
    """Record-safe summary (no statement body)."""
    out = {"verified": res["verified"], "method": res["method"], "envelope": res["envelope"] or "none",
           "signer": res["signer"], "tlog": res["tlog"], "trust_policy_id": trust.policy_id,
           "problems": ["%s: %s" % p for p in res["problems"]]}
    if slsa_level is not None:
        out["slsa_build_level"] = slsa_level
    return out


# ------------------------------------------------------------- signing

def sign_envelope(statement, private_key, keyid=None):
    """Create a DSSE envelope over an in-toto Statement (key-based signing)."""
    payload = json.dumps(statement, separators=(",", ":"), sort_keys=True).encode("utf-8")
    data = pae(INTOTO, payload)
    if isinstance(private_key, ec.EllipticCurvePrivateKey):
        sig = private_key.sign(data, ec.ECDSA(hashes.SHA256(), deterministic_signing=True))
    elif isinstance(private_key, ed25519.Ed25519PrivateKey):
        sig = private_key.sign(data)
    else:
        raise TypeError("unsupported private key type")
    return {"payloadType": INTOTO, "payload": b64e(payload),
            "signatures": [{"keyid": keyid or keyid_for(private_key.public_key()), "sig": b64e(sig)}]}
