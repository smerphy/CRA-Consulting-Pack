## 4. Portfolio inventory and scope register

The scope register is the record every other CRA artefact hangs off, and the first pass almost always undercounts. One consultancy reports inventories growing five-fold once versions, OEM-branded units, companion apps and cloud functions are counted ([OmniTrust](https://omnitrust.com/blog/eu-cra-tales-from-the-trenches-2-the-first-problem-isnt-security-its-scope/), consultancy claim). A register that lists only marketed SKUs will leave products unassessed on 11 Dec 2027.

This section gives the data model, the build method, the decision-record format and the change triggers. The scope tests themselves are in the knowledge base, Scope: what the CRA covers, and the class tests in Product classification.

### Data model

One row per product version, grouped into families and lineages. The "why" column says which obligation the field serves; the source article is where the obligation sits in [Regulation (EU) 2024/2847](https://eur-lex.europa.eu/eli/reg/2024/2847/oj).

| Field | Why | Source article or guidance |
|---|---|---|
| Product id | Stable key joining the register to the technical file, SBOMs, DoCs and case files | Art 13(15) type, batch or serial identification |
| SKU and version lineage | Obligations attach per unit at placing; for software, all copies of a version are deemed placed at first offering. The version is the unit of compliance | Art 3(21)-(22); guidance paras 13-14 |
| Hardware, software and RDPS boundary | Annex I reaches manufacturer-built back-ends needed for a product function; the boundary decides what the risk assessment covers | Art 3(2); Recitals 11-12; guidance Section 8 |
| Companion apps | A mobile or desktop app supplied with the product is itself a product with digital elements, with its own version lineage | Art 3(1); guidance paras 20-21 |
| Variants and families | A family sharing architecture, security-relevant design, intended purpose and risks may share one risk assessment, one technical file and one DoC | Guidance paras 174-177 |
| Markets | Which Member States the product is made available in; drives the DoC language rule and which MSAs can ask | Art 28(2); Art 52(1) |
| Role per market | Manufacturer, importer, distributor or authorised representative; own-brand resale or substantial modification makes you manufacturer | Arts 3(13)-(17), 18-22 |
| Placing date per version | Units placed before 11 Dec 2027 are caught only on substantial modification; Art 14 applies regardless | Art 69(2)-(3) |
| Scope decision and basis | In, out or RDPS, with the test applied and the guidance paragraphs relied on | Art 2(1); guidance Section 2 |
| Class and core-functionality rationale | Default, Class I, Class II or critical, judged on core functionality against the technical descriptions | Art 7; Annexes III-IV; [Implementing Regulation (EU) 2025/2392](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32025R2392); guidance Section 6 |
| Conformity route | Module A, B+C, H or a certificate; Class I needs B+C or H while no harmonised standard is cited | Art 32; Annex VIII; guidance paras 148-151 |
| Support period and end date | Declared per product and per substantially modified software version; month and year shown at purchase | Art 13(8), (19); guidance Section 5 |
| Notified body | Which body, which module, certificate id and surveillance dates | Art 32; Annex VIII Modules B and H |
| DoC id | Which declaration covers this version, who signed it and when | Art 28; Annex V; Section 2 |
| Art 14 coordinator CSIRT | The Member State and CSIRT this product's reports route to | Art 14(7) |
| Legacy flag | Placed before 11 Dec 2027 and not substantially modified since: reportable, not otherwise regulated | Art 69(2)-(3); FAQ Section 5.3 |
| Owner | The product manager and engineering lead accountable for keeping the row true | Section 2 RACI |
| Last reviewed | Date and reviewer of the last scope and class check | Programme board cadence |

Two fields need discipline. The RDPS boundary field must name the functions the product cannot perform without each back-end, the three-element test in guidance Section 8. The class field must record the one core functionality, since separately sold modules are separate products (guidance Section 6).

### How to build it

1. Start from the release system: every tagged release, firmware image, installer and app-store build of the last support period, not the current catalogue.
2. Join the commercial systems: SKUs, price lists, OEM and white-label agreements, reseller contracts and bundles, so own-brand resale and rebranding surface (Art 21).
3. Reconcile with cloud and app stores: list every back-end a product talks to and every app-store listing. Classify each as RDPS, third-party component or out of scope (guidance Section 8).
4. Add acquisitions and legacy lines, where documentation often has to be recreated and classifications are inconsistent ([OmniTrust](https://omnitrust.com/blog/eu-cra-tales-from-the-trenches-2-the-first-problem-isnt-security-its-scope/), consultancy).
5. Run the scope test on each row with a cross-functional group: product, engineering, security, legal and quality. Consultancy practice recommends this mix.
6. Record a decision record for each product (below) before the class test, because class depends on the scope boundary.
7. Fix the economic-operator role per market and flag any market where there is no EU importer or representative (see Section 10).
8. Baseline the register and put it under change control, with the triggers below.

Expect the first count to be wrong. Plan a second reconciliation pass after the first release-gate run, when engineering discovers the components and services the register missed.

### Decision records

Each product gets one scope and classification decision record, held in the system of record (Section 8) and referenced from the register. The record is what a market surveillance authority or notified body will read first.

| Element | Content |
|---|---|
| Decision | In scope, out of scope, or RDPS of a named product; class and conformity route |
| Basis | The three cumulative scope conditions of Art 2(1) applied to this product; the core-functionality test; the exclusion considered (Art 2(2)-(7)) |
| Guidance relied on | Paragraph and example numbers from guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) and section numbers from [FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307), with the versions used |
| Who | The compliance lead as accountable, the product and engineering leads as responsible, legal as consulted (Section 2 RACI) |
| Date | Decision date and the date of the guidance versions relied on |
| Review trigger | Which of the change triggers below reopens the record |
| Open points | Anything unresolved, such as dual licensing or paid hosting where the guidance is silent |

Because the guidance is non-binding and still formally a draft, the record must say which version it relied on. When a later FAQ version or a cited harmonised standard changes the answer, the record is superseded, not edited.

### The per-version rule for software

For standalone software, the register treats each version as the unit placed on the market. Guidance paras 13-14 deem all copies of a version placed at the moment the version is first offered.

A version that is a substantial modification is a new placing and needs its own declared support period (guidance paras 104-124, 128). It may also need its own DoC (FAQ Section 6.8).

The register therefore needs the release engineering feed, not a quarterly product list. The release gate (knowledge base, Engineering compliance programme) is where the security-delta assessment decides whether a release opens a new lineage row.

### Ownership and change triggers

The compliance lead owns the register; product management owns each row's commercial fields and engineering owns the technical ones. The register is reviewed at the monthly programme board (Section 2).

| Trigger | What reopens | Who raises it |
|---|---|---|
| New SKU, bundle or OEM agreement | Scope decision, role per market, family membership | Product management |
| New market or sales channel, including a marketplace or direct-to-consumer site | Role per market, importer or representative, DoC language, CSIRT routing for non-EU manufacturers | Product management with legal |
| Substantial modification found at the release gate | New version row, new placing date, support-period reassessment, DoC review, classification re-check | Engineering lead |
| Module unbundling or a function sold separately | New product with its own core functionality and class | Product management |
| New or changed back-end, or a third-party SaaS integrated | RDPS boundary, component due diligence | Engineering lead |
| Acquisition or divestment | Whole register section; roles and brands | Legal |
| New guidance version, OJ citation or implementing act | Decision records relying on the changed text | Compliance lead (quarterly review) |
| End of support reached | Legacy flag, reportable-only status | Product management |

### Register checklist

- [ ] Every release of the last support period is a row, including companion apps and app-store builds
- [ ] Every row has an RDPS boundary statement naming the dependent functions
- [ ] Every row has a role per market and a flagged gap where no EU operator exists
- [ ] Every product has a dated decision record naming the guidance paragraphs relied on
- [ ] Every Class I and II row has a route and a notified-body plan (Section 10)
- [ ] Legacy rows carry the Art 14 coordinator CSIRT, because they remain reportable
- [ ] Change triggers are wired to the release gate and the commercial systems, not to a calendar
