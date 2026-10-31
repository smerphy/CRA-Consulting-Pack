# Executive and stakeholder interview guide

A 45-minute semi-structured interview with nine executives, held before the 19 Nov 2026 board, tests where leaders agree and differ on exposure, product-risk appetite, roadmap trade-offs, notified bodies, legacy lines, reporting authority and budget.

## Design

Nine 45-minute interviews between 2 and 10 Nov 2026 give the executive sponsor a map of executive stances the day before the board pre-read.

| Item | Design |
| --- | --- |
| Purpose | Surface agreement and disagreement among executives before the board takes decisions BD1 to BD5 on 19 Nov 2026 |
| Core interviewees (9) | CTO (proposed accountable executive, BD2), CFO, General Counsel, the BU presidents of Home & Building Solutions, Industrial Connectivity and Software & Services, CISO, Head of quality & regulatory, Head of procurement |
| Optional (4) | CEO (a 20-minute version: questions 1, 6, 9 and 12), PSIRT lead, Head of platform engineering, Head of customer operations |
| Timing | 2–10 Nov 2026; synthesis on 11 Nov, the day before the board pre-read |
| Format | 45 minutes, semi-structured, in person or by video; a lead interviewer and a note-taker from the programme team or \[Advisor\] |
| Running order | Opening and consent, 3 min; must-ask questions, 30 min; role probes, 9 min; closing, 3 min |
| Preparation | Send the CRA on a page (D04) 48 hours ahead; read the interviewee's workstream status and risks beforehand |
| Recording | Notes only; audio only with explicit consent, deleted once the synthesis is accepted |
| Data protection | Themes reported by role, never by name; quotes used only with permission (tab 1, Data handling) |

## Opening script and consent line

Read or paraphrase the opening; read the consent line word for word and record the answer.

> "Thank you for your time. Project Rampart is preparing Example Group to keep selling in the EU when the Cyber Resilience Act applies in full on 11 Dec 2027; its reporting duties have applied since 11 Sep 2026. Before the board meets on 19 Nov, we are hearing from nine executives about the exposure, the trade-offs and the decisions ahead. There are no right answers. We want your view, including where you disagree with the programme."

**Consent line**

> "We take notes, not recordings. We report themes by role, never by name. If we would like to quote you, we will ask first. You can skip any question or stop at any time. Are you happy to go ahead on that basis?"

Record: consent (yes or no), quote permission (none, ask each time, or general), date and start time.

## Core questions

Twelve open questions cover the decisions in front of the board. Each role answers its must-ask set; questions 2 and 12 go to everyone, so confidence and the priority decision can be compared across all nine interviews.

| # | Theme | Question | Follow-up prompt |
| --- | --- | --- | --- |
| 1 | Exposure | Which parts of your business would be hit first if a product could not be placed on the EU market after 11 Dec 2027? | Which products, customers and revenue? |
| 2 | Readiness | On a scale of 1 (not at all) to 5 (fully), how confident are you that your products will carry a valid EU declaration of conformity by 11 Dec 2027? | What would move your score by one point? |
| 3 | Risk decisions | When a product security risk cannot be fully fixed before a release, who decides today, and on what basis? | Can you give a recent example? |
| 4 | Product-risk rule | The proposed rule (BD4) says cost, risk appetite and commercial strategy are not grounds to leave a product risk unaddressed. Where would it change a decision in your area? | What appeal route would you need? |
| 5 | Roadmap | The plan needs about 26 engineering FTE-years of remediation in 2027. What would you change in the roadmap to make room? | Which items would you protect? |
| 6 | Notified bodies | Seven of thirteen families, with EUR 468m of EU revenue, need a notified body, and none was verifiably designated at checks to 8 Sep 2026. How should we balance booking candidate bodies early against waiting for designations? | What evidence would make you commit? |
| 7 | Legacy lines | Which product lines would you rather withdraw from EU sale than bring into compliance, and why? | What would customers need from us if we did? |
| 8 | Reporting authority | The PSIRT lead or a named deputy may file an Article 14 early warning without prior approval. What concerns, if any, does that raise for you? | What would you want to be told, and when? |
| 9 | Budget | The base case is EUR 9.3m one-off to Dec 2027 and EUR 1.8m a year to run. Which parts would you challenge? | What would a cheaper option give up? |
| 10 | Accountability | What should the signatory of an EU declaration of conformity see before signing? | Who should hold that authority, and who deputises? |
| 11 | Market signals | What are customers, partners or regulators already asking you about the CRA? | What did we answer, and who answered? |
| 12 | Priority | What is the one decision the board must take on 19 Nov 2026 for this programme to succeed? | What happens if it slips by a quarter? |

| Role | Must-ask questions |
| --- | --- |
| CTO | 1, 2, 3, 4, 5, 8, 10, 12 |
| CFO | 1, 2, 4, 6, 9, 12 |
| General Counsel | 1, 2, 3, 4, 8, 10, 12 |
| BU presidents (each) | 1, 2, 4, 5, 6, 7, 11, 12 |
| CISO | 2, 3, 4, 8, 11, 12 |
| Head of quality & regulatory | 1, 2, 6, 7, 10, 12 |
| Head of procurement | 2, 3, 6, 9, 12 |

Facts quoted in questions 5, 6 and 9 are stated, not argued: if the interviewee disputes one, record the challenge as a finding.

## Role-specific probes

Each probe is a single question for the time left after the must-ask set; the facts quoted are as at 30 Oct 2026.

**CTO**

- What would it take to enforce the release security gate on every release, not only design it?
- How will you protect the 26.2 FTE-years of remediation from the 2027 roadmap?
- Signed SBOMs cover 9 of the last 24 releases (38%). What blocks the rest?
- Which update-infrastructure change, HSM signing or anti-rollback, worries you most before 30 Jun 2027?

**General Counsel**

- What do you need from the legal opinion on EG-700 and HomeHub H3, due 27 Nov 2026, to stand behind their classification?
- What should the DoC signing instrument say to limit personal and corporate exposure?
- From 9 Dec 2026, claimants under the Product Liability Directive can seek disclosure of technical files and update logs. How should that change the way we write records?
- In which markets do we need an authorised representative, an importer briefing or a marketplace arrangement? Q10.4 is the weakest statement in the baseline, at 0.08.

**CFO**

- How should the EUR 1.42m planned for Q4 2026 and EUR 7.83m for 2027 be phased against the budget cycle?
- Is a 15% contingency right for a programme with an external dependency on notified bodies?
- Which part of the EUR 1.84m annual run cost should sit with the BUs rather than the centre?
- Should remediation spend be treated as operating cost or capitalised development?
- What should our product-liability and cyber insurers hear before renewal?

**BU presidents**

- Which SKUs carry the revenue that notified-body slots must protect first?
- HBS: L2 Smart Lock (35%) and V1 Video Doorbell (38%) are the least ready families, and both need Module B+C. What would help them most?
- IC: IR-300 and IS-200 are still sold. What would withdrawal from EU sale before 11 Dec 2027 mean for your customers (BD5)?
- S&S: FleetView is Class I, and the cloud platform is remote data processing for several products. Who owns their CRA evidence?
- Which support-period commitments already sit in customer contracts?

**CISO**

- Where should the line sit between the product PSIRT and the infrastructure CSIRT, and who leads an incident that starts CRA, NIS2 and GDPR clocks at once?
- Two people hold most PSIRT knowledge (R08). What would make 24/7 on-call sustainable?
- The first drill filed an early warning in 9h 40m but could not complete the Member State field for two products (issue I01). What else did it show?
- Is a roster of three SRP Assigned Representatives enough?

**Head of quality & regulatory**

- SteerCo endorsed Module H for Industrial Connectivity and FleetView on 30 Oct 2026 (SD1). What must the quality system add to pass?
- What is your preferred route for V1 and L2, and what decides it?
- How much of the 2025 EN 18031 assessment work can the CRA files reuse, given that the RED cybersecurity delegated act is repealed with effect from 11 Dec 2027?
- What conversion options should the pre-assessment contracts carry if a candidate body is designated late?

**Head of procurement**

- Six of the 41 in-scope suppliers are on CRA clauses. Which of the top 15 will push back hardest, and why?
- Which components have no realistic alternative supplier?
- Who should approve an exit plan when a supplier refuses the clause pack?
- How will the clause pack fit the renewal dates of master agreements?

## Closing script

Close on time and leave the interviewee clear about what happens to their answers.

1. "Is there anything I should have asked and did not?"
2. "Who else should we speak to?"
3. Confirm permission for each quote noted verbatim.
4. "We will share the themes with the executive sponsor by 11 Nov, by role and without names. Thank you."

Within 24 hours the note-taker completes the per-interview record below, and the lead interviewer checks it.

## Synthesis template

The synthesis turns nine conversations into stances by theme, mapped to the board decisions and the risk register.

**Per-interview record**

| Field | Entry |
| --- | --- |
| Interview ID and role | INT-\[nn\], \[role\] |
| Date and interviewers | \[date\]; \[lead\], \[note-taker\] |
| Consent and quote permission | \[yes or no\]; \[none, ask each time, general\] |
| Confidence score, question 2 (1 to 5) | \[ \] |
| Themes raised (codes below) | \[ \] |
| Quotes, verbatim and permitted | \[ \] |
| Decisions implied (BD1 to BD5, other) | \[ \] |
| Risks raised (R01 to R10, or new) | \[ \] |
| Disagreements with the programme's position | \[ \] |
| Follow-ups, with owner and date | \[ \] |

**Codebook**

| Code | Theme | Typical signals |
| --- | --- | --- |
| T1 | Market access and notified bodies | Route choice, capacity, timing, conversion options |
| T2 | Engineering capacity and roadmap | FTE ring-fence, deferred features, contractors |
| T3 | Accountability and signing | DoC signatory, release-blocking authority |
| T4 | Product-risk acceptance | Cost-based exceptions, appeal route |
| T5 | Reporting and PSIRT | Awareness authority, on-call, drills |
| T6 | Supply chain | Supplier pushback, SBOM delivery, exit plans |
| T7 | Legacy lines | Withdrawal, migration, customer impact |
| T8 | Budget and value | Envelope, contingency, run cost, pricing |
| T9 | Customers and channel | Evidence requests, contract clauses, trust |
| T10 | People and works council | Training time, on-call allowances, monitoring |

**Cross-interview matrix**

Each cell records one interviewee's stance on the theme: S supports the programme's position, M mixed, O opposes, blank if not raised. GC is the General Counsel; HBS, IC and S&S the BU presidents; Q&R the Head of quality & regulatory; Proc. the Head of procurement.

| Theme | CTO | CFO | GC | HBS | IC | S&S | CISO | Q&R | Proc. | Read-out |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| T1 Market access |  |  |  |  |  |  |  |  |  |  |
| T2 Capacity and roadmap |  |  |  |  |  |  |  |  |  |  |
| T3 Accountability |  |  |  |  |  |  |  |  |  |  |
| T4 Product-risk acceptance |  |  |  |  |  |  |  |  |  |  |
| T5 Reporting and PSIRT |  |  |  |  |  |  |  |  |  |  |
| T6 Supply chain |  |  |  |  |  |  |  |  |  |  |
| T7 Legacy lines |  |  |  |  |  |  |  |  |  |  |
| T8 Budget and value |  |  |  |  |  |  |  |  |  |  |
| T9 Customers and channel |  |  |  |  |  |  |  |  |  |  |
| T10 People and works council |  |  |  |  |  |  |  |  |  |  |

A theme reads as consensus when seven or more of the nine share a stance, and as a split when three or more oppose. Every split goes to the executive sponsor with the quotes behind it; decisions implied are framed as options for BD1 to BD5, not recommendations; new risks reach their owners within a week.

*Project Rampart · Survey and Interview Instruments (D07) · Illustrative · 31 Oct 2026*
