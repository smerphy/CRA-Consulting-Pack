# PageShell

The frame for every hand-built page: a 64px header (wordmark, product name, nav, client logo slot), a 1200px main column, and a footer carrying the engagement, classification and date.

**Anatomy**
- Header: sticky, `bg-page`, hairline `rule` below. Left to right: Wordmark, product line ("Project Rampart · Delivery portal", `text-muted`, hidden on phones), Nav, spacer, ClientLogoSlot.
- Main: `page-max-width` 1200px, centred; 64px top padding (32px on phones); side gutters `page-gutter` 24px, `page-gutter-phone` 16px at phone width.
- Hero (optional): eyebrow, `display` title stating the page's message, one lead paragraph, max 72ch.
- Footer: engagement · Illustrative · date · "Prepared by [Advisor]" left; data currency right ("Regulatory facts verified to 30 Oct 2026"); 12px `text-muted`.

**Page rules**
- `<html lang="en-GB">`; `body` background `bg-page` (bundle.css sets it); light and dark via the semantic tokens.
- One `display` or `heading-1` per page; the page title is an action title.
- No horizontal scroll at 360px: grids collapse (`adv-grid` is auto-fit), wide tables scroll in `adv-table-wrap`, the nav scrolls sideways.
- Everything a reader can act on is a real `<a>`, `<button>` or form control.

**You provide** product name, nav items with the current page, hero copy, footer lines, client logo if supplied.

**Web**
```html
<div class="adv-shell">
  <header class="adv-shell__header">
    <span class="adv-wordmark">Advisory</span>
    <span class="adv-shell__product">Project Rampart · Delivery portal</span>
    <nav class="adv-nav" aria-label="Main"><a href="#" aria-current="page">Overview</a><a href="#">Decks</a></nav>
    <span class="adv-shell__spacer"></span>
    <span class="adv-logo-slot" role="img" aria-label="Client logo placeholder">Client logo</span>
  </header>
  <main class="adv-shell__main">…</main>
  <footer class="adv-shell__footer"><span>Project Rampart · Illustrative · 31 Oct 2026</span><span>Facts verified to 30 Oct 2026</span></footer>
</div>
```
