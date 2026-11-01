"""Release gate: PASS / FAIL / REVIEW for one product version.

Each rule emits reasons with a machine-readable code, a severity (fail,
review, info), a message and the legal basis as summarised in the knowledge
base. Decision = FAIL if any fail reason, else REVIEW if any review reason,
else PASS. The gate decides whether the pipeline may proceed; it does not
decide conformity. REVIEW routes the version to a named human role.
"""

import datetime as _dt
import json
import re

from . import attest as A
from .record import PART_I_ITEMS
from .retention import parse_date, retain_until

DEFAULT_POLICY = {
    "policy_id": "aldermoor-cra-gate/1.1.0",
    "trusted_builders": [],
    "accepted_predicate_types": ["https://slsa.dev/provenance/v1"],
    # OpenVEX in-toto predicate types (vexctl / cosign conventions) and an
    # Aldermoor convention for CSAF VEX, for which no standard in-toto
    # predicate type exists.
    "accepted_vex_predicate_types": ["https://openvex.dev/ns/v0.2.0", "https://openvex.dev/ns",
                                     "https://aldermoor.example/attestation/csaf-vex/v2.0"],
    # Fail closed: with no trust configuration nothing verifies.
    "attestation_trust": {},
    "min_support_years": 5,
    "fail_untriaged_severities": ["critical", "high"],
    "required_tests": {"default": ["sast"]},
    "pentest_required_on": ["first_placing", "substantial"],
    "sarif_fail_level": "error",
    "harmonised_standards_cited": [],
    # Conformity-assessment obligations (route, notified-body certificate)
    # apply to units placed on or after this date (Art 69(2), Art 71(2)). Before it,
    # route and certificate findings are INFO, so the gate does not block EU
    # releases while no notified body can yet issue a certificate.
    "conformity_obligations_apply_from": "2027-12-11",
    "required_matrix_items": PART_I_ITEMS,
}

B = {
    "sbom": "Annex I Part II(1); Annex VII pts 2(b), 8 (KB 08-annex1-part2; guide 06-sbom)",
    "prov": "Annex VII pt 2(c); Art 13(14) (KB 10-conformity; guide 11-documentation-set part 7)",
    "kev": "Annex I Part I(2)(a); guidance paras 233-234 (KB 07-annex1-part1)",
    "vex": "Annex I Part II(2); guidance para 218 (guide 06-sbom)",
    "test": "Annex I Part II(3); Annex VII pt 6 (KB 08-annex1-part2; KB 10-conformity)",
    "risk": "Art 13(2)-(4); Annex VII pt 3 (KB 07-annex1-part1)",
    "annex2": "Annex II; Art 13(18) (KB 08-annex1-part2)",
    "support": "Art 13(8); guidance paras 125-128; Annex VII pt 4 (KB 08-annex1-part2)",
    "sm": "Guidance pts 104-112, 108-110, 116 (KB 10-conformity; KB 03-scope)",
    "bundle": "Annex I Part II(2) 'where technically feasible' (guide 07-updates)",
    "route": "Art 32(1)-(4) (KB 10-conformity 'Routes by class'); applies to units placed from 11 Dec 2027 (Art 69(2), Art 71(2); KB 04-exclusions)",
    "doc": "Art 13(12); Art 28; Annex V; FAQ 6.8 (KB 10-conformity)",
    "ret": "Art 13(13) (KB 10-conformity)",
    "place": "Guidance paras 13-14 (KB 03-scope)",
    "sig": "Annex VII pt 2(c); Art 13(14); integrity of the technical file (guide 05-sdlc 'sign evidence'); "
           "SLSA v1.0 'Verifying artifacts' step 1",
    "slsa": "SLSA v1.0 Build track levels and 'Verifying artifacts' steps 1-2 (design control, not a legal "
            "requirement)",
    "vexsig": "Annex I Part II(2); guidance para 218 (guide 06-sbom): VEX is self-issued, so its origin must be "
              "provable",
}


class Gate:
    def __init__(self, policy=None):
        p = dict(DEFAULT_POLICY)
        p.update(policy or {})
        self.policy = p
        self.reasons = []

    def add(self, code, severity, message, basis, subject=None):
        r = {"code": code, "severity": severity, "message": message, "basis": basis}
        if subject:
            r["subject"] = subject
        self.reasons.append(r)

    # ---------------------------------------------------------- rules
    def evaluate(self, bundle, now=None):
        rec, ctx = bundle.record, bundle.context
        ev = rec.get("evidence", {})
        self.now = now or _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0)
        self.trust = A.TrustPolicy(self.policy.get("attestation_trust") or {}, self.policy.get("_base_dir"))
        self.product_id = rec["product"]["product_id"]
        for code, msg in ctx.get("errors", []):
            self.add(code, "fail", msg, "Evidence must be machine-readable (guide 05-sdlc)")
        for rel in ctx.get("missing", []):
            self.add("EVIDENCE_FILE_MISSING", "fail", "referenced evidence file not found: %s" % rel,
                     "Annex VII (KB 10-conformity)", rel)
        self._sbom(ev, ctx)
        self._provenance(ev, ctx)
        self._vex_signature(ev, ctx)
        self._vulns(ev, ctx)
        self._tests(rec, ev)
        self._risk(ev, ctx)
        self._support(rec)
        self._substantial(rec)
        self._route(rec)
        self._declaration(rec)
        self._retention(rec)
        return self.result(self.now)

    def result(self, now=None):
        sev = {r["severity"] for r in self.reasons}
        decision = "FAIL" if "fail" in sev else "REVIEW" if "review" in sev else "PASS"
        now = now or _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0)
        return {
            "decision": decision,
            "policy_id": self.policy["policy_id"],
            "evaluated_at": now.isoformat().replace("+00:00", "Z"),
            "reasons": self.reasons,
        }

    def _sbom(self, ev, ctx):
        sbom = ev.get("sbom")
        if not sbom:
            self.add("SBOM_MISSING", "fail", "no SBOM for this version", B["sbom"])
            return
        norm = ctx.get("sbom") or {}
        if not norm.get("top_level_recorded"):
            self.add("SBOM_TOP_LEVEL_NOT_RECORDED", "fail",
                     "SBOM has no dependency relationships from the product root component", B["sbom"])
        missing = ctx.get("sbom_missing_top_level") or []
        if missing:
            self.add("SBOM_MISSING_TOP_LEVEL_DEPENDENCIES", "fail",
                     "direct dependencies in the build graph absent from SBOM: %s" % ", ".join(missing),
                     B["sbom"], ",".join(missing))
        root_sha = (norm.get("root") or {}).get("sha256")
        art = ctx.get("artefact_sha256")
        if root_sha and art and root_sha != art:
            self.add("SBOM_SUBJECT_MISMATCH", "fail",
                     "SBOM root component hash does not match the shipped artefact", B["sbom"])
        elif not root_sha:
            self.add("SBOM_SUBJECT_UNBOUND", "review",
                     "SBOM root component carries no SHA-256; binding to the artefact rests on the attestation only",
                     "Guide 06-sbom 'Generation from the shipped artefact'")
        if sbom.get("contains_vulnerability_data"):
            self.add("SBOM_CONTAINS_VULNERABILITY_DATA", "info",
                     "SBOM embeds vulnerability data; BSI TR-03183-2 (non-binding) says keep it in VEX/CSAF",
                     "Guide 06-sbom 'No vulnerability data in the SBOM'")
        self.add("SBOM_OK", "info", "%s %s, %d components, %d top-level" % (
            sbom["format"], sbom["spec_version"], sbom["component_count"],
            len(sbom["top_level_dependencies"])), B["sbom"])

    def _tcfg(self, key, default):
        return (self.policy.get("attestation_trust") or {}).get(key, default)

    def _provenance(self, ev, ctx):
        prov = ev.get("provenance")
        if not prov:
            self.add("PROVENANCE_MISSING", "fail", "no build provenance attestation", B["prov"])
            return
        att = A.select(ctx.get("provenance_attestations") or [], self.policy["accepted_predicate_types"])
        res = A.verify(att, self.trust, self.product_id, "provenance", self.now)
        required = self._tcfg("require_signed_provenance", True)
        for code, msg in res["problems"]:
            sev = "fail" if (required or code != "UNSIGNED") else "review"
            self.add("PROVENANCE_" + code, sev, msg, B["sig"])
        st = res["statement"]
        level = None
        if st is not None:
            level = self._provenance_claims(prov, st, res, ctx)
        else:
            # Claims in an unverified statement are not evidence of anything.
            prov["subject_digest_match"] = False
        prov["verification"] = A.summary(res, self.trust, level)

    def _provenance_claims(self, prov, st, res, ctx):
        """Every check below reads the VERIFIED statement, not the file on disk."""
        rules = self.trust.rules(self.product_id, "provenance")
        pred = st.get("predicate") or {}
        bdef = pred.get("buildDefinition") or {}
        builder_id = ((pred.get("runDetails") or {}).get("builder") or {}).get("id") or ""
        prov.update({"predicate_type": st.get("predicateType") or "", "builder_id": builder_id,
                     "build_type": bdef.get("buildType") or ""})
        if st.get("predicateType") not in self.policy["accepted_predicate_types"]:
            self.add("PROVENANCE_PREDICATE_UNSUPPORTED", "fail",
                     "predicateType %s not accepted" % st.get("predicateType"), B["prov"])
        alg = A.subject_matches(st, ctx.get("artefact_digests") or {})
        prov["subject_digest_match"] = bool(alg)
        if not alg:
            self.add("PROVENANCE_SUBJECT_MISMATCH", "fail",
                     "no subject in the verified statement matches the artefact's SHA-256 or SHA-512", B["prov"])
        # builder identity: org allow-list, then product narrowing
        allowed = builder_id in self.policy["trusted_builders"]
        if allowed and rules.get("builder_ids"):
            allowed = builder_id in rules["builder_ids"]
        if not allowed:
            self.add("PROVENANCE_UNTRUSTED_BUILDER", "fail",
                     "builder.id %s is not a trusted builder" % builder_id, B["prov"], builder_id)
        # SLSA Build level comes from the trust policy's map of
        # (signer, builder.id) -> level, never from the provenance itself.
        b = self.trust.builder(builder_id) or {}
        level = int(b.get("slsa_build_level", 1)) if allowed else 0
        signer = res["signer"] or {}
        ref = ("key:%s" % signer["key"]) if signer.get("key") else ("identity:%s" % signer.get("identity_rule"))
        if b.get("signers") and ref not in b["signers"]:
            self.add("PROVENANCE_BUILDER_SIGNER_MISMATCH", "fail",
                     "%s is not a signer the trust policy binds to builder %s" % (ref, builder_id), B["slsa"])
            level = min(level, 1)
        need = int(rules.get("min_slsa_build_level", self._tcfg("min_slsa_build_level", 2)))
        if level < need:
            self.add("PROVENANCE_BUILD_LEVEL_INSUFFICIENT", "fail",
                     "SLSA Build L%d (per trust policy) below required L%d" % (level, need), B["slsa"])
        for req in rules.get("required_builder_properties") or []:
            if not b.get(req):
                self.add("PROVENANCE_BUILDER_PROPERTY_MISSING", "fail",
                         "builder %s not attested as %s in the trust policy" % (builder_id, req), B["slsa"])
        # Expectations (SLSA v1.0 verification step 2)
        if rules.get("build_types") and bdef.get("buildType") not in rules["build_types"]:
            self.add("PROVENANCE_BUILD_TYPE_UNEXPECTED", "fail",
                     "buildType %s not expected" % bdef.get("buildType"), B["slsa"])
        exp = rules.get("external_parameters")
        if exp is not None:
            got = bdef.get("externalParameters") or {}
            for path, want in exp.items():
                val = _dotted(got, path)
                if isinstance(want, dict):
                    ok = val is not None and re.fullmatch(want["pattern"], str(val)) is not None
                else:
                    ok = val == want
                if not ok:
                    self.add("PROVENANCE_EXTERNAL_PARAMETERS_UNEXPECTED", "fail",
                             "externalParameters.%s = %r, expected %r" % (path, val, want), B["slsa"])
            known = {p.split(".")[0] for p in exp} | set(rules.get("ignored_external_parameters") or [])
            extra = sorted(set(got) - known)
            if extra:
                self.add("PROVENANCE_EXTERNAL_PARAMETERS_UNEXPECTED", "fail",
                         "unrecognised externalParameters: %s" % ", ".join(extra), B["slsa"])
        if rules.get("identity_binding") == "github_workflow" and res["method"] == "sigstore-keyless":
            wf = (bdef.get("externalParameters") or {}).get("workflow") or {}
            claimed = "%s/%s@%s" % (wf.get("repository"), wf.get("path"), wf.get("ref"))
            if claimed != signer.get("san"):
                self.add("PROVENANCE_IDENTITY_CLAIM_MISMATCH", "fail",
                         "signing identity %s does not match the workflow the provenance claims (%s)" % (
                             signer.get("san"), claimed), B["slsa"])
        self.add("PROVENANCE_VERIFIED", "info", "%s signature verified (%s); builder %s at SLSA Build L%d per "
                 "trust policy %s; subject bound by %s" % (
                     res["method"], signer.get("key") or signer.get("san"), builder_id, level,
                     self.trust.policy_id, alg or "none"), B["sig"])
        return level

    def _vex_signature(self, ev, ctx):
        vs = ev.get("vulnerability_status")
        if not vs:
            return
        required = self._tcfg("require_signed_vex", True)
        atts = ctx.get("vex_attestations") or []
        if not atts:
            self.add("VEX_UNSIGNED", "fail" if required else "review",
                     "VEX has no signed attestation; a self-issued not_affected cannot be attributed", B["vexsig"])
            return
        att = A.select(atts, self.policy["accepted_vex_predicate_types"])
        res = A.verify(att, self.trust, self.product_id, "vex", self.now)
        for code, msg in res["problems"]:
            self.add("VEX_" + code, "fail", msg, B["vexsig"])
        st = res["statement"]
        if st is not None:
            if st.get("predicateType") not in self.policy["accepted_vex_predicate_types"]:
                self.add("VEX_PREDICATE_UNSUPPORTED", "fail", "VEX predicateType %s not accepted" %
                         st.get("predicateType"), B["vexsig"])
            if not A.subject_matches(st, ctx.get("artefact_digests") or {}):
                self.add("VEX_SUBJECT_MISMATCH", "fail",
                         "signed VEX does not name this artefact's digest as its subject", B["vexsig"])
            if _canon(st.get("predicate")) != _canon(ctx.get("vex_document")):
                self.add("VEX_ATTESTATION_MISMATCH", "fail",
                         "the VEX document used by the gate differs from the signed VEX predicate", B["vexsig"])
            else:
                self.add("VEX_VERIFIED", "info", "VEX signature verified (%s)" % (
                    (res["signer"] or {}).get("key") or (res["signer"] or {}).get("san")), B["vexsig"])
        vs["verification"] = A.summary(res, self.trust)

    def _vulns(self, ev, ctx):
        vs = ev.get("vulnerability_status")
        if not vs:
            self.add("VEX_MISSING", "fail", "no VEX document for this version", B["vex"])
        stmts = {}
        for s in (vs or {}).get("statements", []):
            stmts.setdefault(s["vulnerability"], s)
            if s["status"] == "not_affected" and not (s.get("justification") or s.get("impact_statement")):
                self.add("VEX_NOT_AFFECTED_UNJUSTIFIED", "fail",
                         "%s marked not_affected without justification or impact statement" % s["vulnerability"],
                         B["vex"], s["vulnerability"])
        fail_sev = set(self.policy["fail_untriaged_severities"])
        for m in ctx.get("matches", []):
            st = None
            for vid in [m["vulnerability"]] + m.get("aliases", []):
                st = st or stmts.get(vid)
            status = st["status"] if st else None
            subj = "%s in %s" % (m["vulnerability"], m["component"])
            if status in ("not_affected", "fixed"):
                self.add("VULN_RESOLVED_BY_VEX", "info", "%s: VEX %s" % (subj, status), B["vex"], subj)
                continue
            if m["known_exploited"]:
                self.add("KNOWN_EXPLOITED_UNRESOLVED", "fail",
                         "%s is in the known-exploited catalogue and VEX status is %s" % (subj, status or "absent"),
                         B["kev"], subj)
            elif status == "affected" and not (st or {}).get("action_statement"):
                self.add("KNOWN_EXPLOITABLE_VULNERABILITY", "fail",
                         "%s: VEX says affected with no mitigation" % subj, B["kev"], subj)
            elif status == "affected":
                self.add("VULN_AFFECTED_MITIGATED", "review",
                         "%s: affected with documented mitigation; risk owner to accept" % subj, B["kev"], subj)
            elif (m.get("severity") or "") in fail_sev:
                self.add("VULN_UNTRIAGED", "fail", "%s (%s) has no final VEX decision (status %s)" % (
                    subj, m["severity"], status or "absent"), B["kev"], subj)
            else:
                self.add("VULN_UNTRIAGED", "review", "%s (%s) has no final VEX decision (status %s)" % (
                    subj, m.get("severity"), status or "absent"), B["kev"], subj)

    def _tests(self, rec, ev):
        pid = rec["product"]["product_id"]
        prod = self.policy["required_tests"].get("products", {})
        req = prod[pid] if pid in prod else self.policy["required_tests"]["default"]
        req = list(req)
        sm = rec.get("substantial_modification", {})
        if sm.get("decision") in self.policy["pentest_required_on"] or sm.get("change_type") == "first_placing":
            req.append("pentest")
        have = {}
        for t in ev.get("tests", []):
            have.setdefault(t["test_type"], []).append(t)
        for t in sorted(set(req)):
            if t not in have:
                self.add("TEST_EVIDENCE_MISSING", "fail", "required %s evidence absent" % t, B["test"], t)
        if sm.get("decision") == "pending_review" and "pentest" not in have:
            self.add("PENTEST_DUE_IF_SUBSTANTIAL", "review",
                     "penetration test required if the change is confirmed substantial", B["test"])
        for t in ev.get("tests", []):
            s = t["summary"]
            if t["format"] == "SARIF" and s.get(self.policy["sarif_fail_level"], 0) > 0:
                self.add("TEST_FINDINGS_OPEN", "fail", "%s: %d unsuppressed %s-level results" % (
                    t["test_type"], s[self.policy["sarif_fail_level"]], self.policy["sarif_fail_level"]),
                    B["test"], t["test_type"])
            if t["format"] == "summary" and (s.get("critical", 0) or s.get("high", 0)):
                self.add("TEST_FINDINGS_OPEN", "fail", "%s: %d critical, %d high open" % (
                    t["test_type"], s.get("critical", 0), s.get("high", 0)), B["test"], t["test_type"])

    def _risk(self, ev, ctx):
        if not ev.get("risk_assessment"):
            self.add("RISK_ASSESSMENT_MISSING", "fail", "no risk-assessment reference", B["risk"])
        if not ev.get("applicability_matrix"):
            self.add("APPLICABILITY_MATRIX_MISSING", "fail", "no Annex I Part I applicability matrix", B["risk"])
        else:
            rows = {r.get("item"): r for r in ctx.get("matrix_rows") or []}
            absent = [i for i in self.policy["required_matrix_items"] if i not in rows]
            if absent:
                self.add("APPLICABILITY_MATRIX_INCOMPLETE", "fail",
                         "matrix lacks Part I items: %s" % ", ".join(absent), B["risk"])
            unjust = [i for i, r in rows.items() if r.get("applies") is False and not r.get("justification")]
            if unjust:
                self.add("APPLICABILITY_NOT_JUSTIFIED", "fail",
                         "items not applied without justification: %s" % ", ".join(unjust),
                         "Art 13(4) 'clear justification' (KB 07-annex1-part1)")
            if rows.get("1", {}).get("applies") is False:
                self.add("PART_I_POINT_1_NOT_APPLIED", "fail", "Part I point (1) is absolute", B["risk"])
        if not ev.get("annex_ii_user_information"):
            self.add("ANNEX_II_MISSING", "fail", "no Annex II user-information reference", B["annex2"])

    def _support(self, rec):
        sp = rec.get("support_period") or {}
        if not sp.get("end_date"):
            self.add("SUPPORT_PERIOD_MISSING", "fail", "no support-period end date", B["support"])
            return
        yrs = sp.get("years", 0)
        if yrs < self.policy["min_support_years"]:
            if sp.get("justification"):
                self.add("SUPPORT_PERIOD_SHORT_JUSTIFIED", "review",
                         "support period %.2f years (< %d) with justification; product counsel to confirm "
                         "expected use is shorter" % (yrs, self.policy["min_support_years"]), B["support"])
            else:
                self.add("SUPPORT_PERIOD_TOO_SHORT", "fail",
                         "support period %.2f years (< %d) without justification" % (
                             yrs, self.policy["min_support_years"]), B["support"])

    def _substantial(self, rec):
        sm = rec.get("substantial_modification") or {}
        q = sm.get("questions") or {}
        ct, dec = sm.get("change_type"), sm.get("decision")
        yes = [k for k in ("new_threat_vectors", "new_attack_scenarios", "changed_likelihood", "changed_impact")
               if q.get(k) is True]
        unanswered = [k for k in ("new_threat_vectors", "new_attack_scenarios", "changed_likelihood",
                                  "changed_impact") if q.get(k) is None]
        if ct == "first_placing":
            self.add("FIRST_PLACING", "info", "first placing: full conformity assessment applies", B["sm"])
            return
        if unanswered:
            self.add("SM_QUESTIONS_UNANSWERED", "review",
                     "pt 110 questions unanswered: %s" % ", ".join(unanswered), B["sm"])
        human = bool(sm.get("assessed_by"))
        if ct in ("intended_purpose_change", "boundary_or_dependency_change"):
            if not (human and dec == "substantial" and sm.get("conformity_assessment_ref")):
                self.add("SM_PT109_CHANGE", "review",
                         "%s: guidance pt 109 case; treat as likely substantial pending assessment" % ct,
                         B["sm"])
        if yes:
            if dec == "substantial" and human and sm.get("conformity_assessment_ref"):
                self.add("SM_SUBSTANTIAL_ASSESSED", "info",
                         "substantial modification assessed (%s); new placing" % sm["conformity_assessment_ref"],
                         B["sm"])
            else:
                self.add("SM_REVIEW_REQUIRED", "review",
                         "pt 110 answered yes for: %s" % ", ".join(yes), B["sm"])
        if ct in ("functionality", "security_and_functionality") and not yes:
            if human and dec == "not_substantial" and not unanswered:
                self.add("SM_FUNCTIONALITY_ASSESSED", "info",
                         "functionality change assessed not substantial by %s" % sm["assessed_by"], B["sm"])
            else:
                self.add("SM_FUNCTIONALITY_CHANGE", "review",
                         "functionality change without a recorded human pt 110 assessment", B["sm"])
        if ct == "security_and_functionality" and not sm.get("bundling_justification"):
            self.add("SECURITY_BUNDLED_UNJUSTIFIED", "review",
                     "security fix bundled with functionality without recorded justification", B["bundle"])
        if ct == "security_update" and not yes and not unanswered:
            self.add("SM_SECURITY_UPDATE", "info", "security update; pt 108 generally not substantial", B["sm"])
        if dec == "substantial" and placing_event(rec) not in ("substantial_modification_placing", "first_placing"):
            self.add("SM_PLACING_EVENT_MISMATCH", "fail",
                     "substantial modification must be recorded as a new placing (pt 116)", B["sm"])

    def _route(self, rec):
        c = rec.get("classification") or {}
        cls, route = c.get("class"), c.get("conformity_route")
        cited = set(self.policy["harmonised_standards_cited"])
        applied = set(c.get("harmonised_standards_applied_in_full") or [])
        # Before the application date no certificate can be required (and none
        # can exist while no CRA notified body is designated): record the gap
        # as INFO so readiness is tracked without blocking releases.
        placing = (rec.get("placing_on_market") or {}).get("date")
        start = self.policy.get("conformity_obligations_apply_from")
        applies = not (start and placing and parse_date(placing) < parse_date(start))
        sev = "fail" if applies else "info"
        sfx = "" if applies else " (placing %s before %s: readiness finding, not enforced)" % (placing, start)
        code = (lambda c_: c_) if applies else (lambda c_: c_ + "_PRE_APPLICATION")
        if cls == "important_class_i" and route == "module_a" and not (applied & cited):
            self.add(code("ROUTE_NOT_PERMITTED"), sev,
                     "Class I with Module A needs an OJ-cited standard applied in full; none cited in policy" + sfx,
                     B["route"])
        if cls in ("important_class_ii", "critical") and route in ("module_a", "foss_module_a_public_docs"):
            self.add(code("ROUTE_NOT_PERMITTED"), sev, "%s cannot use %s%s" % (cls, route, sfx), B["route"])
        if route in ("module_b_c", "module_h") and not c.get("certificate_ref"):
            self.add(code("NB_CERTIFICATE_MISSING"), sev,
                     "%s route without notified-body certificate or approval reference%s" % (route, sfx), B["route"])

    def _declaration(self, rec):
        d = rec.get("declaration") or {}
        sm = rec.get("substantial_modification") or {}
        if not d.get("declaration_id") or d.get("status") == "pending":
            self.add("DECLARATION_MISSING", "fail", "no EU declaration of conformity linked", B["doc"])
            return
        if d.get("status") == "reused" and sm.get("decision") in ("substantial", "first_placing"):
            self.add("DECLARATION_REUSE_INVALID", "fail",
                     "declaration reused for a new placing after a substantial modification", B["doc"])
        if d.get("status") == "reused" and sm.get("decision") == "pending_review":
            self.add("DECLARATION_DEPENDS_ON_REVIEW", "review",
                     "declaration reuse valid only if the change is confirmed not substantial", B["doc"])

    def _retention(self, rec):
        r = rec.get("retention")
        p = (rec.get("placing_on_market") or {}).get("date")
        e = (rec.get("support_period") or {}).get("end_date")
        if not r or not p or not e:
            self.add("RETENTION_UNDETERMINED", "fail", "retention date cannot be computed", B["ret"])
            return
        need = retain_until(p, e)
        if parse_date(r["retain_until"]) < need:
            self.add("RETENTION_TOO_SHORT", "fail", "retain_until %s earlier than %s" % (
                r["retain_until"], need.isoformat()), B["ret"])
        if r.get("object_lock_mode") not in ("compliance",):
            self.add("RETENTION_NOT_LOCKED", "review",
                     "evidence store not in compliance-mode object lock", "Design control (paper.md)")


def _dotted(obj, path):
    for part in path.split("."):
        if not isinstance(obj, dict) or part not in obj:
            return None
        obj = obj[part]
    return obj


def _canon(obj):
    return json.dumps(obj, sort_keys=True, separators=(",", ":"))


def placing_event(rec):
    return (rec.get("placing_on_market") or {}).get("event")


def evaluate(bundle, policy=None, now=None):
    return Gate(policy).evaluate(bundle, now=now)
