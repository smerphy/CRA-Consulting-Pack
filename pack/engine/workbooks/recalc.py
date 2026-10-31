"""Populate cached values in an openpyxl-written workbook, as the v1.0 workbooks were finalised.

openpyxl writes formulas without results, so viewers that do not recalculate show blanks. recalculate():
  1. copies the workbook and recalculates the copy with LibreOffice headless (macro: calculateAll + store);
  2. reads every computed value from the copy;
  3. injects those values as cached <v> results into the ORIGINAL file's sheet XML, so formatting, charts,
     tables, validation and conditional formats stay exactly as openpyxl wrote them (a LibreOffice round-trip
     would rewrite them).
The formulas stay live: Excel and LibreOffice recalculate on edit.
"""
import datetime as dt
import os
import re
import shutil
import subprocess
import tempfile
import zipfile
from pathlib import Path
from xml.sax.saxutils import escape

from openpyxl import load_workbook
from openpyxl.utils.datetime import to_excel
from openpyxl.worksheet.formula import ArrayFormula

ERRORS = ("#VALUE!", "#DIV/0!", "#REF!", "#NAME?", "#NULL!", "#NUM!", "#N/A")

_MACRO = """<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE script:module PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "module.dtd">
<script:module xmlns:script="http://openoffice.org/2000/script" script:name="Module1" script:language="StarBasic">
    Sub RecalculateAndSave()
      ThisComponent.calculateAll()
      ThisComponent.store()
      ThisComponent.close(True)
    End Sub
</script:module>"""

CELL_F_RE = re.compile(
    r'<c r="(?P<ref>[A-Z]{1,3}\d+)"(?P<attrs>[^>]*)><f(?P<fattrs>[^>]*)>(?P<f>[^<]*)</f>(?:<v\s*/>|<v>[^<]*</v>)?</c>')


class RecalcError(RuntimeError):
    pass


def _soffice():
    exe = shutil.which("soffice") or shutil.which("libreoffice")
    if not exe:
        raise RecalcError("LibreOffice (soffice) not found on PATH; it is required to populate cached values")
    return exe


def _env():
    env = os.environ.copy()
    env["SAL_USE_VCLPLUGIN"] = "svp"
    return env


def libreoffice_recalc(path, timeout=180):
    """Recalculate the workbook at `path` in place with LibreOffice headless."""
    exe = _soffice()
    path = Path(path).resolve()
    with tempfile.TemporaryDirectory(prefix="lo-profile-") as prof:
        url = Path(prof).as_uri()
        subprocess.run([exe, "--headless", "--terminate_after_init", f"-env:UserInstallation={url}"],
                       capture_output=True, timeout=timeout, env=_env())
        macro_dir = Path(prof) / "user" / "basic" / "Standard"
        if not macro_dir.exists():
            raise RecalcError("LibreOffice did not create a usable profile")
        (macro_dir / "Module1.xba").write_text(_MACRO)
        before = path.stat().st_mtime_ns, path.stat().st_size
        cmd = [exe, "--headless", "--norestore", f"-env:UserInstallation={url}",
               "vnd.sun.star.script:Standard.Module1.RecalculateAndSave?language=Basic&location=application", str(path)]
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout + 15, env=_env())
        if res.returncode != 0:
            raise RecalcError(f"LibreOffice failed: {(res.stderr or '').strip() or res.returncode}")
        if (path.stat().st_mtime_ns, path.stat().st_size) == before:
            raise RecalcError("LibreOffice exited without rewriting the file (another instance running?)")


def computed_values(path, timeout=180):
    """Recalculate a copy of `path`; return {sheet: {cell: value}} of every cell in the recalculated copy."""
    with tempfile.TemporaryDirectory(prefix="recalc-") as tmpdir:
        tmp = Path(tmpdir) / "recalc_copy.xlsx"
        shutil.copy(path, tmp)
        libreoffice_recalc(tmp, timeout=timeout)
        wb = load_workbook(tmp, data_only=True)
        values = {ws.title: {c.coordinate: c.value for row in ws.iter_rows() for c in row} for ws in wb.worksheets}
        wb.close()
    return values


def _sheet_parts(zf):
    wb_xml = zf.read("xl/workbook.xml").decode("utf8")
    rels = zf.read("xl/_rels/workbook.xml.rels").decode("utf8")
    rid_target = dict(re.findall(r'<Relationship[^>]*Id="([^"]+)"[^>]*Target="([^"]+)"', rels))
    rid_target.update({k: v for v, k in re.findall(r'<Relationship[^>]*Target="([^"]+)"[^>]*Id="([^"]+)"', rels)})
    out = {}
    for name, rid in re.findall(r'<sheet[^>]*name="([^"]+)"[^>]*r:id="([^"]+)"', wb_xml):
        tgt = rid_target[rid].lstrip("/")
        if not tgt.startswith("xl/"):
            tgt = "xl/" + tgt
        out[name.replace("&amp;", "&")] = tgt
    return out


def _encode(value):
    """(t attribute or None, <v> text) for a cached value."""
    if value is None:
        return "str", ""
    if isinstance(value, bool):
        return "b", "1" if value else "0"
    if isinstance(value, (dt.datetime, dt.date)):
        return None, repr(float(to_excel(value)))
    if isinstance(value, (int, float)):
        if isinstance(value, float) and value.is_integer() and abs(value) < 1e15:
            return None, str(int(value))
        return None, repr(value)
    s = str(value)
    if s in ERRORS:
        return "e", s
    return "str", escape(s)


def inject_cached_values(path, values):
    """Write computed values into the formula cells of the openpyxl-written file (in place)."""
    path = str(path)
    tmp_out = path + ".tmp"
    with zipfile.ZipFile(path) as zin:
        part_to_sheet = {v: k for k, v in _sheet_parts(zin).items()}
        with zipfile.ZipFile(tmp_out, "w", zipfile.ZIP_DEFLATED) as zout:
            for item in zin.infolist():
                data = zin.read(item.filename)
                if item.filename == "docProps/app.xml":
                    data = re.sub(rb"<Application>[^<]*</Application>",
                                  b"<Application>Microsoft Excel Compatible</Application>", data)
                if item.filename in part_to_sheet:
                    vals = values.get(part_to_sheet[item.filename], {})

                    def repl(m):
                        ref = m.group("ref")
                        attrs = re.sub(r'\st="[^"]*"', "", m.group("attrs"))
                        t, v = _encode(vals.get(ref))
                        tattr = f' t="{t}"' if t else ""
                        return f'<c r="{ref}"{attrs}{tattr}><f{m.group("fattrs")}>{m.group("f")}</f><v>{v}</v></c>'

                    data = CELL_F_RE.sub(repl, data.decode("utf8")).encode("utf8")
                zout.writestr(item, data)
    os.replace(tmp_out, path)


def scan(values, formulas_wb_path):
    """Count formulas and error results; return a report dict."""
    wb = load_workbook(formulas_wb_path)
    n, errs = 0, {}
    for ws in wb.worksheets:
        for row in ws.iter_rows():
            for c in row:
                v = c.value.text if isinstance(c.value, ArrayFormula) else c.value
                if isinstance(v, str) and v.startswith("="):
                    n += 1
                    r = values.get(ws.title, {}).get(c.coordinate)
                    if isinstance(r, str) and r in ERRORS:
                        errs.setdefault(r, []).append(f"{ws.title}!{c.coordinate}")
    wb.close()
    total = sum(len(v) for v in errs.values())
    return {"status": "success" if total == 0 else "errors_found", "total_formulas": n, "total_errors": total,
            "error_summary": errs}


def recalculate(path, timeout=180):
    """Recalculate `path` with LibreOffice (on a copy) and inject the cached values into `path`.

    Returns a report: {"status": "success"|"errors_found", "total_formulas", "total_errors", "error_summary"}.
    Values are injected even when errors are found, so the report can be inspected; callers decide."""
    values = computed_values(path, timeout=timeout)
    report = scan(values, path)
    inject_cached_values(path, values)
    return report
