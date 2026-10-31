## 9. Training and enablement

Training turns the policies in Section 3 into behaviour, and the survey evidence says most organisations have not started. Bitkom found 29% of German companies know what the CRA means for them (Apr-Jun 2026, 1,003 companies, survey). The Linux Foundation found 56% of CRA-aware respondents unaware of penalties and only 34% identifying 2027 as the compliance year ([LF 2026](https://www.linuxfoundation.org/hubfs/Research%20Reports/lfr_2026_cra_awareness_report_060826.pdf?hsLang=en), 404 CRA-aware respondents of 843 surveyed, survey).

The ENISA SME survey found templates to be the single most requested support, at 73% of respondents (Jun 2026, 194 responses, not representative). This section therefore pairs role-based training with the enablement assets each role needs to act. Module H assessors also look for competence and training records (Annex VIII pt 3.2(g)).

### Role by content

| Role | Must know | Must be able to do | Depth and cadence |
|---|---|---|---|
| Executives and board | The obligations in Arts 13-14; fine tiers in Art 64 (EUR 15m or 2.5%; EUR 10m or 2%; EUR 5m or 1%); the decision rights in Section 2; that cost cannot justify unaddressed product risk (guidance paras 156-163); the 11 Sep 2026 and 11 Dec 2027 dates | Sign or delegate the DoC on evidence; hear a residual-risk appeal; read the Section 11 KPIs | 90 minutes at programme start; annual refresh; briefing on each guidance version change |
| Engineering leads and developers | Annex I Part I patterns for (2)(a)-(m); the applicability matrix; SBOM generation and quality; secure update design; the release gate; the substantial-modification test; Art 13(5)-(6) component duties | Threat-model a product; justify a non-applicable item; produce a release-gate record; file an upstream report | Half-day at onboarding; per-release refresher through the gate checklist; annual update |
| PSIRT | Awareness criteria (guidance para 213; FAQ 5.2, 5.4); the SRP, its roles and limits; the 24-hour, 72-hour and final-report content; CVD policy and disclosure timelines; VEX and CSAF; the multi-regime cell | Declare awareness; file an early warning on a weekend; write a "not reportable" decision; publish an advisory | Full day at appointment; two drills a year; monthly case review |
| Product management | Support-period determination and the five-year floor (Art 13(8)); Annex II content; end-of-support display and notification (Art 13(19)); the scope register fields; the per-version rule for software | Set and document a support period; draft Annex II information; raise a register change | Half-day; refresh at each guidance change on Section 5 of the guidance |
| Procurement and legal | The Section 6 contract clauses; roles under Arts 18-22 and when a reseller becomes manufacturer; FOSS determinations and the steward test (guidance paras 40-88); Art 13(22) requests and Art 64(4) exposure; PLD disclosure from 9 Dec 2026 | Negotiate the clauses; write a steward determination; review a 72-hour report; answer an authority | Half-day; refresh at each guidance or case-law change |
| Support and sales | What the CRA promises customers: support period, security updates, where the DoC, Annex II information and CVD policy are published; what to say during an incident; where SBOM access sits if the organisation offers it (Annex II point 9) | Answer a customer's CRA questionnaire from the published material; route a vulnerability report to PSIRT within the hour; use the incident script | Two hours; refresh with each incident template change |
| Internal audit and compliance sampling | The three lines of assurance (Section 5); what a complete Annex VII file looks like; retention rules; the reasoned-request procedure | Sample a technical file; test the system of record; report to the programme board | Half-day; annual |

Support and sales deserve more attention than they usually get. Customers under NIS2 and DORA will ask for the DoC, SBOM access, support period and CVD policy as supply-chain evidence. See the knowledge base, Interplay with other law, the Digital Omnibus and the UK position.

A sales team that improvises answers creates exposure under Art 64(4) if those answers reach an authority.

### Enablement assets to produce

| Asset | For whom | Built from | Owner |
|---|---|---|---|
| PSIRT runbook with awareness criteria, deputy chain, SRP steps and templates for the three report stages | PSIRT, on-call | ENISA SRP glossary and AR manual v1.2; [BSI TR-03183-3](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-3_v1_0_0.pdf?__blob=publicationFile&v=4); Section 7 | PSIRT lead |
| Risk assessment and applicability matrix template with worked justifications | Engineering, product security | [BSI TR-03183-1](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-1_v1_0_0.pdf?__blob=publicationFile&v=3) Sections 4.8, 5-6 and Annex C network-camera example; [ENISA Playbook v1.0](https://www.enisa.europa.eu/sites/default/files/2026-07/ENISA_Secure_By_Design_and_Default_Playbook_v1.pdf) Section 2.3 | Product security officer |
| Release-gate checklist and record template | Release managers | Knowledge base, Engineering compliance programme; OpenChain CRA checklist (community draft) | Product security officer |
| SBOM pipeline template and quality checks | Build engineering | [ENISA SBOM advisory v1.10](https://www.enisa.europa.eu/sites/default/files/2026-10/ENISA%20Technical%20Advisory%20-%20Software%20Bill%20of%20Materials%20-%20v1.10.pdf) Section 4.1; [BSI TR-03183-2](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-2_v2_1_0.pdf?__blob=publicationFile&v=6) fields | SBOM owner |
| CVD policy, security.txt and advisory templates | PSIRT, web team | ENISA [SME Vulnerability Kit](https://www.enisa.europa.eu/sites/default/files/2026-10/Technical%20Advisory%20on%20security.txt%20CVD%20Policies%20and%20Security%20Advisories%20Public%20Consultation.pdf) (Oct 2026, consultation draft); TR-03183-3 Section 4.4 | PSIRT lead |
| Support-period determination template and end-of-support notice | Product management | Guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) Section 5; Annex II point 7 | Product management |
| Annex II information template | Technical writing | Annex II points 1-9; knowledge base, Annex I Part II: vulnerability handling and lifecycle duties | Technical writing lead |
| Scope and classification decision-record template | Compliance, product | Section 4; guidance Sections 2, 6 and 8; [Implementing Regulation (EU) 2025/2392](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32025R2392) | Compliance lead |
| Supplier clause pack and questionnaire | Procurement | Section 6; [VDMA](https://vdma.eu/en/cyber-resilience-act) self-disclosure guideline (trade association) | Procurement |
| Steward determination memo and Art 24(1) policy template | Legal, OSPO | [ORC WG white paper V1.0](https://orcwg.org/files/cra/resources/white-paper-on-open-source-software-stewards-and-cra.pdf); [LF Stewards Playbook](https://policy.openssf.org/CRA/stewards-playbook.html) | Legal |
| Customer-facing CRA fact sheet and incident script | Support, sales | Published DoC, Annex II, CVD policy, support-period table; Section 7 communication rules | Product management with legal |
| Worked examples: one default product, one Class I product, one software-only product, one legacy product | All | The representative products from the first wave (Section 11) | Compliance lead |
| Executive briefing deck and quarterly dashboard | Executives, board | Sections 2 and 11 | Compliance lead |

Produce the worked examples from the first wave's real products, not hypotheticals. Consultancy practice recommends piloting the record set on one representative product before scaling ([SCHUTZWERK](https://www.schutzwerk.com/en/blog/cra-guidance-2026/), vendor), and the same pilot yields the training material.

### Reference material to build from

| Source | Status on 30 Oct 2026 | Best used for |
|---|---|---|
| ENISA Secure by Design and Default Playbook v1.0 (Jul 2026) | Published; 22 principle playbooks with "minimum evidence" per principle; Annex B reproduces Annex I; Annex C indicative mapping | Developer training on Annex I patterns; threat-modelling method for small teams |
| BSI TR-03183-1 v1.0.0 (31 Jul 2026, living document) | Non-binding; OSCAL controls on request from BSI | Risk-assessment method; the Annex C worked example as a classroom case |
| BSI TR-03183-2 v2.1.0 (20 Aug 2025) | Non-binding | SBOM field and depth training for build engineers |
| BSI TR-03183-3 v1.0.0 (20 Aug 2025) | Non-binding | PSIRT set-up: security.txt, mailboxes, CVD policy content, response targets |
| BSI TR-03183-H v1.1.0 (30 May 2026) | Non-binding | Module H and ISMS extension for quality and compliance staff |
| ENISA SRP FAQ (31 items), glossary, AR user manual v1.2 (21 Oct 2026), factsheet in 10 languages | Live | PSIRT and Assigned Representative training; the factsheet for non-specialists |
| ENISA SME Vulnerability Kit (Oct 2026) | Consultation draft | CVD policy and advisory templates; the "common mistakes" table as a teaching aid |
| ENISA SBOM advisory v1.10 (Oct 2026) and package-manager advisory (10 Mar 2026) | Published, non-mandatory | Pipeline and consumption-policy training |
| ENISA update mechanisms advisory v0.1 (May 2026) | Draft | Secure update design; label as draft |
| ORC Learning Hub | Live; two introductory courses | Open-source-focused CRA training for OSPO and maintainers |
| OpenSSF guides: Stewards Playbook, One Pager, maintainer readiness guide, manufacturer checklist, OSPS Baseline | Living documents | Steward and OSPO enablement; component selection criteria |
| Commission FAQ v1.4 and guidance C(2026) 5252 | Non-binding; guidance formally a draft pending language versions | Legal and product-management training on scope, support period, substantial modification and awareness |
| Knowledge base sections and the Requirement checklists tab | Internal | The per-item questions every role trains against |

Label every training asset with the source version it rests on. When the FAQ or guidance changes, or when EN 40000-1-3 is cited, the quarterly review (Section 2) triggers an update to the affected assets.

### Training checklist

- [ ] Role-by-content matrix adopted and mapped to the organisation's actual roles
- [ ] Executive briefing delivered and minuted, including the residual-risk rule
- [ ] Developer and PSIRT training delivered before the first release-gate run and the first drill
- [ ] Support and sales script and fact sheet issued before any public DoC
- [ ] Thirteen enablement assets produced, each labelled with its source version
- [ ] Worked examples built from the first wave's real products
- [ ] Competence and training records filed in the system of record (Section 8)
