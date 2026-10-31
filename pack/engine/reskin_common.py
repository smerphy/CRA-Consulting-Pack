"""Shared helpers for the client re-skin renderers (diagnostic, portal, classifier, manifest)."""
import datetime as dt
import html
import json
import re
from pathlib import Path

ENGINE = Path(__file__).resolve().parent
PACK = ENGINE.parent
TEMPLATES = ENGINE / "templates"

# The reference engagement the file-based pages in pack/out/ were built for.
REFERENCE = {
    "client": "Example Group",
    "codename": "Project Rampart",
    "advisor": "[Advisor]",
    "version": "1.0",
    "issue_date": "31 Oct 2026",
    "facts_as_at": "30 Oct 2026",
}

# Hosted deliverables that carry no client data (market research, design system, regulatory knowledge base).
SHARED_HOSTED = ("D06", "DS", "KB")
# Hosted deliverables that hold client data and must be re-produced per client.
CLIENT_HOSTED = ("D01", "D02", "D03", "D04", "D05", "D07", "D09", "D14")
# Deliverables regenerated locally by reskin.py.
LOCAL = ("D08", "D10", "D11", "D12", "D13")

# Short readable phrase per diagnostic domain (used in sentences such as "X is weakest at 16%").
DOMAIN_PHRASE = {
    "D1": "Governance and accountability", "D2": "Scope and classification", "D3": "Risk assessment and secure design",
    "D4": "Secure development and testing", "D5": "Supply chain and SBOM", "D6": "Vulnerability handling",
    "D7": "Updates and support", "D8": "Article 14 reporting", "D9": "Documentation and declaration",
    "D10": "Conformity and market access",
}

TOKEN_RE = re.compile(r"\{\{[A-Z_]+(?::[A-Za-z0-9_]+)?\}\}")


def h(s):
    """HTML-escape text content (quotes untouched, matching the hand-written pages)."""
    return html.escape(str(s), quote=False)


def h_attr(s):
    return html.escape(str(s), quote=True)


def js_dq(s):
    """Body of a double-quoted JS string literal."""
    return json.dumps(str(s), ensure_ascii=False)[1:-1].replace("</", "<\\/")


def js_sq(s):
    """Body of a single-quoted JS string literal."""
    return str(s).replace("\\", "\\\\").replace("'", "\\'").replace("\n", "\\n").replace("</", "<\\/")


def possessive(name):
    """British style: "Example Group's", "Northwind Devices'"."""
    return name + ("'" if name.endswith("s") else "'s")


def is_fictional(pd):
    return str(pd["cost_model"].get("label", "")).startswith("Illustrative")


def parse_date(s):
    return dt.datetime.strptime(s, "%d %b %Y").date()


def eur_m(x_eur, nd=1):
    return f"EUR {x_eur / 1e6:.{nd}f}m"


def fill(template, tokens, what="template"):
    out = template
    for k, v in tokens.items():
        out = out.replace("{{" + k + "}}", v)
    left = sorted(set(TOKEN_RE.findall(out)))
    if left:
        raise ValueError(f"{what}: unfilled tokens {left}")
    return out


def nb_classes_phrase(pd):
    c = pd["client"]["counts"]
    parts = []
    if c["class_i"]:
        parts.append("Class I")
    if c["class_ii"]:
        parts.append("Class II")
    if c["critical"]:
        parts.append("critical")
    if not parts:
        return "Class I and II"
    if parts == ["Class I", "Class II"]:
        return "Class I and II"
    if len(parts) == 1:
        return parts[0]
    return ", ".join(parts[:-1]) + " and " + parts[-1]


def weakest_domain(pd):
    di = pd["diagnostic"]["domain_readiness_index"]
    did = min(di, key=lambda k: di[k])  # first minimum in domain order
    return did, di[did]


def load_reference_pack_data():
    return json.loads((PACK / "data" / "pack_data.json").read_text(encoding="utf-8"))


def load_reference_urls():
    p = PACK / "out" / "urls.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}
