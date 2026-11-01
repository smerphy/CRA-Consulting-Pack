# SurveyScale

The 0–4 maturity question for surveys and the readiness diagnostic: a segmented radio scale with level names, separate "Not applicable" and "Don't know" options, and the descriptor of the chosen level.

**Scale** — 0 Not started · 1 Initial · 2 Defined · 3 Implemented · 4 Assured (target 3). Show the level names on the segments; show the full descriptor of the selected level below ("2 · Defined: documented and partly applied; gaps known").

**Anatomy**
- `<fieldset>` with the question as `<legend>`: question ID in `id` style, then the statement (16px 600). Questions are statements the respondent rates, not questions with "do you".
- Five segments in one bordered strip (1px `rule-strong`, `radius-md`), each ≥ 60px tall: number (18px 700) over name (12px). Selected: `action` fill, `text-on-action`. Hover: `bg-subtle`.
- Selection is never coloured by heat or RAG — answering is not judging, and red for 0 would bias answers.
- "Not applicable" and "Don't know" as separate radios in the same group, below the strip; they clear the scale.
- Focus: a 2px `focus` outline around the whole strip; arrow keys move between levels (native radios).
- Phones (≤ 640px): the strip stacks vertically, 48px rows, number then name on one line.

**You provide** question ID, statement, group name, the current value, the descriptors per level.

**Web**
```html
<fieldset class="adv-scale">
  <legend class="adv-scale__q"><span class="id">Q10.2</span>Candidate notified bodies are shortlisted …</legend>
  <div class="adv-scale__options">
    <label class="adv-scale__opt"><input type="radio" name="q10-2" value="0"><span class="adv-scale__n">0</span><span class="adv-scale__name">Not started</span></label>
    <!-- 1 Initial · 2 Defined · 3 Implemented · 4 Assured -->
  </div>
  <div class="adv-scale__extra">
    <label class="adv-scale__alt"><input type="radio" name="q10-2" value="na">Not applicable</label>
    <label class="adv-scale__alt"><input type="radio" name="q10-2" value="dk">Don’t know</label>
  </div>
  <p class="adv-scale__desc"><b>2 · Defined:</b> documented and partly applied; gaps known.</p>
</fieldset>
```
Selection styling uses `:has(input:checked)` (all current browsers).

**Paper and Docs instruments** — print the five levels as a row of boxes with numbers and names, plus "N/A" and "Don't know"; keep the same order and wording.
