"""Regenerate the tokenised templates from the reference pages in pack/out/.

Run this after editing the reference portal (D12) or classifier (D13) for Example Group:
    python3 pack/engine/make_templates.py
It swaps every client-specific value in the reference page for a {{TOKEN}} and fails loudly if a value it expects
is missing, so the regression (Example Group renders byte for byte) keeps holding. The diagnostic (D08) needs no
template: render_diagnostic.py works on the reference page directly.
"""
import re
import sys
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
OUT = PACK / "out"
TPL = Path(__file__).resolve().parent / "templates"


def sub(text, old, new, count=1):
    n = text.count(old)
    if n != count:
        sys.exit(f"make_templates: expected {count} occurrence(s) of {old[:90]!r}, found {n}. Update make_templates.py.")
    return text.replace(old, new)


def portal():
    t = (OUT / "portal" / "index.html").read_text(encoding="utf-8")
    t = sub(t, '<span>Version 1.0</span><span>Issued 31 Oct 2026</span><span>Facts verified to 30 Oct 2026</span><span>Prepared by [Advisor]</span>',
            '<span>Version {{VERSION}}</span><span>Issued {{ISSUE_DATE}}</span><span>Facts verified to {{FACTS_AS_AT}}</span><span>Prepared by {{ADVISOR}}</span>')
    t = sub(t, '<p class="illus"><b>Illustrative engagement.</b> Example Group (fictional manufacturer of connected products) · Project Rampart. Every client number is illustrative; regulatory facts are real and dated.</p>',
            '<p class="illus">{{ILLUS_HTML}}</p>')
    t = sub(t, '<span class="big" id="days">406</span>', '<span class="big" id="days">{{DAYS}}</span>')
    t = sub(t, "Market access, not engineering, sets Example Group's critical path.", "{{NUM_HEADLINE}}")
    t = sub(t, '<span class="v signal tabular">EUR 468m</span><span class="k">of annual EU revenue sits in Class I and II products that need a notified body. None is designated yet.</span>',
            '<span class="v signal tabular">{{EUNB}}</span><span class="k">of annual EU revenue sits in {{NB_CLASSES}} products that need a notified body. None is designated yet.</span>')
    t = sub(t, '<span class="src">Portfolio analysis; Annex III; Commission, checks to 8 Sep 2026</span>',
            '<span class="src">Portfolio analysis; {{NB_ANNEX}}; Commission, checks to 8 Sep 2026</span>')
    t = sub(t, '<span class="v tabular">44%</span><span class="k">baseline readiness across 13 product families. Conformity and market access is weakest at 16%.</span><span class="src">Readiness diagnostic, 28 Oct 2026</span>',
            '<span class="v tabular">{{READINESS}}</span><span class="k">baseline readiness across {{NFAM_TEXT}}. {{WEAKEST}} is weakest at {{WEAKEST_PCT}}.</span><span class="src">Readiness diagnostic, {{BASELINE_DATE}}</span>')
    t = sub(t, '<span class="v emph tabular">EUR 9.3m</span><span class="k">to Dec 2027, then EUR 1.8m a year: 0.77% of one year’s revenue.</span><span class="src">Business case, base scenario incl. 15% contingency</span>',
            '<span class="v emph tabular">{{ONEOFF}}</span><span class="k">to Dec 2027, then {{RUN}} a year: {{ONEOFF_PCT}} of one year’s revenue.</span><span class="src">Business case, base scenario incl. {{CONTINGENCY_PCT}} contingency</span>')
    t = sub(t, '<span class="v tabular">9h 40m</span><span class="k">to file an early warning in the first Article 14 drill, against a 24-hour legal clock.</span><span class="src">Drill record, 22 Oct 2026</span>',
            '<span class="v tabular">{{DRILL_VALUE}}</span><span class="k">{{DRILL_TEXT}}</span><span class="src">{{DRILL_SRC}}</span>')
    t = sub(t, "Regulatory facts are verified to 30 Oct 2026. Re-check", "Regulatory facts are verified to {{FACTS_AS_AT}}. Re-check")
    t = sub(t, "CRA Readiness Programme Pack · v1.0 · 31 Oct 2026 · Prepared by [Advisor] · White-label",
            "CRA Readiness Programme Pack · v{{VERSION}} · {{ISSUE_DATE}} · Prepared by {{ADVISOR}} · White-label")
    t = sub(t, "<span>Example Group and Project Rampart are fictional and used for illustration only. Regulatory",
            "<span>{{FICTION_NOTE}} Regulatory")
    t = sub(t, "The monthly management update, filled for 30 Oct 2026:", "The monthly management update, filled for {{STEERCO1}}:")
    t = sub(t, 'el("span", "pending", "In production")', 'el("span", "pending", "{{PENDING_LABEL}}")')

    # Deliverable cards: every url (and file note) becomes a per-deliverable token.
    def card(m):
        line = m.group(0)
        did = re.search(r'id: "(\w+)"', line).group(1)
        line = re.sub(r'url: "[^"]*"', f'url: "{{{{URL:{did}}}}}"', line)
        line = re.sub(r'file: "[^"]*"', f'file: "{{{{FILE:{did}}}}}"', line)
        return line
    t, n = re.subn(r'^    \{ phase: \d, id: "\w+".*$', card, t, flags=re.M)
    if n != 15:
        sys.exit(f"make_templates: expected 15 deliverable cards in the portal, found {n}")
    for leftover in ("Example Group", "Project Rampart", "claude.ai/artifact"):
        if leftover in t:
            sys.exit(f"make_templates: portal template still contains {leftover!r}")
    return t


def classifier():
    t = (OUT / "classifier" / "index.html").read_text(encoding="utf-8")
    t = sub(t, "<span>Facts as at 30 Oct 2026</span><span>Prepared by [Advisor]</span>",
            "<span>Facts as at {{FACTS_AS_AT}}</span><span>Prepared by {{ADVISOR}}</span>")
    t, n = re.subn(r'(?:^      <button class="chip" type="button" data-preset="(?:L2|T200|SG900|H3)">[^<]*</button>\n)+',
                   "{{PRESET_BUTTONS}}\n", t, flags=re.M)
    if n != 1:
        sys.exit("make_templates: client preset buttons not found in the classifier")
    t = sub(t, 'placeholder="e.g. L2 Smart Lock"', 'placeholder="e.g. {{PNAME_EXAMPLE}}"')
    t = sub(t, " Example Group products are illustrative. ", " {{FOOTER_ILLUS}} ")
    t = sub(t, "<p>Project Rampart · CRA Product Classifier (D13) · v1.0 · 31 Oct 2026 · Prepared by [Advisor]</p>",
            "<p>{{CODENAME}} · CRA Product Classifier (D13) · v{{VERSION}} · {{ISSUE_DATE}} · Prepared by {{ADVISOR}}</p>")
    t, n = re.subn(r'(?:^    (?:L2|T200|SG900|H3): \{ label: .*\n)+', "{{PRESETS_JS}}\n", t, flags=re.M)
    if n != 1:
        sys.exit("make_templates: client presets not found in the classifier")
    t = sub(t, 'load("L2");', 'load("{{FIRST_PRESET}}");')
    for leftover in ("Example Group", "Project Rampart", "L2 Smart", "SG-900", "T200", "HomeHub"):
        if leftover in t:
            sys.exit(f"make_templates: classifier template still contains {leftover!r}")
    return t


def main():
    TPL.mkdir(exist_ok=True)
    (TPL / "portal.html").write_text(portal(), encoding="utf-8")
    (TPL / "classifier.html").write_text(classifier(), encoding="utf-8")
    print("templates written to", TPL)


if __name__ == "__main__":
    main()
