# Annex VII index: npm-sigstore 5.0.0

Record `urn:aldermoor:cra-evidence:npm-sigstore:5.0.0`. Placed 2028-01-20 (new_version_placing). Retain until 2038-01-20. Substantial-modification decision: not_substantial.

| Annex VII point | Evidence | SHA-256 (first 16) | Location |
|---|---|---|---|
| 1 General description: intended purpose, versions affecting compliance, Annex II information | Shipped artefact ; Product npm-sigstore version 5.0.0; previous 4.1.0 | `3718e9a74a5a824a` | s3://aldermoor-cra-evidence-eu/v1/npm-sigstore/5.0.0/artefact/sigstore-5.0.0.tgz |
| 1 | Annex II user information | `c9ccfabfacc0a050` | s3://aldermoor-cra-evidence-eu/v1/npm-sigstore/5.0.0/docs/annex-ii-user-information.md |
| 2(a) Design and development; system architecture | Maintained outside the pipeline in the product technical file; linked by product id | | |
| 2(b) Vulnerability handling: SBOM, CVD policy, reporting contact, secure update distribution | SBOM (CycloneDX 1.5) | `9b24e4142b761b9a` | s3://aldermoor-cra-evidence-eu/v1/npm-sigstore/5.0.0/evidence/sbom.cdx.json |
| 2(b) | VEX (OpenVEX) | `dcf8db7ba7137a93` | s3://aldermoor-cra-evidence-eu/v1/npm-sigstore/5.0.0/evidence/vex.openvex.json |
| 2(b) | Signed VEX attestation (verified key by aldermoor-psirt-vex-2027) | `6875d6d25c321d99` | s3://aldermoor-cra-evidence-eu/v1/npm-sigstore/5.0.0/evidence/vex.openvex.intoto.json |
| 2(b) | CVD policy | `44a1d92cd4381540` | s3://aldermoor-cra-evidence-eu/v1/npm-sigstore/5.0.0/docs/cvd-policy.md |
| 2(b) | Update design note | `976ed63488a0178f` | s3://aldermoor-cra-evidence-eu/v1/npm-sigstore/5.0.0/docs/update-design-note.md |
| 2(c) Production and monitoring processes with validation evidence | Build provenance (https://slsa.dev/provenance/v1; builder https://github.com/actions/runner/github-hosted; verified sigstore-keyless by https://github.com/sigstore/sigstore-js/.github/workflows/release.yml@refs/heads/main ; SLSA Build L2 ; Rekor index 1697019812) ; Release gate decision: REVIEW under aldermoor-cra-gate/1.1.0+real-artefact | `ab9228005186f50e` | s3://aldermoor-cra-evidence-eu/v1/npm-sigstore/5.0.0/evidence/npm-attestations.json |
| 3 Cybersecurity risk assessment and Annex I Part I applicability | Risk assessment | `bd1610da6258754f` | s3://aldermoor-cra-evidence-eu/v1/npm-sigstore/5.0.0/docs/risk-assessment.md |
| 3 | Applicability matrix (not applied: none) | `b09098ccd63dd56e` | s3://aldermoor-cra-evidence-eu/v1/npm-sigstore/5.0.0/docs/applicability-matrix.json |
| 4 Support period | End 2033-01-31 (5.03 years); justification: Synthetic: five years from placing with Art 13(10) latest-version rule.; latest-version rule (Art 13(10)): yes | | |
| 5 Harmonised standards, common specifications, certification schemes | Route module_a; applied in full: none; certificate n/a | | |
| 6 Test reports against Annex I Parts I and II | sast (ESLint; error=0, note=0, suppressed=0, warning=5) | `8f6d487897c2b71c` | s3://aldermoor-cra-evidence-eu/v1/npm-sigstore/5.0.0/evidence/sast.sarif |
| 7 EU declaration of conformity | Declaration AP-DoC-NPM-SIGSTORE-SYNTH (new) at https://www.aldermoor.example/compliance/doc/npm-sigstore | | |
| 8 SBOM for market surveillance authority on reasoned request | SBOM | `9b24e4142b761b9a` | s3://aldermoor-cra-evidence-eu/v1/npm-sigstore/5.0.0/evidence/sbom.cdx.json |
