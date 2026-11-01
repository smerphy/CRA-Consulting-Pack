# Operator roles and supply chain for Aldermoor Platforms

**Executive answer.** Aldermoor holds four CRA roles at once, and the role changes by channel, by legal entity and sometimes by commercial model. It is the manufacturer of every Aldermoor-branded product, including the ODM-built Pulse trackers, earbuds and Hearth thermostats: the brand owner that "has products ... designed, developed or manufactured" is the manufacturer under Art 3(13), so the Art 21 rebadging rule is not needed. Its Irish store entity is an importer for about 210 third-party SKUs it brings in from non-EU brands and a distributor for about 430 more, and it would be an importer of Aldermoor's own US-branded hardware unless the group fixes its manufacturer-of-record model. The Halo Store is an online marketplace, not a CRA economic operator, only while Aldermoor acts as the developers' agent; the Cloud Marketplace, where Aldermoor Ireland resells about 1,900 installable listings, is not. Importer and distributor checks for retail and the marketplace cost an estimated 2.8 FTE in the first year and under 1 FTE a year after. The radio estate has a hard date: the RED cybersecurity act that has applied since 1 Aug 2025 is repealed from 11 Dec 2027, so every radio model on sale across that date needs two declarations and a cut-over plan, and EN 18031 evidence covers 11 of 31 CRA requirement rows only in part and 12 not at all. Acquired products bring their own manufacturer, support promises and Art 14 history, and the tailor-made derogation relaxes only two requirements. Six decisions are needed, most by mid-2027 (below).

All volumes, efforts and dates for Aldermoor are illustrative estimates for a fictional client and are recorded in `channels.yaml`. Legal text is quoted from the Official Journal text of Regulation (EU) 2024/2847 held in `pack/enterprise/oj-verification/source/`. Commission guidance C(2026) 5252 and the FAQ v1.4 are guidance, not law, and are labelled as such.

## Aldermoor holds a different CRA role in each channel, and the role decides which article applies

The CRA attaches duties to roles, not to companies. The manufacturer "develops or manufactures products with digital elements or has [them] designed, developed or manufactured, and markets them under its name or trademark" (Art 3(13)). The importer is "established in the Union" and places on the market a product that "bears the name or trademark of a natural or legal person established outside the Union" (Art 3(16)). The distributor makes a product available "without affecting its properties" (Art 3(17)). Exhibit 1 applies these definitions channel by channel.

**Exhibit 1: Aldermoor's CRA role by channel (volumes illustrative)**

| Channel | Volume | Aldermoor role | Articles | Main exposure |
|---|---|---|---|---|
| Own-brand hardware sold in the EU | All Arc, Hearth, Pulse, Keystone, Lumen OS devices | Manufacturer (named entity to decide); Aldermoor Ireland is importer if Aldermoor Platforms Inc. is the named manufacturer | Arts 13-14; Art 19 | Entity model not yet fixed (Decision 1) |
| ODM-built own-brand products | 18 ODMs | Manufacturer | Art 3(13); Arts 13-14 | ODM firmware depth and support length |
| Third-party devices imported from non-EU brands | 210 SKUs | Importer (Aldermoor Ireland) | Art 19; Art 23 | Must verify the file exists and hold the DoC for 10 years |
| Third-party devices bought from EU distributors | 430 SKUs | Distributor | Art 20; Art 23 | Pre-listing checks and vulnerability relay |
| Third-party product rebadged as Aldermoor | 0 today | Manufacturer | Art 21 | Any rebadge makes Aldermoor liable under Arts 13 and 14 in full |
| Halo Store, third-party apps | 2.4m apps | Online marketplace provider while acting as agent; manufacturer for its own apps | Recital 78; Arts 13-14 for own apps | Commercial model drift into reseller |
| Cloud Marketplace, installable listings | 1,900 listings | Distributor (EU vendor) or importer (non-EU vendor) while Aldermoor Ireland is merchant of record | Arts 19-20 | Largest unplanned check workload |
| Cloud Marketplace, browser-only SaaS | 4,100 listings | None under the CRA | Recital 12 | None |
| Carrier and retail partners selling Aldermoor devices | About 9,000 doors | Manufacturer supplying distributors | Art 20(2)(b) | Partners must receive "all necessary documents" |

Three points in Exhibit 1 need explanation.

First, ODM and white-label products. The KB treats white-label resale under Art 21 (05-roles.md). For Aldermoor's ODM model the better route is Art 3(13) itself: Aldermoor commissions the design and markets the product under its own trademark, so it is the manufacturer from the first unit. Art 21 applies where an importer or distributor "places a product with digital elements on the market under its name or trademark or carries out a substantial modification" of a product already placed. That is the rebadging of a product another company already sells. The result is the same, Arts 13 and 14 in full, but the evidence differs: under Art 3(13) Aldermoor must hold the whole Annex VII file for the ODM design, not lean on someone else's.

Second, the manufacturer-of-record entity. If the label and declaration name Aldermoor Platforms Inc. (US), then Aldermoor Ireland Ltd, as the EU entity that first makes the units available, meets the importer definition for Aldermoor's own hardware. It must then run the Art 19(2) checks, add its own name and contact details (Art 19(4)) and keep the declaration (Art 19(6)). The alternative is to name Aldermoor Ireland as the EU manufacturer. We recommend the first model: one global label naming Inc. as manufacturer, Aldermoor Ireland as importer, and the same Irish entity appointed authorised representative by written mandate under Art 18(1) to hold the file. The importer checks are internal and cheap, and the model matches the Art 14(7) routing to Ireland's CSIRT used in module E2 (Exhibit 2). We found no OJ provision barring one entity from being both importer and authorised representative; counsel should confirm.

Third, the app store and the cloud marketplace. Recital 78 says an entity that "provides only online intermediation services" and "is merely a provider of an online marketplace" as defined in GPSR Art 3(14) "does not qualify as one of the types of economic operator". The same recital says that if the marketplace provider "also distributes a product", it is a distributor for that sale, and if it sells its own branded products it is a manufacturer. The test is what Aldermoor does for each sale, not what it calls itself. Where Aldermoor Ireland buys and resells a licence as merchant of record, it is in the supply chain and is likely a distributor, or an importer when the vendor is outside the EU. This is our reading of recital 78 and the definitions; the guidance does not address app stores as operators.

**Exhibit 2: Entity options for own-brand hardware (recommendation in bold)**

| Option | Named manufacturer | Aldermoor Ireland role | Label | Art 14(7) coordinator | Trade-off |
|---|---|---|---|---|---|
| **A** | **Aldermoor Platforms Inc.** | **Importer (Art 19) and authorised representative (Art 18)** | **One global label plus importer details** | **Ireland, as EU main establishment (E2)** | **Internal importer checks; Art 18(2) keeps design duties with Inc.** |
| B | Aldermoor Ireland Ltd | Manufacturer | EU-specific label | Ireland | Irish entity holds Arts 13-14 for products designed in the US; separate EU SKUs |

## Retail and marketplace sales carry verification duties that start on 11 Dec 2027

Importer and distributor duties apply from 11 Dec 2027 (Art 71(2)), and only to units placed on or after that date (Art 69(2)). The FAQ confirms that distributors need not bring earlier stock into compliance unless they substantially modify it (FAQ 7.5, guidance). The checks differ in depth.

**Exhibit 3: What Aldermoor must check before listing a third-party product (OJ text)**

| Check | Importer (Art 19) | Distributor (Art 20) |
|---|---|---|
| Conformity assessment carried out | Ensure it, Art 19(2)(a) | Not required |
| Technical documentation drawn up | Ensure it, Art 19(2)(b); be able to make it available for 10 years or the support period, Art 19(6) | Not required |
| CE marking | Art 19(2)(c) | Art 20(2)(a) |
| EU declaration of conformity (full or simplified) | Accompanies the product, Art 19(2)(c); keep a copy 10 years or the support period, Art 19(6) | Manufacturer complied with Art 13(20), Art 20(2)(b) |
| Annex II user information in an understood language | Art 19(2)(c) | Art 13(18) via Art 20(2)(b) |
| Type, batch or serial number | Art 13(15) via Art 19(2)(d) | Art 13(15) via Art 20(2)(b) |
| Manufacturer name, address, digital contact | Art 13(16) via Art 19(2)(d) | Art 13(16) via Art 20(2)(b) |
| Support-period end date, at least month and year, at purchase | Art 13(19) via Art 19(2)(d) | Art 13(19) via Art 20(2)(b) |
| Importer name and contact on product, packaging or document | Add its own, Art 19(4) | Check the importer did, Art 20(2)(b) |
| Proof of the checks | "Be able to provide the necessary documents", Art 19(2) last subparagraph | "Have provided all necessary documents to the distributor", Art 20(2)(b) |

The support-period end date matters most for Aldermoor's own storefronts. Art 13(19) requires the end date "at the time of purchase in an easily accessible manner". On an Aldermoor product page that is Aldermoor's display, so the listing system needs a mandatory support-end field for every product with digital elements, sourced from the manufacturer's documents.

Non-conformity has three triggers and three different actions. Before listing, an importer that "considers or has reason to believe" a product does not conform must not place it (Art 19(3)); a distributor must not make it available (Art 20(3)). After sale, both must make sure corrective measures, withdrawal or recall happen (Arts 19(5) and 20(4)). Where the product presents a "significant cybersecurity risk", both inform the manufacturer and the market surveillance authorities. An importer must also tell the authorities where it suspects a significant risk from "non-technical risk factors" (Art 19(3), second subparagraph). Every escalation goes to market surveillance authorities, not to a CSIRT.

The Art 14-style information duty is short. An importer or distributor "upon becoming aware of a vulnerability" must "inform the manufacturer without undue delay" (Art 19(5) and Art 20(4), second subparagraphs). If the product "presents a significant cybersecurity risk", it must "immediately inform the market surveillance authorities" of the Member States where it was sold, with details of non-compliance and corrective measures. There is no 24-hour clock, no ENISA platform filing and no final report for importers or distributors. Aldermoor's PSIRT will nonetheless find vulnerabilities in third-party devices it sells, because it tests what it sells, and needs a relay path for them. We recommend a 5-business-day internal target for the manufacturer notice and same-day escalation where exploitation is seen.

Two further duties are easy to miss. Art 23 requires Aldermoor to name, on request, every operator that supplied it and, where available, every operator it supplied, for 10 years in each direction. Arts 19(8) and 20(6) require Aldermoor to tell authorities and, as far as possible, users if a third-party manufacturer ceases operations. For 640 SKUs this is a monitoring task, not a one-off check.

**Exhibit 4: Check workload (estimates)**

| Population | Role | Hours per item | Year 1 hours | Hours a year after |
|---|---|---|---|---|
| 210 imported SKUs | Importer | 8 | 1,680 | 590 (35% churn) |
| 430 distributed SKUs | Distributor | 2 | 860 | 300 (35% churn) |
| 1,900 installable Cloud Marketplace listings, automated intake | Distributor or importer | 1 | 1,900 | 475 (25% new) |
| **Total** | | | **4,440 (about 2.8 FTE)** | **1,365 (under 1 FTE)** |

Without automated intake, the Cloud Marketplace alone would take about 5,700 hours (3.6 FTE) in year 1. The practical design is a vendor portal that collects the DoC, CE evidence, support-end date and contacts as structured fields, checks them by machine, and routes exceptions to a reviewer.

## The app store's position rests on its commercial model, and the DSA, GPSR and PLD duties are not CRA duties

For apps sold through the Halo Store, the developer is the manufacturer under Art 3(13). Aldermoor is not the distributor while it only intermediates. Three facts could change that, and each is a classification trigger for the store: Aldermoor becoming seller of record or reseller of an app in the EU; Aldermoor altering an app's code in a way that affects its properties, which takes the distributor route away and may trigger Art 22 if it is a substantial modification; and Aldermoor selling an app under its own brand. A non-EU developer selling directly through an intermediary store has no CRA importer, the same position the KB describes for direct-to-consumer sales (05-roles.md). We record this as open question 1.

Aldermoor's other online-platform duties come from other laws. Exhibit 5 separates them.

**Exhibit 5: Marketplace duties by source**

| Duty | Source | CRA duty? |
|---|---|---|
| None as a "mere" marketplace; "should strive to cooperate" with market surveillance authorities | CRA recital 78 | No binding duty (recital) |
| Distributor duties for any product it distributes; manufacturer duties for own-branded products | CRA recital 78, Arts 13-14, 20 | Yes, per sale |
| Interface that lets traders supply product identification, trader marks and "labelling and marking" information; best efforts to check it before listing; random checks of official databases for illegal products | DSA (Regulation (EU) 2022/2065) Art 31, read on a secondary site | No; a CE-marking or support-period field serves both |
| Trader traceability (Art 30) and informing buyers of illegal products (Art 32) | DSA Arts 30 and 32 (headings verified only) | No |
| Online-marketplace product-safety duties | GPSR (Regulation (EU) 2023/988) | No. CRA Art 11 imports only GPSR Chapter III Section 1, Chapters V and VII and Chapters IX to XI, and only for risks the CRA does not cover; whether the GPSR marketplace provisions reach a given product is a GPSR question (open question 2) |
| Liability where no EU operator can be identified | PLD (Directive (EU) 2024/2853) Art 8(3)-(4) | No. A platform is liable as a distributor only if it fails to name an EU operator within one month of a request and the DSA Art 6(3) conditions are met |

The PLD row corrects the KB, which says the online platform is liable wherever no importer or authorised representative exists (05-roles.md; 13-interplay.md). The OJ text of Art 8(1)(c)(iii) puts that liability on the fulfilment service provider; online platforms are caught only through Art 8(4) on the narrower test above.

## ODM and supplier contracts must deliver firmware SBOMs, fast notice and audit access

Aldermoor's due-diligence duty is general: it "shall exercise due diligence when integrating components sourced from third parties so that those components do not compromise the cybersecurity" of the product (Art 13(5)). How much is enough depends on the component's risk (recital 34; FAQ 4.4.2, guidance). At 2,590 suppliers the only workable answer is tiering, with the base pack's supplier clause pack (Template 9, `pack/out/hosted/D14-compliance-templates-kit/md/09-supplier-cra-clause-pack.md`) as the contract schedule.

**Exhibit 6: Supplier tiers and due-diligence depth (counts illustrative)**

| Tier | Suppliers | Who | Template 9 clauses | Due-diligence actions (FAQ 4.4.2 menu, guidance) | Review cycle |
|---|---|---|---|---|---|
| 1 | 140 | 18 ODMs; 42 SoC, modem, Wi-Fi/BT, secure-element and sensor firmware vendors; 35 commercial OS, RTOS, crypto and codec vendors; 45 contract developers of remote data processing | All 12; clause 5 audit right mandatory | SBOM review, binary SCA on every drop, security testing (fuzzing, firmware analysis), update-history and support-period check, posture assessment, annual audit | Each release and yearly |
| 2 | 650 | Commercial libraries, SDKs, build tooling, hosted dependencies | 1-4, 6, 7, 10, 11 | SBOM review, SCA, EUVD and vulnerability-database check, support-period check | Each major version |
| 3 | 1,800 | Hardware without firmware, packaging, low-risk tools | None; intake record | Intended-purpose fit; CE check from Dec 2027 where applicable | At onboarding |

Open-source components taken straight from upstream have no supplier contract. They go through the component intake gate in module E1 and the upstream reporting path in module E4.

ODM firmware needs a stricter SBOM than the legal minimum. Annex I Part II(1) requires an SBOM "covering at the very least the top-level dependencies". That is not enough to remediate a vulnerability in a modem blob or a vendor kernel, which Annex I Part II(2) requires "without delay". Our ODM annex to Template 9 clause 4 sets these rules:

1. **Format.** CycloneDX 1.6 or later, or SPDX 3.0.1 or later, one SBOM per firmware build, bound to the image by its SHA-512 hash (Template 9 clause 4.1, 4.3).
2. **Depth.** Full transitive depth for code the ODM builds from source. For each prebuilt binary, the component's name, supplier, version and hash, plus the binary vendor's own SBOM where one exists. Known unknowns are marked, never omitted.
3. **Mandatory coverage.** Boot chain, TEE and trusted applications, baseband and modem, Wi-Fi and Bluetooth firmware, DSP and GPU firmware, sensor hub, kernel version and configuration, vendor HALs, and the compiler toolchain.
4. **Binary SCA by Aldermoor.** Aldermoor runs binary composition analysis on every delivered image and reconciles it with the ODM SBOM. A gap of more than an agreed threshold blocks the build at the E1 release gate.
5. **Vulnerability status separately.** CSAF 2.0 with VEX, never inside the SBOM (Template 9 clause 4.4).

Notification service levels must fit inside Aldermoor's Art 14 clocks. Aldermoor's early warning is due within 24 hours of its own awareness of an actively exploited vulnerability (Art 14(2)(a)), and module E2 targets 12 hours. A supplier's silence does not stop the clock if Aldermoor learns of the exploit another way.

**Exhibit 7: Tier 1 supplier service levels mapped to Art 14 (commercial targets, not law)**

| Event at supplier | Supplier must | By | Aldermoor clock it feeds |
|---|---|---|---|
| Actively exploited vulnerability or severe incident in a supplied component | Notify the PSIRT 24/7 contact | 12 h from supplier awareness (Template 9 cl. 2.1) | Early warning, 24 h (Art 14(2)(a), (4)(a)) |
| Same | Affected versions, severity, mitigations | 36 h from supplier awareness | Notification, 72 h (Art 14(2)(b), (4)(b)) |
| Same | Fix or mitigation for supported versions | Agreed per severity; 7 days target for critical | "Without delay" (Annex I Part II(2)) |
| Same | Root cause and fix details | 7 days after fix | Final report, 14 days after a measure is available (Art 14(2)(c)) |
| High or critical, not exploited | Notify | 5 business days (Template 9 cl. 2.2) | Vulnerability handling (Annex I Part II) |
| Supplier advisory planned | Notify Aldermoor | No later than publication (cl. 2.4) | Avoids an unseen awareness trigger |
| End of support for a component version | Notice and last-time buy | 24 months (cl. 7.1) | Support period (Art 13(8)) |

Support length is the hardest commercial term. Arc phones carry a 7-year support period. A SoC vendor whose board-support package is supported for less leaves Aldermoor to patch the vendor's code itself. Art 13(8) lets a manufacturer take "the support periods of integrated components that provide core functions" into account when setting its own support period, but Aldermoor has already announced 7 years. The contract must therefore require component support until the end of the support period of the last unit placed with that component, or source-code escrow with the build tooling to patch it.

Audit and evidence rights complete the set. Template 9 clause 5 gives a yearly audit and a 5-business-day turnaround on a reasoned request from an authority. For the Devices organisation, which module E3 puts under Module H, ODM production and firmware build sites sit inside the quality system the notified body will assess. Our reading, not confirmed against Annex VIII, is that the notified body may need access to those sites, so clause 5.3 should name the notified body expressly.

## The RED baseline already applies, and its repeal on 11 Dec 2027 needs a per-model cut-over

Every Aldermoor product with a radio has been subject to RED cybersecurity requirements since 1 Aug 2025. Delegated Regulation (EU) 2022/30 activated RED Art 3(3)(d), (e) and (f) on network harm, personal data and fraud; Delegated Regulation (EU) 2023/2444 set its application date of 1 Aug 2025; and Implementing Decision (EU) 2025/138 cited EN 18031-1, -2 and -3:2024 with restrictions (verification.md claim 32). One restriction denies presumption of conformity where "the user is allowed not to set and use any password". Aldermoor's radio estate covers Arc phones, tablets, Lumen OS laptops, earbuds, every Hearth device, Pulse wearables and the NFC and Bluetooth Keystone keys.

Delegated Regulation (EU) 2026/339 repeals 2022/30 "with effect from 11 December 2027" (Art 1; adopted 16 Feb 2026, OJ 29 Apr 2026, in force 19 May 2026; verification.md claim 13 and E6 claim F18). Recital 30 of the CRA explains why: the CRA's essential requirements "include all the elements" of RED Art 3(3)(d)-(f). The rest of RED, including radio, safety and EMC requirements, continues.

**Exhibit 8: What changes for a radio product on 11 Dec 2027**

| Topic | Units placed up to 10 Dec 2027 | Units placed from 11 Dec 2027 |
|---|---|---|
| Cybersecurity law | RED Art 3(3)(d)-(f) via 2022/30 | CRA Annex I Parts I and II |
| Presumption route | EN 18031-1/-2/-3, with restrictions | Only CRA harmonised standards, none cited at 30 Oct 2026 (11-standards.md) |
| Conformity route for Class I products (cameras, locks, routers, assistants, wearables) | RED Module A if EN 18031 is applied in full without a restriction; otherwise a RED notified body | CRA Module B+C or H with a CRA notified body; RED bodies must be newly notified (recital 100) |
| Declaration | RED declaration | One declaration naming RED and the CRA (Art 28(3)) |
| Process duties | None under RED | Support period, SBOM, vulnerability handling, Art 13(19) end date |
| Reporting | CRA Art 14 since 11 Sep 2026 for all in-scope products (Art 69(3)) | Same |
| Existing RED type-examination certificates | Valid | Valid until 11 Jun 2028 as evidence for the RED risks they cover only (Art 69(1); guidance paras 247-254) |

Two points narrow the Art 69(1) benefit. It covers "EU type-examination certificates and approval decisions", so it helps only models a RED notified body examined. Where Aldermoor self-declared under EN 18031, there is no certificate to carry over. And the guidance says a certificate never exempts the CRA risk assessment: risks such as "vulnerability handling processes, data minimisation, and reduction of the attack surface" still need CRA treatment (guidance para 253).

EN 18031 evidence still carries over a long way. The base pack crosswalk (`pack/data/crosswalk.json`, column `en18031`) rates EN 18031 against 31 CRA requirement rows: partial on 11, weak on 8 and none on 12.

**Exhibit 9: How EN 18031 evidence carries into the CRA technical file (from crosswalk.json)**

| Coverage | CRA rows | Use in the Annex VII file | New work |
|---|---|---|---|
| Partial (11) | Annex I Part I 2(a), (b), (c), (d), (e), (f), (h), (i), (j), (l); Part II(7) | Mechanism test reports and decision records go into the risk assessment and test evidence | Reset to original state; update notification and postponement; unauthorised-access and corruption reporting; logging opt-out; update infrastructure and signing keys |
| Weak (8) | Part I (1), 2(g), 2(k), 2(m); Part II(1), (2); Art 13(2)-(4); Art 13(12) | Context only; decision trees become per-requirement risk justifications | Product risk assessment; exploit mitigation; data minimisation; secure deletion and transfer; SBOM; ongoing remediation |
| None (12) | Part II(3)-(6), (8); Art 13(5), 13(6), 13(8); Art 14 (three rows); Art 32 | Nothing | All process duties, support period, reporting, CRA conformity route |

The engineering work is concentrated in a few Part I gaps; the larger work is the Part II process layer, which the global control set (module E5) and the Art 14 engine (module E2) already fund. KB research notes add that EN 18031 test evidence "does not replace an assessment against EN 40000-1-4", the draft CRA standard that reuses its mechanism vocabulary without the decision trees (11-standards.md; vendor commentary).

Products on sale across the date need a planned cut-over, because the CRA applies per unit placed, not per product type (04-exclusions.md; FAQ 7.2, guidance). Our plan:

1. **Inventory by model.** List every radio model with its expected last RED-only placing date and first CRA placing date. Models launched from Q3 2027 should be CRA-conformant at launch.
2. **Dual-compliant builds from Q3 2027.** Units produced from about Sep 2027 meet both EN 18031 and CRA Annex I, so stock placed on either side of 11 Dec 2027 is lawful. The declaration switches on the date; the hardware and firmware do not.
3. **Class I radio products first.** Hearth cameras, locks, routers and assistants and Pulse wearables need a CRA notified body for units placed from 11 Dec 2027. With none designated at 8 Sep 2026, these models carry the schedule risk.
4. **Stock already in the channel.** Units placed by 10 Dec 2027 can continue to be sold (FAQ 7.5, guidance). When intra-group movement counts as placing is open question 4, so the safe assumption is that any unit first supplied by Aldermoor Ireland to a customer or partner from 11 Dec 2027 needs the CRA declaration.
5. **Post-date changes.** A substantial modification of a RED-era model from 11 Dec 2027 brings it under the CRA (Art 69(2)). Security updates are "generally not" substantial modifications (guidance pt 108), so the release gate in module E1 decides per release.

## Acquired products and enterprise SKUs need their own rules, because the CRA has none

The Regulation has no M&A provision, and we found none in the guidance or FAQ. The rules below are derived from the definitions and are our reading for counsel to confirm.

**Exhibit 10: Who is the manufacturer after a transaction (our reading)**

| Transaction | Units already placed | New units | What Aldermoor must do |
|---|---|---|---|
| Share deal, target brand kept | Target entity stays manufacturer | Target entity, under its brand | Connect target PSIRT to the Art 14 engine on day 1; target's own Art 14(7) CSIRT may not be Ireland |
| Share deal, rebranded to Aldermoor | Target entity, for earlier units | Aldermoor named manufacturer from the first Aldermoor-branded unit | Full conformity assessment and new declaration before the first unit; class may change if bundled (E3) |
| Asset deal | Seller stays manufacturer of earlier units unless it ceases, triggering Art 13(23) | Aldermoor | Contract for seller's support and Art 14 cooperation; plan for Arts 19(8) and 20(6) notices if the seller ceases |
| Aldermoor resells target stock already on the market | Target or seller | Not applicable | Aldermoor is a distributor (Art 20) |
| Aldermoor relabels target stock already on the market | Aldermoor becomes manufacturer (Art 21) | Aldermoor | Treat as a new product placing |
| Target code integrated into an Aldermoor product | Not applicable | Aldermoor, for the whole product | Art 13(5) due diligence on the acquired component (guidance para 120, Example 51) |

Diligence should start before signing. The full checklist is in `checklists.md`. The items that most often change value are the classification of each product (a Class I or II product without a notified-body plan is a schedule risk), the existence of an Annex VII file, published support-end dates (Art 13(19) promises are binding for units already sold), Art 14 notifications made or missed since 11 Sep 2026, open-source licence and steward roles (module E4), and supplier contracts without notification or SBOM terms.

Integration follows four time rules: Art 14 connection on the day of closing; register entries and evidence-store onboarding within 30 days; the substantial-modification gate on all target releases within 90 days; and no Aldermoor-branded unit placed before Aldermoor's own conformity assessment is complete.

Enterprise and custom SKUs mostly are not "tailor-made". Annex I Part I(2)(b) requires a "secure by default configuration, unless otherwise agreed between manufacturer and business user in relation to a tailor-made product with digital elements". Annex I Part II(8) requires security updates "without delay and, unless otherwise agreed between a manufacturer and a business user in relation to a tailor-made product with digital elements, free of charge". Recital 64 limits this to products "fitted to a particular purpose for a particular business user" where both parties "explicitly agreed to a different set of contractual terms". The FAQ (4.2.5, guidance) adds two tests: custom-developed products or products for "highly controlled environments (e.g. closed networks or air-gapped environments)" can qualify; a product with "minor customisations" or plugins that is "fundamentally the same product for every customer" cannot.

**Exhibit 11: Aldermoor enterprise offerings against the tailor-made test**

| Offering | Tailor-made? | What may be varied by contract | What never changes |
|---|---|---|---|
| Lumen Browser enterprise policies, Halo enterprise management, Cloud CLI and SDKs | No: same product for every customer | Nothing | All of Annex I, Arts 13-14 |
| Aldermoor Edge standard appliance | No | Nothing | All of Annex I; Class II route (E3) |
| Cloud Isolated appliance built for one government customer's air-gapped estate | Likely yes, if custom-built under its own contract | Secure-default configuration (2(b)); free-of-charge updates (Part II(8)) | Update dissemination "without delay"; advisory messages; SBOM; vulnerability handling; support period; Art 14 reporting; CE marking |
| Product built exclusively for national security or defence, or to process classified information | Out of scope (Art 2(7)) | Not applicable | Not applicable; record the scope decision |

The derogation varies only the price of updates, not their delivery. For air-gapped estates, automatic updates are required only "where applicable" (Annex I Part I(2)(c)). Aldermoor should ship signed offline update bundles with advisories through the customer's contracted channel, and keep the evidence that the tailor-made terms were "explicitly agreed" in the Annex VII file, as the FAQ expects.

## Decisions for the executive team

1. **Fix the manufacturer-of-record model: Aldermoor Platforms Inc. as manufacturer, Aldermoor Ireland Ltd as importer and Art 18 authorised representative for EU hardware.** Owner: General Counsel with the Head of Product Compliance. Timing: decide by Mar 2027; labels and declarations updated for units placed from 11 Dec 2027.
2. **Hold the Halo Store and Cloud Marketplace positions under classification control.** Keep the Halo Store as agent for third-party apps; accept distributor and importer duties for Cloud Marketplace resales and build automated vendor intake. Any change of commercial model, code processing or own-branding is a classification trigger. Owner: General Counsel with the heads of Halo Store and Cloud Marketplace. Timing: position by Jun 2027; intake live by Oct 2027.
3. **Stand up a third-party product compliance desk for EU retail and the marketplace.** It runs the Exhibit 3 checks, the support-end field, the vulnerability relay and Art 23 records. Owner: VP Retail with the Head of Product Compliance. Timing: staffed (about 3 FTE) by Sep 2027.
4. **Adopt supplier tiering with Template 9 and the ODM firmware SBOM annex.** Owner: Chief Procurement Officer with the CISO. Timing: all Tier 1 contracts amended by Jun 2027; Tier 2 at renewal, all by Dec 2027.
5. **Approve the RED-to-CRA cut-over plan per radio model, with dual-compliant builds from Q3 2027.** Owner: VP Hardware Engineering with the Head of Product Compliance. Timing: model inventory by Mar 2027; dual-compliant production from Sep 2027.
6. **Adopt the M&A CRA diligence checklist and the four integration time rules, and a register of tailor-made contracts.** Owner: Head of Corporate Development with General Counsel. Timing: immediate for deals in progress.

## Risks and open questions

1. **App store role.** Whether an app store acting as agent is "merely" an online marketplace for every EU sale, and who, if anyone, is importer for a non-EU developer's app, is not addressed in the Regulation or the guidance. Counsel and, if needed, ADCO should confirm.
2. **GPSR marketplace duties.** We did not open the GPSR text, so we cannot confirm which chapter holds the online-marketplace provisions or whether CRA Art 11 reaches them. Counsel to confirm per product type.
3. **Importer and authorised representative in one entity.** No bar found in the OJ text; confirm with counsel.
4. **Placing date for intra-group stock.** FAQ 4.2.3 (guidance) describes products "sent to the distribution branch of a manufacturer" after placing; the Blue Guide, which the KB does not hold, governs the general rule. Confirm before relying on any pre-date stock build.
5. **Notified-body access to ODM sites under Module H.** Our reading; confirm against Annex VIII Part IV and the chosen body's contract.
6. **RED transition detail.** Delegated Regulation (EU) 2026/339 Art 1 is verified (E6). Its recitals on market surveillance of RED-era products, and the Commission's intention to delete EN 18031 references after the repeal, come from KB research notes on the draft C(2026) 778; this module could not open EUR-Lex.
7. **M&A rules.** Derived from the definitions; no guidance exists. Certificate transfer on a change of manufacturer name depends on the notified body.
8. **KB corrections found.** KB 05-roles.md cites "Art 19(6)-(9)" and "Art 19(9)" for the cessation notice; the OJ text of Art 19 has eight paragraphs and the cessation notice is Art 19(8). The KB also states the PLD platform liability too broadly (Exhibit 5). It treats white-label under Art 21, where Art 3(13) is the direct route for ODM products. The Art 19 citations and the PLD wording were corrected in the KB on 1 Nov 2026 (claims O09 and O10).
9. **Estimates.** Channel volumes, supplier counts, check hours and service levels are illustrative assumptions (`channels.yaml`).

## Sources

- [Regulation (EU) 2024/2847](https://eur-lex.europa.eu/eli/reg/2024/2847/oj), OJ text held at `pack/enterprise/oj-verification/source/oj_L_2024_2847_EN.txt`: Arts 2(7), 3(13), (16), (17), (21), (22), (30), 11, 13(5), (8), (15)-(20), 14(2), 18-23, 28(3), 64(2)-(3), 69, 71; Annex I Part I(2)(b), (c), Part II(1), (2), (8); recitals 30, 34, 64, 78, 100.
- [Directive (EU) 2024/2853](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024L2853) (PLD), Art 8, OJ text held at `pack/enterprise/oj-verification/source/PLD_2024_2853_EN.txt`.
- [Delegated Regulation (EU) 2026/339](https://eur-lex.europa.eu/eli/reg_del/2026/339/oj/eng), Art 1, as verified in reports/verification.md claim 13 and E6 claims.csv F18.
- Commission guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) (guidance, approved draft): paras 47, 108, 120, 247-254; Examples 3, 9, 51.
- Commission [CRA FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307) (guidance): 4.2.3, 4.2.5, 4.4.1-4.4.4, 7.5.
- [Digital Services Act, Art 31](https://www.springlex.eu/en/packages/dsa/dsa-regulation/article-31/) (secondary reproduction of Regulation (EU) 2022/2065; Arts 30 and 32 headings only).
- Knowledge base: reports/sections/04-exclusions.md (tailor-made, per-unit rule), 05-roles.md (roles), 11-standards.md (EN 18031, EN 40000-1-4), 13-interplay.md (RED, GPSR, Reg 2019/1020); reports/verification.md claims 13 and 32; research_notes/EU CRA engineering compliance/timeline_enforcement_interplay_uk.md (RED transition).
- Base pack: Template 9 supplier CRA clause pack, `pack/out/hosted/D14-compliance-templates-kit/md/09-supplier-cra-clause-pack.md`; crosswalk `pack/data/crosswalk.json` (column `en18031`).
- Enterprise modules: E1 evidence-as-code, E2 art14-operations, E3 portfolio-classification, E4 open-source-strategy, E5 global-control-set.
- This module: `paper.md`, `checklists.md`, `channels.yaml`.
