"""Excel workbooks of the CRA readiness pack, regenerated for any client from pack_data.json.

    from workbooks import build_all              # or: from pack.engine.workbooks import build_all
    paths = build_all("pack/data/pack_data.json", "pack/out/excel")

D10  <codename> - CRA Business Case and Cost Model.xlsx          (d10.build)
D11  <codename> - CRA Obligations Register and Programme Tracker.xlsx  (d11.build)

Each builder writes live formulas with openpyxl; recalculate() then fills cached values with LibreOffice
headless (on a copy) so viewers that do not recalculate still show numbers. Client narrative that pack_data
does not carry can be supplied as `workbook_text` (inside pack_data or a sidecar workbook_text.json next to it);
without it the builders fall back to generic text derived from pack_data.

CLI:  python3 -m pack.engine.workbooks <pack_data.json> <out_dir> [--no-recalc]
"""
from pathlib import Path

from . import d10, d11
from .recalc import recalculate

__all__ = ["build_all", "recalculate", "d10", "d11", "BUILDERS"]

BUILDERS = (d10.build, d11.build)


class WorkbookFormulaError(RuntimeError):
    pass


def build_all(pack_data_path, out_dir, recalc=True, strict=True):
    """Build D10 and D11 from pack_data into out_dir; recalculate each to populate cached values.

    Returns the list of written paths. With strict=True a formula error (#REF!, #VALUE!, #DIV/0!, ...)
    after recalculation raises WorkbookFormulaError. Reports are kept on build_all.reports."""
    paths, reports = [], {}
    out_dir = Path(out_dir)
    for builder in BUILDERS:
        for p in builder(pack_data_path, out_dir):
            if recalc:
                rep = recalculate(p)
                reports[p.name] = rep
                if strict and rep["total_errors"]:
                    raise WorkbookFormulaError(f"{p.name}: {rep['total_errors']} formula errors {rep['error_summary']}")
            paths.append(p)
    build_all.reports = reports
    return paths


build_all.reports = {}
