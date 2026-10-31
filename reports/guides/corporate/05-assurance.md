## 5. Risk and assurance model

Product risk under the CRA is not enterprise risk, and the assurance model must say so in writing. The Art 13 risk assessment is judged against an "appropriate level of cybersecurity based on the risks" (Annex I Part I(1)). Guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) paras 156-163 add that "internal risk tolerance, commercial strategy or mere cost considerations are not relevant" to that judgement.

This section sets out three lines of assurance and the product-risk category the enterprise framework needs. It then covers applicability sign-off and how an ISO/IEC 27001 ISMS can carry Module H. It closes with what auditors expect and what existing certificates prove.

### Three lines of assurance

| Line | Who | What they do | Evidence produced | Independence |
|---|---|---|---|---|
| 1. Engineering self-assessment | Product team, engineering lead | Threat model, risk assessment, Annex I applicability matrix, controls, tests, SBOM, release-gate record | Risk assessment with decision trail; release security gate record; test reports | None; the team that builds also assesses |
| 2. Product security review | Product security officer and reviewers outside the delivering team | Challenge the threat model, verify the applicability justifications, check the release-gate evidence, sign off residual risk | Signed risk assessment; review notes; accepted and rejected residual risks | Reviewer has no delivery role on the product |
| 3. Internal audit or compliance sampling | Internal audit, or the compliance lead sampling across families | Test that lines 1 and 2 ran as written; sample technical files; check retention, system-of-record integrity and reasoned-request readiness | Audit reports to the programme board and executive review | Reports outside the product organisation |

Line 2 is the one most organisations lack. Early adopters performed risk assessments but "could not show the decision trail" ([OmniTrust](https://omnitrust.com/blog/eu-cra-tales-from-the-trenches-3-why-security-maturity-is-not-enough-for-cra-readiness/), consultancy). The second line exists to make that trail visible before a notified body or authority asks for it.

Line 3 should sample, not re-perform. One technical file per product family per year, chosen by risk, shows the system works and feeds the KPIs in Section 11.

### The product-risk rule

The enterprise risk framework needs a product-risk category with its own acceptance rules, because the usual rules do not apply.

| Enterprise risk habit | Product-risk rule under the CRA | Source |
|---|---|---|
| Risk above appetite may be accepted with a business case | Residual risk is judged against the appropriate level of cybersecurity for the product; appetite is irrelevant | Annex I Part I(1); guidance paras 156-163 |
| Cost of control is weighed against likelihood and impact | Cost alone cannot justify leaving a risk unaddressed; if a risk cannot be addressed, design or intended purpose may have to change | Guidance paras 156-163 |
| Risk may be transferred to the customer by contract or warning | Risk cannot be transferred to users to compensate for design shortcomings; user information treats residual risk, not design gaps | Guidance paras 156-163; Recital 55; Annex II point 5 |
| Annual risk review | Update on security-relevant release, newly known vulnerability or new threat; maintained through the support period | Art 13(2)-(4), (7); [BSI TR-03183-1 v1.0.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-1_v1_0_0.pdf?__blob=publicationFile&v=3) RH_UPD.1 |
| Risk owner is any manager | Residual product risk is accepted by the product security officer; appeal to the executive sponsor on a non-cost basis only | Section 2 |

Write the category into the risk policy, with its own register, acceptance authority and escalation. Tailor-made products are the one place contract can narrow obligations, and only for secure-by-default and free updates (FAQ Section 4.2). Everything else stays with the manufacturer whatever the contract says.

### Per-item applicability sign-off

Art 13(3) requires the risk assessment to state whether and how each Annex I Part I(2)(a)-(m) item applies and how it is implemented. Art 13(4) and Recital 55 require a justification for each item marked not applicable. Part II items are not subject to this test; all eight apply throughout the support period (FAQ Section 4.1).

1. Line 1 completes the applicability matrix as a design input, before development, and refreshes it at each release gate.
2. Each "not applicable" entry carries a reason tied to intended purpose or interoperability constraints. It also names the compensating measure, such as limiting intended purpose to trusted environments or informing users (FAQ Section 4.1).
3. Line 2 signs the matrix as a whole; a matrix cannot be signed with a blank justification.
4. The signed matrix is filed in the technical documentation under Annex VII point 3 and referenced from the DoC pre-signature checklist (Section 2).
5. Line 3 samples justifications against the knowledge base, Annex I Part I: essential requirements for product properties, and the Requirement checklists tab.

Items (2)(c) automatic updates and (2)(m) data transfer carry a second "where applicable". Recital 56 gives carve-outs for components and professional or industrial environments. Those are the most common non-applicable entries and the most scrutinised.

### Extending an ISO/IEC 27001 ISMS to carry Module H

Non-binding [BSI TR-03183-H v1.1.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-H_v1_1_0.pdf?__blob=publicationFile&v=3) (30 May 2026) shows how an ISO/IEC 27001 ISMS can be extended to design, development, production and vulnerability handling. It is not a new management-system standard and gives no presumption of conformity. BSI's accreditation programme for Module H bodies builds on ISO/IEC 17021-1 with TR-03183-H, so it is the reference for German-notified bodies at least.

| TR-03183-H refines | Clause or control | What changes |
|---|---|---|
| ISMS scope and context | ISO/IEC 27001 clauses 4.2, 4.3 | Interested parties include users, authorities and notified bodies; scope must include the products, their RDPS, build pipelines and update infrastructure |
| Policy and risk | Clauses 5.2, 6.1.2, 6.1.3, 6.3 | Product-risk assessment per TR-03183-1 sits inside the ISMS risk process; the product-risk rule above is written into 6.1.3 acceptance criteria |
| Communication and documented information | Clauses 7.4, 7.5.1 | Annex II user information, advisories and Art 14 reports are controlled communications; Annex VII files are controlled documents |
| Operational planning | Clause 8.1 | Design, development, production and post-market updates run as controlled processes; updates are "changes to the product" |
| Threat intelligence and project security | ISO/IEC 27002 controls 5.7, 5.8 | Threat feeds drive risk-assessment updates; security is planned into every product project |
| Technical vulnerabilities | Control 8.8 | Covers product vulnerabilities, not only infrastructure; links to Annex I Part II |
| Secure development, testing, change | Controls 8.25, 8.29, 8.32 | SDLC, security testing and change management are specified to CRA Part II expectations |
| Quality additions | ISO 9001 elements | Production, final inspection and testing requirements that ISO/IEC 27001 does not carry |

Two warnings. Module H "is not just a quality system certification" (TR-03183-H Appendix B). The body also reviews one technical file per product category, with a product-field assessor on the team (Annex VIII Module H pts 3.1, 3.3).

An ISMS whose scope excludes firmware, build pipelines or update infrastructure cannot carry Module H, whatever its certificate says.

### Choosing Module H over B+C

| Factor | Favours Module H | Favours Module B+C |
|---|---|---|
| Portfolio size | Many product types; FAQ Section 6.3 describes H as suited to many types or frequent updates | Few, stable product types |
| Change rate | Frequent substantial modifications; scope extensions go to the same body as a "more streamlined process" (FAQ Section 6.3) | Rare substantial modifications; each needs a new type examination |
| Existing systems | ISO/IEC 27001 ISMS already covering product engineering | No ISMS, or one scoped to IT only |
| Marking | Notified-body number follows the CE mark (Art 30(4); Module H pt 5.1) | No body number on the mark; certificate referenced in the DoC (Annex V item 7) |
| Cost (vendor estimates, unverified) | First engagement EUR 80,000-150,000 with surveillance every 1-2 years; break-even around four products ([CRA Decoded](https://cra-decoded.com/blog/posts/cra-notified-body-capacity-crisis/), commentary) | EUR 20,000-60,000 per type examination (same source) |
| Surveillance | Periodic audits of the quality system plus site access (Module H pt 4) | Periodic audits of vulnerability handling under Module B pt 8 |
| Availability | Needs a body accredited to EN ISO/IEC 17021-1 for the CRA; none designated as of checks to 8 Sep 2026 | Needs a body accredited to EN ISO/IEC 17065; same position |

Whichever route is chosen, keep the Module A paperwork complete regardless (knowledge base, Engineering compliance programme). A Module A record is also the fallback if an OJ citation arrives before a Class I product is placed on the market.

### Evidence auditors expect

Notified bodies and labs have not published checklists, but their service pages converge (Brightsight, TÜViT, Applus+, UL, all vendor statements).

- Technical documentation structured to Annex VII, with the risk assessment and its applicability matrix at the centre.
- A threat model with a data-flow diagram and an asset list in three categories: data, functional and security (TR-03183-1).
- Decision records for each applicability path, in the EN 18031 style of requirement, asset, interface, path, rationale and evidence (QIMA, vendor).
- An SBOM per release and a vulnerability-handling process with a live CVD policy.
- Test evidence tied to the release: SAST, DAST or fuzzing, penetration test, and re-tests on new threat input (guidance paras 238-240).
- Mapping from existing certifications (IEC 62443, EUCC, SESIP, EN 18031) to Annex I, with the gaps named.
- A supplier evidence trail: SBOMs, attestations and due-diligence records (UL, vendor).

### Limits of existing certificates as CRA evidence

| Certificate | What it does prove | What it does not prove | Source |
|---|---|---|---|
| ISO/IEC 27001 | A management system exists and is audited | Product conformity; nothing unless the scope covers products, pipelines and update infrastructure; ISO 9000 alone does not satisfy Module H | FAQ Section 6.3; TR-03183-H |
| IEC 62443-4-1 and 4-2 | A strong SDLC and component controls for industrial systems; covers 36 of 42 NIST SSDF tasks (ISAGCA) | Fixed reporting timelines, SBOM depth, public disclosure, user documentation; not expected to be cited in the OJ | JRC-ENISA mapping; [IBF Solutions](https://www.ibf-solutions.com/en/news-and-knowledge/technical-papers-and-news-on-ce-marking/current-status-of-standardisation-for-the-cyber-resilience-act) (consultancy) |
| EN 18031-1/-2/-3 | RED cybersecurity conformity for radio equipment placed to 10 Dec 2027 | CRA conformity. [Delegated Regulation (EU) 2026/339](https://eur-lex.europa.eu/eli/reg_del/2026/339/oj/eng) repeals the RED act from 11 Dec 2027. Evidence is partly reusable but "does not replace" an EN 40000-1-4 assessment | Knowledge base, Interplay with other law, the Digital Omnibus and the UK position |
| EUCC or Common Criteria | Assurance against a protection profile; a "substantial" certificate may lift the third-party duty once an Art 27(9) delegated act names the scheme | CVD policy and free updates sit outside CC; RDPS unaddressed; the Art 27(9) act is planned for Q4 2026 and not adopted | ENISA EUCC-CRA study, Feb 2025; knowledge base, Standards and guidance map |
| Any draft EN 40000 or ETSI EN 304 6xx assessment | Evidence under Annex VII point 5 as a technical specification; reduces rework when cited | No presumption and no Module A eligibility for Class I until the OJ citation exists | Art 27; guidance paras 148-151 |

The common lesson from early adopters is that "being secure and being CRA-ready are not the same thing" ([OmniTrust](https://omnitrust.com/blog/eu-cra-tales-from-the-trenches-3-why-security-maturity-is-not-enough-for-cra-readiness/), consultancy). Certificates are inputs to the risk assessment and the standards list, never substitutes for the file.

### Assurance checklist

- [ ] Product-risk category with its own acceptance rule and authority written into the enterprise risk framework
- [ ] Line 2 reviewers named per product family, with no delivery role on the products they review
- [ ] Applicability matrix template adopted with mandatory justification fields and sign-off
- [ ] ISMS scope statement checked against products, RDPS, pipelines and update infrastructure
- [ ] Module H or B+C decision recorded per family with the factors above
- [ ] Certificate-to-Annex I mapping produced for every existing certification, gaps listed
- [ ] Line 3 sampling plan agreed for the year, one file per family minimum
