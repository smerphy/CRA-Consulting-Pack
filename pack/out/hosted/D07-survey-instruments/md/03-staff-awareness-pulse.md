# Staff awareness pulse survey

Fifteen questions in about six minutes test whether staff know the CRA duties that already apply, starting with Article 14 reporting, live since 11 Sep 2026. Knowledge items carry a marked answer key; results are cut by role and set against published benchmarks from Bitkom (29%) and the Linux Foundation (56%).

## Survey design

A census of all 3,800 employees, fielded 23 Nov – 4 Dec 2026 with results reported on 11 Dec 2026, sets the baseline that the \[Mar 2027\] and \[Oct 2027\] waves measure against.

| Item | Design |
| --- | --- |
| Purpose | Baseline what staff know and believe about the CRA duties that touch their role; repeat to measure whether training and communications land |
| Audience | All employees, reported by eight role groups and four business units |
| Sampling | Census. At least 349 completes overall and 272 of the 920 engineers give ±5 points at 95% confidence. Groups under 10 responses, such as PSIRT, are merged or reported as counts |
| Timing | Baseline fieldwork 23 Nov – 4 Dec 2026, results reported 11 Dec 2026; repeat waves in \[Mar 2027\] and \[Oct 2027\] with the same question IDs |
| Length | 15 questions, about 6 minutes; one question per screen on mobile |
| Languages | English and German; knowledge items back-translated before launch |
| Distribution | Anonymous link by email and intranet; reminders on days 4 and 8; managers see response rates by BU only |
| Data protection | No name, email address, IP address or device ID stored; reporting cells of 10 or more; works council sign-off before launch (tab 1, Data handling) |
| Answer key | Published on the intranet when each wave closes, so the pulse also teaches without leaking answers mid-wave |

## Survey text

Paste the introduction as the form description, then the questions in order. ✓ marks the correct answer: remove it before launch, or set it as the answer key in quiz mode. Show knowledge options in random order, with "Don't know" always last. Basis lines are for the answer key and trainers, not respondents.

**Introduction screen**

> **CRA awareness pulse: 6 minutes, anonymous.** The EU Cyber Resilience Act (CRA) sets security rules for products like ours, and some of them already apply. This short survey shows us what we need to explain better. It is anonymous: we do not record your name, email address or device, and we report only groups of 10 people or more. Results are never used to assess individuals. Please answer from what you know today, without looking anything up; "Don't know" is a useful answer. The answers will be published on the intranet when the survey closes on \[date\]. Questions: \[contact\].

### About you (required)

**PUL-01** Which best describes your role? *Single choice.*

- Executive or senior leader
- Engineering (software, firmware, hardware, test or DevOps)
- PSIRT or security operations
- Product management
- Quality and regulatory
- Procurement or legal
- Sales, key accounts or customer support
- Other role

**PUL-02** Which business unit do you work in? *Single choice.*

- Home & Building Solutions
- Industrial Connectivity
- Software & Services
- Group functions

### Your understanding (required)

Asked before the knowledge items so that the test does not colour the self-rating. Scale: Strongly disagree, Disagree, Neither agree nor disagree, Agree, Strongly agree, Don't know / not applicable.

**PUL-03** I know what the CRA means for my day-to-day work.

### What you know (required; single choice)

**PUL-04** Since when has Example Group had to report actively exploited vulnerabilities in its products under the CRA?

- Since 11 Sep 2026 ✓
- From 11 Dec 2027
- Only once a product carries CE marking under the CRA
- Don't know

*Basis: Art 14 applies from 11 Sep 2026, including to products placed on the market earlier (Art 71(2); Art 69(3)).*

**PUL-05** Under the CRA, when is a vulnerability "actively exploited"?

- When there is reliable evidence that an attacker has exploited it in a system without the owner's permission ✓
- When it has a severity score (CVSS) of 9.0 or higher
- When a security researcher reports it to us
- When proof-of-concept exploit code has been published
- Don't know

*Basis: Art 3(42). A good-faith research finding without evidence of exploitation is not reportable (Commission FAQ v1.4, 5.2 and 5.4).*

**PUL-06** When does the 24-hour deadline for the early warning start?

- When we become aware with a reasonable degree of certainty, after an immediate assessment ✓
- When the first report or alert arrives
- When a fix is available
- When the legal team approves the notification
- Don't know

*Basis: guidance C(2026) 5252 para 213; suspicion starts triage, not the clock.*

**PUL-07** Who decides that Example Group is aware of an actively exploited vulnerability, and files the early warning?

- The PSIRT lead or a named deputy, without prior approval ✓
- The General Counsel, after legal review
- The CISO
- The product's engineering lead
- Don't know

*Basis: Project Rampart PSIRT runbook rule; legal reviews the 72-hour and final reports, not the early warning.*

**PUL-08** A customer tells you they may have found a security flaw in one of our products. What should you do first?

- Pass it to PSIRT straight away through the published vulnerability contact ✓
- Log it in the product team's bug tracker
- Ask the customer for proof before passing it on
- Wait until the flaw is confirmed, then tell your manager
- Don't know

*Basis: Annex I Part II(5) and (6); support and sales route vulnerability reports to PSIRT within the hour.*

**PUL-09** Must Example Group publish the software bill of materials (SBOM) for its products?

- No; the SBOM belongs in the technical documentation and need not be public ✓
- Yes, on each product's web page
- Yes, but only for Class I and Class II products
- Don't know

*Basis: Annex I Part II(1); Recital 77; Annex II point 9 makes user access optional.*

**PUL-10** What is the minimum support period for a product under the CRA?

- Five years, unless the product is expected to be in use for less ✓
- Two years
- Ten years for every product
- There is no minimum
- Don't know

*Basis: Art 13(8). Five years is a floor, not a default; the period must reflect the expected time in use.*

**PUL-11** What is the highest fine for breaching the CRA's essential requirements or reporting obligations?

- EUR 15m or 2.5% of worldwide annual turnover, whichever is higher ✓
- EUR 20m or 4% of worldwide annual turnover, whichever is higher
- EUR 1m
- There are no fines, only product withdrawal
- Don't know

*Basis: Art 64(2). For Example Group the ceiling is EUR 30m (2.5% of EUR 1.2bn).*

### Your view (required)

Same scale as PUL-03.

**PUL-12** I would know what to do in the first hour if I suspected that a vulnerability in one of our products was being exploited.

**PUL-13** I have the time I need to apply CRA requirements in my work.

**PUL-14** In my area, product security work gets the same priority as feature work.

### Anything else (optional)

**PUL-15** What one thing would most help you meet CRA requirements in your role? *Open text, up to 500 characters. Helper text: "Please do not include names or details of unfixed vulnerabilities."*

**Completion screen**

> Thank you. The answers will be published on the intranet on \[date\]. To report a suspected vulnerability in one of our products now, use \[PSIRT contact\].

## Scoring

Tested knowledge is the headline measure, because self-ratings alone overstate readiness; the gap between the two is itself a finding.

| Measure | Definition | Benchmark or reference |
| --- | --- | --- |
| Knowledge index | Share of the eight knowledge items (PUL-04 to PUL-11) answered correctly, averaged across respondents; "Don't know" counts as not correct | Role targets below |
| Essentials score | Share of respondents answering both PUL-04 (reporting already applies) and PUL-08 (where to send a report) correctly | Role targets below |
| Confidence index | % favourable (agree or strongly agree) across PUL-03 and PUL-12 to PUL-14; "Don't know / not applicable" excluded from the base and shown separately | Trend between waves |
| Self-rated understanding | % agree or strongly agree on PUL-03 | Bitkom: 29% of German companies know what the CRA means for them (RD01) |
| Penalty awareness gap | % not answering PUL-11 correctly (wrong or "Don't know") among respondents who agree with PUL-03, the closest match to the Linux Foundation's CRA-aware base | Linux Foundation: 56% of CRA-aware respondents unaware of penalties (404 CRA-aware respondents of 843 surveyed; RD02) |
| Reporting readiness | % favourable on PUL-12, PSIRT and engineering respondents only | First drill filed the early warning in 9h 40m (K05) |
| Understanding gap | PUL-03 % agree minus the knowledge index, by role | A large positive gap flags overconfidence |

Bitkom surveyed companies (1,003 German firms with 10 or more employees, Apr–Jun 2026) and the Linux Foundation's 56% rests on 404 CRA-aware respondents out of 843 surveyed (2026); the pulse surveys individuals inside one company already running a CRA programme. Read each comparison as "are we ahead of the published baseline?", not as a statistical test.

- **Reporting.** By role group and BU, cells of 10 or more: knowledge index, essentials score, confidence index, % correct per knowledge item, and both benchmarks, each with its base and 95% confidence interval.
- **Item analysis.** Any knowledge item answered correctly by fewer than 50% of a role group becomes a targeted message to that group within two weeks.
- **Free text.** PUL-15 is coded into six themes (training, templates, tooling, time, clarity of ownership, other) and counted by role; quotes are used only after names and vulnerability details are removed.

## Targets by role

Targets rise with how directly a role touches the CRA; they are proposed for adoption by the programme board once the baseline is reported on 11 Dec 2026.

| Role group | Knowledge index, \[Mar 2027\] wave | Knowledge index, \[Oct 2027\] wave | Essentials score, \[Mar 2027\] wave |
| --- | --- | --- | --- |
| PSIRT or security operations | 90% | 100% | 100% |
| Executive or senior leader | 75% | 90% | 100% |
| Quality and regulatory | 75% | 90% | 95% |
| Engineering | 70% | 85% | 95% |
| Product management | 70% | 85% | 95% |
| Procurement or legal | 70% | 85% | 95% |
| Sales, key accounts or customer support | 60% | 75% | 95% |
| Other role | 50% | 60% | 80% |

All targets are minimums. Reporting readiness (PUL-12 favourable) should reach at least 95% for PSIRT and 80% for engineering by the \[Mar 2027\] wave.

- **Training.** Results steer the WS8 plan and its role-by-content matrix. K10 counts engineers trained (140 of 920, target 60% by Mar 2027); the pulse shows whether that training landed.
- **Communications.** The measurement section of the Communication Pack (D05) uses these targets and the item analysis above.
- **Article 14.** PUL-12 below target for PSIRT or engineering triggers a runbook briefing before the second Article 14 drill (M9, 16 Apr 2027).
- **KPI pack.** The knowledge index for PSIRT, engineering and product management is proposed as an addition to the KPI pack; it is not yet adopted.

*Project Rampart · Survey and Interview Instruments (D07) · Illustrative · 31 Oct 2026*
