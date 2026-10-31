"""Re-skin the CRA readiness pack for a client.

    python3 pack/reskin.py pack/clients/<slug>/client.yaml [--out dist/<slug>] [--skip-excel] [--urls urls.json]

Validates the intake, then writes:
    <out>/data/        pack_data.json, DATA_SUMMARY.md           (engine)
    <out>/excel/       D10 business case, D11 obligations tracker (workbooks, if available)
    <out>/diagnostic/  D08 readiness diagnostic                  (index.html)
    <out>/portal/      D12 portal                                (index.html)
    <out>/classifier/  D13 product classifier                    (index.html)
    <out>/RESKIN.md, <out>/reskin_values.json                    what to change in the hosted decks, docs and dashboard

Hosted deliverable URLs for the client go in pack/clients/<slug>/urls.json (same keys as pack/out/urls.json); without
it the portal marks client-specific hosted deliverables "To be produced for this client".
"""
import argparse
import json
import subprocess
import sys
import traceback
from pathlib import Path

import yaml

PACK = Path(__file__).resolve().parent
REPO = PACK.parent
ENGINE = PACK / "engine"
sys.path.insert(0, str(ENGINE))

import manifest  # noqa: E402
import render_classifier  # noqa: E402
import render_diagnostic  # noqa: E402
import render_portal  # noqa: E402
from reskin_common import REFERENCE, load_reference_urls  # noqa: E402
from validate import IntakeError, validate  # noqa: E402


def load_intake(path):
    path = Path(path)
    if not path.exists():
        raise IntakeError(path, [f"file not found: {path}"])
    try:
        intake = yaml.safe_load(path.read_text(encoding="utf-8"))
    except yaml.YAMLError as e:
        raise IntakeError(path, [f"not valid YAML: {e}"])
    errors, warnings = validate(intake)
    if errors:
        raise IntakeError(path, errors)
    return intake, warnings


def _workbook_builder():
    """Return build_all(pack_data_path, out_dir) from pack/engine/workbooks, or (None, reason)."""
    last = None
    for mod in ("workbooks", "engine.workbooks"):
        try:
            if mod.startswith("engine.") and str(PACK) not in sys.path:
                sys.path.insert(0, str(PACK))
            m = __import__(mod, fromlist=["build_all"])
            fn = getattr(m, "build_all", None)
            if callable(fn):
                return fn, None
            # Package without build_all yet: fall back to the per-workbook builders if both exist.
            try:
                d10 = __import__(mod + ".d10", fromlist=["build"])
                d11 = __import__(mod + ".d11", fromlist=["build"])
                if callable(getattr(d10, "build", None)) and callable(getattr(d11, "build", None)):
                    def both(pd_path, out_dir):
                        d10.build(pd_path, out_dir)
                        d11.build(pd_path, out_dir)
                    return both, None
            except Exception as e:  # noqa: BLE001
                last = f"{mod} has no build_all() and d10/d11 failed to import ({type(e).__name__}: {e})"
                continue
            last = f"{mod} has no build_all()"
        except Exception as e:  # noqa: BLE001 - report any import problem
            last = f"{type(e).__name__}: {e}"
    return None, last


def resolve_urls(intake_path, intake, explicit=None):
    """Client hosted-artifact URLs and the label for cards without one."""
    if explicit:
        return json.loads(Path(explicit).read_text(encoding="utf-8")), render_portal.PENDING_REFERENCE
    own = Path(intake_path).resolve().parent / "urls.json"
    if own.exists():
        return json.loads(own.read_text(encoding="utf-8")), render_portal.PENDING_REFERENCE
    if intake["engagement"]["client_name"] == REFERENCE["client"]:
        return load_reference_urls(), render_portal.PENDING_REFERENCE
    return {}, render_portal.PENDING_NEW_CLIENT


def run(intake_path, out=None, skip_excel=False, urls_path=None, quiet=False):
    say = (lambda *a: None) if quiet else print
    intake_path = Path(intake_path)
    intake, warnings = load_intake(intake_path)
    slug = intake_path.resolve().parent.name
    out = Path(out) if out else REPO / "dist" / slug
    out.mkdir(parents=True, exist_ok=True)
    for w in warnings:
        say(f"  warning: {w}")
    result = {"out": str(out), "warnings": warnings, "excel": None}

    # 1. engine
    data_dir = out / "data"
    p = subprocess.run([sys.executable, str(ENGINE / "build.py"), str(intake_path), str(data_dir)],
                       capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError(f"engine failed for {intake_path}:\n{p.stderr or p.stdout}")
    pd_path = data_dir / "pack_data.json"
    pd = json.loads(pd_path.read_text(encoding="utf-8"))
    say(f"data        {data_dir}/pack_data.json, DATA_SUMMARY.md")

    # 2. workbooks (D10, D11)
    if skip_excel:
        result["excel"] = "skipped (--skip-excel)"
        say("excel       skipped (--skip-excel)")
    else:
        build_all, why = _workbook_builder()
        if build_all is None:
            result["excel"] = f"not built: pack/engine/workbooks is not available ({why})"
            say(f"excel       NOT BUILT — pack/engine/workbooks is not available yet ({why}). "
                "Rerun reskin.py once it exists, or pass --skip-excel.")
        else:
            (out / "excel").mkdir(parents=True, exist_ok=True)
            build_all(str(pd_path), str(out / "excel"))
            result["excel"] = sorted(str(x) for x in (out / "excel").glob("*.xlsx"))
            say(f"excel       {out / 'excel'} ({len(result['excel'])} workbook(s))")

    # 3. diagnostic (D08)
    _write(out / "diagnostic" / "index.html", render_diagnostic.render(pd))
    say(f"diagnostic  {out / 'diagnostic' / 'index.html'}")

    # 4. classifier (D13)
    presets = (intake.get("classifier") or {}).get("presets")
    _write(out / "classifier" / "index.html", render_classifier.render(pd, presets=presets))
    say(f"classifier  {out / 'classifier' / 'index.html'}")

    # 5. portal (D12)
    urls, pending = resolve_urls(intake_path, intake, urls_path)
    local = {"D08": "../diagnostic/index.html", "D13": "../classifier/index.html"}
    local = {k: v for k, v in local.items() if not urls.get(k)}
    _write(out / "portal" / "index.html", render_portal.render(pd, urls, pending_label=pending, local_links=local))
    say(f"portal      {out / 'portal' / 'index.html'}")

    # 6. manifest for the hosted deliverables
    manifest.write(pd, out, urls=urls)
    say(f"manifest    {out / 'RESKIN.md'}, {out / 'reskin_values.json'}")
    return result


def _write(path, text):
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8")


def main(argv=None):
    ap = argparse.ArgumentParser(description="Re-skin the CRA readiness pack for a client intake.")
    ap.add_argument("intake", help="pack/clients/<slug>/client.yaml")
    ap.add_argument("--out", help="output directory (default: dist/<slug>)")
    ap.add_argument("--skip-excel", action="store_true", help="do not build the D10/D11 workbooks")
    ap.add_argument("--urls", help="JSON mapping of deliverable id -> hosted URL for this client")
    a = ap.parse_args(argv)
    try:
        run(a.intake, a.out, a.skip_excel, a.urls)
    except IntakeError as e:
        print(f"reskin: {e}", file=sys.stderr)
        return 2
    except Exception:  # noqa: BLE001
        traceback.print_exc()
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
