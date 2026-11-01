# Legal positions pack: eight open CRA questions the Aldermoor programme depends on

**Executive answer.** Eight interpretive questions sit under the Enterprise Edition's cost and schedule figures. For each one this pack sets out the text, the readings available, a recommended position, a conservative fallback, the evidence to hold and who can confirm it. Two findings change the programme. First, the Commission guidance does not make every software version a placing on the market: a version that is not a substantial modification keeps the original placing date (guidance para 15, Example 2). Three Enterprise papers said otherwise; the evidence design survives, but the "about 104,000 placing records a year" framing does not. Second, the guidance now takes a side on the Art 32(2) certification-scheme limb: it applies to schemes "specified by the Commission via delegated acts in accordance with Article 27(9)" (footnote 25 to para 148), so Module A through EUCC is not available to Class I products today. Six questions remain genuinely open: one Art 14 record per product or per vulnerability, steward and manufacturer double filing, operating systems supplied to OEMs, the support-period floor for units placed after 11 Dec 2027, the class of a FIDO key with a secure element, and the remote data processing boundary for cloud clients. Only two of the eight (A and D) fall within the remit Ireland's NCSC has set for itself; the letter in this folder asks those two plus coordinator confirmation for steward filings. The other six go to external counsel now and to the Irish market surveillance authority once one is designated, which had not happened by 8 Oct 2026.

All text quoted below was matched by script against the local copies of the sources in `../source/` and `../source/guidance/` (see `../check_positions.py`). Guidance means Commission guidance C(2026) 5252 annex, approved 27 Jul 2026 and not yet formally adopted; the Communication says "It is only from that moment that it will apply". FAQ means the Commission services' FAQ v1.4 of 4 Sep 2026. Figures from other modules are estimates for the fictional client unless stated.

## The eight questions on one page

| ID | Question | Recommended position | Conservative fallback | Who confirms | Decide by |
|---|---|---|---|---|---|
| A | One Art 14 notification per product, or one per vulnerability across products? | The duty attaches per product, but one notification may list several products if each product's details and Member States are given. Operate per product (rule FO-1) until confirmed | Per product permanently | NCSC (coordinator CSIRT); ENISA via NCSC | Letter by 30 Nov 2026 |
| B | Is each software version a placing? What does continuous delivery change? | Follow the guidance: a placing per substantially modified version and per platform variant; other versions inherit the placing date. Record every version anyway | Treat each 4-weekly major as presumptively substantial unless the pt 110 record says otherwise | Commission (guidance author); Irish MSA once designated; notified body; counsel | Counsel note by 31 Jan 2027 |
| C | Do certification schemes "as referred to in Article 27" open Module A for Class I before an Art 27(9) act? | No. Follow guidance footnote 25: only schemes specified by an Art 27(9) delegated act. Plan Module H | Same | Commission (Art 27(9) act); counsel | Counsel note by 30 Nov 2026 |
| D | Steward and manufacturer for the same codebase: one Art 14 filing or two? | Two distinct duties. From 11 Dec 2027 file per product as manufacturer and once per project as steward, cross-referenced, unless NCSC accepts one combined record | Always two filings | NCSC; ENISA via NCSC; Commission (FAQ 5.5) | Letter by 30 Nov 2026; settled by Jun 2027 |
| E | OS inside Aldermoor's own device (Example 58) versus OS supplied to OEMs | Own devices: default class. OEM supply: keep it as free public HOSP source plus a separately licensed services package; never supply OS images or licensed source for payment | Treat any OS image or licensed build supplied to OEMs as an Annex III item 11 component under Module H | Irish MSA; Commission; counsel | Counsel note by 31 Jan 2027 |
| F | Support-period floor per unit or per product type for models on sale across 11 Dec 2027 | Per unit: each unit placed from 11 Dec 2027 gets at least five years (or its expected use time) from its own placing | Same | Irish MSA; ADCO (Art 52(16)); counsel | Policy by Mar 2027 |
| G | FIDO key with a secure element: Class I item 1 or Annex IV item 3? | Annex IV item 3 where the secure element is designed to AVA_VAN.4 or higher and is the key's substance | Same; I.1 only for authenticators with substantial functions outside the secure element | Commission (IR 2025/2392 author); Irish MSA; notified body | By Jan 2027 (E3 decision 3) |
| H | Remote data processing boundary for cloud consoles and installed clients | Consoles are out. For installed clients, RDPS is the Aldermoor-designed endpoints the client calls directly (gateways, sync, identity, update); back-ends behind them are external dependencies | Treat the whole control-plane API of a service as RDPS where an installed client is its main access path | Commission; Irish MSA; counsel | Counsel note by 31 Jan 2027 |

## Who can confirm what: Irish and EU routes

**Ireland's coordinator CSIRT.** Aldermoor Ireland Ltd in Dublin is the EU main establishment, so Art 14(7) routes manufacturer notifications to Ireland's CSIRT. The National Cyber Security Centre (NCSC), which runs CSIRT-IE and sits under the Department of Justice, Home Affairs and Migration, receives CRA notifications through the SRP, publishes the National CRA Guidelines (31 Aug 2026) and runs a helpdesk at cra_helpdesk@ncsc.gov.ie for "the technical process of submitting Article 14 notifications". The Guidelines add: "Please note that the NCSC does not provide assistance or guidance in determining product scope or general regulatory applicability." The letter to NCSC is therefore limited to the reporting questions (A and D) and coordinator confirmation for steward filings.

**Ireland's market surveillance authority.** Not designated on the evidence found. The knowledge base records the NCSC as "anticipated" and Ireland as "Not formally designated as of 14 Sep 2026" (reports/sections/14-enforcement.md). Arthur Cox wrote on 8 Oct 2026 that "Ireland may need to rely on implementing measures to designate a national market surveillance authority" and that "the precise form and timing of any such measures have not yet been confirmed". The government press release of 11 Sep 2026 names the Department of Justice, Home Affairs and Migration as lead department and designates no authority. One secondary tracker (Presencis, dated 4 Oct 2026) lists "CSIRT-IE / NCSC-IE" as the Irish designated authority with status "Implementing"; we found no Irish legal instrument behind it, so we treat it as unconfirmed. Until a designation is made, scope and classification questions (B, C, E, F, G, H) should go to the Department of Justice, Home Affairs and Migration asking for routing, with NCSC in copy, and be re-addressed to the authority once it is named. A favourable answer from an authority that is not yet designated binds no one.

**EU level.** The Commission wrote the guidance and the FAQ and holds the Art 27(9) and Art 8(1) delegated powers. Its CRA Expert Group (register E03967) is the channel where industry associations raise interpretive points; Aldermoor should route questions B, C, E and H through its trade associations' members there. ADCO, the group of market surveillance authorities under Art 52(15), is chaired by BSI (reports/sections/14-enforcement.md) and must publish "indicative support periods" under Art 52(16), which makes it the right forum for question F. ENISA runs the SRP and answers platform questions through its FAQ; data-model questions (A, D) go through NCSC. External counsel should give written opinions on all eight, because neither the guidance nor the FAQ binds a court.

## A. One Art 14 notification per product, or one per vulnerability across products

**Question.** When one actively exploited vulnerability sits in shared code (for example a Lumen Engine bug reachable in Lumen Browser desktop and mobile, Lumen WebView, Lumen OS, the Drive sync client and the Hearth Hub display), does Aldermoor submit one SRP notification listing all affected products, or one per product?

**Why it matters.** Module E2 models 92 SRP records and 413 submissions a year under the per-product rule FO-1, against 33 records and 146 submissions if grouped (base case). The peak case is 6 records and 12 submissions in the first 72 hours against 1 and 2. Headcount barely moves, because the 24/7 filing seat sets a floor of 5.5 FTE either way; the risk is transcription and timing under pressure. Module G shows the same swing for Google: about 40 records a year per product against about 15 grouped. Per-platform builds count as distinct products under guidance para 14, which pushes the per-product number up.

**Relevant text.**
- Art 14(1): "A manufacturer shall notify any actively exploited vulnerability contained in the product with digital elements that it becomes aware of simultaneously to the CSIRT designated as coordinator".
- Art 14(2)(a): "indicating, where applicable, the Member States on the territory of which the manufacturer is aware that their product with digital elements has been made available". Art 14(2)(b) asks for "general information, as available, about the product with digital elements concerned".
- Art 14(2)(c): the final report is due "no later than 14 days after a corrective or mitigating measure is available".
- ENISA SRP FAQ 8 (15 Oct 2026): "Only one notification is required for any given actively exploited vulnerability (AEV) or severe incident (SI), even when a manufacturer has multiple branches or subsidiaries in the EU".
- Commission FAQ 5.4: "The manufacturer of the integrated component is also required to notify it, if that component has been placed on the market."
- Guidance para 218: "Where a product with digital elements contains an actively exploited vulnerability originating from a third-party component, the manufacturer of the product with digital elements is required to notify that actively exploited vulnerability."
- Guidance para 204, on shared back-ends: "If the same RDPS supports several products with digital elements, the RDPS needs to be declared in each product's technical documentation."

Neither the guidance (section 9.1, paras 209-221) nor the ENISA FAQ (35 questions) addresses several products of one manufacturer in one record.

**Interpretations.**
1. *Per vulnerability.* "Any given AEV" in ENISA FAQ 8 means one notification per manufacturer per vulnerability; the products are content of that notification.
2. *Per product.* The duty is drafted around "the product", the 72-hour content is about "the product ... concerned", and the final-report clock runs from a measure for that product. Each product therefore needs its own notification. The SRP's single product field (per the SRP glossary, recorded in the knowledge base) points the same way.
3. *Per product family.* One record for products that share code, a fix and a release train; separate records where fixes ship separately.

**Recommended position.** The obligation attaches to each product, but nothing in Art 14 requires a separate submission per product. A single notification that names every affected product and version, gives the Member States for each, and tracks each product's corrective measure meets the text. Until NCSC confirms in writing that it accepts this, operate FO-1 (one record per product, cross-referenced by a shared case identifier), as module E2 recommends.

**Conservative fallback.** FO-1 permanently. It costs about 280 extra submissions a year at base volume and, in the peak case, ten extra submissions in 72 hours that two filer pairs can absorb (E2 Exhibit 2).

**Evidence to hold.** The fan-out record per case (product, version, reachability tier, Member States); the shared case identifier in each record's title and summary; the NCSC reply; screenshots of each submitted tab.

**Who should confirm.** NCSC as coordinator CSIRT (letter in this folder, question 1). NCSC may consult ENISA on the SRP data model. ADCO or the Commission could later harmonise practice across CSIRTs; ask the Commission to add an FAQ entry.

## B. Per-version placing on the market for software, and the effect of continuous delivery

**Question.** For standalone software released continuously (Lumen Browser 4-weekly majors with weekly security updates; apps weekly), which releases are placings on the market, and what follows for declarations, support periods, notified-body change control and retention?

**Why it matters.** E1 sized its pipeline on "about 104,000 placing records a year" and its review load at about 12 FTE for release-level review, falling to about 2 FTE if the substantial-modification test moves to feature launch. E3 notes that treating every 4-weekly major as a new type would cost about EUR 33m a year in examinations for the three browser families at the high estimate, against under EUR 1m when the point 110 test is applied per release. E3's register (`classification.csv`, field versions_placed_per_year) sets 65 placings a year for each Lumen Browser family. Each placing needs a declared support period of at least five years (guidance para 128) and, under Module H, may need a change notice to the notified body (Annex VIII Part IV point 3.5).

**Relevant text.**
- Art 3(21): placing on the market is "the first making available of a product with digital elements on the Union market".
- Art 3(30): a substantial modification is a change "which affects the compliance of the product with digital elements with the essential cybersecurity requirements set out in Part I of Annex I or which results in a modification to the intended purpose".
- Recital 39: "Where a security update which is designed to decrease the level of cybersecurity risk of a product with digital elements does not modify the intended purpose of a product with digital elements, it is not considered to be a substantial modification."
- Art 13(13): documentation is kept "for at least 10 years after the product with digital elements has been placed on the market or for the support period, whichever is longer".
- Guidance para 13: "As long as this version of the software is not modified in a way that affects compliance with the CRA, the placing on the EU market is to be considered to have occurred at the moment of the first offering for distribution or use."
- Guidance para 14: "where the manufacturer makes software available in different variants that differ in their included components, configurations or enabled functionalities (for example, builds for different operating systems or bundles with differing feature sets), those variants cannot be regarded as multiple copies of the same software product with digital elements".
- Guidance para 15: "Iterations that do not qualify as substantial modifications do not require the manufacturer to perform a new conformity assessment procedure and therefore do not modify that software's date of placement on the market."
- Guidance Example 2: version 1.0.1, which "does not constitute a substantial modification", and version 1.0.0 "are considered to be placed on the market on 1 January 2028".
- Guidance para 131: "the declared support period for each substantially modified version must comply with Article 13(8) at the time it is placed on the market".
- Guidance Example 55: rearchitecting a cloud back-end, "introducing new APIs and data flows", can be a substantial modification with no client release.

**Interpretations.**
1. *Guidance reading.* A placing occurs at the first offering of the original version, at each substantial modification and for each distinct variant (for example the Windows, macOS, Linux and Android builds). Other versions are updates to a placed product and inherit its placing date.
2. *Every release is a placing.* The reading three Enterprise papers took (corrections_enterprise.md C-01 to C-04). It has no support in the guidance text and multiplies declarations and support-period declarations.
3. *Every download is a placing.* Rejected by para 14: copies are "placed on the market at the same time, regardless of when possession or use of each individual copy is transferred".

**Recommended position.** Interpretation 1. Record every version (the documentation must stay current under Art 31(2) and guidance para 113), but tag each as "new placing" (substantial modification or new variant) or "update to placed product" with the inherited placing date. Run the point 110 test at feature launch and roll the answers up to the release. Treat server-side feature enablement and back-end changes as candidates for substantial modification too (Example 55), so the release gate must cover remote data processing releases, not only client builds. Keep the family approach for documentation (guidance paras 174-177) so that platform variants share one technical file and one declaration that lists them.

**Conservative fallback.** Treat each 4-weekly Lumen major as a presumptive substantial modification, with a declaration update and a Module H change notice, unless the point 110 record shows all four answers negative. Keep E1's retention calculation on the version date, which gives a later retain-until date than the inherited placing date.

**Evidence to hold.** Release metadata with change type, the four point 110 answers and the assessor; a version-to-placing map; the feature-flag register showing which features the risk assessment already anticipated (Examples 42-43); the platform-variant list per declaration.

**Who should confirm.** The Commission as author of paras 13-15 (via the Expert Group); the Irish market surveillance authority once designated; Aldermoor's notified body on change-notice practice under Module H; external counsel. Not NCSC, which does not advise on scope.

## C. Art 32(2): certification schemes "as referred to in Article 27" as a route to Module A for Class I

**Question.** Can a Class I product use Module A because it holds a certificate at assurance level "substantial" under a scheme adopted under the Cybersecurity Act (today, EUCC), before any delegated act under Art 27(9) specifies that scheme for the CRA?

**Why it matters.** E3 places 16 Class I families on Module H, with 720-1,460 notified-body days in the first wave and EUR 3.2m-9.3m over five years, in a market where no CRA notified body had been designated at the last check (8 Sep 2026). A usable scheme route would be a relief valve for schedule risk. In practice the gain is small: EUCC is a Common Criteria scheme and does not by itself cover the Annex I Part II vulnerability-handling requirements (base register, E6 paper).

**Relevant text.**
- Art 32(2): "has not applied or has applied only in part harmonised standards, common specifications or European cybersecurity certification schemes at assurance level at least 'substantial' as referred to in Article 27".
- Art 27(8): products "for which an EU statement of conformity or certificate has been issued under a European cybersecurity certification scheme adopted pursuant to Regulation (EU) 2019/881 shall be presumed to be in conformity with the essential cybersecurity requirements set out in Annex I in so far as the EU statement of conformity or European cybersecurity certificate, or parts thereof, cover those requirements".
- Art 27(9): the Commission may adopt delegated acts "specifying the European cybersecurity certification schemes adopted pursuant to Regulation (EU) 2019/881 that can be used to demonstrate conformity", and a certificate under such schemes at least at "substantial" "eliminates the obligation of a manufacturer to carry out a third-party conformity assessment for the corresponding requirements, as set out in Article 32(2), points (a) and (b)".
- Art 32(1)(d) and 32(3)(c) both refer to a scheme "pursuant to Article 27(9)".
- Recital 91: the manufacturer "should apply harmonised standards, common specifications or European cybersecurity certification schemes adopted pursuant to Regulation (EU) 2019/881 which have been identified by the Commission in an implementing act if it wants to carry out the conformity assessment under its own responsibility (module A)".
- Annex VII point 5 lists schemes "adopted pursuant to Regulation (EU) 2019/881 pursuant to Article 27(8) of this Regulation".
- Guidance footnote 25 to para 148: "the same guidance also applies to common specifications adopted in accordance with Article 27(2) and to European cybersecurity certification schemes where specified by the Commission via delegated acts in accordance with Article 27(9)".
- Guidance para 153 reads the Art 27(8) presumption as applying "if this has been specified via delegated acts in accordance with Article 27(9)".

**Interpretations.**
1. *Any Art 27 scheme.* "As referred to in Article 27" includes Art 27(8), which needs no delegated act; Annex VII point 5 also speaks of Art 27(8) schemes. A full-scope "substantial" certificate opens Module A now.
2. *Only Art 27(9) schemes.* Art 27(9) is the provision that removes third-party assessment "as set out in Article 32(2)"; Art 32(1)(d) and 32(3)(c) name 27(9); recital 91 requires schemes "identified by the Commission"; the Commission guidance says so in terms.
3. *Practical convergence.* Even under reading 1, Module A needs every applicable Annex I requirement to be covered. No current scheme covers Part II, so the outcome today is the same.

**Recommended position.** Reading 2. It is the Commission's stated reading and the one a market surveillance authority will start from. Plan Module H for all Class I families (E3), keep the gate's route rule as it is (E1), and revisit when the Art 27(9) act is adopted (planned Q4 2026 on the Commission's factpage; not adopted at 30 Oct 2026).

**Conservative fallback.** The same. Counsel should test reading 1 only for a product that already holds a full-scope EUCC certificate.

**Evidence to hold.** A register of EUCC certificates held (product, target of evaluation, AVA_VAN level, validity) mapped to Annex I Part I and Part II items; the Module H plan.

**Who should confirm.** The Commission, through the Art 27(9) act and the Expert Group; external counsel; notified bodies on how they will treat EUCC evidence under Module H. Not NCSC.

## D. Open-source steward and manufacturer for the same codebase: double reporting under Art 14 and Art 24

**Question.** Aldermoor leads Lumen Engine and HOSP as unmonetised projects (steward) and ships products built on them (manufacturer). From 11 Dec 2027, when one exploited engine bug is found, does it file once or twice? And what if exploitation is seen only in a third-party product built on the engine?

**Why it matters.** E2's base inputs put about 10 exploited Lumen Engine or browser vulnerabilities a year and about 8 in Halo OS and Arc devices. If most engine cases and part of the Halo OS cases also trigger steward filings, that adds roughly 10-18 records a year from 11 Dec 2027 (estimate), each on a 24-hour clock. Module G estimates 8-12 extra steward filings a year for Google. E4 recommends naming Aldermoor Ireland Ltd as the steward entity, which makes NCSC the likely coordinator for both roles if that entity is also the manufacturer; if the manufacturer is a different group company, there are two legal persons and two duties.

**Relevant text.**
- Art 3(14): a steward is "a legal person, other than a manufacturer, that has the purpose or objective of systematically providing support on a sustained basis for the development of specific products with digital elements".
- Art 24(3): "The obligations laid down in Article 14(1) shall apply to open-source software stewards to the extent that they are involved in the development of the products with digital elements. The obligations laid down in Article 14(3) and (8) shall apply to open-source software stewards to the extent that severe incidents having an impact on the security of products with digital elements affect network and information systems provided by the open-source software stewards for the development of such products."
- Commission FAQ 5.5: "In accordance with Article 71(2) of the CRA, Article 24(3) shall apply from 11 December 2027."
- Guidance para 73: "A legal person may therefore simultaneously be a steward for one specific FOSS (where the steward systematically provides support on a sustained basis and ensures the software's viability) and a manufacturer for another specific FOSS".
- Guidance para 76: "a legal entity that develops FOSS for integration into its own products with digital elements and then publishes it without placing it on the market ... is not a manufacturer of the software, but may be a steward to it".
- Guidance para 82: a steward providing engineering resources must "notify, in accordance with Article 14(1), of actively exploited vulnerabilities that it becomes aware of".
- Guidance para 216: "a steward is likely to become aware of active exploitation via reports from third parties, which identify exploitation in FOSS components as integrated into other products with digital elements".
- ENISA SRP FAQ 8: "Only one notification is required for any given actively exploited vulnerability (AEV) or severe incident (SI)".

**Interpretations.**
1. *One filing per legal person.* If the same legal person holds both roles, one notification that identifies both capacities, the products and the project meets both duties. Supported by "any given AEV" in ENISA FAQ 8.
2. *Two filings.* Art 14(1) via Art 24(3) and Art 14(1) directly are separate obligations with different subjects (the project, the product) and different triggers. The SRP associates Assigned Representatives with a "manufacturer" or a "steward"; the roles are filed separately.
3. *Steward filing only where no manufacturer filing exists.* Where Aldermoor has filed as manufacturer, the steward filing adds nothing the CSIRT lacks. Attractive, but no text supports it, and "unless the relevant information has already been provided" in Art 14(2)(b)-(c) applies only to later stages of the same notification.

Where exploitation is seen only in a third-party product, only the steward duty arises for Aldermoor; the other manufacturer files for its product (FAQ 5.4).

**Recommended position.** Treat the duties as distinct. From 11 Dec 2027 file per product as manufacturer (rule FO-1) and once per project as steward, each cross-referencing the other, unless NCSC confirms in writing that one record flagged with both capacities is acceptable. Before 11 Dec 2027, steward-type reports are voluntary under Art 15; make them where Aldermoor already has the facts. Decide which legal entity is steward and which is manufacturer before Jun 2027, because the answer to this question depends on it.

**Conservative fallback.** Always two filings, including where the same legal person holds both roles.

**Evidence to hold.** A steward designation per project naming the legal entity (E4 decision 1); the Art 24(1) policy; a map of products to projects and versions; the case record showing the capacity of each filing; the NCSC reply.

**Who should confirm.** NCSC (letter, questions 2 and 3); ENISA via NCSC on the SRP role model; the Commission, which owns FAQ 5.5 and could add an entry.

## E. Operating system integrated in a device (Example 58) versus operating system supplied separately to OEMs

**Question.** An OS inside Aldermoor's own Arc phone does not make the phone an "operating system" product. When Aldermoor supplies OS code to other device makers (HOSP source, the Halo Services package, Halo Wear OS images), when is it placing an operating system on the market as a component, and so a Class I item 11 product?

**Why it matters.** E3 Exhibit 6 ranks this first: EUR 6.8bn of illustrative enabled revenue (the Halo Services package, F06) would move to the notified-body route and every OEM build would need an item 11 assessment if Aldermoor were held to supply a complete OS. Arc devices (EUR 9.5bn for phones) depend on Example 58. E4 flags the Halo partner early-access programme, which ties earlier security patches to a commercial agreement, as a monetisation trigger that could make Aldermoor the manufacturer of HOSP releases.

**Relevant text.**
- Art 3(1): a product with digital elements includes "software or hardware components being placed on the market separately".
- Art 7(1): integrating an Annex III product "shall not in itself render the product in which it is integrated subject to the conformity assessment procedures referred to in Article 32(2) and (3)".
- IR 2025/2392, Annex I point 11: operating systems are "Software products with digital elements that provide an abstract interface of the underlying hardware and control the execution of software".
- Guidance Example 58: "The mere integration of an operating system does not mean that the smartphone has the core functionality of an operating system."
- Guidance para 24: "where a manufacturer provides its customers with computer code as a product with digital elements, that code is considered to be placed on the market, regardless of whether it is machine code or source code".
- Guidance Example 7: a company that "licences source code to company B" is "placing that source code on the market".
- Guidance para 145: modules made available separately "constitute standalone products with digital elements in their own right".
- Guidance para 67: FOSS "intended for integration by other manufacturers into their own products" is "not considered to be placed on the EU market, unless it is also monetised by the person that publishes it".
- Guidance para 57: "access to a specific version of the product with digital elements including certain benefits such as technical assistance or performance optimisation, is conditioned on remuneration" is a placing.

**Interpretations.**
1. *Public source, OEM builds.* Aldermoor publishes HOSP free to all and is its steward; each OEM builds and places its own device and is manufacturer of the whole; Aldermoor's separately licensed services package is a default-class component. This is E3's position.
2. *OS supplied as a component.* If Aldermoor supplies OS images, binaries or licensed source to OEMs under contract (as it does for Halo Wear OS, F07), it places an item 11 component on the market.
3. *Monetised HOSP.* If access to HOSP releases or patches depends on a commercial agreement, HOSP itself is placed on the market (paras 57, 62 by analogy) and Aldermoor is manufacturer of an item 11 operating system.

**Recommended position.** Interpretation 1 for HOSP and the services package, and Example 58 for Arc devices, provided the facts stay consistent: HOSP releases and fixes public to all on the same day; no OS image or licensed source supplied for payment; the services package documented and marketed as applications and services, not as an OS (guidance para 143 on misrepresentation). Keep Halo Wear OS (F07) as Class I item 11, as E3 already does.

**Conservative fallback.** Treat every OS image or licensed build supplied to an OEM as an item 11 component, bring it into the Platforms Module H scope, and budget the extra notified-body days.

**Evidence to hold.** OEM contracts and supply records showing what is delivered (source, binaries, images); HOSP release and patch publication logs; the decoupled early-access terms (E4 decision 2); marketing and documentation review records.

**Who should confirm.** The Irish market surveillance authority once designated; the Commission through the Expert Group; external counsel. Not NCSC.

## F. Support-period floor per unit or per product type, for devices on sale before and after 11 Dec 2027

**Question.** A device model launched in 2026 stays on sale into 2029. Units placed before 11 Dec 2027 are outside the CRA's product rules. For units placed later, does the five-year floor run from each unit's placing, or can Aldermoor declare one end date for the model?

**Why it matters.** Arc phones carry a 7-year support commitment from launch (E3 portfolio). Under a per-unit reading, a unit placed more than two years after launch would get less than five years, so EU placing of each model must stop two years after launch or support must be extended for later units. Hearth and Pulse devices often sell for longer. Module G shows the effect for published policies such as Pixel Watch (three years) and Fitbit (two years after last sold). E5 notes JC-STAR labels expire after two years, so a longer per-unit tail means more renewals. Art 13(19) requires the end date at the time of purchase, so retail channels need end dates per cohort.

**Relevant text.**
- Art 13(8), first subparagraph: "Manufacturers shall ensure, when placing a product with digital elements on the market, and for the support period, that vulnerabilities of that product, including its components, are handled effectively".
- Art 13(8), third subparagraph: "the support period shall be at least five years. Where the product with digital elements is expected to be in use for less than five years, the support period shall correspond to the expected use time."
- Art 13(19): the end date, "including at least the month and the year, is clearly and understandably specified at the time of purchase".
- Art 69(2): products placed before 11 Dec 2027 "shall be subject to the requirements set out in this Regulation only if, from that date, those products are subject to a substantial modification".
- Guidance para 11 (quoting the Blue Guide): placing refers "to each individual product, not to a type of product".
- FAQ 4.5.3: "for units of that product that are newly placed on the market, manufacturers are required to set the support period", and in its example of later units of the same model, "The manufacturer is required to set a support period for those units, in accordance with Article 13(8) of the CRA."
- FAQ 7.2: "Union harmonisation legislation including the CRA applies to individual products, and not product types."
- Art 52(16): ADCO is to "provide guidance that includes indicative support periods for categories of products with digital elements".

**Interpretations.**
1. *Per unit.* Each unit placed from 11 Dec 2027 is a product placed on the market and must get a support period meeting Art 13(8) from its own placing.
2. *Per model.* The support period reflects the model's expected use time, set once at first placing; later units get the remainder. Para 134 uses similar logic for substantially modified products, but it does not concern later units.
3. *Per model with a floor per unit.* One model end date, extended for later cohorts so each has at least five years. In effect the same as reading 1.

**Recommended position.** Reading 1, implemented as reading 3: an end date per placing cohort (for example by quarter of placing) equal to the later of the model end date and cohort placing plus five years, unless a shorter expected use time is documented. Units placed before 11 Dec 2027 carry no CRA support duty unless substantially modified, but remain under Art 14.

**Conservative fallback.** The same; it is already the conservative reading.

**Evidence to hold.** Placing-cohort records from distribution and importer data; the Art 13(8) rationale per model (Annex VII point 4); the point-of-sale end-date feed per SKU and cohort; the end-of-support notification design (Art 13(19), second subparagraph).

**Who should confirm.** The Irish market surveillance authority; ADCO through its indicative-support-period guidance; external counsel. Not NCSC.

## G. FIDO authenticator with a secure element: Class I item 1 or Annex IV item 3

**Question.** Keystone keys (F25) are FIDO hardware authenticators built around a secure element. Is the core functionality "identity management ... including authentication" (Annex III Class I item 1) or "smartcards or similar devices, including secure elements" (Annex IV item 3)?

**Why it matters.** Today the route is the same: a Class I product with no cited standard needs Module B+C or H, and an Annex IV product goes to the Art 32(3) procedures while no Art 8(1) act exists. E3 puts Keystone in the Devices Module H system, at about EUR 45m of illustrative revenue. The difference comes later. A Class I product can move to Module A once a standard for item 1 is cited; an Annex IV product cannot. And an Art 8(1) delegated act could make EUCC certification mandatory for Annex IV item 3, with "a minimum transitional period of six months".

**Relevant text.**
- Annex III Class I item 1: "Identity management systems and privileged access management software and hardware, including authentication and access control readers, including biometric readers".
- Annex IV item 3: "Smartcards or similar devices, including secure elements".
- IR 2025/2392, Annex I point 1 includes "hardware authentication devices such as transaction authentication number (TAN) generators".
- IR 2025/2392, Annex II point 3: "Secure elements are designed to provide protection of at least AVA_VAN.4" and "Smartcards or similar devices are secure elements integrated into a carrier material, such as plastic or wood, in the shape of a card, or secure elements integrated into carrier materials taking other shapes", with examples including "physical access cards" and "wrist bands with integrated payment secure elements".
- Art 8(1): where no delegated act has been adopted, Annex IV products "shall be subject to the conformity assessment procedures referred to in Article 32(3)".
- Guidance para 152: a product whose core functionality is Class I stays Class I "even though it integrates a component that is itself a critical product with digital elements".
- FAQ 3.2: "integrating a secure element into a laptop does not in itself render the laptop subject to the conformity assessment procedure" for secure elements.

**Interpretations.**
1. *Annex IV item 3.* A key whose substance is a secure element in a plastic or metal housing is a secure element "integrated into carrier materials taking other shapes". The IR's examples (access cards, payment wristbands) are close analogues.
2. *Class I item 1.* The key is a hardware authentication device (the IR's own words for item 1); the secure element is an integrated component, and para 152 keeps the host's class.
3. *Below the threshold.* If the chip is not designed to AVA_VAN.4, it is not a "secure element" in the IR's sense, and item 1 applies.

**Recommended position.** Reading 1 for Keystone models whose secure element is designed to AVA_VAN.4 or higher and performs the authentication functions, because the key adds little beyond the chip and its interfaces. Reading 2 for authenticators with substantial functions outside the secure element (for example a biometric reader or display handled by a separate processor). This changes E3's planning basis for Keystone from item 1 to Annex IV item 3; the route today is unchanged.

**Conservative fallback.** The same. Plan for EUCC at "substantial" or higher for Keystone regardless.

**Evidence to hold.** The secure element's AVA_VAN design target and certificate; an architecture note showing which functions run inside and outside the secure element; marketing and documentation consistency (para 143).

**Who should confirm.** The Commission, as author of IR 2025/2392 and holder of the Art 8 powers; the Irish market surveillance authority; the notified body that will assess Keystone; external counsel. Not NCSC.

## H. Remote data processing boundary for cloud consoles and installed clients

**Question.** Aldermoor Cloud's consoles run only in a browser. Its installed products (Drive sync client, Cloud CLI and SDKs, Cloud Connect connectors, mobile apps) call Aldermoor services. Which of those services are remote data processing solutions (RDPS) and so part of the installed products under the CRA?

**Why it matters.** E3 treats the consoles as out of scope (two families; EUR 9bn of service revenue, not product revenue) and lists "Cloud APIs the CLI calls" as RDPS of the CLI (F30). Whatever is RDPS must meet Annex I, must be in each product's technical documentation, and is in scope for Art 14 severe-incident reporting (guidance para 178). An incident on a shared API front-end could then be a CRA severe incident for several products and a NIS2 incident for the cloud service, the multi-regime case E2 already plans for. Changes to RDPS can be substantial modifications without any client release (Example 55), so the E1 gate must cover them.

**Relevant text.**
- Art 3(2): remote data processing is "data processing at a distance for which the software is designed and developed by the manufacturer, or under the responsibility of the manufacturer, and the absence of which would prevent the product with digital elements from performing one of its functions".
- Recital 11: "Such processing or storage at a distance includes the situation where a mobile application requires access to an application programming interface or to a database provided by means of a service developed by the manufacturer. In such a case, the service falls within the scope of this Regulation as a remote data processing solution."
- Recital 12: "Directive (EU) 2022/2555 applies to cloud computing services and cloud service models".
- Guidance para 21 and Example 5: "a web application accessed by the user exclusively through a web browser is not a product with digital elements".
- Guidance para 190 lists functions including "synchronising files", "automated distribution of updates, including feature update and security patching" and "identity and access management".
- Guidance para 182: CI/CD pipelines and "the distribution of security updates to edge locations, should not be considered as RDPS".
- Guidance para 205: RDPS "should be limited to those software modules that are responsible for the functionality of the product with digital elements, and to the interfaces those modules use with external services. Further back-end systems that carry out subsequent processing, and with which the product with digital elements does not directly interact, are not considered RDPS."
- Guidance section 8.3.1 (banking app): "the CRA covers only those parts of the system that interact directly with the product with digital elements".
- Guidance para 194: "an authentication portal that issues credentials or tokens required for the product with digital elements to operate would be considered RDPS".

**Interpretations.**
1. *Direct-interaction boundary.* RDPS is the Aldermoor-designed software the installed client talks to directly: API gateways and front-end services, the sync service front-end, identity and token services, configuration and update-check endpoints. Back-ends behind them are external dependencies for the risk assessment (para 206), not RDPS.
2. *Whole-service boundary.* The whole cloud service a client fronts is RDPS (a broad reading of recital 11).
3. *Service-first boundary.* Where the client is an optional convenience for a service mainly used in a browser or by API, the service is a NIS2 cloud service only. Weak: the Art 3(2) test is about whether the client's functions fail without it, and they do.

**Recommended position.** Interpretation 1, with an RDPS register per installed product that names each endpoint, the functions that fail without it and whether Aldermoor designed it. Consoles stay out unless a console page issues credentials or tokens an installed product needs (para 194).

**Conservative fallback.** For services where an installed client is the main access path (the Drive storage sync service), treat the service's whole control plane as RDPS of that client.

**Evidence to hold.** The RDPS register; architecture diagrams marking the direct-interaction boundary; the risk assessment of back-ends as dependencies; due diligence on third-party SaaS used by clients (paras 200-201).

**Who should confirm.** The Commission through the Expert Group; the Irish market surveillance authority; external counsel. NCSC only for the reporting consequence, which is folded into question 1 of the letter.

## Decisions for the executive team

1. **Send the letter to NCSC (questions A and D, and coordinator confirmation for steward filings).** Owner: General Counsel with the Head of Product Security. Timing: by 30 Nov 2026 (E2 decision 1).
2. **Instruct external counsel on all eight questions using `counsel-brief.md`.** Owner: General Counsel. Timing: instruct by 15 Nov 2026; Art 32(2) note by 30 Nov 2026; all notes by 31 Jan 2027.
3. **Adopt the recommended positions as interim policy and record them in the E3 register and the E1 gate policy.** In particular: version records tagged "new placing" or "update to placed product" (B); per-cohort support end dates (F); Keystone planned as Annex IV item 3 (G); an RDPS register per installed product (H). Owner: CISO with VP Engineering. Timing: by 31 Jan 2027.
4. **Name the steward and manufacturer legal entities.** Question D cannot be closed until this is decided. Owner: General Counsel. Timing: by Mar 2027 (E4 decision 1).
5. **Route questions B, C, E, F, G and H to the Commission through trade-association members of the CRA Expert Group, and to the Irish market surveillance authority once designated.** Owner: Head of Regulatory Affairs. Timing: Q1 2027, then on designation.

## Risks and open questions

- **No Irish market surveillance authority.** Five of the eight questions are for the authority that will enforce them, and none existed on the evidence found to 8 Oct 2026. Answers from any other body are informal.
- **Guidance status.** C(2026) 5252 applies only once formally adopted; paragraph numbers could change. The register and this pack cite the Commission PDF of 27 Jul 2026 by hash; re-run `build_claims_enterprise.py` and `check_positions.py` on adoption.
- **NCSC remit.** NCSC states it does not advise on scope or applicability. It may decline even questions A and D as platform matters for ENISA.
- **Non-binding sources.** The guidance, FAQs and any authority letter do not bind a court. Counsel's opinions should say where the CRA text alone supports the recommended position.
- **Facts drive E and G.** OEM supply terms and the secure element's design target decide those questions more than law does. Keep both under change control (E3 decision 4).

## Sources

- Regulation (EU) 2024/2847, OJ L, 2024/2847, 20.11.2024, Publications Office cellar copy: `../source/oj_L_2024_2847_EN.txt` (Arts 3(1), 3(2), 3(14), 3(21), 3(30), 7(1), 8(1), 13(8), 13(13), 13(19), 14, 24(3), 27, 32, 52(16), 69(2); recitals 11, 12, 39, 91; Annexes III, IV, VII).
- Commission guidance C(2026) 5252 final, Annex, 27 Jul 2026, [Commission download](https://ec.europa.eu/newsroom/dae/redirection/document/131456) (`../source/guidance/C_2026_5252_annex_guidance_EN.pdf`), and Communication [131455](https://ec.europa.eu/newsroom/dae/redirection/document/131455); [Commission news page](https://digital-strategy.ec.europa.eu/en/library/commission-publishes-new-guidance-support-timely-cyber-resilience-act-implementation).
- Commission FAQ on the CRA v1.4, 4 Sep 2026, [Markdown](https://ec.europa.eu/newsroom/dae/redirection/document/123307) and [PDF](https://ec.europa.eu/newsroom/dae/redirection/document/122331).
- Commission Implementing Regulation (EU) 2025/2392 (`../source/IR_2025_2392_EN.txt`).
- [ENISA SRP FAQ](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/frequently-asked-questions), updated 15 Oct 2026.
- [NCSC Ireland CRA page](https://www.ncsc.gov.ie/cra/), last updated 11 Sep 2026; [National CRA Guidelines v1](https://www.ncsc.gov.ie/pdfs/National_CRA_Guidelines_v1.pdf), 31 Aug 2026.
- [Government of Ireland press release, 11 Sep 2026](https://www.gov.ie/en/department-of-justice-home-affairs-and-migration/press-releases/cyber-resilience-act-guidelines-published-as-reporting-obligations-come-into-effect/) (lead department; no designation).
- [Arthur Cox, "Countdown to compliance", 8 Oct 2026](https://www.arthurcox.com/knowledge/countdown-to-compliance-the-cyber-resilience-act-reporting-deadline-has-arrived/) (market surveillance authority not yet designated).
- [Presencis, CRA national implementation tracker, 4 Oct 2026](https://cdn.presencis.com/regulations/cra/national/) (secondary; lists CSIRT-IE / NCSC-IE, status "Implementing"; unconfirmed).
- Knowledge base: reports/sections/14-enforcement.md (Irish status at 14 Sep 2026; ADCO chair); reports/sections/11-standards.md (Expert Group E03967); reports/sections/16-watchlist.md (Art 27(9) act timing).
- Enterprise modules: E1 `../../evidence-as-code/paper.md`; E2 `../../art14-operations/paper.md` and `volume_model_output.csv`; E3 `../../portfolio-classification/paper.md` and `classification.csv`; E4 `../../open-source-strategy/paper.md`; E5 `../../global-control-set/paper.md`; G `../../google-outside-in/paper.md`.
