# ProgressBar

Progress towards a target as a thin teal bar on a quiet track, with a 2px ink tick at the target and the numbers written out.

**Use** for completion measures (engineers trained, releases with signed SBOMs, budget consumed). Not for status — pair it with a RagPill when a judgement is needed — and not for comparing categories (use BarChart).

**Anatomy**
- Head row: measure on the left (`text-body`), value on the right as "count / base · %" (600, tabular).
- Track: 8px (12px for `adv-progress--lg`), `bg-subtle` with a hairline inset, `radius-sm`.
- Fill: `action` teal, width = value %. One colour only — never RAG-coloured fills.
- Target tick: 2px `text-primary`, 4px proud of the track, at the target %.
- Meta row: source left, target with date right, `text-muted` 12px.
- Accessibility: `role="img"` and an `aria-label` that says value and target in words.

**You provide** label, value, base, target and date, source.

**Web**
```html
<div class="adv-progress">
  <div class="adv-progress__head"><span>Engineers trained</span><span class="adv-progress__value">140 / 920 · 15%</span></div>
  <div class="adv-progress__track" role="img" aria-label="15% of engineers trained; target 60% by Mar 2027">
    <div class="adv-progress__fill" style="width:15.2%"></div>
    <div class="adv-progress__target" style="left:60%"></div>
  </div>
  <div class="adv-progress__meta"><span>Source: LMS, 30 Oct 2026; Illustrative</span><span>Target 60% by Mar 2027</span></div>
</div>
```

**Slides** — painted divs, 16px tall, inside a 960px track:
```html
<div style="position:relative;width:960px;height:16px;background:#EEF1F5;border-radius:2px">
<div style="position:absolute;left:0px;top:0px;width:146px;height:16px;background:#0F6E6A;border-radius:2px"></div>
<div style="position:absolute;left:575px;top:-8px;width:2px;height:32px;background:#0E1A2B"></div>
</div>
```
Widths are value × track width (15.2% × 960 = 146px; target 60% at 576px less 1px).
