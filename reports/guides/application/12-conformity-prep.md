## 12. Preparing for conformity assessment

Prepare the same evidence whichever route the product takes, because a notified body asks for exactly what Module A asks you to hold yourself. The routes by class, the Annex VIII modules and the notified-body landscape are in Conformity assessment and documentation. This section is the preparation procedure.

As of 30 Oct 2026 no harmonised standard is cited and no CRA notified body is designated. Class I products cannot yet use Module A and no body can yet be engaged.

### What a Module A record contains

Module A (Annex VIII Part I) has no external party, so the record is the proof that the manufacturer did the work. It holds the Annex VII technical documentation (section 11) and the measures ensuring that design, development, production and vulnerability handling conform (points 2 and 3).

It also holds the declaration drawn up on the manufacturer's sole responsibility (point 4.2) and the CE marking decision (point 4.1).

Make it a signed internal-control report: scope and product version; the evidence index with every requirement closed; the applicability matrix sign-off. Add the gate record of the release declared, the release-approval minute and the declaration. The person who signs the declaration signs the record, with authority held by the executive sponsor or a written delegate (section 11).

Retain it with the file for 10 years or the support period.

Default-class products use Module A today. A FOSS product in Annex III may use it if the technical file is public (Art 32(5)). Everyone else keeps the same record complete as the fallback and as the body's input.

### What a notified body asks for under Module B

Module B (EU-type examination) examines the technical design and the vulnerability-handling processes and attests both. The application goes to a single body (Annex VIII Module B point 3).

It contains the manufacturer's name and address and a declaration that no other body holds it. It also contains the technical documentation, including "an adequate risk analysis" and the Annex VII elements, plus supporting evidence with test results where needed.

The body examines the documentation, verifies that specimens match it, tests the application of any standards chosen and tests non-standard solutions (point 4).

Prepare a pack with these parts.

- The Annex VII file and the risk assessment with the applicability matrix and the decision trail (section 3)
- Specimens of the product and of each critical part, built from the release under assessment, with an inventory of serials, image hashes and configuration
- Vulnerability-handling process evidence: the CVD policy, the live security.txt, the PSIRT procedure, case files and advisories (section 8)
- The update design note and tests (section 7); the SBOM and VEX per release (section 6)
- Test reports indexed by requirement

The body audits vulnerability handling periodically after certification (point 8), so the PSIRT records must keep accumulating.

### What a notified body asks for under Module H

Module H (full quality assurance) approves a quality system covering design, development, final inspection and testing, and vulnerability handling, maintained through the support period. The application (point 3.1) contains the manufacturer's details, technical documentation for one model per product category, the quality-system documentation and the no-other-body declaration. The audit team includes a product-experienced assessor and the audit includes a site visit where premises exist (point 3.3).

Surveillance means periodic audits plus site access (point 4).

Define the quality-system scope to include firmware, build pipelines, signing infrastructure and the update service; scopes that exclude them are a reported failure pattern. Pick one representative technical file per product category and bring it to the standard of section 11.

[BSI TR-03183-H v1.1.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-H_v1_1_0.pdf?__blob=publicationFile&v=3) (non-binding) shows how an extended ISO/IEC 27001 ISMS carries Module H. It refines clauses 4.2 to 8.1 and controls 5.7, 5.8, 8.8, 8.25, 8.29 and 8.32. ISO 9000 certification alone does not satisfy the module.

### The evidence index

Build one index per product or family and keep it current from the release gate. It is the first page a body or an authority reads, and it is the Module A record's spine.

| Requirement | Evidence | Location | Owner | Date |
|---|---|---|---|---|
| Annex I Part I 2(a) | Gate record G-2026.11 with KEV check; VEX V-031; scan reports | repo/evidence/releases/2.4.1/ | Product security | 2026-11-05 |
| Annex I Part I 2(b) | Default-config baseline FC-09; reset test RT-02; provisioning record P-02 | repo/evidence/controls/2b/ | Firmware lead | 2026-10-20 |
| Annex I Part I 2(c) | Update design note UDN-3; tests UT-01 to UT-12 | repo/evidence/update/ | Platform lead | 2026-10-22 |
| Annex I Part II(1) | Signed SBOM S-2026.10, sbomqs score, attestation | artefact store, release 2.4.1 | SBOM owner | 2026-11-05 |
| Annex I Part II(5), (6) | CVD policy v3; security.txt capture; intake monitoring log | security site; repo/evidence/psirt/ | PSIRT lead | 2026-10-01 |
| Art 13(3)-(4) | Risk assessment RA-7 with applicability matrix and change log | repo/evidence/risk/ | Product security | 2026-10-28 |
| Art 13(8) | Support-period determination SP-2; version-support register | repo/evidence/support/ | Product management | 2026-10-15 |
| Annex II | User information v2.4 at the versioned URL | security site | Technical writing | 2026-11-05 |
| Annex V | Declaration D-2026-02 signed | repo/evidence/doc/ | Compliance lead | 2026-11-06 |

Add one row per Annex I item, per Part II point, per Art 13 paragraph that needs evidence, and per Annex VII point. Every evidence identifier resolves to a file under version control or in the artefact store; nothing resolves to a mailbox.

### Pre-assessment and gap review

Run a gap review on one representative product before engaging anyone, using the evidence index and the Requirement checklists tab. Score each row as present, partial or missing with the owner and the fix date. Record the review itself as evidence of the Module A point 3 measures.

Labs sell readiness assessments and "Module B+C simulations" (TÜViT, DEKRA, Brightsight, Applus+, UL; vendor offers). They give an outside reading of the file but confer no conformity status.

Have someone outside engineering read the file for completeness and traceability. The failure mode early adopters report is not weak security but security that "could not show the decision trail".

### Substantial modifications with the body

Under Module B the manufacturer must inform the body of any modification that may affect conformity or certificate validity. Such modifications need approval as an addition to the certificate (Module B point 7).

Report every positive security-delta decision from the release gate (section 5). Report borderline negative decisions with the reasoning too, since the information duty is wider than the test.

Under Module H, intended changes to the quality system go to the body (point 3.5). New or substantially modified products extend the approved system through the same body in a streamlined process ([Commission FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307) section 6.3).

A substantial modification is a new placing on the market. The re-assessment focuses on the modified parts and reuses unaffected documentation (guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) paras 116, 122-123). Keep the delta assessment and the body's response together in the file.

### While no body is designated

Keep the Module A paperwork complete for every product, including Class I, Class II and critical products that will need a body. The record, the evidence index and the file are the application pack once a body exists. They are also what a market surveillance authority can request from 11 Dec 2027 regardless of route.

Pre-contract two or three candidates now. Brightsight holds RvA accreditation pending Dutch notification and Applus+ is in the accreditation process (both vendor statements); others state they will apply. Ask each for its intended modules, accreditation status, expected designation date and a conditional engagement letter, and check NANDO before signing anything.

Track the OJ for harmonised-standard citations. A citation of a vertical standard covering the product's core functionality reopens Module A for Class I products if applied in full. Aligning the file to the draft's clause structure now reduces re-work.

### Timelines

All figures are vendor or commentator estimates and none comes from an authority or a designated body.

| Item | Estimate | Source |
|---|---|---|
| Accreditation plus notification per body | 12 to 18 months | [CRA Decoded](https://cra-decoded.com/blog/posts/cra-notified-body-capacity-crisis/), commentary |
| Finding and contracting a body | 2 to 4 months | CRA Decoded, commentary |
| Module B+C engagement once engaged | 3 to 6 months; 3 to 12 months for complex products | CRA Decoded; [sota.io](https://sota.io/blog/cra-notified-bodies-developer-guide-conformity-assessment-2026), vendor, unsourced |
| Module H surveillance | Every 1 to 2 years | CRA Decoded, commentary |
| Module B examination fee | EUR 20,000 to 60,000; EUR 15,000 to 80,000 | CRA Decoded; sota.io, vendor, unsourced |
| First Module H engagement | EUR 80,000 to 150,000 | CRA Decoded, commentary |

Working back from 11 Dec 2027 on those estimates means contracting by the first quarter of 2027. Plan on that basis and label it as an estimate in the programme plan. Keep the Module A record complete as the only part of the timeline you control.
