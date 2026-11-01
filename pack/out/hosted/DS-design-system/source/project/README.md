A white-label system for consulting deliverables: board and steering-committee decks, training decks, one-page visuals, reports, survey instruments, dashboards, workbooks and small web tools. It should read like a premium advisory firm with no logo on it — calm ink-navy on warm paper, one confident teal accent, a single signal orange kept for the binding constraint, and disciplined RAG colours that only ever mean status. Every rule below exists so that a busy reader can trust each number and act on it.

Read this page first, then the card of every component you use: `project/components/<Name>/README.md` holds its rules and paste-ready markup, and `preview.html` beside it is the reference rendering.

## Build with it

| You are building | Do this |
|---|---|
| **A Slides deck** | Install this system (its `tokens.json` → `project/ds/advisory/tokens.json`, namespace folder `advisory`) and add the three `faces` below. Start every slide from a **Slide masters** component: copy its `<section>`, keep every position and size, change the words. Slides take inline hex only, so use the hex values in the colour tables. |
| **A Design canvas** (one-pagers, posters) | Install the same way. There is no component bundle to mount: copy the markup of the components you need into the artboard and convert classes to inline styles with the token values. Lay one-pagers on the 12-column grid. |
| **A Claude Doc** | Apply the system through structure, not styling: the heading hierarchy (**Headings**), action headings, numbered exhibits with source lines (**ExhibitCaption**), the five callout labels (**Callout**), tables per **DataTable**, footnotes per **Footnote**. The Docs type owns fonts and colours. |
| **A Dashboard** | Series colours `viz-1` … `viz-6` in that order; status with `rag-*` plus the word; KPI tiles per **KpiTile**; heatmaps per **HeatmapCell**; every number with its source. |
| **A hand-built HTML page** | Paste the token block from **Web: CSS variables and dark mode**, then copy `project/components/bundle.css` (all component classes, prefix `adv-`; it also loads the fonts). Use semantic tokens (`bg-*`, `text-*`, `rule*`, `action*`) so the page follows light and dark. |
| **An Excel workbook** | Follow **Spreadsheets** below. |

**Fonts** — Google Fonts, one stylesheet for all three families:
`https://fonts.googleapis.com/css2?family=Inter:wght@400..700&family=JetBrains+Mono:wght@400..600&family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..700&display=swap`

Slides `faces` entries, keyed exactly so:

```json
"source-serif-4": {"family": "Source Serif 4", "href": "https://fonts.googleapis.com/css2?family=Source+Serif+4:ital,opsz,wght@0,8..60,400..700;1,8..60,400..700&display=swap"},
"inter": {"family": "Inter", "href": "https://fonts.googleapis.com/css2?family=Inter:wght@400..700&display=swap"},
"jetbrains-mono": {"family": "JetBrains Mono", "href": "https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400..600&display=swap"}
```

Stacks: `'Source Serif 4', Georgia, serif` · `Inter, Arial, sans-serif` · `'JetBrains Mono', 'Courier New', monospace`. In CSS they are `--font-serif`, `--font-sans`, `--font-mono`.

## Content fundamentals

### Structure: lead with the answer

- Open every deliverable with its governing thought in one sentence, then its three supporting pillars, then the evidence (pyramid principle). Readers who stop after the first page must still leave with the answer.
- Use situation, complication, question, answer only in the executive summary; everywhere else, the answer comes first.
- One message per slide, section or exhibit. If a slide needs two titles, it is two slides.
- Every recommendation ends in a decision, an owner (a role) and a date.

### Action titles

- Every slide and every document section carries an action title: one full sentence stating the so-what, at most about 15 words, sentence case, no full stop, max two lines.
- Write it last: read the exhibit, ask "so what?", put the answer and its number in the title. The title must be true of the exhibit beneath it.

| Topic label (don't) | Action title (do) |
|---|---|
| Readiness by domain | Conformity and market access is the least ready domain, at 16% |
| Programme costs | Readiness costs EUR 9.3m to Dec 2027, 0.77% of one year's revenue |
| Reporting update | The first drill filed an early warning in 9h 40m, well inside 24 hours |
| Notified bodies | No notified body is designated yet, so capacity must be booked now |

### Labels, sources and evidence

- **Tracker label** top-left on every content slide and above every document section: section number and name, e.g. "02 · Market access" (set uppercase by the style).
- **Source line** bottom-left under every exhibit that shows data: `Source: <source>, <date>; <second source>; Illustrative`. Name survey and vendor data with their type and base: `Source: ONEKEY IoT/OT Cybersecurity Report 2026 (vendor survey, n = 200)`.
- **Illustrative**: label every client number "Illustrative" in its source line or caption, and keep "Illustrative" in the footer of every page of an illustrative engagement.
- **Unverified material**: label it in words — "vendor estimate, unverified", "commentary, unverified" — and use the Draft / unverified callout for anything awaiting a check.
- **Status facts carry a date**: "No CRA notified body was designated (at checks to 8 Sep 2026)."
- **Exhibits are numbered** in documents ("Exhibit 3 — …"); slides are not.

### Numbers, dates and words

| Thing | Write | Never |
|---|---|---|
| Money | EUR 9.3m · EUR 210k · EUR 1.2bn | €9.3M · 9.3 million euros · EUR 9,250,000 in prose |
| Percentages | 44% · 0.77% · +6 pp | 44 % · 44 percent |
| Durations | 9h 40m · 24 hours · 14 days | 9:40 hrs |
| Dates | 11 Dec 2027 · Dec 2027 · Q1 2027 | 12/11/2027 · December 11th, 2027 |
| Ranges | EUR 7.9m–11.4m · 2–4 months · Nov 2026 to Nov 2027 | 7.9-11.4 (hyphen) |
| Counts | 3,800 · 11 of 13 · 140 / 920 | 3.800 |
| Law | Art 14(2) · Annex VII point 3 · Regulation (EU) 2024/2847 | Article fourteen |

- Display money at one decimal in millions (EUR 9.25m shows as EUR 9.3m in headlines); keep source precision in tables, and never mix precisions in one exhibit.
- Numbers in tables use tabular figures and align right; units go in the column header ("EUR k"), not in every cell.
- British English: programme, organisation, prioritise, licence (noun), defence, analyse, modelling, centre, fulfil.
- Roles, never names: CTO, General Counsel, PSIRT lead. The client is "Example Group (illustrative)"; the advisor appears only as `[Advisor]`.

### Voice

- Calm, exact, decision-oriented: say what is true, what it means and what to decide.
- No hedging prose, no hype, no exclamation marks, no emoji, no rhetorical questions in titles.
- Recommendations start with a verb and carry a date: "Contract three notified-body pre-assessments by 29 Jan 2027."

## Visual foundations

### Colour

Ground is `paper`; `surface` lifts cards, tiles and tables; text is `ink-900` (titles), `ink-700` (body) and `ink-500` (secondary). Teal is the only accent.

| Token | Hex | Use |
|---|---|---|
| `ink-900` | `#0E1A2B` | Primary text and dark grounds: titles, headings, table text, title and divider slides. 16.7:1 on paper. |
| `ink-700` | `#26364D` | Body copy on paper, surface and ink-100 (11.7:1 on paper); inverse panels in the dark theme. |
| `ink-500` | `#56667E` | Secondary text — source lines, captions, footers, axis labels — on paper (5.6:1), surface (5.8:1) and ink-100 (5.2:1); form-control borders. |
| `ink-300` | `#C5CDD8` | Hairline rules: table rules, card borders, gridlines, dividers. Decorative only: never text, never the only edge of a control. |
| `ink-100` | `#EEF1F5` | Quiet fills: slide table header band, chips, progress tracks, code, the Illustrative-data callout. |
| `paper` | `#FAFAF7` | The ground: page and slide background. Text on it: ink-900, ink-700, ink-500, accent-600, accent-700, signal. |
| `surface` | `#FFFFFF` | Cards, tiles, tables and form fields on paper; text on accent-600, navy and RAG fills. |
| `accent-700` | `#0A5753` | Tracker labels, links, primary-button hover; text on paper (8.0:1) and on accent-100 (7.0:1). |
| `accent-600` | `#0F6E6A` | Brand teal, the one thing to look at: key numbers, the focus series, primary buttons, focus ring. 5.8:1 on paper; white on it 6.1:1. |
| `accent-400` | `#2E9C93` | Emphasis on ink-900 grounds (5.2:1): eyebrows and numerals on title and divider slides; the dark-theme accent. Never text on paper (3.2:1). |
| `accent-100` | `#DCEFEC` | Teal tint: Key insight ground, highlighted rows, current agenda row. Text on it: ink-900, accent-700 (7.0:1) or accent-600 (5.1:1). |
| `signal` | `#C2410C` | Reserved for the binding constraint and critical callouts, at most once per slide or page. 5.0:1 on paper, 5.2:1 on surface; white on it 5.2:1. |
| `signal-100` | `#FFEDD5` | Ground of the Critical callout; signal text on it 4.5:1, ink-900 text 17:1. |
| `rag-red` | `#B42318` | Status Red only (off track, decision needed), always with the word. White text on it 6.6:1; as text on paper 6.3:1. |
| `rag-amber` | `#B54708` | Status Amber only (at risk), always with the word. White text on it 5.4:1; as text on paper 5.2:1. |
| `rag-green` | `#027A48` | Status Green only (on track, complete), always with the word. White text on it 5.4:1; as text on paper 5.2:1. |
| `rag-grey` | `#8A94A6` | Status Grey only (not started, planned), always with the word. ink-900 text on it 5.7:1; never white text (3.1:1). |
| `rag-red-100` | `#FEE4E2` (dark `#4A1D19`) | High-risk zone (score 12-25) of the risk matrix; markers carry the text. |
| `rag-amber-100` | `#FEF0C7` (dark `#4A2A0C`) | Medium-risk zone (score 5-11) of the risk matrix; markers carry the text. |
| `rag-green-100` | `#D1FADF` (dark `#0F3B29`) | Low-risk zone (score 1-4) of the risk matrix; markers carry the text. |
| `heat-0` | `#B42318` | Maturity level 0, Not started. White number on it (6.6:1). |
| `heat-1` | `#E07A5F` | Maturity level 1, Initial. ink-900 number on it (5.9:1). |
| `heat-2` | `#E9C46A` | Maturity level 2, Defined. ink-900 number on it (10.5:1). |
| `heat-3` | `#7FB8A4` | Maturity level 3, Implemented: the target. ink-900 number on it (7.7:1). |
| `heat-4` | `#0F6E6A` | Maturity level 4, Assured. White number on it (6.1:1). |
| `viz-1` | `#0F6E6A` (dark `#2E9C93`) | Series 1 and the focus series (the client, the base case, the bar the title names). Labels inside: text-on-action. |
| `viz-2` | `#1F3A5F` (dark `#8FA9CC`) | Series 2, the main comparator (plan, prior period). Labels inside: text-on-action. |
| `viz-3` | `#5B8DB8` | Series 3. ink-900 labels inside (5.0:1). |
| `viz-4` | `#C9A66B` | Series 4. ink-900 labels inside (7.6:1). |
| `viz-5` | `#B9573E` | Series 5. White labels inside (4.7:1). |
| `viz-6` | `#8A94A6` | Series 6, 'other', and the context grey for non-focus bars (3.1:1 on surface). ink-900 labels inside. |

Rules:
- **Proportion**: paper and surface about 70%, ink about 25%, teal 5% or less. A slide with three teal elements has two too many.
- **Teal marks the one thing to look at**: the key number, the focus series, the primary button. Grey the rest (`viz-6` bars, `ink-500` labels).
- **Signal is scarce**: `signal` appears only for the binding constraint or a critical callout, at most once per slide or page. In this engagement that is notified-body capacity and the EUR 468m of EU revenue it gates.
- **RAG means status and nothing else**: `rag-red`, `rag-amber`, `rag-green`, `rag-grey` always come with the word (Red, Amber, Green, Grey — or On track, At risk, Off track, Not started). Never use them for categories, emphasis or decoration. Risk-matrix zones use the `rag-*-100` tints.
- **Dark slides**: the title slide and section dividers use an `ink-900` ground, `paper` text and `accent-400` emphasis. The one statement slide uses an `accent-600` ground with `paper` text.
- **Maturity heatmaps** use `heat-0` … `heat-4` for levels 0–4 and always print the number.

On the web and in canvases that follow the theme, use the semantic tokens; their dark values implement dark mode (`ink-900` ground, `paper` text, `accent-400` emphasis):

| Token | Light | Dark | Use |
|---|---|---|---|
| `bg-page` | `#FAFAF7` | `#0E1A2B` | Page background on the web. Text on it: text-primary, text-body, text-muted, text-emphasis, text-accent, text-critical, text-danger. |
| `bg-surface` | `#FFFFFF` | `#16243A` | Cards, tiles, tables, inputs and menus on bg-page; the same text tokens as bg-page. |
| `bg-subtle` | `#EEF1F5` | `#1F2E45` | Quiet fills: table header band, chips, progress track, disabled controls, the Illustrative-data callout. Text: text-primary, text-body, text-muted. |
| `bg-emphasis` | `#DCEFEC` | `#123F3D` | Teal tint: Key insight callout, highlighted row, accent tags. Text: text-primary, text-body, text-accent. |
| `bg-inverse` | `#0E1A2B` | `#26364D` | Inverse panels: the Decision required callout, inverse cards, dark bands. Text: text-on-inverse, accent-on-inverse. |
| `bg-critical` | `#FFEDD5` | `#3B1D0F` | Critical callout ground (the binding constraint). Text: text-primary, text-body, text-critical. |
| `text-primary` | `#0E1A2B` | `#FAFAF7` | Titles, headings, labels and table text on bg-page, bg-surface, bg-subtle, bg-emphasis and bg-critical (13:1 or more in both themes). |
| `text-body` | `#26364D` | `#D5DCE6` | Running text on bg-page, bg-surface, bg-subtle and bg-emphasis (10:1 or more in both themes). |
| `text-muted` | `#56667E` | `#A3AFC0` | Secondary text (source lines, captions, hints, axis labels) on bg-page, bg-surface and bg-subtle: 5.2:1 or more light, 6.1:1 or more dark. |
| `text-emphasis` | `#0F6E6A` | `#2E9C93` | Key numbers and emphasised words on bg-page and bg-surface: 5.8:1 light, 4.7:1 dark. Not on bg-emphasis in the dark theme. |
| `text-accent` | `#0A5753` | `#7FD1C7` | Links, eyebrows and callout labels on bg-page, bg-surface and bg-emphasis: 7.0:1 or more light, 6.5:1 or more dark. |
| `text-critical` | `#C2410C` | `#FB923C` | The Critical callout label and the binding-constraint figure on bg-page, bg-surface and bg-critical: 4.5:1 or more light, 6.7:1 or more dark. |
| `text-danger` | `#B42318` | `#F97066` | Form errors and the word 'Blocked', always with words: 6.3:1 on paper light, 5.6:1 or more dark. |
| `text-on-inverse` | `#FAFAF7` | `#FAFAF7` | Text on bg-inverse (16.7:1 light, 11.7:1 dark). |
| `accent-on-inverse` | `#2E9C93` | `#7FD1C7` | Labels and numbers on bg-inverse: 5.2:1 light, 6.9:1 dark. |
| `action` | `#0F6E6A` | `#2E9C93` | Primary button fill, selected scale segment, checked box, progress fill, current-page rule. |
| `action-hover` | `#0A5753` | `#5CB8AF` | Hover and pressed state of action fills. |
| `text-on-action` | `#FFFFFF` | `#0E1A2B` | Text and icons on action and viz-1/viz-2 fills: 6.1:1 light, 5.2:1 dark. |
| `rule` | `#C5CDD8` | `#2C3C55` | Hairlines: table rules, card borders, dividers, gridlines. Decorative only. |
| `rule-strong` | `#56667E` | `#6B7A90` | Control borders (inputs, secondary buttons, scale segments, checkboxes): 3:1 or more on every ground in both themes. |
| `focus` | `#0F6E6A` | `#2E9C93` | Keyboard focus outline, 2px solid with a 2px offset: 5.8:1 on paper, 5.2:1 on ink-900. |

### Typography

- **Source Serif 4** (500) for titles and headings only; **Inter** for everything else, including all numbers; **JetBrains Mono** for IDs (K07, R01, M5, Q10.4, D01) and code. No other families.
- **Numbers** use Inter with tabular figures (`font-variant-numeric: tabular-nums`) in tables, KPI tiles, axes and footers. Section numerals on dividers and agendas are the one serif exception.
- **Slide scale (1920 × 1080)**: 96 display · 56 action title · 32 lead · 28 body · 24 labels, sources, footers, table text. Nothing on a slide is smaller than 24px. KPI values 64; one hero number 200. Styles: `slide-*`.
- **Document and web scale**: 48 / 36 / 28 serif (`display`, `heading-1`, `heading-2`); 20 / 16 sans (`heading-3`, `heading-4`); 16 body; 14 small and tables; 13 exhibit units; 12 eyebrows and source lines.
- **Measure**: running text 60–75 characters per line (`text-measure`, 72ch); action titles max two lines.
- **Emphasis**: weight 600 or `text-emphasis` colour. Underline means a link; italics are for titles of works and quotations.
- **Uppercase** only for tracker labels and eyebrows, tracked 0.08–0.12em (3px on slides).

### Layout and grid

**Slides** (1920 × 1080): 128px margins left, right and top; content box 1664 × 792 (y 128–920); 12 columns of 102px with 40px gutters — a half is 812px, an 8-column exhibit 1096px, a 4-column side panel 528px.

| Zone | Position |
|---|---|
| Tracker label | pinned `left:128px; top:64px` |
| Action title | first flow child at y 128, max 128px (two lines) |
| Body | 48px under the title; `flex:1` |
| Source line | last flow child, ends at y 920 |
| Footer | pinned `left:128px; bottom:64px; width:1664px`: 1px `ink-300` rule, 16px gap, engagement · deliverable · date left, classification · page right |

**Documents and web**: content max 1200px (`page-max-width`) on a 12-column grid with 24px gutters (`page-gutter`); text column max 72ch; at phone width one column with 16px side gutters (`page-gutter-phone`) and no horizontal scroll.

**One-page visuals**: A4 landscape or 1920 × 1080; the slide grid applies; the governing thought is the title; three pillars as three columns; a source band at the foot.

### Spacing

A 4px scale, `space-1` (4px) to `space-10` (128px). Slides use 16 / 24 / 32 / 48 / 64 / 128; web uses 4–64. Space separates groups; rules separate rows.

### Rules, borders, radii, shadows

- Separate with hairlines and white space, not boxes and shadows: 1px `rule` (`ink-300`). A 1px `ink-900` rule sits under table headers and above document exhibits; a 2px `ink-900` rule above totals; a 4px rule tops a slide column heading (2px on the web).
- Radii are small and square-cornered in feel: `radius-sm` 2px (tags, bars, heat cells), `radius-md` 4px (buttons, inputs, callouts, tiles), `radius-lg` 6px (web cards). **Round means status**: `radius-full` is only for RAG pills, status dots, Harvey balls and risk markers.
- No shadows on slides, documents, cards or tiles. `shadow-raised` is for floating web layers (menus, popovers) only.
- No gradients, textures, glows, 3D, or coloured left-border cards.

### Data visualisation

- One message per exhibit: the title states it, the chart proves it, the source line backs it.
- **Focus and context**: draw the series or bar the title names in `viz-1` / `accent-600` (or `signal` if it is the binding constraint) and the rest in `viz-6`. Use the full categorical order `viz-1` … `viz-6` only when every series matters equally, never more than six.
- Label directly: values at bar ends, series names at line ends; a legend only when direct labels do not fit.
- Bars start at zero; sort by value unless categories have a natural order; horizontal bars for long labels.
- Gridlines hairline `rule` or none; axis text `text-muted`; no chart borders, 3D, pies over three slices, or dual axes.
- Targets: dashed 1.5px `ink-900` line labelled "Target 70%". Today: 2px `accent-600` line labelled "Today 31 Oct 2026". Fixed deadlines: dashed `ink-900` with the date.
- Heatmaps print the value in every cell (white on levels 0 and 4, `ink-900` on 1–3). Status columns show the RAG word.

### Motion and interaction (web)

- Transitions 120ms ease on colour and border only; no entrance animations, parallax or auto-play.
- Keyboard focus: a solid 2px `focus` outline with a 2px offset (`focus-ring` where an outline would clip) — at least 3:1 on every ground.
- Hit targets at least 44px tall for primary controls and scale segments; 24px minimum for anything clickable.

## Iconography

- Simple line icons on a 24px grid: 1.5px stroke (`icon-stroke`), round caps and joins, no fills, drawn in `ink-700` or `accent-600` (inline SVG with `stroke="currentColor"`).
- Use an icon only when it adds meaning a word cannot carry alone — a clock for the 24-hour clock, a lock for secure updates, a warning triangle on a critical callout — and always beside a text label. Never decorative, never emoji, never filled or two-tone sets, never two icon styles in one deliverable.
- The **Iconography** component holds the approved set of 18 icons as paste-ready SVG. On slides, use the Slides `<x-icon>` names at 48px or larger: `Clock`, `Warning`, `CheckCircle`, `Lock`, `Key`, `Users`, `Chart`, `Book`, `Database`, `Settings`, `Verified`, `Globe`.
- No logo exists for the advisor: the `ADVISORY` wordmark (**Wordmark**) is set in type and is a placeholder to swap for a real firm's mark.

## Imagery

- No stock photos, clip art, illustrations of people or AI-generated imagery.
- Diagrams over pictures: timelines, process steps, matrices, who-does-what maps, built from tokens (**Diagram**, **Timeline**, **RiskMatrix**).
- Screenshots only of real tools the client uses, with a 1px `rule` border and an exhibit caption.
- Logos: only the client's own, in the **ClientLogoSlot**, and only when supplied. No consultancy or third-party logos.

## Accessibility

- Text holds at least 4.5:1 on its ground (3:1 at 24px bold or 32px+ on slides). The pairs in the colour tables are measured; do not invent new ones — never set text in `accent-400` on light grounds (3.2:1) or in `ink-300` anywhere.
- Never rely on colour alone: RAG with words, heat cells with numbers, chart series with direct labels, the focus bar named in the title.
- Web pages: `lang="en-GB"`, real buttons, links, inputs and labels; tables with header cells; SVG charts with `role="img"` and an `aria-label` that states the message; a visible focus ring.
- Slides: an `aria-label` on every `<svg>`, `alt` on every image, reading order = source order.

## Spreadsheets

- Font Inter if installed, else Arial; 10pt body, 12pt bold headers.
- Header rows `ink-900` fill with white bold text; input cells `accent-100` fill with `ink-900` text; calculations unfilled; checks with `rag-*` fill, white text and the word (Grey with `ink-900` text).
- Numbers right-aligned with thousands separators; units in headers (EUR k); totals bold with a top border; no merged cells in data ranges.
- Tab colours: `accent-600` inputs, `ink-500` calculations, `ink-900` outputs. Every sheet starts with a title row stating its purpose and an "Illustrative" note where it applies.

## Do and don't

| Do | Don't |
|---|---|
| One teal element per exhibit: the number or bar the title talks about | Teal everywhere, or six coloured series that all matter equally |
| `signal` for the EUR 468m gated by notified-body capacity | `signal` for anything merely important, or for decoration |
| "Amber" pill or word with the colour | A coloured dot with no label |
| A source line on every data exhibit, ending "Illustrative" for client data | Numbers with no source, or "Source: internal" |
| Roles: "PSIRT lead", "General Counsel" | People's names; a real company as the client |
| Hairlines and white space | Boxes around everything, drop shadows, gradients |
| A diagram of the 24h / 72h / 14-day clock | A stock photo of a padlock |
| "EUR 9.3m to Dec 2027 (base case)" | "approx. €9.25M" |

## Pre-flight check

Before handing over any deliverable: every slide or section has a tracker, an action title that its exhibit proves, and (for data) a source line; every client number is labelled Illustrative and matches the engagement data; dates read "11 Dec 2027"; money reads "EUR 9.3m"; no text under 24px on slides; RAG only for status, each with its word; at most one `signal` element per page; no names of people; footers carry engagement · Illustrative · date and a page number.

## Components

- **Brand**: Wordmark, ClientLogoSlot.
- **Slide masters** (paste-ready `<section>` in each README): SlideTitle, SlideDivider, SlideContent, SlideTwoColumn, SlideChart, SlideBigNumber, SlideQuote, SlideAgenda, SlideAppendix.
- **Status and data**: RagPill, KpiTile, HeatmapCell, ProgressBar, MaturityRating, RiskMatrix, Timeline, BarChart, LineChart, DataTable.
- **Document patterns**: Headings, ExhibitCaption, Callout, Checklist, Footnote.
- **Web patterns**: PageShell, Nav, Card, Button, SurveyScale, FormField, Tag.
- **Guidance**: Iconography, Diagram.

Each lives at `project/components/<Name>/`: `README.md` (rules, what you provide, markup) and `preview.html` (reference rendering). Web markup uses the classes in `project/components/bundle.css` plus the type-style classes generated from the tokens (`heading-2`, `body`, `eyebrow`, `kpi-value` …).

## Cover

The system's face at the top of this page, and its one signature motif: a band of ink, teal and tint blocks crossed by fine ground-coloured rules, with the name set large in the serif beneath.

- **Anatomy** (960 × 340): a 120px band flush to the top edge — `bg-inverse` block 448px wide, `action` block 272 × 88px, `bg-emphasis` block bleeding off the right — with 8px gutters (`space-2`); four 1px rules in `bg-page` at a 24px pitch (`space-5`) crossing the blocks; one 16px `signal` diamond with `radius-sm` corners, the binding constraint kept small. Below the band, 32px from the left and bottom (`space-6`): the name in Source Serif 4 64px / 0.95, 500, `text-primary`, broken only at "(white-label)"; one tagline in Inter 14px `text-muted`.
- **Rules**: every fill and stroke binds to a token, so the band reads in both themes; no images, gradients, shadows or extra colours; one diamond only; nothing crosses the name. Reuse the band — without the diamond — as the header strip of report covers and one-page visuals, never on content slides or pages.
- **Markup**: `project/components/Cover/preview.html` — one inline SVG for the band plus two text elements; its comment lists the tokens and sizes. Keep `project/components/Cover/` to that preview alone: documentation for the cover lives here, because a README in that folder turns the cover into an ordinary component and removes it from the top of this page.
