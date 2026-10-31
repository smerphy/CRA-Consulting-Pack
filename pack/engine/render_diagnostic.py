"""D08 readiness diagnostic: rebuild the embedded DATA object and client strings from pack_data.

The template is the reference page pack/out/diagnostic/index.html (Example Group). Rendering Example Group's
pack_data into it reproduces the page byte for byte.
Usage: python3 pack/engine/render_diagnostic.py <pack_data.json> <out.html> [template.html]
"""
import json
import re
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reskin_common import PACK, REFERENCE, h, js_sq, is_fictional, parse_date  # noqa: E402

DEFAULT_TEMPLATE = PACK / "out" / "diagnostic" / "index.html"
DATA_PREFIX = "const DATA = "


def family_short(name, client_name):
    """Short label for heatmap rows: the model code or the first word, without a client-brand prefix."""
    words = name.split()
    brand = client_name.split()[0] if client_name.split() else ""
    if len(words) > 1 and words[0] == brand:
        words = words[1:]
    if len(words) <= 2:
        return " ".join(words)
    return words[0]


def build_data(pd, template_data=None):
    dg = pd["diagnostic"]
    client = pd["client"]
    tpl_domains = {d["id"]: d for d in (template_data or {}).get("domains", [])}
    domains = []
    for d in dg["domains"]:
        t = tpl_domains.get(d["id"], {})
        domains.append(OrderedDict([
            ("id", d["id"]), ("name", d["name"]), ("short", d["short"]),
            ("phrase", t.get("phrase", d["name"][0].lower() + d["name"][1:])),
            ("anchors", t.get("anchors", "")),
            ("questions", d["questions"]),
        ]))
    families = []
    for f in client["product_families"]:
        families.append(OrderedDict([
            ("id", f["id"]), ("name", f["name"]),
            ("short", f.get("short") or family_short(f["name"], client["name"])),
            ("bu", f["bu"]), ("cls", f["cra_class"]), ("wave", f["wave"]), ("route", f["route"]),
            ("annex", f["annex_item"]),
        ]))
    targets = OrderedDict((k, dg["targets"][k]) for k in ("by_jun_2027", "by_nov_2027"))
    base_date = parse_date(dg["baseline_date"])
    return OrderedDict([
        ("scale", dg["scale"]),
        ("target", dg["target_level"]),
        ("indexDefinition", dg["readiness_index_definition"]),
        ("domains", domains),
        ("families", families),
        ("buNames", OrderedDict((b["id"], b["name"]) for b in client["business_units"])),
        ("targets", targets),
        ("baseline", OrderedDict([
            ("date", dg["baseline_date"]),
            ("iso", base_date.isoformat() + "T12:00:00Z"),
            ("label", dg["baseline_label"]),
            ("scores", dg["baseline_scores"]),
        ])),
    ])


def _replacements(pd):
    """(old, new) pairs for every client string in the reference page, escaped for its context."""
    R = REFERENCE
    m = pd["meta"]
    name, code, adv = m["illustrative_client"], m["programme_codename"], m["advisor_placeholder"]
    facts = m["facts_as_at"]
    fict = is_fictional(pd)
    illus = " (illustrative)" if fict else ""
    engagement = "Illustrative engagement" if fict else "Engagement"
    tail = " · Illustrative" if fict else ""
    return [
        # header and footer (HTML)
        (f'<span class="brand-sub">{R["codename"]} · {R["client"]} (illustrative)</span>',
         f'<span class="brand-sub">{h(code)} · {h(name)}{illus}</span>'),
        (f'<p>Prepared by {R["advisor"]} · Illustrative engagement: {R["client"]}</p>',
         f'<p>Prepared by {h(adv)} · {engagement}: {h(name)}</p>'),
        (f'<p>CRA Readiness Diagnostic v1.0 · facts as at {R["facts_as_at"]} · {R["codename"]} · Illustrative</p>',
         f'<p>CRA Readiness Diagnostic v1.0 · facts as at {h(facts)} · {h(code)}{tail}</p>'),
        # plain-text summary (JS single-quoted, copied to clipboard as text)
        (f"L.push('{R['client']} (illustrative) · '",
         f"L.push('{js_sq(name)}{illus} · '"),
        # JS single-quoted strings that become HTML
        (f"'<p class=\"tracker\">{R['codename']} · Readiness diagnostic</p>'",
         f"'<p class=\"tracker\">{js_sq(h(code))} · Readiness diagnostic</p>'"),
        (f"for the fictional client {R['client']}. Switch it off",
         (f"for the fictional client {js_sq(h(name))}. Switch it off" if fict else f"for {js_sq(h(name))}. Switch it off")),
        (f"<dd>{R['codename']}, EU Cyber Resilience Act Readiness Programme</dd>",
         f"<dd>{js_sq(h(code))}, EU Cyber Resilience Act Readiness Programme</dd>"),
        (f"<dd>{R['client']} (illustrative; fictional data)</dd>",
         f"<dd>{js_sq(h(name))}{' (illustrative; fictional data)' if fict else ''}</dd>"),
        (f"<dd>{R['advisor']} · Illustrative engagement: {R['client']}</dd>",
         f"<dd>{js_sq(h(adv))} · {engagement}: {js_sq(h(name))}</dd>"),
    ]


def render(pack_data, template_html=None):
    if template_html is None:
        template_html = DEFAULT_TEMPLATE.read_text(encoding="utf-8")
    lines = template_html.split("\n")
    idx = [i for i, l in enumerate(lines) if l.startswith(DATA_PREFIX)]
    if len(idx) != 1:
        raise ValueError("diagnostic template: expected exactly one line starting with 'const DATA = '")
    i = idx[0]
    tpl_data = json.loads(lines[i][len(DATA_PREFIX):].rstrip().rstrip(";"))
    data = build_data(pack_data, tpl_data)
    payload = json.dumps(data, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    lines[i] = DATA_PREFIX + payload + ";"

    bu_ids = [b["id"] for b in pack_data["client"]["business_units"]]
    bu_line = "const BU_ORDER = [" + ", ".join("'" + js_sq(b) + "'" for b in bu_ids) + "];"
    bidx = [j for j, l in enumerate(lines) if l.startswith("const BU_ORDER = [")]
    if len(bidx) != 1:
        raise ValueError("diagnostic template: BU_ORDER line not found")
    lines[bidx[0]] = bu_line

    out = "\n".join(lines)
    for old, new in _replacements(pack_data):
        n = out.count(old)
        if n == 0:
            raise ValueError(f"diagnostic template: expected text not found: {old[:80]!r}")
        out = out.replace(old, new)
    name = pack_data["meta"]["illustrative_client"]
    if name != REFERENCE["client"]:
        for ref in (REFERENCE["client"], REFERENCE["codename"]):
            if ref in out:
                ln = out[: out.index(ref)].count("\n") + 1
                raise ValueError(f"diagnostic: reference string {ref!r} left at line {ln}; add a replacement rule")
    return out


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    pd = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    tpl = Path(argv[3]).read_text(encoding="utf-8") if len(argv) > 3 else None
    Path(argv[2]).parent.mkdir(parents=True, exist_ok=True)
    Path(argv[2]).write_text(render(pd, tpl), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv)
