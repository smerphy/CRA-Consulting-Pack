## 6. SBOM pipeline

Generate the SBOM at build time from the artefact you ship, not from the manifest you think you built. The legal minimum is one machine-readable SBOM per product covering at least top-level dependencies. The de facto engineering profile is [BSI TR-03183-2 v2.1.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-2_v2_1_0.pdf?__blob=publicationFile&v=6), non-binding but the strictest widely referenced European specification.

The legal position and the missing Art 13(24) implementing act are covered in Annex I Part II: vulnerability handling and lifecycle duties.

### Generation from the shipped artefact

Run generation immediately after compilation or image assembly while the build context exists, so transitive dependencies are captured ([ENISA SBOM advisory v1.10](https://www.enisa.europa.eu/sites/default/files/2026-10/ENISA%20Technical%20Advisory%20-%20Software%20Bill%20of%20Materials%20-%20v1.10.pdf) section 4.1). A manifest-only SBOM misses vendored code, statically linked libraries and binaries copied into images. One vendor teardown found an embedded web server with a 2002 CVE that way ([Finite State](https://finitestate.io/blog/cra-compliance-mistakes), vendor).

Where the build system cannot see a component, scan the final artefact and merge.

| Artefact type | Primary generator | Supplement |
|---|---|---|
| Container image | Syft or Trivy on the image digest | cdxgen for application manifests inside the image |
| Language package (JVM, npm, Go, .NET) | cyclonedx-maven-plugin, @cyclonedx/cyclonedx-npm, cyclonedx-gomod, CycloneDX dotnet tool | Syft on the packaged output |
| Embedded Linux firmware | Yocto or Buildroot built-in SBOM generation | Binary SCA of the final image for blobs and vendored code |
| RTOS or bare-metal firmware | Zephyr "west spdx" or build-system plugin | Linker map cross-check for statically linked libraries |
| Mobile app | cdxgen or platform plugin on the signed bundle | Store-delivered SDK versions recorded per release |
| RDPS backend | Same as container or language package, per deployable service | Infrastructure left out; recorded as a dependency in the file |

Treat RDPS modules as part of the product and give them SBOMs. The hosting platform is a supply-chain dependency, not an SBOM entry (guidance para 205).

### Format and version

Produce CycloneDX 1.6 or later, or SPDX 3.0.1 or later, in JSON or XML (TR-03183-2 section 5). Favour one format natively rather than converting; conversion loses fields. CycloneDX 1.7 (October 2025) adds native VEX metadata and CSAF linkage per ENISA's comparison table, which helps with the separation rule below.

### Required fields per component

TR-03183-2 section 5.2 requires, per component: creator, name (else filename), version (SemVer or CalVer recommended), filename and dependencies with completeness marked. It also requires distribution licences, the SHA-512 hash of the deployable component, and the executable, archive and structured properties. Add where they exist: source-code URI, deployable URI, CPE and purl, original licences.

At SBOM level record creator (email or URL), timestamp in UTC and an SBOM URI where one exists.

Default generator output does not emit the BSI filename, executable, archive and structured properties. Post-process with BSI's registered CycloneDX taxonomy and validate ([CRA Decoded](https://cra-decoded.com/blog/posts/005_cra_sbom_pipeline/), vendor-adjacent). The CISA 2025 and 2026 minimum elements add component hash algorithm, licence, tool name and generation context.

ENISA's advisory carries a BSI-to-CISA field mapping. Recording tool name and generation context costs little and satisfies both.

```json
{
  "type": "library",
  "bom-ref": "pkg:generic/mbedtls@3.6.2?file=libmbedtls.a",
  "supplier": { "name": "Trusted Firmware project", "url": ["https://www.trustedfirmware.org"] },
  "name": "mbedtls",
  "version": "3.6.2",
  "purl": "pkg:github/Mbed-TLS/mbedtls@v3.6.2",
  "hashes": [{ "alg": "SHA-512", "content": "9f2c...e41a" }],
  "licenses": [{ "license": { "id": "Apache-2.0" } }],
  "properties": [
    { "name": "bsi:filename", "value": "libmbedtls.a" },
    { "name": "bsi:executable", "value": "false" },
    { "name": "bsi:archive", "value": "true" },
    { "name": "bsi:structured", "value": "false" },
    { "name": "bsi:dependencies:complete", "value": "true" }
  ]
}
```

Property names shown illustrate the BSI taxonomy pattern; use the identifiers BSI publishes for its CycloneDX namespace.

### Depth

Recurse down every dependency path at least to the first component outside your delivery scope, and include it. TR-03183-2 section 5.1 calls this the "delivery item SBOM".

List multiple instances of the same component with different metadata separately. You may reference a component's own SBOM instead of merging it only if that SBOM is itself compliant.

Mark completeness explicitly and declare known unknowns, distinguishing unknown from redacted.

The CRA floor is top-level dependencies. The OpenChain CRA checklist (community draft) ties the depth decision to the ability to make a 24-hour exploited-vulnerability determination. Record the depth decision and its rationale in the technical file.

### No vulnerability data in the SBOM

The SBOM is static inventory; vulnerability status changes daily. TR-03183-2 section 8.1.14 states the SBOM "MUST NOT contain vulnerability information" and recommends CSAF, with VEX as a profile, for that exchange. Keep three artefacts per release: the SBOM, a VEX document with a justified status per finding, and CSAF advisories for fixed vulnerabilities (section 8).

A "not_affected" VEX statement with a reachability justification is also evidence that no Art 14 report was due (guidance para 218).

### Quality, signing, storage and retention

1. Validate the schema with the CycloneDX CLI or the SPDX validators.
2. Score with sbomqs, which has a TR-03183-2 check, and fail the build below your threshold; record the score.
3. Sign or attest the SBOM bound to the artefact digest with Sigstore cosign or GitHub artefact attestations. Record the SHA-512 of the SBOM in the release gate record (section 5).
4. Store the SBOM, VEX, validation output, signature and generation log with the release artefacts. Use a dedicated location and a naming convention per product and version.
5. Retain for at least 10 years after placing or the support period, whichever is longer. The SBOM is part of the Annex VII technical documentation (Art 13(13)).

```yaml
# sbom job (GitHub Actions excerpt)
- name: Generate SBOM from image
  run: syft ghcr.io/acme/thermostat-fw@${DIGEST} -o cyclonedx-json@1.6 > sbom.cdx.json
- name: Enrich to BSI fields
  run: ./bsi-enrich.py sbom.cdx.json --hash sha512 --mark-completeness
- name: Validate and score
  run: cyclonedx validate --input-file sbom.cdx.json && sbomqs score sbom.cdx.json --category bsi-v2 --min 8.0
- name: Attest
  run: cosign attest --yes --type cyclonedx --predicate sbom.cdx.json ghcr.io/acme/thermostat-fw@${DIGEST}
- name: Upload to Dependency-Track
  run: curl -X PUT "$DT_URL/api/v1/bom" -H "X-Api-Key: $DT_KEY" \
       -F "projectName=thermostat-fw" -F "projectVersion=${GITHUB_REF_NAME}" -F "bom=@sbom.cdx.json"
```

### Continuous monitoring

Upload every release SBOM to Dependency-Track or an equivalent that polls NVD, GHSA and OSV. Add an EUVD watch, because the Commission treats EUVD listing as making a vulnerability "known" (guidance paras 233-234).

Route new matches to PSIRT triage (section 8) with product, version and support status attached. The Art 14 exploitation determination then starts the same day.

Keep monitoring running for every version still inside its support period, including versions no longer sold.

### Who receives the SBOM

The SBOM lives in the Annex VII technical documentation (point 2(b)). It goes to a market surveillance authority on reasoned request (point 8), or under Art 13(25) for an ADCO dependency assessment. Recital 77 says manufacturers need not publish it; Annex II point 9 makes user access optional and, if offered, requires saying where.

Decide per product and record the decision; many B2B customers will ask for it contractually regardless.

### Tooling landscape

ENISA's advisory section 2.2.3 lists generation tools (Syft, Trivy, cdxgen, and build plugins for Maven, Gradle, npm, Go, .NET, Linux and Zephyr). It lists validation (CycloneDX CLI, SPDX tools), quality (sbomqs, sbom-scorecard) and signing (cosign, GitHub attestations). Vulnerability management covers Grype, Trivy, Dependency-Track, OWASP Dependency-Check and dep-scan.

ENISA's SBOM State of Play 2026 (334 responses) found 44% of respondents using CycloneDX, 29% SPDX and 39% generating at build. Completeness was the top challenge at 62%, which is the manifest problem this section exists to prevent.

The signed SBOM and VEX per release close the SBOM lines of checklist 3, Part II, in the Requirement checklists tab.
