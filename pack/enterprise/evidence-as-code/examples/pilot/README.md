# Pilot: the evidence pipeline on a real product line (requests, ten versions)

This folder runs the module end to end on a real open-source project: **requests**, the Python HTTP library ([PyPI](https://pypi.org/project/requests/), [github.com/psf/requests](https://github.com/psf/requests)). It rebuilds ten released versions, 2.31.0 to 2.34.2, from their PyPI source distributions, generates evidence, signs and time-stamps it, runs the release gate, and stores everything in an Object Lock bucket behind a Merkle log. Run on 1 Nov 2026.

**The requests project is not an Aldermoor product, and its maintainers and the Python Software Foundation had no involvement.** The pilot treats it *as if* it were an Aldermoor product line placed on the EU market, so that the pipeline meets real builds, real dependency trees, real SAST findings and real advisories. Every CRA judgement in it is authored by us and labelled so.

```text
python examples/pilot/run_pilot.py            # about 75 s with a warm cache, 100 s cold
python -m cra_evidence verify-evidence-store --store examples/pilot/out/store \
    --policy examples/pilot/policy/pilot-gate-policy.json --deep
```

## What is real and what is authored

| Item | Status | Detail |
|---|---|---|
| Source distributions | Real | Downloaded from files.pythonhosted.org; SHA-256 checked against PyPI's published digest |
| Build | Real, local | `python -m build --wheel` (build 1.6.1) in an isolated build environment, run inside `unshare -rn` (a network namespace with no network). The only build input besides the sdist is setuptools 84.2.1 from a local wheelhouse, pinned by SHA-256 `ca140b45...89c2`. `SOURCE_DATE_EPOCH` is the version's PyPI upload time |
| Reproducibility | Real, measured | Each version is built twice from separate extractions. All ten pairs are bit-identical. All ten wheels contain exactly the same importable files, byte for byte, as the wheel the project published on PyPI; only the `.dist-info` metadata and zip timestamps differ |
| SBOM | Real, generated | The built wheel installed into a fresh venv with dependencies resolved as at the release time (`pip --uploaded-prior-to`), then `cyclonedx-py environment` (cyclonedx-bom 7.6.0), CycloneDX 1.6. Our step binds the SBOM root to the built wheel by SHA-256 and SHA-512 |
| SAST | Real | bandit 1.9.4 over the sdist source, SARIF output |
| Build provenance | Real for this local build | SLSA v1 provenance written by `run_pilot.py`, signed by the pilot builder key (ECDSA P-256) through a `KeyProvider`, with an RFC 3161 timestamp. The trust policy rates this builder **SLSA Build L1**: it is a script on one host, so it is not a hosted platform (L2) and build steps can reach the signing key (not L3) |
| Advisories | Real | OSV records for all five packages (72 records) from api.osv.dev, and the CISA KEV catalogue 2026.10.30 (1,766 entries) from github.com/cisagov/kev-data. "At release" uses OSV records published before the version's upload time; record contents are as they read on 1 Nov 2026, so this approximates the feed as it stood |
| VEX | Authored | OpenVEX per version, signed by the pilot PSIRT key (Ed25519) and time-stamped. No triage was done, so every match would be `under_investigation`; at release there were none |
| CRA metadata | Authored | `authored/product-line.json`: default class, Module A, support period, placing events, the four guidance pt 110 answers per version with rationale, declarations. The `changelog_basis` fields summarise each version's real HISTORY.md |
| Risk assessment, Annex II, matrix | Authored stubs | Generated per version, labelled "AUTHORED PILOT STUB" |
| Keys and TSA | Demonstration | File-based keys in `keys/`; a local test time-stamping authority (generated EC P-256 root and TSA certificate) in `trust/` |
| Object Lock store | Real protocol, emulated service | boto3 against moto 5.2.5's S3 server over HTTP on 127.0.0.1, bucket created with Object Lock, every PUT in compliance mode |

## Results

| Version | PyPI upload | Change type (authored) | Placing event | Retain until | Gate at release | Gate with today's feed | Build, s | End to end, s |
|---|---|---|---|---|---|---|---|---|
| 2.31.0 | 2023-05-22 | first placing | First placing | 2033-05-22 | FAIL (TEST_EVIDENCE_MISSING, TEST_FINDINGS_OPEN) | FAIL (18 untriaged advisories) | 1.4 | 7.7 |
| 2.32.2 | 2024-05-21 | security and functionality | New placing (substantial, authored) | 2034-05-21 | FAIL (TEST_FINDINGS_OPEN) | FAIL (14) | 1.5 | 6.7 |
| 2.32.3 | 2024-05-29 | non-security maintenance | Update; keeps 2024-05-21 | 2034-05-21 | FAIL (TEST_FINDINGS_OPEN) | FAIL (14) | 1.5 | 6.9 |
| 2.32.4 | 2025-06-09 | security update | Update; keeps 2024-05-21 | 2034-05-21 | FAIL (TEST_FINDINGS_OPEN) | FAIL (11) | 1.4 | 6.7 |
| 2.32.5 | 2025-08-18 | functionality | Update; keeps 2024-05-21 | 2034-05-21 | FAIL (TEST_FINDINGS_OPEN) | FAIL (9) | 1.4 | 6.6 |
| 2.33.0 | 2026-03-25 | security and functionality | Update; keeps 2024-05-21 | 2034-05-21 | FAIL (TEST_FINDINGS_OPEN) | FAIL (7) | 1.6 | 6.9 |
| 2.33.1 | 2026-03-30 | non-security maintenance | Update; keeps 2024-05-21 | 2034-05-21 | FAIL (TEST_FINDINGS_OPEN) | FAIL (7) | 1.6 | 6.8 |
| 2.34.0 | 2026-05-11 | functionality | Update; keeps 2024-05-21 | 2034-05-21 | PASS | FAIL (5) | 1.6 | 6.8 |
| 2.34.1 | 2026-05-13 | non-security maintenance | Update; keeps 2024-05-21 | 2034-05-21 | PASS | FAIL (4) | 1.6 | 7.0 |
| 2.34.2 | 2026-05-14 | non-security maintenance | Update; keeps 2024-05-21 | 2034-05-21 | PASS | FAIL (4) | 1.6 | 6.9 |

What the decisions mean:

- **SAST blocked 2.31.0 to 2.33.1.** bandit reports rule B324 (MD5 and SHA-1 use) at error level three times in `auth.py`, the HTTP Digest authentication code. Requests 2.34.0 added `usedforsecurity=False` to those hash calls (its changelog says so), and the finding disappears from that version on. A real programme would triage this (Digest authentication requires those algorithms) and record a justified SARIF suppression; the pilot leaves the finding unsuppressed, so the gate blocks.
- **The first placing also failed for a missing penetration test.** The gate requires one on every first placing; the pilot has none.
- **No advisory matched any version at its release time** after the matcher fixes below, so the authored VEX documents are empty.
- **With today's feed every version fails.** Even 2.34.2, resolved with urllib3 2.7.0 and certifi 2026.4.22 at its release, now matches three urllib3 advisories (two rated high) published on 30 Sep 2026 and a critical certifi advisory published on 20 Oct 2026. This is the post-market view: the stored at-release record is unchanged, and the new exposure needs a new VEX and, where affected, an update.
- **Placing and retention follow the authored decisions.** 2.32.2 is recorded as a substantial modification, so it is a new placing with an updated declaration; later versions keep its placing date, 21 May 2024, and are retained to 21 May 2034 (placing date plus 10 years, which is later than each version's support end).

Time per version, mean of ten (seconds; downloads cached and excluded):

| Stage | Mean | Share |
|---|---|---|
| Build (network-isolated, isolated environment) | 1.52 | 22% |
| Independent rebuild for the reproducibility check | 1.50 | 22% |
| SBOM (venv, dependency install, cyclonedx-py) | 3.11 | 45% |
| SAST (bandit) | 0.47 | 7% |
| Sign and time-stamp provenance and VEX (two signatures, two TSA calls over HTTP) | 0.02 | under 1% |
| Gate, including signature and timestamp verification | 0.11 | 2% (first version includes feed indexing) |
| Sign and time-stamp the record | 0.01 | under 1% |
| Object Lock PUTs (inputs, record, signed record, log entry), with lock read-back | 0.16 | 2% |
| Merkle append, signed and time-stamped checkpoint | 0.02 | under 1% |
| **End to end** | **6.91** | |

The pipeline's own trust work (signing, time-stamping, verification and locked storage) is about 0.3 s of the 6.9 s. Building and SBOM generation dominate.

## Store checks

- 133 objects (1.44 MB) for ten versions, all in compliance mode with the record's retain-until date; listed in `out/s3-inventory.json`.
- `EvidenceStore.verify` over the bucket and over the offline mirror in `out/store/`: no problems. It recomputes the hash chain and the Merkle root, checks the root against the signed checkpoint, and verifies every record signature and timestamp.
- Deleting the 2.31.0 record version: refused (`AccessDenied`). Writing the same key again: refused (`If-None-Match`, precondition failed). Reading 2.32.4 back: signature and RFC 3161 timestamp verified. A copy of a record with its gate decision changed fails signature verification.
- `out/records/*.inclusion-proof.json` hold each record's Merkle inclusion proof; `out/latest-checkpoint.json` is the signed tree head (size 10).

## What the pilot found

1. **False positives from real OSV data.** OSV `PYSEC` records carry GIT ranges with commit hashes as well as ECOSYSTEM ranges. The matcher compared commit hashes as versions, so every version appeared affected by vulnerabilities fixed years earlier (for example CVE-2015-2296 in requests 2.31.0 and CVE-2020-26137 in urllib3 2.7.0). Fixed: only ECOSYSTEM and SEMVER ranges are compared. Synthetic feeds could not have shown this.
2. **Duplicate findings.** The same advisory appears as GHSA and PYSEC records. Fixed: matches are keyed by CVE, or by one canonical id for records that alias each other.
3. **The product's own advisories were not matched**, because the SBOM root was excluded from matching. Fixed: the root is matched too.
4. **Network-isolated builds need sdists extracted without their recorded owners** (`tar --no-same-owner`); otherwise setuptools cannot set timestamps inside the user namespace.

## Limits

- The builder is local and rated SLSA Build L1. It shows the provenance, signing and verification path, not a hardened build platform.
- The TSA and all keys are local demonstration material. A real deployment needs a contracted TSA and KMS or HSM keys.
- moto enforces delete denial for locked versions, `If-None-Match` and the lock headers. In our probe it **did not** refuse shortening a compliance-mode retention date or switching it to governance mode, which AWS S3 does refuse. The backend refuses to shorten retention itself; the AWS guarantee is untested here.
- Release dates fall before 11 Dec 2027, so the Regulation did not apply to these versions; the pilot exercises the mechanics only.
- The as-at-release feed filters today's OSV records by publication date. Records edited after publication are seen in their current form.
