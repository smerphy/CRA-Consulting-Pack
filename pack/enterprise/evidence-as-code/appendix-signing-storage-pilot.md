# Appendix D to E1: record signing, timestamps, locked storage, the real-product pilot and the end-to-end benchmark

This appendix holds the engineering detail behind the main paper ([paper.md](paper.md)) for the parts built on 1 Nov 2026. Aldermoor Platforms is fictional. The pilot uses a real open-source project, requests, whose maintainers had no involvement; its CRA metadata is authored ([pilot README](examples/pilot/README.md)).

## Every evidence record is now a signed, time-stamped in-toto attestation

`cra_evidence/record_signing.py` wraps the gated record as the predicate of an in-toto Statement v1. The subject is the shipped artefact (SHA-256 and SHA-512), so the signature binds the CRA evidence to exactly one artefact. The predicate type is `https://aldermoor.example/attestations/cra-evidence-record/v1`; in-toto lets a producer define predicate types by URI, and no standard CRA predicate exists. The statement is signed as a DSSE envelope and carried in a Sigstore bundle v0.3 whose verification material holds a public-key hint and one RFC 3161 timestamp ([Sigstore bundle format](https://docs.sigstore.dev/about/bundle)). A Rekor entry is optional and, if present, is verified offline like any other bundle.

The read path verifies before it returns anything. `EvidenceStore.get_record` returns a record only when the signature verifies against a key authorised for `evidence_record`, the timestamp verifies against a trusted TSA (where the policy requires one), the predicate type is right, the canonical record digest equals the digest in the log entry, and the stored record bytes hash to the same value. Failure codes add `RECORD_PREDICATE_TYPE`, `RECORD_DIGEST_MISMATCH`, `RECORD_SUBJECT_MISMATCH` and `RECORD_ALTERED` to those in [Appendix A](appendix-trust-model.md).

## Keys stay in KMS or an HSM behind one interface

Every signer (builder, PSIRT, release pipeline, evidence log) is a `KeyProvider` with two operations: return the public key and sign bytes. The bytes signed are always the DSSE pre-authentication encoding, so the gate verifies every provider's output with the public key in the trust policy.

| Provider | Call | Integrity checks in the adapter | Test status |
|---|---|---|---|
| Local file | `cryptography` sign, ECDSA P-256 or Ed25519 | None needed | Used by tests, pilot and benchmark; demonstration only |
| AWS KMS | `Sign` with `MessageType=DIGEST`, `ECDSA_SHA_256`; AWS returns a DER signature ([AWS CLI reference](https://docs.aws.amazon.com/cli/latest/reference/kms/sign.html)) | Key spec ECC_NIST_P256 and usage SIGN_VERIFY; public key equals the one registered in the trust policy; every signature verified locally before use | Unit-tested with a mock client; not run against AWS |
| Google Cloud KMS | `asymmetric_sign` with a SHA-256 digest and its CRC32C | `verified_digest_crc32c` true, response `name` equals the key version, `signature_crc32c` matches ([Cloud KMS API](https://docs.cloud.google.com/python/docs/reference/cloudkms/latest/google.cloud.kms_v1.types.AsymmetricSignResponse)); local verification | Unit-tested with a mock client, including a wrong-key-version reply; not run against Google Cloud |
| HSM (PKCS#11) | CKM_ECDSA over the SHA-256 digest; raw r‖s re-encoded as DER | 64-byte result; public key from the key-ceremony record; local verification | Unit-tested with a mock session; not run against an HSM |

The pipeline role needs only the sign permission on its own key. Rotation, revocation and compromise handling are unchanged from [Appendix A](appendix-trust-model.md).

## RFC 3161 timestamps give key-based signatures an independent time

`cra_evidence/tsa.py` requests and verifies RFC 3161 tokens with `asn1crypto` for parsing and `cryptography` for signatures. The time-stamped message is the signature bytes. Verification checks, in order: PKI status; the message imprint equals the hash of the signature; the nonce, where one was sent; CMS SignedData with content type id-ct-TSTInfo; signed attributes carrying that content type and a message digest equal to the hash of the TSTInfo; the signer certificate found by its identifier and, where present, by the ESS signing-certificate hash; the signature over the signed attributes; a chain to a trusted root (one intermediate at most); an extended key usage of time-stamping only, marked critical, as RFC 3161 section 2.3 requires ([RFC 3161](https://datatracker.ietf.org/doc/html/rfc3161)); and genTime inside the certificate's validity and the authority's configured window.

The verifier now takes signing time from a verified log entry first, then from a verified timestamp, and only then from the gate's clock, and records which. A key that expired on 1 Jun 2026 still verifies a signature time-stamped on 1 Mar 2026, and fails without the timestamp (tested). A timestamp over other bytes, or from an untrusted authority, fails closed as `TIMESTAMP_INVALID`; a policy that requires a timestamp and finds none fails as `TIMESTAMP_MISSING`.

Two independent implementations accept the module's tokens: `rfc3161-client` 1.0.9 (used by sigstore-python) and `openssl ts -verify` (OpenSSL 3.0.13), which also rejects a token checked against other data. Both checks are in the test suite. The authority in tests and the pilot is a local test TSA the module generates. Production needs a contracted authority. A qualified electronic time stamp under eIDAS (Regulation (EU) No 910/2014, Art 41(2)) carries a legal presumption that its time is accurate; this module has not verified that text against the Official Journal.

## Storage: one interface, a local store and an S3 Object Lock backend

`cra_evidence/objectstore.py` defines write-once objects with a retain-until date: `put`, `get`, `list`, `retention`, `extend_retention` (lengthen only) and `delete` (must fail while locked). `LocalBackend` generalises the module's original local store: exclusive create, read-only files, retention in a sidecar. It models the contract but cannot stop a privileged local user; the signed log detects what it cannot prevent.

`S3ObjectLockBackend` refuses a bucket without Object Lock. Each PUT sends `ObjectLockMode=COMPLIANCE`, `ObjectLockRetainUntilDate` (end of the record's retain-until day, UTC), `ChecksumAlgorithm=SHA256` and `If-None-Match: *`, checks the returned checksum, then reads the lock back. Content-addressed blobs shared by several versions are written once and their lock is extended to the latest retain-until date. AWS documents that a compliance-mode version cannot be deleted or overwritten by any user and that its retention cannot be shortened ([AWS S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.md)).

| Behaviour (moto 5.2.5 S3 server over HTTP) | Result | Enforced by |
|---|---|---|
| PUT with compliance retention; lock and checksum read back | Pass | Server |
| Delete a locked version (with or without the governance-bypass header) | Refused, `AccessDenied` | Server |
| Second PUT to the same key | Refused, precondition failed | Server (`If-None-Match`) |
| Delete without a version id | Adds a delete marker; the locked version is still readable | Server |
| Shorten retention, or switch to governance mode | **Accepted by moto**, refused by AWS per its documentation | Backend refuses shortening itself; AWS behaviour untested |
| Bucket without Object Lock | Refused by the backend | Backend |

Production controls (design, not built): a dedicated evidence account and EU-region bucket created with Object Lock; a bucket policy that denies PUTs without lock headers and denies the governance-bypass permission; replication to a second region with its own lock; and alerting on any delete marker.

## A Merkle log makes tampering detectable whatever the storage did

`cra_evidence/merkle.py` implements the RFC 9162 Merkle tree (the hashing Rekor uses), inclusion and consistency proofs and an incremental tree with O(log n) state. `cra_evidence/evidence_store.py` writes, per version: input blobs, the canonical record, the signed record bundle and a log entry (record digest, bundle digest, artefact digest, decision, retain-until, hash-chain link). After every N entries it signs a checkpoint statement (log id, tree size, root hash) with the log key and time-stamps it.

| Attack on the store | Detected by | Tested |
|---|---|---|
| Record edited | Record digest differs from the log entry; signature fails | Yes |
| Log entry edited | Merkle root differs from the signed checkpoint | Yes |
| Latest entries deleted (truncation) | Checkpoint size exceeds the log | Yes |
| Record forged with a valid-looking entry | Inclusion proof fails against the checkpoint | Yes |
| Whole log rewritten and checkpoints re-signed with a stolen log key | Only by a party holding an earlier checkpoint, through a consistency proof | Proofs tested; distribution of checkpoints is a process (design) |

The last row is why checkpoints must leave Aldermoor: send them to the notified body or an internal audit function each quarter, or log them in a public transparency log. That is the optional Rekor step, not built here.

## The pilot rebuilt ten real releases and stored them under lock

| Measure (requests 2.31.0 to 2.34.2, 1 Nov 2026, 2 vCPU) | Result |
|---|---|
| Builds bit-identical when repeated | 10 of 10 |
| Wheel payload identical to the wheel on PyPI | 10 of 10 (metadata and zip timestamps differ) |
| Gate at release | 3 PASS, 7 FAIL: bandit B324 at error level in 2.31.0 to 2.33.1, cleared when 2.34.0 marked the Digest hashes `usedforsecurity=False`; no penetration test for the first placing |
| Gate with the 1 Nov 2026 feed | 10 FAIL: untriaged high and critical advisories in urllib3 and certifi published after release |
| Placing events (authored) | 1 first placing, 1 substantial modification, 8 updates keeping 21 May 2024 |
| Signing time of every attestation | RFC 3161 timestamp |
| Store | 133 objects, 1.44 MB, all compliance mode; verify clean; delete and overwrite refused |
| Time per version | 6.9 s mean end to end; trust work (sign, time-stamp, verify, store) about 0.3 s |

The pilot also found three matcher defects on real OSV data that synthetic feeds hid; all are fixed and tested ([pilot README](examples/pilot/README.md)).

## Benchmark: the hard part costs about 280 ms a version on one thread

`bench/bench_e2e.py` ran 1,000 synthetic versions through producer signing and time-stamping, the gate with signature and timestamp verification, record signing and time-stamping, Object Lock PUTs with read-back, Merkle append and a signed checkpoint, all over HTTP to local services. Results are in `bench/results/bench-e2e-1000.json`.

| Stage (ms per version, 1,000 versions) | Per-version checkpoints: mean (p95) | Batched, checkpoint every 100: mean (p95) |
|---|---|---|
| Sign and time-stamp provenance and VEX | 19.3 (24.6) | 19.8 (25.0) |
| Gate with signature and timestamp verification | 32.2 (46.0) | 29.7 (44.5) |
| Sign and time-stamp the record | 10.2 (14.1) | 0.7 (1.1), not time-stamped individually |
| Object Lock PUTs (about 17) with lock read-back | 196.3 (221.2) | 198.4 (226.9) |
| Merkle append | 0.08 | 0.09 |
| Signed, time-stamped checkpoint | 18.7 (26.9) | 0.2 amortised |
| **End to end** | **278.5 (312.2)** | **249.6 (286.2)** |
| Audit verification of the whole store | 25.0 ms a version | 15.4 ms a version |

Decisions were 926 PASS, 46 REVIEW, 28 FAIL (injected defects), every signing time came from a timestamp, and audit verification found no problems. Storage dominates: about 12 objects and 0.9 MB of inputs per version. In batched mode a record gets its independent time from the next time-stamped checkpoint rather than its own token.

Extrapolation (estimate): 2,000 EU versions a week need about 0.15 single-thread hours, and 104,000 a year about 8 hours. The write path makes 42 remote calls a version (4 signatures, 4 timestamps, 17 PUTs, 17 read-backs). At an assumed 50 ms per call to a real KMS, TSA and object store (an assumption, not a measurement), a version would take about 2.4 s sequentially; calls parallelise within a version and versions are independent. Throughput is not the constraint; KMS and TSA request quotas, and the TSA contract, should be sized against peak release days.

## CI: a pilot workflow, validated but not run

`examples/ci/github-actions-cra-pilot.yml` runs the pilot on `workflow_dispatch`: hash-checked dependency install from `examples/pilot/requirements-pilot.txt`, a step that allows unprivileged user namespaces on Ubuntu 24.04 so the build can run without network, the pilot, an offline `verify-evidence-store`, the test suite, and upload of results. Permissions are read-only and actions are pinned by commit SHA. actionlint 1.7.12 and the GitHub workflow JSON Schema (check-jsonschema) report no errors, and the test suite checks pinning and permissions. Neither workflow has run on GitHub.

## Sources

- Sigstore, [Bundle format](https://docs.sigstore.dev/about/bundle): timestampVerificationData, RFC 3161 timestamps, public-key hint.
- IETF, [RFC 3161](https://datatracker.ietf.org/doc/html/rfc3161): sections 2.3 (critical time-stamping EKU) and 2.4.1 (message imprint, nonce).
- AWS, [CLI reference: kms sign](https://docs.aws.amazon.com/cli/latest/reference/kms/sign.html): DIGEST message type and DER-encoded ECDSA signatures; [S3 Object Lock](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.md).
- Google Cloud, [AsymmetricSignResponse](https://docs.cloud.google.com/python/docs/reference/cloudkms/latest/google.cloud.kms_v1.types.AsymmetricSignResponse): CRC32C integrity fields.
- Pilot inputs: [requests on PyPI](https://pypi.org/project/requests/), [OSV API](https://api.osv.dev/v1/query), [cisagov/kev-data](https://github.com/cisagov/kev-data); digests and retrieval times in `examples/pilot/results/pilot-results.json` and `examples/pilot/feeds/`.
