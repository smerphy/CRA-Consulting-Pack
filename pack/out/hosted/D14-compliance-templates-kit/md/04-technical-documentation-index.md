# 4 · Technical documentation index

The technical documentation index is the first page of a product's Annex VII file. It lists every required content item, the artefact that satisfies it, its owner, where it is kept and its status. Art 31 requires the file before placing on the market; keep the index in the system of record and update it at every release gate.

## At a glance

| Item | Detail |
| --- | --- |
| Legal basis | Art 31; Annex VII pts 1-8; Art 13(12)-(13); Art 13(22) |
| Needed for | Every conformity route; any market surveillance request; the notified-body application under Module B or H |
| Owner | Compliance lead |
| Approver | Head of product security |
| When to create | At project start; populate as artefacts are produced |
| When to update | At each release gate, each placing of a new version and each substantial modification |
| Retention | 10 years after placing or the support period, whichever is longer (Art 13(13)) |
| Feeds | Draws on Templates 1-3 and 5-9; supports Template 10 |

## How to complete

1. Fill the control block: product, variants, file version, retention date and language.
2. For each Annex VII row, name the artefact, owner, location and version.
3. Link every artefact to a controlled record in the system of record, never to a mailbox or personal drive.
4. If one file covers a family, complete the variant list.
5. Mark status per row and close gaps before the release gate.
6. Freeze a copy of the index with each placing on the market.

## Template

### Part A: control block

| Field | What to enter | Basis | Example: L2 Smart Lock (illustrative) |
| --- | --- | --- | --- |
| File ID and version | \[TF-ID\], \[version\], \[date\] | Art 31 | TF-L2 v1.0 |
| Product and variants | \[Family; variant list in Part C\] | Guidance paras 174-177 | L2 Smart Lock, 3 SKUs |
| Conformity route | \[From Template 1\] | Art 32 | Module B+C (planned) |
| Retention end | \[10 years after last placing, or end of support period, whichever is later\] | Art 13(13) | \[Date\] |
| Working language | \[Any language; translation plan for authorities\] | Art 13(22) | English; translation on request |
| System of record | \[GRC platform, document-management system or compliance tool with audit trail\] | Evidence governance | \[Tool name\] |
| Legacy design relief | \[Yes or no; scope\] | Guidance pts 37-39 | \[Yes, for design phases before 11 Dec 2027\] |

### Part B: Annex VII index

Document names show illustrative L2 entries. Point 1 is split into 1(a)-1(d) (sub-lettering for this kit; the regulation numbers point 1 as one item).

| Annex VII point | Content required | Document / artefact | Owner | Location (system of record) | Version | Status |
| --- | --- | --- | --- | --- | --- | --- |
| 1(a) | General description, including intended purpose; core functionality (guidance para 144) | Classification record CR-L2-01 (Template 1); product definition record | Product security officer | \[Path\] | \[v\] | \[Draft / Approved / Missing\] |
| 1(b) | Versions of software affecting compliance with essential requirements | Release manifest per firmware and app version | Release manager | \[Path\] | \[v\] | \[ \] |
| 1(c) | For hardware: photographs or illustrations of external features, marking and internal layout | Photo set PH-L2 | Hardware lead | \[Path\] | \[v\] | \[ \] |
| 1(d) | User information and instructions under Annex II | Annex II document (Template 6) and its URL | Technical writing | \[URL\] | \[v\] | \[ \] |
| 2(a) | Design and development: drawings and system architecture showing how software components build on or feed into each other | Architecture document; data-flow diagram DFD-L2 | Engineering lead | \[Path\] | \[v\] | \[ \] |
| 2(b) | Vulnerability handling: SBOM, CVD policy, evidence of the reporting contact address, secure update distribution | SBOM per release; CVD policy (Template 7); security.txt capture; update design note | PSIRT lead | \[Path\] | \[v\] | \[ \] |
| 2(c) | Production and monitoring processes, with validation | Build, signing and release process; gate records | Quality lead | \[Path\] | \[v\] | \[ \] |
| 3 | Cybersecurity risk assessment under Art 13, with Part I applicability and justifications | RA-L2 (Template 2) with change log | Product security officer | \[Path\] | \[v\] | \[ \] |
| 4 | Information used to determine the support period under Art 13(8) | SP-L2-01 (Template 3); version-support register | Product manager | \[Path\] | \[v\] | \[ \] |
| 5 | Harmonised standards, common specifications or certification schemes applied in full or in part; otherwise the solutions adopted | Standards statement, with drafts labelled "draft" | Compliance lead | \[Path\] | \[v\] | \[ \] |
| 6 | Test reports on the product against Annex I Part I | Test reports indexed by requirement | Test lead | \[Path\] | \[v\] | \[ \] |
| 6 | Test reports on vulnerability-handling processes against Annex I Part II | Process audit and PSIRT test records | PSIRT lead | \[Path\] | \[v\] | \[ \] |
| 7 | Copy of the EU declaration of conformity | Declaration (Template 5) | Compliance lead | \[Path\] | \[v\] | \[ \] |
| 8 | SBOM, where applicable, supplied on a market surveillance authority's reasoned request | SBOM annex per version | SBOM owner | \[Path\] | \[v\] | \[ \] |

No harmonised standard is cited in the OJ as of 30 Oct 2026, so point 5 will describe the solutions adopted.

### Part C: family variant list

One file may cover a family sharing architecture, security-relevant design, intended purpose and risks (guidance pts 174-177).

| Variant | Model and SKU | Differences from reference variant | Affected risk-assessment rows | Separate evidence | Declared end of support |
| --- | --- | --- | --- | --- | --- |
| Reference | L2-STD (illustrative) | None | None | Full set | \[Month, year\] |
| \[Variant\] | \[SKU\] | \[Interface, stack, update or connectivity differences\] | \[e.g. 2(i), 2(j)\] | \[Tests\] | \[Month, year\] |

A different update mechanism or remote connectivity usually means a new family, not a variant.

### Part D: obligations around the file

| Obligation | What to record | Basis |
| --- | --- | --- |
| File complete before placing | Date the file was frozen for this version | Art 31; Art 13(12) |
| Kept current | Update log through the support period | Art 31 |
| Retention | Retention end date per placing | Art 13(13) |
| Reasoned request | Named contact; translation route into a language the authority can easily understand | Art 13(22) |
| Legacy relief | Design phases where test evidence is replaced by the risk assessment; Part II evidence still held | Guidance pts 37-39 |
| Publication | Not owed to customers or the public, except FOSS self-attesting under Art 32(5) | Commission FAQ 6.6 |

The simplified Annex VII format for micro and small enterprises (Art 33(5)) depends on an implementing act. None is adopted, drafted or scheduled as of 30 Oct 2026, so build the full file.

## Common mistakes

- Assembling evidence by hand when asked. Emit gate records, SBOM hashes and test results at release and index them here.
- Keeping the file on a shared drive. It needs controlled versions, access management and an audit trail.
- Overwriting the file for a new version. Each placing freezes a set; earlier versions stay retained.
- Calling products a family because they share a brand. An engineer must be able to name the shared security architecture document.
- Leaving the manufacturer-built backend out of points 2(a) and 3.

*Template 4 · v1.0 · 31 Oct 2026 · Not legal advice; confirm wording against the Official Journal text before use.*
