import copy
import json
import os
import unittest

from helpers import (BROWSER_FAIL, BROWSER_OK, LOCK_OK, LOCK_REVIEW, POLICY, bundle, codes, decide)


class ExampleDecisions(unittest.TestCase):
    def test_lock_security_update_passes(self):
        r = decide(bundle(LOCK_OK))
        self.assertEqual(r["decision"], "PASS", r["reasons"])
        self.assertIn("VULN_RESOLVED_BY_VEX", codes(r, "info"))
        self.assertIn("SM_SECURITY_UPDATE", codes(r, "info"))

    def test_lock_functionality_change_needs_review(self):
        r = decide(bundle(LOCK_REVIEW))
        self.assertEqual(r["decision"], "REVIEW")
        self.assertIn("SM_REVIEW_REQUIRED", codes(r, "review"))
        self.assertIn("DECLARATION_DEPENDS_ON_REVIEW", codes(r, "review"))
        self.assertFalse(codes(r, "fail"))

    def test_browser_fail_reasons(self):
        r = decide(bundle(BROWSER_FAIL))
        self.assertEqual(r["decision"], "FAIL")
        self.assertEqual(codes(r, "fail"), {"SBOM_MISSING_TOP_LEVEL_DEPENDENCIES",
                                            "KNOWN_EXPLOITED_UNRESOLVED", "TEST_FINDINGS_OPEN"})

    def test_browser_fixed_release_passes(self):
        r = decide(bundle(BROWSER_OK))
        self.assertEqual(r["decision"], "PASS", r["reasons"])


class SbomAndProvenance(unittest.TestCase):
    def test_missing_sbom_fails(self):
        r = decide(bundle(LOCK_OK, lambda m: m["evidence"].pop("sbom")))
        self.assertIn("SBOM_MISSING", codes(r, "fail"))

    def test_sbom_without_root_edges_fails(self):
        def strip(d):
            p = os.path.join(d, "evidence", "sbom.cdx.json")
            doc = json.load(open(p))
            doc["dependencies"] = [x for x in doc["dependencies"] if not x["ref"].startswith("pkg:generic/aldermoor/hearth-lock-3")]
            json.dump(doc, open(p, "w"))
        r = decide(bundle(LOCK_OK, mutate_files=strip))
        self.assertIn("SBOM_TOP_LEVEL_NOT_RECORDED", codes(r, "fail"))

    def test_untrusted_builder_fails(self):
        p = copy.deepcopy(POLICY)
        p["trusted_builders"] = ["https://build.example.org/other"]
        r = decide(bundle(LOCK_OK), p)
        self.assertIn("PROVENANCE_UNTRUSTED_BUILDER", codes(r, "fail"))

    def test_provenance_subject_mismatch_fails(self):
        def swap(d):
            with open(os.path.join(d, "artefact", "hearth-lock-3-fw-4.2.0.bin"), "ab") as fh:
                fh.write(b"tampered")
        r = decide(bundle(LOCK_OK, mutate_files=swap))
        self.assertIn("PROVENANCE_SUBJECT_MISMATCH", codes(r, "fail"))
        self.assertIn("SBOM_SUBJECT_MISMATCH", codes(r, "fail"))

    def test_missing_provenance_fails(self):
        r = decide(bundle(BROWSER_OK, lambda m: m["evidence"].pop("provenance")))
        self.assertIn("PROVENANCE_MISSING", codes(r, "fail"))


class Vulnerabilities(unittest.TestCase):
    def _lock_with_vex(self, statement):
        def write(d):
            p = os.path.join(d, "evidence", "vex.openvex.json")
            doc = json.load(open(p))
            doc["statements"] = [statement] if statement else []
            json.dump(doc, open(p, "w"))
        return bundle(LOCK_OK, mutate_files=write)

    def test_not_affected_without_justification_fails(self):
        r = decide(self._lock_with_vex({"vulnerability": {"name": "CVE-2022-37434"}, "status": "not_affected"}))
        self.assertIn("VEX_NOT_AFFECTED_UNJUSTIFIED", codes(r, "fail"))

    def test_affected_without_mitigation_fails(self):
        r = decide(self._lock_with_vex({"vulnerability": {"name": "CVE-2022-37434"}, "status": "affected"}))
        self.assertIn("KNOWN_EXPLOITABLE_VULNERABILITY", codes(r, "fail"))

    def test_affected_with_mitigation_reviews(self):
        r = decide(self._lock_with_vex({"vulnerability": {"name": "CVE-2022-37434"}, "status": "affected",
                                        "action_statement": "Disable gzip import in settings"}))
        self.assertEqual(r["decision"], "REVIEW")
        self.assertIn("VULN_AFFECTED_MITIGATED", codes(r, "review"))

    def test_untriaged_critical_fails(self):
        r = decide(self._lock_with_vex(None))
        self.assertIn("VULN_UNTRIAGED", codes(r, "fail"))

    def test_untriaged_medium_reviews(self):
        b = self._lock_with_vex(None)
        for m in b.context["matches"]:
            m["severity"] = "medium"
        r = decide(b)
        self.assertEqual(r["decision"], "REVIEW")

    def test_kev_resolved_by_fixed_vex(self):
        def write(d):
            p = os.path.join(d, "evidence", "vex.csaf.json")
            doc = json.load(open(p))
            doc["vulnerabilities"][0]["product_status"] = {"fixed": ["LB-141.0.7390.54"]}
            json.dump(doc, open(p, "w"))
        r = decide(bundle(BROWSER_FAIL, mutate_files=write))
        self.assertNotIn("KNOWN_EXPLOITED_UNRESOLVED", codes(r))

    def test_missing_vex_fails(self):
        r = decide(bundle(LOCK_OK, lambda m: m["evidence"].pop("vex")))
        self.assertIn("VEX_MISSING", codes(r, "fail"))


class SubstantialModification(unittest.TestCase):
    def _sm(self, **kw):
        def mut(m):
            m["substantial_modification"].update(kw)
        return mut

    def test_functionality_change_without_human_reviews(self):
        r = decide(bundle(LOCK_OK, self._sm(change_type="functionality")))
        self.assertEqual(r["decision"], "REVIEW")
        self.assertIn("SM_FUNCTIONALITY_CHANGE", codes(r, "review"))

    def test_functionality_change_with_recorded_assessment_passes(self):
        r = decide(bundle(LOCK_OK, self._sm(change_type="functionality",
                                            assessed_by="Product security officer, Hearth")))
        self.assertEqual(r["decision"], "PASS", r["reasons"])
        self.assertIn("SM_FUNCTIONALITY_ASSESSED", codes(r, "info"))

    def test_any_question_yes_reviews(self):
        for q in ("new_threat_vectors", "new_attack_scenarios", "changed_likelihood", "changed_impact"):
            def mut(m, q=q):
                m["substantial_modification"]["questions"][q] = True
            r = decide(bundle(LOCK_OK, mut))
            self.assertIn("SM_REVIEW_REQUIRED", codes(r, "review"), q)

    def test_unanswered_question_reviews(self):
        def mut(m):
            m["substantial_modification"]["questions"]["changed_impact"] = None
        r = decide(bundle(LOCK_OK, mut))
        self.assertIn("SM_QUESTIONS_UNANSWERED", codes(r, "review"))

    def test_pt109_boundary_change_reviews(self):
        r = decide(bundle(LOCK_OK, self._sm(change_type="boundary_or_dependency_change")))
        self.assertIn("SM_PT109_CHANGE", codes(r, "review"))

    def test_bundled_without_justification_reviews(self):
        r = decide(bundle(LOCK_OK, self._sm(change_type="security_and_functionality",
                                            assessed_by="PSO", bundling_justification=None)))
        self.assertIn("SECURITY_BUNDLED_UNJUSTIFIED", codes(r, "review"))

    def test_substantial_with_reused_declaration_fails(self):
        def mut(m):
            m["substantial_modification"].update(decision="substantial", assessed_by="PSO",
                                                 conformity_assessment_ref="CA-1")
            m["substantial_modification"]["questions"]["new_threat_vectors"] = True
            m["placing"]["event"] = "substantial_modification_placing"
        r = decide(bundle(LOCK_OK, mut))
        self.assertIn("DECLARATION_REUSE_INVALID", codes(r, "fail"))
        self.assertIn("TEST_EVIDENCE_MISSING", codes(r, "fail"))  # pentest required

    def test_substantial_must_be_new_placing(self):
        def mut(m):
            m["substantial_modification"].update(decision="substantial", assessed_by="PSO",
                                                 conformity_assessment_ref="CA-1")
            m["declaration"]["status"] = "new"
        r = decide(bundle(LOCK_OK, mut))
        self.assertIn("SM_PLACING_EVENT_MISMATCH", codes(r, "fail"))


class SupportRouteDeclaration(unittest.TestCase):
    def test_short_support_without_justification_fails(self):
        def mut(m):
            m["support_period"] = {"end_date": "2031-01-17", "justification": None}
        r = decide(bundle(LOCK_OK, mut))
        self.assertIn("SUPPORT_PERIOD_TOO_SHORT", codes(r, "fail"))

    def test_short_support_with_justification_reviews(self):
        def mut(m):
            m["support_period"] = {"end_date": "2031-01-17", "justification": "Subscription term 3 years"}
        r = decide(bundle(LOCK_OK, mut))
        self.assertEqual(r["decision"], "REVIEW")
        self.assertIn("SUPPORT_PERIOD_SHORT_JUSTIFIED", codes(r, "review"))

    def test_class_i_module_a_without_cited_standard_fails(self):
        def mut(m):
            m["classification"]["conformity_route"] = "module_a"
        r = decide(bundle(LOCK_OK, mut))
        self.assertIn("ROUTE_NOT_PERMITTED", codes(r, "fail"))

    def test_class_i_module_a_with_cited_standard_passes(self):
        def mut(m):
            m["classification"]["conformity_route"] = "module_a"
            m["classification"]["harmonised_standards_applied_in_full"] = ["EN 40000-x (hypothetical citation)"]
        p = copy.deepcopy(POLICY)
        p["harmonised_standards_cited"] = ["EN 40000-x (hypothetical citation)"]
        r = decide(bundle(LOCK_OK, mut), p)
        self.assertNotIn("ROUTE_NOT_PERMITTED", codes(r))

    def test_class_ii_module_a_fails(self):
        def mut(m):
            m["classification"].update({"class": "important_class_ii", "conformity_route": "module_a"})
        self.assertIn("ROUTE_NOT_PERMITTED", codes(decide(bundle(LOCK_OK, mut)), "fail"))

    def test_missing_declaration_fails(self):
        def mut(m):
            m["declaration"] = {"declaration_id": None, "status": "pending"}
        self.assertIn("DECLARATION_MISSING", codes(decide(bundle(LOCK_OK, mut)), "fail"))

    def test_matrix_incomplete_and_unjustified(self):
        def files(d):
            p = os.path.join(d, "docs", "applicability-matrix.json")
            doc = json.load(open(p))
            doc["items"] = [r for r in doc["items"] if r["item"] != "2m"]
            for r in doc["items"]:
                if r["item"] == "2l":
                    r["applies"] = False
            json.dump(doc, open(p, "w"))
        r = decide(bundle(LOCK_OK, mutate_files=files))
        self.assertIn("APPLICABILITY_MATRIX_INCOMPLETE", codes(r, "fail"))
        self.assertIn("APPLICABILITY_NOT_JUSTIFIED", codes(r, "fail"))

    def test_open_pentest_findings_fail(self):
        def files(d):
            p = os.path.join(d, "evidence", "pentest-summary.json")
            doc = json.load(open(p))
            doc["findings"]["high"] = 1
            json.dump(doc, open(p, "w"))
        r = decide(bundle(LOCK_REVIEW, mutate_files=files))
        self.assertIn("TEST_FINDINGS_OPEN", codes(r, "fail"))

    def test_retention_shortened_fails(self):
        b = bundle(LOCK_OK)
        b.record["retention"]["retain_until"] = "2038-01-18"
        self.assertIn("RETENTION_TOO_SHORT", codes(decide(b), "fail"))

    def test_missing_evidence_file_fails(self):
        def files(d):
            os.remove(os.path.join(d, "docs", "annex-ii-user-information.md"))
        r = decide(bundle(LOCK_OK, mutate_files=files))
        self.assertIn("EVIDENCE_FILE_MISSING", codes(r, "fail"))
        self.assertIn("ANNEX_II_MISSING", codes(r, "fail"))


if __name__ == "__main__":
    unittest.main(verbosity=1)
