## Reporting obligations (Article 14)

Art 14 of the [CRA](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) has applied since 11 Sep 2026 to every in-scope product, including products already on the market (Art 69(3); Art 71(2)). Actively exploited vulnerabilities run on a 24-hour, 72-hour and 14-day clock; severe incidents on 24 hours, 72 hours and 1 month.

Every notification is filed on ENISA's Single Reporting Platform to the coordinator CSIRT of the manufacturer's main-establishment Member State. ENISA has simultaneous access (Art 14(7)).

### Triggers

Art 3(42) defines an actively exploited vulnerability as one with "reliable evidence that a malicious actor has exploited it" in a system without the owner's permission. A severe incident negatively affects, or could affect, the product's ability to protect "sensitive or important data or functions" (Art 14(5)(a)). It also covers an incident that has led, or could lead, to malicious code executing in the product or in users' systems (Art 14(5)(b)).

The clock starts at awareness. [Guidance C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) para 213 says the manufacturer "should assess the suspicious event immediately", and is aware once it has "a reasonable degree of certainty" after that assessment. Suspicion starts triage, not the clock; para 212 aligns this test with NIS2 Implementing Regulation (EU) 2024/2690 recital 31 and EDPB Guidelines 9/2022.

Not reportable, per [Commission FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/122331) 5.2 and 5.4 and guidance paras 217-218: good-faith research or bug-bounty findings without exploitation evidence, and component CVEs not exploitable or not exploited in the product. Voluntary Art 15 notification remains open for both, and Art 13(6) upstream reporting still applies. Exploitation already known before 11 Sep 2026 is not reported retroactively (para 217).

A ransomware incident at the manufacturer counts only if it compromises product security, such as update channels or signing keys ([BSI SRP page](https://www.bsi.bund.de/DE/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Cyber_Resilience_Act/Single_Reporting_Platform-CRA/single_reporting_platform-cra.html)). Reporting continues after the support period ends (guidance para 210).

Routing: the main establishment is where product cybersecurity decisions are predominantly taken, else the EU establishment with most employees. A manufacturer with no EU establishment uses, in order, the Member State of its authorised representative, then importer, then distributor handling most products.

Failing those, it uses the Member State with most users (Art 14(7)). A wrong choice "may invalidate the notification" ([ENISA SRP FAQ 18](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/frequently-asked-questions)).

### Timeline

Mandatory content combines the statute with the required fields in the [ENISA SRP glossary](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2). Date and time fields use UTC; estimates must be labelled.

| Stage | Deadline | Clock start | Recipient | Mandatory content | Article |
|---|---|---|---|---|---|
| AEV early warning | 24 h | Awareness with reasonable certainty | Coordinator CSIRT and ENISA via SRP | Type, title, summary, product name and version, Member States where available, UTC awareness time | 14(2)(a) |
| AEV vulnerability notification | 72 h | Same awareness time | Same; CSIRT disseminates onward | General information on product, exploit and vulnerability; measures taken; measures users can take; sensitivity; optional PEC flag | 14(2)(b) |
| AEV final report | 14 days | Availability of a corrective or mitigating measure | Same | Description of the vulnerability, including severity and impact; malicious actor where available; details of the security update or other corrective measures (date of availability is an SRP field) | 14(2)(c) |
| SI early warning | 24 h | Awareness with reasonable certainty | Same | Whether unlawful or malicious acts are suspected; Member States where available; UTC awareness time | 14(4)(a) |
| SI incident notification | 72 h | Same awareness time | Same | General nature of the incident; initial assessment; measures taken and user measures; sensitivity | 14(4)(b) |
| SI final report | 1 month | Submission of the 72 h notification | Same | Detailed severity and impact; threat type or root cause; applied and ongoing mitigation | 14(4)(c) |
| Intermediate update | On request | CSIRT request | Coordinator CSIRT | Status update | 14(6) |

No severity scale is prescribed; the glossary asks for "assessed severity rating, classification and rationale". The AEV final report has no SRP counter, so patch-availability dates must be tracked internally.

### The Single Reporting Platform

The [portal](https://portal.cra-srp.enisa.europa.eu/) went live on 11 Sep 2026 as an "initial operating capability" ([ENISA launch release](https://www.enisa.europa.eu/news/the-cra-single-reporting-platform-is-launched)). It is a web form only, with no API and no sandbox, in English only, for mandatory Art 14 notifications only. Each filer needs a personal EU Login with MFA; there is no corporate authentication.

1. The Primary Assigned Representative registers, selects the coordinator CSIRT from a drop-down, accepts the legal agreement and enters the manufacturer details ([registration guidance](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-ar-user-registration)).
2. The CSIRT validates the association in parallel (3 business days observed in Belgium); up to 20 notifications may be filed while validation is pending.
3. Once verified, the Primary invites up to 20 Secondary Assigned Representatives; invitation links expire after 7 days.
4. A notification is one record with early-warning, 72-hour and final-report tabs plus updates ([submission guidance](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-ar-notification-submission-and-update)); after the final report the record is frozen.
5. The CSIRT disseminates manually to the CSIRTs of the other Member States listed, and may delay under Art 16(2) and [Delegated Regulation (EU) 2026/881](https://eur-lex.europa.eu/eli/reg_del/2026/881/oj) (adopted 11 Dec 2025, in force 10 May 2026).
6. The "particularly exceptional circumstances" toggle exists only on the AEV 72-hour tab and limits what ENISA receives ([PEC guidance](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-guidance-particular-exceptional-circumstances-pec)).

ENISA listed coordinator CSIRTs for all 27 Member States on 4 Sep 2026 ([list](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/list-of-csirts-designated-as-coordinators)). The documentation set comprises a 31-item FAQ, the glossary, an Assigned Representative user manual (v1.2, 21 Oct 2026), guidance pages, a factsheet in 10 languages and terms and conditions. The help desk is cra-srp-helpdesk@enisa.europa.eu.

Outage fallbacks: wait and file when the platform returns (FAQ 25). [Ireland's NCSC](https://www.ncsc.gov.ie/cra/) accepts cra_fallback@ncsc.gov.ie only once ENISA declares an outage; Germany's CERT-Bund takes email in English only while the SRP is down.

Known quirk: FAQ 26 says the 72-hour counter currently runs 48 hours from early-warning submission, so a notification can show overdue early. Counters are "visibility aids", not deadlines. The Irish [National CRA Guidelines v1](https://www.ncsc.gov.ie/pdfs/National_CRA_Guidelines_v1.pdf) describe the detailed notification as due "within 48 hours of the early warning"; the statute's 72 hours from awareness governs.

No official statistics exist; the one public first-hand account ([Aikido, 23 Sep 2026](https://www.cyberresilienceact.eu/news/aikido-security-first-account-using-enisa-srp-23-september-2026.html), as reported) describes launch-day glitches fixed within hours. The SRP "Assigned Representative" is an individual login, not the Art 18 authorised representative.

### User notification (Art 14(8))

After becoming aware, the manufacturer must inform impacted users and, "where appropriate", all users. Art 14(8) sets no fixed deadline; the test is whether users are informed "in a timely manner", failing which the notified CSIRTs may inform them. The notice covers the vulnerability or incident and any mitigating measures, "where appropriate, in a structured, machine-readable format". Guidance paras 219-221 make the duty risk-based: detailed disclosure may be limited to affected customers until a fix exists, with broader disclosure once mitigated.

If the manufacturer is not timely, the notified CSIRTs may inform users themselves. No format is named; CSAF is the obvious candidate but appears in no primary source.

### Runbook

- [ ] Register at least two people on the SRP now with EU Login, MFA and backup devices; ENISA's advice to register only when needed conflicts with practitioner advice, and pending validation does not block filing
- [ ] Name the Primary and Secondary Assigned Representatives and keep the roster current
- [ ] Decide and document the main-establishment Member State and coordinator CSIRT before any incident
- [ ] Write the exploitation and severity decision criteria, including the Art 14(5) tests and "reliable evidence"
- [ ] Stand up 24/7 on-call with escalation to the person who declares awareness
- [ ] Pre-draft early-warning, 72-hour and final-report templates using the glossary field names
- [ ] Link the runbook to the PSIRT intake and the Part II vulnerability-handling process
- [ ] Dry-run one AEV and one severe incident on paper; never submit synthetic reports
- [ ] Record UTC timestamps for first signal, awareness, escalation and each submission, and retain evidence
- [ ] Prepare user-notification templates, human-readable and machine-readable
- [ ] Hold CSIRT fallback contacts and the ENISA help desk address offline
- [ ] Keep end-of-support and legacy products in the reportable inventory

### Multiple regimes

| Regime | Trigger | Clock | Recipient | Overlap note |
|---|---|---|---|---|
| CRA Art 14 | Actively exploited vulnerability or severe incident affecting product security | 24 h, 72 h, 14 days or 1 month | Coordinator CSIRT and ENISA via SRP | Product-level; applies to manufacturers only |
| NIS2 Art 23 | Significant incident at an essential or important entity | 24 h, 72 h, 1 month | National CSIRT or competent authority | Same awareness test by design; separate filing today |
| GDPR Art 33 | Personal data breach | 72 h | Data protection authority | The [Digital Omnibus proposal COM(2025) 837](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=celex:52025PC0837) would move this to 96 h; proposed, not adopted |
| DORA Art 19 | Major ICT-related incident at a financial entity | Initial, intermediate and final per the RTS | Financial competent authority | No cross-reference to the CRA; AFME asked for DORA-only reporting, a request not law |
| Proposed NIS2 Art 23(12) | CRA Art 14(3) severe-incident report containing NIS2 Art 23(4) content | Deemed to satisfy NIS2 | As CRA | In the Commission proposal and the [Council mandate ST 14756/26](https://data.consilium.europa.eu/doc/document/ST-14756-2026-INIT/en/pdf) of 22 Oct 2026; proposed, not adopted as of 30 Oct 2026 (see Interplay with other law, the Digital Omnibus and the UK position) |

Nothing today lets one filing discharge another. One compromised banking app can start four clocks with four recipients.

### Related duties and status

- Art 15 voluntary reporting of vulnerabilities, threats, incidents and near misses is not yet available in the SRP; CSIRTs must inform the manufacturer of third-party reports (Art 15(4)).
- Importers (Art 19(5)) and distributors (Art 20(4)) must inform the manufacturer of vulnerabilities without undue delay from 11 Dec 2027, and MSAs immediately where there is a significant risk.
- From 11 Dec 2027 open-source stewards fall under Art 14(1) to the extent they are involved in development, and under Art 14(3) and (8) only for severe incidents affecting network and information systems they provide for development (Art 24(3)); they are exempt from fines (Art 64(10)(b)).
- Penalties sit in the top tier: up to EUR 15,000,000 or 2.5% of worldwide annual turnover (Art 64(2)); micro and small enterprises are exempt from fines for missing the 24-hour deadlines (Art 64(10)(a), as corrected by corrigendum OJ L, 2025/90555, which extends the derogation to paragraph 2); enforcement machinery applies from 11 Dec 2027.
- No Art 14(10) implementing act on notification format or procedure has been adopted or drafted; the ENISA glossary is the de facto format.
