# MASTER BRIEF — CRA Readiness Programme Pack (v1.0, 31 Oct 2026)

Read this whole file first, then `/home/claude/pack/data/DATA_SUMMARY.md`, then your own brief in `/home/claude/pack/briefs/`.

## 1. What we are building

A consulting-grade, white-label **EU Cyber Resilience Act Readiness Programme Pack**: the full set of deliverables a top-tier management consultancy (McKinsey / BCG / Deloitte standard) would hand a client during a CRA readiness engagement — board deck, steering-committee management update, communication pack, research report, survey instruments, a live readiness diagnostic, a business-case model, a programme tracker, a KPI dashboard, a training deck and a one-page visual.

The owner is an independent security and GRC consultant who will reuse the pack with real clients. To show the pack working, every deliverable is populated with one **illustrative engagement**:

- Client: **Example Group** — a fictional German-headquartered maker of connected products (EUR 1.2bn revenue). Always label client numbers *Illustrative*. Never use a real company name for the client and never name individuals — use roles (CTO, General Counsel, PSIRT lead…).
- Programme code name: **Project Rampart**. Kick-off 5 Oct 2026; SteerCo #1 held 30 Oct 2026; board meeting 19 Nov 2026.
- Advisor placeholder: `[Advisor]` (only where a consultancy name would appear, e.g. "Prepared by [Advisor]").

Quality bar: the reader should say "wow". That means: pyramid principle, an action title on every slide/section that states the so-what, one message per exhibit, crisp visuals, every number traceable to a source, zero filler, zero hedging prose, British English, impeccable consistency across the pack.

## 2. Sources of truth (precedence order)

1. **Client numbers**: `/home/claude/pack/data/pack_data.json` (machine-readable) and `DATA_SUMMARY.md` (readable). Use these exact numbers. If you need a number that is not there, derive it transparently from them or label it an assumption — and list it in your final report.
2. **Regulatory facts**: the knowledge base built for this engagement (published as the Claude Doc "EU Cyber Resilience Act — Engineering Compliance Knowledge Base", https://claude.ai/artifact/JC24c3EC3qR8Xz8k3858Wj). Local copies:
   - `/home/claude/reports/sections/*.md` — 16 knowledge-base sections (law, guidance, standards, reporting, conformity, open source, interplay, enforcement, programme, watchlist, sources).
   - `/home/claude/reports/guides/corporate/*.md` and `/home/claude/reports/guides/application/*.md` — corporate and application implementation guides.
   - `/home/claude/reports/verification.md` — independent fact-check; **its corrections override the section files**.
   - `/home/claude/reports/digest.md` and `/home/claude/research_notes/EU CRA engineering compliance/*.md` — deeper research notes (surveys, vendor material, URLs).
3. Known corrections to apply everywhere (local files may still show the old text):
   - Germany's CRA implementation law passed the **Bundestag plenary on 15 Oct 2026** (committee 14 Oct); promulgation pending.
   - EUCC: **111 valid certificates from 9 certification bodies** on 30 Oct 2026.
   - Digital Omnibus: Council mandate agreed by Coreper **21 Oct 2026** (ST 14756/26, circulated 22 Oct).
   - Annex VII: point 3 = risk assessment; point 4 = support-period information; point 5 = standards applied; point 6 = test reports.
4. Facts are verified **to 30 Oct 2026**. Say so where status matters ("as at 30 Oct 2026").
5. Do not add new regulatory claims that are not in the knowledge base. If you must, verify with a web search, cite the URL, and flag it in your report. Label vendor statements, commentary and survey data as such (e.g. "vendor estimate, unverified").
6. Do not reproduce long verbatim passages from sources; paraphrase and cite. Short quotes (under 15 words) are fine.

## 3. Storyline (every deliverable must be consistent with it)

**Governing thought:** The CRA turns product cybersecurity into a licence to sell in the EU. Example Group can be ready by 11 Dec 2027, but only if it secures third-party assessment capacity and builds shared compliance infrastructure in the next two quarters.

- **Situation:** CRA (Regulation (EU) 2024/2847) in force since 10 Dec 2024; Art 14 reporting applies since 11 Sep 2026 to every in-scope product, including those already sold; everything else from 11 Dec 2027.
- **Complication:** reporting is already live on a 24-hour clock; seven of thirteen families (EUR 468m of EU revenue) need a notified body or a cited harmonised standard and neither exists today; compliance must be evidenced per product version for ten years.
- **Question:** What must Example Group do, by when and at what cost, to keep selling in the EU after 11 Dec 2027?
- **Answer:** a 14-month, three-wave programme (Project Rampart): build shared capabilities once (PSIRT, SBOM, secure updates, evidence system), apply them per product, lock in notified-body capacity by Q1 2027. About EUR 9.3m to Dec 2027 and EUR 1.8m a year to run. Five board decisions on 19 Nov 2026.

Three pillars: (1) Reporting is already law. (2) Market access is the binding constraint. (3) Compliance is an evidence system, not a project.

Headline numbers (from the data — do not round differently): 406 days from 31 Oct 2026 to 11 Dec 2027 (387 from the 19 Nov board); EU revenue EUR 824m in total, of which EUR 807m from the 13 in-scope product families; EUR 468m of EU revenue needs a notified body (39% of group revenue); baseline readiness index 44%; Class I home products least ready (L2 35%, V1 38%); domain readiness: Art 14 reporting 72% (best), documentation 24%, conformity & market access 16% (worst); investment EUR 9.25m one-off (show as EUR 9.3m) incl. 15% contingency, EUR 1.84m a year run (EUR 1.8m); scenarios EUR 7.9m / 9.3m / 11.4m; 0.77% of one year's revenue; max fine EUR 30m (2.5% of EUR 1.2bn); first drill filed an early warning in 9h 40m; programme RAG Amber.

## 4. Brand and style (white-label "Advisory Design System")

- Fonts: **Source Serif 4** (display/headings), **Inter** (body, UI, tables), **JetBrains Mono** (code, IDs). Google Fonts.
- Colours: ink-900 `#0E1A2B` (primary text, dark backgrounds), ink-700 `#26364D`, ink-500 `#56667E` (secondary text), ink-300 `#C5CDD8` (rules/borders), ink-100 `#EEF1F5` (fills), paper `#FAFAF7` (page background), surface `#FFFFFF`; accent-700 `#0A5753`, **accent-600 `#0F6E6A`** (brand teal — emphasis, key numbers), accent-400 `#2E9C93`, accent-100 `#DCEFEC` (tints); **signal `#C2410C`** (use only for the binding constraint / critical callouts); RAG red `#B42318`, amber `#B54708`, green `#027A48`, grey `#8A94A6`.
- Data-viz categorical order: `#0F6E6A`, `#1F3A5F`, `#5B8DB8`, `#C9A66B`, `#B9573E`, `#8A94A6`. Maturity heatmap 0-4: `#B42318`, `#E07A5F`, `#E9C46A`, `#7FB8A4`, `#0F6E6A` (always print the number in the cell; never rely on colour alone).
- Consulting conventions: action titles (full sentence, the so-what, ≤ ~15 words); tracker/section label top-left; source line bottom-left on every data exhibit ("Source: … ; Illustrative"); exhibit numbers in documents; footers carry "Project Rampart · Illustrative · 31 Oct 2026" (adapt per deliverable).
- Numbers: EUR 9.3m, EUR 210k, 44%, 9h 40m; dates as 11 Dec 2027; ranges with en dash or "to".
- Tone: calm, exact, decision-oriented. No emoji, no clip art, no stock photos, no exclamation marks. Simple line icons only if they add meaning.
- A design-system artifact will exist for decks and visuals; the coordinator will tell slide/design builders its URL.

## 5. The pack (IDs used for cross-references)

| ID | Deliverable | Format | Primary audience |
|---|---|---|---|
| DS | Advisory Design System (white-label) | Design System artifact | All builders; consultant's future work |
| D01 | Board briefing deck — "Keeping our EU market open" | Slides | Board, ExCo |
| D02 | Steering Committee #1 pack — management update | Slides | Programme SteerCo |
| D03 | CRA for engineers and product teams — training deck | Slides | Engineers, PMs, PSIRT |
| D04 | CRA on a page / Project Rampart on a page | Design (one-page visuals) | Everyone |
| D05 | Communication pack | Claude Doc | Sponsor, comms, BU leaders |
| D06 | Research report — State of CRA readiness 2026 | Claude Doc | Executives, strategy |
| D07 | Survey and interview instruments | Claude Doc | Programme team, research |
| D08 | CRA Readiness Diagnostic (live, multi-respondent) | Hand-built web page with shared database | Product teams, programme |
| D09 | Programme dashboard | Dashboard artifact | Sponsor, SteerCo |
| D10 | Business case and cost model | Excel workbook (.xlsx) | CFO, sponsor |
| D11 | Obligations register and programme tracker | Excel workbook (.xlsx) | PMO, compliance |
| D12 | Delivery portal (front door) | Hand-built page (coordinator builds) | Client and consultant |
| KB | Engineering compliance knowledge base (exists) | Claude Doc | Engineering, compliance |

Refer to other deliverables by their name (e.g. "see the Communication Pack (D05)"). Do not invent URLs for them; the portal links everything.

## 6. Rules for every builder

- Build only your deliverable. Do not edit other deliverables or the knowledge base.
- Typed artifacts (Slides, Docs, Dashboard, Design, Design System): first call `Artifact` with `action: "quickstart"` (intent per your brief) or publish directly with the type_url you are given; when creating from a type pass `auto_open: "after_first_write"` (except Docs, which are written through the Claude Docs connector — omit auto_open). Follow the type's returned instructions exactly. **Never call `Artifact` with `action: "open"`**, never pin, never delete anything.
- Gather and draft your material before creating a typed artifact (Docs are the exception: create the doc skeleton first, then fill it).
- Build in stages for long outputs. Check your work at the end: read it back or take a screenshot through the type's read/preview facility, fix layout overflow, typos, number mismatches against DATA_SUMMARY.md, and broken links.
- Keep everything white-label: no consultancy logos; "[Advisor]" placeholder only where needed; client is "Example Group (illustrative)".
- Accessibility: sufficient contrast, numbers printed on colour-coded cells, alt text where the format supports it.
- Your final message (your report back to the coordinator) must contain: the artifact URL(s) or file path(s); the exact title; a 5-line summary of what is inside; any number you had to assume or derive; any fact not found in the knowledge base (with URL); known limitations. Keep it under 300 words.
