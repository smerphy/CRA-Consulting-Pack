# Google outside-in: Article 14 volume calibration

Outside-in analysis from public sources; not affiliated with or reviewed by Google. All figures below are estimates built from public disclosures as at 1 Nov 2026. Source IDs (S01-S63) refer to `sources.md`.

## 1. What is being estimated

Article 14 of Regulation (EU) 2024/2847 has applied since 11 Sep 2026. A manufacturer must notify each actively exploited vulnerability (AEV) "contained in" its product with digital elements, and each severe incident affecting product security, through ENISA's Single Reporting Platform (SRP) on a 24-hour, 72-hour and 14-day (AEV) or one-month (incident) clock (KB `reports/sections/09-reporting.md`). Exploitation must rest on "reliable evidence that a malicious actor has exploited it" (Art 3(42)); authorised research such as Pwn2Own is not malicious exploitation, and exploitation known before 11 Sep 2026 is not reported retroactively (guidance para 217, per KB 09).

The unit counted here is an SRP notification record (one record carries the early warning, the 72-hour notification and the final report). The SRP glossary asks for one "Product Name" per notification, described as "Name that identifies the affected product with digital elements" (S10). We therefore assume, as an inference, that one exploited vulnerability affecting several separately placed Google products produces one record per product. This "fan-out" is the main driver of volume and the main uncertainty.

## 2. Public calibration data, 2023 to 2026

### Exhibit A1: exploited vulnerabilities in Google products by public source

| Source | What it counts | 2023 | 2024 | 2025 | 2026 (to 1 Nov) |
|---|---|---|---|---|---|
| Chrome Releases "exploit ... exists in the wild" notes (S11) | Distinct CVEs Google flagged as exploited in Chrome stable updates | 8 (incl. CVE-2023-4762 flagged later) | 7 | 9 (incl. CVE-2025-24201 and CVE-2025-4664 "knowledge ... exists in the wild") | 7 |
| Press counts of Chrome zero-days (S39-S43) | Chrome zero-days "this year" | 8 | 10 (includes 3 demonstrated at Pwn2Own, S41) | 8 | 7 (BleepingComputer, 9 Sep 2026) |
| Android Security Bulletin "may be under limited, targeted exploitation" (S14) | Distinct CVEs flagged in monthly Android bulletins | 15 | 3 | 10 | 2 |
| Pixel Update Bulletin, same wording (S15) | Additional Pixel-only CVEs flagged | 1 extra (CVE-2023-21237; CVE-2023-4211 also in ASB) | 2 extra (CVE-2024-29745, CVE-2024-29748) | 0 | 1 (CVE-2026-58704, cellular modem) |
| CISA KEV, vendor Google or Android, by date added (S13, catalogue 2026.10.30) | Entries added that year | 9 | 15 | 10 | 10 |
| Project Zero "0day In the Wild" tracker, vendor Google, by patch date (S33) | Zero-days in Google products | 11 (8 Chrome, 3 Android) | 12 (7 Chrome, 5 Android) | 12 (6 Chrome, 6 Android) | 7 (all Chrome; Android 2026 entries not yet listed) |
| GTIG annual review, vendor count for Google (S34-S38) | Zero-days attributed to Google as vendor | 17 "Google products" incl. Android ecosystem devices (S37) | 11 (S35) | 11 (S38, reporting the 5 Mar 2026 review) | not yet published |

The sources disagree at the margin because they count different things: zero-days only (GTIG, Project Zero) versus any flagged exploitation (bulletins, KEV); Google-authored code versus third-party components shipped in Android (Arm Mali, Qualcomm, Linux kernel, FreeType); and calendar of patch versus calendar of catalogue entry.

### Exhibit A2: de-duplicated exploited vulnerabilities likely to touch a Google-manufactured product

Method: union of Chrome Releases ITW notes and Android/Pixel bulletin flags, minus Qualcomm-only CVEs (Pixel phones since Pixel 6 use Google Tensor, not Qualcomm silicon, so these are reportable by the OEMs that ship them, not by Google as Pixel manufacturer; inference), plus other Google entries in KEV (Brotli, CVE-2026-111497, added 27 Oct 2026).

| Year | Chromium-family AEVs | Android or Pixel AEVs affecting Pixel | Other Google components | Union (de-duplicated) |
|---|---|---|---|---|
| 2023 | 8 | 13 (2 overlap with Chrome: Skia, WebP) | 0 | 19 |
| 2024 | 7 | 4 | 0 | 11 |
| 2025 | 9 | 10 | 0 | 19 |
| 2026 (10 months) | 7 | 2 | 1 | 10 (about 12 annualised) |
| Planning base | 8 a year (7-10) | 7 a year (2-13) | 0.5 a year | about 15 a year (10-20) |

Two cautions. Third-party components count: an exploited Arm Mali GPU or Linux kernel flaw in a Pixel is an AEV "contained in" the Pixel, so Google as Pixel manufacturer reports it (KB 09 and Art 13(6) upstream duties). And public flags understate awareness: Google's threat intelligence also sees n-day exploitation (already-patched flaws exploited against unpatched devices, for example by forensic-extraction tools), which is reportable because the definition turns on exploitation, not on zero-day status.

## 3. Fan-out logic

### Exhibit A3: products likely touched by each class of exploited vulnerability

| Vulnerability class | Example (public) | Google products likely affected (separately placed) | Records per AEV: low / central / high |
|---|---|---|---|
| Chromium engine (V8, Blink, Skia, ANGLE, Dawn, WebRTC) | CVE-2026-3909 Skia: KEV says it "affects Google Chrome and ChromeOS, Android, Flutter" (S13) | Chrome (desktop and mobile), Android System WebView, ChromeOS; sometimes the Android platform via shared libraries (Skia, libwebp, libvpx) and therefore Pixel | 1 / 3 / 5 |
| Android framework, runtime or kernel | CVE-2025-48543 ART; CVE-2025-38352 kernel (S14) | Pixel phones (several generations in support), Pixel Tablet units on the market; from 11 Dec 2027 possibly AOSP as steward (Art 24(3)) | 1 / 1.5 / 4 |
| Pixel-specific firmware | CVE-2026-58704 modem; CVE-2024-29745 bootloader (S15) | Pixel phones only | 1 / 1 / 3 |
| Shared Google library | CVE-2026-111497 Brotli (S13) | Any Google product embedding the library (Chrome at least) | 1 / 1 / 3 |
| Smart home, wearables, Titan, Cloud installed software | None found in KEV 2023-2026 (S13) | The device or client concerned | 0 / 0.5 a year / 3 a year |

"Low" assumes one SRP record can list every affected Google product. "Central" assumes one record per separately placed product family. "High" assumes one record per product family and per Pixel generation or platform build with its own technical file.

## 4. Estimate

### Exhibit A4: estimated Article 14 notification records per year (estimate)

| Driver | Low | Central | High | Basis |
|---|---|---|---|---|
| Chromium-family AEVs × fan-out | 7 × 1 = 7 | 8 × 3 = 24 | 10 × 5 = 50 | Exhibits A2, A3 |
| Android and Pixel AEVs × fan-out | 4 × 1 = 4 | 7 × 1.5 = 10.5 | 13 × 4 = 52 | Exhibits A2, A3 |
| Other Google components | 0 | 0.5 | 2 | KEV 2026 Brotli entry |
| n-day exploitation newly evidenced (assumption) | 0 | 3 | 8 | Not publicly countable; assumption |
| Severe incidents under Art 14(3) (assumption) | 0 | 1 | 3 | No public calibration exists |
| **Total records a year** | **about 11** | **about 39 (round to 40)** | **about 115** | Estimate |
| Stage submissions (3 per record) | about 33 | about 120 | about 345 | 24 h, 72 h, final |

Reading the central case: about 40 notification records a year, or between three and four a month, each with a 24-hour first deadline. Exploitation clusters. Chrome flagged four exploited flaws between 9 and 23 May 2024 (CVE-2024-4671, -4761, -4947, -5274) and three between 12 and 31 March 2026 (CVE-2026-3910, -3909, -5281) (S11). A team sized for the average will miss the peaks.

From 11 Dec 2027 the volume may rise. If Google is the open-source steward of Chromium and AOSP with engineering involvement, Art 24(3) applies Art 14(1) to the steward for the same AEVs (KB `12-open-source.md`; `verification.md` claim 5). Whether one legal person must file twice, once as manufacturer and once as steward, is not addressed in any source found. Adding steward records for Chromium and AOSP framework AEVs would add roughly 8 to 12 records a year to the central case (estimate).

## 5. Routing

All records go to the coordinator CSIRT of the manufacturer's main establishment in the Union (Art 14(7)). Public evidence points to Ireland but does not prove it; see `paper.md` section 2. Google's EU declarations of conformity are issued by Google LLC, Mountain View (S04, S05); the EU Google Store is operated by Google Commerce Limited, Dublin (S03); Google Ireland Limited is the EEA service provider and data controller (S01, S02); Google reports more than 6,000 full-time employees in Ireland (S06) against more than 2,500 in Germany in 2021 (S07). A wrong CSIRT choice "may" invalidate a notification (ENISA SRP FAQ 18, per KB 09).

## 6. What would change the estimate

- ENISA or the Commission confirming that one notification may list several products (lowers the central case towards 15).
- Guidance that a steward and a manufacturer which are the same legal person file once (removes the post-2027 uplift).
- A lower evidential bar inside Google than the public "may be under limited, targeted exploitation" wording (raises volume), or a higher one (lowers it).
- Growth in exploited Pixel modem and firmware flaws as Chrome exploitation falls; GTIG reported browsers fell below 10% of 2025 zero-days while mobile zero-days rose from 9 to 15 (S34).
