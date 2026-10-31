## 4. Implementing Annex I Part I: design patterns and acceptance criteria

Each Annex I Part I item below gets a pattern to build, criteria to test and an artefact for the technical file. The legal text, mapping tables and standards state are in Annex I Part I: essential requirements for product properties. Items apply only as the section 3 risk assessment says they do.

Sources are the [ENISA Secure by Design and Default Playbook v1.0](https://www.enisa.europa.eu/sites/default/files/2026-07/ENISA_Secure_By_Design_and_Default_Playbook_v1.pdf) principles 4.1 to 4.22 with their "minimum evidence". Draft [ETSI EN 304 621](https://labs.etsi.org/rep/stan4cra/en-304-621/-/raw/main/EN-304-621.md) v1.0.4 clauses 5.3 to 5.15 are the second source.

They are joined by draft [ETSI EN 304 626](https://labs.etsi.org/rep/stan4cra/en-304-626/-/raw/main/EN-304-626.md) mitigations, EN 18031-1 mechanism families and IEC 62443-4-2 component requirements. The ETSI texts are drafts under public enquiry with no presumption of conformity; EN 18031 is cited under RED only.

Where software and connected devices differ, both are given.

### 2(a) No known exploitable vulnerabilities

Build a release gate that correlates the release SBOM with the EUVD, NVD and the CISA KEV catalogue and blocks on unresolved exploitable findings. Software products add an update-at-first-use check so vulnerabilities disclosed between placing and installation are closed on first launch (draft EN 304 626 MI-KEVD/MI-KEVA). Devices held in stock need the same behaviour on first boot (draft EN 304 621 Annex G.5.3).

- [ ] Every component in the release SBOM has been matched against EUVD, NVD and KEV within 24 hours of the gate
- [ ] Each open finding has a VEX status with justification or a documented public mitigation
- [ ] All available upstream patches are applied or the exception is recorded with severity, exploitability and impact (guidance paras 235-237)
- [ ] First-use update test passes on a unit built from the release image

Evidence: scan reports, VEX file, gate record with SBOM hash, first-use update test log (Annex VII point 6).

### 2(b) Secure by default and reset to original state

Ship with no shared credentials, optional services off, approved cryptography only and debug interfaces protected or disabled. Add an onboarding flow that cannot be skipped (Playbook 4.15, 4.16, 4.19; draft EN 304 621 SBD_TECH-1 to -3). Software products enforce this through the installer and first-run wizard.

Devices add per-unit secrets provisioned at manufacture and a hardware or recovery-mode reset to the secure baseline. The reset must wipe user data, settings and credentials, and it survives the tailor-made carve-out (draft EN 304 621 note to SBD_TECH-3).

- [ ] Fresh-install configuration export contains no default account and no listening optional service
- [ ] First-run flow forces credential set-up and, for privileged roles, a second factor
- [ ] Reset test: write data to every store, reset, read back nothing; cloud bindings revoked
- [ ] Any legacy or interoperability protocol is off by default with a user notice and upgrade path (guidance Example 10)

Evidence: default-configuration baseline, interface inventory with default state, provisioning record, reset test record, EN 18031-1 GEC and AUM decision records where RED applies.

### 2(c) Security updates, automatic where applicable

Build the client side here and the mechanism in section 7. Consumer products install security updates automatically by default, with notification, postponement and a clear opt-out. Managed estates offer scheduling in place of unattended installation (recital 56; draft EN 304 621 SU_UPDATES-7 to -14).

Software products keep OS and application update paths independent. Devices separate firmware from application updates so a security fix never requires a feature image.

- [ ] Default configuration shows automatic security updates enabled, or the recital 56 carve-out is justified in the risk assessment
- [ ] Opt-out and postpone are reachable in at most two steps and are documented in Annex II point 8(e)
- [ ] Security-only release installs without the preceding feature release
- [ ] User sees a notification for each available update with the advisory text

Evidence: Playbook 4.20 minimum evidence (default configuration, release notes showing separable fixes, update tests, user-notification proof).

### 2(d) Access control and unauthorised-access reporting

Authenticate every interface, including device-to-cloud and management paths. Add role-based authorisation, lockout, session limits and expiring machine credentials (Playbook 4.3, 4.16; EN 18031-1 ACM-1/2, AUM-1 to -6; IEC 62443-4-2 FR1). The reporting half is often missed: the product must surface possible unauthorised access, which draft EN 40000-1-4 slides place in a new control GEC-13.

- [ ] No unauthenticated interface in any product state, confirmed by port and endpoint scans
- [ ] Negative tests show denied access for wrong role, expired session and revoked token
- [ ] Ten failed logins trigger lockout or back-off and an audit event
- [ ] Repeated failures or privilege changes raise a visible alert or report

Evidence: access model, IAM inventory, negative-test results, alert catalogue, audit-log samples.

### 2(e) Confidentiality

Use TLS 1.3 or equivalent with server authentication, mutual authentication for machine links and no plaintext fallback. Encrypt data at rest with keys held in a secure element, TEE or key-management service (Playbook 4.17, 4.18; EN 18031-1 SCM, SSM, CCK, CRY-1). Choose algorithms from a published catalogue such as the one draft EN 304 621 Annex K references, and record crypto agility.

Devices without a secure element document the compensating key protection.

- [ ] Cryptographic inventory lists every algorithm, mode, key size and library against the chosen catalogue
- [ ] Downgrade and plaintext-fallback tests fail closed
- [ ] Keys are never in firmware images or logs, confirmed by binary scan
- [ ] Data classification table maps each data type to its at-rest and in-transit protection

Evidence: crypto inventory, protocol configuration, negative tests, key-management design.

### 2(f) Integrity and corruption reporting

Implement verified boot with a hardware or firmware root of trust, signed firmware and software, signed configuration and authenticated commands. Add integrity monitoring that reports corruption (Playbook 4.11, 4.14; IEC 62443-4-2 CR 3.1, 3.4, EDR 3.11 to 3.14). Software products sign packages and configuration bundles and verify at load; devices add anti-tamper and a signed configuration store.

The "report on corruptions" clause needs a user-visible or logged event, not silent repair.

- [ ] Modified image, configuration or command is rejected and an integrity event is logged
- [ ] Boot chain verifies every stage; a tampered stage halts into recovery
- [ ] Key rotation and trust-anchor update are tested without bricking the unit
- [ ] Corruption of stored data is detected and reported to the user or administrator

Evidence: boot-chain description and tests, signature-verification tests, corruption-detection test, tamper evidence.

### 2(g) Data minimisation and telemetry defaults

Inventory every data item per function and collect only what the function needs. Keep telemetry and analytics off by default with explicit opt-in (Playbook 4.2; draft EN 304 621 DM_RETENTION; draft EN 40000-1-4 DTM-1 to -3). Define retention per data type and strip personal data and secrets from logs.

Where the risk assessment marks 2(g) not applicable because no personal data is processed, the data inventory is the justification.

- [ ] Data inventory for the default configuration lists source, purpose, retention and legal basis where GDPR applies
- [ ] Telemetry is disabled in the default configuration export
- [ ] Log scan finds no personal data or secrets
- [ ] Retention is enforced by code or configuration, not policy alone

Evidence: data inventory, retention schedule, default-configuration export, DPIA cross-reference.

### 2(h) Availability and DoS resilience

List essential and basic functions, then protect each with rate limiting, resource quotas, early rejection of bad input, watchdogs and graceful degradation. The references are Playbook 4.5 and 4.12, IEC 62443-4-2 CR 7.1 to 7.4 and EN 18031-1 RLM-1. Devices must keep local control working when the backend is unavailable; backends need failover and tested restore.

Draft EN 304 621 AP_HA and the draft EN 40000-1-4 RLM-2 to -6 objectives add recovery, prioritisation and backup.

- [ ] Essential-function list exists with a mitigation per function
- [ ] Load test at the documented ceiling keeps essential functions responsive
- [ ] Backend outage test: device keeps local operation and recovers automatically
- [ ] Restore from backup meets the documented recovery objective

Evidence: essential-function list, stress and recovery test reports, availability-event logs.

### 2(i) Limiting impact on other networks

Document every network emitter and bound outbound traffic with rate limits and retry back-off. Prevent the product being used as an amplifier or relay (Playbook 4.15; EN 18031-1 TCM-1, NMM-1; IEC 62443-4-2 CR 5.1, 5.2). The JRC-ENISA mapping calls standards coverage "minimal" here, so test it yourself.

Management interfaces accept connections only from known sources where the deployment allows.

- [ ] Emitter inventory lists each outbound destination, protocol, frequency and worst-case volume
- [ ] Amplification factor of every UDP or broadcast service is calculated and below one, or the service is authenticated
- [ ] Retry storms are bounded by exponential back-off with jitter in a backend-outage test
- [ ] External port scan from a separate network segment shows only documented listeners

Evidence: emitter inventory, scan results, amplification calculations, segmentation guidance for Annex II.

### 2(j) Attack-surface reduction

Enumerate services, ports, protocols and physical interfaces per product state and justify each one (Playbook 4.4; draft EN 304 621 MAS_TECH; EN 18031-1 GEC). Devices disable or lock JTAG, SWD, UART and test pads in production, with fuse or lock-state evidence. The references are draft EN 304 626 MI-PDDI-1 to -4 and IEC 62443-4-2 EDR 2.13.

Software products strip development tooling, debug endpoints and sample configurations from release builds.

- [ ] Interface inventory per state (boot, idle, in use, recovery) with a reason for each exposed interface
- [ ] Production unit shows debug ports locked, verified by attempting a debugger attach
- [ ] Release build contains no debug endpoint, test account or development dependency
- [ ] Default-deny network policy confirmed by scan

Evidence: interface inventory, debug-lock evidence, port scans, hardware photographs (Annex VII point 1).

### 2(k) Exploitation mitigation

Prefer memory-safe languages for new code. Where C or C++ remains, build with stack protection, ASLR, W^X, control-flow integrity and fortified libraries, and verify the flags on the shipped binary. The references are Playbook 4.5 and 4.9 and draft EN 304 626 TR-SSDD, TR-MSAF and TR-LMII.

Sandbox parsers and network-facing services, separate privileges and zero secrets after use. Devices with a TEE or TrustZone isolate key handling there.

- [ ] Binary hardening scan of the shipped artefact shows every mandated flag present
- [ ] Fuzzing of each external parser runs in CI with memory-error detection and no open crashes at release
- [ ] Network-facing processes run unprivileged in a sandbox or container with a deny-by-default policy
- [ ] Penetration test confirms a compromised service cannot reach keys or the update path

Evidence: compiler-flag and hardening-scan output, fuzzing reports, privilege model, penetration-test report.

### 2(l) Logging with user opt-out

Log authentication outcomes, privilege and configuration changes, update events and integrity events. Use structured fields with timestamp, actor, action, object and result (Playbook 4.10; IEC 62443-4-2 CR 2.8 to 2.12; draft EN 304 621 MON_LOG). Protect logs from tampering, export them to the user's SIEM, and give the user an opt-out.

Where the opt-out would disable security-essential events, document which events persist and why in the risk assessment and Annex II.

- [ ] Event catalogue exists and every listed event appears in a sample log
- [ ] Logs are tamper-evident and rotated to the documented retention
- [ ] Opt-out control is reachable by the user and its effect is documented
- [ ] No personal data or secrets in log output

Evidence: event catalogue, annotated samples, retention configuration, SIEM forwarding test, opt-out evidence.

### 2(m) Secure erase and transfer

Provide a factory reset or account deletion that permanently removes all user data and settings, by overwrite or by destroying the encryption key. Cover local storage, credentials and cloud bindings (Playbook 4.7, 4.22; EN 303 645 5.11; IEC 62443-4-2 CR 4.2). Ownership transfer must revoke the previous owner's access.

Where data can be exported, the export runs over an authenticated, protected channel. Draft EN 304 621 does not require transfer support.

- [ ] Write-erase-read test per data type on device, in the app and in the cloud account
- [ ] Previous owner cannot reach the unit or its data after transfer
- [ ] Export requires authentication and is encrypted in transit
- [ ] Decommissioning steps are written into Annex II point 8(d)

Evidence: erase test records, crypto-erase design note, transfer test, Annex II text.

### The remote-data-processing boundary

Annex I applies to the product as a whole, including its RDPS modules. Draft EN 304 621 Annex R (draft) adds boundary requirements on both endpoints.

The local side verifies origin, integrity and freshness of what arrives and behaves safely on unavailability. The RDPS side does the same for what the device sends.

The hosting infrastructure stays outside the product and is a supply-chain dependency under Art 13(5). Assurance such as ISO/IEC 27001 or NIS2 evidence is reusable for it (guidance para 207).

- [ ] Each remote function in the section 2 map has an authentication, integrity, confidentiality and availability control on both ends
- [ ] Device behaviour on backend loss is defined and tested per function
- [ ] RDPS modules appear in the SBOM, the risk assessment and the test reports
- [ ] The product connects only to documented remote services

Evidence: remote-function map, boundary test results, RDPS deployment and configuration records.

### The integrator pattern for components and MCUs

A separately sold chip or module is a product in its own right. Items 2(b), 2(l) and 2(m) cannot be fully met at silicon level.

Vendor papers from [TI](https://www.ti.com/lit/pdf/STDA050) and [Microchip](https://www.microchip.com/content/dam/mchp/documents/MCU32/ProductDocuments/SupportingCollateral/An-Embedded-Engineers-Guide-to-the-EU-Cyber-Resilience-Act-DS00006536.pdf) (vendor material) describe a split. Draft EN 304 621 Annex K and EN 304 626 MI-PDDI-1 formalise the same split.

The component vendor documents root of trust, debug-lock states, key provisioning and integration assumptions in Annex II point 8(f). The integrator owns product-level defaults, reset, logging, the risk assessment and the technical file.

As an integrator, treat each vendor's integration assumptions as requirements and test them on your board. Record the vendor documentation reviewed in the due-diligence record (section 9).

Each item's evidence artefact is the entry for checklist 2, Annex I Part I, in the Requirement checklists tab.
