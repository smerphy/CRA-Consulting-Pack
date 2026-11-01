"""Pilot: run the evidence pipeline end to end on a real product line.

Real project: requests (PyPI, github.com/psf/requests), ten released
versions 2.31.0 to 2.34.2. For each version the pilot:

 1. downloads the sdist from PyPI and checks its SHA-256 against PyPI's;
 2. builds a wheel twice with ``python -m build`` in an isolated build
    environment, inside a network namespace with no network (``unshare -rn``)
    and with the build backend installed only from a digest-pinned local
    wheelhouse, with SOURCE_DATE_EPOCH set to the version's PyPI upload time;
    checks the two builds are bit-identical, and compares the wheel's files
    with the wheel the project published on PyPI;
 3. installs the built wheel into a fresh venv with dependencies resolved as
    at the release date (pip ``--uploaded-prior-to``) and generates a
    CycloneDX SBOM with cyclonedx-py, whose root is then bound to the built
    wheel by digest;
 4. runs bandit (SAST) over the sdist source, SARIF output;
 5. writes SLSA v1 provenance for the local build and signs it with the
    pilot builder key (DSSE, ECDSA P-256) through a KeyProvider, with an
    RFC 3161 timestamp from the local test TSA; the trust policy rates this
    builder SLSA Build L1 (a local, non-hosted builder);
 6. fetches real OSV advisories and the CISA KEV catalogue, filters OSV to
    records published before each release (the feed as it stood) and writes
    an authored OpenVEX document (signed by the pilot PSIRT key, timestamped);
 7. writes the release manifest from authored CRA metadata
    (authored/product-line.json), runs the gate, signs the record, stores
    inputs, record, signed record, log entry and checkpoint in an S3 Object
    Lock bucket (moto server over HTTP, compliance mode, retain-until from
    the record) and writes the Annex VII index;
 8. re-runs the gate with today's feed (post-market view, not stored).

Afterwards it verifies the whole store, attempts delete and overwrite of a
stored record (both must be refused), mirrors the bucket to
out/store/ for offline verification and writes results/pilot-results.json.

Usage (from the module root):  python examples/pilot/run_pilot.py [--offline]
Needs: build, cyclonedx-bom, bandit[sarif], boto3, moto[server], asn1crypto,
cryptography; network to pypi.org, files.pythonhosted.org, api.osv.dev and
raw.githubusercontent.com unless --offline (then cached inputs are used).
"""

import argparse
import base64
import datetime as _dt
import hashlib
import json
import os
import platform
import shutil
import socket
import subprocess
import sys
import tempfile
import time
import urllib.request
import uuid
import zipfile

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, ROOT)

from cra_evidence import attest as A  # noqa: E402
from cra_evidence import collectors as C  # noqa: E402
from cra_evidence import evidence_store as ES  # noqa: E402
from cra_evidence import gate as G  # noqa: E402
from cra_evidence import index as I  # noqa: E402
from cra_evidence import keys as K  # noqa: E402
from cra_evidence import objectstore as O  # noqa: E402
from cra_evidence import schema as S  # noqa: E402
from cra_evidence import tsa as TS  # noqa: E402
from cra_evidence.record import build_bundle  # noqa: E402
from cra_evidence.retention import add_years  # noqa: E402

PACKAGE = "requests"
VERSIONS = ["2.31.0", "2.32.2", "2.32.3", "2.32.4", "2.32.5", "2.33.0", "2.33.1", "2.34.0", "2.34.1", "2.34.2"]
SETUPTOOLS = "84.2.1"           # build backend, pinned by version and digest in the wheelhouse
BUILDER_ID = "https://aldermoor.example/builders/cra-pilot-local/v1"
BUILD_TYPE = "https://aldermoor.example/cra-pilot/buildtypes/python-sdist-wheel/v1"
SLSA = "https://slsa.dev/provenance/v1"
OPENVEX_PT = "https://openvex.dev/ns/v0.2.0"
BUCKET = "cra-pilot-evidence"
KEYNAMES = {"builder": ("pilot-builder-provenance", "ecdsa-p256-sha256"),
            "psirt": ("pilot-psirt-vex", "ed25519"),
            "record": ("pilot-release-record", "ecdsa-p256-sha256"),
            "log": ("pilot-evidence-log", "ed25519")}

CACHE = os.environ.get("CRA_PILOT_CACHE") or os.path.join(os.path.expanduser("~"), ".cache", "cra-pilot")
REL = os.path.join(HERE, "releases")
OUT = os.path.join(HERE, "out")
RES = os.path.join(HERE, "results")
AUTH = os.path.join(HERE, "authored")


def log(*a):
    print("[pilot]", *a, flush=True)


def write_json(path, obj):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(obj, fh, indent=2, sort_keys=False)
        fh.write("\n")


def write_text(path, text):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        fh.write(text)


def sha256_file(p):
    h = hashlib.sha256()
    with open(p, "rb") as fh:
        for c in iter(lambda: fh.read(1 << 20), b""):
            h.update(c)
    return h.hexdigest()


def fetch(url, dest=None, offline=False):
    """Download with a local cache keyed by URL."""
    key = hashlib.sha256(url.encode()).hexdigest()[:24] + "-" + os.path.basename(url.split("?")[0])[:60]
    path = dest or os.path.join(CACHE, "http", key)
    if os.path.exists(path):
        return path
    if offline:
        raise RuntimeError("offline and not cached: %s" % url)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    req = urllib.request.Request(url, headers={"User-Agent": "cra-evidence-pilot/1.0"})
    with urllib.request.urlopen(req, timeout=60) as r:  # noqa: S310 (fixed public registry URLs)
        data = r.read()
    with open(path + ".part", "wb") as fh:
        fh.write(data)
    os.replace(path + ".part", path)
    return path


def post_json(url, body, offline=False):
    key = hashlib.sha256((url + json.dumps(body, sort_keys=True)).encode()).hexdigest()[:24]
    path = os.path.join(CACHE, "osv", key + ".json")
    if os.path.exists(path):
        return json.load(open(path))
    if offline:
        raise RuntimeError("offline and not cached: %s %s" % (url, body))
    req = urllib.request.Request(url, data=json.dumps(body).encode(), method="POST",
                                 headers={"Content-Type": "application/json"})
    with urllib.request.urlopen(req, timeout=60) as r:  # noqa: S310
        data = json.loads(r.read())
    write_json(path, data)
    return data


def run(cmd, env=None, cwd=None, netns=False):
    if netns:
        cmd = ["unshare", "-rn"] + cmd
    p = subprocess.run(cmd, env=env, cwd=cwd, capture_output=True, text=True)
    if p.returncode != 0:
        raise RuntimeError("command failed (%d): %s\n%s\n%s" % (p.returncode, " ".join(cmd), p.stdout[-2000:],
                                                                  p.stderr[-2000:]))
    return p


def have_netns():
    try:
        return subprocess.run(["unshare", "-rn", "true"], capture_output=True).returncode == 0
    except FileNotFoundError:
        return False


def tool_version(mod):
    from importlib.metadata import version
    try:
        return version(mod)
    except Exception:  # noqa: BLE001
        return None


# ------------------------------------------------------------- keys, TSA, policy

def keys():
    kd = os.path.join(HERE, "keys")
    os.makedirs(kd, exist_ok=True)
    out = {}
    for role, (name, alg) in KEYNAMES.items():
        p = os.path.join(kd, name + ".demo-private.pem")
        out[role] = K.LocalFileKeyProvider(p, name) if os.path.exists(p) else \
            K.LocalFileKeyProvider.generate(p, name, alg)
    return out


def tsa():
    kd, td = os.path.join(HERE, "keys"), os.path.join(HERE, "trust")
    kp, cp, rp = (os.path.join(kd, "pilot-test-tsa.demo-private.pem"), os.path.join(td, "pilot-test-tsa.cert.pem"),
                  os.path.join(td, "pilot-test-tsa-root.cert.pem"))
    if not os.path.exists(kp):
        _, root, key, cert = TS.generate_tsa("CRA pilot test TSA")
        write_text(kp, TS.pem_of(key))
        write_text(cp, TS.pem_of(cert))
        write_text(rp, TS.pem_of(root))
    return TS.LocalTSA.from_pem_files(kp, cp, rp, name="pilot-test-tsa")


def policy(k):
    trust = {
        "trust_policy_id": "cra-pilot-trust/1.0.0",
        "description": "Pilot trust policy. All keys are file-based demonstration keys (examples/pilot/keys); the "
                       "TSA is a local test authority. The builder is a local script, rated SLSA Build L1.",
        "require_signed_provenance": True, "require_signed_vex": True, "min_slsa_build_level": 1,
        "keys": {
            KEYNAMES["builder"][0]: k["builder"].trust_entry(["provenance"], "Pilot builder (local)"),
            KEYNAMES["psirt"][0]: k["psirt"].trust_entry(["vex"], "Pilot PSIRT (authored VEX)"),
            KEYNAMES["record"][0]: k["record"].trust_entry(["evidence_record"], "Pilot release pipeline"),
            KEYNAMES["log"][0]: k["log"].trust_entry(["log_checkpoint"], "Pilot evidence store"),
        },
        "revoked_keyids": [],
        "builders": {BUILDER_ID: {
            "slsa_build_level": 1, "hosted": False, "isolated": False, "signing_key_isolated": False,
            "signers": ["key:" + KEYNAMES["builder"][0]],
            "basis": "Local pilot builder: provenance generated and signed by the build script on one host. "
                     "Signed provenance would meet L2's authenticity requirement, but L2 also requires a hosted "
                     "build platform, so the verifier rates it L1. Not L3: build steps share the host with the "
                     "signing key."}},
        "timestamp_authorities": [{"name": "pilot-test-tsa", "root_pem_path": "../trust/pilot-test-tsa-root.cert.pem"}],
        "sigstore": {"trusted_root": "trust/sigstore-public-good.trusted_root.json"},
        "products": {"*": {
            "provenance": {"keys": [KEYNAMES["builder"][0]], "builder_ids": [BUILDER_ID], "min_slsa_build_level": 1,
                           "build_types": [BUILD_TYPE], "require_timestamp": True,
                           "external_parameters": {
                               "source.uri": {"pattern": r"https://files\.pythonhosted\.org/packages/.+/requests-[0-9.]+\.tar\.gz"},
                               "source.sha256": {"pattern": r"[0-9a-f]{64}"},
                               "package": "requests", "version": {"pattern": r"[0-9]+\.[0-9]+\.[0-9]+"},
                               "source_date_epoch": {"pattern": r"[0-9]+"}}},
            "vex": {"keys": [KEYNAMES["psirt"][0]], "require_timestamp": True},
            "evidence_record": {"keys": [KEYNAMES["record"][0]], "require_timestamp": True},
            "log_checkpoint": {"keys": [KEYNAMES["log"][0]], "require_timestamp": True}}},
    }
    pol = {
        "policy_id": "cra-pilot-gate/1.0.0",
        "description": "Pilot gate policy (authored) for a default-class software library placed via Module A.",
        "trusted_builders": [BUILDER_ID], "accepted_predicate_types": [SLSA], "min_support_years": 5,
        "fail_untriaged_severities": ["critical", "high"],
        "required_tests": {"default": ["sast"], "products": {}},
        "pentest_required_on": [],
        "sarif_fail_level": "error", "harmonised_standards_cited": [],
        "required_matrix_items": ["1"] + ["2" + c for c in "abcdefghijklm"],
        "accepted_vex_predicate_types": [OPENVEX_PT, "https://openvex.dev/ns"],
        "attestation_trust": trust,
    }
    path = os.path.join(HERE, "policy", "pilot-gate-policy.json")
    write_json(path, pol)
    pol["_base_dir"] = os.path.dirname(path)
    return pol


# ------------------------------------------------------------- PyPI and build

def pypi_meta(version, offline):
    return json.load(open(fetch("https://pypi.org/pypi/%s/%s/json" % (PACKAGE, version), offline=offline)))


def wheelhouse(offline):
    wh = os.path.join(CACHE, "wheelhouse")
    os.makedirs(wh, exist_ok=True)
    have = [f for f in os.listdir(wh) if f.startswith("setuptools-%s-" % SETUPTOOLS)]
    if not have:
        if offline:
            raise RuntimeError("offline and setuptools wheel not cached")
        run([sys.executable, "-m", "pip", "download", "--only-binary", ":all:", "--no-deps", "-q",
             "setuptools==%s" % SETUPTOOLS, "-d", wh])
        have = [f for f in os.listdir(wh) if f.startswith("setuptools-%s-" % SETUPTOOLS)]
    f = os.path.join(wh, have[0])
    return wh, {"uri": "pkg:pypi/setuptools@%s" % SETUPTOOLS, "name": have[0], "digest": {"sha256": sha256_file(f)}}


def build_wheel(src, outdir, epoch, wh, netns):
    env = dict(os.environ, SOURCE_DATE_EPOCH=str(epoch), PIP_NO_INDEX="1", PIP_FIND_LINKS=wh,
               PYTHONHASHSEED="0", PIP_DISABLE_PIP_VERSION_CHECK="1", LC_ALL="C.UTF-8", TZ="UTC")
    env.pop("PIP_INDEX_URL", None)
    run([sys.executable, "-m", "build", "--wheel", "--outdir", outdir, src], env=env, netns=netns)
    whl = [f for f in os.listdir(outdir) if f.endswith(".whl")]
    return os.path.join(outdir, whl[0])


def wheel_payload(path):
    """{filename: sha256} for files outside .dist-info (the importable payload)."""
    out = {}
    with zipfile.ZipFile(path) as z:
        for n in z.namelist():
            if ".dist-info/" not in n:
                out[n] = hashlib.sha256(z.read(n)).hexdigest()
    return out


def wheel_requires(path):
    with zipfile.ZipFile(path) as z:
        meta = [n for n in z.namelist() if n.endswith(".dist-info/METADATA")][0]
        text = z.read(meta).decode()
    deps = []
    for line in text.splitlines():
        if line.startswith("Requires-Dist:"):
            spec = line.split(":", 1)[1].strip()
            if "extra ==" in spec:
                continue
            name = spec.split(";")[0].split("(")[0]
            for ch in "<>=!~[ ":
                name = name.split(ch)[0]
            deps.append(norm(name))
    return sorted(set(deps))


def norm(name):
    return name.lower().replace("_", "-").replace(".", "-")


# ------------------------------------------------------------- SBOM and SAST

def sbom(wheel, version, upload_iso, workdir, offline):
    venv = os.path.join(workdir, "venv")
    run([sys.executable, "-m", "venv", "--without-pip", venv])
    py = os.path.join(venv, "bin", "python")
    deps = os.path.join(CACHE, "deps", version)        # dependencies as resolvable at the release date
    if not offline:
        run([sys.executable, "-m", "pip", "download", "-q", "--disable-pip-version-check", "--uploaded-prior-to",
             upload_iso, "--only-binary", ":all:", "-d", deps, wheel])
    run([sys.executable, "-m", "pip", "--python", py, "install", "-q", "--disable-pip-version-check",
         "--no-index", "--find-links", deps, wheel])
    raw = os.path.join(workdir, "sbom.raw.json")
    run([sys.executable, "-m", "cyclonedx_py", "environment", py, "--sv", "1.6", "--of", "JSON",
         "--output-reproducible", "-o", raw])
    doc = json.load(open(raw))
    comps = doc.get("components") or []
    root = next(c for c in comps if norm(c["name"]) == PACKAGE and c.get("version") == version)
    doc["components"] = [c for c in comps if c is not root]
    with open(wheel, "rb") as fh:
        data = fh.read()
    root = dict(root, hashes=[{"alg": "SHA-256", "content": hashlib.sha256(data).hexdigest()},
                              {"alg": "SHA-512", "content": hashlib.sha512(data).hexdigest()}])
    root["properties"] = (root.get("properties") or []) + [
        {"name": "cra-pilot:root-binding", "value": "metadata.component bound to the built wheel by digest; "
                                                     "dependencies resolved as at %s" % upload_iso}]
    doc.setdefault("metadata", {})["component"] = root
    return doc


def sast(src, out):
    pkg = os.path.join(src, "src", PACKAGE) if os.path.isdir(os.path.join(src, "src", PACKAGE)) \
        else os.path.join(src, PACKAGE)
    p = subprocess.run(["bandit", "-q", "-r", pkg, "-f", "sarif", "-o", out], capture_output=True, text=True)
    if p.returncode not in (0, 1) or not os.path.exists(out):
        raise RuntimeError("bandit failed: %s" % p.stderr[-1000:])
    doc = json.load(open(out))
    for r in doc["runs"][0].get("results") or []:     # relative paths only (no build-host paths in evidence)
        for loc in r.get("locations") or []:
            al = loc.get("physicalLocation", {}).get("artifactLocation", {})
            uri = al.get("uri") or ""
            if uri.startswith("file://"):
                uri = uri[len("file://"):]
            if os.path.isabs(uri):
                al["uri"] = os.path.relpath(uri, src)
    doc["runs"][0].pop("invocations", None)
    write_json(out, doc)
    return doc


# ------------------------------------------------------------- feeds

def feeds(names, offline):
    """Real OSV advisories for every package in the SBOMs and the CISA KEV catalogue."""
    vulns, seen = [], set()
    for n in sorted(names):
        r = post_json("https://api.osv.dev/v1/query", {"package": {"name": n, "ecosystem": "PyPI"}}, offline)
        for v in r.get("vulns") or []:
            if v["id"] not in seen:
                seen.add(v["id"])
                vulns.append(v)
    kev_path = fetch("https://raw.githubusercontent.com/cisagov/kev-data/develop/known_exploited_vulnerabilities.json",
                     offline=offline)
    kev = json.load(open(kev_path))
    return vulns, kev


def as_at(vulns, iso):
    """OSV records published at or before ``iso`` (the feed as it stood, approximately)."""
    return [v for v in vulns if (v.get("published") or "9999") <= iso]


# ------------------------------------------------------------- docs (authored)

def docs(d, version, line):
    write_text(os.path.join(d, "docs", "risk-assessment.md"),
               "# Cybersecurity risk assessment: requests %s (AUTHORED PILOT STUB)\n\nAuthored for the pilot; not "
               "written by the requests maintainers. Assets: credentials in URLs, proxies and netrc; TLS "
               "verification state; redirects. Threats: credential leakage, TLS downgrade or verification bypass, "
               "header injection. Treatment: see the applicability matrix.\n" % version)
    write_text(os.path.join(d, "docs", "annex-ii-user-information.md"),
               "# Security information for requests %s (AUTHORED PILOT STUB)\n\nAnnex II points 1-9 as a pilot "
               "stub. Vulnerability reporting: the project's published security policy. Support period: see "
               "release.json.\n" % version)
    write_text(os.path.join(d, "docs", "update-design-note.md"),
               "# Update design note: requests (AUTHORED PILOT STUB)\n\nUpdates are new versions on PyPI; users "
               "update with their package manager. Security fixes are released as new versions.\n")
    write_text(os.path.join(d, "docs", "cvd-policy.md"),
               "# Coordinated vulnerability disclosure (AUTHORED PILOT STUB)\n\nPilot reference to the project's "
               "public security policy and GitHub security advisories.\n")
    rows = []
    titles = {"1": "Appropriate level of cybersecurity", "2a": "No known exploitable vulnerabilities",
              "2b": "Secure by default", "2c": "Security updates", "2d": "Protection from unauthorised access",
              "2e": "Confidentiality", "2f": "Integrity", "2g": "Data minimisation",
              "2h": "Availability of essential functions", "2i": "Minimise impact on other networks",
              "2j": "Limit attack surface", "2k": "Exploitation mitigation", "2l": "Logging and monitoring",
              "2m": "Secure data removal and transfer"}
    na = {"2l": "A library emits no security logs of its own; the integrating application logs (authored)",
          "2m": "The library stores no user data at rest (authored)"}
    for k, t in titles.items():
        row = {"item": k, "title": t, "applies": k not in na, "implementation": "Pilot stub: see risk assessment"}
        if k in na:
            row["justification"] = na[k]
        rows.append(row)
    write_json(os.path.join(d, "docs", "applicability-matrix.json"),
               {"product_id": "requests", "basis": "Art 13(3)-(4); Annex I Part I (AUTHORED PILOT STUB)", "items": rows})


# ------------------------------------------------------------- per version

def placing_chain(line):
    """Authored placing events: first placing, then updates inheriting the last new placing's date."""
    out, last = {}, None
    for v in line["versions"]:
        out[v["version"]] = (v, last)
        if v["decision"] in ("first_placing", "substantial"):
            last = v["version"]
    return out


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true", help="use cached downloads only")
    ap.add_argument("--keep-store", action="store_true")
    args = ap.parse_args(argv)
    t_run = time.perf_counter()
    for d in (REL, OUT):
        if os.path.exists(d):
            for dp, _, fns in os.walk(d):
                for f in fns:
                    os.chmod(os.path.join(dp, f), 0o644)
            shutil.rmtree(d)
    os.makedirs(CACHE, exist_ok=True)
    line = json.load(open(os.path.join(AUTH, "product-line.json")))
    triage = json.load(open(os.path.join(AUTH, "vex-triage.json")))["statements"]
    chain = placing_chain(line)
    k = keys()
    tsa_local = tsa()
    tsa_url = tsa_local.serve()
    tsa_client = TS.TimestampClient(tsa_url)
    pol = policy(k)
    netns = have_netns()
    wh, setuptools_dep = wheelhouse(args.offline)
    log("netns isolation:", netns, "| TSA:", tsa_url, "| setuptools", SETUPTOOLS)

    # S3 Object Lock bucket on a local moto server (HTTP)
    from moto.server import ThreadedMotoServer
    import boto3
    s = socket.socket()
    s.bind(("127.0.0.1", 0))
    port = s.getsockname()[1]
    s.close()
    moto = ThreadedMotoServer(ip_address="127.0.0.1", port=port, verbose=False)
    moto.start()
    s3 = boto3.client("s3", endpoint_url="http://127.0.0.1:%d" % port, region_name="eu-west-1",
                      aws_access_key_id="pilot", aws_secret_access_key="pilot")
    backend = O.S3ObjectLockBackend(BUCKET, client=s3)
    backend.ensure_bucket(create=True, region="eu-west-1")
    store = ES.EvidenceStore(backend, k["record"], k["log"], tsa_client, log_id="cra-pilot-log/requests")
    trust = A.TrustPolicy(pol["attestation_trust"], pol["_base_dir"])

    results = {"generated": _dt.datetime.now(_dt.timezone.utc).replace(microsecond=0).isoformat(),
               "package": PACKAGE, "versions": [],
               "environment": {"python": platform.python_version(), "platform": platform.platform(),
                               "cpus": os.cpu_count(), "build": tool_version("build"),
                               "cyclonedx-bom": tool_version("cyclonedx-bom"), "bandit": tool_version("bandit"),
                               "moto": tool_version("moto"), "boto3": tool_version("boto3"),
                               "setuptools_pinned": setuptools_dep, "network_namespace_build": netns}}
    staged = []
    work = tempfile.mkdtemp(prefix="cra-pilot-")
    try:
        # Phase 1: build, SBOM, SAST, provenance (per version)
        for ver in VERSIONS:
            t = {}
            meta = pypi_meta(ver, args.offline)
            sd = next(u for u in meta["urls"] if u["packagetype"] == "sdist")
            pw = next(u for u in meta["urls"] if u["packagetype"] == "bdist_wheel")
            upload = sd["upload_time_iso_8601"].replace(".000000Z", "Z")
            upload_dt = _dt.datetime.fromisoformat(upload.replace("Z", "+00:00"))
            epoch = int(upload_dt.timestamp())
            t0 = time.perf_counter()
            sdist = fetch(sd["url"], offline=args.offline)
            pypi_whl = fetch(pw["url"], offline=args.offline)
            t["download"] = time.perf_counter() - t0
            if sha256_file(sdist) != sd["digests"]["sha256"]:
                raise RuntimeError("sdist digest mismatch for %s" % ver)
            wd = os.path.join(work, ver)
            os.makedirs(wd)
            run(["tar", "--no-same-owner", "-xzf", sdist, "-C", wd])
            src = os.path.join(wd, "%s-%s" % (PACKAGE, ver))
            t0 = time.perf_counter()
            started = _dt.datetime.now(_dt.timezone.utc)
            w1 = build_wheel(src, os.path.join(wd, "b1"), epoch, wh, netns)
            t["build"] = time.perf_counter() - t0
            finished = _dt.datetime.now(_dt.timezone.utc)
            src2 = os.path.join(wd, "rebuild")
            os.makedirs(src2)
            run(["tar", "--no-same-owner", "-xzf", sdist, "-C", src2])
            t0 = time.perf_counter()
            w2 = build_wheel(os.path.join(src2, "%s-%s" % (PACKAGE, ver)), os.path.join(wd, "b2"), epoch, wh, netns)
            t["rebuild_check"] = time.perf_counter() - t0
            d1, d2 = sha256_file(w1), sha256_file(w2)
            ours, theirs = wheel_payload(w1), wheel_payload(pypi_whl)
            same_payload = ours == theirs
            d = os.path.join(REL, "%s_%s" % (PACKAGE, ver))
            art_rel = "artefact/" + os.path.basename(w1)
            os.makedirs(os.path.join(d, "artefact"))
            shutil.copyfile(w1, os.path.join(d, art_rel))
            with open(w1, "rb") as fh:
                wbytes = fh.read()
            t0 = time.perf_counter()
            bom = sbom(w1, ver, upload, wd, args.offline)
            t["sbom"] = time.perf_counter() - t0
            write_json(os.path.join(d, "evidence", "sbom.cdx.json"), bom)
            t0 = time.perf_counter()
            sres = sast(src, os.path.join(d, "evidence", "sast.sarif"))
            t["sast"] = time.perf_counter() - t0
            st = {"_type": "https://in-toto.io/Statement/v1",
                  "subject": [{"name": os.path.basename(w1), "digest": {"sha256": hashlib.sha256(wbytes).hexdigest(),
                                                                       "sha512": hashlib.sha512(wbytes).hexdigest()}}],
                  "predicateType": SLSA,
                  "predicate": {
                      "buildDefinition": {
                          "buildType": BUILD_TYPE,
                          "externalParameters": {"source": {"uri": sd["url"], "sha256": sd["digests"]["sha256"]},
                                                 "package": PACKAGE, "version": ver, "source_date_epoch": str(epoch)},
                          "internalParameters": {"frontend": "build %s (isolated build environment)" % tool_version("build"),
                                                 "python": platform.python_version(),
                                                 "network": "none (unshare -rn network namespace)" if netns else "not isolated",
                                                 "index": "pip --no-index; build backend from a digest-pinned wheelhouse"},
                          "resolvedDependencies": [{"uri": sd["url"], "digest": {"sha256": sd["digests"]["sha256"]}},
                                                   setuptools_dep]},
                      "runDetails": {"builder": {"id": BUILDER_ID},
                                     "metadata": {"invocationId": str(uuid.uuid4()),
                                                  "startedOn": started.replace(microsecond=0).isoformat().replace("+00:00", "Z"),
                                                  "finishedOn": finished.replace(microsecond=0).isoformat().replace("+00:00", "Z")},
                                     "byproducts": [{"name": "independent-rebuild.whl", "digest": {"sha256": d2}}]}}}
            t0 = time.perf_counter()
            write_json(os.path.join(d, "evidence", "provenance.sigstore.json"),
                       K.sign_and_timestamp(st, k["builder"], tsa_client))
            t["provenance_sign_timestamp"] = time.perf_counter() - t0
            staged.append({"version": ver, "dir": d, "art_rel": art_rel, "upload": upload, "t": t,
                           "requires": wheel_requires(w1), "bom": bom, "wheel": w1,
                           "repro": {"build_sha256": d1, "rebuild_sha256": d2, "bit_identical": d1 == d2,
                                     "pypi_wheel_sha256": pw["digests"]["sha256"],
                                     "pypi_wheel_identical": d1 == pw["digests"]["sha256"],
                                     "payload_files_identical_to_pypi_wheel": same_payload,
                                     "payload_files": len(ours),
                                     "payload_differences": sorted(set(ours.items()) ^ set(theirs.items()))[:6]},
                           "sast": {"results": len(sres["runs"][0].get("results") or []),
                                    "levels": sorted({r.get("level") for r in sres["runs"][0].get("results") or []}),
                                    "rules": sorted({r.get("ruleId") for r in sres["runs"][0].get("results") or []})}})
            log("%s built (%.1fs + %.1fs), bit-identical=%s, payload==PyPI=%s, sbom %d comps"
                % (ver, t["build"], t["rebuild_check"], d1 == d2, same_payload, len(bom["components"])))

        # Phase 2: feeds (one fetch per run)
        t0 = time.perf_counter()
        names = {PACKAGE} | {norm(c["name"]) for s_ in staged for c in s_["bom"]["components"]}
        osv_all, kev_doc = feeds(names, args.offline)
        t_feeds = time.perf_counter() - t0
        kev_ids = C.load_kev(kev_doc)
        snap = _dt.date.today().isoformat()
        write_json(os.path.join(HERE, "feeds", "osv-pypi-snapshot.json"),
                   {"source": "https://api.osv.dev/v1/query (PyPI ecosystem)", "retrieved": snap,
                    "packages": sorted(names), "vulns": osv_all})
        write_json(os.path.join(HERE, "feeds", "kev-snapshot.json"),
                   {"source": "github.com/cisagov/kev-data (mirror of the CISA KEV catalogue)", "retrieved": snap,
                    "catalogVersion": kev_doc.get("catalogVersion"), "count": kev_doc.get("count"),
                    "vulnerabilities": [{"cveID": v["cveID"]} for v in kev_doc.get("vulnerabilities") or []]})
        log("feeds: %d OSV records for %d packages, KEV %s entries (%.1fs)"
            % (len(osv_all), len(names), kev_doc.get("count"), t_feeds))

        # Phase 3: VEX, manifest, gate, sign, store, index
        for s_ in staged:
            ver, d, t = s_["version"], s_["dir"], s_["t"]
            v, placed_from = chain[ver]
            feed_then = as_at(osv_all, s_["upload"])
            # authored VEX over what the feed showed at release
            comps = s_["bom"]["components"] + [{"name": PACKAGE, "version": ver}]
            matches = C.match_osv([{"name": c["name"], "version": c.get("version"), "purl": c.get("purl")}
                                   for c in comps], feed_then, kev_ids)
            stmts, seen_v = [], set()
            for m in matches:
                if m["vulnerability"] in seen_v:
                    continue
                seen_v.add(m["vulnerability"])
                tri = triage.get(m["vulnerability"]) or {"status": "under_investigation"}
                stmt = {"vulnerability": {"name": m["vulnerability"], "aliases": m["aliases"]},
                        "products": [{"@id": "pkg:pypi/requests@%s" % ver,
                                      "subcomponents": [{"@id": "pkg:pypi/%s" % m["component"]}]}],
                        "status": tri["status"]}
                for f in ("justification", "impact_statement", "action_statement"):
                    if tri.get(f):
                        stmt[f] = tri[f]
                stmts.append(stmt)
            vex = {"@context": OPENVEX_PT, "@id": "https://aldermoor.example/cra-pilot/vex/requests/%s" % ver,
                   "author": "Pilot PSIRT (AUTHORED; no real triage performed)", "timestamp": s_["upload"],
                   "version": 1, "statements": stmts}
            write_json(os.path.join(d, "evidence", "vex.openvex.json"), vex)
            with open(os.path.join(d, s_["art_rel"]), "rb") as fh:
                wb = fh.read()
            vst = {"_type": "https://in-toto.io/Statement/v1",
                   "subject": [{"name": os.path.basename(s_["art_rel"]),
                                "digest": {"sha256": hashlib.sha256(wb).hexdigest()}}],
                   "predicateType": OPENVEX_PT, "predicate": vex}
            t0 = time.perf_counter()
            write_json(os.path.join(d, "evidence", "vex.openvex.sigstore.json"),
                       K.sign_and_timestamp(vst, k["psirt"], tsa_client))
            t["vex_sign_timestamp"] = time.perf_counter() - t0
            docs(d, ver, line)
            rdate = s_["upload"][:10]
            if v["decision"] in ("first_placing", "substantial"):
                event = "first_placing" if v["decision"] == "first_placing" else "substantial_modification_placing"
                placing = {"date": rdate, "event": event, "member_states": line["member_states"]}
                decl = {"declaration_id": "PILOT-DoC-requests-%s" % ver, "status": "new" if event == "first_placing"
                        else "updated", "uri": "https://aldermoor.example/cra-pilot/doc/requests/%s" % ver,
                        "signatory_function": "Pilot signatory (authored)"}
            else:
                pv = chain[placed_from][0]
                pdate = next(x for x in staged if x["version"] == placed_from)["upload"][:10]
                placing = {"date": rdate, "event": "update_to_placed_product", "member_states": line["member_states"],
                           "inherited_placing_date": pdate, "inherited_from_version": pv["version"]}
                decl = {"declaration_id": "PILOT-DoC-requests-%s" % placed_from, "status": "reused",
                        "reused_from_version": placed_from,
                        "uri": "https://aldermoor.example/cra-pilot/doc/requests/%s" % placed_from,
                        "signatory_function": "Pilot signatory (authored)"}
            sm = {kk: v[kk] for kk in ("change_type", "questions", "rationale", "assessed_by", "decision")}
            for kk in ("conformity_assessment_ref", "bundling_justification"):
                if v.get(kk):
                    sm[kk] = v[kk]
            prev = VERSIONS[VERSIONS.index(ver) - 1] if VERSIONS.index(ver) else None
            manifest = {
                "manifest_version": "1.0", "org": "aldermoor-pilot", "product": line["product"], "version": ver,
                "previous_version": prev, "release_date": rdate, "placing": placing,
                "classification": line["classification"], "artefact": s_["art_rel"],
                "build_graph": {"direct_dependencies": s_["requires"],
                                "source": "Requires-Dist (no extras) read from the built wheel's METADATA"},
                "evidence": {"sbom": "evidence/sbom.cdx.json", "provenance": "evidence/provenance.sigstore.json",
                             "vex": "evidence/vex.openvex.json",
                             "vex_attestation": "evidence/vex.openvex.sigstore.json",
                             "tests": [{"type": "sast", "path": "evidence/sast.sarif"}],
                             "risk_assessment": {"path": "docs/risk-assessment.md", "ref": "RA-requests-%s" % ver},
                             "applicability_matrix": {"path": "docs/applicability-matrix.json",
                                                      "ref": "AM-requests-%s" % ver},
                             "annex_ii": {"path": "docs/annex-ii-user-information.md",
                                          "uri": "https://aldermoor.example/cra-pilot/security/requests/%s/" % ver},
                             "update_design_note": {"path": "docs/update-design-note.md", "ref": "UDN-requests"},
                             "cvd_policy": {"path": "docs/cvd-policy.md", "ref": "https://github.com/psf/requests/security"}},
                "support_period": {"end_date": add_years(_dt.date.fromisoformat(rdate),
                                                         line["support"]["years_from_version_date"]).isoformat(),
                                   "latest_version_rule": line["support"]["latest_version_rule"],
                                   "justification": line["support"]["justification"]},
                "substantial_modification": sm, "declaration": decl,
                "signer": {"identity": "spiffe://aldermoor.example/cra-pilot/release-pipeline/requests",
                           "role": "Pilot release manager (accountable); pipeline key signs the record",
                           "signature_ref": "Signed record: DSSE by %s with RFC 3161 timestamp; provenance key %s; "
                                            "VEX key %s" % (KEYNAMES["record"][0], KEYNAMES["builder"][0],
                                                            KEYNAMES["psirt"][0])},
                "store": {"uri_prefix": "s3://%s/v1" % BUCKET, "object_lock_mode": "compliance"},
                "feeds": {"osv": "OSV PyPI records published by %s (snapshot %s)" % (s_["upload"], snap),
                          "kev": "CISA KEV %s (via cisagov/kev-data)" % kev_doc.get("catalogVersion")},
            }
            write_json(os.path.join(d, "release.json"), manifest)
            # Gate as at release
            t0 = time.perf_counter()
            b = build_bundle(d, osv_records=feed_then, kev_ids=kev_ids)
            res = G.evaluate(b, pol)
            b.record["gate"] = res
            errs = S.validate(b.record)
            t["gate_incl_signature_and_timestamp_verification"] = time.perf_counter() - t0
            if errs:
                raise RuntimeError("schema errors for %s: %s" % (ver, errs[:3]))
            # Store: inputs, record, signed record, log entry, checkpoint
            files = [s_["art_rel"], "release.json"] + ["evidence/" + f for f in sorted(os.listdir(os.path.join(d, "evidence")))] \
                + ["docs/" + f for f in sorted(os.listdir(os.path.join(d, "docs")))]
            t0 = time.perf_counter()
            receipt = store.put_release(b.record, files, d)
            t["store_total"] = time.perf_counter() - t0
            for kk in ("record_sign_and_timestamp", "object_lock_put", "merkle_append", "checkpoint_sign_timestamp_put"):
                t[kk] = receipt["timings"].get(kk, 0.0)
            t0 = time.perf_counter()
            idx = I.build_index(b.record)
            write_json(os.path.join(OUT, "index", "requests_%s.annex-vii-index.json" % ver), idx)
            write_text(os.path.join(OUT, "index", "requests_%s.annex-vii-index.md" % ver), I.render_markdown(idx))
            write_json(os.path.join(OUT, "records", "requests_%s.record.json" % ver), b.record)
            write_json(os.path.join(OUT, "records", "requests_%s.inclusion-proof.json" % ver),
                       receipt.get("inclusion_proof"))
            t["index"] = time.perf_counter() - t0
            # Post-market view: same evidence, today's feed (not stored)
            b2 = build_bundle(d, osv_records=osv_all, kev_ids=kev_ids)
            res2 = G.evaluate(b2, pol)
            per = {k2: round(v2, 4) for k2, v2 in t.items()}
            per["end_to_end_excluding_download"] = round(sum(v2 for k2, v2 in t.items()
                                                             if k2 not in ("download", "store_total")), 3)
            results["versions"].append({
                "version": ver, "pypi_upload": s_["upload"], "change_type": v["change_type"],
                "decision_authored": v["decision"], "placing_event": placing["event"],
                "inherited_placing_date": placing.get("inherited_placing_date"),
                "retain_until": b.record["retention"]["retain_until"],
                "gate_at_release": res["decision"],
                "gate_at_release_reasons": [r2["code"] for r2 in res["reasons"] if r2["severity"] != "info"],
                "gate_today": res2["decision"],
                "gate_today_reasons": sorted({"%s %s" % (r2["code"], r2.get("subject") or r2["message"].split(" ")[0])
                                              for r2 in res2["reasons"] if r2["severity"] != "info"}),
                "matches_at_release": sorted({m["vulnerability"] for m in matches}),
                "matches_today": sorted({m["vulnerability"] for m in
                                         b2.record["evidence"]["vulnerability_status"]["known_vulnerability_matches"]}),
                "sbom_components": len(s_["bom"]["components"]), "direct_dependencies": s_["requires"],
                "provenance_signing_time_source":
                    b.record["evidence"]["provenance"]["verification"]["signer"]["signing_time_source"],
                "slsa_build_level": b.record["evidence"]["provenance"]["verification"].get("slsa_build_level"),
                "reproducibility": s_["repro"], "sast": s_["sast"],
                "store": {"record_key": receipt["record_key"], "bundle_key": receipt["bundle_key"],
                          "version_ids": receipt["versions"], "seq": receipt["seq"]},
                "timings_s": per})
            log("%s gate %s (today %s) stored seq %d, e2e %.2fs"
                % (ver, res["decision"], res2["decision"], receipt["seq"], per["end_to_end_excluding_download"]))

        # Store-level checks
        t0 = time.perf_counter()
        problems = store.verify(trust, deep=True)
        t_verify = time.perf_counter() - t0
        first = results["versions"][0]["store"]
        neg = {}
        try:
            backend.delete(first["record_key"], version_id=first["version_ids"][0])
            neg["delete_locked_version"] = "ALLOWED (unexpected)"
        except O.ObjectLockedError as e:
            neg["delete_locked_version"] = "DENIED: %s" % e
        try:
            backend.put(first["record_key"], b"{}", "2040-01-01")
            neg["overwrite_record"] = "ALLOWED (unexpected)"
        except O.WriteOnceError as e:
            neg["overwrite_record"] = "DENIED: %s" % e
        rec, rres = store.get_record("urn:aldermoor-pilot:cra-evidence:requests:2.32.4", trust)
        neg["verify_on_read"] = {"verified": rres["verified"], "signing_time_source":
                                 (rres.get("signer") or {}).get("signing_time_source")}
        # tamper with a copy of a bundle: signature must fail
        bundle = json.loads(backend.get(first["bundle_key"]))
        stmt = json.loads(base64.b64decode(bundle["dsseEnvelope"]["payload"]))
        stmt["predicate"]["gate"]["decision"] = "PASS" if stmt["predicate"]["gate"]["decision"] != "PASS" else "FAIL"
        bundle["dsseEnvelope"]["payload"] = base64.b64encode(json.dumps(stmt).encode()).decode()
        from cra_evidence import record_signing as RS
        neg["tampered_record_copy"] = RS.verify_record_bundle(bundle, trust, PACKAGE)[1]["problems"][:1]
        # inventory and offline mirror
        inv = []
        mirror = O.LocalBackend(os.path.join(OUT, "store"))
        for key in backend.list(""):
            h = s3.head_object(Bucket=BUCKET, Key=key, ChecksumMode="ENABLED")
            ru = h.get("ObjectLockRetainUntilDate")
            inv.append({"key": key, "version_id": h.get("VersionId"), "mode": h.get("ObjectLockMode"),
                        "retain_until": ru.isoformat() if ru else None, "sha256_b64": h.get("ChecksumSHA256"),
                        "size": h.get("ContentLength")})
            mirror.put(key, backend.get(key), (ru - _dt.timedelta(seconds=1)).date())
        write_json(os.path.join(OUT, "s3-inventory.json"), {"bucket": BUCKET, "endpoint": "moto %s server (local)"
                                                             % tool_version("moto"), "objects": inv})
        mirror_problems = ES.EvidenceStore(mirror).verify(trust, deep=True)
        cp_key, cp = store.latest_checkpoint()
        write_json(os.path.join(OUT, "latest-checkpoint.json"), cp)
        results["store"] = {"objects": len(inv), "bytes": sum(o["size"] or 0 for o in inv),
                            "all_compliance_mode": all(o["mode"] == "COMPLIANCE" for o in inv),
                            "verify_problems": problems, "verify_seconds": round(t_verify, 3),
                            "offline_mirror_verify_problems": mirror_problems, "negative_checks": neg,
                            "latest_checkpoint": cp_key, "tree_size": store.tree.size,
                            "root_hash": store.tree.root().hex()}
        results["feeds"] = {"osv_records": len(osv_all), "packages": sorted(names),
                            "kev_catalog_version": kev_doc.get("catalogVersion"), "kev_count": kev_doc.get("count"),
                            "fetch_seconds": round(t_feeds, 2)}
        e2e = [v_["timings_s"]["end_to_end_excluding_download"] for v_ in results["versions"]]
        results["summary"] = {
            "versions": len(e2e), "mean_end_to_end_s": round(sum(e2e) / len(e2e), 2),
            "max_end_to_end_s": round(max(e2e), 2),
            "mean_build_s": round(sum(v_["timings_s"]["build"] for v_ in results["versions"]) / len(e2e), 2),
            "all_bit_identical": all(v_["reproducibility"]["bit_identical"] for v_ in results["versions"]),
            "payload_identical_to_pypi": sum(v_["reproducibility"]["payload_files_identical_to_pypi_wheel"]
                                             for v_ in results["versions"]),
            "gate_at_release": {d_: sum(1 for v_ in results["versions"] if v_["gate_at_release"] == d_)
                                for d_ in ("PASS", "REVIEW", "FAIL")},
            "gate_today": {d_: sum(1 for v_ in results["versions"] if v_["gate_today"] == d_)
                           for d_ in ("PASS", "REVIEW", "FAIL")},
            "run_seconds": round(time.perf_counter() - t_run, 1)}
        write_json(os.path.join(RES, "pilot-results.json"), results)
        log("summary:", json.dumps(results["summary"]))
        log("store verify:", problems or "OK", "| mirror verify:", mirror_problems or "OK")
        return 0 if not problems and not mirror_problems else 1
    finally:
        shutil.rmtree(work, ignore_errors=True)
        tsa_local.stop()
        moto.stop()


if __name__ == "__main__":
    sys.exit(main())
