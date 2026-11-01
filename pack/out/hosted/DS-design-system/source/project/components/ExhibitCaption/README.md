# ExhibitCaption

The frame around every chart or table in a document: "Exhibit n — message" above, a unit line, a ruled body, and a note and source line below.

**Anatomy**
1. Title line: `exhibit-title` (Inter 14px 600, `text-primary`) — "**Exhibit 2** — " in `text-accent`, then the exhibit's message as a sentence. Number exhibits consecutively through the document.
2. Unit line: 13px `text-muted` — what is measured, unit, base, period ("EU revenue of the 13 in-scope families by product class, EUR m").
3. Body: 1px `text-primary` rule above, 1px `rule` below, 16px padding.
4. Note and source: `source-line` (12px `text-muted`). "Note: …" first if needed, then "Source: …; Illustrative". Survey and vendor data carry their type and base.

**Rules**
- One exhibit, one message; the caption title states it and must be true of the data.
- Cross-refer in text by number ("see Exhibit 2"), never "the chart below".
- On slides the action title replaces the caption title and the source line sits in the footer zone; exhibits are not numbered.

**You provide** exhibit number, message, unit line, body, note, source.

**Web**
```html
<figure class="adv-exhibit">
  <figcaption class="adv-exhibit__caption">
    <p class="exhibit-title adv-exhibit__title"><b>Exhibit 2</b> — EUR 468m of EU revenue sits in families that need a notified body</p>
    <p class="adv-exhibit__unit">EU revenue of the 13 in-scope families by product class, EUR m</p>
  </figcaption>
  <div class="adv-exhibit__body">…chart or table…</div>
  <p class="source-line adv-exhibit__source">Source: …; Illustrative</p>
</figure>
```

**Claude Docs** — a bold line "Exhibit 2 — message", then the chart or table, then an italic "Source: …; Illustrative" line.
