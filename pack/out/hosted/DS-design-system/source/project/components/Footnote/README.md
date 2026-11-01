# Footnote

Numbered references for legal citations, definitions and caveats: superscript numbers in teal in the text, notes in `source-line` style under a hairline at the end of the section.

**Rules**
- Use footnotes for citations and caveats that would interrupt the sentence; put sources of exhibits in their source lines instead.
- Number consecutively through the document (web: per page). Place the reference after punctuation only when it covers the whole sentence; otherwise directly after the claim.
- Cite law as "Regulation (EU) 2024/2847, Art 64(2)"; guidance with its reference and status ("C(2026) 5252, pending adoption, as at 30 Oct 2026"); surveys with publisher, sample and type.
- One footnote, one point, at most three lines. No footnotes on slides — use the source line or speaker notes.

**You provide** the reference number and the note text.

**Web**
```html
<p class="body">… EUR 30m<a class="adv-fnref" href="#fn1" id="r1" aria-label="Footnote 1">1</a>.</p>
<div class="adv-footnotes source-line"><ol><li id="fn1">Regulation (EU) 2024/2847, Art 64(2) …</li></ol></div>
```
`adv-fnref`: 0.7em, superscript, 600, `text-accent`. `adv-footnotes`: 1px `rule` above, `text-muted`.

**Claude Docs** — markdown footnotes (`[^1]`) where supported; otherwise "(note 1)" and a "Notes" list at the end of the section.
