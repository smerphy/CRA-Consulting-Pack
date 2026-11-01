# Wordmark

A type-only placeholder for the advisor's mark: "ADVISORY" in letter-spaced small caps, set in Source Serif 4 600 — swap it for a real firm's name or logo.

**Use** top-left on title slides, in web page headers and on document covers. Never on content slides (the footer carries the engagement line instead), never next to the client logo at the same weight.

**Swap**
- A firm's name: replace the text and keep the style.
- A firm's logo: replace the element with the supplied SVG or PNG at 24px high on the web, 32px on slides. Never draw, trace or approximate a logo; with no supplied file, keep the type placeholder.
- White-label delivery: keep "Advisory" or remove the wordmark; write `[Advisor]` where a firm name would appear in text ("Prepared by [Advisor]").

**Web**
```html
<span class="adv-wordmark">Advisory</span>
<span class="adv-wordmark adv-wordmark--lg">Advisory</span>
<span class="adv-wordmark adv-wordmark--inverse">Advisory</span>  <!-- on bg-inverse -->
```
Small caps come from `font-variant-caps: all-small-caps`; 0.24em tracking; `text-primary` (16.7:1 on paper) or `text-on-inverse`.

**Slides** (no small caps in the subset: uppercase plus tracking)
```html
<p style="position:absolute;left:128px;top:64px;width:640px;font-family:'Source Serif 4', Georgia, serif;font-size:28px;line-height:32px;font-weight:600;letter-spacing:8px;text-transform:uppercase;color:#FAFAF7">Advisory</p>
```
Use `#0E1A2B` on paper slides, `#FAFAF7` on `ink-900`.

**Don't** colour it teal, add a symbol or monogram, or set it in Inter.
