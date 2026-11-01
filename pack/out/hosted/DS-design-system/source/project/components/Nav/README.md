# Nav

Two navigation levels: the header nav (between pages, current page marked by a 2px teal rule) and section tabs (views within a page, current tab marked in ink).

**Header nav** (`adv-nav`) — 14px 500 `text-body` links, 64px tall to fill the header; hover `text-primary`; current page `aria-current="page"`, `text-primary` with a 2px `action` bottom rule. Five to seven items; labels are nouns ("Decks", "Diagnostic"). Scrolls sideways on phones; never a hamburger for fewer than seven items.

**Tabs** (`adv-tabs`) — views of one data set ("Summary, Families, Domains, Questions"); 14px 500 `text-muted`, current `text-primary` with a 2px `text-primary` rule sitting on the hairline. If tabs change content without navigation, use `role="tablist"` / `role="tab"` / `aria-selected` and arrow-key movement.

**Rules** — one teal current-marker per screen (the header); tabs stay ink so teal remains the page's single accent. No icons in nav items.

**You provide** items, hrefs, the current item.

**Web**
```html
<nav class="adv-nav" aria-label="Main"><a href="#" aria-current="page">Overview</a><a href="#">Decks</a></nav>
<nav class="adv-tabs" aria-label="Diagnostic views"><a href="#" aria-current="page">Summary</a><a href="#">Families</a></nav>
```
