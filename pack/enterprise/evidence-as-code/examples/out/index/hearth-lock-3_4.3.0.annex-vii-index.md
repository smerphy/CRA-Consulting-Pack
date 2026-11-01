# Annex VII index: hearth-lock-3 4.3.0

Record `urn:aldermoor:cra-evidence:hearth-lock-3:4.3.0`. Placed 2028-03-06. Retain until 2039-12-31. Substantial-modification decision: pending_review.

| Annex VII point | Evidence | SHA-256 (first 16) | Location |
|---|---|---|---|
| 1 General description: intended purpose, versions affecting compliance, Annex II information | Shipped artefact ; Product hearth-lock-3 version 4.3.0; previous 4.2.0 | `adf4b8146683b1db` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.3.0/artefact/hearth-lock-3-fw-4.3.0.bin |
| 1 | Annex II user information | `d1e6221eab260720` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.3.0/docs/annex-ii-user-information.md |
| 2(a) Design and development; system architecture | Maintained outside the pipeline in the product technical file; linked by product id | | |
| 2(b) Vulnerability handling: SBOM, CVD policy, reporting contact, secure update distribution | SBOM (CycloneDX 1.5) | `c5cd3496d5237b26` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.3.0/evidence/sbom.cdx.json |
| 2(b) | VEX (OpenVEX) | `a07254adfbb2a060` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.3.0/evidence/vex.openvex.json |
| 2(b) | CVD policy | `44a1d92cd4381540` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.3.0/docs/cvd-policy.md |
| 2(b) | Update design note | `d786137aa8aa16d7` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.3.0/docs/update-design-note.md |
| 2(c) Production and monitoring processes with validation evidence | Build provenance (https://slsa.dev/provenance/v1; builder https://build.aldermoor.example/hermetic/v2) ; Release gate decision: REVIEW under aldermoor-cra-gate/1.0.0 | `94d8bb4efa541efe` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.3.0/evidence/provenance.intoto.json |
| 3 Cybersecurity risk assessment and Annex I Part I applicability | Risk assessment | `d8364cb9a4f4cb76` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.3.0/docs/risk-assessment.md |
| 3 | Applicability matrix (not applied: none) | `59e535340624231a` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.3.0/docs/applicability-matrix.json |
| 4 Support period | End 2039-12-31 (11.82 years); justification: Expected time in use of door-lock hardware exceeds 10 years; reasonable user expectations for a building fixture.; latest-version rule (Art 13(10)): no | | |
| 5 Harmonised standards, common specifications, certification schemes | Route module_h; applied in full: none; certificate QS-APPROVAL-ILLUSTRATIVE-0142 | | |
| 6 Test reports against Annex I Parts I and II | sast (CodeQL; error=0, note=1, suppressed=1, warning=1) | `d7cdbfff79d49a8a` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.3.0/evidence/sast.sarif |
| 6 | fuzz (libFuzzer (aldermoor-fuzz-farm); error=0, note=0, suppressed=0, warning=0) | `2a30a40038730352` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.3.0/evidence/fuzz.sarif |
| 6 | pentest (Aldermoor Red Team (internal); critical=0, high=0) | `f226f2d6d3f73c57` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.3.0/evidence/pentest-summary.json |
| 7 EU declaration of conformity | Declaration AP-DoC-HL3-2027-001 (reused, from 4.0.0) at https://www.aldermoor.example/compliance/doc/hearth-lock-3 | | |
| 8 SBOM for market surveillance authority on reasoned request | SBOM | `c5cd3496d5237b26` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.3.0/evidence/sbom.cdx.json |
