"""Render the CRA framework crosswalk (D15) from pack/data/crosswalk.json.

The crosswalk is regulatory content shared by every client, so it is not part of the client re-skin.
Usage: python3 pack/engine/render_crosswalk.py [crosswalk.json] [out_dir]
Writes <out_dir>/index.html (the interactive page) and <out_dir>/cra-framework-crosswalk.csv.
"""
import csv, io, json, sys
from pathlib import Path

PACK = Path(__file__).resolve().parents[1]
RANK = {"strong": 3, "partial": 2, "weak": 1, "none": 0}


def validate(xw):
    fws = {f["id"] for f in xw["frameworks"]}
    rqs = {r["id"] for r in xw["requirements"]}
    seen = set()
    for m in xw["mappings"]:
        if m["fw"] not in fws or m["req"] not in rqs:
            raise ValueError(f"mapping {m['req']}/{m['fw']} references an unknown id")
        if m["coverage"] not in RANK:
            raise ValueError(f"mapping {m['req']}/{m['fw']}: coverage {m['coverage']!r} not in {list(RANK)}")
        if (m["req"], m["fw"]) in seen:
            raise ValueError(f"duplicate mapping {m['req']}/{m['fw']}")
        seen.add((m["req"], m["fw"]))
    missing = [(r, f) for r in rqs for f in fws if (r, f) not in seen]
    if missing:
        raise ValueError(f"{len(missing)} requirement x framework pairs have no mapping, e.g. {missing[:3]}")


def to_csv(xw):
    by = {(m["req"], m["fw"]): m for m in xw["mappings"]}
    label = {c["id"]: c["label"] for c in xw["coverage_scale"]}
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["Requirement ID", "CRA reference", "Requirement"] + [h for f in xw["frameworks"] for h in (f"{f.get('short') or f['name']} coverage", f"{f.get('short') or f['name']} clauses", f"{f.get('short') or f['name']} note")])
    for r in xw["requirements"]:
        row = [r["id"], r["ref"], r["title"]]
        for f in xw["frameworks"]:
            m = by[(r["id"], f["id"])]
            refs = m.get("refs", "") + (" (kit mapping; verify)" if m.get("source") == "kit" and m["coverage"] != "none" else "")
            row += [label[m["coverage"]], refs, m.get("note", "")]
        w.writerow(row)
    return buf.getvalue()


def render(xw, template=None):
    template = template or (PACK / "engine" / "templates" / "crosswalk.html").read_text()
    data = json.dumps(xw, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    assert template.count("/*XW_DATA*/null") == 1
    return template.replace("/*XW_DATA*/null", data)


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else PACK / "data" / "crosswalk.json"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else PACK / "out" / "crosswalk"
    xw = json.loads(src.read_text())
    validate(xw)
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(render(xw))
    (out / "cra-framework-crosswalk.csv").write_text(to_csv(xw))
    print(f"crosswalk: {len(xw['requirements'])} requirements x {len(xw['frameworks'])} frameworks -> {out}")


if __name__ == "__main__":
    main()
