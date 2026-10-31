"""Regression and generality tests for the client re-skin pipeline.

Run:  python3 -m pytest pack/tests      (or, without pytest:  python3 pack/tests/test_reskin.py)
"""
import copy
import json
import subprocess
import sys
import tempfile
from pathlib import Path

import yaml

PACK = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACK))
sys.path.insert(0, str(PACK / "engine"))

import reskin  # noqa: E402
import render_classifier  # noqa: E402
import render_diagnostic  # noqa: E402
import render_portal  # noqa: E402
from validate import IntakeError  # noqa: E402

EG = PACK / "clients" / "example-group" / "client.yaml"
NW = PACK / "clients" / "northwind-devices" / "client.yaml"
TEMPLATE = PACK / "clients" / "_template" / "client.yaml"
LEFTOVERS = ("Example Group", "Rampart", "L2 Smart Lock", "SG-900", "T200")
# RESKIN.md and reskin_values.json map reference values to client values, so they name the reference on purpose.
MAPPING_FILES = ("RESKIN.md", "reskin_values.json")


def _read(p):
    return Path(p).read_text(encoding="utf-8")


def _ref_pack_data():
    return json.loads(_read(PACK / "data" / "pack_data.json"))


# ---------------- (a) Example Group byte identity ----------------
def test_example_group_data_identical():
    with tempfile.TemporaryDirectory() as d:
        subprocess.run([sys.executable, str(PACK / "engine" / "build.py"), str(EG), d], check=True, capture_output=True)
        assert (Path(d) / "pack_data.json").read_bytes() == (PACK / "data" / "pack_data.json").read_bytes()
        assert (Path(d) / "DATA_SUMMARY.md").read_bytes() == (PACK / "data" / "DATA_SUMMARY.md").read_bytes()


def test_example_group_diagnostic_identical():
    assert render_diagnostic.render(_ref_pack_data()) == _read(PACK / "out" / "diagnostic" / "index.html")


def test_example_group_portal_identical():
    urls = json.loads(_read(PACK / "out" / "urls.json"))
    out = render_portal.render(_ref_pack_data(), urls, pending_label=render_portal.PENDING_REFERENCE)
    assert out == _read(PACK / "out" / "portal" / "index.html")


def test_example_group_classifier_identical():
    presets = yaml.safe_load(_read(EG))["classifier"]["presets"]
    assert render_classifier.render(_ref_pack_data(), presets=presets) == _read(PACK / "out" / "classifier" / "index.html")


def test_example_group_full_run_identical():
    with tempfile.TemporaryDirectory() as d:
        reskin.run(EG, d, skip_excel=True, quiet=True)
        for sub in ("diagnostic", "portal", "classifier"):
            assert (Path(d) / sub / "index.html").read_bytes() == (PACK / "out" / sub / "index.html").read_bytes(), sub


# ---------------- (b) Northwind: full build, no reference leftovers ----------------
def _texts(out):
    for p in sorted(Path(out).rglob("*")):
        if not p.is_file() or p.name in MAPPING_FILES:
            continue
        if p.suffix == ".xlsx":
            import openpyxl
            wb = openpyxl.load_workbook(p)
            cells = [str(c.value) for ws in wb.worksheets for row in ws.iter_rows() for c in row if c.value is not None]
            yield p, "\n".join([ws.title for ws in wb.worksheets] + cells)
        elif p.suffix in (".json", ".md", ".html", ".csv", ".txt"):
            yield p, _read(p)


def test_northwind_full_build_no_leftovers():
    with tempfile.TemporaryDirectory() as d:
        res = reskin.run(NW, d, quiet=True)
        for sub in ("data/pack_data.json", "data/DATA_SUMMARY.md", "diagnostic/index.html", "portal/index.html",
                    "classifier/index.html", "RESKIN.md", "reskin_values.json"):
            assert (Path(d) / sub).exists(), sub
        found = []
        for p, text in _texts(d):
            for s in LEFTOVERS:
                if s in text:
                    found.append(f"{p.relative_to(d)}: {s}")
        assert not found, "reference strings left in Northwind outputs:\n" + "\n".join(found)
        pd = json.loads(_read(Path(d) / "data" / "pack_data.json"))
        assert pd["meta"]["illustrative_client"] == "Northwind Devices"
        assert {f["cra_class"] for f in pd["client"]["product_families"]} >= {"Default", "Class I", "Class II", "Critical"}
        portal = _read(Path(d) / "portal" / "index.html")
        assert "To be produced for this client" in portal and "../diagnostic/index.html" in portal
        assert "claude.ai/artifact/PR4UPgQDqUmwV8sR7AnZC9" not in portal  # no link to the reference board deck
        cls = _read(Path(d) / "classifier" / "index.html")
        assert 'cat: "IV2"' in cls and 'data-preset="KS1"' in cls
        if res["excel"] and isinstance(res["excel"], list):
            assert len(res["excel"]) >= 2, res["excel"]


def test_template_intake_builds():
    with tempfile.TemporaryDirectory() as d:
        reskin.run(TEMPLATE, d, skip_excel=True, quiet=True)
        assert (Path(d) / "portal" / "index.html").exists()


# ---------------- (c) intake validation ----------------
def test_validation_rejects_broken_intake():
    intake = yaml.safe_load(_read(NW))
    bad = copy.deepcopy(intake)
    bad["client"]["product_families"][0]["bu"] = "XX"
    bad["client"]["product_families"][1]["cra_class"] = "Class III"
    bad["programme"]["waves"][0]["families"].append("NOPE")
    bad["client"]["business_units"][0]["eu_share"] = 1.4
    del bad["engagement"]["programme_codename"]
    with tempfile.TemporaryDirectory() as d:
        p = Path(d) / "client.yaml"
        p.write_text(yaml.safe_dump(bad, sort_keys=False, allow_unicode=True), encoding="utf-8")
        try:
            reskin.run(p, Path(d) / "out", skip_excel=True, quiet=True)
        except IntakeError as e:
            msg = str(e)
        else:
            raise AssertionError("broken intake was accepted")
        assert "engagement.programme_codename is required" in msg, msg
        # structural error stops before the deeper checks; fix it and look for the rest
        bad["engagement"]["programme_codename"] = "Project X"
        p.write_text(yaml.safe_dump(bad, sort_keys=False, allow_unicode=True), encoding="utf-8")
        try:
            reskin.run(p, Path(d) / "out", skip_excel=True, quiet=True)
        except IntakeError as e:
            msg = str(e)
        else:
            raise AssertionError("broken intake was accepted")
        for hint in ("business unit 'XX' is not in client.business_units", "cra_class 'Class III' is not one of",
                     "'NOPE' is neither a product family nor a legacy line id", "eu_share must be a fraction between 0 and 1"):
            assert hint in msg, f"missing {hint!r} in:\n{msg}"
        rc = subprocess.run([sys.executable, str(PACK / "reskin.py"), str(p), "--out", str(Path(d) / "o2"), "--skip-excel"],
                            capture_output=True, text=True)
        assert rc.returncode == 2 and "problem(s)" in rc.stderr


if __name__ == "__main__":
    tests = [v for k, v in sorted(globals().items()) if k.startswith("test_") and callable(v)]
    failed = 0
    for t in tests:
        try:
            t()
            print(f"ok    {t.__name__}")
        except Exception as e:  # noqa: BLE001
            failed += 1
            print(f"FAIL  {t.__name__}: {e}")
    sys.exit(1 if failed else 0)
