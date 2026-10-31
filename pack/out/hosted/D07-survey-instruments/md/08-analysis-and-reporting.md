# Analysis and reporting templates

The illustrative baseline of 28 Oct 2026 puts portfolio readiness at 44%: Article 14 reporting is the strongest domain at 72% and conformity and market access the weakest at 16%. This tab sets how each instrument is aggregated, shows the output tables filled with that baseline, and defines the RAG thresholds and the route into the KPI pack.

## Aggregation rules

Each instrument rolls up to one headline measure, with a minimum base below which nothing is reported.

| Instrument | Unit | Headline measure | Aggregation | Minimum base | Cadence |
| --- | --- | --- | --- | --- | --- |
| DIA | Product family | Readiness index | Mean of min(score, 3) ÷ 3 over 40 statements; portfolio, BU and class indices are unweighted means of family indices | All 40 statements scored | Monthly update; quarterly moderation |
| PUL | Respondent | Knowledge index | Mean share correct over PUL-04 to PUL-11; "Don't know" is not correct | 10 per reported cell | 23 Nov – 4 Dec 2026 (reported 11 Dec); \[Mar 2027\]; \[Oct 2027\] |
| SUP | Supplier and component | Score and route | Points ÷ applicable maximum; must-pass items judged separately; route by tier | Every in-scope supplier | Wave 1 Dec 2026; wave 2 Jan 2027; then at renewal |
| INT | Interview | Stance by theme | Count of S, M and O stances per theme across the nine core interviews | 9 core interviews | Nov 2026; follow-ups as needed |
| CUS | Respondent organisation | Evidence demand | % of respondents requesting each item, by segment | 5 per reported segment | Dec 2026 |
| ENG | Release train | Practice score | Points ÷ applicable maximum over ENG-05 to ENG-14 | Every release train | Nov 2026; repeat Jun 2027 |

## Output 1: portfolio summary and domain readiness

Portfolio readiness is 44%, Amber and on plan at baseline, but four of ten domains are red and only 21 of 520 family scores (4%) reach level 3. Illustrative baseline of 28 Oct 2026 covering all 13 families, self-assessed by product teams and moderated by the programme.

| Measure | Value | RAG |
| --- | --- | --- |
| Portfolio readiness index (K01) | 44% | Amber |
| Strongest domain | Art 14 reporting, 72% | Amber |
| Weakest domain | Conformity & access, 16% | Red |
| By business unit | HBS 39%; IC 52%; S&S 41% | Red; Amber; Amber |
| By class | Default 42%; Class I 45%; Class II 54% | Amber; Amber; Amber |

Outside SRP registration (Q8.1, level 3 for every family), level 3 appears only in the secure development of four Industrial Connectivity families, where the IEC 62443-4-1 process already produces records: IR-500 (Q4.1, Q4.2), IS-300 (Q4.1, Q4.3), SG-900 (Q4.1, Q4.3, Q6.2) and SecureLink (Q4.1). Class I home products are least ready: L2 at 35% and V1 at 38%.

| Domain | Average level (0–4) | Readiness index | Gap to level 3 | Weakest statement (average level) | RAG |
| --- | --- | --- | --- | --- | --- |
| D1 Governance | 1.75 | 58% | 1.25 | Q1.3 (1.00) | Amber |
| D2 Scope & class | 1.35 | 45% | 1.65 | Q2.4 (0.92) | Amber |
| D3 Risk & design | 1.40 | 47% | 1.60 | Q3.2 (1.08) | Amber |
| D4 SDLC & testing | 1.67 | 56% | 1.33 | Q4.4 (1.23) | Amber |
| D5 SBOM & supply chain | 1.13 | 38% | 1.87 | Q5.3 (0.92) | Red |
| D6 Vulnerability handling | 1.15 | 38% | 1.85 | Q6.4 (0.69) | Red |
| D7 Updates & support | 1.44 | 48% | 1.56 | Q7.3 (1.23) | Amber |
| D8 Art 14 reporting | 2.15 | 72% | 0.85 | Q8.4 (1.62) | Amber; target 100% now |
| D9 Documentation & DoC | 0.73 | 24% | 2.27 | Q9.1 (0.46) | Red |
| D10 Conformity & access | 0.48 | 16% | 2.52 | Q10.4 (0.08) | Red |

Gap to level 3 is 3 minus the average level. RAG follows the thresholds below; D8 uses its own rule because reporting already applies.

Source: CRA Readiness Diagnostic, baseline 28 Oct 2026; Illustrative.

## Output 2: family heatmap

Conformity & access is the joint-lowest domain for 12 of 13 families, while Industrial Connectivity's IEC 62443-4-1 heritage shows in SDLC scores of 2.00 to 2.50. Families are sorted from least to most ready.

| Family | BU | Class | Gov | Scope | Risk | SDLC | SBOM | Vuln | Upd | Art 14 | Doc | Conf | Index |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| L2 Smart Lock | HBS | Class I | 1.75 | 1.00 | 1.25 | 1.00 | 0.50 | 0.75 | 1.50 | 2.00 | 0.50 | 0.25 | 35% |
| S-Series Room Sensors | HBS | Default | 1.75 | 1.00 | 1.25 | 1.00 | 0.50 | 0.75 | 2.00 | 2.00 | 0.50 | 0.50 | 38% |
| HomeHub H3 | HBS | Default (prov.) | 1.75 | 0.75 | 1.25 | 1.00 | 0.50 | 1.00 | 1.75 | 2.00 | 0.75 | 0.50 | 38% |
| V1 Video Doorbell | HBS | Class I | 1.75 | 1.25 | 1.50 | 1.00 | 1.00 | 0.50 | 1.75 | 2.00 | 0.50 | 0.25 | 38% |
| Example IoT SDK | S&S | Default | 1.75 | 1.00 | 0.75 | 1.50 | 2.00 | 0.75 | 0.50 | 2.25 | 0.75 | 0.25 | 38% |
| FleetView Device Manager | S&S | Class I | 1.75 | 1.75 | 1.00 | 1.75 | 1.25 | 0.75 | 1.00 | 2.25 | 0.50 | 0.25 | 41% |
| ConfigStudio | S&S | Default | 1.75 | 1.75 | 1.00 | 1.75 | 1.75 | 1.00 | 0.50 | 2.25 | 1.00 | 0.25 | 43% |
| T200 Smart Thermostat | HBS | Default | 1.75 | 1.50 | 2.00 | 1.00 | 1.25 | 0.50 | 1.75 | 2.00 | 1.00 | 1.00 | 46% |
| EG-700 Edge Gateway | IC | Default (prov.) | 1.75 | 1.50 | 1.75 | 2.00 | 1.00 | 1.75 | 1.75 | 2.25 | 0.50 | 0.50 | 49% |
| IR-500 Industrial Router | IC | Class I | 1.75 | 1.50 | 1.50 | 2.50 | 1.00 | 1.75 | 1.75 | 2.25 | 0.75 | 0.25 | 50% |
| IS-300 Managed Switch | IC | Class I | 1.75 | 1.75 | 1.50 | 2.50 | 1.25 | 1.75 | 1.50 | 2.25 | 1.00 | 0.50 | 52% |
| SecureLink Remote Access | IC | Class I | 1.75 | 1.50 | 1.50 | 2.25 | 1.50 | 1.75 | 1.75 | 2.25 | 0.75 | 0.75 | 52% |
| SG-900 Industrial Firewall/IDS | IC | Class II | 1.75 | 1.25 | 2.00 | 2.50 | 1.25 | 2.00 | 1.25 | 2.25 | 1.00 | 1.00 | 54% |
| **Portfolio average** |  |  | **1.75** | **1.35** | **1.40** | **1.67** | **1.13** | **1.15** | **1.44** | **2.15** | **0.73** | **0.48** | **44%** |

Cells show the average level per domain (0–4; target 3). Colour bands: red below 1.00, orange 1.00 to 1.99, yellow 2.00 to 2.99, green 3.00 and above; the number is always printed. Default (prov.) marks EG-700 and HomeHub H3, whose classification awaits the legal opinion due 27 Nov 2026.

Source: CRA Readiness Diagnostic, baseline 28 Oct 2026; Illustrative.

## Output 3: the ten weakest statements

Six of the ten weakest statements sit in documentation and conformity, and each already carries its action; Q10.4 averages 0.08, with 12 of 13 families at level 0.

| Rank | ID | Statement | Average level | Action |
| --- | --- | --- | --- | --- |
| 1 | Q10.4 | EU representation, importer and distributor duties and marketplace arrangements are settled for each market. | 0.08 | Confirm the role per market, appoint an authorised representative where useful and brief importers on their checks. |
| 2 | Q10.2 | Candidate notified bodies are shortlisted and a pre-assessment is contracted where the route needs one. | 0.38 | Shortlist three candidates, contract pre-assessments with conversion options, and check NANDO at every programme board. |
| 3 | Q10.3 | A complete Module A internal-control record is kept for the product, even where a notified body will be used. | 0.38 | Build the Module A record and evidence index now; it is the fallback and the body's application pack. |
| 4 | Q9.1 | An Annex VII technical file exists for each product version and is versioned with releases. | 0.46 | Adopt the 13-part file outline and generate version-linked contents from the release pipeline. |
| 5 | Q6.4 | Vulnerability case records are retained and response metrics are reported. | 0.69 | Report acknowledgement and fix times quarterly and retain case files for 10 years or the support period. |
| 6 | Q9.2 | Annex II user information, including the support end date and the vulnerability contact, is drafted and ready to publish. | 0.69 | Draft the Annex II document per product family and publish it at a stable, versioned URL. |
| 7 | Q9.4 | Evidence sits in a system of record with 10-year retention and can answer a reasoned request within 10 working days. | 0.77 | Select a system of record, compute retention per version and test an end-to-end reasoned-request export. |
| 8 | Q2.4 | The economic-operator role per market and the legacy status of each product line are recorded. | 0.92 | Record manufacturer, importer, distributor or representative per market; flag lines still sold after 11 Dec 2027. |
| 9 | Q5.3 | Supplier contracts require vulnerability notification, SBOM delivery and support-period commitments. | 0.92 | Add the CRA clause pack to master agreements, starting with suppliers of security-relevant components. |
| 10 | Q1.3 | A written product-risk acceptance rule excludes cost, risk appetite and commercial strategy as reasons to leave risk unaddressed. | 1.00 | Add a product-risk category to the enterprise risk framework with its own acceptance authority and a non-cost appeal route. |

Q6.3 and Q9.3 also average 1.00; ties are listed in question order.

Source: CRA Readiness Diagnostic, baseline 28 Oct 2026; Illustrative.

## Output shells for the other instruments

No fieldwork has run yet, so these shells carry structure only. The interview matrix sits in 5 · Executive interviews and the platform sizing matrix in 7 · Engineering practice survey.

**Staff awareness pulse, by role group**

| Role group | Responses (n) | Knowledge index | Essentials score | Confidence index | PUL-03 agree (Bitkom: 29%) | PUL-11 not correct among PUL-03 agreers (LF: 56% of CRA-aware) | Target, \[Mar 2027\] wave | RAG |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| PSIRT or security operations |  |  |  |  |  |  | 90% |  |
| Executive or senior leader |  |  |  |  |  |  | 75% |  |
| Quality and regulatory |  |  |  |  |  |  | 75% |  |
| Engineering |  |  |  |  |  |  | 70% |  |
| Product management |  |  |  |  |  |  | 70% |  |
| Procurement or legal |  |  |  |  |  |  | 70% |  |
| Sales, key accounts or customer support |  |  |  |  |  |  | 60% |  |
| Other role |  |  |  |  |  |  | 50% |  |
| All staff |  |  |  |  |  |  | Role targets |  |

**Supplier risk register**

| Supplier | Component | Tier | Score | Must-pass met | Route | Conditions and due date | Owner | Review date |
| --- | --- | --- | --- | --- | --- | --- | --- | --- |
| \[supplier\] | \[component\] |  | \[ \]% | \[yes or no\] |  | \[ \] | \[ \] | \[ \] |
| \[supplier\] | \[component\] |  | \[ \]% | \[yes or no\] |  | \[ \] | \[ \] | \[ \] |
| \[supplier\] | \[component\] |  | \[ \]% | \[yes or no\] |  | \[ \] | \[ \] | \[ \] |

**Customer evidence demand, by segment** (% of respondents requesting each item, base in brackets)

| Evidence item | All | OEM or integrator | Utility or operator | Installer | Distributor or importer | Retailer |
| --- | --- | --- | --- | --- | --- | --- |
| EU declaration of conformity |  |  |  |  |  |  |
| CE marking under the CRA |  |  |  |  |  |  |
| Support period end date |  |  |  |  |  |  |
| Security update policy |  |  |  |  |  |  |
| Vulnerability contact and disclosure policy |  |  |  |  |  |  |
| SBOM access |  |  |  |  |  |  |
| Machine-readable advisories (CSAF) |  |  |  |  |  |  |
| VEX statements |  |  |  |  |  |  |
| Annex II user information |  |  |  |  |  |  |
| Test reports or certificates |  |  |  |  |  |  |

## RAG thresholds

Readiness RAG combines an absolute band with a check against the plan, so a family can be amber on level and red on trajectory.

| Measure | Green | Amber | Red |
| --- | --- | --- | --- |
| Readiness index: family, domain, BU, class or portfolio | 70% or more, and at or above plan for the month | 40–69%, or 70% or more but below plan | Below 40%, or more than 10 points below plan |
| Art 14 reporting domain (D8), family or portfolio | Every D8 statement at level 3 or above | Average level 2.00 or above | Average level below 2.00 |
| Knowledge index by role (PUL) | At or above the role target | Up to 10 points below target | More than 10 points below target |
| Essentials score by role (PUL) | At or above the role target | Up to 5 points below target | More than 5 points below target |
| Supplier portfolio (SUP), Critical and High components | 90% or more approved, or conditioned with dates | 75–89% | Below 75%, or any Critical component on an exit plan without a funded alternative |
| Platform readiness (ENG), Wave 1 release trains | Every Wave 1 train scores 2 on ENG-05 and ENG-07 | Gaps remain, each with an onboarding date before 31 Mar 2027 | Any Wave 1 gap without an onboarding date |

The plan for the portfolio index runs from the 44% baseline to 46% in Nov 2026, 48% in Dec 2026, 58% in Mar 2027, 71% in Jun 2027, 83% in Sep 2027 and 91% in Nov 2027; monthly values sit in the KPI pack.

Applied to the baseline, the portfolio is Amber (44%, on plan) and HBS is Red (39%). Five families are Red: L2 Smart Lock, S-Series Room Sensors, HomeHub H3, V1 Video Doorbell and Example IoT SDK. Four domains are Red: SBOM & supply chain, Vulnerability handling, Documentation & DoC, and Conformity & access.

## How results update the KPI pack

Results enter the KPI pack through fixed routes, so no KPI moves without a named source; the research readout in the week of 14 Dec 2026 is the first full update.

| Result | KPI or register (value at 30 Oct 2026) | How it updates | When |
| --- | --- | --- | --- |
| DIA portfolio index | K01 Portfolio readiness index (44%) | Replaces the value; moderated quarterly | Monthly programme board |
| DIA Q2.3 | K02 Families with final scope and class decision (11 of 13) | Cross-checked against the scope register | Monthly |
| DIA Q10.1 and Q10.2 | K03 Class I/II families with route and notified-body plan (5 of 7); K12 notified-body candidates (3 shortlisted, 1 proposal) | Cross-checked against route decisions and contracts | Monthly |
| DIA domain D8 | K04 to K06, Article 14 readiness | Any D8 statement below level 3 opens an action; drill records stay the source for K05 | Monthly |
| ENG-05 to ENG-07 | K07 Releases with signed SBOM (38%) | Locates the gaps; the build pipeline stays the source of the value | Nov 2026; Jun 2027 |
| SUP routes | K09 In-scope suppliers on CRA clauses (6 of 41) | Approved and conditioned suppliers enter clause negotiation; exit plans are logged | Each wave |
| PUL | K10 Engineers trained (140 of 920); proposed knowledge-index KPI | The pulse shows whether training landed; K10 shows whether it was delivered | Each wave |
| INT | Risk register (R01 to R10); board decisions BD1 to BD5 | New risks reach owners within a week; stances go into the board pre-read | Nov 2026 |
| CUS | Customer FAQ; support-period records | Evidence demand sets FAQ content; CUS-09 feeds support-period determinations | Dec 2026 |
| All six | Programme RAG (Amber) | Research readout to the programme board, then the next SteerCo | Week of 14 Dec 2026 |

*Project Rampart · Survey and Interview Instruments (D07) · Illustrative · 31 Oct 2026*
