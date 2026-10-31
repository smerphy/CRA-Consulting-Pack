## 6. Supplier and open-source supply chain

Every component a product ships, bought or open source, is the manufacturer's responsibility, and Art 13(5) requires due diligence on all of them. The duty expressly includes free and open-source software never placed on the market. Integrating a component never transfers its compliance to the project or supplier (guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) paras 86-88).

This section covers contract clauses, the supplier questionnaire, the component intake gate and the Art 13(6) upstream channel. It then covers the consumption policy and stewardship decisions for open source the organisation publishes. The legal analysis of who is a steward or manufacturer is in the knowledge base, Open-source software.

### Supplier contract clauses

Procurement is accountable for these clauses (Section 2 RACI). Add them to master agreements for any supplier of software, firmware, hardware with firmware, SaaS integrated into a product, or development services.

| Clause | What it must say | Why |
|---|---|---|
| Vulnerability notification | Supplier notifies the manufacturer of vulnerabilities in supplied components without undue delay, through a named channel, with affected versions and available fixes | Mirrors the Art 19(5) and 20(4) duties on importers and distributors; feeds the Art 14 awareness test |
| SBOM delivery | A machine-readable SBOM per delivered release in CycloneDX 1.6 or later or SPDX 3.0.1 or later, with the [BSI TR-03183-2 v2.1.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-2_v2_1_0.pdf?__blob=publicationFile&v=6) fields and declared known unknowns | Annex I Part II(1); the manufacturer's SBOM depth depends on supplier SBOMs; BSI allows referencing compliant component SBOMs |
| Support-period commitment | Declared support period per component version; notice before end of support; security updates for the period | Art 13(8) lets the manufacturer consider third-party core component support periods; an unsupported component must be replaced or patched by the manufacturer (FAQ Section 4) |
| Disclosure coordination | Embargo handling, joint advisory timing, CVE or EUVD assignment, and who speaks to users | Annex I Part II(4); Art 14(8); avoids a supplier advisory starting the manufacturer's clock unseen |
| Right to request evidence | Access to the supplier's DoC, technical documentation extracts, test reports and risk assessment on request, and on an authority's reasoned request | Art 13(5) due diligence evidence; Art 13(22) reasoned requests reach the manufacturer, not the supplier |
| End-of-life notice | Minimum notice before a component is withdrawn, with a last-time-buy or migration path | Art 13(8); Art 13(19) end-of-support promises to users depend on it |
| Cooperation with authorities | Supplier cooperates with the manufacturer's responses to market surveillance and notified bodies | Art 13(22); Annex VIII Module B pt 8 periodic audits |
| Traceability | Supplier identifies itself and its own suppliers of the component as required | Art 23 ten-year records |
| Fix sharing and licence | For open-source components supplied commercially, the supplier accepts upstream fix sharing in licence-compatible form | Art 13(6) |
| Cessation | Supplier notifies the manufacturer before ceasing operations and escrows or transfers what is needed to keep updating | Art 13(23) applies to the manufacturer, who must be able to keep its own promise |

Clauses are not a substitute for diligence. Where a supplier refuses them, the component enters the intake gate as high risk with a documented exit plan (Section 2 escalation paths).

### Supplier questionnaire outline

The [VDMA](https://vdma.eu/en/cyber-resilience-act) supplier self-disclosure guideline (Jan 2026, trade association) is a usable model; VDMA also warns against over-engineering component testing. Adapt it to the following outline.

1. Identity and role: legal entity, EU establishment, whether the component is itself a CRA product and under which class.
2. Conformity: DoC and CE marking status, standards applied, notified body if any, Art 32(5) public documentation for open-source products.
3. Vulnerability handling: CVD policy URL, security.txt, PSIRT contact, acknowledgement and remediation targets, advisory format (CSAF preferred).
4. SBOM: format, version, depth, known unknowns, delivery mechanism per release.
5. Support: declared support period per version, update mechanism, end-of-life notice period.
6. Secure development: SDLC framework (IEC 62443-4-1, NIST SSDF, OWASP SAMM), testing cadence, signing and provenance practice.
7. Incident and reporting posture: how the supplier will notify the manufacturer of actively exploited vulnerabilities and severe incidents affecting the component.
8. Evidence available on request: risk assessment extracts, test reports, certifications with scope statements.

Score the answers against the component's risk, not against a fixed pass mark. Recital 34 says the level of diligence depends on the nature and level of cybersecurity risk of the component.

### Component intake gate for open source

The gate records a decision for every new component and every major version. It satisfies Art 13(5) and the due-diligence actions in Commission [FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307). Those actions are composition analysis, sandboxing critical components, reviewing the component's SBOM and support period, assessing the maintainer's posture, and testing where risk warrants.

| Gate question | Evidence recorded | Source |
|---|---|---|
| What does the product need from this component? | Functional and security need, trust boundary, data handled | Guidance paras 167-173: define the need, then verify |
| Is it maintained and released regularly? | Last release date, release cadence, responsiveness to issues, number of active maintainers | Recital 34 security-update history |
| What is its security posture? | OpenSSF Scorecard result, Best Practices Badge, SECURITY.md, published CVD channel | OpenSSF guidance; LF Stewards Playbook |
| What is the licence and is it compatible? | SPDX licence identifier, obligations, compatibility with fix sharing | Art 13(6) licence-compatible fixes |
| Any known vulnerabilities? | EUVD, NVD and OSV check at intake and continuously after | Recital 34; FAQ |
| Does it have a steward or a commercial vendor? | Steward determination from the project, vendor contract status | Guidance paras 69-78; Art 25 attestations once they exist |
| Does the SBOM depth reach it? | Whether it will appear in the release SBOM, with its own dependencies | Annex I Part II(1); TR-03183-2 depth rule |
| Fork and exit plan | What the organisation does if the maintainer disappears or the licence changes | Section below |
| Decision | Approved, approved with conditions, rejected; owner and date | Art 13(7) systematic documentation |

Run the gate in the engineering workflow, not in procurement. A pull request that adds a dependency is the natural trigger. The gate record becomes part of the release-gate evidence (knowledge base, Engineering compliance programme).

### The Art 13(6) upstream duty as an organisational channel

Art 13(6) requires the manufacturer to report a component vulnerability to the maintainer and to share any fix it develops, machine-readable where appropriate. Guidance Section 9.2.1 (paras 222-229) sets the practical rules, and ENISA's [SME Vulnerability Kit](https://www.enisa.europa.eu/sites/default/files/2026-10/Technical%20Advisory%20on%20security.txt%20CVD%20Policies%20and%20Security%20Advisories%20Public%20Consultation.pdf) lists failing to report upstream among its common mistakes.

| Rule | Organisational consequence |
|---|---|
| Report only for the integrated version, through the maintainer's CVD channel | PSIRT or the OSPO owns upstream reporting; engineers do not file ad hoc issues |
| No duty where the maintainer is demonstrably already aware; check databases, advisories and issue trackers first | Triage includes a duplicate check and records it |
| Report vulnerabilities in the component itself, not integration-caused ones, though the latter is encouraged | Case file distinguishes component from integration defects |
| No duty where the component has no maintainer or the manufacturer no longer relies on the maintainer | The fork and exit plan takes over; inform the community where possible |
| Share fixes machine-readable, verifiable and licence-compatible, following maintainer guidelines | Legal pre-clears outbound contribution under the organisation's open-source contribution policy |
| No obligation that the fix be accepted or merged, and no obligation to accept the maintainer's fix | Keep the local patch under version control with its rationale |

The duty applies from 11 Dec 2027, but a component vulnerability that is actively exploited in the product is reportable under Art 14 today. The PSIRT case file should therefore carry both the upstream report and the Art 14 decision.

### Consumption policy

The policy says where code may come from and how it is pinned, verified and kept. It applies to developers, build systems and container images alike.

- Approved sources: named registries and mirrors only; direct downloads from arbitrary URLs are blocked in CI.
- Pinning: exact versions or commit hashes, including for CI actions and plugins. The March 2026 compromise of a scanner's GitHub Actions is the cautionary example ([CRA Decoded](https://cra-decoded.com/blog/posts/005_cra_sbom_pipeline/), vendor-adjacent).
- Provenance: signed packages and attestations where available; SLSA-style build provenance for the organisation's own artefacts (OpenSSF guidance).
- Package-manager hygiene per ENISA's Technical Advisory for Secure Use of Package Managers (10 Mar 2026): package selection, integration, monitoring and dependency-vulnerability handling.
- Lock files committed and reviewed; dependency updates arrive as reviewed changes, not silent resolution.
- Private forks are a cost centre: LF's 2025 Open Source ROI survey (n=236), cited in its 2026 CRA report, puts the average at 86 forks and about 60 labour hours each per release. Fork only with an owner and a re-sync plan.
- Binary SCA on the shipped artefact, not only the manifest, because manifest-derived SBOMs miss embedded components ([Finite State](https://finitestate.io/blog/cra-compliance-mistakes), vendor).

### Stewardship decisions for open source the organisation publishes

Each published project gets a written determination, owned by legal with the OSPO (Section 2 RACI). The tests are in the knowledge base, Open-source software; the organisational rule is simple.

| Situation | Role | What the organisation must do |
|---|---|---|
| Unmonetised project the organisation sustains, including code it also uses in its own products | Steward for the project (guidance paras 67-68, 75-78; Ex 25, 29) | Adopt an Art 24(1) policy for the project; cooperate with authorities (Art 24(2)); report under Art 24(3) to the extent of involvement; from 11 Dec 2027 |
| Monetised project: paid binaries, paid updates, paid access to a supported version, donations that gate access | Manufacturer (guidance paras 51-57, 62) | Full CRA for the monetised edition; Art 32(5) lets an Annex III product self-assess if the Annex VII documentation is public |
| Open core | Manufacturer for the paid edition; steward for the community edition (paras 52-53) | Two determinations, two obligation sets; the register (Section 4) holds both |
| Contributions to projects the organisation does not control | Neither (Recital 18; paras 48-49, 85-86) | Contribution policy only; no CRA record needed beyond the intake gate |

The OSPO's role is to maintain the project registry, run the Art 24(1) policies as living documents and own the upstream channel. The OSPO is never itself the regulated entity; the legal person is, project by project (knowledge base, Open-source software).

### What an Art 24(1) policy must contain

Art 24(1) requires a documented, verifiable cybersecurity policy that fosters secure development and effective vulnerability handling by the project's developers. The [ORC WG steward white paper V1.0](https://orcwg.org/files/cra/resources/white-paper-on-open-source-software-stewards-and-cra.pdf) (Jan 2026, "not legal guidance") and the [LF Stewards Playbook](https://policy.openssf.org/CRA/stewards-playbook.html) are the references. The ORC WG's formal steward policy specification (D4.4) is not shipped.

- Scope: the project and versions covered, and the type of support the steward provides, since obligations scale with it (guidance paras 79-82).
- Secure development expectations for contributors, with the OSPS Baseline as a control reference (41 requirements, three levels).
- Vulnerability handling: triage, prioritisation and remediation, and a channel for manufacturers to report (Art 24(1)).
- Information sharing with the community and with upstream and dependency maintainers (Art 24(1)).
- Promotion of voluntary reporting under Art 15 (Art 24(1)).
- Evidence kept in version-controlled files: SECURITY.md, advisories, CVE or EUVD entries (ORC WG white paper).
- Reporting arrangements for actively exploited vulnerabilities and severe incidents where engineering or infrastructure support is provided, including the SRP (Art 24(3)).
- User notification, preferably machine-readable such as CSAF (ORC WG white paper).
- The steward's contact and the legal entity that holds the role (LF One Pager).

### When a maintainer disappears

1. Note that an unmaintained component removes the Art 13(6) upstream duty but not the duty to remediate (guidance paras 222-229; FAQ Section 4).
2. Decide between switching the component, disabling the function and patching autonomously; the FAQ names all three as remediation "via other means".
3. If patching, fork under a named owner, record the patch and rationale, and keep sharing fixes with the community where possible.
4. Update the SBOM to show the fork and its pedigree, and the risk assessment to show the new dependency.
5. Consider becoming the steward if the organisation will sustain the fork. Nobody can be forced into the role; a manufacturer may fork instead ([FSFE](https://fsfe.org/news/2026/news-20260224-01.html), FOSDEM 2026 Q&A).
6. Reopen the intake gate record and the register row (Section 4).

### Supply chain checklist

- [ ] Master agreements carry the ten clauses, or a documented exception per supplier
- [ ] Supplier questionnaire issued to every supplier of in-scope components; answers scored by component risk
- [ ] Intake gate wired to the dependency-change workflow, with records in the system of record
- [ ] Upstream reporting channel owned by PSIRT or the OSPO, with legal pre-clearance of fix sharing
- [ ] Consumption policy enforced in CI: approved sources, pinning, provenance checks, binary SCA
- [ ] Steward or manufacturer determination on file for every published project
- [ ] Art 24(1) policy published for every stewarded project before 11 Dec 2027
- [ ] Fork and exit plan recorded for every component rated high risk
