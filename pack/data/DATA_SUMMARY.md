# DATA SUMMARY — EU Cyber Resilience Act Readiness Programme (v1.0, 31 Oct 2026)

> Illustrative engagement — fictional client data; regulatory facts verified to 30 Oct 2026. Source of truth: `/home/claude/pack/data/pack_data.json`. Never invent client numbers — use these.

## Key numbers (use exactly)

- Days from pack issue (31 Oct 2026) to full application (11 Dec 2027): **406**; from board (19 Nov 2026): **387**
- Client: Example Group (fictional), HQ Germany (main establishment; coordinator CSIRT is Germany's); revenue EUR 1200m; EU revenue EUR 824.0m (69%); 3,800 employees; 920 engineers; 13 product families / 55 SKUs in scope; 7 legacy lines; ~2.3m connected devices in the field
- Classes: 6 default (incl. 2 provisional/borderline), 6 Class I, 1 Class II, 0 critical
- Revenue by class (EUR m): {'Default': 475, 'Class I': 585, 'Class II': 110}; EU revenue by class: {'Default': 338.3, 'Class I': 395.7, 'Class II': 72.6}
- **EU revenue from the 13 in-scope product families: EUR 806.6m (show as EUR 807m)**. Total EU revenue EUR 824.0m also includes EUR 17.4m of EU SaaS revenue (the cloud platform is not itself a product; it is remote data processing for some products). Never call EUR 824m 'in scope'.
- **EU revenue that needs a notified body (Class I+II): EUR 468.3m (39% of group revenue; 58% of in-scope EU revenue)** — headline: 'EUR 468m'
- Max fine per tier for Example Group: Tier 1 EUR 30m; Tier 2 EUR 24m; Tier 3 EUR 12m
- Portfolio readiness index (baseline 28 Oct 2026): **44%**; by BU HBS 39%, IC 52%, SS 41%; by class Default 42%, Class I 45%, Class II 54%
- Investment (base): one-off **EUR 9.25m** to Dec 2027 incl. 15% contingency (Q4 2026 EUR 1.42m; 2027 EUR 7.83m); run **EUR 1.84m/yr** from 2028; one-off = 0.77% of annual revenue; run = 0.15%
- Scenarios one-off: low EUR 7.93m; base EUR 9.25m; high EUR 11.42m. Run: low EUR 1.76m; high EUR 1.90m
- Engineering remediation: 26.2 FTE-years. Spend to date: EUR 410k (Oct 2026) vs plan EUR 384k.
- Overall programme RAG: **Amber** — Reporting capability on track; market access at risk because no notified body is designated (external dependency).

## Product families

| ID | Family | BU | Class | Annex item | Revenue EUR m | EU revenue EUR m | SKUs | Wave | Route | Support yrs | Readiness |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T200 | T200 Smart Thermostat | HBS | Default | - | 170 | 125.8 | 6 | Wave 1 (pilot) | Module A | 10 | 46% |
| SSR | S-Series Room Sensors | HBS | Default | - | 80 | 59.2 | 9 | Wave 2 | Module A | 8 | 38% |
| H3 | HomeHub H3 | HBS | Default (provisional) | Under legal review vs Annex III Class I item 17 (optional alarm mode) | 95 | 70.3 | 3 | Wave 2 | Module A (B+C if Class I) | 7 | 38% |
| V1 | V1 Video Doorbell | HBS | Class I | Annex III Class I item 17 (security cameras) | 100 | 74.0 | 4 | Wave 1 | Module B+C | 7 | 38% |
| L2 | L2 Smart Lock | HBS | Class I | Annex III Class I item 17 (smart door locks) | 75 | 55.5 | 3 | Wave 1 | Module B+C | 10 | 35% |
| IR500 | IR-500 Industrial Router | IC | Class I | Annex III Class I item 12 (routers, modems, switches) | 165 | 108.9 | 7 | Wave 1 | Module H | 12 | 50% |
| IS300 | IS-300 Managed Switch | IC | Class I | Annex III Class I item 12 (routers, modems, switches) | 120 | 79.2 | 10 | Wave 1 | Module H | 12 | 52% |
| EG700 | EG-700 Edge Gateway | IC | Default (provisional) | Under legal review vs Annex III Class I item 12 (cellular uplink routing) | 95 | 62.7 | 4 | Wave 2 | Module A (H if Class I) | 10 | 49% |
| SG900 | SG-900 Industrial Firewall/IDS | IC | Class II | Annex III Class II item 2 (firewalls, IDS/IPS) | 110 | 72.6 | 3 | Wave 1 | Module H | 10 | 54% |
| SLINK | SecureLink Remote Access | IC | Class I | Annex III Class I item 5 (VPN products) | 70 | 46.2 | 2 | Wave 1 | Module H | 7 | 52% |
| FLEET | FleetView Device Manager | SS | Class I | Annex III Class I item 6 (network management systems) | 55 | 31.9 | 2 | Wave 1 | Module H | 5 | 41% |
| CSTUDIO | ConfigStudio | SS | Default | - | 15 | 8.7 | 1 | Wave 2 | Module A | 5 | 43% |
| SDK | Example IoT SDK | SS | Default | - | 20 | 11.6 | 1 | Wave 2 | Module A | 5 | 38% |

Legacy lines: T100 Thermostat (gen 1) (End of sale 2025; support ended Mar 2026; 1100k units); HomeHub H2 (End of sale 2024; security fixes to Dec 2026; 420k units); V0 Indoor Camera (End of sale 2023; unsupported; 260k units); IR-300 Router (Still sold to two OEM customers; 95k units); IS-200 Switch (Still sold as low-cost option; 140k units); SecureLink 3.x (Support ends Jun 2027; 18k units); FleetView 4.x (Support ends Dec 2026; 3k units)

## Diagnostic heatmap (average level 0-4 per domain; target 3)

| Family | Governance | Scope & class | Risk & design | SDLC & testing | SBOM & supply chain | Vulnerability handling | Updates & support | Art 14 reporting | Documentation & DoC | Conformity & access | Index |
|---|---|---|---|---|---|---|---|---|---|---|---|
| T200 Smart Thermostat | 1.75 | 1.50 | 2.00 | 1.00 | 1.25 | 0.50 | 1.75 | 2.00 | 1.00 | 1.00 | 46% |
| S-Series Room Sensors | 1.75 | 1.00 | 1.25 | 1.00 | 0.50 | 0.75 | 2.00 | 2.00 | 0.50 | 0.50 | 38% |
| HomeHub H3 | 1.75 | 0.75 | 1.25 | 1.00 | 0.50 | 1.00 | 1.75 | 2.00 | 0.75 | 0.50 | 38% |
| V1 Video Doorbell | 1.75 | 1.25 | 1.50 | 1.00 | 1.00 | 0.50 | 1.75 | 2.00 | 0.50 | 0.25 | 38% |
| L2 Smart Lock | 1.75 | 1.00 | 1.25 | 1.00 | 0.50 | 0.75 | 1.50 | 2.00 | 0.50 | 0.25 | 35% |
| IR-500 Industrial Router | 1.75 | 1.50 | 1.50 | 2.50 | 1.00 | 1.75 | 1.75 | 2.25 | 0.75 | 0.25 | 50% |
| IS-300 Managed Switch | 1.75 | 1.75 | 1.50 | 2.50 | 1.25 | 1.75 | 1.50 | 2.25 | 1.00 | 0.50 | 52% |
| EG-700 Edge Gateway | 1.75 | 1.50 | 1.75 | 2.00 | 1.00 | 1.75 | 1.75 | 2.25 | 0.50 | 0.50 | 49% |
| SG-900 Industrial Firewall/IDS | 1.75 | 1.25 | 2.00 | 2.50 | 1.25 | 2.00 | 1.25 | 2.25 | 1.00 | 1.00 | 54% |
| SecureLink Remote Access | 1.75 | 1.50 | 1.50 | 2.25 | 1.50 | 1.75 | 1.75 | 2.25 | 0.75 | 0.75 | 52% |
| FleetView Device Manager | 1.75 | 1.75 | 1.00 | 1.75 | 1.25 | 0.75 | 1.00 | 2.25 | 0.50 | 0.25 | 41% |
| ConfigStudio | 1.75 | 1.75 | 1.00 | 1.75 | 1.75 | 1.00 | 0.50 | 2.25 | 1.00 | 0.25 | 43% |
| Example IoT SDK | 1.75 | 1.00 | 0.75 | 1.50 | 2.00 | 0.75 | 0.50 | 2.25 | 0.75 | 0.25 | 38% |
| **Portfolio average** | **1.75** | **1.35** | **1.40** | **1.67** | **1.13** | **1.15** | **1.44** | **2.15** | **0.73** | **0.48** | **44%** |

Domain readiness index: Governance 58%, Scope & class 45%, Risk & design 47%, SDLC & testing 56%, SBOM & supply chain 38%, Vulnerability handling 38%, Updates & support 48%, Art 14 reporting 72%, Documentation & DoC 24%, Conformity & access 16%

Ten weakest questions (portfolio average level):
- Q10.4 (0.08): EU representation, importer and distributor duties and marketplace arrangements are settled for each market. — Action: Confirm the role per market, appoint an authorised representative where useful and brief importers on their checks.
- Q10.2 (0.38): Candidate notified bodies are shortlisted and a pre-assessment is contracted where the route needs one. — Action: Shortlist three candidates, contract pre-assessments with conversion options, and check NANDO at every programme board.
- Q10.3 (0.38): A complete Module A internal-control record is kept for the product, even where a notified body will be used. — Action: Build the Module A record and evidence index now; it is the fallback and the body's application pack.
- Q9.1 (0.46): An Annex VII technical file exists for each product version and is versioned with releases. — Action: Adopt the 13-part file outline and generate version-linked contents from the release pipeline.
- Q6.4 (0.69): Vulnerability case records are retained and response metrics are reported. — Action: Report acknowledgement and fix times quarterly and retain case files for 10 years or the support period.
- Q9.2 (0.69): Annex II user information, including the support end date and the vulnerability contact, is drafted and ready to publish. — Action: Draft the Annex II document per product family and publish it at a stable, versioned URL.
- Q9.4 (0.77): Evidence sits in a system of record with 10-year retention and can answer a reasoned request within 10 working days. — Action: Select a system of record, compute retention per version and test an end-to-end reasoned-request export.
- Q2.4 (0.92): The economic-operator role per market and the legacy status of each product line are recorded. — Action: Record manufacturer, importer, distributor or representative per market; flag lines still sold after 11 Dec 2027.
- Q5.3 (0.92): Supplier contracts require vulnerability notification, SBOM delivery and support-period commitments. — Action: Add the CRA clause pack to master agreements, starting with suppliers of security-relevant components.
- Q1.3 (1.00): A written product-risk acceptance rule excludes cost, risk appetite and commercial strategy as reasons to leave risk unaddressed. — Action: Add a product-risk category to the enterprise risk framework with its own acceptance authority and a non-cost appeal route.

## Cost model — base case lines (EUR)

| Workstream | Line | Q4 2026 | 2027 | Run 2028 |
|---|---|---|---|---|
| Programme & governance | Programme team (director, compliance lead, product security officer, PMO) | 187,500 | 750,000 | 375,000 |
| Reporting & PSIRT | Incremental PSIRT (lead + analyst) and 24/7 on-call allowance | 80,000 | 320,000 | 320,000 |
| Secure engineering | Engineering remediation of Annex I gaps | 471,600 | 2,672,400 | 0 |
| Shared platforms | SBOM/VEX/CSAF tooling, signing HSM and update infrastructure, system of record, PSIRT tooling | 212,500 | 742,500 | 210,000 |
| Secure engineering | Risk assessments and threat models | 175,500 | 409,500 | 0 |
| Secure engineering | Security testing (penetration tests, fuzzing, re-tests) | 0 | 660,000 | 660,000 |
| Documentation & evidence | Technical files and Annex II user information | 0 | 520,000 | 104,000 |
| Conformity & market access | Notified bodies: pre-assessments, Module B examinations, Module H approval | 20,000 | 335,000 | 55,000 |
| People & change | Training and awareness | 30,000 | 110,000 | 40,000 |
| Conformity & market access | Legal, EU representation and translations | 60,000 | 198,000 | 50,000 |
| Supply chain | Supplier contract remediation and questionnaire programme | 0 | 90,000 | 30,000 |
| | Subtotal | 1,237,100 | 6,807,400 | 1,844,000 |
| | Contingency 15% | 185,565 | 1,021,110 | - |
| | **Total** | **1,422,665** | **7,828,510** | **1,844,000** |

By workstream (one-off excl. contingency / run): Programme & governance EUR 938k / EUR 375k; Reporting & PSIRT EUR 400k / EUR 320k; Secure engineering EUR 4.39m / EUR 660k; Shared platforms EUR 955k / EUR 210k; Documentation & evidence EUR 520k / EUR 104k; Conformity & market access EUR 613k / EUR 105k; People & change EUR 140k / EUR 40k; Supply chain EUR 90k / EUR 30k

Monthly cumulative plan (incl. contingency): Oct 2026 EUR 384k, Nov 2026 EUR 854k, Dec 2026 EUR 1.42m, Jan 2027 EUR 1.85m, Feb 2027 EUR 2.36m, Mar 2027 EUR 2.95m, Apr 2027 EUR 3.61m, May 2027 EUR 4.32m, Jun 2027 EUR 5.06m, Jul 2027 EUR 5.81m, Aug 2027 EUR 6.51m, Sep 2027 EUR 7.22m, Oct 2027 EUR 7.92m, Nov 2027 EUR 8.62m, Dec 2027 EUR 9.25m

## Programme

Phases: P0 Reporting readiness (1 Sep 2026 - 30 Oct 2026, Complete); P1 Inventory, scope and classification (2 Nov 2026 - 18 Dec 2026, In progress); P2 Risk assessment and gap analysis (1 Dec 2026 - 26 Feb 2027, Planned); P3 Remediation and SDLC changes (4 Jan 2027 - 31 Aug 2027, Planned); P4 Documentation and declarations (1 Jun 2027 - 30 Sep 2027, Planned); P5 Conformity assessment (1 Apr 2027 - 30 Nov 2027, Planned); P6 Go-live and operations (11 Dec 2027 - ongoing, Planned)

Waves: Wave 1: T200, V1, L2, IR500, IS300, SG900, SLINK, FLEET (Nov 2026 - Nov 2027); Wave 2: SSR, H3, EG700, CSTUDIO, SDK (Jan 2027 - Oct 2027); Wave 3: T100, H2, V0, IR300, IS200, SL3, FV4 (Continuous)

Milestones:
- M0 10 Sep 2026 — SRP registration and coordinator CSIRT decision [Complete]
- M1 22 Oct 2026 — First Art 14 tabletop drill (actively exploited vulnerability) [Complete]
- M2 30 Oct 2026 — Programme mobilised; SteerCo #1 [Complete]
- M3 19 Nov 2026 — Board decisions (budget, signing authority, notified-body strategy, legacy lines) [Planned]
- M4 18 Dec 2026 — Scope and classification register baselined [On track]
- M5 29 Jan 2027 — Notified-body pre-assessments contracted (3 candidates) [At risk]
- M6 26 Feb 2027 — Wave 1 risk assessments signed [On track]
- M7 31 Mar 2027 — Formal notified-body engagements contracted (Module H; Module B+C) [At risk]
- M8 31 Mar 2027 — SBOM pipeline live on all Wave 1 release trains [At risk]
- M9 16 Apr 2027 — Second Art 14 drill (weekend severe-incident scenario) [Planned]
- M10 30 Jun 2027 — Update infrastructure hardened (HSM signing, anti-rollback) [Planned]
- M11 30 Sep 2027 — Wave 1 technical files complete [Planned]
- M12 30 Nov 2027 — Module H approval and Module B certificates [Planned]
- M13 3 Dec 2027 — Declarations signed; CE marking; Annex II published [Planned]
- M14 11 Dec 2027 — Full application of the CRA [Fixed]

Workstreams:
- WS1 Governance & PMO (lead: Programme director) — Green: Sponsor named; programme board running; signing instrument drafted for board approval.
- WS2 Portfolio & classification (lead: Compliance lead) — Amber: 11 of 13 families classified; EG-700 and HomeHub H3 need legal opinion (borderline Class I).
- WS3 Reporting & PSIRT (lead: PSIRT lead) — Green: SRP live with 3 Assigned Representatives; first drill filed early warning in 9h 40m.
- WS4 Secure engineering & SDLC (lead: Product security officer) — Amber: T200 pilot risk assessment in review; release gate designed, not yet enforced.
- WS5 SBOM & supply chain (lead: Head of platform engineering) — Red: Signed SBOMs on 38% of releases; HBS firmware builds lack binary SCA; 6 of 41 suppliers on CRA clauses.
- WS6 Documentation & evidence (lead: Compliance lead) — Amber: System of record not yet selected; Annex VII outline agreed.
- WS7 Conformity & market access (lead: Head of quality & regulatory) — Red: No CRA notified body designated (external); 3 candidates shortlisted; V1/L2 route undecided.
- WS8 People & change (lead: Head of engineering enablement) — Amber: 140 of 920 engineers trained; works council consultation on PSIRT on-call opened.

## KPIs (SteerCo #1, as at 30 Oct 2026)

| ID | KPI | Value | Target | RAG | Trend | Source |
|---|---|---|---|---|---|---|
| K01 | Portfolio readiness index | 44% | 70% by Jun 2027; 90% by Nov 2027 | Amber | Baseline | Readiness diagnostic, 28 Oct 2026 |
| K02 | Families with final scope and class decision | 11 / 13 | 13 / 13 by 18 Dec 2026 | Amber | New | Scope register |
| K03 | Class I/II families with route and notified-body plan | 5 / 7 | 7 / 7 by 19 Nov 2026 | Amber | New | Scope register |
| K04 | SRP Assigned Representatives registered | 3 | >= 2 at all times | Green | Stable | SRP roster |
| K05 | Art 14 drill: time to early warning | 9h 40m | < 24h incl. weekends | Green | First drill | Drill record 22 Oct 2026 |
| K06 | Art 14 cases assessed (reportable / not reportable) | 0 / 4 | 100% decided with UTC timeline | Green | Stable | PSIRT case files |
| K07 | Releases with signed SBOM (last 30 days) | 38% (9 / 24) | 100% by 31 Mar 2027 | Red | Up from 21% | Build pipeline |
| K08 | Families with signed risk assessment | 0 / 13 (T200 in review) | Wave 1 (8) by 26 Feb 2027 | Green | On plan | System of record |
| K09 | In-scope suppliers on CRA clauses | 6 / 41 (15%) | Top 15 by Jan 2027; all by Jun 2027 | Amber | New | Contract register |
| K10 | Engineers trained | 140 / 920 (15%) | 60% by Mar 2027 | Amber | Up | LMS |
| K11 | Spend to date vs plan | EUR 0.41m vs EUR 0.38m | Within +/-10% of plan | Green | Oct 2026 | Finance |
| K12 | Notified-body candidates | 3 shortlisted; 1 proposal | 3 pre-assessments contracted by 29 Jan 2027 | Amber | New | Programme |

## Risks

| ID | Risk | L | I | Score | Rating | Owner | Mitigation | Trend |
|---|---|---|---|---|---|---|---|---|
| R01 | No notified-body capacity in time: No CRA notified body is designated with capacity before Q2 2027, so Class I/II families cannot be certified by 11 Dec 2027. | 4 | 5 | 20 | High | Head of quality & regulatory | Pre-contract three candidates with conversion options; Module H for IC to cover five families with one body; check NANDO at every programme board; prioritise top-revenue SKUs. | Rising |
| R02 | Engineering capacity: Remediation competes with the 2027 product roadmap for the same engineers. | 4 | 4 | 16 | High | CTO | Ring-fence 26 FTE-years in the 2027 plan; defer two roadmap features; contractors for documentation and testing. | Stable |
| R03 | No harmonised standard cited for Class I: EN 304 6xx verticals are not cited in time, so Class I products cannot use Module A. | 4 | 3 | 12 | High | Compliance lead | Plan Class I on third-party routes; align files to draft clause structure; switch to Module A only if a citation lands before assessment. | Stable |
| R04 | SBOM and supplier transparency gaps: Binary blobs and supplier components without SBOMs or vulnerability notification undermine Annex I Part II(1) and the 24-hour determination. | 3 | 4 | 12 | High | Head of platform engineering | Binary SCA on firmware images; clause pack to top 15 suppliers first; exit plans for refusers. | Stable |
| R05 | Legacy lines still sold after 11 Dec 2027: IR-300 and IS-200 units placed after 11 Dec 2027 must comply with Annex I. | 3 | 4 | 12 | High | BU president IC | Board decision on 19 Nov 2026 to withdraw from EU sale and migrate customers; remediate only if the decision changes. | New |
| R06 | Late or wrong Art 14 filing: Awareness misjudged or a stale distribution map delays the 24-hour early warning. | 2 | 5 | 10 | Medium | PSIRT lead | Written awareness criteria; deputies with authority to file; distribution map refresh (T10); two drills a year. | Falling |
| R07 | Scope undercount: Versions, companion apps and backends found late enlarge the portfolio. | 3 | 3 | 9 | Medium | Compliance lead | Build the register from release and cloud systems; second reconciliation after the first gate run. | Stable |
| R08 | Key-person dependency in PSIRT: Two people hold most PSIRT knowledge; on-call cannot be sustained. | 3 | 3 | 9 | Medium | PSIRT lead | Hire PSIRT lead; second analyst; documented runbook; cross-training from IC. | Stable |
| R09 | Guidance changes: Formal adoption of C(2026) 5252 or later FAQ versions change scope or support-period decisions. | 3 | 2 | 6 | Medium | Compliance lead | Decision records cite the guidance version; quarterly standards and guidance review. | Stable |
| R10 | Product-liability disclosure: From 9 Dec 2026 claimants can seek disclosure of technical files and update logs under the PLD. | 2 | 4 | 8 | Medium | General Counsel | Write records for disclosure; legal review of risk acceptances; align with product liability insurance. | New |

Issues: I01 Distribution map stale — The 22 Oct drill showed the 'Member States where available' field could not be completed for two products from current data. (owner Product management, due 20 Nov 2026); I02 Borderline classifications — EG-700 (cellular uplink routing) and HomeHub H3 (optional alarm mode) could be Class I; notified-body capacity planning includes them until the legal opinion lands. (owner General Counsel, due 27 Nov 2026); I03 HBS firmware SBOM depth — Manifest-only SBOMs on HBS firmware miss vendored code; binary SCA needed. (owner Head of platform engineering, due 15 Jan 2027)

## Decisions

SteerCo #1 (30 Oct 2026): SD1 Endorse Module H as the route for Industrial Connectivity and FleetView (five families), using the IEC 62443-4-1 process as the base. SD2 Apply the stricter reading to EG-700 and HomeHub H3 until the legal opinion lands on 27 Nov 2026: include them in notified-body capacity planning, keep them in Wave 2 for remediation. SD3 Release EUR 0.75m of pre-approval spend ahead of the 19 Nov board. SD4 Approve system-of-record selection criteria.

Board (19 Nov 2026):
- BD1 Approve the Project Rampart investment envelope. — EUR 9.3m one-off to Dec 2027 (incl. 15% contingency) and EUR 1.8m a year run from 2028.
- BD2 Appoint the accountable executive and execute the DoC signing instrument. — CTO as accountable executive; CEO signs declarations or delegates in writing; compliance lead counter-signs the pre-signature checklist.
- BD3 Authorise notified-body pre-contracting. — Pre-assessments with three candidate bodies (up to EUR 60k) and formal contracts by Q1 2027 (Module H for IC + FleetView; Module B+C for V1 and L2).
- BD4 Adopt the product-risk acceptance rule. — Cost, risk appetite and commercial strategy are not grounds to leave product risk unaddressed (guidance paras 156-163); appeals go to the executive sponsor.
- BD5 Withdraw IR-300 and IS-200 from EU sale before 11 Dec 2027. — EUR 18m of declining EU revenue versus about EUR 1.4m remediation plus notified-body fees; migrate customers to IR-500 and IS-300.

## Canonical regulatory facts

- F01: The CRA is Regulation (EU) 2024/2847; it entered into force on 10 Dec 2024. (Art 71; EUR-Lex; https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- F02: Article 14 reporting applies from 11 Sep 2026 to all in-scope products, including those placed on the market before 11 Dec 2027. (Art 71(2); Art 69(3); https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- F03: Chapter IV (notification of conformity assessment bodies) applies from 11 Jun 2026; all other provisions from 11 Dec 2027. (Art 71(2); https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- F04: Reporting clocks: actively exploited vulnerability 24h early warning, 72h notification, final report 14 days after a corrective measure is available; severe incident 24h, 72h, final report 1 month after the 72h notification. (Art 14(2), (4); https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- F05: Reports go through ENISA's Single Reporting Platform to the coordinator CSIRT of the main-establishment Member State; the platform has been live since 11 Sep 2026 (web form, English only, no API). (Art 14(7); ENISA; https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp)
- F06: Fines: up to EUR 15m or 2.5% of worldwide annual turnover (Annex I, Arts 13-14); EUR 10m or 2% (other obligations); EUR 5m or 1% (misleading information), whichever is higher. (Art 64(2)-(4); https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- F07: No harmonised standard is cited in the OJ and no common specification is adopted (30 Oct 2026); Class I products cannot use Module A until one is cited and applied in full. (Art 32(2); guidance para 149; https://digital-strategy.ec.europa.eu/en/factpages/cyber-resilience-act-implementation)
- F08: No CRA notified body was verifiably designated in NANDO at checks to 8 Sep 2026; Member States must 'strive' for enough bodies by 11 Dec 2026. (Art 35(2); Commission; https://digital-strategy.ec.europa.eu/en/policies/cra-conformity-assessment)
- F09: Annexes III and IV list 19 Class I, 4 Class II and 3 critical categories (26 in total); Implementing Regulation (EU) 2025/2392 gives their technical descriptions (in force 21 Dec 2025). (Art 7; Art 8; https://eur-lex.europa.eu/eli/reg_impl/2025/2392/oj/eng)
- F10: Commission guidance C(2026) 5252 (content approved 27 Jul 2026) is non-binding and formally pending adoption in all languages; FAQ v1.4 is dated 4 Sep 2026. (Art 26; https://ec.europa.eu/newsroom/dae/redirection/document/131456)
- F11: Support period must reflect expected time in use and be at least five years unless the product is expected to be used for less; security updates stay available for at least 10 years or the rest of the support period. (Art 13(8)-(9); https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- F12: Technical documentation and the declaration are kept for 10 years after placing on the market or the support period, whichever is longer. (Art 13(13); https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- F13: The SBOM is part of the technical documentation; manufacturers are not obliged to make it public. (Annex I Part II(1); Annex VII; Recital 77; https://eur-lex.europa.eu/eli/reg/2024/2847/oj)
- F14: Manufacturer-built backends a product needs for a function are remote data processing and part of the product. (Art 3(2); guidance paras 184-205; https://ec.europa.eu/newsroom/dae/redirection/document/131456)
- F15: The Product Liability Directive (EU) 2024/2853 applies from 9 Dec 2026; software is a product and a vulnerability can be a defect. (PLD Arts 4, 7, 9-10; https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024L2853)
- F16: National enforcement acts adopted by 30 Oct 2026: Finland (Act 439/2026), Hungary (Act CXXXV/2025), Malta (LN 238/2026); Germany's law passed the Bundestag plenary on 15 Oct 2026, promulgation pending. France has named ANSSI as notifying authority. (KB: Enforcement)
- F17: The Digital Omnibus COM(2025) 837 does not amend the CRA; Council mandate agreed 21 Oct 2026 (ST 14756/26); not adopted. (KB: Interplay; https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52025PC0837)
- F18: RED cybersecurity delegated act 2022/30 is repealed with effect from 11 Dec 2027 by Delegated Regulation (EU) 2026/339. (KB: Interplay; https://eur-lex.europa.eu/eli/reg_del/2026/339/oj/eng)
- F19: EUCC: 111 valid certificates from 9 certification bodies on 30 Oct 2026; the Art 27(9) act that would let EUCC replace third-party assessment is planned, not adopted. (KB: Standards; verification)
- F20: Open-source stewards have a light-touch regime (Art 24) and are exempt from fines (Art 64(10)(b)); integrating FOSS never transfers the manufacturer's duty (Art 13(5)). (Arts 13(5), 24, 64(10); https://eur-lex.europa.eu/eli/reg/2024/2847/oj)

## Research datapoints (label type exactly as given)

- RD01: German companies that know what the CRA means for them = 29% (67% have heard of it; 38% cannot assess it; 28% unaware; sample: 1,003 German companies with 10+ employees; Apr-Jun 2026; Bitkom Research via IT Finanzmagazin, 11 Sep 2026; type: Survey; https://www.it-finanzmagazin.de/cyber-resilience-act-cra-nur-jedes-dritte-unternehmen-vorbereitet-250594/)
- RD02: CRA-aware respondents unaware of CRA penalties = 56% (Only 34% identify 2027 as the compliance year; 66% of all 843 respondents are not or only slightly familiar with the CRA; sample: 404 CRA-aware respondents (of 843 surveyed); early 2026; Linux Foundation Research, CRA awareness report 2026; type: Survey; https://www.linuxfoundation.org/hubfs/Research%20Reports/lfr_2026_cra_awareness_report_060826.pdf?hsLang=en)
- RD03: Manufacturers relying passively on upstream projects for security fixes = 51% (Separately, LF's 2025 Open Source ROI survey (n=236), cited in the 2026 report, found an average of 86 private forks per organisation at about 60 hours each per release cycle; sample: Manufacturer module (n=194-219) of the 843-respondent survey; early 2026; Linux Foundation Research 2026; type: Survey; https://www.linuxfoundation.org/hubfs/Research%20Reports/lfr_2026_cra_awareness_report_060826.pdf?hsLang=en)
- RD04: SME manufacturers planning to raise prices to cover compliance = 47% (Stewards' top support needs in 2026: financial support 50%, legal guidance 39% (n=28); the 2025 legal-guidance figure was 47% (n=34); sample: 54 SME manufacturers; early 2026; Linux Foundation Research 2026; type: Survey (small subsample); https://www.linuxfoundation.org/hubfs/Research%20Reports/lfr_2026_cra_awareness_report_060826.pdf?hsLang=en)
- RD05: SMEs asking for technical documentation templates = 73% (13% rate their understanding of documentation requirements as good; sample: 194 responses, not representative; Jun 2026 report; ENISA SME CRA survey; type: Survey (official); https://www.enisa.europa.eu/sites/default/files/2026-06/SME%20CRA%20survey%20report.pdf)
- RD06: Firms expecting longer product development under the CRA = >60% (28% 'significantly longer'; 28% have CRA teams of up to 10 people, 22% larger, 16% up to 3; sample: 200 German industrial firms; Sep 2026; ONEKEY IoT/OT Cybersecurity Report 2026; type: Vendor survey; https://www.onekey.com/press-release/onkey-iot-ot-cybersecurity-report-2026-half-of-all-companies-have-formed-cra-teams)
- RD07: Respondents with partly or fully automated SBOM generation = 74% (Completeness is the top challenge (62%); 44% CycloneDX, 29% SPDX; 39% generate at build; sample: 334 responses; Jun 2026; ENISA SBOM Adoption State of Play 2026; type: Survey (official); https://www.enisa.europa.eu/sites/default/files/2026-06/SBOM%20Adoption%20State%20of%20Play%202026.pdf)
- RD08: Companies expecting cost increase under 20% = 50% (25% expect 20-40%; 25% no impact; sample: 12 companies; 2024; KONE-authored industrial study (arXiv 2505.14325); type: Survey (small sample); https://arxiv.org/pdf/2505.14325)
- RD09: Illustrative cost for three default products at medium readiness = EUR 78,300 one-off; EUR 13,500 a year (At EUR 45 per hour; 'illustrative and intended for planning only'; sample: Model; 2026; cyberresilienceact.eu cost calculator; type: Independent model; https://www.cyberresilienceact.eu/cra-compliance-cost-calculator/)
- RD10: CRA notified bodies verifiably designated = 0 (Checks to 8 Sep 2026; Brightsight (RvA accreditation, pending Dutch notification) and Applus+ in the pipeline per vendor statements; sample: NANDO / Single Market Compliance Space; 8 Sep 2026; European Commission; vendor statements; type: Official + vendor; https://digital-strategy.ec.europa.eu/en/policies/cra-conformity-assessment)
- RD11: Valid EUCC certificates = 111 from 9 certification bodies (EUCC is the only adopted EU cybersecurity certification scheme; sample: ENISA register; 30 Oct 2026; ENISA EUCC register (fact-checked); type: Official)
- RD12: Time to designate a notified body = 12-18 months (2-4 months to contract; 3-6 months per Module B+C engagement; sample: Commentary; 2026; CRA Decoded; type: Commentary (unverified); https://cra-decoded.com/blog/posts/cra-notified-body-capacity-crisis/)

## Stakeholders

| ID | Stakeholder | Power | Interest | Now | Target | Key concern | Key message | Channel | Owner | Frequency |
|---|---|---|---|---|---|---|---|---|---|---|
| ST01 | Board of directors | 5 | 3 | Aware | Committed | Liability, fines, market access, cost | A funded 14-month programme protects EUR 468m of EU revenue; five decisions now. | Board paper and briefing | Executive sponsor | Quarterly |
| ST02 | CEO and executive committee | 5 | 4 | Supportive | Committed | Revenue at risk, roadmap impact | Reporting is live; market access is the constraint; build once, apply per product. | ExCo agenda item; monthly dashboard | Executive sponsor | Monthly |
| ST03 | CTO (accountable executive) | 5 | 5 | Committed | Leading | Engineering capacity, release gates | You own the release gate and the evidence; the programme gives you shared tooling. | SteerCo; 1:1 | Programme director | Fortnightly |
| ST04 | General Counsel | 4 | 4 | Supportive | Committed | DoC liability, PLD disclosure, classification calls | Decision records and the signing instrument limit personal and corporate exposure. | SteerCo; legal working group | Compliance lead | Fortnightly |
| ST05 | CISO | 4 | 5 | Committed | Leading | PSIRT vs CSIRT split, NIS2/GDPR overlap | Product PSIRT is separate from the infrastructure CSIRT; one coordination cell for multi-regime incidents. | SteerCo; incident cell | PSIRT lead | Weekly |
| ST06 | BU presidents (HBS, IC, S&S) | 5 | 4 | Mixed | Committed | Margin, roadmap, legacy lines | Your EU revenue depends on notified-body slots we must book now. | BU reviews; SteerCo | Executive sponsor | Monthly |
| ST07 | Engineering leads and developers | 3 | 4 | Unaware to aware | Practising | Extra process, release friction | Evidence comes from the pipeline, not from paperwork; the gate checks what you already test. | Engineering all-hands; training; Slack | Product security officer | Fortnightly |
| ST08 | Product management | 3 | 4 | Aware | Committed | Support periods, roadmap trade-offs | Support period and Annex II content are product decisions with legal weight. | PM forum; briefing pack | Compliance lead | Monthly |
| ST09 | PSIRT and on-call staff | 2 | 5 | Committed | Committed | Workload, 24/7 on-call, authority to file | You may file an early warning without prior approval; legal reviews the 72-hour report. | Runbook; drills | PSIRT lead | Weekly |
| ST10 | Quality & regulatory (CE/RED team) | 3 | 5 | Supportive | Leading | Notified-body capacity, RED transition | Your CE experience runs conformity; RED delegated act ends 11 Dec 2027. | Workstream meetings | Programme director | Weekly |
| ST11 | Procurement | 3 | 3 | Aware | Committed | Supplier pushback, contract renegotiation | Clause pack and questionnaire; refusals go to the intake gate as high risk. | Procurement council | Head of procurement | Monthly |
| ST12 | Sales, key accounts and customer support | 2 | 3 | Unaware | Informed | Customer questions, competitive positioning | Say what we do, not 'CRA certified'; use the FAQ; route vulnerability reports to PSIRT within the hour. | Briefing; FAQ; LMS module | Head of customer operations | At launch, then quarterly |
| ST13 | Works council | 4 | 3 | Neutral | Supportive | On-call arrangements, training time, monitoring | On-call is voluntary-rota based with allowances; training is in working time. | Formal consultation | HR business partner | As required |
| ST14 | All employees | 1 | 2 | Unaware | Informed | What it means for me | Security is now part of what we sell; know where to report a vulnerability. | Intranet; town hall | Internal communications | Quarterly |
| ST15 | B2B customers and integrators | 4 | 4 | Asking | Confident | Supply-chain evidence for their own NIS2/CRA duties | Support periods, CVD contact, SBOM on request and declarations on a published timetable. | Account letters; customer FAQ; trust page | Head of customer operations | Quarterly |
| ST16 | Consumers (via retail and app) | 2 | 2 | Unaware | Informed | Updates, privacy, support length | Automatic security updates by default and a clear support end date at purchase. | Product pages; app notices | Marketing | At launch |
| ST17 | Distributors, importers and retail partners | 3 | 3 | Asking | Confident | Their Art 19-20 checks, labelling, stock after 11 Dec 2027 | We will supply DoCs, Annex II information and CE marking per product before 11 Dec 2027. | Channel letter; partner portal | Head of channel | Quarterly |
| ST18 | Suppliers (chipsets, modules, ODMs, software) | 3 | 3 | Mixed | Cooperative | Contract changes, SBOM effort | We need vulnerability notification, SBOMs and support commitments; here is the clause pack. | Supplier letter; questionnaire | Head of procurement | Quarterly |
| ST19 | Notified bodies (candidates) | 5 | 3 | Engaged | Contracted | Capacity, designation timing | We are assessment-ready early and want a slot with conversion options. | Pre-assessment meetings | Head of quality & regulatory | Monthly |
| ST20 | Coordinator CSIRT and market surveillance (Germany) | 5 | 3 | Neutral | Trusting | Timely, accurate reporting | We report on time with complete data and answer reasoned requests within 10 working days. | SRP; formal correspondence | PSIRT lead / Compliance lead | As required |
| ST21 | Open-source communities and maintainers | 2 | 3 | Neutral | Collaborative | Burden shifted to unpaid maintainers | We report upstream through your CVD channel and share fixes; we do not demand compliance from you. | OSPO; upstream channels | OSPO lead | As required |
| ST22 | Insurers (product liability, cyber) | 3 | 2 | Unaware | Informed | PLD exposure from 9 Dec 2026 | Our evidence system lowers defect and disclosure risk. | Broker briefing | CFO office | At renewal |
