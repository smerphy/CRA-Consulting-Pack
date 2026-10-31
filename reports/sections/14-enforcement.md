## Enforcement, market surveillance and penalties

Market surveillance authorities enforce the [CRA](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) from 11 Dec 2027 with fines of up to EUR 15m or 2.5% of worldwide turnover (Art 64(2)). Their tools are document access on reasoned request (Art 53) and corrective orders up to recall (Arts 54-58). Four Member States (Finland, Hungary, Malta, Germany) have enforcement laws in place as of 30 Oct 2026.

Most others are drafting, and Finland alone already enforces Art 14 breaches. Enforcement is national under [Regulation (EU) 2019/1020](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019R1020), to which Art 66 adds the CRA.

### Powers and procedures (Chapter V)

Article text was read from mirrors, not the authentic OJ text; article references are to Regulation (EU) 2024/2847.

| Article | Power or procedure | What it means for you |
|---|---|---|
| Art 52(1)-(2) | Reg 2019/1020 applies; each Member State designates one or more market surveillance authorities (MSAs) | Your MSA is in the Member State where the product is made available, not only where you are established |
| Art 52(3) | MSAs supervise stewards' Art 24 duties and may require "all appropriate corrective actions" | Steward exposure is corrective action, not fines; see Open-source software |
| Art 52(4)-(5) | Cooperation with national certification authorities, coordinator CSIRTs and ENISA, which may give technical advice or analysis | Expect the CSIRT that received your Art 14 report to be consulted during an evaluation |
| Art 52(7) | Cooperation with data protection authorities, which may request and access CRA documentation | Keep the technical file in a form you can share with a DPA |
| Art 52(10)-(11) | MSAs may advise economic operators; consumer complaints route via Reg 2019/1020 Art 11 | A customer complaint can start a file |
| Art 52(14) | AI Act market surveillance authorities perform CRA surveillance for high-risk AI systems | One authority for both regimes on AI products |
| Art 52(15)-(16) | ADCO under Reg 2019/1020 Art 30(2); publishes statistics and indicative guidance on support periods and may recommend enforcement focus | The CRA ADCO is operational, chaired by BSI with Cyprus's Digital Security Authority as vice-chair ([Expert Group minutes, 10-11 Jun 2026](https://ec.europa.eu/transparency/expert-groups-register/core/api/front/document/135392/download)) |
| Art 13(25) | ADCO may run a Union-wide dependency assessment; MSAs may request SBOMs from manufacturers of the relevant categories, passed on anonymised and aggregated | SBOM requests can arrive outside any investigation of your product |
| Art 53 | On "reasoned request", access to data "required to assess the design, development, production and vulnerability handling", including internal documentation, in a language the MSA easily understands | The mirror served one paragraph and no source-code wording; whether Art 53 expressly reaches source code is not verified against the OJ text, confirm before relying on it |
| Art 16(3) | CSIRTs pass actively-exploited-vulnerability and severe-incident information to the MSAs of their Member States | Every Art 14 report is visible to the enforcer; ENISA may also propose sweeps from Art 14 data (Art 60) |
| Art 54 | National procedure for a product presenting a "significant cybersecurity risk": evaluation, possibly with the CSIRT; corrective action, withdrawal or recall within a period "commensurate with the nature of the cybersecurity risk"; provisional measures notified EU-wide; no objection within three months means the measure is "deemed to be justified" and all Member States follow | Art 54(2) imports non-technical risk factors from NIS2 Art 22 supply-chain assessments, so supplier origin can be an enforcement factor |
| Art 55 | Union safeguard procedure: on objection the Commission decides within nine months of the Art 54(5) notification; standards shortcomings go to Reg 1025/2012 Art 11 | A single national finding can become an EU-wide withdrawal |
| Art 56 | Commission implementing acts requiring corrective or restrictive measures where national action is absent or ineffective, including on ENISA information | Reserved for exceptional situations; examination procedure under Art 62(2) |
| Art 57 | Compliant products that still present a significant risk to health, safety, fundamental rights or essential services may be withdrawn or recalled | Conformity is not a complete defence |
| Art 58 | Formal non-compliance: CE marking wrongly affixed or missing, DoC absent or incorrect, notified-body number missing, technical documentation unavailable or incomplete; restrict, prohibit, withdraw or recall if it persists | Paperwork defects are enforceable on their own |
| Art 59 | Joint activities on products "often found to present cybersecurity risks"; the Commission or ENISA may propose joint compliance checks; agreements are public | Watch published agreements for your product category |
| Art 60 | Coordinated "sweeps", including inspection of products bought under a "cover identity" | Assume test purchases of retail and online products from 11 Dec 2027 |

### Penalties (Art 64)

| Tier | Maximum | Which breaches | Notes |
|---|---|---|---|
| Art 64(2) | EUR 15,000,000 or 2.5% of total worldwide annual turnover, whichever is higher | Annex I essential requirements; manufacturer obligations in Arts 13 and 14 | The percentage exceeds the fixed cap only above about EUR 600m turnover |
| Art 64(3) | EUR 10,000,000 or 2% | Arts 18-23 (representatives, importers, distributors, rebranding and modification, identification), 28 (DoC), 30(1)-(4) (CE marking), 31(1)-(4) (technical documentation), 32(1)-(3) (conformity assessment), 33(5), 39, 41, 47, 49 (notified bodies), 53 (access to data) | An importer that rebrands or substantially modifies moves to the top tier via Art 21 |
| Art 64(4) | EUR 5,000,000 or 1% | Incorrect, incomplete or misleading information to notified bodies or MSAs in reply to a request | Applies to the content of your reasoned-request responses |
| Art 64(5) | Factors | Nature, gravity, duration and consequences; prior fines for similar breaches; size and market share, with regard to micro, small and start-up enterprises | Recital 121 adds income level for non-undertakings |
| Art 64(10)(a) | Exemption | Micro and small enterprise manufacturers for missing the 24-hour early warnings in Art 14(2)(a) and 14(4)(a) | The 72-hour and final-report deadlines remain fineable |
| Art 64(10)(b) | Exemption | Any infringement by open-source software stewards | Recital 120: no other pecuniary penalties either |
| Art 64(1), (6)-(9) | National rules | Member States set "effective, proportionate and dissuasive" penalties and notify the Commission; fines shared via ICSMS; each state decides whether public authorities can be fined (64(7)); courts or other bodies may impose them (64(8)); fines may combine with corrective measures (64(9)) | Fines apply from 11 Dec 2027 with the rest of the Regulation |

Malta has chosen not to copy the tiers. Legal Notice 238 of 2026 applies the MDIA Act Part VIII regime of EUR 350,000 per infringement plus EUR 12,000 per day ([Hogan Lovells, Oct 2026](https://www.hlc.com/en/publications/eu-cyber-resilience-act-germany-adopts-cra-implementation-act-as-national-enforcement-regimes)). That rises to 5% of turnover where there is significant market effect; other states have so far mirrored Art 64.

### Member State implementation

Verified subset only; no official EU-wide tracker was found, and Austria, Belgium, Sweden, Poland, Portugal and Czechia among others were not checked.

| Country | Authority | Law | Status and date |
|---|---|---|---|
| Finland | Traficom (NCSC-FI): market surveillance and notifying authority | Act 439/2026 | Adopted; in force 1 Jun 2026; Art 14 breaches enforceable since 11 Sep 2026 ([Traficom](https://www.kyberturvallisuuskeskus.fi/en/our-activities/regulation-and-supervision/cyber-resilience-act-cra/business-opportunities-notified-bodies-under-cra)) |
| Hungary | SZTFH: both roles | Act CXXXV of 2025 | Adopted; follows the Art 71(2) timeline |
| Malta | Malta Digital Innovation Authority: both roles from 11 Dec 2027 | [Legal Notice 238 of 2026](https://www.cyberresilienceact.eu/news/malta-names-cra-enforcement-authorities-11-september-2026.html) | Adopted 11 Sep 2026; own fine regime |
| Germany | BSI: sole market surveillance authority, notifying authority and CSIRT (BNetzA for high-risk AI) | CRA Implementation Act, new Part 8 BSIG | Passed the Bundestag 14 Oct 2026, Bundesrat did not object; fines in Secs 68-69 BSIG from 11 Dec 2027; the [BSI CRA page](https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Cyber_Resilience_Act/cyber_resilience_act_node.html) of 11 Sep 2026 still says no national implementation is needed |
| Netherlands | RDI: both roles | Uitvoeringswet verordening cyberweerbaarheid | Draft in the legislative process |
| Italy | ACN: both roles | Draft decree, Government Act No 447 | Draft sent to Parliament 9 Oct 2026 |
| Denmark | Danish Resilience Agency (Styrelsen for Samfundssikkerhed): both roles | Draft act | Consultation from 5 Oct 2026; entry planned 11 Dec 2027 |
| Spain | Secretary of State for Telecommunications (market surveillance); CCN (notifying); INCIBE (CSIRT) | Draft royal decree | Consultation Dec 2025; not adopted; no penalty regime published ([Innovatech Legal, 7 Oct 2026](https://innovatech.legal/en/digital-regulation/cyber-resilience-act-penalties/)) |
| France | ANSSI: notifying authority only | Décret n° 2026-944 of 9 Oct 2026 | Adopted for Chapter IV; no market surveillance or fine rules yet |
| Ireland | NCSC anticipated | None | Not formally designated as of 14 Sep 2026 ([Legal 500](https://www.legal500.com/intelligence/european-union/media-telecoms-it-entertainment/the-eu-cyber-resilience-act-reporting-obligations-take-effect)) |

Because Art 64(1) obliges every Member State to notify its penalty rules, expect a burst of national acts in the first half of 2027. Capacity will be uneven on 11 Dec 2027.

### Being ready for a reasoned request

Have the Annex VII technical file retrievable per product version. It should contain the risk assessment with its Annex I applicability matrix, the SBOM, the vulnerability-handling process description, test reports and the DoC. Annex VII point 8 names the SBOM as a reasoned-request item in its own right.

Art 13(22) requires all information and documentation showing conformity of the product and your processes, on paper or electronically, in a language the authority understands. The text as read sets no fixed response deadline, so agree one internally and name the owner.

An authorised representative or importer must hold the DoC and technical documentation for 10 years or the support period, whichever is longer (Arts 18(3), 19). The file must therefore exist outside engineering tooling.

Expect requests to be informed by your own filings. Art 16(3) feeds every Art 14 report to the MSAs, and Art 60 lets ENISA propose sweeps from that data. Log who answered what and when; a careless answer is itself a breach under Art 64(4).
