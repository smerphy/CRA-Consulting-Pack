# Brief DS — Advisory Design System (white-label)

**Goal:** a reusable, white-label consulting design system that every deck, one-pager and web page in this pack (and the consultant's future client work) is built on. Speed matters: slide and design builders are waiting for your URL. Aim to publish a complete, high-quality v1 in one pass.

**Create from:** the Design System artifact type — `type_url: https://claude.ai/artifact/5M7UeXXcx16TP3vzVFNDzd`, `title: "Advisory Design System (white-label)"`, `auto_open: "after_first_write"`. Follow the instructions the type returns.

**Identity (use exactly the tokens in BRIEF.md section 4):**
- Personality: premium management-consulting restraint. Calm ink-navy on warm paper, one confident teal accent, a single signal orange reserved for the binding constraint, disciplined RAG colours for status only.
- Type: Source Serif 4 for display and slide titles (action titles are sentences, so set them in serif at comfortable line length), Inter for body/UI/tables/numbers (tabular figures), JetBrains Mono for IDs and code. Provide a type scale for slides (16:9) and for documents/web.
- Spacing scale, radius (small — 2/4/6 px; consulting decks are crisp, not bubbly), border/rule weights (hairlines in ink-300).
- Wordmark/logo slot: a neutral text wordmark placeholder "ADVISORY" (letter-spaced small caps) plus a "client logo slot" component; both swappable.

**Components to define (with live previews where the type supports them):**
1. Slide masters: title slide; section divider; action-title content slide (tracker label top-left, action title, body, source line bottom-left, footer with classification label + page number); two-column; chart slide; big-number slide; quote/callout slide; agenda; appendix.
2. Status and data: RAG pill (Red/Amber/Green/Grey with text label), KPI tile (label, value, target, trend, RAG), maturity heatmap cell (0-4 colours, number always printed), progress bar, Harvey ball or 0-4 dot rating, risk matrix (5x5 likelihood x impact), Gantt/timeline bar with milestone diamonds and "today" marker, stacked/clustered bar conventions, line chart conventions, table style (zebra off, hairline rules, right-aligned numbers, bold totals).
3. Document patterns: heading hierarchy, exhibit caption ("Exhibit 3 — …" + source line), callout boxes (Key insight, Decision required, Illustrative data, Draft/unverified), checklist style, footnote style.
4. Web patterns for hand-built pages: page shell, card, nav, buttons (primary teal, secondary outline), form controls for surveys (0-4 segmented scale), tags/chips, dark mode tokens (ink-900 background, paper text, accent-400 for emphasis).
5. Iconography guidance (simple 1.5 px line icons, only when they add meaning) and imagery guidance (no stock photos; diagrams over pictures).

**README (critical — future AI agents will read it):** concise rules for building consulting deliverables in this system: pyramid principle; action titles; one message per exhibit; source lines; "Illustrative" labelling; number and date formats (EUR 9.3m; 11 Dec 2027; British English); how to apply tokens in Slides, Docs, Dashboards and hand-built HTML; accessibility (contrast, numbers on coloured cells); do/don't examples.

**Report back:** the design system URL, and a 10-line "how to use this design system in Slides and hand-built pages" note for other builders (CSS variable names, font links, which slide masters exist).
