# Annex VII index: requests 2.32.4

Record `urn:aldermoor-pilot:cra-evidence:requests:2.32.4`. Version first offered 2025-06-09; not a new placing, so it keeps placing date 2024-05-21 from version 2.32.2 (guidance para 15, Example 2). Retain until 2034-05-21. Substantial-modification decision: not_substantial.

| Annex VII point | Evidence | SHA-256 (first 16) | Location |
|---|---|---|---|
| 1 General description: intended purpose, versions affecting compliance, Annex II information | Shipped artefact ; Product requests version 2.32.4; previous 2.32.3 | `d88cda03bd7a8108` | s3://cra-pilot-evidence/v1/requests/2.32.4/artefact/requests-2.32.4-py3-none-any.whl |
| 1 | Annex II user information | `5b373d54a4773155` | s3://cra-pilot-evidence/v1/requests/2.32.4/docs/annex-ii-user-information.md |
| 2(a) Design and development; system architecture | Maintained outside the pipeline in the product technical file; linked by product id | | |
| 2(b) Vulnerability handling: SBOM, CVD policy, reporting contact, secure update distribution | SBOM (CycloneDX 1.6) | `2a01b5db17065bcd` | s3://cra-pilot-evidence/v1/requests/2.32.4/evidence/sbom.cdx.json |
| 2(b) | VEX (OpenVEX) | `6bb58c327d558ebc` | s3://cra-pilot-evidence/v1/requests/2.32.4/evidence/vex.openvex.json |
| 2(b) | Signed VEX attestation (verified key by pilot-psirt-vex) | `7ef46fc8fa43d08f` | s3://cra-pilot-evidence/v1/requests/2.32.4/evidence/vex.openvex.sigstore.json |
| 2(b) | CVD policy | `6fefeb586c89150b` | s3://cra-pilot-evidence/v1/requests/2.32.4/docs/cvd-policy.md |
| 2(b) | Update design note | `48d8d713f9bd8bac` | s3://cra-pilot-evidence/v1/requests/2.32.4/docs/update-design-note.md |
| 2(c) Production and monitoring processes with validation evidence | Build provenance (https://slsa.dev/provenance/v1; builder https://aldermoor.example/builders/cra-pilot-local/v1; verified key by pilot-builder-provenance ; SLSA Build L1) ; Release gate decision: FAIL under cra-pilot-gate/1.0.0 | `e4808dd7c69bec8a` | s3://cra-pilot-evidence/v1/requests/2.32.4/evidence/provenance.sigstore.json |
| 3 Cybersecurity risk assessment and Annex I Part I applicability | Risk assessment | `ca5a29bf812bbaeb` | s3://cra-pilot-evidence/v1/requests/2.32.4/docs/risk-assessment.md |
| 3 | Applicability matrix (not applied: 2l, 2m) | `e885c3dad355630d` | s3://cra-pilot-evidence/v1/requests/2.32.4/docs/applicability-matrix.json |
| 4 Support period | End 2030-06-09 (5.00 years); justification: Authored: each version supported for 5 years from its release date; users receive fixes by moving to the latest version (Art 13(10)).; latest-version rule (Art 13(10)): yes | | |
| 5 Harmonised standards, common specifications, certification schemes | Route module_a; applied in full: none; certificate n/a | | |
| 6 Test reports against Annex I Parts I and II | sast (Bandit; error=3, note=6, suppressed=0, warning=0) | `ab3cc23c7c4f2e75` | s3://cra-pilot-evidence/v1/requests/2.32.4/evidence/sast.sarif |
| 7 EU declaration of conformity | Declaration PILOT-DoC-requests-2.32.2 (reused, from 2.32.2) at https://aldermoor.example/cra-pilot/doc/requests/2.32.2 | | |
| 8 SBOM for market surveillance authority on reasoned request | SBOM | `2a01b5db17065bcd` | s3://cra-pilot-evidence/v1/requests/2.32.4/evidence/sbom.cdx.json |
