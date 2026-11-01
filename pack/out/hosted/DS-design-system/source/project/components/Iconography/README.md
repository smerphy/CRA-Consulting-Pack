# Iconography

The approved icon set: 18 simple line icons on a 24px grid with a 1.5px stroke, round caps and joins and no fills — used only where an icon adds meaning, and always beside a word.

**Rules**
- Draw with `stroke="currentColor"` (class `adv-icon`): `text-body` / `ink-700` by default, `text-emphasis` / `accent-600` for the one emphasised item, `text-critical` only inside a Critical callout.
- Sizes: 16px inline with text, 24px default, 32px in cards and diagrams; the stroke stays 1.5px at every size (`vector-effect: non-scaling-stroke`).
- Every icon has a visible text label; decorative copies get `aria-hidden="true"`. An icon-only button needs an `aria-label`.
- One icon style per deliverable; never emoji, filled glyphs, two-tone icons or icons as bullet decoration.
- Meanings are fixed: `clock` = reporting clock / time limit, `alert` = critical or binding constraint, `shield-check` = conformity, `layers` = SBOM, `building` = notified body or authority. Do not reuse an icon for a different idea in the same pack.

**Set** — clock · calendar · flag · shield · shield-check · lock · key · document · clipboard-check · alert · users · building · chip · layers · link · scale · check · arrow-right. Paste-ready SVG for each is in `preview.html` beside this file; for example:
```html
<svg class="adv-icon" viewBox="0 0 24 24" aria-hidden="true"><circle cx="12" cy="12" r="9"/><path d="M12 7v5l3 2"/></svg>
```
Outside bundle.css (canvases, docs), add `fill="none" stroke="#26364D" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round"` to the `<svg>`.

**Slides** — use the Slides `<x-icon>` set at 48px or larger beside 24–28px text, coloured `#26364D` or `#0F6E6A`: `Clock`, `Warning`, `CheckCircle`, `Check`, `Lock`, `Key`, `Users`, `Chart`, `Book`, `Database`, `Settings`, `Verified`, `Globe`, `Link`. Our inline SVGs also work in slides (an `<svg aria-label>` with the stroke attributes above).

**Imagery** — no stock photos, clip art, people or AI images; diagrams over pictures (Diagram, Timeline, RiskMatrix).
