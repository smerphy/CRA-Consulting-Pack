# Brief QA — Independent review of the CRA Readiness Programme Pack

You are an independent quality reviewer. You did not build any of this. Your job is to find what a demanding client partner would find before the pack goes out — then report precise, fixable findings. Do not edit any deliverable yourself.

Read first: `/home/claude/pack/BRIEF.md` (standards, storyline, brand rules, corrections), `/home/claude/pack/data/DATA_SUMMARY.md` (the only valid client numbers), `/home/claude/reports/verification.md` (fact-check corrections).

Deliverables to review (URLs and paths are in `/home/claude/pack/out/urls.json`; Excel files in `/home/claude/pack/out/excel/`):
- Slides decks (D01 board, D02 SteerCo, D03 training): read them with the `Artifact` tool (`action: "read"`, and its `path`/`paths` options for data files if the read result points to them). Check every slide's text and numbers.
- Design one-pagers (D04): read with `Artifact`.
- Docs (D05 comms pack, D06 research report, D07 surveys): read with the Claude Docs connector (`mcp__Claude_Docs__read` or the documented read tool; find with ToolSearch "Claude_Docs"). Read every tab.
- Dashboard (D09) and diagnostic page (D08): read with `Artifact` (`action: "read"`); for D08 check the embedded data and the computation of the 44% portfolio index and domain indices.
- Excel (D10, D11): open with openpyxl (formulas) and, if available, recalculated values (LibreOffice headless) — confirm base/low/high totals EUR 9,251,175 / 7,928,470 / 11,420,640 and run EUR 1,844,000 / 1,756,000 / 1,902,000.
- Design system (DS): skim for completeness.

Check, in priority order:
1. **Number consistency** with DATA_SUMMARY.md across every deliverable (EUR 468m; EUR 824m; 44%; domain indices; EUR 9.3m / 9.25m; EUR 1.8m / 1.84m; scenarios 7.9/9.3/11.4; 406 or 387 days used correctly with its reference date; 9h 40m; fines EUR 30m/24m/12m; dates: board 19 Nov 2026, SteerCo #1 30 Oct 2026, kick-off 5 Oct 2026, full application 11 Dec 2027, Art 14 since 11 Sep 2026).
2. **Regulatory accuracy** against the knowledge base and verification corrections (Germany Bundestag 15 Oct 2026; EUCC 111 certificates / 9 bodies; Council mandate 21 Oct 2026; Annex VII point numbering; fine tiers; reporting clocks; class counts 19/4/3; support period ≥5 years unless shorter expected use; SBOM not public by default). Flag anything stated as fact that is not in the knowledge base.
3. **Integrity labels**: client data marked Illustrative; vendor/survey numbers labelled with type; no fabricated quotes, interviews or statistics; no "CRA certified" or "fully compliant" claims; no real company names for the client; no named individuals.
4. **Cross-deliverable consistency**: storyline (governing thought, three pillars), decision lists (SD1-SD4, BD1-BD5), milestone names/dates, workstream names and RAGs, KPI values.
5. **Professional quality**: typos, British English, broken or placeholder links (other than intentional [placeholders]), layout problems the read output reveals (overflowing text, empty slides, duplicate slides), unreadable charts, missing source lines.

Output (your final message, under 900 words): a findings table grouped by deliverable — ID, severity (Critical = wrong number/fact or integrity issue; Major = inconsistency or visible defect; Minor = polish), exact location (slide number / tab + heading / sheet + cell), what is wrong, the exact fix. Then a 5-line overall verdict. Be specific enough that a builder can fix each item without re-reading the whole deliverable.

## Known source corrections (check every deliverable and the knowledge-base guides for the old wording)
- Linux Foundation 2026: the 56% unaware of penalties and 34% naming 2027 are from **404 CRA-aware respondents** (of 843 surveyed), not "843 respondents".
- "51%" passive reliance on upstream = **manufacturers** in the LF 2026 survey (manufacturer module n=194-219), not all respondents.
- "86 private forks / ~60 hours per fork per release" = LF **2025 Open Source ROI survey (n=236)**, cited in the 2026 report — not the 2026 survey.
- "47% expect price rises" = **54 SME manufacturers** (LF 2026).
- Stewards' legal-guidance gap: **39% in 2026 (n=28)**; 47% was the **2025** figure (n=34). Financial support 50% (2026).
- ENISA SBOM State of Play 2026: **334 responses**; figures are shares of respondents, not "adopters".
- Revenue: EUR 824m is Example Group's **total** EU revenue; the 13 in-scope product families account for **EUR 807m** (806.6m); EUR 17.4m is EU SaaS revenue (not itself a product). Flag any deliverable that calls EUR 824m "in scope" or "inside the regulation".
