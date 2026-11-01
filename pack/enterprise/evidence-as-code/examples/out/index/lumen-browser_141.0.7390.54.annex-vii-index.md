# Annex VII index: lumen-browser 141.0.7390.54

Record `urn:aldermoor:cra-evidence:lumen-browser:141.0.7390.54`. Version first offered 2028-02-03; not a new placing, so it keeps placing date 2028-01-06 from version 141.0.7390.40 (guidance para 15, Example 2). Retain until 2038-01-06. Substantial-modification decision: not_substantial.

| Annex VII point | Evidence | SHA-256 (first 16) | Location |
|---|---|---|---|
| 1 General description: intended purpose, versions affecting compliance, Annex II information | Shipped artefact ; Product lumen-browser version 141.0.7390.54; previous 141.0.7390.40 | `cfbeb4ccf87c71c0` | s3://aldermoor-cra-evidence-eu/v1/lumen-browser/141.0.7390.54/artefact/lumen-browser-141.0.7390.54-linux-x64.tar.zst |
| 1 | Annex II user information | `75d9263a86bcb4f3` | s3://aldermoor-cra-evidence-eu/v1/lumen-browser/141.0.7390.54/docs/annex-ii-user-information.md |
| 2(a) Design and development; system architecture | Maintained outside the pipeline in the product technical file; linked by product id | | |
| 2(b) Vulnerability handling: SBOM, CVD policy, reporting contact, secure update distribution | SBOM (SPDX 2.3) | `6a3d29f51d587627` | s3://aldermoor-cra-evidence-eu/v1/lumen-browser/141.0.7390.54/evidence/sbom.spdx.json |
| 2(b) | VEX (CSAF-VEX) | `328cd76eb9e24645` | s3://aldermoor-cra-evidence-eu/v1/lumen-browser/141.0.7390.54/evidence/vex.csaf.json |
| 2(b) | Signed VEX attestation (verified key by aldermoor-psirt-vex-2027) | `466602ff5c720f2a` | s3://aldermoor-cra-evidence-eu/v1/lumen-browser/141.0.7390.54/evidence/vex.csaf.intoto.json |
| 2(b) | CVD policy | `44a1d92cd4381540` | s3://aldermoor-cra-evidence-eu/v1/lumen-browser/141.0.7390.54/docs/cvd-policy.md |
| 2(b) | Update design note | `37ca7dece61e1034` | s3://aldermoor-cra-evidence-eu/v1/lumen-browser/141.0.7390.54/docs/update-design-note.md |
| 2(c) Production and monitoring processes with validation evidence | Build provenance (https://slsa.dev/provenance/v1; builder https://build.aldermoor.example/hermetic/v2; verified key by aldermoor-build-provenance-2027 ; SLSA Build L3) ; Release gate decision: FAIL under aldermoor-cra-gate/1.1.0 | `14ddce522143f000` | s3://aldermoor-cra-evidence-eu/v1/lumen-browser/141.0.7390.54/evidence/provenance.intoto.json |
| 3 Cybersecurity risk assessment and Annex I Part I applicability | Risk assessment | `896d6cdf84deaa07` | s3://aldermoor-cra-evidence-eu/v1/lumen-browser/141.0.7390.54/docs/risk-assessment.md |
| 3 | Applicability matrix (not applied: none) | `d55194eb9a00a65a` | s3://aldermoor-cra-evidence-eu/v1/lumen-browser/141.0.7390.54/docs/applicability-matrix.json |
| 4 Support period | End 2033-02-28 (5.07 years); justification: Product support period for Lumen Browser; Art 13(10) latest-version rule with free upgrade.; latest-version rule (Art 13(10)): yes | | |
| 5 Harmonised standards, common specifications, certification schemes | Route module_h; applied in full: none; certificate QS-APPROVAL-ILLUSTRATIVE-0142 | | |
| 6 Test reports against Annex I Parts I and II | sast (CodeQL; error=0, note=0, suppressed=0, warning=1) | `ed54847348230975` | s3://aldermoor-cra-evidence-eu/v1/lumen-browser/141.0.7390.54/evidence/sast.sarif |
| 6 | fuzz (libFuzzer (aldermoor-fuzz-farm); error=1, note=0, suppressed=0, warning=0) | `18780cb95733739d` | s3://aldermoor-cra-evidence-eu/v1/lumen-browser/141.0.7390.54/evidence/fuzz.sarif |
| 7 EU declaration of conformity | Declaration AP-DoC-LB-141 (reused, from 141.0.7390.40) at https://www.aldermoor.example/compliance/doc/lumen-browser | | |
| 8 SBOM for market surveillance authority on reasoned request | SBOM | `6a3d29f51d587627` | s3://aldermoor-cra-evidence-eu/v1/lumen-browser/141.0.7390.54/evidence/sbom.spdx.json |
