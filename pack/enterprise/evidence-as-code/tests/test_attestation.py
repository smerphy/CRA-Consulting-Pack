"""Cryptographic verification: DSSE (key-based), Sigstore keyless, transparency log, trust policy."""

import base64
import copy
import datetime as dt
import hashlib
import io
import json
import os
import sys
import unittest
from contextlib import redirect_stdout

from cryptography.hazmat.primitives.asymmetric import ec, ed25519

from helpers import EX, LOCK_OK, LOCK_REVIEW, BROWSER_OK, POLICY, ROOT, bundle, codes, decide

from cra_evidence import attest as A
from cra_evidence import transparency as T
from cra_evidence.cli import main

sys.path.insert(0, EX)
import make_examples as MX  # noqa: E402

REAL = os.path.join(EX, "real", "releases", "npm-sigstore_5.0.0")
REAL_POLICY_PATH = os.path.join(EX, "real", "policy", "real-artefact-gate-policy.json")
REAL_ATT = os.path.join(REAL, "evidence", "npm-attestations.json")
SLSA = "https://slsa.dev/provenance/v1"
PUBLISH = "https://github.com/npm/attestation/tree/main/specs/publish/v0.1"

try:
    import sigstore  # noqa: F401
    HAVE_SIGSTORE = True
except ImportError:
    HAVE_SIGSTORE = False


def statement(digest="ab" * 32, builder=MX.BUILDER):
    return {"_type": "https://in-toto.io/Statement/v1",
            "subject": [{"name": "x.bin", "digest": {"sha256": digest}}],
            "predicateType": SLSA,
            "predicate": {"buildDefinition": {"buildType": "t", "externalParameters": {}},
                          "runDetails": {"builder": {"id": builder}}}}


def trust_for(name, key, purposes=("provenance",), **extra):
    from cryptography.hazmat.primitives import serialization
    pem = key.public_key().public_bytes(serialization.Encoding.PEM,
                                        serialization.PublicFormat.SubjectPublicKeyInfo).decode()
    spec = dict({"algorithm": "x", "public_key_pem": pem, "purposes": list(purposes)}, **extra)
    return A.TrustPolicy({"trust_policy_id": "t", "keys": {name: spec},
                          "products": {"p": {"provenance": {"keys": [name]}, "vex": {"keys": [name]}}}})


def rewrite_provenance(mutate, resign=True):
    """Mutate the lock 4.2.0 provenance statement, optionally re-signing with the build key."""
    def files(d):
        p = os.path.join(d, "evidence", "provenance.intoto.json")
        env = json.load(open(p))
        st = json.loads(base64.b64decode(env["payload"]))
        mutate(st)
        if resign:
            env = MX.sign(st, MX.BUILD_KEY)
        else:
            env["payload"] = base64.b64encode(json.dumps(st).encode()).decode()
        json.dump(env, open(p, "w"))
    return files


def real_policy():
    return json.load(open(REAL_POLICY_PATH))


def real_bundle(mutate_files=None):
    import shutil
    import tempfile
    from cra_evidence import collectors as C
    from cra_evidence.record import build_bundle
    src = REAL
    if mutate_files:
        tmp = tempfile.mkdtemp(prefix="cra-real-")
        src = os.path.join(tmp, "r")
        shutil.copytree(REAL, src)
        mutate_files(src)
    feeds = os.path.join(REAL, "feeds")
    return build_bundle(src, C.load_json(os.path.join(feeds, "osv-snapshot.json"))["vulns"],
                        C.load_kev(C.load_json(os.path.join(feeds, "kev-snapshot.json"))),
                        generated_at="2026-11-01T12:00:00Z")


class Envelope(unittest.TestCase):
    def test_pae_matches_dsse_spec(self):
        self.assertEqual(A.pae("http://example.com/HelloWorld", b"hello world"),
                         b"DSSEv1 29 http://example.com/HelloWorld 11 hello world")

    def _roundtrip(self, key):
        env = A.sign_envelope(statement(), key)
        res = A.verify(A.load_attestations(env)[0], trust_for("k", key), "p", "provenance")
        self.assertTrue(res["verified"], res["problems"])
        self.assertEqual(res["statement"]["subject"][0]["digest"]["sha256"], "ab" * 32)

    def test_ecdsa_p256_verifies(self):
        self._roundtrip(ec.generate_private_key(ec.SECP256R1()))

    def test_ed25519_verifies(self):
        self._roundtrip(ed25519.Ed25519PrivateKey.generate())

    def test_tampered_payload_rejected(self):
        k = ed25519.Ed25519PrivateKey.generate()
        env = A.sign_envelope(statement(), k)
        st = statement(digest="cd" * 32)
        env["payload"] = base64.b64encode(json.dumps(st).encode()).decode()
        res = A.verify(A.load_attestations(env)[0], trust_for("k", k), "p", "provenance")
        self.assertFalse(res["verified"])
        self.assertEqual(res["problems"][0][0], "SIGNATURE_INVALID")
        self.assertIsNone(res["statement"])

    def test_unknown_key_rejected(self):
        env = A.sign_envelope(statement(), ec.generate_private_key(ec.SECP256R1()))
        res = A.verify(A.load_attestations(env)[0], trust_for("k", ec.generate_private_key(ec.SECP256R1())),
                       "p", "provenance")
        self.assertEqual(res["problems"][0][0], "SIGNATURE_INVALID")

    def test_payload_type_checked(self):
        k = ed25519.Ed25519PrivateKey.generate()
        env = A.sign_envelope(statement(), k)
        env["payloadType"] = "text/plain"
        res = A.verify(A.load_attestations(env)[0], trust_for("k", k), "p", "provenance")
        self.assertEqual(res["problems"][0][0], "PAYLOAD_TYPE_UNSUPPORTED")

    def test_key_expired(self):
        k = ed25519.Ed25519PrivateKey.generate()
        env = A.sign_envelope(statement(), k)
        res = A.verify(A.load_attestations(env)[0], trust_for("k", k, not_after="2026-01-01T00:00:00Z"), "p",
                       "provenance", now=dt.datetime(2026, 11, 1, tzinfo=dt.timezone.utc))
        self.assertEqual(res["problems"][0][0], "KEY_EXPIRED")
        self.assertFalse(res["verified"])

    def test_key_not_yet_valid(self):
        k = ed25519.Ed25519PrivateKey.generate()
        env = A.sign_envelope(statement(), k)
        res = A.verify(A.load_attestations(env)[0], trust_for("k", k, not_before="2030-01-01T00:00:00Z"), "p",
                       "provenance", now=dt.datetime(2026, 11, 1, tzinfo=dt.timezone.utc))
        self.assertEqual(res["problems"][0][0], "KEY_NOT_YET_VALID")

    def test_key_revoked_by_status_and_by_list(self):
        k = ed25519.Ed25519PrivateKey.generate()
        env = A.sign_envelope(statement(), k)
        res = A.verify(A.load_attestations(env)[0], trust_for("k", k, status="revoked"), "p", "provenance")
        self.assertEqual(res["problems"][0][0], "KEY_REVOKED")
        tp = trust_for("k", k)
        tp.revoked = {A.keyid_for(k.public_key())}
        self.assertEqual(A.verify(A.load_attestations(env)[0], tp, "p", "provenance")["problems"][0][0], "KEY_REVOKED")

    def test_wrong_purpose_not_authorised(self):
        k = ed25519.Ed25519PrivateKey.generate()
        env = A.sign_envelope(statement(), k)
        res = A.verify(A.load_attestations(env)[0], trust_for("k", k, purposes=("vex",)), "p", "provenance")
        self.assertEqual(res["problems"][0][0], "SIGNER_NOT_AUTHORISED")

    def test_no_trust_configured_fails_closed(self):
        env = A.sign_envelope(statement(), ed25519.Ed25519PrivateKey.generate())
        res = A.verify(A.load_attestations(env)[0], A.TrustPolicy({}), "p", "provenance")
        self.assertEqual(res["problems"][0][0], "NO_TRUSTED_SIGNER")

    def test_bare_statement_is_unsigned(self):
        res = A.verify(A.load_attestations(statement())[0], A.TrustPolicy({}), "p", "provenance")
        self.assertEqual(res["problems"][0][0], "UNSIGNED")

    def test_jsonl_loader(self):
        k = ed25519.Ed25519PrivateKey.generate()
        text = json.dumps(A.sign_envelope(statement(), k)) + "\n" + json.dumps(A.sign_envelope(statement("cd" * 32), k))
        self.assertEqual(len(A.load_attestations(text)), 2)


class GateProvenance(unittest.TestCase):
    def test_example_records_carry_verification(self):
        b = bundle(LOCK_OK)
        r = decide(b)
        v = b.record["evidence"]["provenance"]["verification"]
        self.assertTrue(v["verified"])
        self.assertEqual((v["method"], v["slsa_build_level"]), ("key", 3))
        self.assertTrue(b.record["evidence"]["vulnerability_status"]["verification"]["verified"])
        self.assertIn("PROVENANCE_VERIFIED", codes(r, "info"))

    def test_tampered_provenance_fails(self):
        r = decide(bundle(LOCK_OK, mutate_files=rewrite_provenance(
            lambda st: st["predicate"]["runDetails"]["builder"].update(id="https://evil.example/b"), resign=False),
            resign_after=False))
        self.assertEqual(r["decision"], "FAIL")
        self.assertIn("PROVENANCE_SIGNATURE_INVALID", codes(r, "fail"))
        self.assertNotIn("PROVENANCE_VERIFIED", codes(r))

    def test_unsigned_provenance_fails(self):
        def files(d):
            p = os.path.join(d, "evidence", "provenance.intoto.json")
            env = json.load(open(p))
            json.dump(json.loads(base64.b64decode(env["payload"])), open(p, "w"))
        r = decide(bundle(LOCK_OK, mutate_files=files, resign_after=False))
        self.assertIn("PROVENANCE_UNSIGNED", codes(r, "fail"))

    def test_wrong_subject_digest_fails_even_when_signed(self):
        r = decide(bundle(LOCK_OK, mutate_files=rewrite_provenance(
            lambda st: st["subject"][0]["digest"].update(sha256="0" * 64))))
        self.assertIn("PROVENANCE_SUBJECT_MISMATCH", codes(r, "fail"))
        self.assertNotIn("PROVENANCE_SIGNATURE_INVALID", codes(r))

    def test_signed_claim_of_untrusted_builder_fails(self):
        r = decide(bundle(LOCK_OK, mutate_files=rewrite_provenance(
            lambda st: st["predicate"]["runDetails"]["builder"].update(id="https://ci.example/laptop"))))
        self.assertIn("PROVENANCE_UNTRUSTED_BUILDER", codes(r, "fail"))
        self.assertIn("PROVENANCE_BUILD_LEVEL_INSUFFICIENT", codes(r, "fail"))

    def test_provenance_signed_by_vex_key_not_authorised(self):
        def files(d):
            p = os.path.join(d, "evidence", "provenance.intoto.json")
            st = json.loads(base64.b64decode(json.load(open(p))["payload"]))
            json.dump(MX.sign(st, MX.PSIRT_KEY), open(p, "w"))
        r = decide(bundle(LOCK_OK, mutate_files=files, resign_after=False))
        self.assertIn("PROVENANCE_SIGNER_NOT_AUTHORISED", codes(r, "fail"))

    def test_expired_build_key_fails(self):
        p = copy.deepcopy(POLICY)
        p["attestation_trust"]["keys"][MX.BUILD_KEY]["not_after"] = "2026-06-30T00:00:00Z"
        r = G_decide(bundle(LOCK_OK), p, now=dt.datetime(2026, 11, 1, tzinfo=dt.timezone.utc))
        self.assertIn("PROVENANCE_KEY_EXPIRED", codes(r, "fail"))

    def test_revoked_build_key_fails(self):
        p = copy.deepcopy(POLICY)
        p["attestation_trust"]["revoked_keyids"] = [p["attestation_trust"]["keys"][MX.BUILD_KEY]["keyid"]]
        self.assertIn("PROVENANCE_KEY_REVOKED", codes(decide(bundle(LOCK_OK), p), "fail"))

    def test_builder_level_policy(self):
        p = copy.deepcopy(POLICY)
        p["attestation_trust"]["builders"][MX.BUILDER]["slsa_build_level"] = 2
        self.assertIn("PROVENANCE_BUILD_LEVEL_INSUFFICIENT", codes(decide(bundle(LOCK_OK), p), "fail"))
        p["attestation_trust"]["products"]["hearth-lock-3"]["provenance"]["min_slsa_build_level"] = 2
        self.assertNotIn("PROVENANCE_BUILD_LEVEL_INSUFFICIENT", codes(decide(bundle(LOCK_OK), p)))

    def test_builder_signer_binding(self):
        p = copy.deepcopy(POLICY)
        p["attestation_trust"]["builders"][MX.BUILDER]["signers"] = ["key:some-other-key"]
        self.assertIn("PROVENANCE_BUILDER_SIGNER_MISMATCH", codes(decide(bundle(LOCK_OK), p), "fail"))

    def test_unrecognised_external_parameters_fail(self):
        r = decide(bundle(LOCK_OK, mutate_files=rewrite_provenance(
            lambda st: st["predicate"]["buildDefinition"]["externalParameters"].update(debug_shell="true"))))
        self.assertIn("PROVENANCE_EXTERNAL_PARAMETERS_UNEXPECTED", codes(r, "fail"))

    def test_external_parameter_value_mismatch_fails(self):
        r = decide(bundle(LOCK_OK, mutate_files=rewrite_provenance(
            lambda st: st["predicate"]["buildDefinition"]["externalParameters"].update(
                source="git+https://github.com/attacker/fork@refs/heads/main"))))
        self.assertIn("PROVENANCE_EXTERNAL_PARAMETERS_UNEXPECTED", codes(r, "fail"))

    def test_unexpected_build_type_fails(self):
        r = decide(bundle(LOCK_OK, mutate_files=rewrite_provenance(
            lambda st: st["predicate"]["buildDefinition"].update(buildType="https://example/ad-hoc"))))
        self.assertIn("PROVENANCE_BUILD_TYPE_UNEXPECTED", codes(r, "fail"))

    def test_default_policy_fails_closed(self):
        r = G_decide(bundle(LOCK_OK), {})
        self.assertIn("PROVENANCE_NO_TRUSTED_SIGNER", codes(r, "fail"))
        self.assertIn("VEX_NO_TRUSTED_SIGNER", codes(r, "fail"))


def G_decide(b, policy, now=None):
    from cra_evidence import gate as G
    return G.evaluate(b, copy.deepcopy(policy), now=now)


class GateVex(unittest.TestCase):
    def test_unsigned_vex_fails(self):
        r = decide(bundle(LOCK_OK, lambda m: m["evidence"].pop("vex_attestation")))
        self.assertIn("VEX_UNSIGNED", codes(r, "fail"))

    def test_plain_vex_edited_after_signing_fails(self):
        def files(d):
            p = os.path.join(d, "evidence", "vex.openvex.json")
            doc = json.load(open(p))
            doc["statements"][0]["status"] = "fixed"
            json.dump(doc, open(p, "w"))
        r = decide(bundle(LOCK_OK, mutate_files=files, resign_after=False))
        self.assertIn("VEX_ATTESTATION_MISMATCH", codes(r, "fail"))

    def test_tampered_vex_attestation_fails(self):
        def files(d):
            p = os.path.join(d, "evidence", "vex.openvex.intoto.json")
            env = json.load(open(p))
            st = json.loads(base64.b64decode(env["payload"]))
            st["predicate"]["statements"][0]["justification"] = "component_not_present"
            env["payload"] = base64.b64encode(json.dumps(st).encode()).decode()
            json.dump(env, open(p, "w"))
        r = decide(bundle(LOCK_OK, mutate_files=files, resign_after=False))
        self.assertIn("VEX_SIGNATURE_INVALID", codes(r, "fail"))

    def test_vex_signed_by_build_key_not_authorised(self):
        def files(d):
            p = os.path.join(d, "evidence", "vex.openvex.intoto.json")
            st = json.loads(base64.b64decode(json.load(open(p))["payload"]))
            json.dump(MX.sign(st, MX.BUILD_KEY), open(p, "w"))
        r = decide(bundle(LOCK_OK, mutate_files=files, resign_after=False))
        self.assertIn("VEX_SIGNER_NOT_AUTHORISED", codes(r, "fail"))

    def test_vex_for_other_artefact_fails(self):
        def files(d):
            with open(os.path.join(d, "artefact", "hearth-lock-3-fw-4.2.0.bin"), "ab") as fh:
                fh.write(b"x")
        r = decide(bundle(LOCK_OK, mutate_files=files))
        self.assertIn("VEX_SUBJECT_MISMATCH", codes(r, "fail"))

    def test_csaf_vex_attestation_verified(self):
        b = bundle(BROWSER_OK)
        r = decide(b)
        self.assertIn("VEX_VERIFIED", codes(r, "info"))
        self.assertEqual(b.record["evidence"]["vulnerability_status"]["verification"]["signer"]["key"], MX.PSIRT_KEY)


class Transparency(unittest.TestCase):
    def test_rfc9162_inclusion_small_tree(self):
        leaves = [hashlib.sha256(b"\x00" + bytes([i])).digest() for i in range(5)]
        h = lambda a, b: hashlib.sha256(b"\x01" + a + b).digest()  # noqa: E731
        n01, n23 = h(leaves[0], leaves[1]), h(leaves[2], leaves[3])
        root = h(h(n01, n23), leaves[4])
        self.assertEqual(T.root_from_inclusion_proof(2, 5, leaves[2], [leaves[3], n01, leaves[4]]), root)
        self.assertEqual(T.root_from_inclusion_proof(4, 5, leaves[4], [h(n01, n23)]), root)
        with self.assertRaises(T.TlogError):
            T.root_from_inclusion_proof(5, 5, leaves[4], [])

    def _publish(self):
        atts = A.load_attestation_file(REAL_ATT)
        return A.select(atts, (PUBLISH,)), A.TrustPolicy(real_policy()["attestation_trust"])

    def test_real_npm_publish_attestation_key_and_tlog(self):
        att, tp = self._publish()
        res = A.verify(att, tp, "npm-sigstore", "publish")
        self.assertTrue(res["verified"], res["problems"])
        self.assertEqual(res["signer"]["key"], "npm-registry-2")
        self.assertTrue(res["tlog"]["inclusion_proof"] and res["tlog"]["checkpoint"]
                        and res["tlog"]["signed_entry_timestamp"])
        self.assertEqual(res["signer"]["signing_time_source"], "transparency log integrated time")

    def test_tampered_inclusion_proof_rejected(self):
        att, tp = self._publish()
        proof = att.raw["verificationMaterial"]["tlogEntries"][0]["inclusionProof"]
        h = bytearray(base64.b64decode(proof["hashes"][3]))
        h[0] ^= 1
        proof["hashes"][3] = base64.b64encode(bytes(h)).decode()
        res = A.verify(att, tp, "npm-sigstore", "publish")
        self.assertEqual(res["problems"][0][0], "TLOG_INVALID")

    def test_forged_checkpoint_rejected(self):
        att, tp = self._publish()
        e = att.raw["verificationMaterial"]["tlogEntries"][0]
        e["inclusionProof"]["checkpoint"]["envelope"] = e["inclusionProof"]["checkpoint"]["envelope"].replace(
            "\n\n", "\nextra\n\n", 1)
        res = A.verify(att, tp, "npm-sigstore", "publish")
        self.assertEqual(res["problems"][0][0], "TLOG_INVALID")

    def test_required_tlog_missing(self):
        att, tp = self._publish()
        att.raw["verificationMaterial"]["tlogEntries"] = []
        self.assertEqual(A.verify(att, tp, "npm-sigstore", "publish")["problems"][0][0], "TLOG_MISSING")


@unittest.skipUnless(HAVE_SIGSTORE, "sigstore-python not installed")
class RealKeyless(unittest.TestCase):
    """Sigstore keyless SLSA v1 provenance for the real npm package, verified offline."""

    def _att(self):
        return A.select(A.load_attestation_file(REAL_ATT), (SLSA,))

    def _trust(self, mutate=None):
        cfg = real_policy()["attestation_trust"]
        if mutate:
            mutate(cfg["products"]["npm-sigstore"]["provenance"]["identities"][0])
        return A.TrustPolicy(cfg)

    def test_verifies_offline_with_pinned_root(self):
        res = A.verify(self._att(), self._trust(), "npm-sigstore", "provenance")
        self.assertTrue(res["verified"], res["problems"])
        self.assertEqual(res["method"], "sigstore-keyless")
        self.assertEqual(res["signer"]["extensions"]["source_repository_digest"],
                         "7d2900eca1c22b3f87c13987c8d4b7c9a29b733a")
        self.assertTrue(res["tlog"]["inclusion_proof"])
        self.assertIn("cra_evidence.transparency", res["tlog"]["verified_by"])
        digs = {"sha512": hashlib.sha512(open(os.path.join(REAL, "artefact", "sigstore-5.0.0.tgz"), "rb").read()).hexdigest()}
        self.assertEqual(A.subject_matches(res["statement"], digs), "sha512")

    def test_wrong_san_is_identity_mismatch(self):
        res = A.verify(self._att(), self._trust(lambda r: r.update(
            san="https://github.com/sigstore/sigstore-js/.github/workflows/other.yml@refs/heads/main")),
            "npm-sigstore", "provenance")
        self.assertEqual(res["problems"][0][0], "IDENTITY_MISMATCH")

    def test_wrong_issuer_is_identity_mismatch(self):
        res = A.verify(self._att(), self._trust(lambda r: r.update(issuer="https://accounts.google.com")),
                       "npm-sigstore", "provenance")
        self.assertEqual(res["problems"][0][0], "IDENTITY_MISMATCH")

    def test_wrong_source_repository_is_identity_mismatch(self):
        res = A.verify(self._att(), self._trust(lambda r: r["extensions"].update(
            source_repository_uri="https://github.com/attacker/sigstore-js")), "npm-sigstore", "provenance")
        self.assertEqual(res["problems"][0][0], "IDENTITY_MISMATCH")

    def test_tampered_payload_fails(self):
        att = self._att()
        st = json.loads(att.payload)
        st["subject"][0]["digest"]["sha512"] = "0" * 128
        att.raw["dsseEnvelope"]["payload"] = base64.b64encode(json.dumps(st).encode()).decode()
        res = A.verify(A.load_attestations(att.raw)[0], self._trust(), "npm-sigstore", "provenance")
        self.assertFalse(res["verified"])
        self.assertEqual(res["problems"][0][0], "SIGNATURE_INVALID")

    def test_sigstore_missing_fails_closed(self):
        saved = {k: sys.modules[k] for k in list(sys.modules) if k == "sigstore" or k.startswith("sigstore.")}
        try:
            for k in saved:
                sys.modules[k] = None
            res = A.verify(self._att(), self._trust(), "npm-sigstore", "provenance")
            self.assertEqual(res["problems"][0][0], "SIGSTORE_UNAVAILABLE")
        finally:
            sys.modules.update(saved)


@unittest.skipUnless(HAVE_SIGSTORE, "sigstore-python not installed")
class RealArtefactGate(unittest.TestCase):
    def test_end_to_end_review_with_all_signatures_verified(self):
        b = real_bundle()
        r = decide(b, real_policy())
        self.assertEqual(r["decision"], "REVIEW", r["reasons"])
        self.assertEqual(codes(r, "review"), {"VULN_UNTRIAGED"})
        self.assertTrue({"PROVENANCE_VERIFIED", "VEX_VERIFIED", "SBOM_OK"} <= codes(r, "info"))
        v = b.record["evidence"]["provenance"]["verification"]
        self.assertEqual((v["method"], v["slsa_build_level"]), ("sigstore-keyless", 2))

    def test_requiring_build_l3_blocks_it(self):
        p = real_policy()
        p["attestation_trust"]["products"]["npm-sigstore"]["provenance"]["min_slsa_build_level"] = 3
        self.assertIn("PROVENANCE_BUILD_LEVEL_INSUFFICIENT", codes(decide(real_bundle(), p), "fail"))

    def test_swapped_tarball_fails(self):
        def files(d):
            with open(os.path.join(d, "artefact", "sigstore-5.0.0.tgz"), "ab") as fh:
                fh.write(b"\0")
        r = decide(real_bundle(files), real_policy())
        self.assertIn("PROVENANCE_SUBJECT_MISMATCH", codes(r, "fail"))
        self.assertIn("VEX_SUBJECT_MISMATCH", codes(r, "fail"))
        self.assertIn("SBOM_SUBJECT_MISMATCH", codes(r, "fail"))

    def test_unexpected_ref_fails(self):
        p = real_policy()
        p["attestation_trust"]["products"]["npm-sigstore"]["provenance"]["external_parameters"][
            "workflow.ref"] = "refs/tags/v5.0.0"
        self.assertIn("PROVENANCE_EXTERNAL_PARAMETERS_UNEXPECTED", codes(decide(real_bundle(), p), "fail"))


class CliAndSchema(unittest.TestCase):
    def _run(self, *argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(list(argv))
        return rc, buf.getvalue()

    def test_verify_attestation_cli(self):
        rc, out = self._run("verify-attestation", REAL_ATT, "--policy", REAL_POLICY_PATH, "--product",
                            "npm-sigstore", "--purpose", "publish", "--predicate-type", PUBLISH,
                            "--artefact", os.path.join(REAL, "artefact", "sigstore-5.0.0.tgz"))
        self.assertEqual(rc, 0, out)
        self.assertEqual(json.loads(out)["artefact"]["subject_match"], "sha512")
        rc, out = self._run("verify-attestation", REAL_ATT, "--policy", REAL_POLICY_PATH, "--product",
                            "npm-sigstore", "--purpose", "publish", "--predicate-type", PUBLISH,
                            "--artefact", os.path.join(EX, "releases", LOCK_OK, "artefact", "hearth-lock-3-fw-4.2.0.bin"))
        self.assertEqual(rc, 1)

    def test_records_validate_against_declared_schema(self):
        from cra_evidence import schema as S
        b = bundle(LOCK_REVIEW)
        b.record["gate"] = decide(b)
        self.assertEqual(b.record["schema_version"], "1.1.0")
        self.assertEqual(S.validate(b.record), [])
        self.assertEqual(S.validate(b.record, force_fallback=True), [])
        legacy = copy.deepcopy(b.record)
        legacy["schema_version"] = "1.0.0"
        del legacy["evidence"]["provenance"]["verification"]
        for k in ("verification", "attestation"):
            legacy["evidence"]["vulnerability_status"].pop(k, None)
        self.assertEqual(S.validate(legacy), [])
        bad = copy.deepcopy(b.record)
        bad["evidence"]["provenance"]["verification"]["method"] = "trust-me"
        self.assertTrue(S.validate(bad, force_fallback=True))


class CiWorkflow(unittest.TestCase):
    def test_github_actions_yaml_is_valid_and_pinned(self):
        try:
            import yaml
        except ImportError:
            self.skipTest("PyYAML not installed")
        import re
        path = os.path.join(EX, "ci", "github-actions-cra-release-gate.yml")
        wf = yaml.safe_load(open(path))
        self.assertIn("jobs", wf)
        on = wf.get("on", wf.get(True))          # YAML 1.1 reads the key 'on' as boolean True
        self.assertTrue(on)
        uses = [s["uses"] for j in wf["jobs"].values() for s in j.get("steps", []) if "uses" in s]
        self.assertTrue(uses)
        for u in uses:
            self.assertRegex(u, r"^[\w.-]+/[\w.-]+(/[\w.-]+)*@[0-9a-f]{40}$", u)
        perms = wf["jobs"]["build-and-attest"]["permissions"]
        self.assertEqual((perms["id-token"], perms["attestations"]), ("write", "write"))
        text = open(path).read()
        self.assertIn("python -m cra_evidence gate", text)
        self.assertFalse(re.search(r"@0{40}", text))


class Benchmark(unittest.TestCase):
    def test_benchmark_smoke(self):
        sys.path.insert(0, os.path.join(ROOT, "bench"))
        import bench_scale
        res = bench_scale.run(n=6, workers=1, min_components=200, max_components=260, feed_size=500, seed=7,
                              quiet=True)
        self.assertEqual(res["versions"], 6)
        self.assertEqual(sum(res["decisions"].values()), 6)
        self.assertGreater(res["per_core_versions_per_second"], 0)
        self.assertEqual(res["signature_failures"], 0)


if __name__ == "__main__":
    unittest.main(verbosity=1)
