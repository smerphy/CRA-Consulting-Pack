## 10. Product-level reporting runbook

The product team's job in an Art 14 case is to supply the facts fast enough for a filing within 24 hours. The clocks, the Single Reporting Platform, the registration steps and the fallbacks are in Reporting obligations (Article 14). This section lists what the product team contributes, in the form the ENISA [SRP glossary](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2) fields need.

Art 14 has applied since 11 Sep 2026 to every in-scope product, including products no longer sold or past support (Art 69(3); para 210). The reportable inventory therefore includes every version in the field.

### Awareness decision inputs

Awareness arrives when, after an immediate initial assessment, the manufacturer has "a reasonable degree of certainty" of exploitation or a severe incident. The source is guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) para 213. The product team owns most of the inputs to that assessment and must deliver them within hours.

| Input | Product-team source | What to hand over |
|---|---|---|
| Product telemetry | Crash reports, authentication-failure spikes, anomalous update or command traffic, integrity-event logs (Annex I items 2(d), 2(f), 2(l)) | Timeline of anomalous events in UTC; affected versions; whether evidence shows exploitation or only vulnerability |
| Honeypots and canaries | Exposed decoy units or endpoints for the product class | Capture of exploitation attempts; indicators; whether the attack path works against shipped versions |
| Customer and partner reports | Support tickets, integrator escalations, PSIRT intake (section 8) | Reproduction status; affected configurations; exploitation evidence quality |
| Third-party intelligence | CSIRT or ENISA notices, researcher contact, vendor advisories, KEV additions for a component, media reporting | Reachability analysis for component findings; whether the exploited path exists in the product |
| Internal findings | Test results, scanner hits, bug-bounty submissions | Marked "no exploitation evidence" unless telemetry says otherwise; these are not actively exploited vulnerabilities on their own ([Commission FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307) section 5) |

The PSIRT case file (section 8) records each input with its UTC time. The incident commander declares awareness; monitoring these channels is good practice, not itself mandated.

### Product data every notification needs

Keep a current product data pack per product family so the notification owner never has to ask engineering for basics under the clock.

| Field (glossary name where applicable) | Content | Owner |
|---|---|---|
| Product name and version | Commercial name, model, firmware and app versions affected; version-support status | Release engineering |
| Product type, class and category | From the product definition record (section 2); "default" if no Annex III or IV match | Compliance lead |
| Affected configurations | Hardware revisions, feature flags, deployment modes, RDPS dependencies affected | Product security |
| Component name | Upstream component and version where the vulnerability sits; VEX status | SBOM owner |
| Member States where available | Current distribution map per product, maintained from sales and app-store data; drives dissemination under Art 16(2) | Product management |
| End-of-support indicator | Whether any affected version is past its declared end date | Product management |
| Mitigating measure expected shortly; user action able to reduce impact | Yes or no, and the interim guidance text | Remediation lead |
| CVE ID and EUVD ID | Only once assigned; a CVE record is not a notification | PSIRT |
| Date and time became aware | UTC, from the case file; estimates labelled | Incident commander |
| Attack vector | Network, adjacent, local, physical, with the reachability note | Product security |

A stale distribution map is the most common blocker to a 24-hour filing. The "Member States where product available" field is required at early warning.

### Content by stage

| Stage | Product team supplies | Glossary fields served |
|---|---|---|
| Early warning (24 h) | Title and summary; product name and version; Member States; awareness time in UTC; for incidents, whether malicious or unlawful acts are suspected | Type, Title, Summary, Product name and version, Member States, Date/time became aware, Incident suspected of unlawful or malicious acts |
| 72-hour notification | General information on the vulnerability and exploit, or the incident and initial assessment; corrective or mitigating measures taken; measures users can take; sensitivity view; attack vector; whether to request limited dissemination | General information, Initial assessment, Corrective or mitigating measures taken, Corrective or mitigating measures users can take, Considered sensitivity, Attack vector, PEC indicator |
| Final report (14 days after a fix for vulnerabilities; 1 month after the 72-hour report for incidents) | Severity rating, classification and rationale; impact description; malicious actor if known, else "unknown"; details of the security update; date the measure became available; root cause for incidents | Description of severity and impact, Malicious actor, Details of the security update, Date corrective measure became available, Type of threat or root cause, Applied and ongoing mitigation |

No severity scale is prescribed; supply the CVSS vector and a plain-language rationale. Track the date a fix became available internally, because the vulnerability final report has no platform counter.

### User notification (Art 14(8))

After awareness the manufacturer informs impacted users and, where appropriate, all users without undue delay, including mitigating measures, "where appropriate" in a machine-readable format. Guidance paras 219-221 make this proportionate: affected customers may receive detail before a fix exists and the wider public once mitigated. The product team prepares both forms.

- Human-readable: in-product notice, app notification or email with the interim action, the fix version and the advisory link. The same text travels with the update as its advisory message (section 7).
- Machine-readable: a CSAF advisory, with a VEX "under_investigation" or "known_affected" status until the fix, then the final advisory with fixed versions (section 8). CSAF is the obvious candidate and appears in no primary source as a required format.
- Channel list per product: which users can be reached directly, which only through distributors or integrators, and which only through the public page. A CSIRT may inform users if the manufacturer is not timely.

### Link to the PSIRT case

One identifier binds the case file, the VEX and CSAF documents, the SRP notification reference, the user notices and the fixing release. Record the SRP notification ID in the case once filed. The platform stores drafts only in the individual filer's account, so the case file is the authoritative record.

After the final report, file the post-incident review against the case and update the risk assessment rows affected (section 3).

### Timeline from first signal to final report

| Step | Owner | Target | Output |
|---|---|---|---|
| 1 First signal logged | PSIRT on-call | Within 1 hour of receipt | Case opened; UTC first-signal time |
| 2 Initial assessment | Product security analyst with incident commander | Immediately; hours, not days | Reachability, exploitation evidence, severity; awareness declared or not, with UTC time |
| 3 Product data pack checked | Release engineering and product management | Within 4 hours of awareness | Versions, configurations, Member States, support status confirmed |
| 4 Early warning drafted and filed | Notification owner (24 h) with incident commander | Within 24 hours of awareness | SRP notification ID recorded in the case |
| 5 User interim notice | Remediation lead with communications | Without undue delay; affected customers first | Interim guidance, human-readable and CSAF |
| 6 72-hour notification | Notification owner (72 h) with legal review | Within 72 hours of awareness | General information, measures, sensitivity view |
| 7 Fix built, tested and released | Remediation lead; release engineering | Per severity SLA; security-only release | Signed update; gate record; CSAF final advisory |
| 8 Final report | Notification owner (final) | 14 days after the fix is available (vulnerability); 1 month after step 6 (incident) | Severity, impact, actor, update details |
| 9 Post-incident review | PSIRT lead; product security | Within 2 weeks of the final report | Case closed; risk assessment and test plan updated; drill lessons |

Treat the 24-hour and 72-hour deadlines as both running from awareness, not consecutively; remediation never pauses the clock. Two paper exercises a year, one vulnerability and one incident, keep the data pack and the roles honest. Never submit synthetic reports to the live platform.

The product data pack and case-file links are the product team's contribution to checklist 5, reporting, in the Requirement checklists tab.
