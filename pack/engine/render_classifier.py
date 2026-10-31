"""D13 product classifier: render pack/engine/templates/classifier.html with presets from the client's families.

Presets: up to four client families (one per class present, clear matches first, then one borderline/provisional
family if there is room), followed by the generic presets already in the template (smart meter gateway, HR web
app). The intake can pin the choice and wording in an optional `classifier.presets` list (see the _template intake).
Example Group renders byte-identical to pack/out/classifier/index.html.
Usage: python3 pack/engine/render_classifier.py <pack_data.json> <out.html> [client.yaml]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reskin_common import TEMPLATES, h, h_attr, is_fictional, fill  # noqa: E402

MAX_CLIENT_PRESETS = 4
GENERIC_KEYS = ("SMG", "SAAS")
CLASS_ORDER = ("Class I", "Default", "Class II", "Critical")
SW_WORDS = ("software", "sdk", "library", "libraries", "desktop", "tool", "console", "on-premises", "on-prem")


def annex_to_category(annex_item):
    """'Annex III Class I item 17 (smart door locks)' -> 'I17'; 'Annex IV item 2 (...)' -> 'IV2'; else ''."""
    s = str(annex_item or "")
    if s.lower().startswith("under legal review"):
        return ""
    m = re.search(r"Annex\s+III,?\s+Class\s+(II|I)\b,?\s+item\s+(\d+)", s, re.I)
    if m:
        return f"{m.group(1).upper()}{int(m.group(2))}"
    m = re.search(r"Annex\s+IV,?\s+item\s+(\d+)", s, re.I)
    if m:
        return f"IV{int(m.group(1))}"
    return ""


def _class_group(cls):
    return "Default" if cls.startswith("Default") else cls


def guess_form(f):
    text = f"{f.get('name', '')} {f.get('description', '')}".lower()
    words = set(re.findall(r"[a-z][a-z\-]*", text))
    if any(w in text for w in SW_WORDS):
        return "sw"
    if "app" in words or "apps" in words or "cloud" in words:
        return "both"
    return "hw"


def guess_core(f):
    d = str(f.get("description") or f["name"]).strip()
    d = re.split(r"(?<=[.;])\s", d)[0].rstrip(".;")
    return d


def choose_families(families):
    """One per class present (clear matches first), then one provisional family, up to four."""
    chosen = []
    for k in CLASS_ORDER:
        cands = [f for f in families if f["cra_class"] == k]
        if k != "Default":
            clear = [f for f in cands if annex_to_category(f["annex_item"])]
            cands = clear or cands
        if cands:
            chosen.append(cands[0])
    prov = [f for f in families if "provisional" in f["cra_class"]]
    if prov:
        chosen.append(prov[0])
    return chosen[:MAX_CLIENT_PRESETS]


def build_presets(pack_data, overrides=None):
    fams = pack_data["client"]["product_families"]
    by_id = {f["id"]: f for f in fams}
    if overrides:
        picks = []
        for o in overrides:
            o = {"family": o} if isinstance(o, str) else dict(o)
            if o["family"] not in by_id:
                raise ValueError(f"classifier preset refers to unknown family {o['family']!r}")
            picks.append((by_id[o["family"]], o))
        picks = picks[:MAX_CLIENT_PRESETS]
    else:
        picks = [(f, {}) for f in choose_families(fams)]
    name = pack_data["meta"]["illustrative_client"]
    fict = is_fictional(pack_data)
    out = []
    for f, o in picks:
        key = o.get("key") or re.sub(r"[^A-Za-z0-9_]", "", f["id"]) or "P"
        if key in GENERIC_KEYS or key[0].isdigit():
            key = "C" + key
        borderline = "provisional" in f["cra_class"]
        tag = f"illustrative {name} product" if fict else f"{name} product"
        label = f"{f['name']} ({tag}{'; borderline' if borderline else ''})"
        chip = o.get("chip") or (f["name"] if len(f["name"]) <= 24 else f["name"].split()[0])
        out.append({
            "key": key, "chip": chip,
            "fields": [
                ("label", label), ("form", o.get("form") or guess_form(f)), ("conn", o.get("conn", "yes")),
                ("market", o.get("market", "commercial")), ("excl", o.get("excl", "none")), ("pname", f["name"]),
                ("pcore", o.get("core") or guess_core(f)), ("cat", o.get("cat", annex_to_category(f["annex_item"]))),
                ("conf", "borderline" if borderline else "clear"), ("foss", o.get("foss", "no")),
                ("ai", o.get("ai", "no")), ("legacy", o.get("legacy", "yes")),
            ],
        })
    keys = [p["key"] for p in out]
    if len(set(keys)) != len(keys):
        raise ValueError(f"classifier presets: duplicate keys {keys}")
    return out


def _js_key(k):
    return k if re.fullmatch(r"[A-Za-z_$][A-Za-z0-9_$]*", k) else json.dumps(k)


def render(pack_data, template_html=None, presets=None):
    """presets: optional list from the intake's classifier.presets (family ids or dicts)."""
    if template_html is None:
        template_html = (TEMPLATES / "classifier.html").read_text(encoding="utf-8")
    m = pack_data["meta"]
    ps = build_presets(pack_data, presets)
    buttons = "\n".join(f'      <button class="chip" type="button" data-preset="{h_attr(p["key"])}">{h(p["chip"])}</button>' for p in ps)
    js = "\n".join(
        "    " + _js_key(p["key"]) + ": { " + ", ".join(f"{k}: {json.dumps(v, ensure_ascii=False)}" for k, v in p["fields"]) + " },"
        for p in ps)
    name = m["illustrative_client"]
    tokens = {
        "FACTS_AS_AT": h(m["facts_as_at"]),
        "ADVISOR": h(m["advisor_placeholder"]),
        "VERSION": h(m["version"]),
        "ISSUE_DATE": h(m["issue_date"]),
        "CODENAME": h(m["programme_codename"]),
        "PRESET_BUTTONS": buttons,
        "PRESETS_JS": js.replace("</", "<\\/"),
        "PNAME_EXAMPLE": h_attr(ps[0]["fields"][5][1]) if ps else "Smart meter gateway",
        "FOOTER_ILLUS": (f"{h(name)} products are illustrative." if is_fictional(pack_data)
                         else f"Example presets are {h(name)} products."),
        "FIRST_PRESET": json.dumps(ps[0]["key"] if ps else "SMG")[1:-1],
    }
    if not ps:  # no client presets: drop the empty line left by the buttons/JS tokens
        template_html = template_html.replace("{{PRESET_BUTTONS}}\n", "").replace("{{PRESETS_JS}}\n", "")
    return fill(template_html, tokens, "classifier template")


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    pd = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    presets = None
    if len(argv) > 3:
        import yaml
        presets = (yaml.safe_load(Path(argv[3]).read_text(encoding="utf-8")).get("classifier") or {}).get("presets")
    Path(argv[2]).parent.mkdir(parents=True, exist_ok=True)
    Path(argv[2]).write_text(render(pd, presets=presets), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv)
