## 5. Secure development lifecycle integration

The CRA is satisfied by evidence a pipeline produces, so add gates to the existing lifecycle rather than a parallel compliance process. Teams already running IEC 62443-4-1, NIST SSDF or OWASP SAMM add rather than replace. The additions are the Annex I applicability matrix, SBOM depth and quality, the per-release security-delta check, declared support periods and the Art 14 clock.

The programme view is in Engineering compliance programme; this section specifies the gates.

### The gates to add

| Gate | Where | What it checks | Record produced |
|---|---|---|---|
| Design review | Before implementation of a feature or product | Threat model updated for the change; applicability matrix rows affected; RDPS boundary unchanged or re-mapped | Design review minute referencing threat identifiers |
| Component intake | On adding or upgrading a dependency | Need statement, maintenance signals, licence, EUVD and OSV history, exit plan (section 9) | Due-diligence record (Art 13(5)) |
| Code review | Every merge | Security-relevant change flagged; secure-coding checklist; no secrets or debug endpoints | Review approval with security label |
| Static and dynamic analysis | Every release candidate | SAST with critical and high findings resolved or risk-accepted; DAST on exposed interfaces; fuzzing of external parsers with memory-error detection | Scan reports attached to the build |
| Dependency and SBOM check | Every build | SBOM generated from the artefact (section 6); quality score; vulnerability match against EUVD, NVD, GHSA and OSV; VEX for non-reachable findings | Signed SBOM, VEX, scan output |
| Release gate | Before tagging a release | Tests complete; SBOM hash recorded; known-exploitable check against EUVD, NVD and the CISA KEV catalogue; secure-default configuration verified; security-delta assessment; substantial-modification decision; documentation delta | Release security gate record |
| Post-release | Continuous | Monitoring feeds, PSIRT triage, risk-assessment update triggers (section 3) | PSIRT case files, assessment versions |

The release security gate record is the single most useful artefact in the file. It ties a shipped artefact to its tests, SBOM, exploitability decision and placing decision. That is what a notified body or market surveillance authority will ask to see first.

### The security-delta assessment

Every release answers whether it is a substantial modification. A substantial modification is a new placing on the market with its own declaration and support period (see Conformity assessment and documentation).

Use the four questions from guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) para 110: new threat vectors, new attack scenarios, changed likelihood, changed impact. Four negative answers mean not substantial.

Security updates that reduce risk and keep the intended purpose are "generally not" substantial (para 108). Features foreseen in the risk assessment are not substantial. Small features adding unassessed risk, such as persistent login tokens or unencrypted log export, can be (paras 103-108, Examples 40-48).

Record the answers, the assessor and the decision on the gate record. Route a positive decision to section 11 for a new declaration and to section 12 for the notified body where one is involved.

### Mapping to existing frameworks

| Framework | What it already covers | What the CRA adds |
|---|---|---|
| IEC 62443-4-1 | Security management, requirements, secure design, implementation, verification, defect management, update management; covers 36 of 42 SSDF tasks fully ([ISAGCA](https://gca.isa.org/blog/new-resource-comparison-of-isa/iec-62443-4-1-and-nist-sp-800-218-secure-software-development-framework)) | Fixed Art 14 clocks, SBOM depth and fields, Annex II user information, declared support periods, separation of security from feature updates |
| NIST SSDF (SP 800-218) | Prepare, protect, produce, respond practices | Post-release practices that 62443-4-1 has and SSDF lacks; the Annex I applicability trail; EU reporting |
| OWASP SAMM | Maturity measurement across governance, design, implementation, verification, operations | Nothing CRA-specific; use it to score the gates above and show improvement over time |
| ISO/IEC 27001 with BSI TR-03183-H | ISMS extended to design, development, production and vulnerability handling; controls 5.7, 5.8, 8.8, 8.25, 8.29, 8.32 refined | The Module H route; see section 12 |

The [ENISA Playbook v1.0](https://www.enisa.europa.eu/sites/default/files/2026-07/ENISA_Secure_By_Design_and_Default_Playbook_v1.pdf) references OWASP SAMM for maturity and gives per-principle release gates and evidence lists that fit the table above. None of these frameworks is cited under the CRA and none gives presumption of conformity.

### Testing cadence: threat-driven, not calendar-driven

Part II point 3 requires "effective and regular tests and reviews". Guidance paras 238-240 read "regular" as reviewing whether new threats or vulnerabilities require the test set to change, then executing.

Repeating an unchanged campaign at fixed intervals is not the obligation. Proportionality to the risk profile is explicit, and a review finding no new input needs no new tests.

"Regular" must still be shown. Keep a test plan per product with a review log: date, inputs reviewed, decision, tests added or re-run, results. Inputs include EUVD and vendor advisories, threat reports and product changes.

Regression tests after every modification remain mandatory in that reading. Quarterly review entries, each citing the intelligence considered, demonstrate regularity without treating calendar repetition as the obligation.

Minimum content of the plan: SAST on every release candidate, fuzzing of every external parser and DAST or API testing on every exposed interface. Add a penetration test on the product and its RDPS before first placing and after any substantial modification, plus re-tests triggered by PSIRT findings.

### Evidence capture in CI

Generate evidence where the work happens and sign it, so the technical file is assembled rather than written. The ENISA Playbook section 5.1 argues machine-processable attestations keep documentation current, while cautioning that a self-issued attestation is not proof of security.

1. Emit SAST, DAST and fuzzing results as SARIF or equivalent and store them with the build identifier.
2. Generate the SBOM at build and attach it as an attestation bound to the artefact digest (section 6).
3. Sign release artefacts and attestations with Sigstore cosign or GitHub artefact attestations. Keep signing keys out of the pipeline runner where an HSM-backed signer exists (section 7).
4. Record the gate decisions as a structured file committed with the release tag.
5. Pin third-party CI actions to commit hashes. One vendor-adjacent guide cites the March 2026 compromise of a popular scanner action as the reason ([CRA Decoded](https://cra-decoded.com/blog/posts/005_cra_sbom_pipeline/), vendor-adjacent).

```yaml
# release-gate job (GitHub Actions excerpt)
- name: Verify SBOM attestation
  run: cosign verify-attestation --type cyclonedx \
       --certificate-identity-regexp '^https://github.com/acme/.*' \
       --certificate-oidc-issuer https://token.actions.githubusercontent.com \
       ghcr.io/acme/thermostat-fw@${{ steps.build.outputs.digest }}
- name: Known-exploitable check
  run: grype sbom:sbom.cdx.json --fail-on high --only-fixed=false \
       && ./kev-check.sh sbom.cdx.json kev.json
- name: Record gate
  run: ./gate-record.sh --sbom-sha512 "$(sha512sum sbom.cdx.json | cut -d' ' -f1)" \
       --delta "$DELTA_DECISION" --out gate-${{ github.ref_name }}.json
```

The gate record travels with the release into the technical file and into the evidence index (section 12).

### Sample release-gate checklist

- [ ] Threat model and applicability matrix reviewed for this release; affected rows updated or confirmed
- [ ] Code review complete with every security-relevant change labelled and approved
- [ ] SAST: no open critical or high finding without a recorded risk acceptance
- [ ] Fuzzing and DAST run on changed parsers and interfaces; no open crash or exploitable finding
- [ ] SBOM generated from the shipped artefact, quality-checked, signed; SHA-512 recorded here
- [ ] Known-exploitable check against EUVD, NVD and KEV complete; every finding fixed, mitigated with a VEX justification, or release-blocked
- [ ] Secure-default configuration export matches the baseline; no default credentials, telemetry off, debug interfaces locked
- [ ] Update package signed with the release key; anti-rollback version incremented; first-use update test passed
- [ ] Security-delta assessment answered on the four guidance questions; substantial-modification decision recorded with assessor
- [ ] Separation check: security fix shipped separately from features, or the bundling exception recorded (FAQ section 4.3)
- [ ] Documentation delta: Annex II text, advisory, release notes and support-period statement updated
- [ ] Declaration decision: existing declaration covers this release, or a new declaration is triggered
- [ ] Gate record signed by the release manager and product security owner

### Legacy designs

Products designed before 11 Dec 2027 but placed after may rely on the Art 13(2) risk assessment and technical documentation to show appropriate security. No redesign and no recreated historical design or test documentation is needed (guidance paras 33-39, Example 12). Conformity assessment, the declaration, the CE marking and Part II process evidence are still required.

For such a product, the gates above apply from the next release onward. Build the applicability matrix against the product as it exists and run the current tests.

State in the file which design-phase evidence is contemporary and which rests on the assessment. Any later substantial modification brings the modified parts under the full set of gates.

The gate records are the evidence for checklists 2, 3 and 4 in the Requirement checklists tab.
