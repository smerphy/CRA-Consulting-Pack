"""Pluggable key custody for signing: the pipeline never needs the private key.

Every signer (build provenance, PSIRT VEX, evidence record, log checkpoint)
is a ``KeyProvider``. The provider exposes the public key and a ``sign``
operation over bytes; the bytes signed are always the DSSE
pre-authentication encoding, so any provider produces envelopes the gate
verifies with the public key in the trust policy.

Providers
- ``LocalFileKeyProvider``: PEM private key on disk. Tests, the pilot and
  the benchmark only; never production.
- ``AwsKmsKeyProvider``: AWS KMS asymmetric key (KeySpec ECC_NIST_P256,
  KeyUsage SIGN_VERIFY). Calls ``kms.sign(KeyId, Message=SHA-256(data),
  MessageType="DIGEST", SigningAlgorithm="ECDSA_SHA_256")``, which returns a
  DER ECDSA signature. IAM grants the pipeline role ``kms:Sign`` on that key
  only; ``kms:GetPublicKey`` is used once to check the configured public key.
- ``GcpKmsKeyProvider``: Cloud KMS key version (EC_SIGN_P256_SHA256). Calls
  ``asymmetric_sign`` with a SHA-256 digest and its CRC32C, and checks the
  service's ``verified_digest_crc32c`` and ``name`` in the reply, as Google
  documents for integrity.
- ``Pkcs11KeyProvider``: HSM through PKCS#11 (python-pkcs11 style session).
  Signs the SHA-256 digest with CKM_ECDSA, which returns raw r||s; the
  provider re-encodes it as DER. The public key comes from the key ceremony
  record (PEM) rather than from the token.

Cloud and HSM SDKs are imported lazily and can be injected (``client=``),
which is how the unit tests exercise each adapter with mocks. The adapters
are skeletons: they have not been run against real AWS, Google Cloud or an
HSM in this module.
"""

import hashlib
import json
import os

from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, ed25519, utils

from . import attest as A


class KeyProviderError(RuntimeError):
    pass


class KeyProvider:
    """Interface. Subclasses implement ``public_key`` and ``sign``."""

    name = None          # key name used in the trust policy
    algorithm = None     # "ecdsa-p256-sha256" | "ed25519"
    custody = None       # human-readable custody statement for records

    def public_key(self):
        raise NotImplementedError

    def sign(self, data):
        raise NotImplementedError

    def keyid(self):
        return A.keyid_for(self.public_key())

    def public_pem(self):
        return self.public_key().public_bytes(serialization.Encoding.PEM,
                                              serialization.PublicFormat.SubjectPublicKeyInfo).decode("ascii")

    def trust_entry(self, purposes, owner, not_before="2026-01-01T00:00:00Z", not_after="2030-12-31T23:59:59Z"):
        """Trust-policy key entry for this provider's public key."""
        return {"algorithm": self.algorithm, "keyid": self.keyid(), "public_key_pem": self.public_pem(),
                "owner": owner, "purposes": list(purposes), "status": "active",
                "not_before": not_before, "not_after": not_after, "custody": self.custody}


def _check_ec(pub):
    if not isinstance(pub, ec.EllipticCurvePublicKey) or pub.curve.name != "secp256r1":
        raise KeyProviderError("expected an ECDSA P-256 public key")


class LocalFileKeyProvider(KeyProvider):
    def __init__(self, path, name=None, password=None):
        with open(path, "rb") as fh:
            self._key = serialization.load_pem_private_key(fh.read(), password=password)
        self.name = name or path
        if isinstance(self._key, ec.EllipticCurvePrivateKey):
            self.algorithm = "ecdsa-p256-sha256"
        elif isinstance(self._key, ed25519.Ed25519PrivateKey):
            self.algorithm = "ed25519"
        else:
            raise KeyProviderError("unsupported key type in %s" % path)
        self.custody = "local file (demonstration only): %s" % path

    @classmethod
    def generate(cls, path, name, algorithm="ecdsa-p256-sha256"):
        key = ec.generate_private_key(ec.SECP256R1()) if algorithm.startswith("ecdsa") \
            else ed25519.Ed25519PrivateKey.generate()
        with open(path, "wb") as fh:
            fh.write(key.private_bytes(serialization.Encoding.PEM, serialization.PrivateFormat.PKCS8,
                                       serialization.NoEncryption()))
        return cls(path, name)

    def public_key(self):
        return self._key.public_key()

    def sign(self, data):
        if self.algorithm == "ed25519":
            return self._key.sign(data)
        return self._key.sign(data, ec.ECDSA(hashes.SHA256(), deterministic_signing=True))


class AwsKmsKeyProvider(KeyProvider):
    """AWS KMS asymmetric signing key (ECC_NIST_P256)."""

    def __init__(self, key_id, name=None, region=None, client=None, expected_public_pem=None):
        if client is None:
            import boto3  # lazy: optional dependency
            client = boto3.client("kms", region_name=region)
        self.client, self.key_id = client, key_id
        self.name = name or key_id
        self.algorithm = "ecdsa-p256-sha256"
        self.custody = "AWS KMS key %s (non-exportable; kms:Sign granted to the pipeline role)" % key_id
        self._pub = None
        self._expected = expected_public_pem

    def public_key(self):
        if self._pub is None:
            resp = self.client.get_public_key(KeyId=self.key_id)
            if resp.get("KeySpec") not in (None, "ECC_NIST_P256") or \
                    resp.get("KeyUsage") not in (None, "SIGN_VERIFY"):
                raise KeyProviderError("KMS key %s is %s/%s, expected ECC_NIST_P256/SIGN_VERIFY"
                                       % (self.key_id, resp.get("KeySpec"), resp.get("KeyUsage")))
            pub = serialization.load_der_public_key(resp["PublicKey"])
            _check_ec(pub)
            if self._expected:
                exp = serialization.load_pem_public_key(self._expected.encode("ascii"))
                if A.keyid_for(exp) != A.keyid_for(pub):
                    raise KeyProviderError("KMS public key does not match the key registered in the trust policy")
            self._pub = pub
        return self._pub

    def sign(self, data):
        digest = hashlib.sha256(data).digest()
        resp = self.client.sign(KeyId=self.key_id, Message=digest, MessageType="DIGEST",
                                SigningAlgorithm="ECDSA_SHA_256")
        sig = resp["Signature"]
        self.public_key().verify(sig, data, ec.ECDSA(hashes.SHA256()))   # fail fast on a wrong key
        return sig


def _crc32c(data):
    """CRC32C (Castagnoli), used by Cloud KMS for request/response integrity."""
    try:
        import google_crc32c  # optional, fast
        return int(google_crc32c.value(data))
    except ImportError:
        pass
    crc = 0xFFFFFFFF
    for b in data:
        crc ^= b
        for _ in range(8):
            crc = (crc >> 1) ^ (0x82F63B78 if crc & 1 else 0)
    return crc ^ 0xFFFFFFFF


class GcpKmsKeyProvider(KeyProvider):
    """Google Cloud KMS asymmetric key version (EC_SIGN_P256_SHA256)."""

    def __init__(self, key_version_name, name=None, client=None):
        if client is None:
            from google.cloud import kms  # lazy: optional dependency
            client = kms.KeyManagementServiceClient()
        self.client, self.key_version = client, key_version_name
        self.name = name or key_version_name
        self.algorithm = "ecdsa-p256-sha256"
        self.custody = "Google Cloud KMS key version %s (HSM or software protection level)" % key_version_name
        self._pub = None

    def public_key(self):
        if self._pub is None:
            resp = self.client.get_public_key(request={"name": self.key_version})
            alg = str(getattr(resp, "algorithm", "EC_SIGN_P256_SHA256"))
            if "EC_SIGN_P256_SHA256" not in alg:
                raise KeyProviderError("Cloud KMS key algorithm %s is not EC_SIGN_P256_SHA256" % alg)
            pem = resp.pem
            if hasattr(resp, "pem_crc32c") and resp.pem_crc32c is not None and \
                    int(resp.pem_crc32c) != _crc32c(pem.encode("ascii")):
                raise KeyProviderError("public key CRC32C mismatch (corrupted in transit)")
            pub = serialization.load_pem_public_key(pem.encode("ascii"))
            _check_ec(pub)
            self._pub = pub
        return self._pub

    def sign(self, data):
        digest = hashlib.sha256(data).digest()
        crc = _crc32c(digest)
        resp = self.client.asymmetric_sign(request={"name": self.key_version, "digest": {"sha256": digest},
                                                    "digest_crc32c": crc})
        if not getattr(resp, "verified_digest_crc32c", False):
            raise KeyProviderError("Cloud KMS did not verify the request digest CRC32C")
        if getattr(resp, "name", self.key_version) != self.key_version:
            raise KeyProviderError("Cloud KMS signed with an unexpected key version %s" % resp.name)
        if getattr(resp, "signature_crc32c", None) is not None and \
                int(resp.signature_crc32c) != _crc32c(resp.signature):
            raise KeyProviderError("signature CRC32C mismatch (corrupted in transit)")
        self.public_key().verify(resp.signature, data, ec.ECDSA(hashes.SHA256()))
        return resp.signature


class Pkcs11KeyProvider(KeyProvider):
    """HSM key through PKCS#11. ``session`` is a python-pkcs11-style session.

    The private key object is found by label; signing uses CKM_ECDSA over the
    SHA-256 digest (the HSM never sees the payload), returning raw r||s.
    """

    def __init__(self, session, key_label, public_pem, name=None):
        self.session, self.key_label = session, key_label
        self.name = name or key_label
        self.algorithm = "ecdsa-p256-sha256"
        self.custody = "HSM via PKCS#11, key label %s (non-extractable, CKA_SENSITIVE)" % key_label
        self._pub = serialization.load_pem_public_key(public_pem.encode("ascii"))
        _check_ec(self._pub)
        self._key = None

    @classmethod
    def open(cls, lib_path, token_label, pin, key_label, public_pem, name=None):
        import pkcs11  # lazy: optional dependency (python-pkcs11)
        token = pkcs11.lib(lib_path).get_token(token_label=token_label)
        return cls(token.open(user_pin=pin), key_label, public_pem, name)

    def public_key(self):
        return self._pub

    def _private(self):
        if self._key is None:
            try:
                from pkcs11 import KeyType, ObjectClass
                self._key = self.session.get_key(object_class=ObjectClass.PRIVATE_KEY, key_type=KeyType.EC,
                                                 label=self.key_label)
            except ImportError:
                self._key = self.session.get_key(label=self.key_label)
        return self._key

    def sign(self, data):
        digest = hashlib.sha256(data).digest()
        try:
            from pkcs11 import Mechanism
            mech = Mechanism.ECDSA
        except ImportError:
            mech = "CKM_ECDSA"
        raw = self._private().sign(digest, mechanism=mech)
        if len(raw) != 64:
            raise KeyProviderError("CKM_ECDSA returned %d bytes, expected 64 (r||s for P-256)" % len(raw))
        r, s = int.from_bytes(raw[:32], "big"), int.from_bytes(raw[32:], "big")
        sig = utils.encode_dss_signature(r, s)
        self._pub.verify(sig, data, ec.ECDSA(hashes.SHA256()))
        return sig


def provider_from_config(cfg, base_dir=None):
    """Build a provider from a config dict: {type: file|aws-kms|gcp-kms|pkcs11, ...}."""
    t = cfg.get("type", "file")
    if t == "file":
        p = cfg["path"]
        if base_dir and not os.path.isabs(p):
            p = os.path.join(base_dir, p)
        return LocalFileKeyProvider(p, cfg.get("name"))
    if t == "aws-kms":
        return AwsKmsKeyProvider(cfg["key_id"], cfg.get("name"), cfg.get("region"),
                                 expected_public_pem=cfg.get("public_key_pem"))
    if t == "gcp-kms":
        return GcpKmsKeyProvider(cfg["key_version"], cfg.get("name"))
    if t == "pkcs11":
        return Pkcs11KeyProvider.open(cfg["lib"], cfg["token_label"], os.environ[cfg.get("pin_env", "PKCS11_PIN")],
                                      cfg["key_label"], cfg["public_key_pem"], cfg.get("name"))
    raise KeyProviderError("unknown key provider type %r" % t)


# ------------------------------------------------------------ signing

def sign_statement(statement, provider):
    """DSSE envelope over an in-toto Statement, signed by ``provider``."""
    payload = json.dumps(statement, separators=(",", ":"), sort_keys=True).encode("utf-8")
    sig = provider.sign(A.pae(A.INTOTO, payload))
    return {"payloadType": A.INTOTO, "payload": A.b64e(payload),
            "signatures": [{"keyid": provider.keyid(), "sig": A.b64e(sig)}]}


BUNDLE_V03 = "application/vnd.dev.sigstore.bundle.v0.3+json"


def to_bundle(envelope, keyid_hint, timestamps=(), tlog_entries=()):
    """Wrap a key-signed DSSE envelope as a Sigstore bundle v0.3 with RFC 3161 timestamps."""
    vm = {"publicKey": {"hint": keyid_hint}, "tlogEntries": list(tlog_entries)}
    if timestamps:
        vm["timestampVerificationData"] = {"rfc3161Timestamps": [{"signedTimestamp": A.b64e(t)} for t in timestamps]}
    return {"mediaType": BUNDLE_V03, "verificationMaterial": vm, "dsseEnvelope": envelope}


def sign_and_timestamp(statement, provider, tsa=None):
    """Sign a statement and, with a TSA client, timestamp the signature bytes."""
    env = sign_statement(statement, provider)
    ts = []
    if tsa is not None:
        ts.append(tsa.timestamp(A.b64d(env["signatures"][0]["sig"])))
    return to_bundle(env, provider.keyid(), ts)
