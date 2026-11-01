# The pack's CRA legal claims checked against the Official Journal and the Commission guidance

**Executive answer.** We obtained the authentic texts the pack relies on and checked its legal citations against them by script: the Official Journal text of Regulation (EU) 2024/2847 from the EU Publications Office, and the Commission's own PDF of guidance C(2026) 5252 (27 Jul 2026; 257 points, 67 Examples) with the Commission FAQ v1.4, the ENISA SRP FAQ and Ireland's NCSC guidelines. The base register checks 184 claims in the base pack: 148 (80%) are exact, 26 imprecise, 7 wrong and 3 outside the OJ. No deadline, fine, application date or Annex point number is wrong, but five corrections change what a client would do (single declaration under Art 28(3), notified-body language under Art 31(4), the 2025 fines corrigendum, Art 14(8) timing, and the Art 32(2) scheme limb). The Enterprise register checks 180 claims in the six Enterprise papers and the programme case, including 100 quotations from 69 guidance points and Examples: 151 (84%) are exact, 12 imprecise, 3 cite the wrong point, 5 state what the source does not say, and 9 rest on instruments or facts outside our sources. The main Enterprise error ran through four papers and the knowledge base: the guidance does not make every software version a placing on the market, because versions that are not substantial modifications keep the original placing date (para 15, Example 2). We fixed nine wrong citations in four papers. The eleven substantive corrections were then applied on 1 Nov 2026, including a change to the E1 gate so that retention and certificate checks use the inherited placing date; for the programme case the correction shortens Lumen's exposure to a late certificate. Eight open questions the programme depends on are now set out in a legal positions pack, with a letter to Ireland's NCSC and instructions to counsel. One narrowed: the guidance reads the Art 32(2) scheme limb as needing an Art 27(9) act, so Module A through EUCC is not open to Class I products today.

## The authentic text came from the Publications Office, not from EUR-Lex pages or mirrors

EUR-Lex refused automated access and served only a JavaScript shell, which is why the knowledge base had relied on mirrors (reports/verification.md). The Publications Office content-negotiation endpoint returned CELEX 32024R2847 in English as the 81-page PDF/A-2a edition of 14 Nov 2024 and as XHTML. Every quotation was matched by script against both, and they agree. The Commission guidance, FAQ, ENISA FAQ and NCSC documents were obtained from their publishers and pinned by hash. No mirror text was used for any status. [Appendix A](appendix-method.md) lists every route tried, every source used and the status definitions.

## Four in five base claims are exact, and none of the numbers is wrong

**Exhibit 1. Base claims by source and status**

| Pack source | Claims | Verified | Wording difference | Wrong article/point | Not found | Could not verify |
|---|---|---|---|---|---|---|
| pack_data.json facts F01-F20 and fine tiers | 27 | 18 | 7 | 0 | 0 | 2 |
| 03 Scope (Art 2, Art 3 definitions) | 16 | 15 | 1 | 0 | 0 | 0 |
| 07 Annex I Part I | 22 | 20 | 2 | 0 | 0 | 0 |
| 08 Annex I Part II and Art 13 | 32 | 30 | 2 | 0 | 0 | 0 |
| 09 Reporting (Art 14) | 20 | 16 | 4 | 0 | 0 | 0 |
| 10 Conformity (Arts 28-33, Annexes V-VIII) | 28 | 21 | 4 | 0 | 2 | 1 |
| Compliance Templates Kit (D14) | 31 | 21 | 6 | 2 | 2 | 0 |
| Other KB sections and guides | 8 | 7 | 0 | 0 | 1 | 0 |
| **Total** | **184** | **148 (80%)** | **26 (14%)** | **2 (1%)** | **5 (3%)** | **3 (2%)** |

The core numbers all hold. Art 14 runs on 24 hours, 72 hours and 14 days for actively exploited vulnerabilities, and on 24 hours, 72 hours and one month for severe incidents. Art 64 sets fines of EUR 15m or 2.5%, EUR 10m or 2%, and EUR 5m or 1%. Art 71 gives 11 Jun 2026, 11 Sep 2026 and 11 Dec 2027, and Art 69 gives 11 Jun 2028. Annex III lists 19 Class I and 4 Class II categories and Annex IV lists 3 critical ones. All 13 quotations from Annex I Part I points (2)(a)-(m) and all 8 Part II points are exact.

## Seven base claims are wrong and five corrections change client behaviour

`corrections.md` lists 63 edits in three priorities. The five below change what a client would do; [Appendix B](appendix-findings.md) has every non-verified claim.

**Exhibit 2. Base corrections that change client behaviour**

| ID | Pack claim (abridged) | What the OJ says |
|---|---|---|
| T17, K17 | One declaration, or a dossier of declarations, "may" cover all applicable acts | Art 28(3): "a single EU declaration of conformity shall be drawn up" for all acts. FAQ 6.8 accepts a dossier format for that single declaration |
| K14 | Technical documentation "may be written in any language" | For notified-body procedures it must be in an official language of the body's Member State or one the body accepts (Art 31(4)) |
| PD-N1, F20b | Art 64(10) exempts micro and small enterprises from fines | True only as corrected: the corrigendum of 2 Jul 2025 (OJ L, 2025/90555) changed "paragraphs 3 to 9" to "2 to 9". Cite it, or a reader of the original PDF sees the opposite |
| R12 | Users informed "without undue delay" | Art 14(8) says "in a timely manner", failing which CSIRTs may inform users |
| K01, F07 | Module A for Class I with an "Art 27(9) scheme" | The text says schemes "as referred to in Article 27"; the Art 27(9) reading is the guidance's (footnote 25 to para 148) |

Every open question the knowledge base had flagged is now closed against the OJ text. "Provider" is the authentic Annex V point 3 wording in English, German and French; Module H has no unexpected-visit clause; Art 53 does not mention source code. Eight corrigenda exist, three of which change the English text (Art 64(10), Art 67 and the title). Both lists are in [Appendix B](appendix-findings.md).

## The Enterprise register holds 180 claims; 84% are exact, and one error ran through four papers

Each guidance quotation was checked by script inside the point or Example the paper cites, not anywhere in the document, and the register is not written if any quotation fails.

**Exhibit 3. Enterprise claims by paper and status (as stated on 1 Nov 2026, before correction)**

| Paper | Claims | Verified | Wording difference | Wrong article/point | Not found | Could not verify |
|---|---|---|---|---|---|---|
| E1 evidence-as-code | 34 | 27 | 4 | 1 | 2 | 0 |
| E2 art14-operations | 30 | 27 | 2 | 0 | 0 | 1 |
| E3 portfolio-classification | 38 | 32 | 2 | 1 | 1 | 2 |
| E4 open-source-strategy | 33 | 32 | 1 | 0 | 0 | 0 |
| E5 global-control-set | 16 | 12 | 0 | 0 | 0 | 4 |
| G google-outside-in | 19 | 15 | 1 | 1 | 1 | 1 |
| Programme case | 10 | 6 | 2 | 0 | 1 | 1 |
| **Total** | **180** | **151 (84%)** | **12 (7%)** | **3 (2%)** | **5 (3%)** | **9 (5%)** |

The five "Not found" rows were one error. E1, E3, G and the programme case, following knowledge-base section 03, said the guidance makes every software version a placing on the market. It does not. Para 15 says iterations that are not substantial modifications "do not modify that software's date of placement on the market", and in Example 2 versions 1.0.0 and 1.0.1 "are considered to be placed on the market on 1 January 2028". New placings come from substantial modifications (paras 15, 116, 122) and from distinct variants such as builds for another operating system (para 14).

The consequences are now reflected in the modules. E1's "104,000 placing records a year" are version records, and its gate now runs the retention and certificate checks from the inherited placing date. E3's demand model already drove notified-body work from substantial modifications, not version count, so no figure changed. In the programme case, a version placed before 11 Dec 2027 can keep receiving non-substantial and security updates without a certificate (Art 69(2)), so a late Module H approval blocks Lumen's next substantially modified version, not every release; the model's dates and probabilities do not change.

**Exhibit 4. Non-verified Enterprise claims and what was done**

| Group | Claims | Status | Correction | Done |
|---|---|---|---|---|
| Every software version is a placing | EAC-04, EAC-31, PC-20, GOI-14, PCS-03 | Not found | Non-substantial versions keep the original placing date (para 15, Example 2); platform variants are distinct products (para 14) | Applied 1 Nov 2026 (C-01 to C-04, C-11; C-10 in the knowledge base) |
| Wrong point or provision cited | EAC-03, PC-25, GOI-12 | Wrong article/point | Citation replaced | Fixed in papers (Part A) |
| Misquoted or incomplete citation | EAC-10, EAC-15, A14-14, A14-16, PC-05, PC-12 | Wording difference | Wording or citation aligned with the source | Fixed in papers (Part A) |
| Overstated guidance or law | EAC-06, EAC-08, OSS-09, GOI-17, PCS-01, PCS-05 | Wording difference | Softer wording or added source (pt 111 says "likely"; pt 109 "may qualify"; pts 60-62 cover donations; FAQ 4.5.3 and 7.2 point to a per-unit support floor; 23 languages is a model assumption, not a CRA rule) | Applied 1 Nov 2026 (C-05, C-06, C-08, C-11) |

E6 edited other papers only to fix citations: nine edits in E1, E2, E3 and G, logged in `corrections_enterprise.md` Part A. The substantive corrections in Part B were applied by the module owners, as logged there. The register keeps each claim as first stated, so it remains an audit trail. The guidance pass also softened one base finding: FAQ 6.8 accepts a dossier format for the single declaration, so base claim T17 keeps its OJ status with a softer correction.

## Eight open questions are set out as legal positions, with a letter to Ireland's NCSC and a brief to counsel

Several conclusions rest on draft guidance or on questions no authority has answered. `legal-positions/positions.md` takes each in turn: the question, why it matters in the modules' own figures, the OJ and guidance text, the readings available, a recommended position and fallback, the evidence to hold, and who can confirm. `check_positions.py` checks every quotation (108 matched; 4 from web pages read but not saved).

**Exhibit 5. Positions and who should confirm them**

| Question | Recommended position | Confirm with |
|---|---|---|
| A. One Art 14 notification per product or per vulnerability | One notification may list several products, but operate per product (FO-1) until confirmed | NCSC |
| B. Placing of software versions; continuous delivery | New placing per substantially modified version and per platform variant; record every version and whether it is a new placing | Commission; Irish MSA; counsel |
| C. Art 32(2) scheme limb | Only Art 27(9)-specified schemes, as the guidance says; plan Module H | Commission; counsel |
| D. Steward and manufacturer double filing | Two duties; file both from 11 Dec 2027, cross-referenced, unless NCSC accepts one | NCSC; Commission |
| E. OS in own device versus OS supplied to OEMs | Default for own devices; keep OEM supply to free public source plus a licensed services package | Irish MSA; counsel |
| F. Support-period floor per unit or per type | Per unit, applied as per-cohort end dates | Irish MSA; ADCO; counsel |
| G. FIDO key with a secure element | Class I item 1 by default; Annex IV item 3 if the key is a secure element or smartcard-like device designed to AVA_VAN.4 or higher | Commission; Irish MSA; notified body |
| H. Remote data processing boundary | Consoles out; RDPS is what installed clients call directly | Commission; Irish MSA; counsel |

Ireland's NCSC (CSIRT-IE) is Aldermoor's coordinator CSIRT, but its Guidelines say it "does not provide assistance or guidance in determining product scope or general regulatory applicability". The letter (`legal-positions/letter-to-ncsc.md`) therefore asks only questions A and D and coordinator confirmation for steward filings. No Irish market surveillance authority had been designated on the evidence found to 8 Oct 2026, so the scope and classification questions go to external counsel now (`legal-positions/counsel-brief.md`, opinions due 30 Nov 2026 to 31 Jan 2027) and to the authority once designated.

## Keeping the registers true needs a monthly corrigenda check and an event-driven re-verification

Corrigenda, delegated acts amending the annexes, implementing acts and formal adoption of the guidance will all move the text. `fetch_oj.sh` re-fetches the OJ act, its corrigenda and the Commission documents and prints their hashes. Any new corrigendum, hash change or new act triggers a re-check of the register rows that cite the affected provision, not a full re-read. Three rules keep the registers honest: the source column names the exact OJ edition or corrigendum; every quotation must pass the script check, with guidance quotations inside the point or Example cited; and after a corrigendum its reference must appear wherever the pack states the corrected rule. [Appendix A](appendix-method.md) has the process flow and the trigger table by row and owner.

## Decisions for the executive team

1. **Approve the 16 Priority 1 corrections before any further client issue of the Templates Kit or knowledge base.** Owner: General Counsel (or the content's legal reviewer). Timing: by 8 Nov 2026.
2. **Adopt the Publications Office OJ text in this module as the single legal source of record, pinned by hash, and retire mirror sites as sources for quotations.** Owner: knowledge-base maintainer. Timing: immediately.
3. **Take a counsel position on the Art 32(2) certification-scheme limb.** The question is whether a full-scope EUCC certificate at "substantial", recognised under Art 27(8) before any Art 27(9) act, can open Module A for a Class I product. The pack assumes not, and the Commission guidance agrees (footnote 25 to para 148; para 153). Owner: General Counsel with external counsel (counsel brief, question C). Timing: by 30 Nov 2026, before the Art 27(9) act lands.
4. **Keep the statutory Annex V wording verbatim in every client declaration.** "Provider" stays, the manufacturer's legal name may follow it, and one single declaration covers all applicable EU acts. Owner: compliance lead. Timing: from the next declaration issued.
5. **Run the monthly corrigenda, guidance and implementing-act check and record each run in the register.** Owner: regulatory watch lead. Timing: monthly from 1 Dec 2026.
6. **Confirm the placing-of-versions corrections and send the positions pack out.** Review the applied corrections C-01 to C-11 in E1, E3, E4, G, the programme case and the knowledge base; carry the same correction into the live Templates Kit (Template 3) and re-export the knowledge-base doc; send the NCSC letter; instruct counsel on the eight questions. Owner: General Counsel with the module owners. Timing: review and live-doc edits by 30 Nov 2026; letter by 30 Nov 2026; counsel opinions 30 Nov 2026 to 31 Jan 2027.

## Risks and open questions

- **Art 32(2) interpretation.** The text refers to schemes "as referred to in Article 27" without naming paragraph 9, and Annex VII point 5 mentions Art 27(8) schemes. The guidance applies the scheme limb only to schemes specified by an Art 27(9) act (footnote 25 to para 148; para 153). EUCC does not by itself cover the Annex I Part II process requirements, so the practical outcome is the same. Still open in law; see legal-positions question C.
- **Guidance status.** C(2026) 5252 applies only once formally adopted in all languages; point numbers could move. The register cites the 27 Jul 2026 PDF by hash. If the adopted text treated every version as a placing, the C-01 to C-04 and C-11 corrections would need reversing.
- **No Irish market surveillance authority.** None had been designated on the evidence found to 8 Oct 2026. Answers to the scope questions in the positions pack stay informal until one is.
- **Electronic signature.** The PDF obtained has no embedded signature. Its authenticity rests on retrieval from the Publications Office cellar. Obtain a signed copy through EUR-Lex in a browser if a filing ever depends on it.
- **Coverage.** Sections 04, 05, 06, 11 to 16 and the guides were searched for known error strings, not read sentence by sentence. A repository-wide search for out-of-range article or paragraph numbers found none.
- **Non-English versions.** Statuses are for the English text. Translated declarations and user information should be checked against the corrected language version.
- **Facts outside the OJ.** National acts, the Digital Omnibus, EUCC counts and notified-body status rest on reports/verification.md (30 Oct 2026). ENISA platform facts were re-checked against the ENISA SRP FAQ of 15 Oct 2026. Non-EU instruments in E5 were not re-checked.
- **Art 14(8) timing and Art 53 scope.** An internal user-notice target is good practice but not law. Whether Art 53 reaches source code is interpretation, with Art 63(1)(a) confidentiality as the counterweight.

## Sources

- Regulation (EU) 2024/2847, OJ L, 2024/2847, 20.11.2024, ELI [http://data.europa.eu/eli/reg/2024/2847/oj](http://data.europa.eu/eli/reg/2024/2847/oj); text obtained from the Publications Office cellar via [https://publications.europa.eu/resource/celex/32024R2847](https://publications.europa.eu/resource/celex/32024R2847) (English PDF/A-2a and XHTML; German and French XHTML), retrieved 1 Nov 2026. Local copies: `source/oj_L_202402847EN.pdf`, `source/oj_L_2024_2847_EN.txt`.
- Corrigenda: [OJ L, 2024/90780](http://data.europa.eu/eli/reg/2024/2847/corrigendum/2024-12-05/oj); [OJ L, 2025/90555](http://data.europa.eu/eli/reg/2024/2847/corrigendum/2025-07-02/oj); [OJ L, 2025/90768](http://data.europa.eu/eli/reg/2024/2847/corrigendum/2025-10-03/oj); [OJ L, 2025/90828](http://data.europa.eu/eli/reg/2024/2847/corrigendum/2025-10-17/oj); [OJ L, 2026/90243](http://data.europa.eu/eli/reg/2024/2847/corrigendum/2026-03-25/oj); OJ L, 2026/90148 (SK), 2026/90667 (DE) and 2026/90847 (SL), retrieved from the cellar as CELEX 32024R2847R(05), R(07) and R(08). Local copies of the English corrigenda: `source/corrigendum_R0*_EN_*.txt`.
- [Commission Implementing Regulation (EU) 2025/2392](https://eur-lex.europa.eu/eli/reg_impl/2025/2392/oj/eng), OJ L 1.12.2025; [Commission Delegated Regulation (EU) 2026/339](https://eur-lex.europa.eu/eli/reg_del/2026/339/oj/eng), OJ L 29.4.2026; [Commission Delegated Regulation (EU) 2026/881](https://eur-lex.europa.eu/eli/reg_del/2026/881/oj), OJ L 20.4.2026; [Directive (EU) 2024/2853](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024L2853), OJ L 18.11.2024. All texts were read from the cellar.
- [Council PE-CONS 100/23](https://data.consilium.europa.eu/doc/document/PE-100-2023-INIT/en/pdf), 25 Sep 2024 (attempted; recitals only).
- Knowledge base: reports/sections/03-scope.md, 05-roles.md, 07-annex1-part1.md, 08-annex1-part2.md, 09-reporting.md, 10-conformity.md, 13-interplay.md, 14-enforcement.md, 16-watchlist.md, 17-sources.md; reports/verification.md (claims #15, #17, #20, #23, #24, #28 for facts outside the OJ; addendum 10 for C-10); reports/guides/application/03, 09, 10, 11; reports/guides/corporate/08-evidence.md.
- Pack: pack/data/pack_data.json (facts F01-F20, exposure tiers); pack/engine/build.py; pack/out/hosted/D14-compliance-templates-kit/md/00-10.
- Commission guidance C(2026) 5252 final, [Annex](https://ec.europa.eu/newsroom/dae/redirection/document/131456) and [Communication](https://ec.europa.eu/newsroom/dae/redirection/document/131455), 27 Jul 2026; [Commission news page](https://digital-strategy.ec.europa.eu/en/library/commission-publishes-new-guidance-support-timely-cyber-resilience-act-implementation). Commission FAQ on the CRA v1.4, 4 Sep 2026, [Markdown](https://ec.europa.eu/newsroom/dae/redirection/document/123307) and [PDF](https://ec.europa.eu/newsroom/dae/redirection/document/122331). All retrieved 1 Nov 2026; local copies and hashes in `source/guidance/`.
- [ENISA SRP FAQ](https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp/frequently-asked-questions), updated 15 Oct 2026; [NCSC Ireland CRA page](https://www.ncsc.gov.ie/cra/), 11 Sep 2026; [NCSC National CRA Guidelines v1](https://www.ncsc.gov.ie/pdfs/National_CRA_Guidelines_v1.pdf), 31 Aug 2026.
- Irish designation status: [Government of Ireland press release, 11 Sep 2026](https://www.gov.ie/en/department-of-justice-home-affairs-and-migration/press-releases/cyber-resilience-act-guidelines-published-as-reporting-obligations-come-into-effect/); [Arthur Cox, 8 Oct 2026](https://www.arthurcox.com/knowledge/countdown-to-compliance-the-cyber-resilience-act-reporting-deadline-has-arrived/); [Presencis tracker, 4 Oct 2026](https://cdn.presencis.com/regulations/cra/national/) (secondary, unconfirmed).
- Enterprise papers checked: `../evidence-as-code/paper.md`, `../art14-operations/paper.md`, `../portfolio-classification/paper.md`, `../open-source-strategy/paper.md`, `../global-control-set/paper.md`, `../google-outside-in/paper.md`, `../programme-case/paper.md`.
- Module files: `claims.csv` (184-claim base register), `corrections.md` (63 edits), `claims_enterprise.csv` (180-claim Enterprise register) built and checked by `build_claims_enterprise.py`, `corrections_enterprise.md` (nine citation edits made; eleven substantive corrections, applied 1 Nov 2026), `guidance_index.py` and `source/guidance/C_2026_5252_index.json`, `source/guidance/MANIFEST.csv`, `legal-positions/` checked by `check_positions.py`, `fetch_oj.sh`, `h2t.py`, `check_quotes.py`.

Appendices: [A. Sources, method and maintenance](appendix-method.md); [B. Base-register findings, resolved questions and corrigenda](appendix-findings.md).
