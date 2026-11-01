## Interplay with other law, the Digital Omnibus and the UK position

The [CRA](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) sits beside the other regimes rather than replacing them, and only the AI Act carries a deemed-compliance rule (CRA Art 12(1)). The RED cybersecurity delegated act is repealed with effect from 11 Dec 2027. The Product Liability Directive makes a vulnerability a potential defect from 9 Dec 2026.

The Digital Omnibus does not amend the CRA. A GB manufacturer is a third-country manufacturer, and the CRA does not apply in Northern Ireland as of 30 Oct 2026.

### Instrument by instrument

| Instrument | Relationship to the CRA | Cross-reference | Engineering consequence |
|---|---|---|---|
| NIS2, Directive (EU) 2022/2555 (not opened directly; read through CRA recitals) | Complementary: NIS2 regulates entities, the CRA regulates products; cloud services are CRA-relevant only as the manufacturer's remote data processing | CRA recitals 12, 13, 24, 72; Arts 54(2), 56(2) (NIS2 Arts 8, 22); Art 16(2) (NIS2 Art 12) | Expect NIS2 customers to demand the DoC, SBOM, support period and CVD policy under NIS2 Art 21(2)(d); document the remote-data-processing boundary; CRA and customer NIS2 reports stay separate |
| RED Delegated Regulation (EU) 2022/30, repealed by [Delegated Regulation (EU) 2026/339](https://eur-lex.europa.eu/eli/reg_del/2026/339/oj/eng) (OJ 29 Apr 2026, in force 19 May 2026) | Replacement from 11 Dec 2027; CRA Annex I includes all RED Art 3(3)(d)-(f) elements (recital 30) | Del Reg 2026/339 Arts 1-2, recitals 3-5; CRA recitals 30, 100; Art 69(1) | Radio equipment placed 1 Aug 2025 to 10 Dec 2027 stays under RED and EN 18031; RED type-examination certificates remain valid to 11 Jun 2028 but evidence RED, not CRA, conformity; EN 18031 test evidence is partly reusable against EN 40000-1-4 |
| AI Act, Regulation (EU) 2024/1689, amended by [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32026R1744) | The only true deemed-compliance rule: a high-risk AI system meeting CRA Annex I Parts I and II, with the DoC saying so, meets AI Act Art 15 cybersecurity | CRA Art 12(1)-(4), Art 52(14), recital 51; AI Act Art 42(3) as inserted by Reg 2026/1744; AI Act Art 43 route | One risk assessment can serve both regimes if it covers data poisoning and adversarial inputs; important or critical products using AI Act Annex VI internal control follow CRA procedures; AI Act Annex I products apply from 2 Aug 2028, after the CRA |
| GDPR, Regulation (EU) 2016/679 | Unaffected; CRA controls support data protection by design | CRA recital 32; Art 52(7) (DPA cooperation and access to CRA documentation); recital 72 | A breach can start GDPR Art 33 (72 h, controller) and CRA Art 14 (24 h, manufacturer) clocks at once; keep the technical file DPA-shareable |
| [Data Act, Regulation (EU) 2023/2854](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32023R2854) | No cross-reference in either text; parallel design duties for connected products placed after 12 Sep 2026 | Data Act Art 3(1); recital 31 | Build authenticated, logged data-export interfaces; do not treat user data access as an attack surface to close |
| eIDAS, Regulation (EU) No 910/2014 (EUDI Wallet, Art 5a) | Cumulative; a Cybersecurity Act certification scheme may give presumption for both | CRA recital 33 | Wallet software is a CRA product; plan for the EUDI Wallet scheme (Implementing Reg 2024/2981) as the dual route |
| Machinery Regulation (EU) 2023/1230, applies 20 Jan 2027 | Cumulative; CRA compliance "could facilitate" Annex III 1.1.9 and 1.2.1, not a presumption | CRA recital 53; [Machinery Reg Art 20(9)](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32023R1230) presumes only for Reg 2019/881 certificates | Map one risk assessment to both annexes; keep the 5-year safety-software intervention log; run both conformity procedures |
| MDR 2017/745, IVDR 2017/746, vehicles Reg 2019/2144, EASA-certified aviation, Marine Equipment Directive 2014/90/EU | Excluded | CRA Art 2(2)-(4); recital 25; [Delegated Regulation (EU) 2025/1535](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32025R1535) (L-category vehicles) | Medical-device software stays under MDR/IVDR; a generic module sold separately for medical use remains a CRA product |
| [Product Liability Directive (EU) 2024/2853](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024L2853), applies 9 Dec 2026 | No express cross-reference, but software is a product and a vulnerability can be a defect | PLD recital 32; Art 7(2)(f); Art 10(2)(b); Art 11(2)(c); Art 9 disclosure | From 11 Dec 2027 breach of Annex I creates a rebuttable presumption of defect; missing security updates remove the later-defect defence; the technical file and update logs become disclosable evidence |
| [DORA, Regulation (EU) 2022/2554](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R2554) | No cross-reference either way; recital 72 names DORA only as a parallel reporting regime | [DORA Art 28(5)](https://www.digital-operational-resilience-act.com/Article_28.html) "highest quality information security standards" | CRA conformity is the natural evidence for bank and insurer procurement, not a safe harbour; CRA Art 14 and DORA Art 19 reports stay separate; AFME's Jul 2026 request to report under DORA only is a request, not law |
| Cybersecurity Act 2019/881; EUCC ([Implementing Reg 2024/482](https://certification.enisa.europa.eu/browse-topic/EUCC_en)); EUCS; CSA2 | A certificate at level "substantial" or higher removes third-party assessment for covered requirements, once an Art 27(9) delegated act exists | CRA Arts 8, 27(8)-(9), 52(4); recitals 46-48, 81-82 | Art 27(9) act "planned Q4 2026" on the [Commission factpage](https://digital-strategy.ec.europa.eu/en/factpages/cyber-resilience-act-implementation), not adopted; EUCS unadopted per [COM(2026) 502](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX%3A52026PC0502); CSA2 proposed 20 Jan 2026, trilogue status not verified; do not plan on a cloud certificate |
| [General Product Safety Regulation (EU) 2023/988](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32023R0988) | GPSR Chapter III Section 1, including Art 16, applies to safety risks the CRA does not cover | CRA Art 11 | An EU responsible person is needed for consumer products outside other harmonisation law |
| [Market Surveillance Regulation (EU) 2019/1020](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019R1020) | Applies to CRA products; the CRA is added to Annex I but not to Art 4(5) | CRA Arts 52(1), 66; Reg 2019/1020 Arts 4, 6 | The CRA itself imposes no mandatory EU responsible operator; Art 6 deems EU-targeted online offers "made available"; the CRA is inserted as point 72 of Annex I (Art 66, OJ text) |

### The Digital Omnibus

The AI Omnibus is law. [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/eli/reg/2026/1744/oj/eng) (OJ 24 Jul 2026, in force 27 Jul 2026) inserted AI Act Art 42(3). It also moved high-risk application to 2 Dec 2027 for Annex III systems and 2 Aug 2028 for Annex I product-embedded systems.

The data and cyber Omnibus, [COM(2025) 837](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52025PC0837) of 19 Nov 2025 (procedure 2025/0360(COD)), is a proposal, not adopted as of 30 Oct 2026. It does not list the CRA among the acts it amends. The operative articles were only partly retrieved, so that finding rests on the explanatory memorandum and secondary sources.

| Element | Commission proposal (19 Nov 2025) | Council mandate ([ST 14756/26](https://data.consilium.europa.eu/doc/document/ST-14756-2026-INIT/en/pdf), Coreper 21 Oct 2026) |
|---|---|---|
| Entry point | New NIS2 Art 23a: ENISA single entry point that "may" build on the CRA platform | National entry points (new Art 23b); ENISA "incident reporting information point" that cannot receive notifications |
| Mandatory use | NIS2, GDPR, DORA, eIDAS, CER | Same regimes, national portals |
| GDPR Art 33 | 72 h to 96 h | 96 h kept; high-risk breaches only |
| CRA and NIS2 | NIS2 Art 23(12): a CRA Art 14(3) severe-incident report with the Art 23(4) content counts as the NIS2 report | Kept |
| Application | 18 months, extendable to 24 | Fallback 30 months |

Parliament has not voted. The [OEIL file](https://oeil.europarl.europa.eu/oeil/en/procedure-file?reference=2025%2F0360%28COD%29) shows joint ITRE/LIBE committees, rapporteurs Aura Salla and Marina Kaljurand, and a draft report of 22 Jun 2026. Over 1,750 amendments were tabled on 27 Jul 2026; status is "awaiting committee decision" with no trilogue.

For a CRA manufacturer nothing changes in Art 14 before 2028; see Reporting obligations (Article 14).

### United Kingdom and Northern Ireland

A GB manufacturer selling into the EU is a third-country manufacturer and carries Arts 13 and 14 itself. Its EU importer carries Art 19 duties. An Art 18 authorised representative is optional and cannot take over Art 13(1)-(11), 13(12) first subparagraph or 13(14).

Art 14(7) routes reports to the CSIRT of the authorised representative, then the importer, then the distributor, then where most users are. Three parallel rules make an EU responsible operator effectively necessary for direct-to-consumer sales. [Reg 2019/1020](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019R1020) Art 4(5) requires one for radio equipment, and [GPSR](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32023R0988) Art 16 applies via CRA Art 11.

PLD Art 8 adds the third: where no EU importer or authorised representative exists, liability falls on the fulfilment service provider (Art 8(1)(c)(iii)); an online platform is liable only if it fails to identify an EU operator within one month of a request and the DSA Art 6(3) conditions are met (Art 8(3)-(4)).

UK Approved Bodies can certify only for UKCA ([gov.uk UKCA guidance](https://www.gov.uk/guidance/using-the-ukca-marking), 21 Aug 2026). Module B+C or H therefore needs an EU notified body, and none is listed as of 8 Sep 2026.

Northern Ireland. The CRA is not in Annex 2 of the Windsor Framework; only Arts 66 and 68 apply, via Art 13(3) ([DSIT explanatory memorandum, 4 Dec 2024](https://www.niassembly.gov.uk/globalassets/committee-blocks/windsor-framework-democratic-scrutiny-committee/reg-eu-20242847/regulation-eu-20242847-em.pdf)). Council Decision (EU) 2025/799 of 14 Apr 2025 proposes adding it to point 47.

The Art 13(4) exchange of views ran from Jun 2025 and was reported concluded on 7 May 2026. The [DSIT memorandum of 5 May 2026](https://assets.publishing.service.gov.uk/media/69fb0d9ad0e316a40f269a51/EM_Council_Decision__EU__2025_799_signed.pdf) nonetheless says it "remains ongoing". No Joint Committee decision was found as of 30 Oct 2026.

UK agreement needs Schedule 6B safeguards, normally an NI Assembly applicability motion. If the CRA is added, [PSTI SI 2023/1007 Schedule 3](https://www.legislation.gov.uk/uksi/2023/1007/schedule/3) para 1 would switch NI supplies from PSTI to the CRA.

| Attribute | UK PSTI regime | EU CRA |
|---|---|---|
| Instrument | [PSTI Act 2022](https://www.legislation.gov.uk/ukpga/2022/46/part/1/chapter/3) and [SI 2023/1007](https://www.legislation.gov.uk/uksi/2023/1007/made) | Regulation (EU) 2024/2847 |
| Scope | Consumer connectable products; excepts desktops, laptops, non-cellular tablets, medical devices, smart meters, EV charge points, vehicles | All products with digital elements with a data connection, B2B and B2C |
| Requirements | Three: no default passwords, vulnerability-reporting information, published minimum support period | Annex I Part I (13 items plus risk-based design), Part II (8 lifecycle duties), Arts 13 and 14 |
| Deadlines | In force 29 Apr 2024 | Reporting 11 Sep 2026; full application 11 Dec 2027 |
| Regulator | OPSS under DSIT MoU | National market surveillance authorities; ENISA and CSIRTs for reporting |
| Maximum penalty | GBP 10m or 4% of worldwide revenue; GBP 20,000 daily | EUR 15m or 2.5% of worldwide turnover |
| Who it binds | Manufacturers, importers, distributors | Manufacturers, importers, distributors, authorised representatives, stewards |

The [Cyber Security and Resilience Bill](https://www.gov.uk/government/collections/cyber-security-and-resilience-bill) amends the NIS Regulations 2018 and imposes no product-security duties. It reached Lords Report Stage on 26 Oct 2026, with Third Reading expected 2 Nov 2026; stage dates come from vendor trackers.

The Budget of 28 Oct 2026 commits to a 2027 consultation on "insecure technology at source" and breach liability ([The Record](https://therecord.media/uk-budget-proposal-software-companies-liable-cyber-breaches)). The Law Commission's product-liability consultation runs 8 Oct 2026 to 14 Jan 2027 and would add software to the Consumer Protection Act 1987. Neither is law.
