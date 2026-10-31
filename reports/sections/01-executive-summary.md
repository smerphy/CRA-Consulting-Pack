## Executive summary

The [Cyber Resilience Act](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) (Regulation (EU) 2024/2847, the CRA) is a horizontal New Legislative Framework product law that puts CE marking on cybersecurity. It covers every product with digital elements made available on the EU market in a commercial activity, from firmware to operating systems.

It applies in full from 11 Dec 2027. Article 14 reporting has been live since 11 Sep 2026 and already covers products placed on the market earlier (Art 69(3)).

Three design choices drive the engineering workload. The manufacturer carries almost every duty, and the law reaches the manufacturer-built backends a product needs to function (Art 3(2)). Obligations attach per unit, so a unit shipped on 10 Dec 2027 escapes Annex I and one shipped next day does not (Art 69(2)).

Classification decides the conformity route (Art 32). Default products self-assess under Module A; the 26 named categories in Annexes III and IV need a notified body or a recognised certificate. Class I may self-assess only under a fully applied cited harmonised standard; none is cited on 30 Oct 2026 (see Product classification).

### State of play on 30 Oct 2026

| Item | Status on 30 Oct 2026 | Source |
|---|---|---|
| Commission FAQ | v1.4 of 4 Sep 2026, 66 pages, a "living document" that is not an official Commission position | [FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| Art 26 guidance C(2026) 5252 | Content approved 27 Jul 2026; non-binding; formal adoption in all languages still pending, so formally a draft | [Communication](https://ec.europa.eu/newsroom/dae/redirection/document/131455) and [guidance annex](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| Implementing Regulation (EU) 2025/2392 | Adopted 28 Nov 2025, in force 21 Dec 2025; technical descriptions of the 26 important and critical categories | [EUR-Lex](https://eur-lex.europa.eu/eli/reg_impl/2025/2392/oj/eng) |
| Delegated Regulation (EU) 2026/881 | Adopted 11 Dec 2025, in force 10 May 2026; when a CSIRT may delay dissemination of a notification | [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32026R0881) |
| ENISA Single Reporting Platform | Live since 11 Sep 2026; web form only, English only, mandatory Art 14 reports only | [ENISA SRP hub](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp) |
| Harmonised standards | None cited in the OJ; no common specification adopted; first citations expected in 2027 (commentary) | [Commission factpage](https://digital-strategy.ec.europa.eu/en/factpages/cyber-resilience-act-implementation) |
| Notified bodies | None verifiably designated for the CRA; Member States "strive" for enough bodies by 11 Dec 2026 (Art 35(2)) | [Commission conformity assessment page](https://digital-strategy.ec.europa.eu/en/policies/cra-conformity-assessment) |
| Digital Omnibus COM(2025) 837 | Proposed, not adopted as of 30 Oct 2026; does not amend the CRA; Council mandate 21 Oct 2026; Parliament at committee stage | [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52025PC0837) |
| RED cybersecurity delegated act | Delegated Regulation (EU) 2026/339 repeals Delegated Regulation (EU) 2022/30 with effect from 11 Dec 2027 | [EUR-Lex](https://eur-lex.europa.eu/eli/reg_del/2026/339/oj/eng) |
| AI Act | High-risk AI systems meeting Annex I are deemed to meet AI Act Art 15 (CRA Art 12; AI Act Art 42(3), inserted by Regulation (EU) 2026/1744) | [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32026R1744) |
| Product Liability Directive (EU) 2024/2853 | Applies from 9 Dec 2026; software is a product and a cybersecurity vulnerability can be a defect | [EUR-Lex](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024L2853) |

No presumption of conformity exists yet, and Class I products cannot use Module A internal control today. The guidance is the best available evidence of how market surveillance authorities will read the law. Decisions that rest on it should be recorded as reliance on a published, non-binding Commission interpretation.

Enforcement starts on 11 Dec 2027. The top fine tier is EUR 15m or 2.5% of worldwide turnover for Annex I and Arts 13-14 breaches (Art 64(2)). Only Finland, Hungary, Malta and Germany had adopted national enforcement acts by 30 Oct 2026 (see Enforcement, market surveillance and penalties).

UK manufacturers are third-country manufacturers for every EU sale. The CRA does not yet apply in Northern Ireland; see Interplay with other law, the Digital Omnibus and the UK position.

### What an engineering team must have in place

Start with what is live now: the Art 14 reporting runbook with SRP registration, and the product inventory behind scope and classification decisions. Then build the risk assessment, because every Annex I Part I item hangs off it (Art 13(3)). Everything else in the table follows from those three artefacts.

| Obligation | Legal basis | Deadline | Status today |
|---|---|---|---|
| Reporting process for actively exploited vulnerabilities and severe incidents; SRP registration; CSIRT chosen under Art 14(7) | Art 14; Art 16 | Live since 11 Sep 2026 | Mandatory now, including for legacy products (Art 69(3)) |
| Product inventory with a recorded scope decision per product, variant and backend | Art 2(1); Art 3(1)-(2) | Before 11 Dec 2027 | Guidance available; record each decision and its basis |
| Classification register (default, Class I, Class II, critical) with core-functionality rationale | Art 7; Art 8; Implementing Regulation (EU) 2025/2392 | Before 11 Dec 2027 | Technical descriptions adopted; no delegated act changes the lists |
| Cybersecurity risk assessment per product or family, stating how each Annex I Part I point (2) item applies | Art 13(2)-(4) | Before placing on the market; maintained through the support period | No mandated method; BSI TR-03183-1 v1.0.0 is a usable template |
| Annex I Part I design controls built, tested and evidenced | Art 13(1); Annex I Part I | Each placing on the market from 11 Dec 2027 | No harmonised standard cited; drafts usable as evidence only |
| Annex I Part II processes: SBOM, CVD policy, secure update mechanism, declared support period of at least 5 years | Art 13(8); Annex I Part II | From 11 Dec 2027, for the support period | SBOM format act not adopted; ENISA and BSI profiles available |
| Technical documentation (Annex VII), EU declaration of conformity (Annex V or VI), CE marking | Arts 28, 30, 31; Art 13(12)-(13) | Before placing on the market; retained 10 years or the support period | Simplified SME format not adopted |
| Annex II user information, including the end-of-support month and year at purchase | Art 13(18)-(19); Annex II | From 11 Dec 2027 | Legal text is complete; no implementing act needed |
| Conformity route chosen; notified body contracted where Module A is unavailable | Art 32; Annex VIII | Assessment complete before placing on the market | No notified body designated; pre-assessment with candidate bodies only |
| Due diligence on third-party and open-source components; upstream vulnerability reporting | Art 13(5)-(7) | From 11 Dec 2027 | FAQ gives an action list; no Art 25 attestation programme exists |

### Five facts that surprise teams

- Legacy products still report. Art 14 applies to every in-scope product placed on the market before 11 Dec 2027, and continues after the support period ends (Art 69(3)).
- The SBOM need not be public. Recital 77 says manufacturers "should not be obliged to make the SBOM public". It sits in the technical documentation and goes to authorities on reasoned request.
- Class I products cannot self-assess today. Module A needs a fully applied OJ-cited harmonised standard covering the core-functionality risks (Art 32(2); guidance para 149). Nothing is cited, and no notified body has been designated for the alternative routes.
- The authorised representative is optional. Art 18(1) says a manufacturer "may" appoint one, and the CRA adds no mandatory EU responsible operator (see Economic operators and roles).
- Manufacturer-run backends are in scope. A vendor-built API, authentication portal or update service that a product needs for a function is remote data processing. It is part of that product's conformity assessment (Art 3(2); guidance paras 184-194).
