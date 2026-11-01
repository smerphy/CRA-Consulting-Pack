# ClientLogoSlot

Reserved space for the client's own logo, top-right opposite the wordmark; a dashed placeholder until the client supplies a file.

**Use** on title slides, document covers and web page headers. Only the client's logo, and only a file the client supplied — never a logo found online, redrawn or recoloured.

**Sizes** — web header 160 × 48; document cover 240 × 72; title slide 320 × 96 pinned at `left:1472px; top:48px`. The logo sits centred inside the box at its own aspect ratio (`object-fit: contain`), with at least 8px clear space.

**Filled**
```html
<span class="adv-logo-slot adv-logo-slot--filled"><img src="/_blob/<id>" alt="Client name logo"></span>
```
On dark grounds use the client's reversed artwork; if none exists, place the logo on the light pages only.

**Empty** (drafts only)
```html
<span class="adv-logo-slot" role="img" aria-label="Client logo placeholder">Client logo</span>
```
1px dashed `rule-strong`, `radius-sm`, label 12px 600 uppercase `text-muted`. Delete the empty slot before delivery — never ship "Client logo". For the illustrative engagement (Example Group), leave the slot empty or remove it.

**Slides**
```html
<div style="position:absolute;left:1472px;top:48px;width:320px;height:96px;display:flex;align-items:center;justify-content:center;border:1px dashed #56667E;border-radius:4px"><p style="font-size:24px;line-height:32px;color:#56667E">Client logo</p></div>
```
Filled: replace the `<p>` with `<img src="/_blob/<id>" alt="…" style="width:288px;height:72px;object-fit:contain">` and remove the border.
