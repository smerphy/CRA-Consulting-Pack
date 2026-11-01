# Annex VII index: hearth-lock-3 4.2.0

Record `urn:aldermoor:cra-evidence:hearth-lock-3:4.2.0`. Version first offered 2028-01-18 as an update to a placed product. Retain until 2039-12-31. Substantial-modification decision: not_substantial.

| Annex VII point | Evidence | SHA-256 (first 16) | Location |
|---|---|---|---|
| 1 General description: intended purpose, versions affecting compliance, Annex II information | Shipped artefact ; Product hearth-lock-3 version 4.2.0; previous 4.1.3 | `dfe29277baeedf0e` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.2.0/artefact/hearth-lock-3-fw-4.2.0.bin |
| 1 | Annex II user information | `982aad7131b37e1e` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.2.0/docs/annex-ii-user-information.md |
| 2(a) Design and development; system architecture | Maintained outside the pipeline in the product technical file; linked by product id | | |
| 2(b) Vulnerability handling: SBOM, CVD policy, reporting contact, secure update distribution | SBOM (CycloneDX 1.5) | `68d7e52c7ca4768e` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.2.0/evidence/sbom.cdx.json |
| 2(b) | VEX (OpenVEX) | `3268316e7e2e05ae` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.2.0/evidence/vex.openvex.json |
| 2(b) | Signed VEX attestation (verified key by aldermoor-psirt-vex-2027) | `8ba9461850367fda` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.2.0/evidence/vex.openvex.intoto.json |
| 2(b) | CVD policy | `44a1d92cd4381540` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.2.0/docs/cvd-policy.md |
| 2(b) | Update design note | `d786137aa8aa16d7` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.2.0/docs/update-design-note.md |
| 2(c) Production and monitoring processes with validation evidence | Build provenance (https://slsa.dev/provenance/v1; builder https://build.aldermoor.example/hermetic/v2; verified key by aldermoor-build-provenance-2027 ; SLSA Build L3) ; Release gate decision: PASS under aldermoor-cra-gate/1.1.0 | `801b9404d0b14459` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.2.0/evidence/provenance.intoto.json |
| 3 Cybersecurity risk assessment and Annex I Part I applicability | Risk assessment | `e54496dcbf63d4dd` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.2.0/docs/risk-assessment.md |
| 3 | Applicability matrix (not applied: none) | `59e535340624231a` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.2.0/docs/applicability-matrix.json |
| 4 Support period | End 2039-12-31 (11.95 years); justification: Expected time in use of door-lock hardware exceeds 10 years; reasonable user expectations for a building fixture.; latest-version rule (Art 13(10)): no | | |
| 5 Harmonised standards, common specifications, certification schemes | Route module_h; applied in full: none; certificate QS-APPROVAL-ILLUSTRATIVE-0142 | | |
| 6 Test reports against Annex I Parts I and II | sast (CodeQL; error=0, note=1, suppressed=1, warning=1) | `d7cdbfff79d49a8a` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.2.0/evidence/sast.sarif |
| 6 | fuzz (libFuzzer (aldermoor-fuzz-farm); error=0, note=0, suppressed=0, warning=0) | `2a30a40038730352` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.2.0/evidence/fuzz.sarif |
| 7 EU declaration of conformity | Declaration AP-DoC-HL3-2027-001 (reused, from 4.0.0) at https://www.aldermoor.example/compliance/doc/hearth-lock-3 | | |
| 8 SBOM for market surveillance authority on reasoned request | SBOM | `68d7e52c7ca4768e` | s3://aldermoor-cra-evidence-eu/v1/hearth-lock-3/4.2.0/evidence/sbom.cdx.json |
