## Engineering compliance programme

A 12 to 14 month programme takes a product portfolio from inventory to a declaration of conformity by 11 Dec 2027. Reporting readiness comes first, because Art 14 of the [CRA](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) has applied since 11 Sep 2026. Class I and Class II products must be assessment-ready early enough to secure a notified-body slot.

No notified body was listed in NANDO as of 8 Sep 2026 and no harmonised standard is cited. The critical path for important products is therefore external capacity, not internal engineering. Everything below rests on the Commission [FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307), guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456), ENISA advisories and [BSI TR-03183](https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Standards-und-Zertifizierung/Technische-Richtlinien/TR-nach-Thema-sortiert/tr03183/tr-03183.html), none of which gives presumption of conformity.

### Gap assessment

Run it on one representative product per family first, then scale. Record the answer to every line with evidence, not a tick.

### Inventory and scope
- [ ] Every product, version, variant, companion app and OEM-branded unit is listed; early adopters report inventories growing five-fold once versions and cloud pieces are counted ([OmniTrust](https://omnitrust.com/blog/eu-cra-tales-from-the-trenches-2-the-first-problem-isnt-security-its-scope/), consultancy)
- [ ] Remote data processing boundary documented per product: which functions need which back-end (guidance Section 8)
- [ ] Economic-operator role fixed per product and market: manufacturer, importer, distributor, authorised representative
- [ ] Legacy products placed before 11 Dec 2027 tagged: Art 14 applies to them, the rest only on substantial modification (Art 69(2)-(3))

### Classification
- [ ] Core functionality tested against Annex III and IV using [Implementing Regulation (EU) 2025/2392](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32025R2392); rationale recorded
- [ ] Conformity route chosen per product: Module A, B+C or H; Class I plans for B+C or H while no standard is cited
- [ ] Classification review trigger set for each release

### Risk assessment
- [ ] Threat model exists per product with a data-flow diagram and asset list (data, functional, security)
- [ ] Each Annex I Part I(2)(a)-(m) item marked applicable or not, with written justification (Art 13(3)-(4))
- [ ] Residual risk judged against "appropriate level of cybersecurity", not cost or appetite (guidance paras 156-163)
- [ ] Update triggers defined: security-relevant release, new vulnerability, new threat (TR-03183-1 RH_UPD.1)

### Annex I Part I controls
- [ ] No known exploitable vulnerabilities at release; EUVD and vendor advisories checked (guidance paras 230-237)
- [ ] Secure defaults, reset to original state, no default credentials, default-deny exposure
- [ ] Security updates separable from feature updates where technically feasible (FAQ Section 4.3)
- [ ] Automatic security updates default-on with opt-out, or the Recital 56 carve-out documented

### Part II processes
- [ ] SBOM generated at build for every release to at least top-level dependencies
- [ ] Vulnerability handling process written down with triage, remediation and advisory steps
- [ ] CVD policy published with RFC 9116 security.txt and an anonymous intake form
- [ ] Support period declared per product and per substantially modified version; at least 5 years unless use time is shorter

### Documentation
- [ ] Annex VII technical file assembled per product version and retrievable in 10 working days
- [ ] Test reports, SBOM, risk assessment and DoC version-linked to the release
- [ ] Retention set to 10 years or the support period, whichever is longer (Art 13(13))

### Reporting
- [ ] Primary and Secondary Assigned Representatives registered on the ENISA SRP with the right coordinating CSIRT
- [ ] Awareness definition, UTC timestamp log and 24-hour escalation path in the PSIRT runbook
- [ ] Two tabletop exercises run: one actively exploited vulnerability, one severe incident

### Supply chain and open source
- [ ] Component intake gate records needs, evidence, EUVD check and maintenance status (Art 13(5))
- [ ] Upstream reporting and fix-sharing channel defined for each major component (Art 13(6))
- [ ] Supplier contracts carry vulnerability-notification, SBOM and disclosure-coordination clauses

### User information
- [ ] Annex II content drafted: intended purpose, security properties, secure configuration, end-of-support month and year, reporting contact, foreseeable misuse
- [ ] End-of-support date shown at purchase; notification mechanism designed (Art 13(19))

### Governance
- [ ] Accountable programme owner named with executive sponsor
- [ ] Standards and guidance tracking log maintained; re-mapping planned for EN 40000-1-3 when cited
- [ ] Evidence lives in a product system of record, not in mailboxes and spreadsheets

### Artefact inventory

| Artefact | CRA basis | Owner | Tooling or template |
|---|---|---|---|
| Product inventory and classification record | Art 3(1); Annexes III-IV; IR 2025/2392; guidance Sections 6, 8 | Product management with compliance lead | GRC register; [OpenChain CRA checklist](https://github.com/OpenChain-Project/CRA-Compliance/blob/main/CRA_Checklist_Requirement_latest.md) Section 2.5 |
| Cybersecurity risk assessment with Annex I applicability matrix | Art 13(2)-(4), (7); Annex VII point 4 | Product security architect | [TR-03183-1 v1.0.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-1_v1_0_0.pdf?__blob=publicationFile&v=3) Sections 5-6; STRIDE; IEC 62443-3-2 |
| Component due-diligence records | Art 13(5); guidance Section 7.3 | Engineering lead or OSPO | SCA; OpenSSF Scorecard; [VDMA](https://vdma.eu/en/cyber-resilience-act) supplier self-disclosure |
| Secure development process description | Annex I Part I(1); Annex VII point 2 | Head of engineering | IEC 62443-4-1, NIST SSDF, OWASP SAMM; TR-03183-H |
| Release security gate record | Annex I Part I(2)(a); Art 3(30); guidance Sections 4.3, 9.2.2 | Release manager | CI attestations per [ENISA Playbook v1.0](https://www.enisa.europa.eu/sites/default/files/2026-07/ENISA_Secure_By_Design_and_Default_Playbook_v1.pdf) Section 5.1 |
| SBOM per release | Annex I Part II(1); Annex VII points 2(b), 8 | SBOM owner (build engineering) | Syft, Trivy, cdxgen, build plugins; sbomqs; cosign; [TR-03183-2 v2.1.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-2_v2_1_0.pdf?__blob=publicationFile&v=6) |
| VEX and CSAF statements and advisories | Annex I Part II(2), (4); guidance para 218 | PSIRT | OpenVEX, CSAF provider, Dependency-Track |
| Security test reports | Annex I Part II(3); Annex VII point 5 | Security testing lead | SAST, DAST, fuzzing in CI; lab penetration tests |
| CVD policy, security.txt, anonymous intake form, PSIRT runbook | Annex I Part II(5)-(6); Art 13(17); Annex VII point 2 | PSIRT lead | [TR-03183-3 v1.0.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-3_v1_0_0.pdf?__blob=publicationFile&v=4); [ENISA SME Vulnerability Kit](https://www.enisa.europa.eu/sites/default/files/2026-10/Technical%20Advisory%20on%20security.txt%20CVD%20Policies%20and%20Security%20Advisories%20Public%20Consultation.pdf) templates |
| Reporting runbook, templates, awareness log, SRP registrations, drill records | Arts 14, 16; Delegated Regulation (EU) 2026/881 | Notification owners (24 h, 72 h, final) | [ENISA SRP](https://www.enisa.europa.eu/topics/product-security/vulnerability-services/eu-incident-response-and-cyber-crisis-management/single-reporting-platform-srp) AR manual v1.2; OpenChain Section 4.5 |
| Upstream reporting and fix-sharing records | Art 13(6); guidance Section 9.2.1 | PSIRT or OSPO | Issue trackers; maintainer CVD channels |
| Secure update mechanism design and evidence | Annex I Part I(2)(c), (f); Part II(2), (7), (8) | Platform or firmware lead | [ENISA update advisory v0.1 draft](https://www.enisa.europa.eu/sites/default/files/2026-05/Draft%20-%20ENISA%20Technical%20Advisory%20-%20Update%20Mechanisms%20-%20v0.6.pdf); TUF, Uptane |
| Support-period policy, version and support register, end-of-support notices | Art 13(8), (10), (19); guidance Section 5 | Product management | Register per version; OpenChain Section 6 |
| Annex II user information | Art 13(18); Annex II | Technical writing with product security | Docs pipeline; public security page |
| Technical documentation (Annex VII file) | Art 31; Annex VII; Art 13(13) | Compliance lead | TR-03183-1 Section 4.8 report structure as skeleton |
| EU declaration of conformity and CE marking placement | Arts 28-30; Annexes V-VI | Legal with compliance lead | FAQ Sections 6.7-6.8; software CE mark on the DoC or website |
| Conformity assessment records | Art 32; Annex VIII | Quality or compliance lead | [TR-03183-H v1.1.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-H_v1_1_0.pdf?__blob=publicationFile&v=3); notified body |
| Standards applicability matrix and tracking log | Art 27 | Compliance lead | CEN-CENELEC and ETSI work programmes; OJ citation watch |
| Traceability records, 10 years up and down the chain | Art 23 | Supply chain operations | ERP and order records |
| FOSS determination memos, steward registry, authorised-representative mandate | Arts 24, 32(5), 18 | Legal | OpenChain Sections 5, 7.4 |

### SDLC changes

1. Threat model before development and a per-product risk assessment stating per-item Annex I applicability; refresh on every substantial change (TR-03183-1 RH_RA.1; Playbook Section 2.3).
2. Secure defaults, factory reset, no default credentials and default-deny network exposure as acceptance criteria.
3. SBOM generation in CI immediately after the build, in CycloneDX 1.6 or later or SPDX 3.0.1 or later, enriched to the TR-03183-2 fields, checked with sbomqs, signed and stored with the release ([ENISA SBOM advisory v1.10](https://www.enisa.europa.eu/sites/default/files/2026-10/ENISA%20Technical%20Advisory%20-%20Software%20Bill%20of%20Materials%20-%20v1.10.pdf)).
4. VEX and CSAF publication for affectedness and advisories; never embed vulnerability data in the SBOM (TR-03183-2 Section 8.1.14).
5. Continuous dependency monitoring in Dependency-Track against NVD, GHSA and OSV, feeding PSIRT triage.
6. Signed updates with role-separated keys and anti-rollback metadata following TUF or Uptane patterns; auto-update default-on with opt-out and recorded outcomes.
7. Security updates released separately from functionality updates, with the Commission's bundling exceptions documented per case.
8. Security testing cadence tied to threat input, not the calendar (guidance paras 238-240), with a release gate recording tests, SBOM hash, exploitability decision and the security-delta assessment.
9. CVD intake and PSIRT built on the [FIRST PSIRT Services Framework v1.1](https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1), with security.txt, functional mailboxes, 5 and 10 working-day response targets and a 90-day disclosure default (TR-03183-3).
10. End-of-support process: per-version dates, purchase-time display, notification and a legacy-version owner.
11. Upstream reporting to component maintainers and fix sharing in licence-compatible, machine-readable form.

### Roadmap

| Phase | When | Outputs | Gate |
|---|---|---|---|
| 0 Reporting readiness | Now; 4-8 weeks, then quarterly drills | SRP Assigned Representatives registered, CSIRT chosen, runbook, templates, awareness log, two tabletop exercises | Early warning can be filed within 24 h on a weekend |
| 1 Inventory, scope and classification | Nov-Dec 2026; 1-2 months | Product register with RDPS boundaries, roles, classes, routes; candidate notified bodies shortlisted | Every product has a class, a route and an owner |
| 2 Risk assessment and gap analysis | Dec 2026-Feb 2027; 4-8 weeks per family | TR-03183-1 style assessment on a representative product; evidence inventory; prioritised gap list | Annex I applicability matrix signed off |
| 3 Remediation and SDLC changes | Jan-Aug 2027; 6-8 months; largest cost | SBOM pipeline, update infrastructure, release gate, PSIRT, support policy, supplier clauses | Pipeline evidence generated automatically for one release |
| 4 Documentation and DoC | Jun-Sep 2027; 2-4 months per family, in parallel | Annex VII files, Annex II information, draft DoC per family | File complete and reviewed by someone outside engineering |
| 5 Conformity assessment | Contract by Q1 2027; engagement Apr-Nov 2027 | Module A record, or Module B certificate and Module C controls, or Module H certificate | Certificate or internal-control record in hand |
| 6 Go-live and operations | 11 Dec 2027 onwards | CE marking, DoC published, PSIRT and monitoring live, standards re-mapping | Declared products only on the market |

Phase 5 is the constraint. Commentators put accreditation plus notification at 12-18 months per body, contracting at 2-4 months and a Module B+C engagement at 3-6 months ([CRA Decoded](https://cra-decoded.com/blog/posts/cra-notified-body-capacity-crisis/), commentary). Brightsight has RvA accreditation pending RDI notification; others say they will apply.

Pre-contract two or three candidates and keep Module A paperwork complete regardless.

### Roles

| Role | Accountable for | Notes |
|---|---|---|
| Executive sponsor | Budget, release-blocking authority, Art 64 exposure | Signs the DoC or delegates it in writing |
| Compliance lead | Classification record, Annex VII file, DoC, standards tracking, notified-body relationship | Owns the system of record |
| Product security officer | Risk assessments, Annex I applicability, release gate, remediation decisions | Chairs the gap assessment |
| PSIRT lead | CVD intake, triage, advisories, Art 14 awareness decision and SRP submissions | Distinct from the infrastructure CSIRT (TR-03183-3); names 24 h, 72 h and final-report owners with deputies |
| SBOM owner | Build-time generation, quality, signing, monitoring feeds | One per release train |
| Engineering leads | Threat models, controls, update mechanism, test evidence, due-diligence records | Per product family |
| Legal | FOSS determinations, steward registry, authorised-representative mandate, supplier terms | Reviews 72 h and final reports, not the 24 h early warning |
| Procurement and supplier management | Contract clauses, supplier SBOMs and attestations, traceability records | Art 23 records for 10 years |

### Effort and cost benchmarks

| Source | Type | Figure |
|---|---|---|
| [ENISA SME CRA survey](https://www.enisa.europa.eu/sites/default/files/2026-06/SME%20CRA%20survey%20report.pdf), Jun 2026, 194 responses | Survey, not representative | Threat modelling used by 24%; SBOMs by 35%; templates requested by 73%; documentation and conformity assessment top challenges |
| [Linux Foundation 2026](https://www.linuxfoundation.org/hubfs/Research%20Reports/lfr_2026_cra_awareness_report_060826.pdf?hsLang=en), 843 respondents | Survey | Manufacturers (module n=194-219 of 843): 32% produce SBOMs for all products; 41% expect compliance by 2027. Cited LF 2025 ROI survey (n=236): forks average 86 with about 60 hours each per release |
| Bitkom, Apr-Jun 2026, 1,003 German companies | Survey | 29% know what the CRA means for them; 67% have heard of it |
| [ONEKEY](https://www.onekey.com/press-release/onkey-iot-ot-cybersecurity-report-2026-half-of-all-companies-have-formed-cra-teams), Sep 2026, 200 German industrial firms | Vendor survey | 61% budgeting; over 60% expect longer development, 28% "significantly longer" |
| [cyberresilienceact.eu calculator](https://www.cyberresilienceact.eu/cra-compliance-cost-calculator/) | Independent model, illustrative | EUR 78,300 one-off and EUR 13,500 a year for three default-class products at medium readiness, EUR 45 per hour |
| Notified-body fees | Vendor estimates, unsourced | Module B EUR 15,000-80,000; first Module H EUR 80,000-150,000; surveillance every 1-2 years |
| KONE-authored industrial study, 2024, 12 companies | Survey | 50% expected cost increases under 20% |

### Pitfalls

- Planning for 11 Dec 2027 while Art 14 has applied to every in-scope product, legacy included, since 11 Sep 2026.
- Undercounting scope: versions, OEM variants, mobile apps and cloud functions multiply the inventory.
- Treating IEC 62443, ISO/IEC 27001 or EN 18031 certification as CRA compliance; ISMS scopes that exclude firmware, build pipelines and update infrastructure.
- Risk accepted on cost or appetite grounds, or without a decision trail.
- SBOMs built from manifests rather than shipped binaries; SBOMs with no owner; vulnerability data inside the SBOM.
- CVE counts or scanner hits treated as risk or as active exploitation, with no reachability or VEX discipline.
- A published CVD policy that nobody staffs, with expired contacts and no check of each report for exploitation.
- Clock errors: awareness postponed pending approval, 24 h and 72 h treated as consecutive, the wrong coordinating CSIRT chosen.
- Security fixes bundled with features when separation was feasible; no security-delta assessment per release.
- Five years treated as the default support period; no per-version declaration for software.
- Evidence scattered across tools, assembled by hand for each request.
- Waiting for notified-body designation or standards citation before building the technical file.

### Using BSI TR-03183 as scaffolding

TR-03183-1 Section 4.8 lists the minimum content of an assessment report, and that list is a usable Annex VII skeleton until EN 40000-1-x is cited. It covers product identification with versions and SBOM, risk assessment with accepted risks, and design documentation naming applicable and non-applicable essential requirements with justification. It closes with the vulnerability-handling description and the user documentation.

TR-03183-H v1.1.0 (30 May 2026) shows how a Module H quality system can be an ISO/IEC 27001 ISMS extended to cover design, development, production and vulnerability handling. It adds CRA refinements to clauses 4.2 to 8.1 and to controls 5.7, 5.8, 8.8, 8.25, 8.29 and 8.32. Its Appendix B warns that Module H still includes review of one technical file per product category.

Both documents are non-binding and give no presumption of conformity; see Standards and guidance map.
