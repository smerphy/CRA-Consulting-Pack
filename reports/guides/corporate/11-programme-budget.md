## 11. Programme plan, budget and metrics

The portfolio programme runs the phases from the knowledge base, Engineering compliance programme, as waves rather than as one project. Each wave takes a set of products through inventory, risk assessment, remediation, documentation and conformity assessment. Each later wave reuses what the first produced; the phase dates, outputs and gates are in that section's roadmap.

This section covers wave planning, budget lines, the KPIs the programme board tracks and what the board itself sees. The benchmark figures are thin; all are survey or vendor material and are labelled as such.

### Running the phases at portfolio level

| Principle | How it works | Why |
|---|---|---|
| Wave by class and revenue | Wave 1: Class I and II products with the highest revenue or exposure, plus one default product as a control. Wave 2: remaining important products. Wave 3: default products by revenue. Wave 4: legacy products due for substantial modification | Important products face the notified-body constraint; revenue decides what cannot be left off the market on 11 Dec 2027 |
| Representative product first | One product per family goes through every phase before the rest of the family starts; its records become the templates and worked examples (Section 9) | Consultancy practice: pilot the record set on one product, then scale ([SCHUTZWERK](https://www.schutzwerk.com/en/blog/cra-guidance-2026/), vendor); lab practice: gap-assess a representative product (Nemko, vendor) |
| Parallel documentation | Technical-file assembly starts when the risk assessment is signed, not when remediation ends; families share one file where guidance paras 174-177 allow | Phase 4 runs in parallel at 2-4 months per family; waiting for remediation to finish pushes documentation into the notified-body window |
| Reporting first, everywhere | Phase 0 covers the whole portfolio, including legacy products, before any wave starts | Art 14 applies now (Art 69(3)); it does not wait for waves |
| Shared services, product decisions | SBOM pipeline, update infrastructure, PSIRT, system of record and policies are built once; scope, class, risk and support period are decided per product | Engineering uplift is the largest cost (phase 3); sharing it is where the saving is |
| Notified-body slot drives the wave calendar | Wave 1 contracting by Q1 2027 (commentary), with assessment from Q2 2027; Wave 2 slots follow | Phase 5 is the constraint; vendor estimates give 2-4 months to contract and 3-6 months per Module B+C engagement, unverified |
| Guidance changes are re-planned, not absorbed | A cited harmonised standard, a new FAQ version or a notified-body designation triggers a wave review at the next programme board | Class I products may switch to Module A on citation; records relying on old guidance are superseded (Section 4) |

A mid-size manufacturer should expect 12 to 18 months from a standing start to assessment-ready for an important product. That is roughly the time left to 11 Dec 2027 (an inference in the research notes, not an authority figure). The waves therefore overlap: Wave 2 inventory and risk assessment start while Wave 1 is in remediation.

### Budget lines

| Line | What it covers | Benchmark, labelled |
|---|---|---|
| People | Compliance lead, product security officer, PSIRT lead and on-call, SBOM owner per release train, line 2 reviewers, programme management; engineering time for remediation | ONEKEY (Sep 2026, 200 German industrial firms, vendor survey): 28% have CRA teams of up to 10 people, 22% larger, 16% up to 3; over 60% expect longer development, 28% "significantly longer". No authoritative FTE benchmark exists |
| Tooling | SBOM generation and quality (Syft, Trivy, cdxgen, sbomqs), signing and attestation (cosign), dependency monitoring (Dependency-Track), VEX and CSAF, threat-modelling tools, the system of record, SRP access devices | ENISA SBOM State of Play 2026 (survey) (334 responses): 74% have partly or fully automated SBOM generation; completeness is the top challenge at 62%. Open-source tooling dominates ENISA's landscape table |
| Notified-body fees | Pre-assessments, Module B type examinations, Module H quality-system approval and surveillance, scope extensions | Vendor estimates, unverified: EUR 20,000-60,000 per Module B examination; EUR 80,000-150,000 for a first Module H engagement with surveillance every 1-2 years ([CRA Decoded](https://cra-decoded.com/blog/posts/cra-notified-body-capacity-crisis/), commentary); another vendor gives EUR 15,000-80,000 for Module B (sota.io, unsourced) |
| External testing | Penetration tests, fuzzing, binary SCA, lab gap assessments | [cyberresilienceact.eu calculator](https://www.cyberresilienceact.eu/cra-compliance-cost-calculator/) (independent model, illustrative): security testing EUR 6,400 within a EUR 78,300 one-off for three default products at medium readiness and EUR 45 per hour |
| Training | Role-based training (Section 9), drills, ORC Learning Hub and vendor courses | ENISA SME survey (Jun 2026, 194 responses, not representative): 73% want technical documentation templates; 13% rate their documentation understanding good |
| Legal | Steward determinations, supplier clause negotiation, authorised-representative mandate, DoC signing instrument, reasoned-request responses, PLD readiness | LF 2026 (survey, 28 stewards): 39% of stewards cite legal guidance as a support need (47% in 2025, n=34) |
| Representation and market access | Authorised representative fees, EU-language DoCs and Annex II translations, marketplace compliance | No benchmark found; UK groups carry this as a separate line (Section 10) |
| Running cost after go-live | Vulnerability handling, security updates, surveillance audits, standards re-mapping, SRP operation | Calculator (illustrative): EUR 13,500 a year for three default products; vulnerability handling and updates EUR 6,000 each |

Two further figures frame the business case. The KONE-authored industrial study (2024, 12 companies, survey) found 50% expecting cost increases under 20%. LF 2026 found 47% of SME manufacturers expecting to raise prices to cover compliance (survey, 54 SME manufacturers).

Treat every figure above as a planning prompt, not a quote. Bitkom, Orgalim, DigitalEurope, ZVEI and techUK have published positions but no quantitative cost surveys that the research found.

### KPIs

The programme board (Section 2) tracks these monthly; the executive review sees them quarterly. Every KPI reads from the system of record (Section 8) or the scope register (Section 4), never from a slide.

| Metric | Target | Source of truth |
|---|---|---|
| Products with a recorded scope and class decision | 100% of register rows by end of phase 1 (Dec 2026); 100% maintained | Scope register; decision records |
| Products with a conformity route and notified-body plan | 100% of Class I and II rows by end of phase 1 | Scope register |
| Risk assessments signed off by line 2 | 100% of Wave 1 by Feb 2027; 100% of in-scope products before placing on or after 11 Dec 2027 | System of record, risk assessment status |
| Annex I applicability matrices with no blank justification | 100% of signed assessments | System of record |
| SBOM coverage per release | 100% of releases with a signed SBOM meeting the TR-03183-2 fields; depth to the first out-of-scope component | Build pipeline; sbomqs results |
| Mean time to remediate by severity | Set per the vulnerability-handling policy; one vendor's example is 7 days critical, 30 days high, 90 days medium (CVD Portal, vendor); the CRA itself gives no numeric "without delay" | PSIRT case files |
| Upstream reports filed where due | 100% of component vulnerabilities found, with duplicate-check recorded | PSIRT case files |
| Drill results against 24-hour and 72-hour targets | Two drills a year; early warning filed on paper within 24 hours by a deputy at a weekend; 72-hour content complete | Drill records |
| Awareness-to-early-warning time in live cases | Under 24 hours in 100% of cases; median tracked | PSIRT case files, UTC timeline |
| Technical files complete per Annex VII | 100% of Wave 1 by Sep 2027; 100% before placing | System of record, file completeness check |
| Reasoned-request readiness | Test export of a complete file in under 10 working days, twice a year | Line 3 sampling |
| DoCs issued | One per family or product as planned, signed under the Section 2 instrument, before placing | DoC register |
| Supplier clauses in place | 100% of suppliers of in-scope components under the Section 6 clauses or a documented exception | Procurement contract register |
| Supplier SBOMs received per release | 100% of commercial components | Intake-gate records |
| Open high-risk findings | Zero at any release gate; ageing of open findings reported | Risk register, product-risk category |
| Residual-risk acceptances and appeals | All recorded with a non-cost basis; appeals count reported | Product-risk register |
| Steward determinations and Art 24(1) policies | 100% of published projects determined; policies published before 11 Dec 2027 | Project registry |
| Training completion by role | 100% of named roles before their first gate, drill or signature | Training records |
| Assigned Representative roster currency | Reviewed within 30 days of any personnel change; at least two active | Roster in the system of record |
| Standards and guidance review held | Quarterly, with a dated re-mapping decision | Review minutes |

### Board reporting cadence and content

The executive sponsor reports to the board quarterly, aligned with the executive review (Section 2). The report is short and reads from the KPIs.

1. Portfolio status: products in scope by class and wave; the share with a decision record, signed risk assessment, complete file and DoC.
2. The constraint: notified-body status for each Class I and II product, slot dates and the fallback.
3. Reporting performance: live cases and drills against the 24-hour and 72-hour targets; roster currency.
4. Risk: open high-risk findings, residual-risk acceptances and any appeal the sponsor decided.
5. Exposure: the Art 64 tiers, Member States with enforcement laws in force (three adopted on 30 Oct 2026; Germany awaiting promulgation), the PLD from 9 Dec 2026.
6. Money: spend against the budget lines above and any re-forecast.
7. Changes in the authority stack since the last report: FAQ or guidance versions, OJ citations, designations, delegated or implementing acts.
8. Decisions requested of the board, if any, with the written basis.

Keep the board aware that the authority stack is non-binding and moving. A board that signs off a programme built on a draft guidance version should know when that version changes.

### Programme checklist

- [ ] Waves defined by class and revenue, with one representative product per family in Wave 1
- [ ] Phase 0 reporting readiness complete for the whole portfolio, legacy included
- [ ] Budget lines approved with benchmark labels retained in the papers
- [ ] KPIs wired to the system of record and the scope register, not to manual reporting
- [ ] Notified-body contracting milestone set for Q1 2027 with a fallback body
- [ ] Board report template agreed with the eight items above
- [ ] Wave review trigger set for any OJ citation, guidance version or designation
