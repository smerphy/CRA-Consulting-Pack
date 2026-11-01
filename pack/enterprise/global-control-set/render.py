"""Render the Global Product Security Control Set (module E5).

Reuses validate() and render() from pack/engine/render_crosswalk.py (shared renderer left untouched);
writes its own CSV because the columns differ (controls x regimes, plus the strictest regime).
Usage: python3 render.py [controls.json] [out_dir]   (defaults: ./controls.json, ./site)
Writes <out_dir>/index.html and <out_dir>/global-control-set.csv.
"""
import csv, io, json, sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ENGINE = HERE.parents[1] / "engine"
sys.path.insert(0, str(ENGINE))
from render_crosswalk import RANK, render, validate  # noqa: E402


def strictest(xw, rid, regimes):
    """Highest-coverage regime among `regimes` for control `rid`; ties go to data order (CRA first)."""
    by = {(m["req"], m["fw"]): m["coverage"] for m in xw["mappings"]}
    best = ("none", None)
    for f in xw["frameworks"]:
        if f["id"] in regimes and RANK[by[(rid, f["id"])]] > RANK[best[0]]:
            best = (by[(rid, f["id"])], f["id"])
    return best


def to_csv(xw):
    by = {(m["req"], m["fw"]): m for m in xw["mappings"]}
    label = {c["id"]: c["label"] for c in xw["coverage_scale"]}
    short = {f["id"]: f.get("short") or f["name"] for f in xw["frameworks"]}
    target = xw["meta"].get("default_selected") or list(short)
    buf = io.StringIO()
    w = csv.writer(buf)
    w.writerow(["Control ID", "Group", "Control", "Summary", "Evidence (one artefact, all regimes)", "Build to"]
               + [h for f in xw["frameworks"] for h in (f"{short[f['id']]} coverage", f"{short[f['id']]} clauses", f"{short[f['id']]} note")]
               + [f"Strictest of {', '.join(short[t] for t in target)}"])
    for r in xw["requirements"]:
        row = [r["id"], r["group"], r["title"], r["summary"], r.get("evidence", ""), r.get("strictest", "")]
        for f in xw["frameworks"]:
            m = by[(r["id"], f["id"])]
            row += [label[m["coverage"]], m.get("refs", ""), m.get("note", "")]
        cov, fid = strictest(xw, r["id"], set(target))
        row.append(f"{short[fid]} ({label[cov]})" if RANK[cov] >= 2 else "Not required")
        w.writerow(row)
    return buf.getvalue()


def main():
    src = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "controls.json"
    out = Path(sys.argv[2]) if len(sys.argv) > 2 else HERE / "site"
    xw = json.loads(src.read_text())
    validate(xw)
    out.mkdir(parents=True, exist_ok=True)
    (out / "index.html").write_text(render(xw, (HERE / "template.html").read_text()))
    (out / "global-control-set.csv").write_text(to_csv(xw))
    print(f"global control set: {len(xw['requirements'])} controls x {len(xw['frameworks'])} regimes -> {out}")


if __name__ == "__main__":
    main()
