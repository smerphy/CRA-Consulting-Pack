"""D12 portal: render pack/engine/templates/portal.html from pack_data and a deliverable URL mapping.

Example Group (pack/data/pack_data.json + pack/out/urls.json, pending label "In production") renders
byte-identical to pack/out/portal/index.html.
Usage: python3 pack/engine/render_portal.py <pack_data.json> <out.html> [urls.json]
"""
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reskin_common import (TEMPLATES, SHARED_HOSTED, DOMAIN_PHRASE, h, js_dq, is_fictional, fill, possessive,  # noqa: E402
                           nb_classes_phrase, weakest_domain, load_reference_urls)

PENDING_REFERENCE = "In production"
PENDING_NEW_CLIENT = "To be produced for this client"
FILE_NOTE = "Excel workbook (.xlsx), delivered with the pack as a file"
CARD_IDS = ("D01", "D02", "D03", "D04", "D05", "D06", "D07", "D08", "D09", "D10", "D11", "D13", "D14", "DS", "KB")


def _drill(pd):
    """Headline 4: the Art 14 drill result if the client has one, else the reporting clock itself."""
    for k in pd.get("kpis", []):
        if "drill" in k.get("name", "").lower() and k.get("display") and "auto" != k.get("display"):
            src = k.get("source") or "Drill record"
            src = re.sub(r"^Drill record (\d)", r"Drill record, \1", src)
            return (k["display"], "to file an early warning in the first Article 14 drill, against a 24-hour legal clock.", src)
    return ("24h", "to file an early warning once an actively exploited vulnerability is known. No drill has been run yet.",
            "Art 14(2)(a); programme plan")


def tokens(pd, urls=None, pending_label=PENDING_NEW_CLIENT, local_links=None, files=None):
    m, c, dg, cm = pd["meta"], pd["client"], pd["diagnostic"], pd["cost_model"]
    fict = is_fictional(pd)
    name, code = m["illustrative_client"], m["programme_codename"]
    tot = cm["base_totals"]
    wid, wval = weakest_domain(pd)
    nfam = c["counts"]["families"]
    if fict:
        illus = (f"<b>Illustrative engagement.</b> {h(name)} (fictional manufacturer of connected products) · {h(code)}. "
                 "Every client number is illustrative; regulatory facts are real and dated.")
        fiction = f"{h(name)} and {h(code)} are fictional and used for illustration only."
    else:
        illus = (f"<b>Client engagement.</b> {h(name)} · {h(code)}. "
                 "Client numbers come from the client's own data; regulatory facts are real and dated.")
        fiction = f"Prepared for {h(name)} ({h(code)}); client figures come from the client's data."
    drill_v, drill_t, drill_s = _drill(pd)
    t = {
        "VERSION": h(m["version"]),
        "ISSUE_DATE": h(m["issue_date"]),
        "FACTS_AS_AT": h(m["facts_as_at"]),
        "ADVISOR": h(m["advisor_placeholder"]),
        "ILLUS_HTML": illus,
        "DAYS": str(m["days_to_full_application_from_issue"]),
        "NUM_HEADLINE": f"Market access, not engineering, sets {h(possessive(name))} critical path.",
        "NB_ANNEX": "Annexes III and IV" if c["counts"]["critical"] else "Annex III",
        "EUNB": f"EUR {c['eu_revenue_needing_notified_body_m']:.0f}m",
        "NB_CLASSES": nb_classes_phrase(pd),
        "READINESS": f"{dg['portfolio_readiness_index'] * 100:.0f}%",
        "NFAM_TEXT": f"{nfam} product famil{'y' if nfam == 1 else 'ies'}",
        "WEAKEST": h(DOMAIN_PHRASE.get(wid, wid)),
        "WEAKEST_PCT": f"{wval * 100:.0f}%",
        "BASELINE_DATE": h(dg["baseline_date"]),
        "ONEOFF": f"EUR {tot['one_off_total_incl_contingency'] / 1e6:.1f}m",
        "RUN": f"EUR {tot['run_2028'] / 1e6:.1f}m",
        "ONEOFF_PCT": f"{cm['one_off_pct_of_revenue'] * 100:.2f}%",
        "CONTINGENCY_PCT": f"{tot['contingency_rate'] * 100:.0f}%",
        "DRILL_VALUE": h(drill_v), "DRILL_TEXT": h(drill_t), "DRILL_SRC": h(drill_s),
        "FICTION_NOTE": fiction,
        "STEERCO1": js_dq(m["steerco_1"]),
        "PENDING_LABEL": js_dq(pending_label),
    }
    urls = dict(urls or {})
    local_links = dict(local_links or {})
    ref_urls = load_reference_urls()
    files = dict(files or {})
    for did in CARD_IDS:
        u = urls.get(did) or local_links.get(did) or ""
        if not u and did in SHARED_HOSTED:
            u = m.get("knowledge_base_url", "") if did == "KB" else ref_urls.get(did, "")
        t[f"URL:{did}"] = js_dq(u)
    t["FILE:D10"] = js_dq(files.get("D10", FILE_NOTE))
    t["FILE:D11"] = js_dq(files.get("D11", FILE_NOTE))
    return t


def render(pack_data, urls=None, template_html=None, pending_label=PENDING_NEW_CLIENT, local_links=None, files=None):
    if template_html is None:
        template_html = (TEMPLATES / "portal.html").read_text(encoding="utf-8")
    return fill(template_html, tokens(pack_data, urls, pending_label, local_links, files), "portal template")


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    pd = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    urls = json.loads(Path(argv[3]).read_text(encoding="utf-8")) if len(argv) > 3 else {}
    pending = PENDING_REFERENCE if urls else PENDING_NEW_CLIENT
    Path(argv[2]).parent.mkdir(parents=True, exist_ok=True)
    Path(argv[2]).write_text(render(pd, urls, pending_label=pending), encoding="utf-8")


if __name__ == "__main__":
    main(sys.argv)
