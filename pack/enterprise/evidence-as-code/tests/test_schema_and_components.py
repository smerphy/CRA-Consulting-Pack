import base64
import copy
import datetime as dt
import io
import json
import os
import shutil
import tempfile
import unittest
from contextlib import redirect_stdout

from helpers import (BROWSER_FAIL, BROWSER_OK, LOCK_OK, LOCK_REVIEW, POLICY, ROOT, RELEASES, bundle, decide)

from cra_evidence import collectors as C
from cra_evidence import index as I
from cra_evidence import retention as R
from cra_evidence import schema as S
from cra_evidence import store as ST
from cra_evidence.cli import main

ALL = [LOCK_OK, LOCK_REVIEW, BROWSER_FAIL, BROWSER_OK]


def gated(name):
    b = bundle(name)
    b.record["gate"] = decide(b)
    return b


class Schema(unittest.TestCase):
    def test_examples_valid_both_validators(self):
        for name in ALL:
            rec = gated(name).record
            self.assertEqual(S.validate(rec, force_fallback=True), [], name)
            if S.have_jsonschema():
                self.assertEqual(S.validate(rec), [], name)

    def test_schema_every_property_has_legal_basis(self):
        schema = S.load_schema()
        for key, prop in schema["properties"].items():
            self.assertIn("x-cra-basis", prop, key)

    def _invalid(self, mutate):
        rec = copy.deepcopy(gated(LOCK_OK).record)
        mutate(rec)
        fb = S.validate(rec, force_fallback=True)
        self.assertTrue(fb, "fallback accepted invalid record")
        if S.have_jsonschema():
            self.assertTrue(S.validate(rec), "jsonschema accepted invalid record")

    def test_bad_digest_rejected(self):
        self._invalid(lambda r: r["evidence"]["sbom"]["digests"].update(sha256="xyz"))

    def test_missing_required_rejected(self):
        self._invalid(lambda r: r.pop("retention"))

    def test_bad_enum_rejected(self):
        self._invalid(lambda r: r["substantial_modification"].update(change_type="refactor"))

    def test_bad_date_rejected(self):
        self._invalid(lambda r: r["support_period"].update(end_date="31/12/2039"))

    def test_extra_property_rejected(self):
        self._invalid(lambda r: r.update(comment="free text"))


class Retention(unittest.TestCase):
    def test_placing_plus_ten_dominates(self):
        self.assertEqual(R.retain_until("2028-02-03", "2033-02-28"), dt.date(2038, 2, 3))

    def test_support_end_dominates(self):
        self.assertEqual(R.retain_until("2028-01-18", "2039-12-31"), dt.date(2039, 12, 31))

    def test_leap_day(self):
        self.assertEqual(R.retain_until("2028-02-29", "2030-01-01"), dt.date(2038, 2, 28))

    def test_record_uses_rule(self):
        self.assertEqual(gated(LOCK_OK).record["retention"]["retain_until"], "2039-12-31")
        # 141.0.7390.65 is a security update that keeps the placing date of
        # 141.0.7390.40 (2028-01-06; guidance para 15, Example 2).
        rec = gated(BROWSER_OK).record
        self.assertEqual(rec["retention"]["retain_until"], "2038-01-06")
        self.assertIn("inherited from version 141.0.7390.40", rec["retention"]["rule"])

    def test_inherited_placing_date_used_where_earlier(self):
        self.assertEqual(R.retain_until("2028-02-10", "2033-02-28", inherited_placing_date="2028-01-06"),
                         dt.date(2038, 1, 6))
        # a later "inherited" date never extends or shortens below the version date rule
        self.assertEqual(R.retain_until("2028-02-10", "2033-02-28", inherited_placing_date="2028-03-01"),
                         dt.date(2038, 2, 10))
        # support end still dominates when later
        self.assertEqual(R.retain_until("2028-02-10", "2039-12-31", inherited_placing_date="2028-01-06"),
                         dt.date(2039, 12, 31))

    def test_effective_placing_date(self):
        upd = {"date": "2028-02-10", "event": "update_to_placed_product", "inherited_placing_date": "2028-01-06"}
        self.assertEqual(R.effective_placing_date(upd), dt.date(2028, 1, 6))
        new = dict(upd, event="substantial_modification_placing")
        self.assertEqual(R.effective_placing_date(new), dt.date(2028, 2, 10))
        self.assertEqual(R.effective_placing_date({"date": "2028-02-10", "event": "update_to_placed_product"}),
                         dt.date(2028, 2, 10))
        self.assertIsNone(R.effective_placing_date({}))

    def test_update_availability(self):
        self.assertEqual(R.update_available_until("2028-02-10", "2033-02-28"), dt.date(2038, 2, 10))


class Collectors(unittest.TestCase):
    def test_cyclonedx(self):
        n = C.normalise_sbom(C.load_json(os.path.join(RELEASES, LOCK_OK, "evidence", "sbom.cdx.json")))
        self.assertEqual((n["format"], n["spec_version"]), ("CycloneDX", "1.5"))
        self.assertIn("zlib", n["top_level_dependencies"])
        self.assertTrue(n["top_level_recorded"])

    def test_spdx(self):
        n = C.normalise_sbom(C.load_json(os.path.join(RELEASES, BROWSER_FAIL, "evidence", "sbom.spdx.json")))
        self.assertEqual((n["format"], n["spec_version"]), ("SPDX", "2.3"))
        self.assertNotIn("harfbuzz", n["top_level_dependencies"])
        self.assertIn("harfbuzz", [c["name"] for c in n["components"]])

    def test_not_an_sbom(self):
        with self.assertRaises(C.CollectorError):
            C.normalise_sbom({"hello": "world"})

    def test_dsse_provenance(self):
        n = C.normalise_provenance(C.load_json(os.path.join(RELEASES, BROWSER_OK, "evidence", "provenance.intoto.json")))
        self.assertTrue(n["dsse_envelope"])
        self.assertEqual(n["predicate_type"], "https://slsa.dev/provenance/v1")

    def test_bad_dsse_payload_type(self):
        with self.assertRaises(C.CollectorError):
            C.normalise_provenance({"payloadType": "text/plain", "payload": base64.b64encode(b"{}").decode()})

    def test_csaf_and_openvex(self):
        c = C.normalise_vex(C.load_json(os.path.join(RELEASES, BROWSER_FAIL, "evidence", "vex.csaf.json")))
        self.assertEqual(c["statements"][0]["status"], "under_investigation")
        o = C.normalise_vex(C.load_json(os.path.join(RELEASES, LOCK_OK, "evidence", "vex.openvex.json")))
        self.assertEqual(o["statements"][0]["justification"], "vulnerable_code_not_in_execute_path")

    def test_sarif_suppression_counted(self):
        s = C.normalise_sarif(C.load_json(os.path.join(RELEASES, LOCK_OK, "evidence", "sast.sarif")))
        self.assertEqual(s["summary"], {"error": 0, "warning": 1, "note": 1, "suppressed": 1})

    def test_osv_ranges(self):
        ev = [{"introduced": "0"}, {"fixed": "1.2.13"}]
        self.assertTrue(C.version_in_range("1.2.12", ev))
        self.assertFalse(C.version_in_range("1.2.13", ev))
        self.assertFalse(C.version_in_range("1.3.1", ev))
        self.assertFalse(C.version_in_range("2.0", [{"introduced": "3.0.0"}, {"fixed": "3.5.2"}]))


class IndexAndStore(unittest.TestCase):
    def test_index_points(self):
        idx = I.build_index(gated(LOCK_OK).record)
        self.assertEqual([p["point"] for p in idx["points"]], ["1", "2(a)", "2(b)", "2(c)", "3", "4", "5", "6", "7", "8"])
        md = I.render_markdown(idx)
        self.assertIn("Annex VII index: hearth-lock-3 4.2.0", md)

    def test_store_append_only_and_tamper_evident(self):
        tmp = tempfile.mkdtemp()
        try:
            b = gated(LOCK_OK)
            ST.put_record(tmp, b.record, os.path.join(RELEASES, LOCK_OK), ["evidence/sbom.cdx.json"])
            with self.assertRaises(ST.StoreError):
                ST.put_record(tmp, b.record, os.path.join(RELEASES, LOCK_OK), [])
            b2 = gated(BROWSER_OK)
            ST.put_record(tmp, b2.record, os.path.join(RELEASES, BROWSER_OK), [])
            self.assertEqual(ST.verify(tmp), [])
            rdir = os.path.join(tmp, "records", "hearth-lock-3", "4.2.0")
            f = os.path.join(rdir, os.listdir(rdir)[0])
            os.chmod(f, 0o644)
            with open(f, "a") as fh:
                fh.write(" ")
            self.assertTrue(any("altered" in p for p in ST.verify(tmp)))
        finally:
            for dirpath, _, files in os.walk(tmp):
                for fn in files:
                    os.chmod(os.path.join(dirpath, fn), 0o644)
            shutil.rmtree(tmp)


class Cli(unittest.TestCase):
    def _run(self, *argv):
        buf = io.StringIO()
        with redirect_stdout(buf):
            rc = main(list(argv))
        return rc, buf.getvalue()

    def test_gate_exit_codes(self):
        pol = os.path.join(ROOT, "examples", "policy", "aldermoor-gate-policy.json")
        feeds = os.path.join(ROOT, "examples", "feeds")
        expect = {LOCK_OK: 0, LOCK_REVIEW: 3, BROWSER_FAIL: 1, BROWSER_OK: 0}
        for name, code in expect.items():
            rc, out = self._run("gate", os.path.join(RELEASES, name), "--policy", pol, "--feeds", feeds)
            self.assertEqual(rc, code, out)

    def test_retention_cli(self):
        rc, out = self._run("retention", "--placing", "2028-01-18", "--support-end", "2039-12-31")
        self.assertEqual(json.loads(out)["retain_until"], "2039-12-31")
        rc, out = self._run("retention", "--placing", "2028-02-10", "--support-end", "2033-02-28",
                            "--inherited-placing", "2028-01-06")
        res = json.loads(out)
        self.assertEqual((res["retain_until"], res["placing_date"], res["version_date"]),
                         ("2038-01-06", "2028-01-06", "2028-02-10"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
