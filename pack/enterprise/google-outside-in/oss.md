# Google outside-in: open-source projects and likely CRA roles

Outside-in analysis from public sources; not affiliated with or reviewed by Google. Roles below are likely readings of public facts against the knowledge base (KB `reports/sections/12-open-source.md`, Commission guidance C(2026) 5252 section 3 as summarised there). They are not legal conclusions. Source IDs refer to `sources.md`.

## The rules applied

- Unmonetised FOSS is not placed on the market; a legal person that systematically sustains FOSS intended for commercial use is an open-source software steward (Art 3(14), Art 24). Steward duties apply from 11 Dec 2027.
- Status is assessed per project. "Company publishes unmonetised FOSS it also integrates into its own products" makes the company steward for the FOSS and manufacturer for its products (guidance pts 67-68, Examples 25 and 29, per KB 12).
- Charging for binaries, updates or a supported version makes the publisher a manufacturer (pts 51, 57). Paid hosting of FOSS as a service is "not addressed in the guidance" (KB 12).
- A foundation that sustains the project is the steward; companies that contribute are neither steward nor manufacturer for their contributions (Recital 18; pts 48-49, 76-78).
- A steward with engineering involvement (employed developers, releases, patches) must notify actively exploited vulnerabilities under Art 24(3), which applies Art 14(1) (`verification.md` claim 5).
- A Google product that ships the project still carries full manufacturer duties, including Art 13(5) due diligence and Art 13(6) upstream reporting.

## Exhibit O1: Google-led and Google-originated projects

| Project | Governance on public evidence | Google products that ship it | Likely CRA role for Google | Confidence | Source |
|---|---|---|---|---|---|
| Chromium (incl. V8, Blink, Skia, ANGLE, Dawn) | Google-run project site; Chromium security team describes its aim as protecting "Chrome and Chrome OS users" | Chrome, Android System WebView, ChromeOS, Android (Skia) | Steward for Chromium; manufacturer for Chrome, WebView and ChromeOS | Medium. Chromium is distributed free, but the line between Chromium and Chrome is a build and branding line, not a governance one | S50, S51, S13 |
| Android Open Source Project | Google develops AOSP; from 2026 Google publishes source to AOSP twice a year (Q2 and Q4) | Pixel; GMS-licensed OEM devices | Steward for AOSP (likely); manufacturer for Pixel and any OS builds it supplies commercially | Medium-low. Indirect monetisation through the Android ecosystem and GMS licensing invites the argument that AOSP is supplied in a commercial activity | S30, S31 |
| Go (language and toolchain) | go.dev: "An open-source programming language supported by Google" | Toolchain used across Google; Go binaries distributed free | Steward (likely) | Medium-high | S52 |
| Kubernetes | CNCF project; accepted 10 Mar 2016, graduated 6 Mar 2018 | GKE (service); GDC software only for bare metal (installed) | Neither steward nor manufacturer for Kubernetes itself (the Linux Foundation/CNCF is the likely steward); manufacturer for its installed Kubernetes distributions | High for the project role | S53, S27 |
| Istio | CNCF project; accepted 30 Sep 2022, graduated 12 Jul 2023 | Managed service mesh offerings | Neither (CNCF likely steward) | High | S54 |
| gRPC | CNCF project; accepted 16 Feb 2017 (incubating) | Cloud client libraries and services | Neither (CNCF likely steward) | High | S55 |
| TensorFlow | Google-operated project site; models "built by Google and the community" | Google ML products | Steward (likely); manufacturer for any paid supported distribution | Medium. Governance document on GitHub could not be retrieved | S58 |
| Flutter | "Developed by engineers at Google along with hundreds of open source contributors"; BSD 3-Clause | Google apps built with Flutter | Steward (likely) | Medium-high | S57 |
| Bazel | "The Bazel project is led and managed by Google" | Internal build systems (Blaze lineage) | Steward (likely) | High | S56 |
| gVisor | Open-source container sandbox ("runs anywhere existing container tooling does") | Google Cloud sandboxed runtimes | Steward for gVisor; note it would be Annex III Class II.1 (container runtime) if ever placed on the market, with the Art 32(5) public-documentation route available | Medium | S59 |
| Brotli | Google GitHub organisation; exploited flaw CVE-2026-111497 added to CISA KEV on 27 Oct 2026 | Chrome and other Google products | Steward (likely) | Medium. GitHub release page could not be opened (HTTP 403) | S13 |
| SLSA, OSV, OSS-Fuzz | SLSA originated in Google's Binary Authorization for Borg work and is now an open specification | Supply-chain tooling | Steward or neither depending on current host foundation (not verified here) | Low | S44, S45 |

## What this means for Google

1. Google is likely to be a steward for a long tail of projects. Each needs a documented and verifiable cybersecurity policy under Art 24(1) from 11 Dec 2027, set per project, and a named legal-entity steward (the OpenSSF Stewards Playbook checklist starts with "My Legal Entity Steward is:", S61).
2. Chromium and AOSP are the two projects where steward and manufacturer roles overlap most. The same exploited V8 flaw is a manufacturer AEV for Chrome now and may also be a steward AEV for Chromium from 11 Dec 2027. No source found says whether one legal person files once or twice.
3. Google's own reliance on foundation-hosted projects (Kubernetes, gRPC, Istio) creates Art 13(5) due-diligence duties for its installed products, not steward duties.
4. The 2026 move to twice-yearly AOSP source drops (S30) widens the gap between what OEMs and downstream manufacturers can see and what Google ships on Pixel. For downstream manufacturers relying on AOSP, that affects their Art 13(5) evidence.
5. Monetisation decisions change roles. A paid long-term-support Go, TensorFlow or Flutter distribution would make Google the manufacturer of that edition from the date of monetisation (guidance pts 83-84, per KB 12).

## Public statements on the CRA

- Google: no public Google statement specific to the CRA was found in searches of Google's open-source and security blogs and Google Cloud pages (searches run 1 Nov 2026). This is an absence of evidence, not evidence of absence. Public filings to EU consultations were not searched.
- OpenSSF (Google's membership and tier were not verified; the members page did not render server-side): the 11 Sep 2026 community guide says steward requirements "do not take effect until December 11, 2027, but the requirements for Manufacturers take effect today, on September 11, 2026", and that "most of the open source software community will qualify under the CRA's Steward framework" (S60). The Stewards Playbook gives the per-project steward checklist (S61).
