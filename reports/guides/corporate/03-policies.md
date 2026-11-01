## 3. The policy set

Seven policies carry the CRA into the organisation, and two of them are legal requirements rather than good practice. Annex I Part II point 5 requires a coordinated vulnerability disclosure (CVD) policy of every manufacturer. Art 24(1) requires a documented, verifiable cybersecurity policy of every open-source software steward.

The other five are the organisation's way of making the remaining obligations repeatable. Each policy names an owner, maps to articles and annex points, and borrows from a published template where one exists. None of the templates gives presumption of conformity.

### The seven policies

| Policy | Mandatory contents mapped to articles and annex points | Owner | Template or reference |
|---|---|---|---|
| Product cybersecurity (secure by design and default) | Risk assessment per product and version, maintained through the support period (Art 13(2)-(4), (7)); Annex I Part I(1) and per-item applicability for (2)(a)-(m) with justification (Art 13(3)-(4)); release gate and "no known exploitable vulnerabilities" decision (Part I(2)(a)); secure defaults (Part I(2)(b)); remote data processing in scope (Art 3(2)); substantial-modification test per release (Art 3(30); guidance paras 104-124) | Product security officer | [BSI TR-03183-1 v1.0.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-1_v1_0_0.pdf?__blob=publicationFile&v=3) Sections 5-6; [ENISA Playbook v1.0](https://www.enisa.europa.eu/sites/default/files/2026-07/ENISA_Secure_By_Design_and_Default_Playbook_v1.pdf); OpenChain CRA checklist (community draft) |
| Vulnerability handling and coordinated disclosure | Component and vulnerability documentation and SBOM (Part II(1)); remediation without delay and separation of security from functionality updates (Part II(2)); regular tests and reviews (Part II(3)); public disclosure of fixed vulnerabilities (Part II(4)); CVD policy (Part II(5)); information sharing and contact address (Part II(6); Art 13(17)); secure update distribution (Part II(7)-(8)); upstream reporting and fix sharing (Art 13(6)) | PSIRT lead | [BSI TR-03183-3 v1.0.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-3_v1_0_0.pdf?__blob=publicationFile&v=4); [ENISA SME Vulnerability Kit](https://www.enisa.europa.eu/sites/default/files/2026-10/Technical%20Advisory%20on%20security.txt%20CVD%20Policies%20and%20Security%20Advisories%20Public%20Consultation.pdf) (Oct 2026, consultation draft); [FIRST PSIRT Services Framework v1.1](https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1) |
| Support period and end of support | Determination criteria and evidence (Art 13(8); Annex VII point 4); 10-year update availability (Art 13(9)); latest-version rule and archives (Art 13(10)-(11)); end date at purchase and end-of-support notification (Art 13(19)); Annex II point 7 | Product management | Guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) Section 5, paras 125-135; OpenChain CRA checklist Section 6 |
| Third-party and open-source component due diligence | Due diligence on all components including unplaced FOSS (Art 13(5); Recital 34; guidance paras 167-173); documentation of third-party information (Art 13(7)); upstream reporting (Art 13(6); guidance paras 222-229); SBOM inclusion (Part II(1)); traceability records (Art 23) | Engineering lead or OSPO, with procurement | Commission FAQ v1.4 due-diligence actions; [ENISA SBOM advisory v1.10](https://www.enisa.europa.eu/sites/default/files/2026-10/ENISA%20Technical%20Advisory%20-%20Software%20Bill%20of%20Materials%20-%20v1.10.pdf); [VDMA](https://vdma.eu/en/cyber-resilience-act) supplier self-disclosure guideline (trade association); OpenChain CRA checklist |
| CRA reporting | Triggers and awareness test (Art 3(42); Art 14(1), (3), (5); guidance paras 211-218); clocks and content (Art 14(2), (4), (6)); routing to the coordinator CSIRT via the SRP (Art 14(7)); user notification (Art 14(8)); legacy products (Art 69(3)); records | PSIRT lead | [ENISA SRP](https://www.enisa.europa.eu/topics/product-security/vulnerability-services/eu-incident-response-and-cyber-crisis-management/single-reporting-platform-srp) glossary and AR manual v1.2; BSI TR-03183-3; OpenChain CRA checklist Section 4.5 |
| Documentation and records | Technical documentation before placing on the market and kept current (Art 31; Annex VII); DoC (Art 28; Annexes V-VI); retention of 10 years or the support period (Arts 13(13), 13(18), 18(3), 19); reasoned requests in a language the authority understands (Art 13(22)); traceability (Art 23) | Compliance lead | BSI TR-03183-1 Section 4.8 report structure; Commission FAQ v1.4 Sections 6.6-6.8 |
| Open-source stewardship (where the organisation publishes open source) | Documented, verifiable cybersecurity policy for each stewarded project (Art 24(1)); cooperation with authorities and supply on reasoned request (Art 24(2)); reporting to the extent involved (Art 24(3); guidance paras 79-82); per-project steward or manufacturer determination (guidance paras 69-74, 84) | Legal, with the OSPO | [ORC WG steward white paper V1.0](https://orcwg.org/files/cra/resources/white-paper-on-open-source-software-stewards-and-cra.pdf) (Jan 2026, "not legal guidance"); [LF Stewards Playbook](https://policy.openssf.org/CRA/stewards-playbook.html); [OSPS Baseline](https://openssf.org/wp-content/uploads/2026/01/OpenSSF-OSPS-Baseline.pdf) |

### Legal status of each policy

| Policy | Status | Basis |
|---|---|---|
| Vulnerability handling and coordinated disclosure | Legally required: the CVD policy is Annex I Part II point 5; the process behind it is Art 13(8) fourth subparagraph | Must exist by 11 Dec 2027 for every product placed from then; Annex VII point 2(b) puts it in the technical file |
| Open-source stewardship | Legally required where the organisation is a steward (Art 24(1)); applies from 11 Dec 2027 | No fines for stewards (Art 64(10)(b)), but corrective action under Art 52(3) |
| Product cybersecurity | Good practice; the obligations are real but no policy document is prescribed | Module H assessors expect written policies (Annex VIII pt 3.2) |
| Support period and end of support | Good practice; the determination evidence is required (Annex VII point 4) | A policy makes per-product decisions consistent |
| Third-party and open-source component due diligence | Good practice; Art 13(5) is an obligation of conduct, not a document | Due-diligence records are the evidence |
| CRA reporting | Good practice; Art 14 prescribes the duty, not a policy | A written awareness rule protects the 24-hour clock |
| Documentation and records | Good practice; Arts 13(13) and 31 prescribe the records | A policy stops evidence drifting into mailboxes |

### What each policy must say

**Product cybersecurity**

- Every product and every substantially modified version has a risk assessment before placing on the market. It is kept current through the support period (Art 13(2)-(4), (7)).
- The risk assessment states for each Annex I Part I(2)(a)-(m) item whether it applies and how it is implemented. Any non-applicable item carries a written justification (Art 13(3)-(4)).
- Residual risk is judged against "appropriate level of cybersecurity based on the risks". Cost, appetite or commercial strategy cannot justify unaddressed risk (guidance paras 156-163).
- No product is released with a known exploitable vulnerability; "known" includes EUVD and other databases, private disclosure and reliable media (guidance paras 230-237).
- Secure defaults, reset to original state, no default credentials and default-deny exposure are acceptance criteria (Part I(2)(b)).
- Remote data processing under the manufacturer's responsibility and needed for a product function is inside the assessed boundary (Art 3(2); guidance Section 8).
- Every release passes a security-delta assessment against the four-question substantial-modification test (guidance paras 104-124).
- Threat modelling follows a documented method and precedes development; TR-03183-1 and the ENISA Playbook are the reference methods.

**Vulnerability handling and coordinated disclosure**

- The public contact: a single point of contact that is not automated-only (Art 13(17)). Add a security.txt per RFC 9116 and an anonymous web form (TR-03183-3).
- Scope: which products, versions and services the policy covers, including out-of-support versions still reportable under Art 14.
- Safe harbour: assurances of confidentiality, no disclosure of reporter data, no legal action and no NDA requirement for good-faith research (TR-03183-3 Section 4.4).
- Timelines: acknowledgement and detailed feedback targets. BSI gives 5 and 10 working days; draft prEN 40000-1-3 caps acknowledgement at 7 calendar days (ENISA kit footnote, draft standard).
- What reporters can expect: triage, status updates, credit and a default disclosure window. BSI's model is 90 days, extendable once by 90 days with the national CSIRT.
- Every report is checked for active exploitation, because that check starts the Art 14 clock (ENISA kit "common mistakes").
- Security updates are released separately from functionality updates where technically feasible, with the Commission's exceptions documented (FAQ Section 4.3).
- Fixed vulnerabilities are disclosed publicly with affected versions and remediation, machine-readable where appropriate (Part II(4); CSAF recommended by BSI).

**Support period and end of support**

- Five years is a floor, not the default; expected use time governs (Art 13(8); guidance paras 125-128).
- The period is set per product and per substantially modified software version using the Art 13(8) criteria. The evidence goes in Annex VII point 4.
- A substantial modification triggers reassessment but does not reset the period by itself (guidance paras 132-135).
- The end date, at least month and year, is shown at purchase and in the Annex II information (Art 13(19); Annex II point 7). It also goes on the product or packaging where applicable.
- Users receive an end-of-support notification where technically feasible, and a legacy-version owner is named (Art 13(19); OpenChain CRA checklist).
- Security updates stay available for at least 10 years or the remainder of the support period (Art 13(9)).
- Remediating only the latest version is allowed only where users can upgrade free of charge without "additional costs" (Art 13(10); guidance paras 129-131).
- Reporting under Art 14 continues after the end of support; vulnerability handling does not (guidance para 210).

**Third-party and open-source component due diligence**

- Every component passes an intake gate that records the need, the evidence and the decision (Art 13(5); guidance paras 167-173; Section 6).
- The level of diligence matches the component's risk; Recital 34 and the FAQ list the actions to choose from.
- Unplaced FOSS gets the same gate; the project's own status under the CRA is irrelevant to the integrator's duty (guidance paras 86-88).
- Vulnerabilities found in a component are reported to its maintainer through the maintainer's channel (Art 13(6)). Fixes are shared in licence-compatible, machine-readable form (guidance paras 222-229).
- Suppliers of commercial components must accept the contract clauses in Section 6, or the component is treated as unsupported.
- Every component appears in the release SBOM to at least top-level dependencies (Part II(1)), with BSI TR-03183-2 depth as the target.
- Supply-chain records are kept for 10 years up and down the chain (Art 23).

**CRA reporting**

- The PSIRT lead or a named deputy declares awareness at "reasonable degree of certainty" after immediate initial assessment (guidance para 213). No approval step precedes it.
- Not reportable: good-faith findings without exploitation evidence, and component CVEs not reachable or exploited in the product (FAQ 5.2, 5.4; guidance para 218). These are still documented.
- The early warning is filed within 24 hours of awareness and the notification within 72 hours of the same awareness. The final report follows Art 14(2)(c) or 14(4)(c) timing.
- Legal reviews the 72-hour and final reports, not the early warning.
- The main-establishment Member State and coordinator CSIRT are decided in advance (Art 14(7)); a wrong choice "may invalidate the notification" (ENISA SRP FAQ 18).
- Users are informed in a timely manner, in a risk-based and proportionate way (Art 14(8); guidance paras 219-221).
- Legacy products placed before 11 Dec 2027 stay in the reportable inventory (Art 69(3)).
- UTC timestamps for first signal, awareness, escalation and each submission are recorded in the case file.

**Documentation and records**

- The Annex VII technical file exists before placing on the market and is kept current at least through the support period (Art 31(2)).
- Each product version has its own file state, with the SBOM, risk assessment, test reports and DoC version-linked to the release.
- Retention is 10 years from placing on the market or the support period, whichever is longer (Art 13(13), (18); Annex VIII).
- Documents can be supplied on reasoned request in a language the authority easily understands (Art 13(22)). The internal target is 10 working days.
- Evidence lives in the system of record (Section 8), not in mailboxes or spreadsheets.
- Every answer to an authority is logged with author, recipient and date, because misleading information is fined under Art 64(4).

**Open-source stewardship**

- Each published open-source project has a written steward or manufacturer determination, reviewed when monetisation changes (guidance paras 69-74, 84).
- The policy fosters secure development and effective vulnerability handling by the project's developers (Art 24(1)).
- It covers documenting, addressing and remediating vulnerabilities, and sharing information on discovered vulnerabilities within the community (Art 24(1)).
- It promotes voluntary reporting under Art 15 (Art 24(1)).
- It states the type of support provided, because non-technical, infrastructure and engineering support carry different Art 14 duties (guidance paras 79-82).
- It is "verifiable": evidence lives in version-controlled files such as SECURITY.md, advisories and CVE or EUVD entries (ORC WG white paper V1.0).
- It can be supplied to a market surveillance authority on reasoned request in a language it understands (Art 24(2)).

### Policy checklist

- [ ] Seven policies drafted, each with an owner from the RACI in Section 2
- [ ] CVD policy published at the URL named in security.txt and the Annex II information
- [ ] Steward policies published for every project with a steward determination
- [ ] Each policy cites the guidance version it relies on and has a review trigger in the quarterly standards review
- [ ] Policies cross-reference the Requirement checklists tab for the per-product questions they govern
