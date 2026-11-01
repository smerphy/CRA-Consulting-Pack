"""Run the worked sample case used in paper.md through the CLI and print its outputs.

Usage (from art14-operations/):  python3 run_sample_case.py [store_path]
The store defaults to a temporary file so nothing is left behind.
"""
import io
import sys
import tempfile
from pathlib import Path

from case_engine import cli

C = "ART14-2611-001"
ALL_ENGINE = ["lumen-browser-desktop", "lumen-browser-mobile", "lumen-os", "halo-os",
              "hearth-hub-display", "drive-sync-client"]


def run(store, *argv, show=False):
    buf = io.StringIO()
    rc = cli.main(["--store", store, *argv], out=buf)
    if rc != 0:
        raise SystemExit(f"step failed: {argv}")
    if show:
        print(buf.getvalue().rstrip())
    return buf.getvalue()


def main():
    store = sys.argv[1] if len(sys.argv) > 1 else str(Path(tempfile.mkdtemp()) / "sample.json")
    run(store, "create", "--id", C, "--type", "aev",
        "--title", "Lumen Engine JIT type confusion exploited in the wild (CVE pending)",
        "--summary", "A type confusion in the Lumen Engine JIT compiler allows remote code execution in the renderer "
                     "when a user opens crafted web content. Exploitation observed against Lumen Browser desktop.",
        "--first-signal", "2026-11-06T21:40Z", "--source", "partner_report", "--component", "lumen-engine",
        "--component-products", "reachable", "--evidence", "lumen-browser-desktop=exploited", show=True)
    run(store, "aware", "--case", C, "--at", "2026-11-07T01:10Z", "--by", "PSIRT duty officer (Dublin)",
        "--role", "psirt_duty_officer",
        "--rationale", "Partner exploit sample reproduced against shipped stable build; telemetry shows matching crash signatures",
        "--occurred", "2026-11-05T00:00Z")
    run(store, "content", "--case", C,
        "general_information=Type confusion in the Lumen Engine optimising JIT; renderer remote code execution via crafted web content; sandbox escape not observed.",
        "user_action=Apply the update as soon as offered; restart the browser or device.",
        "mitigation_expected_shortly=Yes", "attack_vector=Network (user visits crafted web content)",
        "sensitivity=TLP:AMBER until fixed builds are available on all affected products")
    run(store, "file", "--case", C, "--notification", "all", "--stage", "early_warning", "--at", "2026-11-07T07:30Z",
        "--filed-by", "Assigned Representative A", "--checked-by", "Assigned Representative B", "--srp-id", "SRP-{n}",
        "--evidence-ref", "evidence/ART14-2611-001/ew")
    run(store, "upstream", "--case", C, "--at", "2026-11-07T09:00Z")
    for p in ALL_ENGINE:
        run(store, "notice", "--case", C, "--product", p, "--kind", "affected_users", "--at", "2026-11-08T12:00Z",
            "--channel", "targeted advisory to enterprise admins and partners")
    run(store, "fix", "--case", C, "--product", "lumen-browser-desktop", "--at", "2026-11-08T18:00Z", "--desc", "Stable channel security update")
    run(store, "fix", "--case", C, "--product", "lumen-browser-mobile", "--at", "2026-11-08T22:00Z", "--desc", "App-store security update")
    for p in ("lumen-browser-desktop", "lumen-browser-mobile"):
        run(store, "notice", "--case", C, "--product", p, "--kind", "all_users", "--at", "2026-11-09T10:00Z",
            "--channel", "public advisory, release notes and CSAF")
    run(store, "legal", "--case", C, "--notification", "all", "--stage", "notification", "--at", "2026-11-08T20:00Z",
        "--by", "Product counsel", "--role", "product_counsel")
    run(store, "content", "--case", C, "measures_taken=Fixed builds released for Lumen Browser; OS and device builds in staged rollout.",
        "measures_users=Update Lumen Browser; enable automatic updates; enterprise admins can force-update via policy.")
    run(store, "file", "--case", C, "--notification", "all", "--stage", "notification", "--at", "2026-11-09T06:30Z",
        "--filed-by", "Assigned Representative A", "--checked-by", "Assigned Representative C")
    run(store, "fix", "--case", C, "--product", "drive-sync-client", "--at", "2026-11-10T10:00Z", "--desc", "Client update with patched webview")
    run(store, "fix", "--case", C, "--product", "lumen-os", "--at", "2026-11-10T17:00Z", "--desc", "Lumen OS out-of-cycle update")
    run(store, "fix", "--case", C, "--product", "halo-os", "--at", "2026-11-12T08:00Z", "--desc", "Halo OS system WebView update via app store")
    run(store, "fix", "--case", C, "--product", "hearth-hub-display", "--at", "2026-11-17T08:00Z", "--desc", "Hearth Hub firmware")
    print("\n$ python -m case_engine timeline --case", C)
    run(store, "timeline", "--case", C, show=True)
    print("\n$ python -m case_engine due --now 2026-11-13T09:00Z")
    run(store, "due", "--now", "2026-11-13T09:00Z", show=True)
    print("\n$ python -m case_engine pack --case", C, "--notification N4 --stage early_warning")
    run(store, "pack", "--case", C, "--notification", "N4", "--stage", "early_warning", show=True)


if __name__ == "__main__":
    main()
