## 1. Purpose and how to run this guide

This guide takes one product or product family from scope decision to EU declaration of conformity, and keeps it compliant through the support period. It is written for product security engineers, tech leads, release and platform engineers and the PSIRT. The knowledge base sections hold the legal detail; this guide holds procedures, patterns, templates and acceptance criteria.

Run it per product or family, in section order. Each section produces one named artefact, and the next section consumes it. Skipping ahead produces evidence nobody can trace to a decision, the failure early adopters report most often (see Engineering compliance programme).

| Section | Artefact produced | Requirement checklist served |
|---|---|---|
| 2 Define the product | Product definition record | 1 scope gate; 10 transition |
| 3 Risk assessment | Art 13 risk assessment with applicability matrix | 2 Annex I Part I; 4 Article 13 |
| 4 Annex I patterns | Control notes and acceptance evidence | 2 Annex I Part I |
| 5 SDLC integration | Release gate records and attestations | 2; 3 Part II; 4 |
| 6 SBOM pipeline | Signed SBOM per release | 3 Part II |
| 7 Secure updates | Update design note and tests | 2; 3 |
| 8 Vulnerability handling | CVD policy, security.txt, case files, advisories | 3 Part II; 4 |
| 9 Open source | Due-diligence records; FOSS determination memo | 3; 4; 9 other operators |
| 10 Reporting runbook | Product reporting data pack | 5 reporting |
| 11 Documentation set | Annex VII file, Annex II document, declaration | 6 Annex II; 7 documentation and declaration |
| 12 Conformity preparation | Evidence index; Module A record or body pack | 8 modules |
| 13 Worked example | Reference walk-through | All |
| 14 Pitfalls | Review list | All |

Three dates frame the work. Art 14 reporting has applied since 11 Sep 2026 to every in-scope product, including products already sold (Art 69(3)). Everything else applies from 11 Dec 2027; earlier products are caught only on substantial modification (Art 69(2)).

No harmonised standard is cited in the OJ and no notified body is designated. This guide therefore relies on [Commission FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307), guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456), ENISA advisories, BSI TR-03183 and draft standards, all non-binding. Drafts and vendor material are labelled as such, and each artefact should record which guidance it followed.

Each section opens with the point it makes, names the knowledge base section that holds the law, then gives the procedure. Tables list items against attributes, numbered lists give sequences, and `- [ ]` lines are acceptance criteria to tick with evidence. Code blocks show a CI step, a file or a document skeleton that can be copied and adapted.

The artefacts map one-to-one onto the Requirement checklists tab. Finish a section, tick its lines there with the artefact reference, and move on. Section 13 walks a fictional smart thermostat through sections 2 to 12; read it first if the shape of the end result is unclear.
