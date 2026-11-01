"""RFC 3161 time-stamping: request, verify, and a local test authority.

Why: a key-based DSSE signature without a transparency-log entry carries no
independent time. The gate would otherwise take its own clock as the signing
time, so a key revoked or expired today could not be distinguished from one
that was valid when the evidence was signed. An RFC 3161 token from a
time-stamping authority (TSA) binds a hash of the signature bytes to the
TSA's clock under the TSA's own key.

Conventions (aligned with the Sigstore bundle v0.3
``timestampVerificationData.rfc3161Timestamps[].signedTimestamp``): the token
is the DER-encoded TimeStampResp, and the time-stamped message is the
signature bytes (for DSSE, the envelope signature).

This module provides:
- ``build_request`` / ``TimestampClient``: TimeStampReq over HTTP
  (``application/timestamp-query``), with a random nonce checked on reply.
- ``verify_response``: full verification written for this module with
  ``asn1crypto`` (parsing) and ``cryptography`` (signatures, certificates):
  PKI status; messageImprint equals the hash of the message; nonce; CMS
  SignedData with content type id-ct-TSTInfo; signed attributes carry the
  content type and a message digest equal to the hash of the TSTInfo; the
  signer certificate is identified by the SignerIdentifier and, where
  present, by the ESS signing-certificate(-v2) hash; the signature over the
  DER SET OF signed attributes verifies (ECDSA or RSA PKCS#1 v1.5); the
  signer certificate chains to a trusted root (at most one intermediate);
  its extended key usage is id-kp-timeStamping and critical (RFC 3161
  section 2.3); genTime lies inside the signer certificate's validity and the
  authority's configured validity window.
- ``LocalTSA``: a self-contained TSA (generated EC P-256 root and TSA
  certificate) for tests, the pilot and the benchmark, served in-process or
  over HTTP on 127.0.0.1. It is a test authority, not a trusted service.

Failure raises ``TimestampError`` with a code: TSA_STATUS, TSA_PARSE,
TSA_IMPRINT, TSA_NONCE, TSA_CONTENT, TSA_DIGEST, TSA_SIGNER, TSA_SIGNATURE,
TSA_CHAIN, TSA_EKU, TSA_TIME.
"""

import base64
import datetime as _dt
import hashlib
import http.server
import os
import secrets
import threading
import urllib.request

from asn1crypto import algos, cms, core, tsp
from asn1crypto import x509 as ax509
from cryptography import x509
from cryptography.exceptions import InvalidSignature
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, padding, rsa
from cryptography.x509.oid import ExtendedKeyUsageOID, NameOID

HASHES = {"sha256": hashlib.sha256, "sha384": hashlib.sha384, "sha512": hashlib.sha512}
CHASH = {"sha256": hashes.SHA256, "sha384": hashes.SHA384, "sha512": hashes.SHA512}
DEFAULT_POLICY = "1.3.6.1.4.1.57264.2"   # illustrative policy OID used by the local test TSA
EKU_TIMESTAMPING = ExtendedKeyUsageOID.TIME_STAMPING


class TimestampError(ValueError):
    def __init__(self, code, message):
        super().__init__("%s: %s" % (code, message))
        self.code = code


def _now():
    return _dt.datetime.now(_dt.timezone.utc)


# ------------------------------------------------------------ requests

def build_request(message, hash_alg="sha256", nonce=None, cert_req=True, policy=None):
    """Return (der, nonce) for a TimeStampReq over ``message``."""
    nonce = secrets.randbits(63) if nonce is None else nonce
    req = {"version": "v1",
           "message_imprint": {"hash_algorithm": {"algorithm": hash_alg},
                               "hashed_message": HASHES[hash_alg](message).digest()},
           "nonce": nonce, "cert_req": cert_req}
    if policy:
        req["req_policy"] = policy
    return tsp.TimeStampReq(req).dump(), nonce


class TimestampClient:
    """RFC 3161 client over HTTP POST (RFC 3161 section 3.4)."""

    def __init__(self, url, timeout=10.0, hash_alg="sha256"):
        self.url, self.timeout, self.hash_alg = url, timeout, hash_alg
        self.name = url

    def timestamp(self, message):
        der, nonce = build_request(message, self.hash_alg)
        req = urllib.request.Request(self.url, data=der, method="POST",
                                     headers={"Content-Type": "application/timestamp-query",
                                              "Accept": "application/timestamp-reply"})
        with urllib.request.urlopen(req, timeout=self.timeout) as r:  # noqa: S310 (configured TSA URL)
            body = r.read()
        check_response(body, message, nonce)
        return body


def check_response(resp_der, message, nonce=None):
    """Light client-side check before storing: status, imprint and nonce."""
    resp = _load(resp_der)
    tst = _tst_info(resp)
    _check_imprint(tst, message)
    if nonce is not None and (tst["nonce"].native if tst["nonce"].native is not None else None) != nonce:
        raise TimestampError("TSA_NONCE", "nonce in reply does not match the request")
    return tst


# ---------------------------------------------------------- verification

def _load(resp_der):
    try:
        resp = tsp.TimeStampResp.load(resp_der)
        status = resp["status"]["status"].native
    except Exception as e:  # noqa: BLE001
        raise TimestampError("TSA_PARSE", "not a TimeStampResp: %s" % e)
    if status not in ("granted", "granted_with_mods"):
        raise TimestampError("TSA_STATUS", "TSA status %s" % status)
    return resp


def _tst_info(resp):
    token = resp["time_stamp_token"]
    if token["content_type"].native != "signed_data":
        raise TimestampError("TSA_CONTENT", "token is not CMS SignedData")
    encap = token["content"]["encap_content_info"]
    if encap["content_type"].native != "tst_info":
        raise TimestampError("TSA_CONTENT", "encapsulated content is not id-ct-TSTInfo")
    return encap["content"].parsed


def _check_imprint(tst, message):
    alg = tst["message_imprint"]["hash_algorithm"]["algorithm"].native
    if alg not in HASHES:
        raise TimestampError("TSA_IMPRINT", "unsupported imprint hash %s" % alg)
    if tst["message_imprint"]["hashed_message"].native != HASHES[alg](message).digest():
        raise TimestampError("TSA_IMPRINT", "messageImprint does not match the time-stamped message")
    return alg


def _load_cert(c):
    if isinstance(c, x509.Certificate):
        return c
    if isinstance(c, bytes) and c.startswith(b"-----BEGIN"):
        return x509.load_pem_x509_certificate(c)
    if isinstance(c, str):
        return x509.load_pem_x509_certificate(c.encode("ascii"))
    return x509.load_der_x509_certificate(c)


def _verify_sig(pub, sig, data, alg):
    h = CHASH.get(alg, hashes.SHA256)()
    if isinstance(pub, ec.EllipticCurvePublicKey):
        pub.verify(sig, data, ec.ECDSA(h))
    elif isinstance(pub, rsa.RSAPublicKey):
        pub.verify(sig, data, padding.PKCS1v15(), h)
    else:
        raise InvalidSignature("unsupported TSA key type")


def _issued_by(child, parent):
    try:
        child.verify_directly_issued_by(parent)
        return True
    except (ValueError, TypeError, InvalidSignature):
        return False


def verify_response(resp_der, message, authorities, nonce=None):
    """Verify a TimeStampResp over ``message`` against trusted ``authorities``.

    ``authorities``: list of dicts {name, roots: [cert], leaf: cert|None,
    valid_for: {start, end}|None}; certificates as PEM strings, DER bytes
    or ``cryptography`` objects. Returns a dict describing the token.
    """
    resp = _load(resp_der)
    tst = _tst_info(resp)
    alg = _check_imprint(tst, message)
    if nonce is not None and tst["nonce"].native != nonce:
        raise TimestampError("TSA_NONCE", "nonce mismatch")
    sd = resp["time_stamp_token"]["content"]
    tst_bytes = sd["encap_content_info"]["content"].contents
    infos = sd["signer_infos"]
    if len(infos) != 1:
        raise TimestampError("TSA_SIGNER", "expected exactly one SignerInfo, found %d" % len(infos))
    si = infos[0]
    dalg = si["digest_algorithm"]["algorithm"].native
    if dalg not in HASHES:
        raise TimestampError("TSA_DIGEST", "unsupported digest algorithm %s" % dalg)
    attrs = {a["type"].native: a["values"] for a in si["signed_attrs"]} if si["signed_attrs"] else {}
    if not attrs:
        raise TimestampError("TSA_DIGEST", "SignerInfo has no signed attributes")
    if attrs.get("content_type") is None or attrs["content_type"][0].native != "tst_info":
        raise TimestampError("TSA_DIGEST", "signed content-type attribute is not id-ct-TSTInfo")
    if attrs.get("message_digest") is None or attrs["message_digest"][0].native != HASHES[dalg](tst_bytes).digest():
        raise TimestampError("TSA_DIGEST", "signed message-digest does not match the TSTInfo")

    embedded = [_load_cert(c.chosen.dump()) for c in (sd["certificates"] or []) if c.name == "certificate"]
    sid = si["sid"]
    gen_time = tst["gen_time"].native
    errors = []
    for auth in authorities or []:
        roots = [_load_cert(r) for r in auth.get("roots") or []]
        pinned = _load_cert(auth["leaf"]) if auth.get("leaf") else None
        candidates = ([pinned] if pinned else []) + embedded
        signer = None
        for c in candidates:
            if sid.name == "issuer_and_serial_number":
                ias = sid.chosen
                if c.serial_number == ias["serial_number"].native and \
                        c.issuer.public_bytes() == ias["issuer"].dump():
                    signer = c
                    break
            elif sid.name == "subject_key_identifier":
                try:
                    ski = c.extensions.get_extension_for_class(x509.SubjectKeyIdentifier).value.digest
                except x509.ExtensionNotFound:
                    continue
                if ski == sid.chosen.native:
                    signer = c
                    break
        if signer is None:
            errors.append("%s: signer certificate not found" % auth.get("name"))
            continue
        cert_der = signer.public_bytes(serialization.Encoding.DER)
        for key, halg in (("signing_certificate_v2", None), ("signing_certificate", "sha1")):
            if key in attrs:
                ids = attrs[key][0]["certs"]
                h = halg or ids[0]["hash_algorithm"]["algorithm"].native
                if ids and ids[0]["cert_hash"].native != hashlib.new(h, cert_der).digest():
                    raise TimestampError("TSA_SIGNER", "ESS signing-certificate hash does not match signer")
        signed = b"\x31" + si["signed_attrs"].dump()[1:]
        try:
            _verify_sig(signer.public_key(), si["signature"].native, signed, dalg)
        except InvalidSignature:
            raise TimestampError("TSA_SIGNATURE", "TSA signature over signed attributes does not verify")
        chained = False
        if pinned is not None and signer == pinned and any(_issued_by(pinned, r) or pinned == r for r in roots):
            chained = True
        for r in roots:
            if chained:
                break
            if _issued_by(signer, r):
                chained = True
                break
            for inter in embedded:
                if inter != signer and _issued_by(signer, inter) and _issued_by(inter, r):
                    chained = True
                    break
        if not chained:
            errors.append("%s: signer does not chain to a trusted root" % auth.get("name"))
            continue
        try:
            eku = signer.extensions.get_extension_for_class(x509.ExtendedKeyUsage)
        except x509.ExtensionNotFound:
            raise TimestampError("TSA_EKU", "TSA certificate has no extended key usage")
        if not eku.critical or list(eku.value) != [EKU_TIMESTAMPING]:
            raise TimestampError("TSA_EKU", "TSA certificate EKU must be timeStamping only and critical")
        if not (signer.not_valid_before_utc <= gen_time <= signer.not_valid_after_utc):
            raise TimestampError("TSA_TIME", "genTime %s outside the TSA certificate validity" % gen_time)
        vf = auth.get("valid_for") or {}
        start = _dt.datetime.fromisoformat(vf["start"].replace("Z", "+00:00")) if vf.get("start") else None
        end = _dt.datetime.fromisoformat(vf["end"].replace("Z", "+00:00")) if vf.get("end") else None
        if (start and gen_time < start) or (end and gen_time > end):
            raise TimestampError("TSA_TIME", "genTime %s outside the authority's trusted window" % gen_time)
        acc = {k: v for k, v in (tst["accuracy"].native or {}).items() if v is not None} or None
        return {"tsa": auth.get("name"), "gen_time": gen_time.isoformat().replace("+00:00", "Z"),
                "serial": str(tst["serial_number"].native), "policy": tst["policy"].native,
                "hash_algorithm": alg, "accuracy": acc,
                "tsa_certificate_sha256": hashlib.sha256(cert_der).hexdigest()}
    raise TimestampError("TSA_CHAIN", "; ".join(errors) or "no trusted time-stamping authority configured")


def authorities_from_policy(cfg, base_dir=None):
    """Read ``timestamp_authorities`` from a trust policy block."""
    out = []
    for a in (cfg or {}).get("timestamp_authorities") or []:
        def pem(field, path_field):
            if a.get(field):
                return a[field]
            p = a.get(path_field)
            if not p:
                return None
            if not os.path.isabs(p) and base_dir:
                p = os.path.join(base_dir, p)
            with open(p, "r", encoding="ascii") as fh:
                return fh.read()
        roots = [pem("root_pem", "root_pem_path")]
        out.append({"name": a.get("name"), "roots": [r for r in roots if r],
                    "leaf": pem("leaf_pem", "leaf_pem_path"), "valid_for": a.get("valid_for")})
    return out


# ------------------------------------------------------- local test TSA

def _name(cn):
    return x509.Name([x509.NameAttribute(NameOID.ORGANIZATION_NAME, "CRA evidence pilot (test authority)"),
                      x509.NameAttribute(NameOID.COMMON_NAME, cn)])


def generate_tsa(cn="CRA pilot test TSA", days=3650, not_before=None):
    """Generate (root_key, root_cert, tsa_key, tsa_cert) for a test authority."""
    nb = not_before or (_now() - _dt.timedelta(days=1))
    root_key = ec.generate_private_key(ec.SECP256R1())
    root = (x509.CertificateBuilder().subject_name(_name(cn + " root")).issuer_name(_name(cn + " root"))
            .public_key(root_key.public_key()).serial_number(x509.random_serial_number())
            .not_valid_before(nb).not_valid_after(nb + _dt.timedelta(days=days))
            .add_extension(x509.BasicConstraints(ca=True, path_length=0), critical=True)
            .add_extension(x509.KeyUsage(False, False, False, False, False, True, True, False, False), critical=True)
            .add_extension(x509.SubjectKeyIdentifier.from_public_key(root_key.public_key()), critical=False)
            .sign(root_key, hashes.SHA256()))
    tsa_key = ec.generate_private_key(ec.SECP256R1())
    leaf = (x509.CertificateBuilder().subject_name(_name(cn)).issuer_name(root.subject)
            .public_key(tsa_key.public_key()).serial_number(x509.random_serial_number())
            .not_valid_before(nb).not_valid_after(nb + _dt.timedelta(days=days))
            .add_extension(x509.BasicConstraints(ca=False, path_length=None), critical=True)
            .add_extension(x509.KeyUsage(True, False, False, False, False, False, False, False, False), critical=True)
            .add_extension(x509.ExtendedKeyUsage([EKU_TIMESTAMPING]), critical=True)
            .add_extension(x509.SubjectKeyIdentifier.from_public_key(tsa_key.public_key()), critical=False)
            .add_extension(x509.AuthorityKeyIdentifier.from_issuer_public_key(root_key.public_key()), critical=False)
            .sign(root_key, hashes.SHA256()))
    return root_key, root, tsa_key, leaf


def pem_of(obj):
    if isinstance(obj, x509.Certificate):
        return obj.public_bytes(serialization.Encoding.PEM).decode("ascii")
    return obj.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                             serialization.NoEncryption()).decode("ascii")


class LocalTSA:
    """A minimal RFC 3161 authority for tests, the pilot and the benchmark."""

    def __init__(self, tsa_key=None, tsa_cert=None, root_cert=None, name="local-test-tsa", policy=DEFAULT_POLICY,
                 clock=None):
        if tsa_key is None:
            _, root_cert, tsa_key, tsa_cert = generate_tsa()
        self.key, self.cert, self.root = tsa_key, tsa_cert, root_cert
        self.name, self.policy, self.clock = name, policy, clock or _now
        self._serial = int.from_bytes(os.urandom(8), "big")
        self._lock = threading.Lock()
        self._cert_der = tsa_cert.public_bytes(serialization.Encoding.DER)
        self._acert = ax509.Certificate.load(self._cert_der)
        self._server = None
        self.url = None

    @classmethod
    def from_pem_files(cls, key_path, cert_path, root_path, **kw):
        with open(key_path, "rb") as fh:
            key = serialization.load_pem_private_key(fh.read(), password=None)
        with open(cert_path, "rb") as fh:
            cert = x509.load_pem_x509_certificate(fh.read())
        with open(root_path, "rb") as fh:
            root = x509.load_pem_x509_certificate(fh.read())
        return cls(key, cert, root, **kw)

    def authority(self):
        """Trust-policy entry for this authority."""
        return {"name": self.name, "roots": [pem_of(self.root)], "leaf": None, "valid_for": None}

    def issue(self, req_der):
        """TimeStampReq DER -> TimeStampResp DER."""
        try:
            req = tsp.TimeStampReq.load(req_der)
            imprint = req["message_imprint"]
            alg = imprint["hash_algorithm"]["algorithm"].native
            if alg not in HASHES:
                raise ValueError("bad alg")
        except Exception:  # noqa: BLE001
            return tsp.TimeStampResp({"status": {"status": "rejection", "fail_info": {"bad_request"}}}).dump()
        with self._lock:
            self._serial += 1
            serial = self._serial
        gen = self.clock().replace(microsecond=0)
        info = {"version": "v1", "policy": self.policy,
                "message_imprint": {"hash_algorithm": {"algorithm": alg},
                                    "hashed_message": imprint["hashed_message"].native},
                "serial_number": serial, "gen_time": gen, "accuracy": {"seconds": 1}}
        if req["nonce"].native is not None:
            info["nonce"] = req["nonce"].native
        tst = tsp.TSTInfo(info)
        encap = cms.EncapsulatedContentInfo({"content_type": "tst_info",
                                             "content": core.ParsableOctetString(tst.dump())})
        md = hashlib.sha256(tst.dump()).digest()
        attrs = cms.CMSAttributes([
            cms.CMSAttribute({"type": "content_type", "values": ["tst_info"]}),
            cms.CMSAttribute({"type": "signing_time", "values": [cms.Time({"utc_time": gen})]}),
            cms.CMSAttribute({"type": "message_digest", "values": [md]}),
            cms.CMSAttribute({"type": "signing_certificate_v2", "values": [
                {"certs": [{"cert_hash": hashlib.sha256(self._cert_der).digest()}]}]}),
        ])
        sig = self.key.sign(attrs.dump(), ec.ECDSA(hashes.SHA256()))
        si = cms.SignerInfo({
            "version": "v1",
            "sid": cms.SignerIdentifier({"issuer_and_serial_number": cms.IssuerAndSerialNumber(
                {"issuer": self._acert.issuer, "serial_number": self._acert.serial_number})}),
            "digest_algorithm": algos.DigestAlgorithm({"algorithm": "sha256"}),
            "signed_attrs": attrs,
            "signature_algorithm": algos.SignedDigestAlgorithm({"algorithm": "sha256_ecdsa"}),
            "signature": sig,
        })
        sd = cms.SignedData({
            "version": "v3",
            "digest_algorithms": [algos.DigestAlgorithm({"algorithm": "sha256"})],
            "encap_content_info": encap,
            "certificates": [self._acert] if req["cert_req"].native else [],
            "signer_infos": [si],
        })
        token = cms.ContentInfo({"content_type": "signed_data", "content": sd})
        return tsp.TimeStampResp({"status": {"status": "granted"}, "time_stamp_token": token}).dump()

    def timestamp(self, message):
        """In-process client interface (same as TimestampClient.timestamp)."""
        der, nonce = build_request(message)
        resp = self.issue(der)
        check_response(resp, message, nonce)
        return resp

    # HTTP service on 127.0.0.1 (tests, pilot, benchmark)
    def serve(self, port=0):
        tsa = self

        class H(http.server.BaseHTTPRequestHandler):
            def do_POST(self):  # noqa: N802
                n = int(self.headers.get("Content-Length") or 0)
                body = tsa.issue(self.rfile.read(n))
                self.send_response(200)
                self.send_header("Content-Type", "application/timestamp-reply")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                self.wfile.write(body)

            def log_message(self, *a):
                pass

        self._server = http.server.ThreadingHTTPServer(("127.0.0.1", port), H)
        threading.Thread(target=self._server.serve_forever, daemon=True).start()
        self.url = "http://127.0.0.1:%d/" % self._server.server_address[1]
        return self.url

    def stop(self):
        if self._server:
            self._server.shutdown()
            self._server.server_close()
            self._server = None


def b64(b):
    return base64.b64encode(b).decode("ascii")
