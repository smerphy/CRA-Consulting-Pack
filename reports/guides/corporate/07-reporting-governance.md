## 7. Reporting and incident governance

Art 14 has applied since 11 Sep 2026, so this part of the programme must already work, legacy products included (Art 69(3)). The organisational design has to deliver an early warning within 24 hours of awareness on any day of the year. That rules out committee approval and legal review before the first filing.

This section covers the PSIRT, the awareness authority, platform governance and the choice of coordinator CSIRT. It then covers multi-regime coordination, user communication, drills and records. The platform mechanics, clocks and field sets are in the knowledge base, Reporting obligations (Article 14), and are not repeated here.

### PSIRT distinct from the infrastructure CSIRT

[BSI TR-03183-3 v1.0.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-3_v1_0_0.pdf?__blob=publicationFile&v=4) requires at least two roles: a PSIRT for products and services, and a CSIRT for the organisation's own infrastructure. They may not be the same person unless the organisation is a microenterprise.

Art 14 is about the product's security. A ransomware incident at the manufacturer counts only if it compromises product security, such as update channels or signing keys (knowledge base, Reporting obligations).

| Function | PSIRT | Infrastructure CSIRT |
|---|---|---|
| Object | Products, companion apps, RDPS, components shipped | Corporate networks, endpoints, SaaS the company uses |
| Intake | security.txt, psirt@ mailbox, anonymous web form, supplier notifications, telemetry | SOC alerts, IT service desk, threat intelligence |
| Decision owned | Art 14 awareness; CVD disclosure timing; Art 14(8) user notification | Incident severity for the enterprise; NIS2 or GDPR notifications where applicable |
| Reporting channel | ENISA SRP to the coordinator CSIRT | National CSIRT or competent authority under NIS2; DPA under GDPR |
| Framework | [FIRST PSIRT Services Framework v1.1](https://www.first.org/standards/frameworks/psirts/psirt_services_framework_v1.1) | NIST SP 800-61 or equivalent |
| Shared | Threat intelligence, forensics, the multi-regime coordination cell below | |

BSI recommends functional mailboxes with "psirt" and "csirt" prefixes and dedicated OpenPGP keys valid for five years or less. It also recommends daily automated reachability tests and enough staff "to compensate for any absences". A published CVD policy that nobody staffs is among the most reported pitfalls (ENISA [SME Vulnerability Kit](https://www.enisa.europa.eu/sites/default/files/2026-10/Technical%20Advisory%20on%20security.txt%20CVD%20Policies%20and%20Security%20Advisories%20Public%20Consultation.pdf), Oct 2026 consultation draft).

### 24/7 on-call and the deputy chain

1. One PSIRT lead holds the awareness authority (Section 2); two named deputies hold it in the lead's absence, in a written order.
2. An on-call rota covers every hour; the person on call can reach an Assigned Representative with SRP access within one hour.
3. At least two Assigned Representatives are registered with EU Login, MFA and backup devices; the SRP has no corporate login, so each is personal.
4. The Primary and Secondary Assigned Representatives are themselves on the rota or reachable from it, because only they can file.
5. The rota, deputy chain and awareness authority are re-confirmed annually and on any personnel change (OpenChain CRA checklist Section 4.5, community draft).
6. Weekend coverage, loss of platform access and supplier delays are tested in drills (below).

### The awareness decision and its written criteria

Guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) para 213 requires an "immediate" assessment of a suspicious event. Awareness follows at "a reasonable degree of certainty". Suspicion starts triage; certainty starts the clock.

The criteria below are the PSIRT runbook's written test; they belong to the PSIRT lead and no one else.

| Criterion | Reportable when | Not reportable when | Source |
|---|---|---|---|
| Actively exploited vulnerability | There is reliable evidence that a malicious actor exploited the vulnerability in a system without permission | A proof of concept or published exploit exists but no exploitation is observed | Art 3(42); BSI webinar examples via [SCHUTZWERK](https://www.schutzwerk.com/en/blog/cra-guidance-2026/) (vendor, second-hand) |
| Research or bug-bounty finding | Only if exploitation evidence accompanies it | Good-faith finding without exploitation evidence; voluntary Art 15 report possible | FAQ 5.2; guidance para 218 |
| Component vulnerability | The vulnerable code is present, reachable and exploited in this product | Code not present, not reachable or not exploited in the product; record the VEX justification | FAQ 5.4; guidance para 218 |
| Severe incident | The incident affects, or could affect, the product's ability to protect sensitive data or functions, or leads to malicious code in the product or users' systems | An enterprise incident with no product-security effect | Art 14(5)(a)-(b) |
| Legacy product | Same tests; products placed before 11 Dec 2027 are reportable | Exploitation already known before 11 Sep 2026 is not reported retroactively | Art 69(3); guidance para 217 |
| Out-of-support product | Same tests; reporting continues after end of support | | Guidance para 210 |

Write a "not reportable" decision with the same rigour as a report ([Clarysec](https://blog.clarysec.com/posts/eu-cra-2026-vulnerability-reporting-readiness/), vendor). The case file records the awareness timestamp in UTC, the criterion applied and the evidence. For a component, a "not_affected" VEX statement with its justification is both the engineering artefact and the evidence that no report was due.

### Where legal review sits

Legal reviews the 72-hour notification and the final report, never the 24-hour early warning. The early warning carries only the glossary's mandatory fields: type, title, summary, product and version, Member States and UTC awareness time. For incidents it adds whether malicious acts are suspected.

Nothing in it needs legal drafting, and waiting for approval is a named pitfall ([Wavect](https://wavect.io/blog/cyber-resilience-act-reporting-playbook-2026/), vendor).

Legal's job at 72 hours is the description of the vulnerability or incident, the measures taken and the user-facing wording. At the final report it is severity, impact and the record that will be visible to market surveillance under Art 16(3). Legal also owns the "particularly exceptional circumstances" decision, which exists only on the actively-exploited-vulnerability 72-hour tab.

### Platform governance

The SRP Assigned Representative is an individual with an EU Login, not the Art 18 authorised representative. The roster needs managing like any privileged access.

| Item | Rule | Source |
|---|---|---|
| Accounts | Personal EU Login with MFA for each Assigned Representative; passkeys and backup MFA devices; no shared accounts | ENISA SRP FAQ 9; practitioner account via [cyberresilienceact.eu](https://www.cyberresilienceact.eu/news/aikido-security-first-account-using-enisa-srp-23-september-2026.html) |
| Roles | One Primary Assigned Representative; up to 20 Secondary Assigned Representatives invited by the Primary once verified; invitation links expire after 7 days | ENISA SRP FAQ 9; registration guidance |
| Who holds them | PSIRT lead and deputies as Primary and first Secondaries; compliance lead as a Secondary; no one outside the on-call chain | Section 2 |
| Roster | Held in the system of record with name, role, EU Login identity, date granted, date reviewed | Section 8 |
| Offboarding | Remove or replace a leaver's association on exit day; a Secondary may claim the Primary role subject to CSIRT approval, so plan the succession | ENISA SRP FAQ 9 |
| Drafts | Drafts are visible only to the creating Assigned Representative, so the authoritative case record is internal, never the SRP | ENISA SRP FAQ; Section 8 |
| Validation | The coordinator CSIRT validates the association in parallel; up to 20 notifications may be filed while pending | ENISA SRP FAQ 9 |
| Help desk and fallbacks | cra-srp-helpdesk@enisa.europa.eu, national fallbacks and the coordinator CSIRT contact held offline | Knowledge base, Reporting obligations |

ENISA advises registering only when a notification is needed, to limit CSIRT workload; practitioners advise pre-registering. The safer position is to create the EU Login accounts and pre-decide the coordinator CSIRT now. Validation does not block filing (knowledge base, Reporting obligations).

### Choosing and documenting the coordinator CSIRT

Art 14(7) routes every report to the CSIRT designated as coordinator in the Member State of the manufacturer's main establishment. The main establishment is where decisions on product cybersecurity are predominantly taken, else the EU establishment with most employees. A manufacturer with no EU establishment uses the Member State of its authorised representative, then importer, then distributor, then most users.

1. Legal and the compliance lead decide the Member State and record the reasoning in a decision record (Section 4 format), before any incident.
2. The record names the coordinator CSIRT from ENISA's list of 4 Sep 2026 and its contact URL.
3. A group with several legal entities decides per manufacturer entity, because the SRP association is per manufacturer.
4. The decision is reviewed when product-security decision-making moves, on acquisition or restructuring, and at the quarterly review.
5. The reason this matters: a wrong choice "may invalidate the notification" (ENISA SRP FAQ 18).

### The multi-regime coordination cell

One compromised product can start several clocks with several recipients, and nothing in force lets one filing discharge another (knowledge base, Reporting obligations). Organisations also under NIS2, GDPR or DORA need a standing coordination cell, convened by the PSIRT lead on any awareness declaration.

| Regime | Who in the cell | Their clock | Their recipient |
|---|---|---|---|
| CRA Art 14 | PSIRT lead, Assigned Representative | 24 h, 72 h, 14 days or 1 month from awareness | Coordinator CSIRT and ENISA via the SRP |
| NIS2 Art 23 | Infrastructure CSIRT, NIS2 compliance owner | 24 h, 72 h, 1 month | National CSIRT or competent authority |
| GDPR Art 33 | Data protection officer | 72 h from awareness of the breach | Data protection authority |
| DORA Art 19 | ICT risk function of the financial entity | Initial, intermediate, final per the RTS | Financial competent authority |

The cell shares one fact base and one UTC timeline, and each owner files separately. The Digital Omnibus proposal (COM(2025) 837) would let a CRA severe-incident report satisfy NIS2 Art 23(4) and would move GDPR to 96 hours. Both remain proposals, with trilogues not started as of 30 Oct 2026, so the cell plans for cumulative filing.

### Customer and user communication governance

Art 14(8) requires the manufacturer to inform impacted users, and where appropriate all users, in a timely manner (no fixed deadline), "where appropriate, in a structured, machine-readable format". Guidance paras 219-221 make the duty risk-based: detailed disclosure may be limited to affected customers until a fix exists, with broader disclosure once mitigated. If the manufacturer is not timely, the CSIRTs may inform users themselves.

| Decision | Owner | Rule |
|---|---|---|
| Who is told first | PSIRT lead with product management | Affected customers with mitigations before public disclosure; wider notice once mitigated |
| Wording | Legal with communications | Pre-approved templates, human-readable and machine-readable; CSAF is the obvious format but no primary source names one |
| Channels | Support and sales leadership | Named customer contacts, in-product notices, advisory page, security.txt pointers |
| Timing relative to filings | PSIRT lead | User notice is not gated on the SRP filing, and the SRP filing is not gated on the user notice |
| Record | PSIRT | Who was told, when, through which channel, with the message text |

Support and sales staff need a script: what has happened, what to do, where the advisory is, and what not to speculate about. Section 9 covers their training.

### Drills twice a year

Run two tabletop exercises a year: one actively exploited vulnerability in a third-party component, one severe incident affecting an update channel or signing key. Never submit synthetic reports to the live SRP; there is no sandbox (ENISA SRP FAQ). Rehearse on paper against the glossary field names.

Each drill tests awareness declared by a deputy at a weekend, platform access by a Secondary Assigned Representative and an unresponsive supplier. It also tests the multi-regime cell, user-notification wording and the UTC timeline. Record the results against the 24-hour and 72-hour targets as a KPI (Section 11) and feed lessons into the runbook within a month.

### Records

- UTC timestamps for first signal, organisational awareness, internal escalation and each SRP submission. The glossary's mandatory "date and time became aware" field must match the case file.
- A decision log entry for every awareness declaration and every "not reportable" decision, naming the criterion and the decider.
- The internal case file as the authoritative record; the SRP is a submission surface whose drafts live in one person's account.
- Submission receipts and notification identifiers, retained with the technical documentation for 10 years or the support period (Art 13(13)).
- Patch-availability dates tracked internally, because the actively-exploited-vulnerability final report has no SRP counter.
- User-notification records under Art 14(8).
- Drill records and lessons learned.

### Reporting governance checklist

- [ ] PSIRT and infrastructure CSIRT defined as separate roles with separate mailboxes and keys
- [ ] Awareness authority, deputy chain and written criteria in the runbook; no approval step before the early warning
- [ ] Legal review placed on the 72-hour and final reports only
- [ ] At least two Assigned Representatives registered with EU Login, MFA and backup devices; roster and offboarding rule in force
- [ ] Coordinator CSIRT decision record signed before any incident, per manufacturer entity
- [ ] Multi-regime cell membership and clocks documented
- [ ] User-notification templates pre-approved, human-readable and machine-readable
- [ ] Two drills scheduled for the year with results feeding the KPIs
