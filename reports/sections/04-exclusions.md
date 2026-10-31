## Exclusions and exceptions

The [CRA](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) has only six narrow sectoral carve-outs in Art 2(2)-(7), plus one delegated act under Art 2(5) covering L-category vehicles. Most things teams call "exceptions" are not exclusions at all. They are either products never placed on the market, or legacy units that escape Annex I because they were placed before 11 Dec 2027.

Each exclusion is act-based. The test is whether the other EU act applies to that product, not whether the product looks medical or automotive.

### Exclusions and exceptions

| Exclusion or exception | Legal basis | What it covers | What it does not cover, watch-outs | Source |
|---|---|---|---|---|
| Medical devices and in-vitro diagnostics | Art 2(2)(a)-(b); Recital 25 | Products to which Regulation (EU) 2017/745 or 2017/746 apply, including software that is itself a device | A generic component sold to a device maker that is not itself a device stays in scope for its own manufacturer | [Commission FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| Type-approved motor vehicles | Art 2(2)(c); Recital 27 | Products to which Regulation (EU) 2019/2144 applies; components "exclusively designed" for such vehicles and sold through restricted B2B channels (guidance paras 241-246) | Generic components usable in other products, or sold through open retail or online channels, are in regardless of intended-use statements | [Guidance C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| L-category vehicles | Art 2(5); Delegated Regulation (EU) 2025/1535, in force 18 Nov 2025 | Two- and three-wheel vehicles and quadricycles under Regulation (EU) No 168/2013 | Pedal-assist L1e vehicles (e-bikes) stay in; no other Art 2(5) delegated act exists for any sector | [EUR-Lex 2025/1535](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32025R1535) |
| Certified aviation products | Art 2(3); Recital 27 | Products certified under Regulation (EU) 2018/1139 | Open-category drones and uncertified components intended for certified aircraft "may be covered" | [Commission FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| Marine equipment | Art 2(4) | Equipment within Directive 2014/90/EU, as listed in the annex to Implementing Regulation (EU) 2025/1533 | Components intended for marine equipment but outside the Directive may be covered | [Commission FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| Identical-specification spare parts | Art 2(6); Recital 29 | Parts supplied to replace identical components, built to the same specifications, including a whole sub-product such as a PLC (guidance Example 39) | Repair purpose must be evident from the supply context; a part with different cryptography or secure boot is not identical and is a product in its own right (Example 37) | [Guidance C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| National security, defence and classified information | Art 2(7); Recital 26 | Products developed or modified exclusively for national security or defence, or designed to process classified information | Dual-use products on the open market are in; Member States may add procurement requirements under Art 5 | [Commission FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| Free and open-source software outside a commercial activity | Art 3(22); Recitals 15-20 | FOSS not monetised by its manufacturer is not made available on the market | Charging for binaries, updates or access makes the publisher a manufacturer; see Open-source software | [Guidance C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| Open-source software stewards | Art 3(14); Art 24; Recital 19 | Legal persons sustaining FOSS intended for commercial activities without placing it on the market | Light regime, not an exclusion: documented security policy, cooperation with authorities and limited Art 14 reporting from 11 Dec 2027; see Open-source software | [Guidance C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| Not placed on the market | Art 3(21)-(22); Blue Guide s.2.3 | Internal-use software and tools; software developed by a public body exclusively for its own use (Recital 16); unfinished code shared for review or testing; sample and demo code (guidance paras 22-24) | A later commercial supply of the same software is a placing on the market | [Commission FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| Trade fairs and time-limited testing | Art 4(2)-(4); Recital 37 | Prototypes shown at fairs with a visible non-compliance sign; unfinished software made available "for a limited period required for testing" with a visible sign | Only for the time needed to test and gather feedback; a risk assessment is still expected; not for safety components under other harmonisation law | [Commission FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| Tailor-made derogations | Annex I Part I 2(b); Annex I Part II(8); Recital 64 | Secure-by-default configuration and free security updates may be varied by explicit contract for a product fitted to one business user, including closed or air-gapped networks | Only those two requirements; a multi-tenant product with minor customisation or plugins is not tailor-made; keep the evidence in the technical documentation | [Commission FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| Products placed before 11 Dec 2027 | Art 69(2) | Units placed on the market before full application are subject to the CRA only if substantially modified from that date | Art 14 reporting applies to all of them regardless (Art 69(3)); further units of a non-compliant type cannot be placed on or after 11 Dec 2027 | [Commission FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |

Two points on the legacy rule deserve emphasis. The CRA applies to individual units, not product types (FAQ s.7.2). A design that shipped in 2026 must still be assessed, declared and CE-marked for units shipped from 11 Dec 2027.

The guidance allows such legacy designs to be placed "without redesign" where the risk assessment shows adequate security (paras 33-39). It does not require recreating historical design documentation.

### Partial reliefs

These do not remove a product from scope. They soften one obligation each.

| Relief | Legal basis | Effect | Status on 30 Oct 2026 |
|---|---|---|---|
| No fine for a missed 24-hour early warning | Art 64(10)(a); Recital 120 | Micro and small enterprise manufacturers cannot be fined for missing the deadlines in Art 14(2)(a) and 14(4)(a); the duty to report still stands | Adopted; national acts should impose no other pecuniary penalty for this (Recital 120) |
| No fines for stewards | Art 64(10)(b) | Open-source software stewards are exempt from administrative fines; corrective action under Art 52(3) remains | Adopted |
| Simplified technical documentation for micro and small enterprises | Art 33(5); Recital 93 | A simplified Annex VII format, once the Commission specifies it by implementing act; notified bodies must accept it | No implementing act adopted, drafted or scheduled; build the full Annex VII set |
| SME support measures | Art 33(1)-(4); Art 32(6); Art 39(12) | Awareness, advice channels, testing support, optional regulatory sandboxes; proportionately reduced conformity assessment fees | Sandboxes are optional and none was identified; fee reductions depend on notified bodies that do not yet exist |
| Internal control for important FOSS products | Art 32(5) | A manufacturer of FOSS in an Annex III category may use any Art 32(1) procedure, including Module A, if the technical documentation is public at placing on the market | Adopted; this is the only case where technical documentation must be published (FAQ s.6.6) |
| Automatic-update carve-outs | Annex I Part I 2(c); Recital 56 | Default-on automatic security updates do not apply to products primarily intended as components, or where users would not expect them, such as professional ICT networks and critical or industrial environments | Record the justification in the risk assessment (Art 13(4)); updates must still be made available without delay |
| Shorter support period | Art 13(8) | Less than 5 years only where the product is expected to be in use for less, such as a subscription product unusable after expiry | FAQ examples; five years is a floor, not a default (guidance section 5) |
| Existing type-examination certificates | Art 69(1) | EU type-examination certificates and approval decisions on cybersecurity requirements under other harmonisation law remain valid until 11 Jun 2028 | They count as evidence only for the risks they cover and never replace the CRA risk assessment (guidance paras 247-257) |

### Things that are not exclusions

- B2B-only sale. The CRA has no consumer-only limitation; B2B status matters only for the tailor-made derogations and for classification (Art 2(1); Recital 64).
- Free products from a company. Supply "free of charge" in a commercial activity is making available (Art 3(22)); ads, monetised platforms and personal-data conditions are commercial indicators (Recital 15).
- A non-EU manufacturer. The CRA applies to any product made available in the EU. The manufacturer's location changes who the importer is, not whether the product is in scope.
- Offline products with an indirect connection. Software on a networked host is in scope through the operating system (Recital 9; FAQ).
- Hardware that never receives updates. The absence of an update mechanism is a compliance gap against Annex I Part II, not a reason for being out of scope.
- Products sold through online marketplaces. A marketplace that only intermediates is not an economic operator, but the manufacturer and any importer keep their duties (Recital 78).
- White-label resale. Selling someone else's product under your own brand makes you the manufacturer (Art 21; Recital 78); see Economic operators and roles.
- Products designed before the CRA. Legacy designs placed on the market from 11 Dec 2027 need a conformity assessment, declaration and CE marking (guidance paras 33-39).
