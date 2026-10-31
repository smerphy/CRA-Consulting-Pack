## 13. Worked example: a connected device with a mobile app and a vendor backend

A fictional smart thermostat, the Thermostat T200, shows the guide applied end to end. The product comprises device firmware, iOS and Android apps, and a vendor cloud for remote control and updates hosted on third-party IaaS. A third-party weather API feeds scheduling; the manufacturer, Example GmbH, is established in Germany and sells across the EU through retail and installers.

### Section 2: boundary, class and route

The product is the device, the two apps, and two cloud modules: the remote-control service and the update service. Both cloud modules pass the three-element test.

They process at a distance and a product function fails without them. Example GmbH built them to its own design on IaaS (guidance paras 184-196; thermostat example in section 8.3).

The IaaS hypervisor and the account database the app never talks to are outside the product and are recorded as dependencies (para 205).

The weather API is a licensed third-party service, so it fails element (iii). It is a component under Art 13(5), not RDPS, and the remote-function map records "weather API: scheduling input, provider X, fallback to last-known forecast". Telemetry sent for product analytics is not RDPS (para 192) and is off by default under item 2(g).

Intended purpose: residential heating control by consumers, with optional installer configuration, expected in use for 10 years. Core functionality is heating control. Nothing in [Implementing Regulation (EU) 2025/2392](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32025R2392) matches.

The Class I smart-home categories cover general-purpose virtual assistants and products with security functionalities such as locks, cameras and alarms (see Product classification). The T200 has a presence sensor for scheduling but no security function, so it is default class and the route is Module A. The record notes the review trigger: adding a door-sensor integration or a camera would re-run the test.

Variants: T200 with cellular backup and T200 Wi-Fi only share architecture and security design, so one family. The emitter inventory and the 2(i) and 2(j) rows differ.

The support period is 10 years to match expected use, declared per variant. Firmware releases are per-version placings and app releases follow the hardware units.

### Section 3: risk assessment highlights

Method: BSI TR-03183-1 structure with STRIDE on the data-flow diagram covering device, apps, remote-control service, update service, weather API and installer laptop. Assets: boiler-control function and setpoints (functional); account credentials, device keys, occupancy data (data); root of trust, update signing keys, audit log (security). Attacker profile: opportunistic remote attackers and a local attacker on the home network; no capable-adversary assumption, recorded with reasoning.

| Threat and asset | Item and control | Residual risk and treatment |
|---|---|---|
| Replayed or forged remote command turns heating off in winter (boiler-control function) | 2(f) and 2(d): device-bound signed commands with nonce; mutual TLS to the control service; local override always available | Low; residual on clock drift covered by signed time; Annex II point 5 states the local override |
| Occupancy data exposes when the home is empty (occupancy data) | 2(g) and 2(e): presence used only on-device for scheduling; cloud receives setpoints only; TLS 1.3; encrypted at rest with device-wrapped key | Low; justification for 2(g) applicability recorded with the data inventory |
| Compromised update signing key pushes malicious firmware (signing keys) | 2(f) and 2(c): offline root in HSM, online targets key in KMS, two-person release approval, anti-rollback counter | Low; key-rotation test UT-09; recovery image; residual accepted with monitoring of signing events |

All thirteen items apply except 2(m) transfer. It is marked not applicable because no exportable data exists beyond schedules, which the app can re-create. Annex II point 8(d) carries the erase procedure.

### Section 4: the items that bite hardest

Item 2(b): per-unit pairing codes printed under the faceplate, no default account, debug UART locked by fuse in production, Bluetooth pairing limited to onboarding. Item 2(c): automatic security updates on by default, in-app postpone of up to 7 days, a labelled opt-out; installers set maintenance windows.

Item 2(h): heating control continues on the local schedule when the cloud is unreachable, tested with a 72-hour outage.

Item 2(i): the device's only emitters are the control-service connection, the update check and NTP; retry back-off is tested. Item 2(l): authentication, pairing, update and integrity events are logged and exportable from the app, with an opt-out that keeps update and integrity events. The RDPS boundary rows follow draft EN 304 621 Annex R (draft): both ends authenticate, check integrity and freshness, and define behaviour on loss.

### Section 5: lifecycle

Design review on every firmware or service change; component intake for every dependency. SAST runs on every candidate, fuzzing covers the command parser and the weather-API response parser, and DAST covers the control-service API. The release gate records the SBOM hash, the KEV check, the secure-default export, the security-delta answers and the declaration decision.

Firmware 2.4.1, a security-only release fixing the command-replay flaw, answered all four guidance questions negatively and shipped under the existing declaration.

### Section 6 and 7: SBOM and update design

SBOMs: Yocto-generated CycloneDX 1.6 for the firmware image, cdxgen for each app bundle, Syft on each service container. Each is enriched to the TR-03183-2 fields, scored with sbomqs, attested with cosign and uploaded to Dependency-Track with an EUVD watch. Depth recurses to the first component outside the delivery scope; the weather API appears in the remote-function map, not the SBOM.

VEX is produced per release; no vulnerability data enters the SBOM.

Updates: TUF-style metadata with root, targets, snapshot and timestamp roles; A/B firmware slots with power-fail recovery; a monotonic version counter. First-boot update runs before onboarding completes, security and feature trains are separated by maintenance branches, and the advisory text travels with each update. The update repository is immutable storage budgeted for 10 years after the last release, with archive pages carrying the Art 13(11) warning.

### Section 8 and 10: CVD and reporting data

security.txt sits at the example.com well-known path with psirt@example.com, the anonymous form, the PGP key, the CVD policy URL and the CSAF provider metadata. A monitored phone line satisfies Art 13(17). Targets: acknowledgement in 5 working days, detailed response in 10, disclosure default 90 days.

Example GmbH's coordinating CSIRT is Germany's; two Assigned Representatives are registered on the SRP (see Reporting obligations (Article 14)).

The product data pack holds firmware and app versions, hardware revisions, configuration flags and the distribution map (14 Member States). It also holds end-of-support dates and the component list with VEX status.

For the replay flaw, telemetry showed probing but no successful exploitation. The incident commander recorded "no awareness of active exploitation" with reasoning and no Art 14 report was filed.

The fix shipped with a CSAF advisory carrying the CVE and EUVD IDs within the 90-day window.

### Section 11 and 12: documentation and declaration

The Annex VII file follows the thirteen-part outline, one file for the family with a variant list. The Annex II document sits at a versioned URL with the CE marking for the apps, the Annex VI text and the full declaration. The same page holds the support-period table (end of support November 2036 for first-batch units), the advisory index and the archive warnings.

The device carries the CE marking on the back plate and the end month and year on the packaging. The app shows the end-of-support notice when reached.

The Module A record is a signed internal-control report. It holds the evidence index, the gate record for firmware 2.4.0 and apps 3.1, and the applicability matrix sign-off.

The managing director signs the declaration. The record is retained with the file for 10 years after the last unit is placed or the support period, whichever is longer.

### Artefacts produced

- Product definition record with remote-function map and variant list
- Art 13 risk assessment RA-7 with data-flow diagram, threat list, applicability matrix and change log
- Control implementation notes and acceptance test records per Annex I item, including RDPS boundary tests
- Release gate records per firmware, app and service release with security-delta decisions
- Signed SBOMs, sbomqs scores, attestations and VEX documents per release
- Update design note with key hierarchy, metadata, recovery and the twelve acceptance tests
- CVD policy, security.txt, PSIRT procedure, case files and CSAF advisories
- Component due-diligence records, including the weather API and the TLS library
- Reporting data pack and distribution map; awareness decision records
- Annex VII technical file for the family; Annex II document at a versioned URL
- EU declaration of conformity and the Annex VI simplified text; CE marking placement record
- Module A internal-control record with the evidence index

Each artefact above maps to a line in the Requirement checklists tab, from checklist 1 scope gate to checklist 8 modules.
