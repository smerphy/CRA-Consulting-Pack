# Appendix C to E1: record fields, control points, authority queries and storage sizing

This appendix holds reference detail behind the main paper ([paper.md](paper.md)). Aldermoor Platforms is fictional. All cost and volume figures are estimates unless marked as measured.

## Record fields and their legal basis

`spec/cra-evidence-record.v1.1.0.schema.json` (JSON Schema 2020-12) defines one record per version. Each property carries an `x-cra-basis` annotation citing the knowledge-base (KB) section.

| Field group | Content | Legal basis (KB) |
|---|---|---|
| `product`, `version` | Product id, name, manufacturer, type, family and variants; version, release date, previous version, artefact digest | Annex V pt 1; Annex VII pt 1; Annex II pt 3; guidance paras 174-177 (reports/sections/10-conformity.md; reports/guides/application/11-documentation-set.md) |
| `placing_on_market` | Version date; event type (first placing, new variant placing, substantial-modification placing, update to placed product); for an update, the inherited placing date and the version it comes from; Member States | Art 3(21); guidance paras 13-15 and Example 2 (reports/sections/03-scope.md); pt 116 |
| `classification` | Class, Annex III/IV category, route, standards applied in full, notified body, certificate | Art 32(1)-(5); Annex VIII (reports/sections/06-classification.md; reports/sections/10-conformity.md) |
| `evidence.sbom` | CycloneDX or SPDX, spec version, component count, top-level dependencies, completeness flag, SHA-256 and SHA-512 | Annex I Part II(1); Annex VII pts 2(b) and 8; Art 13(24)-(25) (reports/sections/08-annex1-part2.md; reports/guides/application/06-sbom.md) |
| `evidence.provenance` | Predicate type, builder id, build type, invocation id, subject-digest match, and (1.1.0) a `verification` block: method, signer key or certificate identity, Rekor entry, SLSA Build level, trust-policy id | Annex VII pt 2(c); Art 13(14) (reports/guides/application/11-documentation-set.md part 7). The format is a design choice |
| `evidence.vulnerability_status` | OpenVEX or CSAF VEX statements; known-vulnerability matches with KEV flag; feeds used; (1.1.0) the signed VEX attestation and its `verification` block | Annex I Part I(2)(a); guidance paras 233-234 (reports/sections/07-annex1-part1.md); para 218 (reports/guides/application/06-sbom.md) |
| `evidence.tests` | SAST, DAST, fuzz, pen test, update-mechanism tests: format, tool, counts | Annex I Part II(3); Annex VII pt 6 (reports/sections/08-annex1-part2.md) |
| `evidence.risk_assessment`, `evidence.applicability_matrix` | Reference and digest; Part I items covered and not applied | Art 13(2)-(4); Annex VII pt 3 (reports/sections/07-annex1-part1.md) |
| `evidence.annex_ii_user_information`, `update_design_note`, `cvd_policy` | Versioned URL and digest | Annex II; Art 13(18); Annex VII pts 1(d), 2(b) (reports/guides/application/07-updates.md; 11-documentation-set.md) |
| `support_period` | End date, years, justification, Art 13(10) latest-version flag | Art 13(8), 13(10), 13(19); guidance paras 125-128; Annex VII pt 4 (reports/sections/08-annex1-part2.md) |
| `substantial_modification` | Change type (pt 108/109 classes), the four pt 110 answers, bundling justification, assessor, decision, conformity-assessment reference | Guidance pts 104-112, 116, 122-123; Annex I Part II(2) (reports/sections/10-conformity.md; reports/sections/03-scope.md) |
| `declaration` | Declaration id, status (new, reused, updated, pending), source version, URL, signatory function | Art 13(12), 13(20), 28; Annex V; FAQ 6.8 (reports/sections/10-conformity.md) |
| `signer` | Pipeline identity, accountable role, signature reference | Design field supporting Art 13(22) |
| `retention` | Retain-until date, rule (naming any inherited placing date), store URI, object-lock mode | Art 13(13) (reports/sections/10-conformity.md) |
| `gate` | Decision, policy id, reasons with code, severity and basis | Release gate record (reports/guides/application/05-sdlc.md) |

The schema is semantically versioned. Optional additions are minor versions. Changes to required fields or enumerations are major versions, and old records keep validating against the version they declare. Version 1.1.0 adds the optional verification results and the optional `inherited_placing_date` and `inherited_from_version` fields. The 1.0.0 records already in the sample store still validate against 1.0.0. The enumeration is unchanged: `new_version_placing` now documents a version that is a new placing without a substantial modification, such as a build for another platform (guidance para 14).

## The gate applies eleven control points, each with a named reason, severity and basis

`cra_evidence/gate.py` implements the controls below (moved from the main paper on 1 Nov 2026). Every reason carries a code, a severity and its basis. A FAIL reason blocks the release. A REVIEW reason routes it to a named role. INFO reasons are kept for the audit trail.

| Control | FAIL when | REVIEW when |
|---|---|---|
| SBOM | Missing; no dependency edges from the root; a direct dependency in the build graph is absent; root hash does not match the artefact | Root carries no hash |
| Provenance signature | Unsigned; signature invalid; signer unknown, not authorised for this product or purpose, revoked, expired or not yet valid; keyless identity mismatch; transparency-log entry missing (where required) or failing offline verification | Unsigned, only where policy sets `require_signed_provenance: false` (shadow mode) |
| Provenance claims (from verified bytes only) | Predicate not SLSA v1; no subject matches the artefact digest; builder not trusted for the product or not bound to the signer; SLSA Build level below the product minimum; unexpected `buildType` or `externalParameters`; keyless identity differs from the workflow named | None |
| VEX origin | No signed VEX attestation; signature or signer fails as above; subject is not this artefact; signed predicate differs from the VEX document the gate used | Unsigned, only where policy allows |
| Known vulnerabilities | A KEV-listed match lacks VEX `not_affected` or `fixed`; VEX says `affected` with no mitigation; untriaged critical or high; `not_affected` without justification | `affected` with a documented mitigation; untriaged medium or low |
| Tests | Required test type missing (pen test on first placing or substantial modification); unsuppressed SARIF errors; open critical or high pen-test findings | Pen test absent while the substantial-modification decision is pending |
| Risk assessment and Annex II | No reference; matrix lacks any Part I item; item not applied without justification; Part I point (1) not applied; no Annex II reference | None |
| Support period | Missing; under 5 years without justification | Under 5 years with justification (counsel confirms that expected use is shorter) |
| Substantial modification and placing | Decision "substantial" not recorded as a new placing; inherited placing date later than the version date | Any pt 110 answer yes or unanswered; functionality change without a recorded human assessment; pt 109 change type; security fix bundled without justification; a new placing that also claims an inherited date |
| Route and declaration | For products placed from 11 Dec 2027 only (Art 69(2), Art 71(2); reports/sections/04-exclusions.md): Class I on Module A without a cited harmonised standard applied in full; Class II on Module A unless it is FOSS with public technical documentation (Art 32(5); guidance para 148); critical on either Module A route; Module B+C or H without a certificate reference. Any date: no declaration; declaration reused after a substantial modification | Declaration reuse depends on a pending review. Route and certificate gaps are INFO (`*_PRE_APPLICATION`) where the effective placing date, inherited or not, is before 11 Dec 2027 |
| Retention | Retain-until earlier than max(effective placing date + 10 years, support end); not computable | Store not in compliance-mode lock |

Two rules follow from the corrected reading of the guidance. The retention check uses the inherited placing date where it is earlier than the version date, which is the legal minimum. The route check uses the same effective date, so a product placed before 11 Dec 2027 can keep receiving non-substantial and security updates without a certificate, while its next substantially modified version cannot. A functionality release whose four answers are all "no", with a named assessor on record, passes with an INFO reason. The review has already happened, at the point where the person answered the questions.

## For Aldermoor the build system already holds most of the evidence

| Aldermoor asset | Use in the evidence pipeline | Gap to close |
|---|---|---|
| Monorepo with hermetic build | The SBOM comes from the build graph, which sees vendored third-party code that manifest scanners miss | Prebuilt binaries and vendor blobs (modem, GPU and secure-element firmware) need binary scanning plus supplier SBOMs (reports/guides/application/06-sbom.md) |
| Signed provenance for internal artefacts | Extend the same attestation to external release artefacts; register the builder, key and assessed SLSA level in the trust policy | Subjects must be the shipped, signed artefact; an L3 assessment of the builder |
| Release calendars and launch reviews | Supply version dates, placing events and inherited dates, Member States, change type and the four pt 110 answers | Decision rights for "not substantial" (Decision 3) |
| PSIRT (module E2 case engine) | Exports OpenVEX or CSAF per version; the same `not_affected` statement is evidence that no Art 14 report was due (guidance para 218) | PSIRT KMS signing key and two-person release for KEV items |
| Portfolio classification (module E3) | Supplies class, route and certificate reference per product | Module H approval depends on a notified body. None was designated at 8 Sep 2026 (reports/sections/10-conformity.md) |
| Versioned security pages | Annex II at `/security/<product>/<version>/`, kept online for the retention period (reports/guides/application/11-documentation-set.md) | Retention of web pages for 10+ years |

The store answers the predictable questions from authorities and notified bodies by query: the file for version X, which versions were on the market on a date, why a version was or was not a new placing, and whether the gate is enforced. The next section maps each question to the record fields.

## Authorities and notified bodies will ask predictable questions, and the store answers each by query

| Question | How the store answers |
|---|---|
| Show the technical documentation for version X as placed on date Y (Art 13(22)) | Retrieve the record by `record_id`; export the Annex VII index and its digested items as one package |
| Which versions were on the market on date D, and what was their status for CVE-Z? | Query records by version date, inherited placing date and support end; read VEX statements and the matches against the stored feed snapshot |
| Prove the file has not changed since placing | Object-lock retention per object; signed record with its RFC 3161 timestamp; Merkle inclusion proof against a signed checkpoint; digests in the record; DSSE signatures and Rekor entries the authority can verify itself ([Appendix A](appendix-trust-model.md)) |
| Who built and signed this version, and on what platform? | `verification` blocks: signer key or certificate identity, Rekor index and time, builder id and the SLSA level the trust policy assigned |
| Why was 4.3.0 (not) a substantial modification, and so (not) a new placing? | Four pt 110 answers, change type, assessor, rationale, conformity-assessment reference and placing event |
| Is the gate enforced, and how are exceptions controlled? (Module H audit) | Ledger of every decision, including FAIL and REVIEW; policy version per record; override log |
| Which declaration covers this version? | Declaration id, status, the version it was reused from, and its public URL |

## Storage sizing

The benchmark measured the machine evidence itself: SBOM, signed provenance and VEX, small SARIF files, record and index came to 126 KiB per version compressed (mean 1,100 SBOM components), or 0.013 TB a year at 104,000 versions. The cases below are therefore driven almost entirely by what else is retained: full SARIF, fuzz logs and crash corpora, pen-test reports and OS-scale SBOMs. These are retention choices, not measurements. All figures except the measured row are estimates.

| Case | Evidence per version (compressed, excluding binaries) | Per year at 104,000 versions | Held at steady state (about 11-year window) | Archive-tier cost per year |
|---|---|---|---|---|
| Measured core evidence (benchmark) | 0.13 MB | 0.013 TB | 0.15 TB | under USD 2 |
| Low (core plus full SARIF) | 5 MB | 0.5 TB | 5.7 TB | about USD 70 |
| Central (plus fuzz and pen-test reports) | 25 MB | 2.6 TB | 29 TB | about USD 340 |
| High (large SARIF, OS-scale SBOMs, fuzz logs) | 150 MB | 15.6 TB | 172 TB | about USD 2,100 |

The 11-year window is conservative. A version that keeps an earlier placing date (guidance para 15, Example 2) is retained to that date plus 10 years, or to its support end if later, so many records can expire sooner than their own version date implies.

The cost column uses the archive price AWS announced for S3 Glacier Deep Archive, about USD 1 per TB-month ([AWS, 2019](https://aws.amazon.com/ru/about-aws/whats-new/2019/03/S3-glacier-deep-archive/)); current list prices were not checked. Even at 25 times that price for a warmer tier, the high case stays near USD 50,000 a year. Release binaries are excluded. Art 13(9) already requires each security update to stay available for at least 10 years or the rest of the support period, whichever is longer, so the distribution system holds those; functionality-release binaries need their own retention decision (reports/sections/08-annex1-part2.md). Archive tiers charge per object, so bundle each version into one archive object plus a small hot index. Compliance-mode object lock prevents deletion or overwrite of a locked version "by any user, including the root user", and its retention period cannot be shortened ([AWS S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.md)). The module now ships an S3 Object Lock backend and a Merkle log over the records, tested against a local S3-compatible server; measured costs are in [Appendix D](appendix-signing-storage-pilot.md). Any WORM store with equivalent guarantees serves behind the same interface.

## Sources

- reports/sections/03-scope.md: placing date for software versions (guidance paras 13-15, Example 2).
- reports/sections/10-conformity.md, 08-annex1-part2.md, 07-annex1-part1.md, 06-classification.md; reports/guides/application/05-sdlc.md, 06-sbom.md, 07-updates.md, 11-documentation-set.md: as cited in the field table.
- AWS, [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.md) and [S3 Glacier Deep Archive announcement](https://aws.amazon.com/ru/about-aws/whats-new/2019/03/S3-glacier-deep-archive/).
