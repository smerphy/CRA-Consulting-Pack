## Economic operators and roles

The manufacturer carries almost every obligation in the [CRA](https://eur-lex.europa.eu/eli/reg/2024/2847/oj): Art 13 alone has 25 paragraphs, and Art 14 reporting sits with the manufacturer too. The real question for each product is therefore who the manufacturer is. Art 3(13) answers it by brand, not authorship: whoever markets the product under its own name or trademark, paid or free.

### The roles

| Role | Definition and article | Main obligations with articles | Applies from | Notes |
|---|---|---|---|---|
| Manufacturer | Art 3(13): develops or has developed the product and markets it under its own name or trademark, for payment or free | Annex I Part I design controls (Art 13(1)); risk assessment maintained through the support period (Art 13(2)-(4)); component due diligence and upstream reporting (Art 13(5)-(7)); support period and update availability (Art 13(8)-(11)); technical documentation, conformity assessment, declaration, CE marking (Art 13(12)-(13)); contact details and single point of contact (Art 13(15)-(17)); user information and end-of-support date (Art 13(18)-(20)); corrective action and cessation notice (Art 13(21)-(23)); reporting (Art 14) | Art 14 since 11 Sep 2026; the rest 11 Dec 2027 | Top fine tier, EUR 15m or 2.5% of worldwide turnover (Art 64(2)) |
| Authorised representative | Art 3(15): EU-established person with a written mandate from the manufacturer; Art 18(1) says a manufacturer "may" appoint one | Keep the declaration and technical documentation for 10 years or the support period; supply information on reasoned request; cooperate with authorities (Art 18(3)) | 11 Dec 2027 | Optional. Art 18(2) bars delegating Art 13(1)-(11), Art 13(12) first subparagraph and Art 13(14): design, risk assessment, support period, documentation and conformity assessment stay with the manufacturer |
| Importer | Art 3(16): EU-established person placing on the market a product bearing a non-EU name or trademark | Place only compliant products (Art 19(1)); verify conformity assessment, documentation, CE marking, declaration and Annex II information (Art 19(2)); withhold non-conforming products and alert authorities (Art 19(3)); add own name and contact details (Art 19(4)); inform the manufacturer of vulnerabilities "without undue delay" (Art 19(5)); keep the declaration 10 years or the support period; notify if the manufacturer ceases operations (Art 19(6)-(9)) | 11 Dec 2027 | Second fine tier, EUR 10m or 2% (Art 64(3)) |
| Distributor | Art 3(17): supply-chain person who makes the product available without affecting its properties | Act with due care (Art 20(1)); verify the CE marking and that manufacturer and importer met Art 13(15), (16), (18), (19), (20) and Art 19(4) (Art 20(2)); withhold products believed non-conforming (Art 20(3)); inform the manufacturer of vulnerabilities without undue delay (Art 20(4)); cooperate; notify on cessation (Art 20(5)-(6)) | 11 Dec 2027 | Not required to bring pre-11 Dec 2027 stock into compliance unless it substantially modifies it (FAQ) |
| Open-source software steward | Art 3(14): legal person, other than a manufacturer, systematically sustaining FOSS intended for commercial activities | Documented, verifiable cybersecurity policy (Art 24(1)); cooperate with authorities and supply the policy on reasoned request (Art 24(2)); Art 14 reporting only to the extent involved (Art 24(3)) | 11 Dec 2027 | No CE marking, no fines (Art 64(10)(b)); see Open-source software |
| Any other person who substantially modifies | Art 22(1): a person other than manufacturer, importer or distributor who substantially modifies a product and makes it available | Becomes manufacturer for the modified part, or for the whole product where the modification affects its cybersecurity as a whole (Art 22(2)) | 11 Dec 2027 | The original manufacturer's duties continue for the original product (guidance paras 117-121) |
| Fulfilment service providers and online marketplaces | Not CRA economic operators unless they manufacture, import or distribute (Recital 78) | Reg (EU) 2019/1020 Art 6 deems online offers targeted at EU users "made available"; GPSR Art 16 applies to consumer products via CRA Art 11 for safety risks the CRA does not cover | 11 Dec 2027 | A marketplace selling its own-branded products is a manufacturer (Recital 78) |

[Guidance C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) adds a per-product rule. The same legal person can be steward for a free community edition and manufacturer for the paid edition (paras 71-74). A steward that starts monetising becomes manufacturer from that date, not for earlier versions (para 84).

### When you become the manufacturer

Work through this list for every product, variant and resale arrangement.

- [ ] Own brand or trademark. An importer or distributor that places a product on the market under its own name or trademark is the manufacturer (Art 21). It takes on Arts 13 and 14 in full; the original developer's compliance is evidence, not a transfer of responsibility.
- [ ] Substantial modification (test in Scope: what the CRA covers). An importer or distributor that substantially modifies a product becomes its manufacturer (Art 21). Anyone else becomes manufacturer for the affected part, or the whole product if its security as a whole is affected (Art 22).
- [ ] Integration into a new product. Assembling third-party components, even modified ones, into a product you place on the market is not substantial modification. You are the manufacturer of the new product "in its entirety" (guidance para 120, Example 51: an agricultural monitor built from third-party microcontroller modules).
- [ ] White-label and resale. Same result as own brand: full manufacturer duties (Art 21; Recital 78).
- [ ] A distributor who patches. Installing or configuring software on a customer's systems without substantial modification is not placing it on the market (guidance para 59, Example 19). One who substantially modifies it as part of the service falls under Art 22.
- [ ] Software you host but the customer runs. If the customer obtains and runs the software, it is a product and you are its manufacturer. If the customer only accesses it in a browser, it is at most remote data processing for one of your products (guidance paras 20-21).
- [ ] Free software from a company. Free supply in a commercial activity is making available (Art 3(22); Recital 15); unmonetised FOSS makes a company a steward at most (guidance paras 67-68). A free closed-source app with no monetisation is a grey area the guidance resolves case by case (paras 40-41).
- [ ] Outsourced development. A product you had developed and sell under your brand is yours (Art 3(13) "has ... developed").

### Non-EU manufacturers, including the UK

The CRA itself imposes no mandatory EU representative, because Art 18 is permissive. CRA Art 66 adds the CRA to Annex I of [Regulation (EU) 2019/1020](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32019R1020) but not to its Art 4(5) list. Only that list requires an EU responsible economic operator.

The scope notes initially inferred otherwise; the timeline notes checked the Art 4(5) list and found the CRA absent. Treat the absence as the better-supported reading, but confirm with counsel.

What the CRA does require is that whoever places the product on the EU market is an importer (Art 19) with verification and record duties. In a pure direct-to-consumer model there is no importer, because a consumer does not act in a commercial activity. The manufacturer then carries Arts 13-14 alone.

Other laws close that gap for many products. Radio equipment is listed in Reg 2019/1020 Art 4(5), so an EU responsible operator is mandatory anyway. Consumer products outside other harmonisation law pick up the GPSR Art 16 responsible-person rule through CRA Art 11.

From 9 Dec 2026, [Directive (EU) 2024/2853](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024L2853) Art 8 adds liability. Where no EU importer or authorised representative exists, the EU fulfilment service provider or online platform is liable. The practical advice in the notes is to appoint an authorised representative even though Art 18 is optional.

Reporting routes through the CSIRT of the main-establishment Member State, where product cybersecurity decisions are predominantly taken (Art 14(7)). A manufacturer with no EU establishment uses, in order, the Member State of its authorised representative, importer, distributor, or most users. ENISA's [SRP FAQ](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/frequently-asked-questions) warns that a wrong CSIRT choice may invalidate the filing; see Reporting obligations (Article 14).

UK and Northern Ireland detail is in Interplay with other law, the Digital Omnibus and the UK position.

### Record-keeping and contacts

| Duty | Article | What to keep or publish | Period |
|---|---|---|---|
| Traceability up and down the chain | Art 23 | Name and address of every operator that supplied you and, where available, every operator you supplied | 10 years after being supplied and 10 years after supplying |
| Identification on the product | Art 13(15)-(16); Art 19(4) | Type, batch or serial number; manufacturer and importer name, trade name or trademark, postal address, email or digital contact, website, on the product, packaging or accompanying document and in the Annex II information | For the life of the product |
| Single point of contact for users | Art 13(17) | Easily identifiable channel for reporting and receiving vulnerability information; must not be limited to automated tools | Throughout the support period |
| Technical documentation and declaration | Art 13(13); Art 18(3) | Annex VII dossier and EU declaration of conformity available to authorities; the authorised representative may hold them | At least 10 years after placing on the market or the support period, whichever is longer |
| User information | Art 13(18) | Annex II information in a language users and authorities understand | At least 10 years or the support period, whichever is longer |
| Cessation of operations | Art 13(23); Art 19(9); Art 20(6) | Manufacturer informs authorities and users before ceasing; importers and distributors inform authorities and users if the manufacturer has ceased | Before cessation |

Vulnerability information flows upstream and downstream. Importers (Art 19(5)) and distributors (Art 20(4)) must inform the manufacturer of vulnerabilities without undue delay. They must also alert authorities where there is a significant cybersecurity risk.

Manufacturers must report vulnerabilities found in components, including open-source ones, to the component maintainer and share fixes (Art 13(6)). Fixes go "where appropriate in a machine-readable format". Actively exploited vulnerabilities and severe incidents are reported under Art 14; see Reporting obligations (Article 14).

Article references in this section were checked against the OJ text on 1 Nov 2026 (E6). The fine tier for Arts 18-23 breaches (EUR 10m or 2%) is confirmed in Art 64(3).
