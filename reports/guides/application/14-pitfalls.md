## 14. Application-level pitfalls

These are the product-level mistakes that recur in early-adopter reports and vendor teardowns, each with the countermeasure this guide prescribes. The programme-level pitfalls are in Engineering compliance programme. Sources are the [Commission FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307), guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456), [BSI TR-03183-2](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-2_v2_1_0.pdf?__blob=publicationFile&v=6) and vendor material from [Finite State](https://finitestate.io/blog/cra-compliance-mistakes) and [OmniTrust](https://omnitrust.com/blog/eu-cra-tales-from-the-trenches-3-why-security-maturity-is-not-enough-for-cra-readiness/).

- SBOM generated from the manifest misses vendored and statically linked code. Generate from the shipped artefact at build and add binary scanning (section 6).
- Vulnerability data embedded in the SBOM goes stale and breaks the BSI profile. Keep status in VEX and CSAF beside a static SBOM (sections 6 and 8).
- CVE counts or scanner hits treated as risk or as active exploitation. Apply reachability, record VEX justifications and reserve Art 14 for reliable exploitation evidence (sections 3, 8, 10).
- Default credentials or shared secrets shipped for convenience. Provision per-unit secrets, force credential set-up at first use and test the fresh-install export (section 4, item 2(b)).
- Debug ports left enabled in production units. Lock JTAG, SWD and UART by fuse or configuration and verify by attempting a debugger attach (section 4, item 2(j)).
- Telemetry on by default and justified as product improvement. Inventory every data item, default telemetry off with opt-in and record the 2(g) justification (section 4).
- Logging without a user opt-out, or an opt-out that silently disables security events. Provide the control, document which events persist and why, and say so in Annex II (section 4, item 2(l)).
- Updates verified by signature but without anti-rollback, so an attacker reinstalls a vulnerable version. Add a monotonic counter and an audited downgrade path (section 7).
- Security fixes bundled into feature releases because one train is easier. Run maintenance branches with a security-only channel and record any exception per FAQ section 4.3 (sections 5, 7).
- No per-version support declaration for software, so nobody knows which versions receive fixes. Keep a version-support register with end month and year and the Art 13(10) upgrade path (sections 7, 11).
- Evidence not linked to releases and assembled by hand when asked. Emit gate records, SBOM hashes, test results and attestations in CI and index them per requirement (sections 5, 12).
- The manufacturer-built backend left out of the risk assessment because "it is cloud". Apply the three-element test, map every remote function and assess both ends of each RDPS boundary (sections 2, 4).
- A weather-API-style third-party service treated as RDPS and assessed as the manufacturer's own. It fails element (iii) and belongs under Art 13(5) due diligence with product-level mitigations (sections 2, 9).
