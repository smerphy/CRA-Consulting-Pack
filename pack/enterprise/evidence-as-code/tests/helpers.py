import copy
import json
import os
import shutil
import sys
import tempfile

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

from cra_evidence import collectors as C  # noqa: E402
from cra_evidence import gate as G  # noqa: E402
from cra_evidence.record import build_bundle  # noqa: E402

EX = os.path.join(ROOT, "examples")
RELEASES = os.path.join(EX, "releases")
POLICY = C.load_json(os.path.join(EX, "policy", "aldermoor-gate-policy.json"))
OSV = C.load_json(os.path.join(EX, "feeds", "osv-snapshot.json"))["vulns"]
KEV = C.load_kev(C.load_json(os.path.join(EX, "feeds", "kev-snapshot.json")))

LOCK_OK = "hearth-lock-3_4.2.0"
LOCK_REVIEW = "hearth-lock-3_4.3.0"
BROWSER_FAIL = "lumen-browser_141.0.7390.54"
BROWSER_OK = "lumen-browser_141.0.7390.65"


def ensure_examples():
    if not os.path.exists(os.path.join(RELEASES, LOCK_OK, "release.json")):
        sys.path.insert(0, EX)
        import make_examples
        make_examples.main()


def bundle(name, mutate_manifest=None, mutate_files=None):
    """Build a bundle from an example release, optionally on a mutated copy."""
    ensure_examples()
    src = os.path.join(RELEASES, name)
    if not mutate_manifest and not mutate_files:
        return build_bundle(src, OSV, KEV, generated_at="2028-01-11T10:15:00Z")
    tmp = tempfile.mkdtemp(prefix="cra-test-")
    dst = os.path.join(tmp, name)
    shutil.copytree(src, dst)
    if mutate_manifest:
        p = os.path.join(dst, "release.json")
        m = C.load_json(p)
        mutate_manifest(m)
        with open(p, "w") as fh:
            json.dump(m, fh)
    if mutate_files:
        mutate_files(dst)
    return build_bundle(dst, OSV, KEV, generated_at="2028-01-11T10:15:00Z")


def decide(b, policy=None):
    return G.evaluate(b, copy.deepcopy(policy or POLICY))


def codes(result, severity=None):
    return {r["code"] for r in result["reasons"] if severity is None or r["severity"] == severity}
