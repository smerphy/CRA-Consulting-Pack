## 8. Evidence and records management

The CRA is enforced on documents, so the organisation needs one system of record for product compliance evidence, not mailboxes and spreadsheets. Early adopters with mature security programmes "could not show the decision trail"; evidence sat across ticketing, file shares, test platforms and email ([OmniTrust](https://omnitrust.com/blog/eu-cra-tales-from-the-trenches-3-why-security-maturity-is-not-enough-for-cra-readiness/), consultancy). Formal non-compliance, such as unavailable or incomplete technical documentation, is enforceable on its own under Art 58.

This section defines what the system holds per product version, for how long, and how it is versioned and controlled. It then covers answering an authority, custody with representatives and importers, the product-liability dimension from 9 Dec 2026 and the audit trail.

### The system of record

The system of record is wherever the organisation chooses to keep controlled, versioned, access-managed records with an audit trail. A GRC platform, a document-management system or a dedicated product-compliance tool all qualify. A shared drive with naming conventions does not, and neither does the ENISA SRP, whose drafts live in one individual's account.

| Property | Requirement | Why |
|---|---|---|
| Single index | Every product version in the scope register (Section 4) resolves to its evidence set | Annex VII point 1(b): software versions affecting compliance must be identifiable |
| Immutable versions | Records are superseded, not edited; the state at placing on the market is recoverable | Art 31(2): documentation drawn up before placing and kept current; authorities ask about the version placed |
| Machine-readable where possible | SBOMs, VEX, attestations, test outputs stored as data, not screenshots | ENISA [Playbook v1.0](https://www.enisa.europa.eu/sites/default/files/2026-07/ENISA_Secure_By_Design_and_Default_Playbook_v1.pdf) Section 5.1: machine-processable attestations keep documentation current |
| Pipeline-fed | Release gates write their records automatically; humans add decisions | Reduces hand assembly for each request |
| Access-controlled | Role-based access with a log of reads and exports | Art 13(22) responses and Art 64(4) exposure need to show who saw and sent what |
| Exportable | A complete technical file per version exports as a package an authority can read | Art 13(22): paper or electronic form, in a language the authority understands |
| Retained | Retention rules enforced by the system, not by memory | Arts 13(13), 13(18), 18(3), 19, 23 |

### What it holds per product version

| Record | CRA basis | Produced by | Notes |
|---|---|---|---|
| Technical documentation per Annex VII | Art 31; Annex VII points 1-8 | Compliance lead assembles from the records below | [BSI TR-03183-1 v1.0.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-1_v1_0_0.pdf?__blob=publicationFile&v=3) Section 4.8 is a usable skeleton until EN 40000-1-x is cited |
| Cybersecurity risk assessment with the Annex I applicability matrix | Art 13(2)-(4), (7); Annex VII point 3 | Product security officer (Section 5) | Signed, with decision trail and update log |
| SBOM per release | Annex I Part II(1); Annex VII points 2(b), 8 | Build engineering | Signed, with known unknowns; supplied to an MSA on reasoned request; not public by default (Recital 77) |
| VEX and CSAF statements and advisories | Annex I Part II(2), (4); guidance para 218 | PSIRT | "Not_affected" statements are evidence that no Art 14 report was due |
| Test evidence | Annex I Part II(3); Annex VII point 6 | Security testing | SAST, DAST, fuzzing, penetration tests, re-tests on new threat input |
| Release security gate record | Annex I Part I(2)(a); guidance paras 230-237, 104-124 | Release manager | Exploitability decision, SBOM hash, secure-default check, security-delta assessment |
| EU declaration of conformity | Art 28; Annexes V-VI | Legal with compliance lead | DoC id, signatory, authority instrument reference (Section 2) |
| Annex II user information | Art 13(18); Annex II | Technical writing | Each published version, with the end-of-support date shown |
| Classification and scope decision records | Arts 2, 7; Section 4 | Compliance lead | Guidance paragraphs relied on and their version |
| Conformity assessment records | Art 32; Annex VIII | Compliance or quality lead | Module A record; Module B certificate and change notifications; Module H approvals, changes and audit reports |
| Supplier and component evidence | Art 13(5)-(7); Art 23 | Procurement, engineering, OSPO | Questionnaires, SBOMs, attestations, intake-gate records, upstream reports |
| Support-period determination | Art 13(8); Annex VII point 4 | Product management | The information taken into account, per version |
| Reporting records | Art 14; Art 16 | PSIRT | Case files, UTC timelines, decision logs, SRP receipts, user notifications, drill records (Section 7) |
| Standards and guidance applied | Annex VII point 5 | Compliance lead | Which standards, specifications and guidance versions, fully or partly applied |
| Traceability records | Art 23 | Supply chain operations | Who supplied you and whom you supplied, 10 years each way |

### Retention

| Record | Period | Source |
|---|---|---|
| Technical documentation and EU declaration of conformity | At least 10 years after placing on the market, or the support period, whichever is longer | Art 13(13); Annex VIII Module A pt 4.2, B pt 10, C pt 3.2, H pts 5.2 and 6 |
| User information and instructions | At least 10 years or the support period, whichever is longer | Art 13(18) |
| Copies held by an authorised representative | 10 years or the support period, whichever is longer | Art 18(3) |
| Copy of the declaration held by an importer | 10 years or the support period, whichever is longer | Art 19 |
| Traceability of operators up and down the chain | 10 years after being supplied and 10 years after supplying | Art 23 |
| Module B certificate, annexes and additions | With the technical documentation, 10 years or the support period | Annex VIII Module B pt 10 |
| Module H quality-system documentation, approved changes, body decisions and audit reports | At least 10 years or the support period | Annex VIII Module H pt 6 |
| Security updates themselves | Available for at least 10 years or the remainder of the support period | Art 13(9) |
| Reporting case files and receipts | Align to the technical documentation period for the product concerned | Internal rule; Art 16(3) makes reports visible to MSAs |

Because the support period for a long-lived product can exceed 10 years, the retention clock is per version and ends at the later date. The system must compute it from the scope register, not from a fixed policy figure.

### Versioning tied to releases

1. Every release that passes the gate creates or updates a version record; nothing is filed against "the product" without a version.
2. The record carries the state of each artefact at placing on the market, plus later updates with their dates. Both Art 31(2) currency and the original state are then recoverable.
3. A substantial modification opens a new version lineage with its own risk-assessment delta and support period (guidance paras 104-124). It may need its own DoC (FAQ Section 6.8).
4. A product family may share one risk assessment, technical file and DoC (guidance paras 174-177). Each variant still resolves to that shared set.
5. Guidance para 113 requires documentation kept "accurate, complete and continuously up to date" whether or not an update is substantial. The pipeline feed meets that without hand editing.

### Answering an authority

Art 13(22) requires the manufacturer to answer a reasoned request from a market surveillance authority with all information needed to demonstrate conformity. It may be on paper or electronic, but must be in a language the authority easily understands. The text sets no deadline, so set an internal one and name the owner.

| Step | Owner | Target |
|---|---|---|
| Log the request, its legal basis and the authority's language | Compliance lead | Same day |
| Confirm the product versions concerned from the register | Compliance lead | Day 1 |
| Export the technical file package for those versions | System of record | Day 2 |
| Legal review of the package and the covering response | Legal | Days 3-7 |
| Translation or summary where the file is not in a language the authority understands | Compliance lead | Within the target |
| Deliver, log recipient, date and contents | Compliance lead | 10 working days |

Ten working days is an internal target, not a legal deadline. Documentation may be kept in any language, but the authority is entitled to a version it understands (FAQ Section 6.6). Plan translation capacity for the Member States in the register.

The knowledge base, Enforcement, market surveillance and penalties, covers the powers behind the request.

Expect requests informed by your own filings. Art 16(3) feeds every Art 14 report to the market surveillance authorities, and Art 60 lets ENISA propose sweeps from that data. Art 13(25) lets MSAs request SBOMs for ADCO dependency assessments outside any investigation.

### Custody with the authorised representative and importers

An authorised representative must keep the DoC and technical documentation for 10 years or the support period (Art 18(3)). It must supply them on reasoned request. An importer must keep a copy of the DoC for the same period and verify that the technical documentation exists (Art 19).

Both therefore need a controlled copy or controlled access, not an email attachment.

- Give the representative read access to the system of record for the products in its mandate. Alternatively, deliver a versioned package at each placing and update.
- Record in the mandate which Annex VIII tasks the representative performs, since Modules A, B, C and H each allow delegation of specified points.
- Supply importers with the DoC per version and a confirmation that the technical documentation exists, logged in the system.
- On a change of representative or importer, transfer custody formally and record it; the 10-year duty follows the product, not the contract.
- Review custody arrangements at the quarterly review and on any market change in the register.

### The product-liability dimension from 9 Dec 2026

[Directive (EU) 2024/2853](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024L2853) applies to products placed on the market from 9 Dec 2026. Software is a product, a cybersecurity vulnerability can be a defect (recital 32), and Art 9 gives claimants a right to disclosure of evidence. The CRA technical file, SBOM, risk assessment and update logs therefore become disclosable evidence in civil claims, and the main defence file.

Three consequences follow. Art 10(2)(b) presumes defectiveness where the claimant shows non-compliance with mandatory safety requirements, which Annex I becomes from 11 Dec 2027. Art 11(2)(c) removes the later-defect defence for a lack of software updates within the manufacturer's control, so update logs matter.

Art 7(2)(f) counts "safety-relevant cybersecurity requirements" in assessing defectiveness, so courts as well as authorities will read the applicability matrix.

Write records as if they will be disclosed. Decision trails, justifications and risk acceptances should stand on their own without oral explanation. See the knowledge base, Interplay with other law, the Digital Omnibus and the UK position.

### Audit trail for answers to authorities

Art 64(4) fines incorrect, incomplete or misleading information supplied to notified bodies or authorities in reply to a request. The ceiling is EUR 5m or 1% of worldwide turnover. The exposure sits on the content of the answer, so the trail must show who said what to whom.

- Every outbound answer to an authority or notified body is logged with author, approver, recipient, date, the question and the documents sent.
- Answers are drawn from the system of record, not reconstructed; where a statement cannot be evidenced, it says so.
- Corrections are filed as new entries referencing the original, never by editing the original.
- Oral exchanges, such as calls with a CSIRT or notified-body auditor, are minuted and filed the same day.
- Legal reviews any statement about conformity, classification or awareness before it leaves (Section 2).
- The trail is sampled by the third line of assurance (Section 5).

### Evidence checklist

- [ ] System of record chosen and every scope-register row resolves to a version-level evidence set
- [ ] Retention computed per version from the support period, with the later of 10 years or support period enforced
- [ ] Release gate writes its record automatically; manual records are the decisions only
- [ ] Reasoned-request procedure tested end to end against the 10 working-day target, with translation capacity identified
- [ ] Authorised representative and importers hold controlled copies or access, recorded in the mandate
- [ ] Records reviewed for disclosure readiness under Directive (EU) 2024/2853 Art 9
- [ ] Outbound-answer log in use for every authority and notified-body contact
