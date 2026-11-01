"""Record signing, key providers, RFC 3161 timestamps, Merkle log and object-lock storage."""

import base64
import copy
import datetime as dt
import hashlib
import json
import os
import shutil
import socket
import stat
import tempfile
import unittest
from types import SimpleNamespace

from cryptography import x509
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import ec, utils

from helpers import LOCK_OK, ROOT, bundle, decide

from cra_evidence import attest as A
from cra_evidence import evidence_store as ES
from cra_evidence import keys as K
from cra_evidence import merkle as M
from cra_evidence import objectstore as O
from cra_evidence import record_signing as RS
from cra_evidence import tsa as T

UTC = dt.timezone.utc

try:
    import boto3  # noqa: F401
    from moto.server import ThreadedMotoServer
    HAVE_MOTO = True
except ImportError:
    HAVE_MOTO = False

try:
    import rfc3161_client  # noqa: F401
    HAVE_RFC3161_CLIENT = True
except ImportError:
    HAVE_RFC3161_CLIENT = False

_TMP = tempfile.mkdtemp(prefix="cra-trust-")
_TSA = T.LocalTSA()
_REC = K.LocalFileKeyProvider.generate(os.path.join(_TMP, "rec.pem"), "test-record")
_LOG = K.LocalFileKeyProvider.generate(os.path.join(_TMP, "log.pem"), "test-log", "ed25519")
_BUILD = K.LocalFileKeyProvider.generate(os.path.join(_TMP, "build.pem"), "test-build")


def trust_cfg(require_ts=True, tsa=_TSA, build_not_after="2030-12-31T23:59:59Z"):
    return {"trust_policy_id": "test-trust/1",
            "keys": {"test-record": _REC.trust_entry(["evidence_record"], "release pipeline"),
                     "test-log": _LOG.trust_entry(["log_checkpoint"], "evidence store"),
                     "test-build": _BUILD.trust_entry(["provenance"], "builder", not_before="2020-01-01T00:00:00Z",
                                                      not_after=build_not_after)},
            "timestamp_authorities": [{"name": "local-test-tsa", "root_pem": T.pem_of(tsa.root)}],
            "products": {"*": {"evidence_record": {"keys": ["test-record"], "require_timestamp": require_ts},
                               "log_checkpoint": {"keys": ["test-log"], "require_timestamp": require_ts},
                               "provenance": {"keys": ["test-build"], "require_timestamp": require_ts}}}}


def trust(**kw):
    return A.TrustPolicy(trust_cfg(**kw))


def gated_record():
    b = bundle(LOCK_OK)
    b.record["gate"] = decide(b)
    return b.record


def statement(digest="ab" * 32):
    return {"_type": "https://in-toto.io/Statement/v1", "subject": [{"name": "x.bin", "digest": {"sha256": digest}}],
            "predicateType": "https://slsa.dev/provenance/v1", "predicate": {}}


# --------------------------------------------------------------- RFC 3161

class Timestamps(unittest.TestCase):
    def test_issue_and_verify(self):
        resp = _TSA.timestamp(b"signature-bytes")
        info = T.verify_response(resp, b"signature-bytes", [_TSA.authority()])
        self.assertEqual(info["tsa"], "local-test-tsa")
        self.assertEqual(info["hash_algorithm"], "sha256")
        gt = dt.datetime.fromisoformat(info["gen_time"].replace("Z", "+00:00"))
        self.assertLess(abs((dt.datetime.now(UTC) - gt).total_seconds()), 120)

    def test_wrong_message_rejected(self):
        resp = _TSA.timestamp(b"a")
        with self.assertRaises(T.TimestampError) as cm:
            T.verify_response(resp, b"b", [_TSA.authority()])
        self.assertEqual(cm.exception.code, "TSA_IMPRINT")

    def test_untrusted_root_rejected(self):
        other = T.LocalTSA()
        resp = other.timestamp(b"a")
        with self.assertRaises(T.TimestampError) as cm:
            T.verify_response(resp, b"a", [_TSA.authority()])
        self.assertEqual(cm.exception.code, "TSA_CHAIN")

    def test_tampered_signature_rejected(self):
        resp = bytearray(_TSA.timestamp(b"a"))
        from asn1crypto import tsp
        r = tsp.TimeStampResp.load(bytes(resp))
        sig = r["time_stamp_token"]["content"]["signer_infos"][0]["signature"].native
        i = bytes(resp).find(sig)
        resp[i + 10] ^= 0x01
        with self.assertRaises(T.TimestampError) as cm:
            T.verify_response(bytes(resp), b"a", [_TSA.authority()])
        self.assertIn(cm.exception.code, ("TSA_SIGNATURE", "TSA_PARSE"))

    def test_tampered_gen_time_rejected(self):
        resp = _TSA.timestamp(b"a")
        from asn1crypto import tsp
        r = tsp.TimeStampResp.load(resp)
        tst = r["time_stamp_token"]["content"]["encap_content_info"]["content"].parsed
        old = tst["gen_time"].dump()
        new_tst = tsp.TSTInfo.load(tst.dump().replace(old, tsp.TSTInfo({"version": "v1", "policy": "1.2.3",
            "message_imprint": {"hash_algorithm": {"algorithm": "sha256"}, "hashed_message": b"0" * 32},
            "serial_number": 1, "gen_time": dt.datetime(2020, 1, 1, tzinfo=UTC)})["gen_time"].dump()))
        bad = resp.replace(tst.dump(), new_tst.dump())
        self.assertNotEqual(bad, resp)
        with self.assertRaises(T.TimestampError) as cm:
            T.verify_response(bad, b"a", [_TSA.authority()])
        self.assertEqual(cm.exception.code, "TSA_DIGEST")

    def test_nonce_and_window(self):
        der, nonce = T.build_request(b"m", nonce=42)
        resp = _TSA.issue(der)
        self.assertTrue(T.verify_response(resp, b"m", [_TSA.authority()], nonce=42))
        with self.assertRaises(T.TimestampError) as cm:
            T.verify_response(resp, b"m", [_TSA.authority()], nonce=43)
        self.assertEqual(cm.exception.code, "TSA_NONCE")
        auth = dict(_TSA.authority(), valid_for={"start": "2001-01-01T00:00:00Z", "end": "2002-01-01T00:00:00Z"})
        with self.assertRaises(T.TimestampError) as cm:
            T.verify_response(resp, b"m", [auth])
        self.assertEqual(cm.exception.code, "TSA_TIME")

    def test_certificate_without_timestamping_eku_rejected(self):
        root_key, root, _, _ = T.generate_tsa()
        key = ec.generate_private_key(ec.SECP256R1())
        now = dt.datetime.now(UTC) - dt.timedelta(days=1)
        leaf = (x509.CertificateBuilder().subject_name(T._name("no-eku")).issuer_name(root.subject)
                .public_key(key.public_key()).serial_number(x509.random_serial_number())
                .not_valid_before(now).not_valid_after(now + dt.timedelta(days=30)).sign(root_key, hashes.SHA256()))
        bad = T.LocalTSA(key, leaf, root)
        with self.assertRaises(T.TimestampError) as cm:
            T.verify_response(bad.timestamp(b"a"), b"a", [bad.authority()])
        self.assertEqual(cm.exception.code, "TSA_EKU")

    def test_http_client_against_local_tsa(self):
        url = _TSA.serve()
        try:
            resp = T.TimestampClient(url).timestamp(b"over-http")
            self.assertEqual(T.verify_response(resp, b"over-http", [_TSA.authority()])["tsa"], "local-test-tsa")
        finally:
            _TSA.stop()

    @unittest.skipUnless(shutil.which("openssl"), "openssl not installed")
    def test_openssl_verifies_our_tokens(self):
        import subprocess
        d = tempfile.mkdtemp(prefix="cra-ossl-", dir=_TMP)
        for name, data in (("msg", b"sig-bytes"), ("resp.tsr", _TSA.timestamp(b"sig-bytes")),
                           ("root.pem", T.pem_of(_TSA.root).encode()), ("other", b"x")):
            with open(os.path.join(d, name), "wb") as fh:
                fh.write(data)
        ok = subprocess.run(["openssl", "ts", "-verify", "-data", os.path.join(d, "msg"), "-in",
                             os.path.join(d, "resp.tsr"), "-CAfile", os.path.join(d, "root.pem")],
                            capture_output=True, text=True)
        self.assertEqual(ok.returncode, 0, ok.stderr)
        bad = subprocess.run(["openssl", "ts", "-verify", "-data", os.path.join(d, "other"), "-in",
                              os.path.join(d, "resp.tsr"), "-CAfile", os.path.join(d, "root.pem")],
                             capture_output=True, text=True)
        self.assertNotEqual(bad.returncode, 0)

    @unittest.skipUnless(HAVE_RFC3161_CLIENT, "rfc3161-client not installed")
    def test_independent_library_accepts_our_tokens(self):
        from rfc3161_client import VerifierBuilder, decode_timestamp_response
        resp = _TSA.timestamp(b"cross-check")
        v = VerifierBuilder().add_root_certificate(_TSA.root).build()
        self.assertTrue(v.verify_message(decode_timestamp_response(resp), b"cross-check"))


# ------------------------------------------------- timestamps in the gate path

class TimestampedSignatures(unittest.TestCase):
    def _bundle(self, tsa=_TSA, provider=_BUILD):
        return K.sign_and_timestamp(statement(), provider, tsa)

    def test_signing_time_comes_from_timestamp(self):
        att = A.load_attestations(self._bundle())[0]
        res = A.verify(att, trust(), "p", "provenance")
        self.assertTrue(res["verified"], res["problems"])
        self.assertTrue(res["signer"]["signing_time_source"].startswith("RFC 3161 timestamp"))
        self.assertEqual(len(res["signer"]["timestamps"]), 1)

    def test_timestamp_proves_key_was_valid_when_signed(self):
        # The key expired on 1 Jun 2026; the TSA says the signature existed on 1 Mar 2026.
        _, root, key, cert = T.generate_tsa(not_before=dt.datetime(2025, 1, 1, tzinfo=UTC))
        past = T.LocalTSA(key, cert, root, clock=lambda: dt.datetime(2026, 3, 1, tzinfo=UTC))
        tp = trust(tsa=past, build_not_after="2026-06-01T00:00:00Z")
        att = A.load_attestations(self._bundle(tsa=past))[0]
        res = A.verify(att, tp, "p", "provenance")
        self.assertTrue(res["verified"], res["problems"])
        self.assertTrue(res["signer"]["signing_time"].startswith("2026-03-01"))
        # Without a timestamp, the gate clock (after expiry) is the signing time and the key is expired.
        bare = A.load_attestations(K.sign_statement(statement(), _BUILD))[0]
        res = A.verify(bare, A.TrustPolicy(trust_cfg(require_ts=False, build_not_after="2026-06-01T00:00:00Z")),
                       "p", "provenance")
        self.assertEqual(res["problems"][0][0], "KEY_EXPIRED")

    def test_missing_timestamp_fails_when_required(self):
        bare = K.to_bundle(K.sign_statement(statement(), _BUILD), _BUILD.keyid())
        res = A.verify(A.load_attestations(bare)[0], trust(), "p", "provenance")
        self.assertFalse(res["verified"])
        self.assertEqual(res["problems"][0][0], "TIMESTAMP_MISSING")

    def test_timestamp_over_other_bytes_fails(self):
        b = self._bundle()
        other = _TSA.timestamp(b"not the signature")
        b["verificationMaterial"]["timestampVerificationData"]["rfc3161Timestamps"][0]["signedTimestamp"] = \
            base64.b64encode(other).decode()
        res = A.verify(A.load_attestations(b)[0], trust(), "p", "provenance")
        self.assertEqual(res["problems"][0][0], "TIMESTAMP_INVALID")

    def test_timestamp_from_untrusted_tsa_fails(self):
        b = self._bundle(tsa=T.LocalTSA())
        res = A.verify(A.load_attestations(b)[0], trust(), "p", "provenance")
        self.assertEqual(res["problems"][0][0], "TIMESTAMP_INVALID")


# ---------------------------------------------------------- key providers

class FakeAwsKms:
    """Mock of the boto3 KMS client surface the adapter uses."""

    def __init__(self, key, spec="ECC_NIST_P256"):
        self.key, self.spec, self.calls = key, spec, []

    def get_public_key(self, KeyId):  # noqa: N803
        return {"KeyId": KeyId, "KeySpec": self.spec, "KeyUsage": "SIGN_VERIFY",
                "PublicKey": self.key.public_key().public_bytes(serialization.Encoding.DER,
                                                                serialization.PublicFormat.SubjectPublicKeyInfo)}

    def sign(self, **kw):
        self.calls.append(kw)
        assert kw["MessageType"] == "DIGEST" and kw["SigningAlgorithm"] == "ECDSA_SHA_256" and len(kw["Message"]) == 32
        return {"Signature": self.key.sign(kw["Message"], ec.ECDSA(utils.Prehashed(hashes.SHA256())))}


class FakeGcpKms:
    def __init__(self, key, name, tamper=None):
        self.key, self.name, self.tamper = key, name, tamper

    def get_public_key(self, request):
        pem = self.key.public_key().public_bytes(serialization.Encoding.PEM,
                                                 serialization.PublicFormat.SubjectPublicKeyInfo).decode()
        return SimpleNamespace(pem=pem, pem_crc32c=K._crc32c(pem.encode()), algorithm="EC_SIGN_P256_SHA256")

    def asymmetric_sign(self, request):
        d = request["digest"]["sha256"]
        ok = request["digest_crc32c"] == K._crc32c(d)
        sig = self.key.sign(d, ec.ECDSA(utils.Prehashed(hashes.SHA256())))
        name = self.name if self.tamper != "name" else self.name + "-other"
        return SimpleNamespace(signature=sig, signature_crc32c=K._crc32c(sig), verified_digest_crc32c=ok, name=name)


class FakePkcs11Key:
    def __init__(self, key, raw_len=64):
        self.key, self.raw_len = key, raw_len

    def sign(self, digest, mechanism=None):
        r, s = utils.decode_dss_signature(self.key.sign(digest, ec.ECDSA(utils.Prehashed(hashes.SHA256()))))
        raw = r.to_bytes(32, "big") + s.to_bytes(32, "big")
        return raw[:self.raw_len]


class FakePkcs11Session:
    def __init__(self, key):
        self.key = key

    def get_key(self, **kw):
        return self.key


def _dsse_ok(provider):
    env = K.sign_statement(statement(), provider)
    tp = A.TrustPolicy({"keys": {"k": provider.trust_entry(["provenance"], "o")},
                        "products": {"*": {"provenance": {"keys": ["k"]}}}})
    return A.verify(A.load_attestations(env)[0], tp, "p", "provenance")["verified"]


class KeyProviders(unittest.TestCase):
    def test_local_file_ecdsa_and_ed25519(self):
        self.assertTrue(_dsse_ok(_REC))
        self.assertTrue(_dsse_ok(_LOG))
        self.assertEqual(_LOG.algorithm, "ed25519")

    def test_aws_kms_adapter(self):
        key = ec.generate_private_key(ec.SECP256R1())
        fake = FakeAwsKms(key)
        p = K.AwsKmsKeyProvider("arn:aws:kms:eu-west-1:111122223333:key/demo", "aws-key", client=fake)
        self.assertTrue(_dsse_ok(p))
        self.assertEqual(fake.calls[0]["KeyId"], "arn:aws:kms:eu-west-1:111122223333:key/demo")
        with self.assertRaises(K.KeyProviderError):
            K.AwsKmsKeyProvider("k", client=FakeAwsKms(key, spec="RSA_2048")).public_key()
        other = ec.generate_private_key(ec.SECP256R1()).public_key().public_bytes(
            serialization.Encoding.PEM, serialization.PublicFormat.SubjectPublicKeyInfo).decode()
        with self.assertRaises(K.KeyProviderError):
            K.AwsKmsKeyProvider("k", client=FakeAwsKms(key), expected_public_pem=other).public_key()

    def test_gcp_kms_adapter(self):
        key = ec.generate_private_key(ec.SECP256R1())
        name = "projects/p/locations/europe-west1/keyRings/cra/cryptoKeys/record/cryptoKeyVersions/1"
        self.assertTrue(_dsse_ok(K.GcpKmsKeyProvider(name, client=FakeGcpKms(key, name))))
        with self.assertRaises(K.KeyProviderError):
            K.GcpKmsKeyProvider(name, client=FakeGcpKms(key, name, tamper="name")).sign(b"x")
        self.assertEqual(K._crc32c(b"123456789"), 0xE3069283)   # CRC32C check value

    def test_pkcs11_adapter(self):
        key = ec.generate_private_key(ec.SECP256R1())
        pem = key.public_key().public_bytes(serialization.Encoding.PEM,
                                            serialization.PublicFormat.SubjectPublicKeyInfo).decode()
        p = K.Pkcs11KeyProvider(FakePkcs11Session(FakePkcs11Key(key)), "cra-record-2027", pem)
        self.assertTrue(_dsse_ok(p))
        bad = K.Pkcs11KeyProvider(FakePkcs11Session(FakePkcs11Key(key, raw_len=63)), "x", pem)
        with self.assertRaises(K.KeyProviderError):
            bad.sign(b"x")

    def test_provider_from_config(self):
        p = K.provider_from_config({"type": "file", "path": "rec.pem", "name": "n"}, base_dir=_TMP)
        self.assertEqual(p.keyid(), _REC.keyid())
        with self.assertRaises(K.KeyProviderError):
            K.provider_from_config({"type": "nope"})


# ---------------------------------------------------------- record signing

class RecordSigning(unittest.TestCase):
    def test_sign_and_verify(self):
        rec = gated_record()
        b = RS.sign_record(rec, _REC, _TSA)
        self.assertEqual(b["mediaType"], K.BUNDLE_V03)
        got, res = RS.verify_record_bundle(b, trust(), "hearth-lock-3", RS.record_digest(rec))
        self.assertTrue(res["verified"], res["problems"])
        self.assertEqual(got, rec)
        st = A.load_attestations(b)[0].unverified_statement()
        self.assertEqual(st["predicateType"], RS.PREDICATE_TYPE)
        self.assertEqual(st["subject"][0]["digest"]["sha256"], rec["version"]["artefact"]["digests"]["sha256"])

    def test_tampered_record_fails(self):
        rec = gated_record()
        b = RS.sign_record(rec, _REC, _TSA)
        st = json.loads(base64.b64decode(b["dsseEnvelope"]["payload"]))
        st["predicate"]["gate"]["decision"] = "PASS" if st["predicate"]["gate"]["decision"] != "PASS" else "FAIL"
        b["dsseEnvelope"]["payload"] = base64.b64encode(RS.canonical(st)).decode()
        got, res = RS.verify_record_bundle(b, trust(), "hearth-lock-3")
        self.assertIsNone(got)
        self.assertTrue(res["problems"][0].startswith("SIGNATURE_INVALID"))

    def test_logged_digest_must_match(self):
        rec = gated_record()
        got, res = RS.verify_record_bundle(RS.sign_record(rec, _REC, _TSA), trust(), "hearth-lock-3", "00" * 32)
        self.assertIsNone(got)
        self.assertTrue(res["problems"][-1].startswith("RECORD_DIGEST_MISMATCH"))

    def test_wrong_key_purpose_fails(self):
        rec = gated_record()
        got, res = RS.verify_record_bundle(RS.sign_record(rec, _BUILD, _TSA), trust(), "hearth-lock-3")
        self.assertIsNone(got)
        self.assertTrue(res["problems"][0].startswith("SIGNER_NOT_AUTHORISED"))


# --------------------------------------------------------------- Merkle

class Merkle(unittest.TestCase):
    def test_compact_tree_matches_reference_root(self):
        t = M.CompactTree()
        leaves = []
        for i in range(70):
            lh = M.leaf_hash(b"%d" % i)
            leaves.append(lh)
            t.append(lh)
            self.assertEqual(t.root(), M.mth(leaves))

    def test_inclusion_proofs(self):
        leaves = [M.leaf_hash(b"%d" % i) for i in range(23)]
        for n in (1, 2, 3, 7, 8, 13, 23):
            root = M.mth(leaves[:n])
            for i in range(n):
                self.assertTrue(M.verify_inclusion(i, n, leaves[i], M.inclusion_proof(i, leaves[:n]), root))
        p = M.inclusion_proof(4, leaves)
        self.assertFalse(M.verify_inclusion(4, 23, leaves[5], p, M.mth(leaves)))

    def test_consistency_proofs(self):
        leaves = [M.leaf_hash(b"%d" % i) for i in range(20)]
        for n in range(1, 21):
            for m in range(1, n + 1):
                proof = M.consistency_proof(m, leaves[:n])
                self.assertTrue(M.verify_consistency(m, n, M.mth(leaves[:m]), M.mth(leaves[:n]), proof), (m, n))
        rewritten = leaves[:5] + [M.leaf_hash(b"evil")] + leaves[6:]
        proof = M.consistency_proof(8, rewritten)
        self.assertFalse(M.verify_consistency(8, 20, M.mth(leaves[:8]), M.mth(rewritten), proof))


# ------------------------------------------------------------ stores

class LocalStore(unittest.TestCase):
    def setUp(self):
        self.dir = tempfile.mkdtemp(prefix="cra-store-")
        self.be = O.LocalBackend(self.dir)
        self.st = ES.EvidenceStore(self.be, _REC, _LOG, _TSA)
        self.rec = gated_record()
        for k in range(3):
            self.st.put_release(dict(self.rec, generated_at="2028-01-1%dT00:00:00Z" % k), [("e.json", b"{}")])

    def tearDown(self):
        for dp, _, fns in os.walk(self.dir):
            for f in fns:
                os.chmod(os.path.join(dp, f), stat.S_IRUSR | stat.S_IWUSR)
        shutil.rmtree(self.dir, ignore_errors=True)

    def _force_write(self, key, data):
        p = os.path.join(self.dir, key)
        os.chmod(p, stat.S_IRUSR | stat.S_IWUSR)
        with open(p, "wb") as fh:
            fh.write(data)

    def test_clean_store_verifies_and_reads(self):
        self.assertEqual(self.st.verify(trust(), deep=True), [])
        got, res = self.st.get_record(self.rec["record_id"], trust())
        self.assertTrue(res["verified"])
        self.assertEqual(got["generated_at"], "2028-01-12T00:00:00Z")
        reopened = ES.EvidenceStore(self.be, _REC, _LOG, _TSA)
        self.assertEqual(reopened.tree.root(), self.st.tree.root())

    def test_write_once_and_retention(self):
        with self.assertRaises(O.WriteOnceError):
            self.be.put("log/entries/000000000000.json", b"x", "2040-01-01")
        with self.assertRaises(O.ObjectLockedError):
            self.be.delete("log/entries/000000000000.json")
        with self.assertRaises(O.ObjectLockedError):
            self.be.extend_retention("log/entries/000000000000.json", "2001-01-01")

    def test_edited_record_detected_on_read_and_verify(self):
        e = self.st.entries[2]
        rec = json.loads(self.be.get(e["record_key"]))
        rec["gate"]["decision"] = "PASS"
        rec["gate"]["reasons"] = []
        self._force_write(e["record_key"], RS.canonical(rec))
        probs = self.st.verify(trust())
        self.assertTrue(any("record bytes altered" in p for p in probs), probs)

    def test_rewritten_entry_detected_by_checkpoint(self):
        e = dict(self.st.entries[1], decision="FAIL-ALTERED")
        self._force_write("log/entries/000000000001.json", ES._canon(e))
        probs = self.st.verify(trust())
        self.assertTrue(any("log rewritten" in p for p in probs), probs)

    def test_truncation_detected(self):
        p = os.path.join(self.dir, "log", "entries", "000000000002.json")
        os.chmod(p, stat.S_IRUSR | stat.S_IWUSR)
        os.remove(p)
        probs = self.st.verify(trust())
        self.assertTrue(any("entries deleted" in p for p in probs), probs)

    def test_inclusion_proof_is_storage_independent(self):
        cp = self.st.checkpoint()["bundle"]
        proof = self.st.inclusion_proof(1)
        ok, info = ES.verify_inclusion(self.st.entries[1], proof, cp, trust())
        self.assertTrue(ok, info)
        self.assertEqual(info["tree_size"], 3)
        forged = dict(self.st.entries[1], decision="FAIL-ALTERED")
        self.assertFalse(ES.verify_inclusion(forged, proof, cp, trust())[0])
        self.assertTrue(info["signer"]["signing_time_source"].startswith("RFC 3161"))


def _free_port():
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    p = s.getsockname()[1]
    s.close()
    return p


@unittest.skipUnless(HAVE_MOTO, "moto[server] and boto3 not installed")
class S3ObjectLock(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.port = _free_port()
        cls.server = ThreadedMotoServer(ip_address="127.0.0.1", port=cls.port, verbose=False)
        cls.server.start()
        import boto3
        cls.client = boto3.client("s3", endpoint_url="http://127.0.0.1:%d" % cls.port, region_name="eu-west-1",
                                  aws_access_key_id="testing", aws_secret_access_key="testing")
        cls.be = O.S3ObjectLockBackend("cra-evidence-test", client=cls.client)
        cls.be.ensure_bucket(create=True, region="eu-west-1")

    @classmethod
    def tearDownClass(cls):
        cls.server.stop()

    def test_put_with_compliance_retention(self):
        r = self.be.put("t/a.json", b"evidence", "2038-01-06")
        self.assertTrue(r["version_id"])
        ret = self.be.retention("t/a.json")
        self.assertEqual(ret["mode"], "COMPLIANCE")
        self.assertEqual(ret["retain_until"], "2038-01-06")
        self.assertEqual(ret["sha256_b64"], O.sha256_b64(b"evidence"))

    def test_delete_and_overwrite_denied(self):
        r = self.be.put("t/b.json", b"original", "2038-01-06")
        with self.assertRaises(O.ObjectLockedError):
            self.be.delete("t/b.json", version_id=r["version_id"])
        from botocore.exceptions import ClientError
        with self.assertRaises(ClientError) as cm:
            self.client.delete_object(Bucket="cra-evidence-test", Key="t/b.json", VersionId=r["version_id"],
                                      BypassGovernanceRetention=True)
        self.assertEqual(cm.exception.response["Error"]["Code"], "AccessDenied")
        with self.assertRaises(O.WriteOnceError):
            self.be.put("t/b.json", b"forged", "2038-01-06")
        # A delete without a version id only adds a delete marker; the locked version survives.
        self.be.delete("t/b.json")
        body = self.client.get_object(Bucket="cra-evidence-test", Key="t/b.json", VersionId=r["version_id"])
        self.assertEqual(body["Body"].read(), b"original")

    def test_retention_only_extends(self):
        self.be.put("t/c.json", b"c", "2036-01-01")
        self.be.extend_retention("t/c.json", "2040-01-01")
        self.assertEqual(self.be.retention("t/c.json")["retain_until"], "2040-01-01")
        with self.assertRaises(O.ObjectLockedError):
            self.be.extend_retention("t/c.json", "2030-01-01")

    def test_dedup_extends_shared_blob(self):
        self.be.put_dedup("blobs/sha256/x", b"same", "2035-01-01")
        r = self.be.put_dedup("blobs/sha256/x", b"same", "2039-01-01")
        self.assertTrue(r["deduplicated"])
        self.assertEqual(self.be.retention("blobs/sha256/x")["retain_until"], "2039-01-01")
        with self.assertRaises(O.StorageError):
            self.be.put_dedup("blobs/sha256/x", b"different", "2039-01-01")

    def test_bucket_without_object_lock_refused(self):
        self.client.create_bucket(Bucket="cra-no-lock", CreateBucketConfiguration={"LocationConstraint": "eu-west-1"})
        with self.assertRaises(Exception):
            O.S3ObjectLockBackend("cra-no-lock", client=self.client).ensure_bucket()

    def test_evidence_store_on_s3(self):
        be = O.S3ObjectLockBackend("cra-evidence-test", client=self.client, prefix="store1/")
        st = ES.EvidenceStore(be, _REC, _LOG, _TSA)
        rec = gated_record()
        r = st.put_release(rec, [("evidence/sbom.json", b"{}")])
        self.assertEqual(be.retention(r["record_key"])["mode"], "COMPLIANCE")
        self.assertEqual(be.retention(r["record_key"])["retain_until"], rec["retention"]["retain_until"])
        self.assertEqual(st.verify(trust(), deep=True), [])
        with self.assertRaises(O.ObjectLockedError):
            be.delete(r["record_key"], version_id=r["versions"][0])



# ------------------------------------------------- OSV matching on real data shapes

class OsvRealShapes(unittest.TestCase):
    """Bugs the pilot found on real OSV data: GIT ranges and GHSA/PYSEC aliases."""

    PYSEC = {"id": "PYSEC-2020-148", "aliases": ["CVE-2020-26137", "GHSA-wqvq-5m8c-6g24"],
             "affected": [{"package": {"name": "urllib3", "ecosystem": "PyPI"}, "ranges": [
                 {"type": "GIT", "events": [{"introduced": "0"}, {"fixed": "1dd69c5c5982fae7c87a620d487c2ebf7a6b436b"}]},
                 {"type": "ECOSYSTEM", "events": [{"introduced": "0"}, {"fixed": "1.25.9"}]}]}]}
    GHSA = {"id": "GHSA-wqvq-5m8c-6g24", "aliases": ["CVE-2020-26137", "PYSEC-2020-148"],
            "affected": [{"package": {"name": "urllib3", "ecosystem": "PyPI"}, "ranges": [
                {"type": "ECOSYSTEM", "events": [{"introduced": "0"}, {"fixed": "1.25.9"}]}]}],
            "database_specific": {"severity": "MODERATE"}}

    def test_git_ranges_are_not_versions(self):
        from cra_evidence import collectors as C
        self.assertEqual(C.match_osv([{"name": "urllib3", "version": "2.7.0"}], [dict(self.PYSEC)], set()), [])

    def test_aliases_match_once(self):
        from cra_evidence import collectors as C
        m = C.match_osv([{"name": "urllib3", "version": "1.25.8"}], [dict(self.PYSEC), dict(self.GHSA)], set())
        self.assertEqual([x["vulnerability"] for x in m], ["CVE-2020-26137"])
        no_cve = [{"id": "PYSEC-2026-1", "aliases": ["GHSA-aaaa-bbbb-cccc"], "affected": self.GHSA["affected"]},
                  {"id": "GHSA-aaaa-bbbb-cccc", "aliases": ["PYSEC-2026-1"], "affected": self.GHSA["affected"]}]
        m = C.match_osv([{"name": "urllib3", "version": "1.0"}], no_cve, set())
        self.assertEqual(len(m), 1)


# ------------------------------------------------------------- pilot outputs

PILOT = os.path.join(ROOT, "examples", "pilot")
PILOT_POLICY = os.path.join(PILOT, "policy", "pilot-gate-policy.json")


@unittest.skipUnless(os.path.isdir(os.path.join(PILOT, "out", "store")), "pilot has not been run")
class PilotOutputs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        pol = json.load(open(PILOT_POLICY))
        cls.trust = A.TrustPolicy(pol["attestation_trust"], os.path.dirname(PILOT_POLICY))
        cls.results = json.load(open(os.path.join(PILOT, "results", "pilot-results.json")))

    def test_offline_store_verifies(self):
        st = ES.EvidenceStore(O.LocalBackend(os.path.join(PILOT, "out", "store")))
        self.assertEqual(st.tree.size, len(self.results["versions"]))
        self.assertEqual(st.verify(self.trust, deep=True), [])
        self.assertEqual(st.tree.root().hex(), self.results["store"]["root_hash"])

    def test_every_record_is_signed_timestamped_and_schema_valid(self):
        from cra_evidence import schema as S
        st = ES.EvidenceStore(O.LocalBackend(os.path.join(PILOT, "out", "store")))
        for e in st.entries:
            rec, res = st.get_record(e["record_id"], self.trust)
            self.assertTrue(res["verified"], res["problems"])
            self.assertTrue(res["signer"]["signing_time_source"].startswith("RFC 3161"))
            self.assertEqual(S.validate(rec), [])
            prov = rec["evidence"]["provenance"]["verification"]
            self.assertTrue(prov["verified"])
            self.assertEqual(prov["slsa_build_level"], 1)

    def test_results_record_reproducible_builds_and_locked_store(self):
        self.assertTrue(all(v["reproducibility"]["bit_identical"] for v in self.results["versions"]))
        self.assertTrue(self.results["store"]["all_compliance_mode"])
        neg = self.results["store"]["negative_checks"]
        self.assertTrue(neg["delete_locked_version"].startswith("DENIED"))
        self.assertTrue(neg["overwrite_record"].startswith("DENIED"))
        events = {v["placing_event"] for v in self.results["versions"]}
        self.assertEqual(events, {"first_placing", "substantial_modification_placing", "update_to_placed_product"})

    def test_cli_sign_and_verify_record(self):
        import io
        from contextlib import redirect_stdout
        from cra_evidence.cli import main
        t = T.LocalTSA.from_pem_files(os.path.join(PILOT, "keys", "pilot-test-tsa.demo-private.pem"),
                                      os.path.join(PILOT, "trust", "pilot-test-tsa.cert.pem"),
                                      os.path.join(PILOT, "trust", "pilot-test-tsa-root.cert.pem"))
        url = t.serve()
        try:
            rec = os.path.join(PILOT, "out", "records", "requests_2.34.2.record.json")
            out = os.path.join(_TMP, "signed.json")
            with redirect_stdout(io.StringIO()):
                self.assertEqual(main(["sign-record", rec, "--key", os.path.join(
                    PILOT, "keys", "pilot-release-record.demo-private.pem"), "--key-name", "pilot-release-record",
                    "--tsa-url", url, "-o", out]), 0)
            buf = io.StringIO()
            with redirect_stdout(buf):
                rc = main(["verify-record", out, "--policy", PILOT_POLICY, "--product", "requests"])
            self.assertEqual(rc, 0, buf.getvalue())
            self.assertEqual(json.loads(buf.getvalue())["gate_decision"], "PASS")
        finally:
            t.stop()


class PilotWorkflow(unittest.TestCase):
    def test_pilot_workflow_is_valid_pinned_and_read_only(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
        path = os.path.join(ROOT, "examples", "ci", "github-actions-cra-pilot.yml")
        wf = yaml.safe_load(open(path))
        self.assertEqual(wf["permissions"], {"contents": "read"})
        self.assertIn("workflow_dispatch", wf[True] if True in wf else wf["on"])
        import re
        for step in wf["jobs"]["pilot"]["steps"]:
            if "uses" in step:
                self.assertRegex(step["uses"], r"^[\w.-]+/[\w.-]+@[0-9a-f]{40}$")
        runs = " ".join(s.get("run", "") for s in wf["jobs"]["pilot"]["steps"])
        self.assertIn("run_pilot.py", runs)
        self.assertIn("--require-hashes", runs)
        self.assertTrue(re.search(r"verify-evidence-store", runs))


if __name__ == "__main__":
    unittest.main()
