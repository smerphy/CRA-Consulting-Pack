# Annex VII index: requests 2.31.0

Record `urn:aldermoor-pilot:cra-evidence:requests:2.31.0`. Placed 2023-05-22 (first_placing). Retain until 2033-05-22. Substantial-modification decision: first_placing.

| Annex VII point | Evidence | SHA-256 (first 16) | Location |
|---|---|---|---|
| 1 General description: intended purpose, versions affecting compliance, Annex II information | Shipped artefact ; Product requests version 2.31.0; previous None | `886d67a1035069de` | s3://cra-pilot-evidence/v1/requests/2.31.0/artefact/requests-2.31.0-py3-none-any.whl |
| 1 | Annex II user information | `b9d5396c4045b2bf` | s3://cra-pilot-evidence/v1/requests/2.31.0/docs/annex-ii-user-information.md |
| 2(a) Design and development; system architecture | Maintained outside the pipeline in the product technical file; linked by product id | | |
| 2(b) Vulnerability handling: SBOM, CVD policy, reporting contact, secure update distribution | SBOM (CycloneDX 1.6) | `5ff426b29e549fbf` | s3://cra-pilot-evidence/v1/requests/2.31.0/evidence/sbom.cdx.json |
| 2(b) | VEX (OpenVEX) | `e33439dd708e75ef` | s3://cra-pilot-evidence/v1/requests/2.31.0/evidence/vex.openvex.json |
| 2(b) | Signed VEX attestation (verified key by pilot-psirt-vex) | `434f2d033fee9d2a` | s3://cra-pilot-evidence/v1/requests/2.31.0/evidence/vex.openvex.sigstore.json |
| 2(b) | CVD policy | `6fefeb586c89150b` | s3://cra-pilot-evidence/v1/requests/2.31.0/docs/cvd-policy.md |
| 2(b) | Update design note | `48d8d713f9bd8bac` | s3://cra-pilot-evidence/v1/requests/2.31.0/docs/update-design-note.md |
| 2(c) Production and monitoring processes with validation evidence | Build provenance (https://slsa.dev/provenance/v1; builder https://aldermoor.example/builders/cra-pilot-local/v1; verified key by pilot-builder-provenance ; SLSA Build L1) ; Release gate decision: FAIL under cra-pilot-gate/1.0.0 | `640defe5c8ab2ff7` | s3://cra-pilot-evidence/v1/requests/2.31.0/evidence/provenance.sigstore.json |
| 3 Cybersecurity risk assessment and Annex I Part I applicability | Risk assessment | `dced93fc83d1a299` | s3://cra-pilot-evidence/v1/requests/2.31.0/docs/risk-assessment.md |
| 3 | Applicability matrix (not applied: 2l, 2m) | `e885c3dad355630d` | s3://cra-pilot-evidence/v1/requests/2.31.0/docs/applicability-matrix.json |
| 4 Support period | End 2028-05-22 (5.00 years); justification: Authored: each version supported for 5 years from its release date; users receive fixes by moving to the latest version (Art 13(10)).; latest-version rule (Art 13(10)): yes | | |
| 5 Harmonised standards, common specifications, certification schemes | Route module_a; applied in full: none; certificate n/a | | |
| 6 Test reports against Annex I Parts I and II | sast (Bandit; error=3, note=6, suppressed=0, warning=0) | `9aad81c5b5ded076` | s3://cra-pilot-evidence/v1/requests/2.31.0/evidence/sast.sarif |
| 7 EU declaration of conformity | Declaration PILOT-DoC-requests-2.31.0 (new) at https://aldermoor.example/cra-pilot/doc/requests/2.31.0 | | |
| 8 SBOM for market surveillance authority on reasoned request | SBOM | `5ff426b29e549fbf` | s3://cra-pilot-evidence/v1/requests/2.31.0/evidence/sbom.cdx.json |
