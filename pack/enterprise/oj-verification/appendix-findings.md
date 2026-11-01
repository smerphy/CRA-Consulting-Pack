# Appendix B to E6: base-register findings, resolved questions and corrigenda

This appendix holds the full base-pack findings behind the main paper ([paper.md](paper.md)). The old and new text for every edit is in `corrections.md` (base pack) and `corrections_enterprise.md` (Enterprise papers).

## Every non-verified base claim, with its correction

Eleven minor quotation fixes are grouped in one row.

**Exhibit B1. Non-verified base claims and corrections**

| ID | Pack claim (abridged) | Cited | Status | Correction |
|---|---|---|---|---|
| T17 | Kit: "One declaration, or a dossier of declarations, may cover all applicable acts" | Art 28(3) | Not found | Art 28(3): "a single EU declaration of conformity shall be drawn up" for all acts, each identified with its OJ reference; FAQ 6.8 accepts a dossier format for that single declaration |
| K17 | KB: one declaration "may" cover several acts | Art 28(3) | Wording difference | It is mandatory ("shall") |
| K14 | Technical documentation "may be written in any language" | Art 31(4); 13(22) | Not found | For notified-body procedures the language must be an official language of the body's Member State or one it accepts (Art 31(4)) |
| K11, O08 | Module H pt 4 "unexpected visits" disputed between mirrors | Annex VIII Part IV pt 4 | Not found | Point 4 has only 4.1-4.3: site access, periodic audits, audit report. No unexpected-visit clause |
| T10 | Component inventory basis "recital 58" | Recital 58 | Wrong point | Component due diligence is recital 34 |
| T11 | Guides: recital 58 asks manufacturers to list high-risk supplier dependencies in the risk assessment | Recital 58 | Not found | Recital 58 asks the Commission and market surveillance authorities to weigh non-technical risk factors |
| T15 | Kit: "the regulation numbers [Annex VII] point 1 as one item"; 1(a)-(d) is kit lettering | Annex VII pt 1 | Wrong point | The OJ letters point 1 as (a)-(d); the kit rows already match it |
| R12 | Users informed "without undue delay" | Art 14(8) | Wording difference | No such words; the test is "in a timely manner", failing which CSIRTs may inform users |
| K01, F07 | Module A for Class I only with a cited standard, common specification or "Art 27(9) scheme" | Art 32(2) | Wording difference | Text: schemes "at assurance level at least 'substantial' as referred to in Article 27"; the Art 27(9) reading is interpretation, but it is the guidance's reading (footnote 25 to para 148) |
| F04b, R10 | Severe-incident final report "1 month after the 72h notification" | Art 14(4)(c) | Wording difference | "within one month after the submission of the incident notification under point (b)"; runs from actual submission |
| R06, T24 | AEV final report: "severity and impact; actor; details and date" | Art 14(2)(c) | Wording difference | Point (i) is "a description of the vulnerability, including its severity and impact"; the date is an SRP field |
| F06, PD-T2 | Tier 2 "other obligations (e.g. Arts 18-23, 28, 30-33)" | Art 64(3) | Wording difference | Closed list: Arts 18-23, 28, 30(1)-(4), 31(1)-(4), 32(1)-(3), 33(5), 39, 41, 47, 49, 53; tier 3 is information "in reply to a request" |
| R17 | Stewards under Art 14(1), (3), (8) "to the extent involved in development" | Art 24(3) | Wording difference | Two limbs: 14(1) to the extent involved; 14(3) and (8) only for incidents on steward development infrastructure |
| F19 | Art 27(9) act would let EUCC replace third-party assessment | Art 27(9) | Wording difference | Only certificates at "substantial" or above, and only for the requirements covered |
| F20c | Integrating FOSS "never transfers" the manufacturer's duty | Art 13(5) | Wording difference | Text imposes due diligence; "never transfers" is inference |
| T14 | Support-period evidence mapped to "reasonable user expectations" and "feasibility" | Art 13(8) | Wording difference | These are the OJ's optional factors (similar products; integrated components; operating environment) |
| F15, B02, K16, K08, T18, T25, T12, B32, T21, A16, A21, S16 | Eleven quotations or scope statements that are slightly loose (recital wording, Annex VIII point wording, PLD and Art 69(1) scope, Annex VIII model level, corrigendum count) | Various | Wording difference | Exact text in `claims.csv`; edits in `corrections.md` priorities 2-3 |
| K25 | Accreditation against ISO/IEC 17065 and 17021-1 | None | Could not verify | Not in the CRA text; label as accreditation practice |
| F16, F17 | National acts; Digital Omnibus | None | Could not verify | Outside the OJ text; rely on verification.md #20 and #24 |

Two claims are marked Verified but still need an edit, because they are true only as corrected by a corrigendum. As published, Art 64(10) exempted micro and small enterprises (point a) and open-source stewards (point b) from fines under "paragraphs 3 to 9". That left the Art 64(2) tier, which covers Art 14, untouched, and so made point (a) ineffective. The corrigendum in OJ L, 2025/90555 of 2 Jul 2025 reads "paragraphs 2 to 9". The pack's statements (PD-N1, F20b) are right today, but they should cite the corrigendum. Anyone reading the original OJ PDF will otherwise see the opposite.

## Every open question the knowledge base flagged is now closed

**Exhibit B2. Resolution of known open questions**

| Question | OJ text | Resolution |
|---|---|---|
| Annex V point 3: "provider" or "manufacturer"? | "A statement that the EU declaration of conformity is issued under the sole responsibility of the provider" | "Provider" is the authentic English text. German ("Anbieter") and French ("fournisseur") match, and no corrigendum changes it. Keep the word verbatim in declarations; adding the manufacturer's legal name after it is acceptable. Art 28(4) still makes the manufacturer responsible. Remove the "confirm the OJ wording" caveats in D14 Template 5. |
| Art 13 numbering for support-period display and end date | Art 13(8): six subparagraphs. Art 13(19): end date "including at least the month and the year … at the time of purchase"; second subparagraph: end-of-support notification "where technically feasible" | The pack's numbering is correct: period and five-year floor, Art 13(8) second and third subparagraphs; technical file, fifth subparagraph and Annex VII point 4; end date at purchase and in-product notice, Art 13(19) first and second subparagraphs; user information, Annex II point 7. |
| Annex VII point 1 lettering | "1. a general description … including: (a) its intended purpose; (b) versions of software …; (c) … photographs or illustrations …; (d) user information and instructions as set out in Annex II" | The OJ letters point 1 as (a)-(d). Template 4's rows are right; its note saying otherwise is wrong (T15). |
| Art 14 final-report clocks | 14(2)(c): "no later than 14 days after a corrective or mitigating measure is available". 14(4)(c): "within one month after the submission of the incident notification under point (b)" | Both clocks are as the pack states. The incident clock runs from actual submission of the 72-hour-stage notification, so an early filing starts it early. Both final reports, and the 72-hour notifications, are owed "unless the relevant information has already been provided". |
| Art 3(30) wording | "a change to the product with digital elements following its placing on the market, which affects the compliance … with the essential cybersecurity requirements set out in Part I of Annex I or which results in a modification to the intended purpose for which the product … has been assessed" | The pack's paraphrase is accurate. Template 10 can quote it (corrections.md, priority 3). |
| Module H unexpected visits (16-watchlist) | Annex VIII Part IV point 4 has 4.1-4.3 only | No unexpected-visit clause. Close the watchlist item. |
| Art 53 and source code (14-enforcement; 16-watchlist) | Art 53 is a single paragraph: access to "the data … required to assess the design, development, production and vulnerability handling … including related internal documentation" | No source-code wording. Source code appears only in the Art 63(1)(a) confidentiality duty. Whether design data includes source code remains interpretation. |
| Art 66 point number (13-interplay) | "In Annex I to Regulation (EU) 2019/1020, the following point is added: '72." | Point 72. Art 67 also adds point 72 to Annex I of Directive 2020/1828, as corrected on 17 Oct 2025. |

## Eight corrigenda exist, and three change the English text

Corrigenda apply only to the language versions they name. Five of the eight correct other languages and leave the English text unchanged. They matter to a multinational only where a local-language version is relied on, for example in a declaration translated under Art 28(2).

**Exhibit B3. Corrigenda to Regulation (EU) 2024/2847 found on 1 Nov 2026**

| No. | OJ reference and date | Language | What it corrects |
|---|---|---|---|
| R(01) | OJ L, 2024/90780, 5.12.2024 | English | Title: "(EU) No 2019/1020" becomes "(EU) 2019/1020" |
| R(02) | OJ L, 2025/90555, 2.7.2025 | English | Art 64(10): derogation from "paragraphs 2 to 9", not "3 to 9" |
| R(03) | OJ L, 2025/90768, 3.10.2025 | French | Annex I Part I (2)(c) grammar |
| R(04) | OJ L, 2025/90828, 17.10.2025 | English | Art 67: the CRA is point "72.", not "69.", of Annex I to Directive 2020/1828 |
| R(05) | OJ L, 2026/90148, 23.2.2026 | Slovak | Art 14(6) and other points |
| R(06) | OJ L, 2026/90243, 25.3.2026 | French | Annex III Class I point 6: "systèmes de gestion de réseau" |
| R(07) | OJ L, 2026/90667, 6.8.2026 | German | Art 7(2)(b) and other points |
| R(08) | OJ L, 2026/90847, 9.10.2026 | Slovenian | Art 3(17), Art 14(7) third subparagraph (c) and other points |

The knowledge base recorded only R(04), and its watchlist listed R(08) as unverified from a vendor feed. Both are now confirmed.

## Sources

As listed in the main paper's Sources section; corrigenda links and local copies are given there.
