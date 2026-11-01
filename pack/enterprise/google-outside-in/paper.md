*Outside-in analysis from public sources; not affiliated with or reviewed by Google. Estimates are labelled as estimates. Facts as at 1 Nov 2026.*

# Google outside-in: what the CRA means for Google, from public sources

**Executive answer.** On public evidence, 25 Google product families are likely to be products with digital elements made available in the EU. Fourteen of them (56%) are likely important Class I products: Chrome on desktop and mobile, Android System WebView, ChromeOS, Pixel Watch, Fitbit wearables, Nest cameras and doorbells, smart speakers, smart displays, Nest Wifi Pro, the Titan Security Key, Google Authenticator and the Windows credential provider. The other 11 are likely default products, including Pixel phones. None is firmly Class II or critical, but four are borderline upwards, and the Titan Security Key could be an Annex IV secure element. With no harmonised standard cited and no CRA notified body designated, 56% of families would need third-party assessment if placed after 11 Dec 2027 on today's facts. The figure rises to about 70% if the borderline cases go against Google. We estimate about 40 Article 14 notification records a year (range 11 to 115). Each record runs a 24-hour first clock. The volume is driven by about 8 exploited Chromium flaws and 7 exploited Android or Pixel flaws a year, fanned out across separately placed products. Google's EU service provider and EU store operator are Dublin companies, and Ireland has the largest Google EU workforce figure we found (more than 6,000), so Ireland's CSIRT is the likely coordinator. But the manufacturer named on EU declarations is Google LLC in Mountain View, and Google has published no CRA main-establishment designation. The top five implications are:

1. Fourteen families would need third-party assessment for units placed from 11 Dec 2027 unless standards are cited first, and no CRA notified body has yet been found designated.
2. Article 14 volume is a 24/7 operating problem, not a filing task.
3. Published support periods anchored to US launch dates would need review for units placed from 11 Dec 2027, when the CRA requires a declared end date per product.
4. Chromium and AOSP put Google in steward and manufacturer roles at once.
5. Google's build-provenance foundations are strong for servers and Pixel images but not yet visibly product-by-product evidence for the CRA.

## 1. Twenty-five Google families are likely in scope, and fourteen are important Class I products (E3)

We applied the knowledge-base classification rules (KB `06-classification.md`, `03-scope.md`) to every Google product line we could verify from public pages. Five rules did most of the work:

- one core functionality per product;
- integration does not reclassify the host (Art 7(1));
- a smartphone with an operating system is not an operating system (guidance Example 58);
- browser-only software is not a product (guidance para 21);
- separately supplied software is its own product.

EU availability was checked on the Irish, German and French Google Stores on 1 Nov 2026 (S20). The full register, with rationale, borderline flags and support periods, is in `portfolio.csv`.

### Exhibit 1: likely classification of the 25 headline families (estimate)

| Likely class | Families | Annex item | Notified body likely needed (units placed from 11 Dec 2027, on today's facts) |
|---|---|---|---|
| Important Class I, software (6) | Chrome desktop; Chrome mobile; Android System WebView; ChromeOS and ChromeOS Flex; Google Authenticator; Google Credential Provider for Windows | III-I.2 browsers; III-I.11 operating systems; III-I.1 identity and authentication | Yes (Module B+C or H) |
| Important Class I, hardware (8) | Pixel Watch; Fitbit wearables; Nest cameras; Nest doorbells; smart speakers; smart displays; Nest Wifi Pro; Titan Security Key | III-I.19 wearables; III-I.17 smart-home security; III-I.16 assistants; III-I.12 routers; III-I.1 authentication | Yes |
| Default (11) | Pixel phones; Pixel Buds; Nest Learning Thermostat; Google TV Streamer; Google Mobile Services bundle for OEMs; directory and password sync connectors; desktop clients; consumer and enterprise mobile apps; Cloud CLI and client libraries; Cloud on-premises software; Google Distributed Cloud appliances | None | No (4 conditional on borderline outcomes) |
| Class II or critical (0 firm) | Borderline: GDC software only for bare metal and GDC appliances (II.1 container runtime); Titan Security Key (Annex IV.3) | | |

Families excluded from the headline count are listed in `portfolio.csv`:

- products not listed on EU stores today: Pixel Tablet, Nest x Yale lock, Nest Protect, Fitbit Ace;
- integrated chips not sold separately: Titan M2 and M3, Tensor;
- AOSP as open source;
- OS builds for Wear OS and TV makers, where the supply model was not verified;
- browser-only Workspace and Cloud consoles, which are out of scope as products.

Units of the delisted products already on the EU market still fall under Article 14.

### The borderline cases are few but material

| Family | Question | Why it matters |
|---|---|---|
| Titan Security Key | Class I.1 authentication hardware, or Annex IV.3 "smartcards or similar devices, including secure elements"? The store page says it "uses a purpose-built secure element chip" (S20) | Annex IV is treated as Class II until an Art 8(1) act. The deciding fact is the designed AVA_VAN level of the key, which is not public |
| Android System WebView | Separate embedded-browser product or part of the OS image? | It is updated separately through Play, so it is likely a separate Class I.2 product |
| ChromeOS, and Wear OS or TV OS supplied to device makers | Is Google placing an operating system on the market as a component? | If so, each is Class I.11 with its own technical file. The device maker is manufacturer of the finished device |
| Google Mobile Services | Does Play Protect make Play services anti-malware (I.4)? | We read malware scanning as ancillary, so the bundle is default |
| GDC software only for bare metal; GDC appliances | Is the container runtime the core functionality (II.1)? | Class II would need a notified body or a "substantial" EUCC certificate once the Art 27(9) act exists |
| Directory and password sync | Identity management (I.1) or provisioning utility? | Moves a default product into Class I |

Integrated security silicon is a design strength, not a classification burden. Google says Titan M2 was certified to Common Criteria PP0084 at AVA_VAN.5 (S22). That is above the AVA_VAN.4 threshold that the Implementing Regulation (EU) 2025/2392 description uses for Annex IV.3 secure elements (KB `06-classification.md`). Because the chip is not sold separately, Pixel stays a default product. Google must still assess the chip as a component.

## 2. Ireland is the likely coordinator CSIRT, but the public record does not settle it

Article 14(7) sends every notification to the CSIRT of the Member State of the manufacturer's main establishment in the Union. That is where cybersecurity decisions on its products are "predominantly taken". If that cannot be determined, it is the establishment with the most employees in the Union (KB `09-reporting.md`).

### Exhibit 2: public facts on Google's EU establishment

| Fact | Source | Points to |
|---|---|---|
| EU declarations of conformity are issued by Google LLC, Mountain View, and signed there, including by a product-area cybersecurity compliance lead | S04, S05 | Decisions taken outside the EU |
| Google Ireland Limited, Dublin, provides Google services in the EEA and is the GDPR controller for EEA users | S01, S02 | Ireland |
| Google Commerce Limited, Dublin, operates the EU Google Store and so is likely the importer or distributor of Google hardware | S03 | Ireland |
| More than 6,000 full-time employees in Ireland | S06 | Ireland on the headcount fallback |
| More than 2,500 staff in Germany (2021, stale); Munich hosts Google's "global hub of privacy and security engineering" with 300+ engineers | S07, S08 | A possible argument for Germany on the "decisions" test, which we judge weak |
| No Google statement designating a CRA main establishment or coordinator CSIRT | Searches, 1 Nov 2026 | Unverified |

Our reading is that the "decisions predominantly taken" test cannot point to an EU Member State if those decisions sit in the United States. The headcount fallback then applies, and Ireland is the likely answer. If Google LLC were instead treated as having no EU main establishment, the third subparagraph of Art 14(7) would apply: an authorised representative first, if one exists, then the importer. Google Commerce Limited in Dublin would likely point to Ireland on that route too (inference). Two points remain unverified. First, which Member State Google has selected on the SRP. Second, whether establishments of subsidiaries count as the manufacturer's own establishments. A wrong choice "may" invalidate a notification (ENISA SRP FAQ 18, per KB 09).

## 3. Google should expect about 40 Article 14 records a year, with peaks of several a week (E2)

Public disclosures give a usable calibration (`art14_estimate.md`).

- Chrome Releases flagged 8, 7, 9 and 7 distinct CVEs as exploited in the wild in 2023, 2024, 2025 and 2026 to date (S11).
- Android and Pixel bulletins flagged 16, 5, 10 and 3 (S14, S15).
- CISA's catalogue added 9, 15, 10 and 10 Google or Android entries (S13).
- Google's threat intelligence group attributed 11 zero-days to Google in both 2024 and 2025 (S35, S38).

### Exhibit 3: estimated Article 14 volume (estimate)

| Driver | Low | Central | High |
|---|---|---|---|
| Exploited Chromium-family flaws a year | 7 | 8 | 10 |
| Records per Chromium flaw (Chrome, WebView, ChromeOS, sometimes Pixel) | 1 | 3 | 5 |
| Exploited Android or Pixel flaws affecting Pixel a year | 4 | 7 | 13 |
| Records per Android or Pixel flaw | 1 | 1.5 | 4 |
| n-day exploitation, other components, severe incidents (assumptions) | 0 | 4.5 | 13 |
| **Notification records a year** | **about 11** | **about 40** | **about 115** |
| Stage submissions (24 h, 72 h, final) | about 33 | about 120 | about 345 |

The fan-out assumption is the swing factor. The SRP form asks for a single "Product Name" per notification (S10), so we assume one record per separately placed product. Three further points move the estimate:

- **Third-party components count.** Exploited Arm Mali and Linux kernel flaws in Pixels made up a large share of 2023 and 2025 flags. They are reportable by Google as Pixel manufacturer.
- **Exploitation clusters.** Four Chrome flaws were flagged as exploited between 9 and 23 May 2024, and three in March 2026 (S11).
- **Steward filings may add volume.** From 11 Dec 2027 Art 24(3) may add steward filings for Chromium and AOSP, about 8 to 12 records a year (estimate). No source says whether one legal person acting as both manufacturer and steward files once or twice.

The operating consequence is a standing 24/7 decision cell. It must declare "awareness" against the guidance test of reasonable certainty (KB 09) and file to one coordinator CSIRT. It must also issue Art 14(8) user notices across consumer, enterprise and OEM channels.

## 4. Google's provenance and transparency work is a strong foundation for evidence-as-code, with visible gaps (E1)

Google has published more of the building blocks than most manufacturers.

### Exhibit 4: public foundations against CRA evidence needs

| Public foundation | What Google says | CRA evidence it can feed | Gap visible from outside |
|---|---|---|---|
| Binary Authorization for Borg (updated Sep 2026) | Every build produces signed provenance covering sources, dependencies, hashes and build parameters; deploy-time checks enforce policy (S44) | Annex I Part I secure development; Annex VII point 2 design and production evidence | Described for services on Borg. Public material does not say it covers Chrome, ChromeOS, Pixel or Nest client binaries |
| SLSA | Key BAB concepts were contributed to SLSA, introduced by Google teams in 2021 (S44, S45) | A recognised provenance format for per-version records | No public statement of the SLSA level of shipped consumer products |
| AOSP SBOM tooling | SBOMs "automatically generated for Android Continuous Integration builds", SPDX 2.3, NTIA minimum elements (S31) | Annex I Part II(1) SBOM | No public SBOM for Pixel, Chrome or Nest builds found. CRA SBOMs need not be public, so absence is not a gap in compliance |
| Pixel Binary Transparency | Public log of Pixel 6+ factory image metadata to detect tampered images (S47) | Secure update and integrity evidence (Annex I Part I) | Factory images only, not every over-the-air update or other device lines |
| Nest security validation results | Third-party validation result PDFs per device (S21) | Test reports for Annex VII point 6 | Not CRA-specific; method and coverage not checked here |
| Bulletins and release notes | Monthly Android and Pixel bulletins; Chrome Releases per update (S11, S14, S15) | Annex I Part II(4) public disclosure of fixed vulnerabilities | Formats are human-readable pages. CSAF or other machine-readable feeds were not checked |

The E1 design in this pack fits Google's starting point. Each release pipeline should emit a CRA evidence bundle per product version: provenance, SBOM, the vulnerability-handling record and the support-period end date. The bundle should be keyed to the product identifiers used in the declaration of conformity. The hardest part at Google's cadence is versioning. Chrome ships a new major version every four weeks and Pixel ships monthly. Under Commission guidance (not the Regulation's text), a substantially modified version is a new placing, while other versions keep the original placing date (paras 13-15, Example 2; KB `03-scope.md`). Every version still needs a record of which it is, and its documentation kept current, so declarations, CE marking and technical documentation must be generated by the pipeline, not assembled by hand.

## 5. Google is likely a steward for many projects and a manufacturer for the products built on them (E4)

Our role analysis is in `oss.md`. Google likely sustains several projects as an open-source steward: Chromium, AOSP, Go, Bazel, Flutter, TensorFlow, gVisor and Brotli. It is not the steward for foundation-hosted projects it founded or contributes to, such as Kubernetes (graduated in the CNCF in 2018), Istio and gRPC (S53-S55). For those, its duties are Art 13(5) due diligence as a downstream manufacturer.

Two projects need executive attention.

- **Chromium.** The same exploited V8 or Skia flaw is a manufacturer notification for Chrome, WebView and ChromeOS today. It may also be a steward notification for Chromium from 11 Dec 2027. The CISA catalogue entry for CVE-2026-3909 shows the reach: Chrome, ChromeOS, Android and Flutter (S13).
- **AOSP.** Google moved to publishing AOSP source twice a year from 2026 (S30). That strengthens Pixel's position as a Google product. It also invites the argument that AOSP is supplied in a commercial context rather than sustained as unmonetised open source. If that argument succeeded, Google would become a manufacturer of an operating system (Class I.11). Until a harmonised standard, common specification or substantial-level scheme can be applied in full (Art 32(2)), its only self-assessment route would be Art 32(5), which requires public technical documentation.

We found no public Google statement on the CRA. OpenSSF's 11 Sep 2026 guide expects "most of the open source software community" to fall under the steward framework (S60).

## 6. Existing UK and US work helps, but CRA support periods will force policy changes (E5)

Google already publishes UK PSTI statements of compliance for Pixel, Nest, Chromecast and Fitbit devices, naming Google LLC as manufacturer and stating minimum support periods (S17, S18). It also publishes per-device minimum security-update dates for its connected-home range (S21). On the US Cyber Trust Mark, Google was named among industry participants at the July 2023 launch (S48). The programme had not labelled any product by 28 Oct 2026, and its lead administrator changed in April 2026 (S49). We found no Google product with the mark.

### Exhibit 5: published support policies against the CRA floor

| Family | Published policy | Fit with the CRA for units placed from 11 Dec 2027 (KB `08-annex1-part2.md`) |
|---|---|---|
| Pixel phones | Seven years from first US availability (S16) | Above the five-year floor at launch. A unit placed in the EU late in the cycle gets less, and the end date must be shown at purchase (Art 13(19)). The Commission FAQ (4.5.3, 7.2) points to a per-unit reading: units placed later need their own support period under Art 13(8). Not settled by the Regulation's text; see legal-positions question F (module E6) |
| ChromeOS | Ten years from platform release (S12) | Above the floor |
| Nest and Google Home devices | At least five years from first US Google Store sale (S21) | Would need review. Published minimum dates have passed for several products still on EU stores: Nest Cam battery, floodlight and Doorbell battery (24 Aug 2026), Nest Hub 2nd gen (30 Mar 2026). The CRA support-period duty does not reach units placed before 11 Dec 2027; units placed after it would each need a declared end date |
| Pixel Watch | At least three years from first US availability (S18, Pixel Watch 3) | Would need review: three years is below the five-year floor unless a shorter expected use time is evidenced |
| Fitbit | At least two years after last sold (S19) | Would need review: may fall below the floor for units placed late in a model's sales life |
| Titan Security Key, Pixel Buds, Chrome, apps | No published period found | A declared period is needed per product |

For products placed after 11 Dec 2027, Google will need a declared, product-specific support period with an end date visible at purchase. On public evidence it has not yet published one for most families; none is required before that date. One control set can serve all three regimes: the EU CRA, UK PSTI, which already requires published support periods, and the Cyber Trust Mark. The CRA is the binding constraint, because its floor and reporting duties are the strictest.

## 7. What a CTO would do in the next 90 days

1. **Weeks 1-2: fix the routing.** Confirm and minute the Art 14(7) main establishment and coordinator CSIRT, likely Ireland. Register Primary and Secondary SRP representatives for every product line. Test the NCSC email fallback contact.
2. **Weeks 1-4: stand up one exploitation decision cell.** It covers Chrome, Android, Pixel, Nest, Fitbit and Cloud installed software. It needs 24/7 cover, written "reliable evidence" criteria, and a product fan-out table that maps each shared component (V8, Skia, kernel, Mali, Brotli) to every Google product that ships it.
3. **Weeks 2-6: freeze the classification register at SKU level.** Use `portfolio.csv` as a starting point. Resolve the six borderline cases with counsel and record the single core functionality per product (guidance para 144).
4. **Weeks 4-8: book third-party capacity.** Fourteen Class I families need Module B+C or H unless OJ-cited standards arrive in time. Prefer Module H for fast-release software lines (Chrome, ChromeOS, WebView). Engage notifying authorities on designation timelines.
5. **Weeks 4-10: rewrite support-period policy.** Move from "years from US launch" to a declared EU end date per product and per unit. Start with Pixel Watch and Fitbit, where the published periods are shortest.
6. **Weeks 6-12: extend provenance to client products.** Map BAB, SLSA and AOSP SBOM outputs onto the Annex VII bundle for one Class I product, such as Chrome, and one device, such as Nest Cam. Use the E1 pipeline pattern.
7. **Weeks 8-12: name the steward entities.** Name the legal-entity steward and publish an Art 24(1) policy for Chromium and AOSP first. Decide whether steward and manufacturer filings will be combined.

## Decisions for the executive team

1. **Main establishment and coordinator CSIRT.** Owner: General Counsel with the CISO. Timing: within 2 weeks. Decide and document the Art 14(7) answer and the evidence behind it.
2. **Single Article 14 operating model across product areas.** Owner: CISO. Timing: decision within 4 weeks, live within 90 days. Decide whether one cell owns awareness and filing for all Google products, with a fan-out rule per shared component.
3. **Conformity route per Class I family.** Owner: VP Engineering for each product area, with the Head of Product Compliance. Timing: within 8 weeks. Choose Module H or B+C per family, and decide whether to wait for harmonised standards or contract a notified body as soon as one is designated.
4. **Support-period policy.** Owner: hardware and software product leads, with General Counsel. Timing: within 10 weeks. Adopt a declared EU end date per product that meets the five-year floor unless shorter use is evidenced.
5. **Open-source roles.** Owner: Head of Open Source Programmes, with General Counsel. Timing: within 12 weeks. Confirm steward status per project, starting with Chromium and AOSP, and the filing approach where Google is both steward and manufacturer.

## Risks and open questions

- **Fan-out.** Whether one SRP notification may cover several products is not answered in any source opened. This changes the central estimate from about 15 to about 40 records a year.
- **Main establishment.** Google's actual Art 14(7) choice is not public. The test is not settled for a manufacturer whose security decisions sit outside the EU and whose EU presence is through subsidiaries.
- **Support-period baseline.** The Commission FAQ (4.5.3, 7.2) points to a per-unit reading: units placed later need their own support period under Art 13(8). Not settled by the Regulation's text; see legal-positions question F (module E6). Exhibit 5 findings for Pixel, Nest and Fitbit depend on it.
- **Evidence threshold.** Public "may be under limited, targeted exploitation" flags may sit below or above the Art 3(42) "reliable evidence" bar inside Google.
- **Classification borderlines.** The Titan key's AVA_VAN level, WebView's product boundary, the OS supply model to device makers, and the GDC core functionality all need non-public facts.
- **Supply models not verified.** GMS licensing, Wear OS and TV OS supply were inferred, not read from contracts or official pages.
- **Steward and manufacturer overlap.** There is no guidance on double filing, or on whether indirect monetisation of the Android ecosystem makes AOSP commercial.
- **Regulatory timing.** No CRA harmonised standard is cited and no CRA notified body was found as at the last check (KB 10; `verification.md` claim 23). Both could move before 11 Dec 2027.
- **Coverage limits.** This review did not open Google's vulnerability-disclosure pages, CSAF feeds, EU consultation filings or JC-STAR listings. Absence of a public statement is not evidence that Google lacks the capability.

## Sources

Full list with access dates and what each supports: `sources.md`. Knowledge base: `reports/sections/03-scope.md`, `06-classification.md`, `08-annex1-part2.md`, `09-reporting.md`, `10-conformity.md`, `12-open-source.md`, and `reports/verification.md`.

Key external sources (all accessed 1 Nov 2026):

- [Google Privacy Policy, EEA](https://policies.google.com/privacy?hl=en-GB&gl=IE)
- [Google Terms of Service, EEA](https://policies.google.com/terms?hl=en-GB&gl=IE)
- [Google Store Sales Terms, Ireland](https://store.google.com/intl/en_ie/about/device-terms/)
- [EU DoC, Pixel Watch 3](https://support.google.com/product-documentation/answer/15157855?hl=en)
- [Google in Ireland](https://blog.google/intl/en-ie/company-news/economic-impact-ireland/)
- [GSEC Munich](https://safety.google/safety/engineering-center/munich)
- [ENISA SRP glossary](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/cra-srp-glossary2)
- [Commission services CRA FAQ v1.4, 4 Sep 2026](https://ec.europa.eu/newsroom/dae/redirection/document/123307) (sections 4.5.3 and 7.2; local copy and hash in module E6 `source/guidance/MANIFEST.csv`)
- [NCSC Ireland CRA page](https://www.ncsc.gov.ie/cra/)
- [Chrome Releases](https://chromereleases.googleblog.com/)
- [Android Security Bulletins](https://source.android.com/docs/security/bulletin/)
- [Pixel Update Bulletins](https://source.android.com/docs/security/bulletin/pixel/)
- [CISA KEV catalogue](https://www.cisa.gov/sites/default/files/feeds/known_exploited_vulnerabilities.json)
- [Project Zero 0day "In the Wild"](https://projectzero.google/0day.html)
- [GTIG 2025 zero-day review](https://cloud.google.com/blog/topics/threat-intelligence/2025-zero-day-review/)
- [GTIG 2024 zero-day trends](https://cloud.google.com/blog/topics/threat-intelligence/2024-zero-day-trends/)
- [SecurityWeek on 2025 vendor counts](https://securityweek.com/google-half-of-2025s-90-exploited-zero-days-aimed-at-enterprises)
- [Pixel update policy](https://support.google.com/pixelphone/answer/4457705?hl=en-GB)
- [ChromeOS update policy](https://support.google.com/chrome/a/answer/6220366?hl=en)
- [UK PSTI Statement of Compliance](https://support.google.com/product-documentation/answer/14811823?hl=en)
- [UK PSTI, Pixel Watch 3](https://support.google.com/product-documentation/answer/14984076?hl=en)
- [Nest security update commitments](https://support.google.com/product-documentation/answer/10231940?hl=en-GB)
- [Fitbit legacy device policy](https://www.fitbit.com/global/uk/legal/legacy-device-policy)
- [Google Store Ireland](https://store.google.com/ie/category/connected_home)
- [Titan M2 certification (Google Italy blog)](https://blog.google/intl/it-it/prodotti/devices-services/google-pixel-7-e-pixel-7-pro-la-prossima-evoluzione-della-sicurezza-mobile/)
- [Binary Authorization for Borg](https://cloud.google.com/docs/security/binary-authorization-for-borg)
- [Introducing SLSA](https://security.googleblog.com/2021/06/introducing-slsa-end-to-end-framework.html)
- [AOSP SBOM](https://source.android.com/docs/setup/create/create-sbom?hl=en)
- [Pixel Binary Transparency](https://developers.google.com/android/binary_transparency/pixel_overview?hl=en)
- [AOSP twice-yearly releases](https://www.androidauthority.com/aosp-source-code-schedule-3630018/)
- [CNCF Kubernetes](https://www.cncf.io/projects/kubernetes/)
- [OpenSSF CRA guide](https://openssf.org/blog/2026/09/11/a-community-guide-to-the-eu-cra-september-11-deadline-for-manufacturers/)
- [Euronews on Cyber Trust Mark](https://www.euronews.com/2023/07/18/us-announces-a-cybersecurity-labeling-programme-for-smart-devices)
- [Nextgov on Cyber Trust Mark status](https://www.nextgov.com/cybersecurity/2026/10/fcc-commissioner-hopes-cyber-trust-mark-products-reach-shoppers-within-year/416878/)
