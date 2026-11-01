# Corrections to the Enterprise papers from the extended verification (E6, 1 Nov 2026)

Scope: the six Enterprise papers (E1 evidence-as-code, E2 art14-operations, E3 portfolio-classification, E4 open-source-strategy, E5 global-control-set, G google-outside-in) and the programme case (`programme-case/paper.md`), which appeared during this verification. The programme case needed no citation fix; its corrections are C-11. Claim IDs refer to `claims_enterprise.csv`. Legal sources: OJ L, 2024/2847 with the English corrigenda; Commission guidance C(2026) 5252 annex (Commission PDF, 27 Jul 2026); Commission FAQ v1.4; ENISA SRP FAQ of 15 Oct 2026; NCSC Ireland CRA page and Guidelines; Implementing Regulation (EU) 2025/2392; Directive (EU) 2024/2853. All copies are in `source/` and `source/guidance/` with hashes in `source/guidance/MANIFEST.csv`.

## Part A. Citation edits made (applied to the papers on 1 Nov 2026)

E6 was permitted to edit other modules' papers only to fix a citation. Nine edits were made in four papers (E1 three, E2 two, E3 three, G one). Each old string occurred once. E4 and E5 needed none.

| # | File | Claim | Old text | New text | Reason |
|---|---|---|---|---|---|
| A1 | evidence-as-code/paper.md | EAC-03 | `(guidance paras 13-14; reports/sections/03-scope.md)` | `(guidance paras 13-15 and Example 2; reports/sections/03-scope.md)` | The no-reset rule for non-substantial versions is para 15 and Example 2 |
| A2 | evidence-as-code/paper.md | EAC-15 | `Art 3(21); guidance paras 13-14 (reports/sections/03-scope.md); pt 116` | `Art 3(21); guidance paras 13-15 and Example 2 (reports/sections/03-scope.md); pt 116` | As A1 |
| A3 | evidence-as-code/paper.md | EAC-10 | `(FAQ 6.8)` in the "Three rules" table | `(Art 28(2); FAQ 6.8)` | FAQ 6.8 says only "might need"; the binding rule is Art 28(2) |
| A4 | portfolio-classification/paper.md | PC-05 | `(pts 142-143; 06-classification.md)` | `(pts 139, 142-143; 06-classification.md)` | The list of sources (instructions, marketing, documentation) is para 139 |
| A5 | portfolio-classification/paper.md | PC-25 | `Default (Example 58; FAQ s.3; guidance Example 8)` | `Default (Example 58; FAQ s.3; guidance para 141)` | Example 8 is a printer and its drivers; para 141 is the integration rule |
| A6 | portfolio-classification/paper.md | PC-12 | `is an open interpretation (module E6).` | `is an open interpretation (module E6; the Commission guidance reads the scheme limb as needing an Art 27(9) act, guidance para 148 footnote 25).` | Adds the guidance text that now addresses the question |
| A7 | google-outside-in/paper.md | GOI-12 | `Art 13(6) and Annex I Part II(4) public disclosure of fixed vulnerabilities` | `Annex I Part II(4) public disclosure of fixed vulnerabilities` | Art 13(6) is upstream reporting to a component maintainer |
| A8 | art14-operations/paper.md | A14-14 | `Ireland's National CRA Guidelines describe the detailed notification as due "within 48 hours of the early warning".` | `Ireland's NCSC describes the detailed notification as due "within 48 hours of the Early Warning submission" (NCSC CRA page; the National CRA Guidelines say "within 48hrs of the EW submission").` | Quotation did not match the Guidelines |
| A9 | art14-operations/paper.md | A14-16 | `A wrong choice of coordinator "may invalidate the notification" (FAQ 18)` | `A notification sent to the wrong coordinator "may be invalidated" (FAQ 18)` | Quotation did not match ENISA's wording |

A3, A8 and A9 correct what a citation or quotation attributes to a source; the substance of each sentence is unchanged.

## Part B. Substantive corrections proposed to module owners (not applied)

These change what a sentence asserts, so E6 has not edited them.

### C-01 (Priority 1) E1 executive answer and "Three rules" table: placing per version

Claims EAC-04. The guidance does not make every software version a placing. Para 15: iterations that are not substantial modifications "do not modify that software's date of placement on the market". Example 2: versions 1.0.0 and 1.0.1 (non-substantial) "are considered to be placed on the market on 1 January 2028". New placings arise from a substantial modification (paras 15, 116, 122) or a distinct variant, such as a build for another operating system (para 14).

Old (executive answer): `Under the Commission's draft guidance (not the Regulation's text), placing on the market is judged per version for standalone software. Every placing needs an Annex VII file, a declaration link and a substantial-modification decision.`

New: `Under the Commission's draft guidance (not the Regulation's text), a standalone software version is placed on the market at its first offering, and later versions keep that date unless they substantially modify the product; separate builds for different platforms are separate products (paras 13-15, Example 2). Every version still needs an up-to-date Annex VII file, a declaration link and a recorded substantial-modification decision.`

Old (table, effect column): `Each new Lumen Browser, Lumen OS or app version is its own placing event with a date that must be provable. At about 2,000 EU-relevant versions a week (estimate), that is about 104,000 placing records a year`

New: `Each new version needs a record that shows whether it is a new placing (substantial modification or new variant) or an update to a placed product, with the placing date it inherits. At about 2,000 EU-relevant versions a week (estimate), that is about 104,000 version records a year`

Effect on the design: none on the schema, which already has the event type "update to placed product". The retention calculator should use the inherited placing date where it is earlier; using the version date, as now, gives a later retain-until date, so the current output errs on the safe side.

### C-02 (Priority 1) E1 Risks bullet 4

Claim EAC-31. Old: `Guidance paras 13-14 make each software version a placing, while non-substantial updates "do not reset" the placing date (reports/sections/03-scope.md). Whether every security point release is a new placing is not settled. Recording every version is the conservative choice and costs little.`

New: `Guidance paras 13-15 and Example 2 fix the placing date at the first offering of a version and keep it for later versions that are not substantially modified; only substantially modified versions and distinct variants are new placings. A security point release is normally not a new placing (para 108). Recording every version is still required for documentation and costs little. See legal-positions question B.`

### C-03 (Priority 2) E3 "Version discipline" paragraph

Claim PC-20. Old: `Under Commission guidance (paras 13-14; guidance, not the Regulation's text), placing on the market is per version for standalone software, but security updates are "generally not" substantial modifications (pt 108).`

New: `Under Commission guidance (paras 13-15 and Example 2; guidance, not the Regulation's text), a software version that is not a substantial modification keeps the original placing date, and security updates are "generally not" substantial modifications (pt 108).`

### C-04 (Priority 2) G section 4

Claim GOI-14. Old: `Under Commission guidance (not the Regulation's text), each software version is a separate placing on the market (KB 03-scope.md).`

New: `Under Commission guidance (not the Regulation's text), a substantially modified version is a new placing, while other versions keep the original placing date (paras 13-15, Example 2).`

### C-05 (Priority 2) E1 "Three rules" table, row 2

Claims EAC-06, EAC-08. Old: `All negative means not substantial (pts 111-112).` New: `All negative indicates the update is likely not substantial, provided the risk-assessment assumptions still hold (pt 111).` Old: `Changes of intended purpose or material boundary or dependency changes are (pt 109).` New: `Changes of intended purpose, or boundary or dependency changes not foreseen in the risk assessment, may be (pt 109).`

### C-06 (Priority 3) E4 Exhibit 1, row 5

Claim OSS-09. Points 60-62 concern donations. Replace `Donations or membership that gate access` with `Donations that gate access`, and add a row note: membership fees paid to a not-for-profit steward do not make it a manufacturer (para 66, Example 33).

### C-07 (Priority 3) E4 Exhibit 2, engineering-support row

Claim OSS-17. Add after "not a steward duty": `(guidance para 82 nonetheless describes informing users as "required" where the steward has a direct relationship with them; follow it as practice)`.

### C-08 (Priority 2) G Exhibit 5 and Risks: support-period floor

Claim GOI-17. The sources do address the point in part. Commission FAQ 4.5.3 says that for "units of that product that are newly placed on the market, manufacturers are required to set the support period", and gives an example of later units of the same model needing a support period set under Art 13(8); FAQ 7.2 says the CRA applies to individual products, not types. Replace `Whether the floor runs per unit is not settled in the KB` and the matching Risks bullet with: `The Commission FAQ (4.5.3, 7.2) points to a per-unit reading: units placed later need their own support period under Art 13(8). Not settled by the Regulation's text; see legal-positions question F.`

### C-09 (Priority 3) E3 rule 5 (Tensile LTS)

Claim PC-10. Add: `If LTS source code is shared only with paying customers, the LTS build is not FOSS at all (guidance para 46), so the Art 32(5) route would not be open to it.`

### C-10 (Priority 1, knowledge base) Source of C-01 to C-04

`reports/sections/03-scope.md` line 21 (`Judged per unit; for standalone software, per version (guidance paras 13-14)`) and line 67 (`Placing on the market is per unit, and for standalone software per version.`) are ambiguous and led three modules to the wrong inference. `reports/guides/application/11-documentation-set.md` line 71 (`For software it is the first offering of each version (guidance paras 11-16)`) is wrong for non-substantial versions. Proposed text for all three: `Judged per unit. For standalone software, all copies of a version are placed at its first offering; later versions keep that date unless they are a substantial modification, and builds for different platforms are distinct products (guidance paras 11, 13-15, Examples 1-2).`

### C-11 (Priority 1) Programme case, lever L2 and Risks

Claims PCS-03, PCS-05, PCS-01. Old (L2): `Lumen carries 62% of notified-body revenue (E3) and, as software, cannot bridge the deadline with stock: each new version after 11 Dec 2027 is a new placing under the Commission's draft guidance (E1).`

New: `Lumen carries 62% of notified-body revenue (E3). Under the Commission's draft guidance only substantially modified versions are new placings (paras 15, 108, Example 2), so a version placed before 11 Dec 2027 can keep receiving non-substantial and security updates without a certificate (Art 69(2)). A late certificate therefore blocks Lumen's next substantially modified version, which at a 4-weekly major cadence may come within weeks.`

Old (Risks): `If every Lumen security release is a new placing after 11 Dec 2027, a late certificate stops EU releases, not just launches.` New: `The guidance treats security releases as updates, not new placings (paras 15, 108); if the adopted guidance or an authority took the opposite view, a late certificate would stop EU releases, not just launches.`

Old (budget bullet): `translations into 23 languages (Art 28; Art 13(18))`. New: `translations into the languages each Member State requires for the declaration (Art 28(2)) and that users there easily understand (Art 13(18)); the model assumes all 23 non-English official languages`.

Effect on the model: the Lumen ready-date and probability results do not change, because they are driven by the Module H approval date; what changes is the consequence of missing it (exposure limited to substantially modified versions).

## Part C. Change to the base register

`claims.csv` row T17 (Templates Kit, "dossier of declarations"): status unchanged (Not found against Art 28(3)), but the correction now records that Commission FAQ 6.8 accepts a dossier format for the single declaration. `corrections.md` item 1.5 carries the same note.
