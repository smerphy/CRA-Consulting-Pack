"""python3 -m pack.engine.workbooks <pack_data.json> <out_dir> [--no-recalc]"""
import json
import sys

from . import build_all


def main(argv):
    args = [a for a in argv if not a.startswith("--")]
    if len(args) != 2:
        print(__doc__)
        return 2
    paths = build_all(args[0], args[1], recalc="--no-recalc" not in argv)
    for p in paths:
        rep = build_all.reports.get(p.name)
        print(p, json.dumps({k: rep[k] for k in ("status", "total_formulas", "total_errors")}) if rep else "")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
