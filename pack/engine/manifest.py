"""Re-skin manifest for the hosted deliverables (decks, docs, dashboard, one-pagers).

Hosted deliverables live on claude.ai and cannot be regenerated locally. This writes:
  RESKIN.md           per-deliverable tables of reference value -> client value, plus how to update each artifact type
  reskin_values.json  the same mapping, machine-readable, for a Claude session to apply
Usage: python3 pack/engine/manifest.py <client pack_data.json> <out_dir> [reference pack_data.json]
"""
import json
import sys
from collections import OrderedDict
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from reskin_common import (PACK, DOMAIN_PHRASE, SHARED_HOSTED, is_fictional, load_reference_pack_data,  # noqa: E402
                           load_reference_urls, nb_classes_phrase, weakest_domain)

DELIVERABLES = OrderedDict([
    ("D01", ("Board briefing deck", "Slides", "briefs/D01-board-deck.md")),
    ("D02", ("SteerCo #1 pack", "Slides", "briefs/D02-steerco-deck.md")),
    ("D03", ("Engineering training deck", "Slides", "briefs/D03-training-deck.md")),
    ("D04", ("CRA on a page (two one-pagers)", "Design", "briefs/D04-one-pagers.md")),
    ("D05", ("Communication pack", "Docs", "briefs/D05-communication-pack.md")),
    ("D07", ("Survey and interview instruments", "Docs", "briefs/D07-survey-instruments.md")),
    ("D09", ("Programme dashboard", "Dashboard", "briefs/D09-programme-dashboard.md")),
    ("D14", ("Compliance templates kit", "Docs", "briefs/D14-compliance-templates-kit.md")),
    ("D06", ("Research report: State of CRA readiness 2026", "Docs", "briefs/D06-research-report.md")),
    ("DS", ("Advisory design system", "Design System", "briefs/DS-design-system.md")),
    ("KB", ("Engineering compliance knowledge base", "Page", None)),
])
ORDER = ["D09", "D01", "D04", "D02", "D05", "D07", "D03", "D14", "D06"]
ALL_CLIENT = ["D01", "D02", "D03", "D04", "D05", "D07", "D09", "D14"]

TYPE_HOWTO = OrderedDict([
    ("Slides", [
        "Never edit the reference artifact. Read it (Artifact tool, action read), then either re-run its brief against this client's "
        "`data/DATA_SUMMARY.md` to create a fresh deck from the Slides type, or publish a copy as a new artifact and edit the copy.",
        "Apply the replacements in `reskin_values.json` longest string first, exact match, on slide text, speaker notes and chart labels.",
        "Rebuild every chart from `data/pack_data.json` (paths are given per value below); never scale old charts by hand.",
        "Re-read every action title: a title that was true for the reference client (for example that market access sets the critical path) "
        "must still be true for this client, or be rewritten.",
    ]),
    ("Design", [
        "Copy the reference design into a new artifact, apply the replacements, then check every frame for text overflow: client names, "
        "product names and numbers change length.",
        "Print-preview both pages (A4 and Letter) before sharing.",
    ]),
    ("Docs", [
        "Duplicate the document (Claude Docs connector) or create a new doc from the brief; do not edit the reference doc.",
        "Work tab by tab: apply the replacements, then rewrite tables that list products, stakeholders or dates from `data/pack_data.json` "
        "(`client.product_families`, `stakeholders`, `programme.milestones`).",
        "Search the finished doc for every string in `must_not_remain` before sharing.",
    ]),
    ("Dashboard", [
        "Create the client's dashboard from the Dashboard type or a copy of the reference, then load its data from `data/pack_data.json`: "
        "`kpis`, `kpi_trajectories`, `diagnostic.family_readiness_index`, `cost_model.monthly_plan`, `programme.milestones`, `risks`, `issues`.",
        "Where the dashboard keeps rows in its database, write them with ArtifactData (batch) rather than editing the page source.",
    ]),
    ("Design System", ["Shared and white-label: no client values. Re-use the same URL unless the client wants its own brand tokens."]),
    ("Page", ["Shared regulatory content: no client values. Re-use the same URL."]),
])


def _pct(x, nd=0):
    return f"{x * 100:.{nd}f}%"


def _m(x_eur, nd=1):
    return f"EUR {x_eur / 1e6:.{nd}f}m"


def _int(n):
    return f"{n:,}"


def scalar_values(pd):
    """key -> (label, display value, pack_data path, deliverables)."""
    m, c, dg, cm, ex = pd["meta"], pd["client"], pd["diagnostic"], pd["cost_model"], pd["exposure"]
    tot, sc = cm["base_totals"], cm["scenarios"]
    wid, wval = weakest_domain(pd)
    cnt = c["counts"]
    code = m["programme_codename"]
    rag = pd["programme"]["overall_rag"]
    v = OrderedDict()

    def add(key, label, val, path, dels):
        v[key] = (label, val, path, dels)
    add("client_name", "Client name", m["illustrative_client"], "meta.illustrative_client", ALL_CLIENT)
    add("codename", "Programme codename", code, "meta.programme_codename", ALL_CLIENT)
    add("codename_short", "Codename (short form)", code.replace("Project ", "", 1), "meta.programme_codename", ALL_CLIENT)
    add("fictional_tag", "Illustrative / fictional tag", "Illustrative" if is_fictional(pd) else "(remove the 'Illustrative' tags)", "cost_model.label", ALL_CLIENT)
    add("issue_date", "Pack issue date", m["issue_date"], "meta.issue_date", ALL_CLIENT + ["D06"])
    add("board_date", "Board meeting", m["board_meeting"], "meta.board_meeting", ["D01", "D02", "D04", "D05", "D09"])
    add("steerco_1", "SteerCo #1 date", m["steerco_1"], "meta.steerco_1", ["D02", "D05", "D09"])
    add("kickoff", "Programme kickoff", pd["programme"]["kickoff"], "programme.kickoff", ["D02", "D05"])
    add("baseline_date", "Diagnostic baseline date", dg["baseline_date"], "diagnostic.baseline_date", ["D01", "D02", "D09"])
    add("days_issue", "Days from issue to 11 Dec 2027", str(m["days_to_full_application_from_issue"]), "meta.days_to_full_application_from_issue", ["D01", "D04", "D06", "D09"])
    add("days_board", "Days from board to 11 Dec 2027", str(m["days_to_full_application_from_board"]), "meta.days_to_full_application_from_board", ["D01", "D04"])
    add("hq", "Headquarters / main establishment", c["hq"], "client.hq", ["D01", "D05"])
    add("employees", "Employees", _int(c["employees"]), "client.employees", ["D01", "D05", "D07"])
    add("engineers", "Engineers", _int(c["engineers"]), "client.engineers", ["D01", "D03", "D07", "D09"])
    add("suppliers", "In-scope suppliers", str(c["suppliers_in_scope"]), "client.suppliers_in_scope", ["D01", "D02", "D07", "D09"])
    add("installed_base", "Connected devices in the field", f"{c['installed_base_m']}m", "client.installed_base_m", ["D01", "D05"])
    add("revenue", "Group revenue", f"EUR {c['revenue_m']:,}m", "client.revenue_m", ["D01", "D04"])
    add("eu_revenue", "EU revenue (total)", f"EUR {c['eu_revenue_m']:.0f}m", "client.eu_revenue_m", ["D01", "D04"])
    add("eu_in_scope", "EU revenue from in-scope products", f"EUR {c['eu_revenue_in_scope_products_m']:.0f}m", "client.eu_revenue_in_scope_products_m", ["D01", "D04", "D09"])
    add("eu_nb", "EU revenue needing a notified body", f"EUR {c['eu_revenue_needing_notified_body_m']:.0f}m", "client.eu_revenue_needing_notified_body_m", ["D01", "D02", "D04", "D05", "D09"])
    add("nb_classes", "Classes needing a notified body (phrase)", nb_classes_phrase(pd), "client.counts", ["D01", "D04", "D05"])
    add("eu_nb_share", "Notified-body revenue as share of group revenue", _pct(c["eu_revenue_needing_notified_body_share_of_group"]), "client.eu_revenue_needing_notified_body_share_of_group", ["D01", "D09"])
    add("readiness", "Portfolio readiness index (baseline)", _pct(dg["portfolio_readiness_index"]), "diagnostic.portfolio_readiness_index", ["D01", "D02", "D04", "D09"])
    add("weakest_domain", "Weakest diagnostic domain", f"{DOMAIN_PHRASE.get(wid, wid)} ({_pct(wval)})", "diagnostic.domain_readiness_index", ["D01", "D02", "D09"])
    add("readiness_by_bu", "Readiness by business unit", "; ".join(f"{k} {_pct(x)}" for k, x in dg["bu_readiness_index"].items()), "diagnostic.bu_readiness_index", ["D01", "D09"])
    add("readiness_by_class", "Readiness by class", "; ".join(f"{k} {_pct(x)}" for k, x in dg["class_readiness_index"].items()), "diagnostic.class_readiness_index", ["D01", "D09"])
    add("one_off", "One-off investment to Dec 2027 (base, incl. contingency)", _m(tot["one_off_total_incl_contingency"]), "cost_model.base_totals.one_off_total_incl_contingency", ["D01", "D02", "D04", "D05", "D09"])
    add("run", "Run cost a year from 2028", _m(tot["run_2028"]), "cost_model.base_totals.run_2028", ["D01", "D04", "D09"])
    add("q4_2026", "Q4 2026 spend incl. contingency", _m(tot["q4_2026_incl_contingency"], 2), "cost_model.base_totals.q4_2026_incl_contingency", ["D01", "D02", "D09"])
    add("y2027", "2027 spend incl. contingency", _m(tot["y2027_incl_contingency"], 2), "cost_model.base_totals.y2027_incl_contingency", ["D01", "D02", "D09"])
    add("contingency", "Contingency rate", _pct(tot["contingency_rate"]), "cost_model.base_totals.contingency_rate", ["D01", "D09"])
    add("scenario_range", "Scenario range one-off (low-high)",
        f"{_m(sc['low']['totals']['one_off_total_incl_contingency'])}-{_m(sc['high']['totals']['one_off_total_incl_contingency'])[4:]}" if "low" in sc and "high" in sc else "n/a",
        "cost_model.scenarios.*.totals.one_off_total_incl_contingency", ["D01", "D09"])
    add("one_off_pct", "One-off as share of annual revenue", _pct(cm["one_off_pct_of_revenue"], 2), "cost_model.one_off_pct_of_revenue", ["D01", "D04"])
    add("fte_years", "Engineering remediation effort", f"{cm['engineering_fte_years']:.1f} FTE-years", "cost_model.engineering_fte_years", ["D01", "D02"])
    add("spend_to_date", "Spend to date vs plan", next((k["display"] for k in pd["kpis"] if k["value"] == cm["actual_to_date"]["actual"] and "EUR" in str(k["display"])),
        f"{_m(cm['actual_to_date']['actual'], 2)} vs {_m(cm['actual_to_date']['plan'], 2)}"), "cost_model.actual_to_date", ["D02", "D09"])
    for i, tier in enumerate(ex["fine_tiers"], 1):
        add(f"fine_tier{i}", f"Maximum fine, tier {i}", f"EUR {tier['example_group_max_m']:.0f}m", f"exposure.fine_tiers[{i - 1}]", ["D01", "D03", "D04"])
    add("families", "Product families in scope", str(cnt["families"]), "client.counts.families", ALL_CLIENT)
    add("skus", "SKUs in scope", str(cnt["skus"]), "client.counts.skus", ["D01", "D09"])
    add("n_default", "Default families (incl. provisional)", str(cnt["default"]), "client.counts.default", ["D01", "D04", "D09"])
    add("n_provisional", "Provisional / borderline families", str(cnt["provisional"]), "client.counts.provisional", ["D01", "D02", "D09"])
    add("n_class_i", "Class I families", str(cnt["class_i"]), "client.counts.class_i", ["D01", "D04", "D09"])
    add("n_class_ii", "Class II families", str(cnt["class_ii"]), "client.counts.class_ii", ["D01", "D04", "D09"])
    add("n_critical", "Critical (Annex IV) families", str(cnt["critical"]), "client.counts.critical", ["D01", "D04", "D09"])
    add("n_nb", "Families needing a notified body", str(cnt["class_i"] + cnt["class_ii"] + cnt["critical"]), "exposure.market_access.families", ["D01", "D02", "D04", "D09"])
    add("n_legacy", "Legacy lines", str(cnt["legacy_lines"]), "client.counts.legacy_lines", ["D01", "D02"])
    ld = ex["legacy_decision"]
    add("legacy_eu_revenue", "Legacy lines still sold: EU revenue", f"EUR {ld['eu_revenue_m']}m", "exposure.legacy_decision.eu_revenue_m", ["D01", "D02"])
    add("legacy_remediation", "Legacy remediation estimate", f"EUR {ld['remediation_cost_estimate_m']}m", "exposure.legacy_decision.remediation_cost_estimate_m", ["D01", "D02"])
    add("overall_rag", "Overall programme RAG", rag, "programme.overall_rag", ["D02", "D09"])
    return v


def text_blocks(pd):
    """Longer texts that are replaced wholesale, not string by string."""
    s = pd["storyline"]
    out = OrderedDict()
    out["governing_thought"] = ("Governing thought", s["governing_thought"], "storyline.governing_thought", ["D01", "D04"])
    for k in ("situation", "complication", "question", "answer"):
        out[f"scqa_{k}"] = (f"SCQA {k}", s["scqa"][k], f"storyline.scqa.{k}", ["D01"])
    for i, p in enumerate(s["pillars"]):
        out[f"pillar_{i + 1}"] = (f"Pillar {i + 1}", f"{p['title']}: {p['message']}", f"storyline.pillars[{i}]", ["D01", "D04", "D05"])
    out["overall_status"] = ("Overall programme status", pd["programme"]["overall_status"], "programme.overall_status", ["D02", "D09"])
    out["legacy_recommendation"] = ("Legacy-line recommendation", pd["exposure"]["legacy_decision"]["recommendation"], "exposure.legacy_decision.recommendation", ["D01", "D02"])
    for d in pd["decisions"]["board"]:
        out[f"board_{d['id']}"] = (f"Board decision {d['id']}", f"{d['decision']} {d['detail']}", "decisions.board", ["D01", "D04"])
    return out


def _by_class(fams):
    groups = OrderedDict((k, []) for k in ("Default", "Default (provisional)", "Class I", "Class II", "Critical"))
    for f in fams:
        groups.setdefault(f["cra_class"], []).append(f)
    return groups


def product_mapping(ref, new):
    """Pair reference products with client products of the same class, in portfolio order."""
    rg, ng = _by_class(ref["client"]["product_families"]), _by_class(new["client"]["product_families"])
    pairs = []
    for k in rg:
        r, n = rg.get(k, []), ng.get(k, [])
        for i in range(max(len(r), len(n))):
            pairs.append(OrderedDict(cls=k, old=r[i]["name"] if i < len(r) else None, old_id=r[i]["id"] if i < len(r) else None,
                                     new=n[i]["name"] if i < len(n) else None, new_id=n[i]["id"] if i < len(n) else None))
    for k in ng:
        if k not in rg:
            for f in ng[k]:
                pairs.append(OrderedDict(cls=k, old=None, old_id=None, new=f["name"], new_id=f["id"]))
    return pairs


def bu_mapping(ref, new):
    rb, nb = ref["client"]["business_units"], new["client"]["business_units"]
    out = []
    for i in range(max(len(rb), len(nb))):
        out.append(OrderedDict(old=f"{rb[i]['name']} ({rb[i]['id']})" if i < len(rb) else None,
                               new=f"{nb[i]['name']} ({nb[i]['id']})" if i < len(nb) else None))
    return out


def legacy_names(pd):
    return [l["name"] for l in pd["client"]["legacy_lines"]]


def build(pd, ref=None, urls=None):
    ref = ref or load_reference_pack_data()
    ref_urls = load_reference_urls()
    urls = urls or {}
    sv_old, sv_new = scalar_values(ref), scalar_values(pd)
    tb_old, tb_new = text_blocks(ref), text_blocks(pd)
    products = product_mapping(ref, pd)
    bus = bu_mapping(ref, pd)
    values = []
    for k, (label, new_val, path, dels) in sv_new.items():
        old_val = sv_old[k][1] if k in sv_old else None
        values.append(OrderedDict(key=k, label=label, old=old_val, new=new_val, changed=old_val != new_val, source=path, deliverables=dels))
    blocks = []
    for k in list(tb_new) + [k for k in tb_old if k not in tb_new]:
        o, n = tb_old.get(k), tb_new.get(k)
        src = (n or o)
        blocks.append(OrderedDict(key=k, label=src[0], old=o[1] if o else None, new=n[1] if n else "(remove)", source=src[2], deliverables=src[3]))
    # Exact string pairs that are distinctive enough to apply mechanically. Everything else (dates, percentages, counts)
    # can collide with regulatory text (e.g. the steerco date and the facts date are both 30 Oct 2026 in the reference),
    # so those stay in `values` for review in context.
    safe = ("client_name", "codename", "codename_short", "hq", "revenue", "eu_revenue", "eu_in_scope", "eu_nb", "one_off",
            "run", "q4_2026", "y2027", "scenario_range", "fte_years", "spend_to_date")
    replacements = []
    for v in values:
        if v["changed"] and v["old"] and v["key"] in safe:
            replacements.append(OrderedDict(old=v["old"], new=v["new"], key=v["key"]))
    for p in products:
        if p["old"] and p["new"]:
            replacements.append(OrderedDict(old=p["old"], new=p["new"], key=f"product:{p['cls']}"))
    for b in bus:
        if b["old"] and b["new"]:
            replacements.append(OrderedDict(old=b["old"].rsplit(" (", 1)[0], new=b["new"].rsplit(" (", 1)[0], key="business_unit"))
    replacements.sort(key=lambda r: -len(r["old"]))
    old_products = [f["name"] for f in ref["client"]["product_families"]]
    must_not_remain = [ref["meta"]["illustrative_client"], ref["meta"]["programme_codename"]] + old_products + legacy_names(ref)
    new_names = {pd["meta"]["illustrative_client"], pd["meta"]["programme_codename"]} | {f["name"] for f in pd["client"]["product_families"]}
    must_not_remain = [s for s in must_not_remain if s not in new_names]
    dels = OrderedDict()
    for did, (title, typ, brief) in DELIVERABLES.items():
        shared = did in SHARED_HOSTED
        dels[did] = OrderedDict(title=title, type=typ, brief=brief, shared=shared,
                                reference_url=(ref["meta"]["knowledge_base_url"] if did == "KB" else ref_urls.get(did, "")),
                                client_url=urls.get(did) or (ref_urls.get(did, "") if shared else ""))
    return OrderedDict(
        schema="cra-pack-reskin/1",
        reference=OrderedDict(client=ref["meta"]["illustrative_client"], codename=ref["meta"]["programme_codename"], pack_data="pack/data/pack_data.json"),
        client=OrderedDict(name=pd["meta"]["illustrative_client"], codename=pd["meta"]["programme_codename"], fictional=is_fictional(pd),
                           facts_as_at=pd["meta"]["facts_as_at"],
                           pack_data="data/pack_data.json", data_summary="data/DATA_SUMMARY.md"),
        order=ORDER, deliverables=dels, values=values, text_blocks=blocks, products=products, business_units=bus,
        legacy_lines=OrderedDict(old=legacy_names(ref), new=legacy_names(pd)),
        replacements=replacements, must_not_remain=must_not_remain,
    )


def _cell(s):
    return "—" if s is None else str(s).replace("|", "\\|").replace("\n", " ")


def to_markdown(rv):
    cl, rf = rv["client"], rv["reference"]
    L = [f"# Re-skin manifest — {cl['name']} ({cl['codename']})", "",
         f"Reference pack: {rf['client']} ({rf['codename']}). Hosted deliverables (decks, docs, dashboard, one-pagers) live on claude.ai "
         "and cannot be regenerated locally; this manifest lists every client-specific value to change in each one. "
         "`reskin_values.json` holds the same mapping for a Claude session to apply.", "",
         "Regenerated locally by `reskin.py` (no manual work): `data/` (pack_data.json, DATA_SUMMARY.md), `excel/` (D10, D11), "
         "`diagnostic/` (D08), `portal/` (D12), `classifier/` (D13).", "",
         "Two kinds of change: `replacements` in the JSON are distinctive strings (names, codename, money) that can be applied "
         "mechanically, longest first; the per-deliverable tables below also list dates, percentages and counts, which must be "
         "changed by reading the sentence they sit in (a reference date or percentage can also appear in regulatory text).", "",
         "## Recommended order", ""]
    for i, did in enumerate(rv["order"], 1):
        d = rv["deliverables"][did]
        why = {"D09": "the dashboard is the numeric source the decks quote",
               "D01": "the board story; everything else repeats its numbers",
               "D04": "condensed from D01", "D02": "uses the D09 KPIs and D01 decisions",
               "D05": "messages and calendar follow the board date", "D07": "client names, BUs and headcounts only",
               "D03": "product examples only", "D14": "worked example product only",
               "D06": "market-level; only the days-to-deadline count may change"}.get(did, "")
        L.append(f"{i}. **{did} {d['title']}** ({d['type']}) — {why}")
    L += [f"{len(rv['order']) + 1}. Record each new URL in `pack/clients/<slug>/urls.json` (keys D01…D14) and rerun `reskin.py`: "
          "the portal then links the client's own artifacts instead of showing \"To be produced for this client\".",
          f"{len(rv['order']) + 2}. QA: search every finished artifact for the strings under *Must not remain* below.", "",
          "## How to update each artifact type", ""]
    for typ, steps in TYPE_HOWTO.items():
        L.append(f"**{typ}**")
        L += [f"- {s}" for s in steps]
        L.append("")
    L += ["## Product families (reference → client, paired by class)", "", "| Class | Reference product | Client product |", "|---|---|---|"]
    for p in rv["products"]:
        L.append(f"| {p['cls']} | {_cell(p['old'] and p['old'] + ' (' + p['old_id'] + ')')} | {_cell(p['new'] and p['new'] + ' (' + p['new_id'] + ')')} |")
    L += ["", "A dash means there is no counterpart: delete the reference product's content, or add the client product where the "
          "reference had none. Examples that use one product (D03 training, D14 worked example) should use the paired product of the same class.", "",
          "| Business unit (reference) | Business unit (client) |", "|---|---|"]
    for b in rv["business_units"]:
        L.append(f"| {_cell(b['old'])} | {_cell(b['new'])} |")
    L += ["", f"Legacy lines — reference: {', '.join(rv['legacy_lines']['old']) or '—'}; client: {', '.join(rv['legacy_lines']['new']) or '—'}.", ""]
    vals = {v["key"]: v for v in rv["values"]}
    for did in rv["order"] + [d for d in rv["deliverables"] if d not in rv["order"]]:
        d = rv["deliverables"][did]
        L.append(f"## {did} — {d['title']} ({d['type']})")
        L.append("")
        meta = [f"Reference: {d['reference_url'] or '—'}"]
        if d["brief"]:
            meta.append(f"brief: `pack/{d['brief']}`")
        meta.append(f"client artifact: {d['client_url'] or 'to be produced'}")
        L.append(" · ".join(meta))
        L.append("")
        if d["shared"]:
            L.append("Shared content with no client values; keep the reference artifact.")
            if did == "D06":
                v = vals["days_issue"]
                L.append(f"Only check the days-to-deadline count: {v['old']} → {v['new']} (if the issue date differs).")
            L.append("")
            continue
        L += ["| Value | Reference | This client | Source in pack_data.json |", "|---|---|---|---|"]
        for v in rv["values"]:
            if did in v["deliverables"]:
                new = v["new"] if v["changed"] else f"{v['new']} (no change)"
                L.append(f"| {v['label']} | {_cell(v['old'])} | {_cell(new)} | `{v['source']}` |")
        L.append("")
        tb = [b for b in rv["text_blocks"] if did in b["deliverables"]]
        if tb:
            L.append("Rewrite these passages in full:")
            L.append("")
            for b in tb:
                L.append(f"- **{b['label']}** (`{b['source']}`): {_cell(b['new'])}")
            L.append("")
        extra = {
            "D02": "Also refresh from pack_data: `kpis` (all displays), `programme.milestones`, `programme.workstreams` (RAG and notes), `risks`, `issues`, `decisions.steerco_1`.",
            "D05": "Also refresh from pack_data: `stakeholders` (map, concerns, messages, owners), calendar dates keyed to `programme.kickoff`, board and SteerCo dates.",
            "D07": "Also refresh: business-unit names in demographic questions, engineer and supplier counts, the works-council gate date if the client has one.",
            "D09": "Load all data from pack_data rather than editing numbers: `kpis`, `kpi_trajectories`, `diagnostic`, `cost_model.monthly_plan`, `programme`, `risks`, `issues`.",
            "D03": "Swap worked examples to the paired client products (see the product table); the regulatory content stays.",
            "D14": "Re-fill the worked example with the paired Class I client product (class, annex item, support period, RDPS, route).",
            "D01": "Rebuild charts (exposure by class, readiness heatmap, cost by workstream, scenarios, Gantt, risk matrix) from pack_data.",
            "D04": "Programme page: phases and milestones from `programme.phases` / `programme.milestones`.",
        }.get(did)
        if extra:
            L += [extra, ""]
    L += ["## Must not remain", "", "After re-skinning, none of these reference strings may appear in a client artifact:", "",
          ", ".join(f"`{s}`" for s in rv["must_not_remain"]), "",
          "## Limits", "",
          "- The programme window is fixed to Q4 2026–Dec 2027 by the cost model periods (Oct 2026 – Dec 2027 monthly plan).",
          "- Regulatory content (facts, diagnostic questions, classifier categories, knowledge base) is shared and dated "
          f"to {rv['client']['facts_as_at']}; re-verify before issue (notified bodies, harmonised standards, guidance, national laws).",
          "- Text replacements are exact strings. Numbers embedded in charts, images or rephrased sentences must be found by reading.", ""]
    return "\n".join(L)


def write(pd, out_dir, ref=None, urls=None):
    out_dir = Path(out_dir)
    out_dir.mkdir(parents=True, exist_ok=True)
    rv = build(pd, ref, urls)
    (out_dir / "reskin_values.json").write_text(json.dumps(rv, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    (out_dir / "RESKIN.md").write_text(to_markdown(rv), encoding="utf-8")
    return rv


def main(argv):
    if len(argv) < 3:
        sys.exit(__doc__)
    pd = json.loads(Path(argv[1]).read_text(encoding="utf-8"))
    ref = json.loads(Path(argv[3]).read_text(encoding="utf-8")) if len(argv) > 3 else None
    write(pd, argv[2], ref)


if __name__ == "__main__":
    main(sys.argv)
