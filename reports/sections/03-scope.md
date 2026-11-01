## Scope: what the CRA covers

A product is in scope when three cumulative conditions in Art 2(1) of the [CRA](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) are met. It is a product with digital elements, and it is made available on the EU market in a commercial activity. Its intended or reasonably foreseeable use includes a data connection to a device or network, direct or indirect, logical or physical.

The [Commission FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307) and the [Art 26 guidance C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) both apply this three-part test. The operative article text in this doc was checked on 1 Nov 2026 against the authentic OJ text (OJ L, 2024/2847, 20.11.2024, Publications Office cellar) and the English corrigenda; see the E6 claims register.

### Definitions that decide scope

Art 3 has 51 definitions. The ones below settle most scope and role questions.

| Term | Art 3 point | Meaning in plain words | Engineering note |
|---|---|---|---|
| Product with digital elements | (1) | A software or hardware product and its remote data processing solutions, including components placed on the market separately | A library, SDK, driver, firmware image or chip sold on its own is a product with its own manufacturer |
| Remote data processing | (2) | Processing at a distance, built by or under the responsibility of the manufacturer, without which the product cannot perform one of its functions | Your backend is in scope; a licensed third-party SaaS you integrate is a component instead |
| Software | (4) | The part of an electronic information system that consists of computer code | Covers source code as well as machine code (guidance para 22) |
| Hardware | (5) | A physical system, or parts of one, able to process, store or transmit digital data | Integrated circuits and motherboards count (guidance para 18) |
| Component | (6) | Software or hardware intended for integration into an electronic information system | Component status does not remove a separately sold item from scope |
| Logical, physical and indirect connection | (8)-(10) | Software interfaces; electrical, optical, mechanical or radio links; connection through a larger system that is itself connectable | Indirect connection is what brings offline desktop software into scope |
| Manufacturer | (13) | Whoever develops or has developed the product and markets it under its own name or trademark, paid or free | Outsourced development under your brand still makes you the manufacturer |
| Support period | (20) | The period during which vulnerabilities must be handled under Annex I Part II | At least 5 years unless the expected use time is shorter (Art 13(8)) |
| Placing on the market | (21) | The first making available on the EU market | Judged per unit; for standalone software, per version (guidance paras 13-14) |
| Making available on the market | (22) | Supply for distribution or use in the course of a commercial activity, paid or free | Free supply by a business is still caught (Recital 15) |
| Intended purpose | (23) | The use the manufacturer specifies in instructions, marketing and technical documentation | Your marketing copy defines the assessed purpose |
| Reasonably foreseeable use | (24) | Use likely to result from foreseeable human behaviour or technical interaction, even if not intended | The connection test is run against this, not only the intended purpose |
| Substantial modification | (30) | A post-placing change that affects Annex I Part I compliance or alters the assessed intended purpose | Triggers a new placing on the market; see below |
| Security update and functionality update | not defined in Art 3 | The guidance and FAQ distinguish fixes that reduce risk from changes that add features | Ship them separately where technically feasible (Annex I Part II(2)) |
| Free and open-source software | (48) | Software whose source is openly shared under a licence allowing free use, modification and redistribution | Monetisation, not licence, decides whether it is placed on the market |

The table paraphrases Art 3; each row was checked against the OJ text on 1 Nov 2026 (E6 claims register S03-S13).

### The data-connection test

The test is about exchanging digital information, not the presence of electronics. The guidance (paras 26-28) requires binary states deliberately encoded as information and decodable at the destination. A signal that only triggers or powers a function is not a data connection.

The FAQ lists a dishwasher with cycle firmware, a basic calculator and a toy with pre-recorded effects as out of scope. It adds that the same firmware sold separately may be in scope.

Indirect connections count. Recital 9 covers products "only indirectly connected". The FAQ treats an offline text editor on a networked operating system as in scope.

Almost all commercial software is therefore in scope. The live questions are who the manufacturer is and whether a backend is remote data processing.

### Remote data processing versus SaaS

The guidance applies a three-element test (paras 184-188). The processing is at a distance; the product needs it for one of its functions; and the manufacturer designed it or had it designed. Elements two and three are decisive and cumulative.

"At a distance" includes edge and on-premises deployments. Who operates the solution is not decisive (para 196).

"Functions" is broad (paras 189-192). Sending commands, synchronising files, onboarding, configuration, update distribution and identity and access management all count. Telemetry analysed only for statistics or future development does not.

The worked examples draw the line. A bank's self-hosted API that its mobile app calls is remote data processing; the ledger systems the app never talks to are not (section 8.3.1). An authentication portal that issues tokens the product needs is remote data processing (para 194).

A third-party support-chat SaaS embedded in an app is different. It is a component for Art 13(5) due diligence, not remote data processing (paras 197-202).

Browser-only software is not a product. Software must be "provided to a user" and run on the user's side (para 20). A progressive web app used only in a browser, or a website, is not a product (para 21, Examples 5-6).

Recital 12 sends cloud services built outside a manufacturer's responsibility to NIS2 (Directive (EU) 2022/2555). NIS2 covers medium-sized and larger SaaS, PaaS and IaaS providers. The same SaaS becomes remote data processing the moment the vendor ships an installed client that depends on it.

### Bespoke, internal and per-unit rules

Internal-use software is not placed on the market. The FAQ relies on Blue Guide section 2.3: a product "manufactured for one's own use" is not placed on the market. Internal build and configuration tools are out unless sold separately, and Recital 16 gives the same result for public bodies.

Bespoke software for one customer is placed on the market. Guidance Example 7 treats source code licensed to a single company as placed on the market by the licensor.

Such a product may use the tailor-made derogations for exactly two requirements. They are secure-by-default configuration (Annex I Part I 2(b)) and free security updates (Annex I Part II(8)). Both parties must have explicitly agreed different contractual terms (Recital 64).

A multi-tenant CRM with minor customisation is not tailor-made (FAQ). Keep the evidence of tailor-made status in the technical documentation.

Placing on the market is per unit, and for standalone software per version. All copies of a version are deemed placed at the first commercial offering, whatever the later download dates (guidance paras 13-14, Example 1). Non-substantial updates do not reset that date.

Variants that differ in components, configuration or enabled features are distinct products. Product families with the same architecture, security-relevant design, intended purpose and risks may share one risk assessment and one technical file. They may also share one declaration listing the variants (paras 174-177).

### Substantial modification

The test is risk-based, not size-based (guidance paras 104-110). Ask four questions about a change: new threat vectors; new attack scenarios; changed likelihood of known scenarios; changed impact. All-negative answers with the original risk assessment still valid mean no substantial modification (paras 111-112).

Security updates are "generally not" substantial, even when technically large (para 108). A "remember me" token-storage feature or an unencrypted log export is substantial because the risk was never assessed (Examples 44-45). A substantial modification is a new placing on the market with an assessment focused on the modified parts; see Conformity assessment and documentation.

### Hard cases

Rows marked "inference" rest on the researchers' reading, not on guidance text.

| Case | In or out | Why | Source |
|---|---|---|---|
| SaaS admin console used only in a browser | Out as a product; in only as remote data processing of an in-scope product | Guidance para 21, Examples 5-6; Recital 12 | [Guidance](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| Mobile app controlling the manufacturer's device | In; app and device are one product and the vendor's control, sync and update backends are remote data processing | Guidance para 25, Example 9; paras 189-192 | [Guidance](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| Internal tool used only by the developing company | Out; not placed on the market | FAQ, Blue Guide s.2.3; Recital 16 | [FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| Open-source library, free download, maintainer sells optional paid support | Out for the library if access and maintenance are not conditioned on payment; publisher may be a steward | Recital 18; guidance paras 55-58, Example 18 | [Guidance](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| Firmware security fix pushed to an in-scope device | Not a new product; not a substantial modification if it reduces risk and keeps the intended purpose | Recital 39; guidance para 108, Examples 46-48 | [Guidance](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| Firmware update adding new connectivity or control | Likely substantial; new placing on the market | Recital 39; guidance Examples 40, 44, 45; FAQ smart-TV example | [FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| Firmware image supplied separately to an OEM | In, as a component placed on the market separately | Art 3(1); FAQ product-forms list | [FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| PC with pre-installed operating system | In; the PC maker is manufacturer of the whole; a separately marketed OS is its own product | Guidance para 25, Example 8; para 120, Example 51 | [Guidance](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| Vendor-hosted API | Not a product itself; remote data processing where an in-scope client needs it; deeper backends out | Recital 11; guidance para 205, section 8.3.1 | [Guidance](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| SDK or library sold or monetised | In, as a software component placed on the market separately | Art 3(1), (6); guidance para 24, Example 7 | [Guidance](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| ML model weights file | Not addressed by guidance; inference: in when supplied as part of software executing on the user's side; a bare weights file is unresolved | Art 3(1), (4); guidance para 22 | [Guidance](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| Product sold only B2B | In; B2B status matters only for the tailor-made derogations | Art 2(1); Recital 64; FAQ | [FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| Free consumer app monetised by ads or personal data | In; free supply in a commercial activity | Art 3(22); Recital 15; guidance Examples 14-16 | [Guidance](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| Free, unmonetised, non-FOSS app from a company | Grey area; Blue Guide "business-related context" case by case; inference | Recital 15; guidance paras 40-41 | [Guidance](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| Offline desktop utility with no network code | In; indirect logical connection via the host OS | FAQ connection entry; Recital 9 | [FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| Open-category drone, not EASA-certified | In; only certified aviation products are excluded | Art 2(3); FAQ aviation entry | [FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| Dual-use product sold on the open market | In unless developed or modified exclusively for national security or defence | Art 2(7); Recital 26; FAQ | [FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |
| Identical-specification spare part via after-sales channel | Out; a part with different cryptography or secure boot is not identical and is in | Art 2(6); guidance paras 97-101, Examples 36-38 | [Guidance](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| Vendor CI/CD pipeline and update-distribution infrastructure | Out as remote data processing, but the user-facing update service a product calls can be in; inference reconciling paras 182 and 190 | Guidance paras 182, 190 | [Guidance](https://ec.europa.eu/newsroom/dae/redirection/document/131456) |
| Appliance with firmware and no connectivity | Out; no direct or indirect data connection | Art 2(1); FAQ examples; guidance para 28 | [FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) |

### Status of the guidance

The FAQ is a "living document" prepared by Commission services and is not an official Commission position. It was first published 3 Dec 2025 and reached v1.4 on 4 Sep 2026. The Commission told its Expert Group that the FAQ and the guidance have equal authoritative value.

Guidance C(2026) 5252 is non-binding; only the Court of Justice interprets the Regulation authoritatively (paras 7-9). The Commission approved its content on 27 Jul 2026 and said it "will be formally adopted" once all language versions exist. No evidence of adoption or OJ C-series publication was found by 30 Oct 2026, so it is formally a draft (see Open questions and watchlist).

Three corrigenda change the English text: 5 Dec 2024 (title: "(EU) 2019/1020"), 2 Jul 2025 (Art 64(10): the fines derogation runs from "paragraphs 2 to 9", not 3 to 9) and 17 Oct 2025 (Art 67: the CRA is point 72, not 69, of Annex I to Directive 2020/1828). Five more correct other language versions only (FR 3 Oct 2025 and 25 Mar 2026; SK 23 Feb 2026; DE 6 Aug 2026; SL 9 Oct 2026). No adopted amendment to scope, definitions or roles existed on 30 Oct 2026.
