# Headings

The document heading hierarchy: serif for the title and section action headings, sans for sub-heads, an eyebrow tracker above each section and a 72-character text measure.

| Level | Style | Use |
|---|---|---|
| Eyebrow | `eyebrow` — Inter 12px 600, 0.08em, uppercase, `text-accent` | Section tracker above every H2: "02 · Market access"; document type and date above the H1 |
| Display | `display` — Source Serif 4 48px 500 | Cover titles and web page heroes only |
| H1 | `heading-1` — Source Serif 4 36px / 44px 500 | The document title, once |
| H2 | `heading-2` — Source Serif 4 28px / 36px 500 | Section **action headings**: full sentences with the so-what |
| H3 | `heading-3` — Inter 20px / 28px 600 | Sub-sections; may be topic labels |
| H4 | `heading-4` — Inter 16px / 24px 600 | Paragraph heads, card titles |
| Lead | `body` in `text-primary` | One-sentence summary under the H1 or an H2 |
| Body | `body` — Inter 16px / 26px | Running text in `text-body` |

**Rules**
- H2s, read in order, must tell the whole story; a reader who reads only them gets the argument.
- Never skip a level; never more than four levels; no numbered headings except the eyebrow's section number.
- Sentence case everywhere; no full stops in headings.
- Keep text to `text-measure` (72ch); headings may run the full column.

**Web**
```html
<article class="adv-doc">
  <p class="eyebrow">02 · Market access</p>
  <h2 class="heading-2">Third-party assessment capacity, not technical work, sets the critical path</h2>
  <p class="body">…</p>
</article>
```
`adv-doc` supplies the vertical rhythm (48px before a section, 8px between a heading and its first paragraph).

**Claude Docs** — H1 for the title, H2 for action headings, H3/H4 below; put the tracker as a short bold line above each H2 ("**02 · Market access**").
