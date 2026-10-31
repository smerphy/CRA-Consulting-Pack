"""Derived, client-neutral view of pack_data.json for the workbook builders.

Every client-specific word that reaches a workbook cell comes from here (or straight from pack_data):
names, codename, dates, counts, product lists and programme cross-references. Builders never hard-code them.

Narrative that pack_data does not carry (a decision's rationale, an issue's next step, an assumption's
rationale) is written as a generic, data-templated default in the builder and can be overridden per client
through optional *workbook text*: either a ``workbook_text`` object inside pack_data.json or a sidecar
``workbook_text.json`` next to it. Overrides apply only when their ``client`` field matches the pack's client,
so a stale sidecar can never leak one client's narrative into another client's workbook.
"""
import datetime as dt
import json
import re
from pathlib import Path

# Default regulatory state: no CRA notified body designated. A pack can override with
# meta.notified_body_available = true once a body is designated and contracted.
NOTIFIED_BODY_AVAILABLE_DEFAULT = False
NB_CHECK_DATE_DEFAULT = "8 Sep 2026"

FULL_APPLICATION = dt.date(2027, 12, 11)
REPORTING_APPLIES = dt.date(2026, 9, 11)

_WORDS = ["zero", "one", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "eleven",
          "twelve", "thirteen", "fourteen", "fifteen", "sixteen", "seventeen", "eighteen", "nineteen", "twenty"]


def pdate(s):
    return dt.datetime.strptime(s, "%d %b %Y").date()


def fdate(d):
    return f"{d.day} {d.strftime('%b %Y')}"


def words(n):
    return _WORDS[n] if 0 <= n < len(_WORDS) else str(n)


def Words(n):
    w = words(n)
    return w[:1].upper() + w[1:]


def join(items, conj="and"):
    items = [str(i) for i in items if i not in (None, "")]
    if not items:
        return ""
    if len(items) == 1:
        return items[0]
    return ", ".join(items[:-1]) + f" {conj} " + items[-1]


def eur_m0(x):
    """EUR millions, no decimals: 'EUR 468m'."""
    return f"EUR {round(x):,}m"


def plan_class(fam):
    return "Default" if fam["cra_class"].startswith("Default") else fam["cra_class"]


class Ctx:
    def __init__(self, D, pack_data_path=None):
        self.D = D
        m, cl = D["meta"], D["client"]
        self.meta, self.cl = m, cl
        self.client = cl.get("name") or m["illustrative_client"]
        self.codename = m["programme_codename"]
        self.CODENAME = self.codename.upper()
        self.ver = str(m["version"])
        self.v = f"v{self.ver}"
        self.issue = m["issue_date"]
        self.issue_date = pdate(self.issue)
        self.facts = m["facts_as_at"]
        self.board = m["board_meeting"]
        self.board_date = pdate(self.board)
        self.steerco = m["steerco_1"]
        self.steerco_date = pdate(self.steerco)
        self.baseline = D["diagnostic"]["baseline_date"]
        self.kickoff = D["programme"].get("kickoff", "")
        self.advisor = m["advisor_placeholder"]
        self.days_board = m.get("days_to_full_application_from_board", (FULL_APPLICATION - self.board_date).days)
        fictional = "fictional" in (m.get("classification_label", "") + cl.get("disclaimer", "")).lower()
        self.client_pos = self.client + ("'" if self.client.endswith("s") else "'s")
        self.engagement = (f"Illustrative engagement — {self.client} (fictional)" if fictional
                           else f"Engagement — {self.client}")
        # notified-body state (data-driven, defaults to 'none designated')
        self.nb_available = bool(m.get("notified_body_available", NOTIFIED_BODY_AVAILABLE_DEFAULT))
        self.nb_check = m.get("notified_body_check_date") or self._nb_check_from_facts() or NB_CHECK_DATE_DEFAULT
        # portfolio
        self.fams = list(cl["product_families"])
        self.fam_by_id = {f["id"]: f for f in self.fams}
        self.bus = list(cl["business_units"])
        self.bu_ids = [b["id"] for b in self.bus]
        self.bu_by_id = {b["id"]: b for b in self.bus}
        self.legacy = list(cl.get("legacy_lines", []))
        self.legacy_sold = [l for l in self.legacy if l.get("still_sold_after_dec_2027")]
        self.nb_fams = [f for f in self.fams if f.get("needs_notified_body")]
        self.prov_fams = [f for f in self.fams if "provisional" in f["cra_class"].lower()]
        self.pilot_fams = [f for f in self.fams if "pilot" in f.get("wave", "").lower()]
        # programme lookups
        PG = D["programme"]
        self.tasks = {t["id"]: t for t in PG.get("mobilisation_plan", [])}
        self.milestones = {x["id"]: x for x in PG.get("milestones", [])}
        self.workstreams = {w["id"]: w for w in PG.get("workstreams", [])}
        self.risks = {r["id"]: r for r in D.get("risks", [])}
        self.issues = {i["id"]: i for i in D.get("issues", [])}
        self.kpis = {k["id"]: k for k in D.get("kpis", [])}
        decs = D.get("decisions", {})
        self.decisions = {d["id"]: d for grp in decs.values() for d in grp}
        self.stakeholders = {s["id"]: s for s in D.get("stakeholders", [])}
        self.facts_by_id = {f["id"]: f for f in D.get("facts", [])}
        self.text = self._load_text(pack_data_path)

    # ---------------- workbook text overrides ----------------
    def _load_text(self, pack_data_path):
        cand = []
        if isinstance(self.D.get("workbook_text"), dict):
            cand.append(self.D["workbook_text"])
        if pack_data_path is not None:
            side = Path(pack_data_path).with_name("workbook_text.json")
            if side.exists():
                cand.append(json.loads(side.read_text()))
        for c in cand:
            if c.get("client") == self.client and c.get("programme_codename", self.codename) == self.codename:
                return dict(c.get("text", {}))
        return {}

    def t(self, key, default):
        """Workbook text slot: client override if present, else the generic data-templated default."""
        return self.text.get(key, default)

    # ---------------- helpers ----------------
    def _nb_check_from_facts(self):
        for f in self.D.get("facts", []):
            mm = re.search(r"checks to (\d{1,2} [A-Z][a-z]{2} \d{4})", f.get("statement", ""))
            if mm and "notified body" in f.get("statement", "").lower():
                return mm.group(1)
        return None

    @property
    def nfam(self):
        return len(self.fams)

    @staticmethod
    def short(f):
        """Short product reference: model number if the name starts with one, otherwise the family ID."""
        tok = f["name"].split()[0]
        return tok if any(ch.isdigit() for ch in tok) else f["id"]

    @staticmethod
    def label(f):
        """Product name as used in prose: the model number if the name starts with one, the full name when it
        ends in the ID, a CamelCase brand word ('FleetView Device Manager' -> 'FleetView'), else the full name."""
        parts = f["name"].split()
        if any(ch.isdigit() for ch in parts[0]):
            return parts[0]
        if parts[-1] == f["id"]:
            return f["name"]
        if any(ch.isupper() for ch in parts[0][1:]):
            return parts[0]
        return f["name"]

    def fam(self, fid):
        return self.fam_by_id.get(fid)

    def labels(self, fams, sort=False):
        out = [self.label(f) for f in fams]
        return sorted(out, key=str.lower) if sort else out

    def shorts(self, fams):
        return [self.short(f) for f in fams]

    def fams_by_class(self, cls):
        return [f for f in self.fams if plan_class(f) == cls]

    def fams_by_route(self, word):
        return [f for f in self.fams if word in f.get("route", "")]

    def ms_date(self, mid, default=""):
        m = self.milestones.get(mid)
        return m["date"] if m else default

    def task_end(self, tid, default=""):
        t = self.tasks.get(tid)
        return t["end"] if t else default

    def has(self, *ids):
        pools = (self.tasks, self.milestones, self.workstreams, self.risks, self.issues, self.kpis, self.decisions,
                 self.stakeholders)
        return all(any(i in p for p in pools) for i in ids)

    def ids(self, *ids, sep=", "):
        """Join the cross-reference IDs that exist in this pack."""
        return sep.join(i for i in ids if self.has(i))

    def find_task(self, pred, default=None):
        for t in self.tasks.values():
            if pred(t):
                return t
        return default

    def find_decision(self, pred, default=None):
        for d in self.decisions.values():
            if pred(d):
                return d
        return default

    def module_h_scope(self):
        """'IC families + FleetView': Module H families grouped by business unit."""
        fams = self.fams_by_route("Module H")
        parts = []
        for bu in self.bu_ids:
            fs = [f for f in fams if f["bu"] == bu]
            if len(fs) > 1:
                parts.append(f"{bu} families")
            elif fs:
                parts.append(self.label(fs[0]))
        return " + ".join(parts)

    def module_h_bu(self):
        """Business unit with the most Module H families (the quality system in scope)."""
        fams = self.fams_by_route("Module H")
        counts = {bu: sum(1 for f in fams if f["bu"] == bu) for bu in self.bu_ids}
        return max(counts, key=counts.get) if fams else ""

    @property
    def nb_status(self):
        if self.nb_available:
            return "CRA notified body designated and contracted"
        return f"No CRA notified body verifiably designated (checks to {self.nb_check})"

    @property
    def saas_bu(self):
        saas = self.cl.get("saas") or {}
        if saas.get("bu") in self.bu_ids:
            return saas["bu"]
        for b in self.bus:
            if "saas" in b.get("profile", "").lower():
                return b["id"]
        return self.bu_ids[-1]

    @property
    def saas_revenue_m(self):
        saas = self.cl.get("saas") or {}
        return self.cl.get("counts", {}).get("saas_revenue_m", saas.get("revenue_m", 0)) or 0

    def phase(self, pid):
        for p in self.D["programme"].get("phases", []):
            if p["id"] == pid:
                return p
        return None

    def decision_id(self, pred, prefix="", default=""):
        for d in self.decisions.values():
            if d["id"].startswith(prefix) and pred((d.get("decision", "") + " " + d.get("detail", "")).lower()):
                return d["id"]
        return default

    def issue_id(self, pred, default=""):
        for i in self.issues.values():
            if pred((i.get("title", "") + " " + i.get("description", "")).lower()):
                return i["id"]
        return default

    def task_id(self, pred, default=""):
        for t in self.tasks.values():
            if pred(t["task"].lower()):
                return t["id"]
        return default

    @property
    def country(self):
        return self.cl.get("hq", "").split(" (")[0].strip()

    @property
    def is_sme(self):
        return self.cl.get("employees", 0) < 250

    @property
    def rev_m(self):
        return sum(b["revenue_m"] for b in self.bus)

    @property
    def eu_nb_m(self):
        return self.cl.get("eu_revenue_needing_notified_body_m",
                           sum(f["eu_revenue_m"] for f in self.nb_fams))

    @property
    def eu_nb_share(self):
        return self.cl.get("eu_revenue_needing_notified_body_share_of_group", self.eu_nb_m / self.rev_m)

    def support_years_range(self):
        ys = [f["support_period_years"] for f in self.fams]
        return (min(ys), max(ys)) if ys else (5, 5)

    def provisional_annex_items(self):
        nums = set()
        for f in self.prov_fams:
            nums.update(int(n) for n in re.findall(r"item (\d+)", f.get("annex_item", "")))
        return sorted(nums)
