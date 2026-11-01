## Standards and guidance map

No harmonised standard for the [CRA](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) is cited in the Official Journal as of 30 Oct 2026, so no product has Art 27(1) presumption of conformity. The first candidate for citation is prEN 40000-1-3 (vulnerability handling), expected to publish end-2026 to Feb 2027 and to be cited in 2027 at the earliest. EN 40000-1-4, the horizontal standard for Annex I Part I product properties, is due 30 Oct 2027.

Until citation, existing standards such as EN 18031, ETSI EN 303 645 and IEC 62443 are design baselines and Annex VII point 5 evidence. They give no presumption of conformity.

### Table 1: the harmonised-standards programme

Status is as of 30 Oct 2026 from CEN-CENELEC, ETSI and national standards-body records and the trackers named in the Sources section. "Enquiry" and "formal vote" are CEN-CENELEC stages; ETSI runs a Public Enquiry followed by a Vote.

| Deliverable | Scope | Stage on 30 Oct 2026 | Expected publication or citation | Notes |
|---|---|---|---|---|
| EN 40000-1-1 | Vocabulary | Passed formal vote; ratification scheduled 2 Nov 2026 | Publication Nov 2026; no citation expected | Supporting deliverable |
| EN 40000-1-2 | Principles for cyber resilience (Annex I Part I point 1; M/606 item 1) | Passed formal vote; ratification scheduled 2 Nov 2026 | Publication Nov 2026; CEN-CENELEC records "no citation expected" | Process standard; implementation shown by documented outputs |
| prEN 40000-1-3 | Vulnerability handling (Annex I Part II; item 15) | Enquiry closed 15 Feb 2026; sent for pre-formal-vote HAS assessment 3 Aug 2026; formal-vote draft agreed by WG 9 | Publication end-2026 to Feb 2027 ([Vulnir](https://www.vulnir.com/cra/en-40000/), commentary); citation 2027 at the earliest | Built normatively on ISO/IEC 29147 and 30111; only horizontal standard expected to be cited |
| prEN 40000-1-4 | Generic security requirements (Part I points 2(a)-(m); items 2-14) | Drafting | Due 30 Oct 2027 | Clauses 6.1-6.13 mirror 2(a)-(m); built on EN 18031 without its applicability trees |
| TR 40000-1-5 | Threats and security objectives | Discontinued; content folded into EN 40000-1-4 ([DKE list](https://www.dke.de/resource/blob/2435170/a4c8225091ac18023516487e3e55cb23/normungsprojekte-zum-cra-data.pdf)) | Will not publish | One tracker still shows it in vote; treat DKE as current |
| prEN 50765, 50766, 50764 and FPGA/ASIC standard (CLC/TC 47X) | Microprocessors and microcontrollers with security functions; tamper-resistant variants; EUCC-certified smart card platforms; ASICs and FPGAs | Enquiry 24 Jan to 25 Mar 2026 closed for 50765 and 50766; ASIC/FPGA draft entered enquiry 25 Sep 2026 | Vertical deadline 30 Oct 2026, proposed 31 Dec 2026 | Being renumbered EN 40001-3, 40002-3, 40003-3, 40004-3; AVA_VAN.1 (50765) and AVA_VAN.2-3 (50766) profiles |
| prEN 18330, EN 40000-10, EN 40000-11 (CEN/TC 224) | Smartcards and secure elements; identity management and PAM; hardware with security boxes | Enquiry closed | Vertical deadline 30 Oct 2026, proposed 31 Dec 2026 | Identity standard has basic (AVA_VAN.2), substantial (AVA_VAN.3) and high profiles |
| prEN 50770-1-1, -1-2, -2, -3, -4, -5, -6 (CLC/TC 65X) | OT profiles: firewalls, IDS/IPS, network management, network interfaces, VPN, routers and switches, SIEM | Draft or preliminary work item, pending EN IEC 62443-4-2 and -4-1 A11:2026 amendments | "Expected 31 Dec 2026", seen as uncertain ([Blue Panther](https://panther.blue/en/insights/cra-harmonised-standards-status/), commentary) | Laggard track |
| Smart meter gateway (JTC 13 WG 6) | Annex IV category 2 | Under development, no number | None announced | Restricted drafting setting under M/606 Art 2(3) |
| ETSI EN 304 617-627 and 631-636 | 17 verticals covering Annex III Class I items 2-12 and 16-19 and Class II items 1-2 | Public Enquiry opened 13 Aug 2026; windows close mid-Sep to mid-Nov 2026 | Vote and HAS assessment imply 2027 adoption | Common clause spine 5.2-5.15 with Annex A CRA mapping; EN 304 627 enquiry draft does not yet reference EN 40000-1-3 |
| ETSI EN 304 642 | Telecom network functions | Tracked by ETSI | Not verified | Not among the 41 M/606 items |

### The standardisation request and citation

[Commission Implementing Decision C(2025) 618](https://www.ibf-solutions.com/fileadmin/Dateidownloads/standardisation-request-cra.pdf) of 3 Feb 2025 (mandate M/606, mirror copy) requested 41 European standards: 15 horizontal and 26 vertical. Deadlines were 30 Aug 2026 for items 1 and 15, 30 Oct 2026 for items 16-41 and 30 Oct 2027 for items 2-14. CEN, CENELEC and ETSI accepted on 3 Apr 2025 ([CEN-CENELEC](https://www.cencenelec.eu/news-events/news/2025/newsletter/ots-62-cra/)).

A [draft amending decision](https://www.ibf-solutions.com/fileadmin/dateidownloads/cra-standardization-request-amendment.pdf) notified 7 Jul 2026 would move the dates to 30 Oct 2026, 31 Dec 2026 and 30 Oct 2027. Trackers dated 17-26 Oct 2026 report it not adopted, so the original deadlines remain operative and the 2026 ones have passed. Neither set of dates changes when the CRA applies.

Citation follows the Regulation (EU) No 1025/2012 process (CRA Art 27(6)). A draft passes mandatory HAS-consultant assessments at mature-draft and pre-formal-vote stages, carries a Common Checklist and an Annex ZZ mapping clauses to Annex I, then goes to Commission assessment and OJ publication ([CENELEC BOSS](https://boss.cenelec.eu/homegrowndeliverables/en/pages/enforojeu/)). The RED precedent matters: Implementing Decision (EU) 2025/138 cited EN 18031-1, -2 and -3 with restrictions where the HAS consultant found gaps.

Citation decides the conformity route. Under Art 32(2) and guidance paras 148-151, an important Class I product may self-assess only if it applies in full a cited harmonised standard, a common specification or a "substantial" certification scheme that covers all core-functionality risks.

Otherwise Module B+C or H applies (see Conformity assessment and documentation). No Art 27(2) common specification has been adopted or signalled.

The Commission's levers have been the deadline extension and a second standardisation request for products outside Annex III and IV. It told the Expert Group on 11 Jun 2026 that it is drafting that request ([Expert Group minutes](https://ec.europa.eu/transparency/expert-groups-register/core/api/front/document/135392/download)).

### Table 2: certification schemes

| Scheme | Legal basis | Status on 30 Oct 2026 | CRA relevance |
|---|---|---|---|
| EUCC | [Implementing Regulation (EU) 2024/482](https://certification.enisa.europa.eu/browse-topic/EUCC_en), amended by 2024/3144; applicable 27 Feb 2025 | Only adopted EU scheme; 103 valid certificates from 8 certification bodies in the ENISA register; first "substantial" certificate 23 Jul 2025 (DEKRA, GMV GNSS cryptographic module) | Presumption under Art 27(8) only "in so far as" covered; the Art 27(9) delegated act naming EUCC is planned for Q4 2026 and not adopted; AVA_VAN.1-2 map to "substantial", AVA_VAN.3-5 to "high" |
| EUCC gaps per the [ENISA CRA-via-EUCC study](https://certification.enisa.europa.eu/publications/cyber-resilience-act-implementation-eucc-and-its-applicable-technical-elements_en) (26 Feb 2025) | Exploratory analysis, not guidance | CVD policy and free updates fall outside Common Criteria; protection profiles narrower than product scope; remote data processing unaddressed | Expect a gap assessment even with a certificate |
| EUCS (cloud) | Draft candidate scheme since Dec 2020 | Not adopted; deadlocked since 2024; [COM(2026) 502](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A52026PC0502) of 3 Jun 2026 confirms work resumes with the Cybersecurity Act revision | Cannot support CRA presumption; remote data processing cannot be covered this way |
| EU5G | Candidate scheme | Not adopted | None today |
| Cybersecurity Act revision (CSA2) | Commission proposal of 20 Jan 2026 | Proposed, not adopted; one tracker reports trilogue, not verified | Would keep certification voluntary and reform scheme development |

### Table 3: official guidance inventory

| Document | Body | Date or version | Use it for | Link |
|---|---|---|---|---|
| Guidance on the application of the CRA, Communication C(2026) 5252 with annex | European Commission (Art 26) | Approved 27 Jul 2026; formal adoption pending language versions; non-binding | Scope, FOSS, substantial modification, support period, classification, risk assessment, remote data processing, reporting, vulnerability handling | [Annex](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| FAQs on the Cyber Resilience Act | Commission services | v1.0 3 Dec 2025 to v1.4 4 Sep 2026; living document | Worked examples on scope, classification, Annex I, due diligence, support period, reporting, conformity modules | [PDF](https://ec.europa.eu/newsroom/dae/redirection/document/122331) |
| Implementing Regulation (EU) 2025/2392 | Commission (Art 7(4)) | 28 Nov 2025; in force 21 Dec 2025 | Technical descriptions of important and critical product categories | [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32025R2392) |
| Delegated Regulation (EU) 2026/881 | Commission (Art 14(9)) | Adopted 11 Dec 2025; in force 10 May 2026 | Grounds for CSIRTs to delay dissemination of notifications | [EUR-Lex](https://eur-lex.europa.eu/eli/reg_del/2026/881/oj) |
| Delegated Regulation (EU) 2026/339 | Commission | Adopted 16 Feb 2026; in force 19 May 2026 | Repeals the RED cybersecurity delegated act with effect from 11 Dec 2027 | [EUR-Lex](https://eur-lex.europa.eu/eli/reg_del/2026/339/oj/eng) |
| Delegated Regulation (EU) 2025/1535 | Commission (Art 2(5)) | In force 18 Nov 2025 | Excludes L-category vehicles except pedal-assist L1e | [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32025R1535) |
| CRA Expert Group E03967 minutes | Commission expert group | 5th meeting 10-11 Jun 2026 | Primary record of standards, EUCC, SBOM and SRP state of play | [Minutes](https://ec.europa.eu/transparency/expert-groups-register/core/api/front/document/135392/download) |
| JRC-ENISA Requirements Standards Mapping | JRC and ENISA | 4 Apr 2024 | Per-requirement coverage and gaps in existing standards | [PDF](https://www.enisa.europa.eu/sites/default/files/2024-11/Cyber%20Resilience%20Act%20Requirements%20Standards%20Mapping%20-%20final_with_identifiers_0.pdf) |
| CRA implementation via EUCC | ENISA | 26 Feb 2025 | Common Criteria mapping and protection-profile gaps | [Page](https://certification.enisa.europa.eu/publications/cyber-resilience-act-implementation-eucc-and-its-applicable-technical-elements_en) |
| Secure by Design and Default Playbook | ENISA | v1.0, July 2026 | 22 principles with minimum evidence; Annex C indicative Annex I mapping | [PDF](https://www.enisa.europa.eu/sites/default/files/2026-07/ENISA_Secure_By_Design_and_Default_Playbook_v1.pdf) |
| Technical Advisory for Software Bill of Materials | ENISA | v1.10, Oct 2026 | SBOM formats, lifecycle, CI/CD integration, tooling | [PDF](https://www.enisa.europa.eu/sites/default/files/2026-10/ENISA%20Technical%20Advisory%20-%20Software%20Bill%20of%20Materials%20-%20v1.10.pdf) |
| Technical Advisory on Secure Update Mechanisms | ENISA | Draft v0.1 May 2026; consulted to 10 Jul 2026 | Signing, retrieval, verification, anti-rollback, recovery | [Draft PDF](https://www.enisa.europa.eu/sites/default/files/2026-05/Draft%20-%20ENISA%20Technical%20Advisory%20-%20Update%20Mechanisms%20-%20v0.6.pdf) |
| Technical Advisory on security.txt, CVD policies and advisories (SME Vulnerability Kit) | ENISA | Oct 2026, public consultation draft | security.txt profile, CVD policy and CSAF advisory templates | [PDF](https://www.enisa.europa.eu/sites/default/files/2026-10/Technical%20Advisory%20on%20security.txt%20CVD%20Policies%20and%20Security%20Advisories%20Public%20Consultation.pdf) |
| Technical Advisory for Secure Use of Package Managers | ENISA | Final 10 Mar 2026 | Third-party package selection, integration and monitoring | [Page](https://www.enisa.europa.eu/publications/enisa-technical-advisory-for-secure-use-of-package-managers) |
| Technical Competence Requirements for CRA Notified Bodies | ENISA | 4 Jun 2026 | Auditor and evaluator competences | [Page](https://www.enisa.europa.eu/publications/technical-competence-requirements-for-cra-notified-bodies) |
| Single Reporting Platform hub: FAQ, glossary, user manual, guidance, CSIRT list | ENISA | Live 11 Sep 2026; manual v1.2 21 Oct 2026 | Art 14 filing mechanics and field definitions | [Hub](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp) |
| TR-03183-1 General Requirements | BSI (Germany) | v1.0.0, PDF dated 31 Jul 2026, announced 5 Aug 2026; living document | Risk-assessment method, control selection, assessment-report skeleton | [PDF](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-1_v1_0_0.pdf?__blob=publicationFile&v=3) |
| TR-03183-2 SBOM | BSI | v2.1.0, 20 Aug 2025 | SBOM formats, fields and depth | [PDF](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-2_v2_1_0.pdf?__blob=publicationFile&v=6) |
| TR-03183-3 Vulnerability Reports and Notifications | BSI | v1.0.0, 20 Aug 2025 | Receiving vulnerability reports: security.txt, PSIRT, CVD policy | [PDF](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-3_v1_0_0.pdf?__blob=publicationFile&v=4) |
| TR-03183-H Module H | BSI | v1.1.0, 30 May 2026 | Module H through an ISO/IEC 27001 ISMS | [PDF](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-H_v1_1_0.pdf?__blob=publicationFile&v=3) |
| Gids Cyber Resilience Act v2.0 | RDI and NCSC-NL (Netherlands) | Sep 2025; English Oct 2025 | Scope test, obligations per role, Annex VII contents | [PDF](https://www.digitaltrustcenter.nl/sites/default/files/2025-10/CRA%20Gids%20v2.0%20september%202025%20UK.pdf) |
| National CRA Guidelines v1 | NCSC Ireland | 31 Aug 2026, released 11 Sep 2026 | Reporting thresholds and SRP use; one researcher could not fetch it | [PDF](https://www.ncsc.gov.ie/pdfs/National_CRA_Guidelines_v1.pdf) |

All BSI parts are non-binding and give no presumption of conformity. The Commission told the Expert Group that FAQ and guidance "have equal authoritative value" and that CRA-AI Act and CRA-DORA interplay guidance is targeted for end-2026.

### Table 4: existing standards against the CRA

Rows marked "official" rest on the JRC-ENISA mapping, ETSI TR 103 990 or the ENISA EUCC study. Rows marked "assessment" are the researchers' reading of the standard against the CRA text; no EU mapping was found for them.

| Standard | What it covers | Gaps against the CRA | Use it for | Basis |
|---|---|---|---|---|
| IEC 62443-4-1:2018 | Secure product development lifecycle for IACS components | IACS scope; no hashes, verification or code-signing certificates; free updates not explicit; not expected to be cited | Process evidence for Part I point 1 and Part II points 2, 4, 7, 8 | Official |
| IEC 62443-4-2:2019 | Technical component requirements, SL 1-4 | IACS scope; A11:2026 amendment pending; CRA vehicle will be prEN 50770 profiles | Deepest control catalogue for 2(d), (e), (f), (h), (j), (l) | Official |
| ETSI EN 303 645 V3.1.3 (Sep 2024) | Consumer IoT baseline, provisions 5.1-5.13 and clause 6 | "Very high level"; 37 of 68 provisions are "should"; no explicit security logging; no deletion detail; no CRA citation | Consumer product baseline; TS 103 701 test scheme | Official |
| EN 18031-1, -2, -3:2024 | RED Art 3(3)(d)-(f) radio equipment; mechanism families ACM, AUM, SUM, SSM, SCM, RLM, NMM, TCM, CCK, GEC, CRY | Cited only under RED with restrictions; secure defaults and integrity partly covered; no CRA presumption; RED act repealed from 11 Dec 2027 | Control vocabulary reused by EN 40000-1-4; reusable test evidence | Official (RED citation) and assessment |
| ISO/IEC 27001 and 27002:2022 | ISMS and controls | Organisational, not product-level; covers 6 of 13 Part I items; no SBOM or reporting timelines | Governance; Module H via BSI TR-03183-H; third-party service assurance (guidance para 207) | Official |
| ISO/IEC 27034 | Application security | No vulnerability handling detail; no testing cadence | Part II point 3 and 2(k) process framing | Official |
| ISO/IEC 29147:2018 | Vulnerability disclosure | Covers 4 of 8 Part II items; no third-party component sharing; no timelines or formats | CVD policy and advisory process; normative base of prEN 40000-1-3 | Official |
| ISO/IEC 30111:2019 | Vulnerability handling processes | Covers 5 of 8 Part II items; no free updates or notification methods; no SBOM | PSIRT process; normative base of prEN 40000-1-3 | Official |
| ISO/IEC 18974:2023 and 5230:2020 (OpenChain) | Open-source security assurance and licence compliance programmes | Programme-level; no product controls or SBOM format | Art 13(5) due diligence on open-source components; steward governance | Assessment |
| NIST SP 800-218 SSDF v1.1 | Secure software development practices | Not EU-recognised; no SBOM minimum content; no reporting | Process evidence for Part I point 1 and Part II points 2-3 | Assessment |
| NIST IR 8259 Rev 1 with 8259A/B | IoT manufacturer activities and device capability baseline | US framework; original withdrawn 20 Apr 2026 | Capability vocabulary comparable to 2(b)-(f), (j), (l) | Assessment |
| UL 2900-1 | Network-connectable product software security, private scheme | Not in EU mappings; no CRA presumption | Test and documentation evidence | Assessment |
| IEC 81001-5-1:2022 | Health software security lifecycle | MDR and IVDR devices are CRA-excluded; relevant only to in-scope health software | Lifecycle evidence for wellness and fitness software | Assessment |
| OWASP ASVS 5.0 and ISVS 1.0 | Web and IoT verification requirements | Community standards; ISVS Appendix B maps every Part I item except 2(i) | Requirement-level crosswalk for web, API and IoT verification | Assessment |

The JRC-ENISA conclusion stands: "there is not a single standard capable of covering all the requirements". Coverage is thinnest for Part II (SBOM, free and timely updates, third-party information sharing, testing cadence), hardware-level measures and generic products. No listed standard covers support-period determination, SRP reporting, Annex VII or Annex II; those come from the Regulation, the guidance and the FAQ alone.
