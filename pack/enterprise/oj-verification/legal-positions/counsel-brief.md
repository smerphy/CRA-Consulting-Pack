# Instructions to external counsel: Cyber Resilience Act interpretive questions

**Privileged and confidential. Prepared for the purpose of obtaining legal advice.**

From: General Counsel, Aldermoor Ireland Ltd (contact: [Head of Product Security])
To: [Firm], [Partner]
Date: [Date]
Matter: CRA interpretive opinions, Aldermoor group
Reference: [Matter number]

## 1. What we need

Written opinions on eight questions on Regulation (EU) 2024/2847 (the CRA). Each opinion should state: the reading you consider correct; how confident you are (high, medium or low); the strongest argument against it; whether the Commission guidance or FAQ changes the answer; the enforcement and liability exposure if a market surveillance authority or court takes the other reading; and whether we should seek confirmation from an authority, and which one.

Timetable:
- Question C (Art 32(2)) by **30 Nov 2026**, because it feeds the notified-body contracting decision.
- Questions A and D by **15 Dec 2026**, so the opinion can be read with the reply we expect from Ireland's NCSC.
- Questions B, E, F, G and H by **31 Jan 2027**, in time for the executive team's ratification of the classification register.

Please send a fee estimate by return and tell us at once if any question needs a specialist in another Member State's law.

## 2. Background

The Aldermoor group is a US-headquartered technology group. Aldermoor Ireland Ltd in Dublin is its EU main establishment for Art 14(7); we file Art 14 notifications with Ireland's NCSC through the ENISA Single Reporting Platform. The products concerned include a mobile operating system with an open-source base (the Halo Open Source Project, HOSP) and a proprietary services package licensed to other device makers; Arc phones and tablets; Lumen Browser and its open-source engine (Lumen Engine), released in 4-weekly majors with weekly security updates; Lumen OS for laptops; Hearth smart-home devices; Pulse wearables; Keystone FIDO security keys; and Aldermoor Cloud with browser-only consoles and installed clients (desktop sync client, CLI and SDKs, connectors, mobile apps). The group leads several open-source projects it does not monetise.

Our internal positions are set out in the enclosed legal positions pack (`positions.md`), with the text of every provision and guidance passage relied on. You do not need to repeat that analysis; we want your view on it.

Status of sources at 1 Nov 2026: Art 14 has applied since 11 Sep 2026; the rest of the Regulation applies from 11 Dec 2027. Commission guidance C(2026) 5252 was approved on 27 Jul 2026 and will apply only once formally adopted in all languages. The Commission FAQ is at version 1.4 (4 Sep 2026). No CRA harmonised standard is cited, no Art 27(9) delegated act is adopted, and no CRA notified body had been designated at our last check (8 Sep 2026). We have found no designation of an Irish market surveillance authority for the CRA.

## 3. The questions

**A. Art 14 notifications for several products.** Does Art 14(1)-(2) require a separate notification for each product that contains the same actively exploited vulnerability, or may one notification cover several products of the same manufacturer? How should the 14-day final-report clock in Art 14(2)(c) be applied where corrective measures ship on different dates? Same questions for a severe incident in a back-end shared by several products. Is there any exposure in filing one notification per product when the authority would have preferred one?

**B. Placing on the market of software versions.** Is the guidance reading (paras 13-15, Example 2: non-substantial versions keep the original placing date; platform builds are distinct products, para 14) consistent with Art 3(21) and Art 3(30) and with the Blue Guide? What follows for: the EU declaration of conformity per version; the support period per substantially modified version (guidance paras 128, 131); Module H change notices; and the start of the Art 13(13) retention period? Can a change made only to a remote data processing solution, with no client release, be a substantial modification and so a new placing (guidance Example 55)?

**C. Art 32(2) certification-scheme limb.** Can a Class I product use Module A on the strength of a certificate at assurance level "substantial" under a scheme adopted under Regulation (EU) 2019/881 (EUCC) before a delegated act under Art 27(9) specifies that scheme? Please address Art 27(8), Art 27(9), Art 32(1)(d), Art 32(3)(c), recital 91, Annex VII point 5, and guidance footnote 25 and para 153. If Module A were available, would a certificate need to cover every applicable Annex I requirement, including Part II?

**D. Steward and manufacturer for the same code.** Where one legal person is steward of an unmonetised project (Art 3(14), Art 24) and manufacturer of products integrating it, does an actively exploited vulnerability in the project require one notification or two from 11 Dec 2027? Does it matter whether the steward and the manufacturer are the same legal person or different group companies? Which Member State's CSIRT is coordinator for a steward whose parent is outside the EU, and can the group choose by naming an Irish steward entity? Please also confirm that the steward regime is not available for a project from the date any version of it is monetised (guidance para 84) and comment on the risk that partner early access to security patches is treated as monetisation (guidance paras 57, 62).

**E. Operating systems supplied to device makers.** Confirm that an operating system integrated in our own phones does not make the phone an Annex III item 11 product (Art 7(1); guidance Example 58). When we supply OS code to other device makers, in which of the following cases are we placing an item 11 product on the market: (i) public, free HOSP source that OEMs build themselves; (ii) a separately licensed package of proprietary applications and services; (iii) compiled OS images supplied under contract; (iv) source licensed under a commercial agreement (guidance para 24, Example 7)? What contract and documentation terms keep case (i) and (ii) outside item 11?

**F. Support period for models on sale across 11 Dec 2027.** Does the minimum five-year support period in Art 13(8) run from the placing of each unit, or may a manufacturer set one end date for a model, so that units placed later get the remainder? Please address Art 13(8) first and third subparagraphs, Art 13(19), Art 69(2) and FAQ 4.5.3 and 7.2. Is a per-cohort end date (for example by quarter of placing) a compliant way to apply a per-unit rule, and how must it be shown "at the time of purchase"?

**G. FIDO security keys.** Is a FIDO hardware authenticator whose substance is a secure element designed to AVA_VAN.4 or higher a Class I item 1 product or an Annex IV item 3 product? Please address the descriptions in Implementing Regulation (EU) 2025/2392 (Annex I point 1 "hardware authentication devices"; Annex II point 3 "secure elements integrated into carrier materials taking other shapes"), Art 7(1), Art 8(1) and guidance para 152. Would the answer change for a key with a biometric sensor handled outside the secure element?

**H. Remote data processing for cloud clients.** Where an installed client (desktop sync client, CLI, SDK, mobile app) calls Aldermoor cloud services, which of those services are "remote data processing" under Art 3(2) and so part of the client as a product? Is the boundary the services the client interacts with directly (guidance para 205 and section 8.3.1), or the whole service (recital 11)? Are browser-only consoles outside the CRA unless a console function issues credentials an installed product needs (guidance paras 21, 194)? What follows for severe-incident reporting where one front-end serves several products?

## 4. Assumptions you may make

- Aldermoor Ireland Ltd is the EU main establishment and the decisions on product cybersecurity are predominantly taken there.
- The open-source projects are published under licences that meet Art 3(48) and are not monetised, save for the arrangements named in question D.
- Facts about specific products are as in the positions pack; we will confirm any fact your answer turns on.

## 5. Out of scope

Irish implementing measures and penalties (please flag if any draft exists); the Digital Omnibus proposal; NIS2 obligations of the cloud business; product liability under Directive (EU) 2024/2853, except where a CRA reading changes liability exposure.

## 6. Enclosures

1. Legal positions pack (`positions.md`) and the draft letter to the NCSC (`letter-to-ncsc.md`).
2. Claims register for the Enterprise papers (`claims_enterprise.csv`) and the base register (`claims.csv`), with exact quotations from the Official Journal text and the Commission guidance.
3. Source copies: Regulation (EU) 2024/2847 (OJ text and English corrigenda), Commission guidance C(2026) 5252 annex and Communication, Commission FAQ v1.4, ENISA SRP FAQ (15 Oct 2026), NCSC National CRA Guidelines (31 Aug 2026), Implementing Regulation (EU) 2025/2392.
4. Classification register (`classification.csv`) and the Article 14 volume model (`volume_model_output.csv`).

Please address all correspondence to the General Counsel, marked privileged.
