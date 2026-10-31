"""Single source of truth for the CRA Readiness Programme Pack.

Everything client-specific here is ILLUSTRATIVE (fictional client "Example Group").
Regulatory facts are taken from the knowledge base files under ../reports.
Run:  python3 pack/build_data.py   -> writes data/pack_data.json and data/DATA_SUMMARY.md
"""
import json, random, math, datetime as dt
from pathlib import Path
from collections import OrderedDict

DATA_DIR = Path(__file__).resolve().parent / "data"
OUT_JSON = DATA_DIR / "pack_data.json"
OUT_MD = DATA_DIR / "DATA_SUMMARY.md"

AS_AT = dt.date(2026, 10, 30)          # facts verified to
PACK_DATE = dt.date(2026, 10, 31)      # pack issue date
FULL_APPLICATION = dt.date(2027, 12, 11)
BOARD_DATE = dt.date(2026, 11, 19)
STEERCO1 = dt.date(2026, 10, 30)

def fmt_date(d):
    return d.strftime("%-d %b %Y")

meta = OrderedDict(
    pack_name="EU Cyber Resilience Act Readiness Programme",
    pack_short="CRA Readiness Programme Pack",
    version="1.0",
    issue_date=fmt_date(PACK_DATE),
    facts_as_at=fmt_date(AS_AT),
    illustrative_client="Example Group",
    programme_codename="Project Rampart",
    advisor_placeholder="[Advisor]",
    classification_label="Illustrative engagement — fictional client data; regulatory facts verified to 30 Oct 2026",
    days_to_full_application_from_issue=(FULL_APPLICATION - PACK_DATE).days,
    days_to_full_application_from_board=(FULL_APPLICATION - BOARD_DATE).days,
    board_meeting=fmt_date(BOARD_DATE),
    steerco_1=fmt_date(STEERCO1),
    knowledge_base_url="https://claude.ai/artifact/JC24c3EC3qR8Xz8k3858Wj",
)

brand = OrderedDict(
    design_system_name="Advisory Design System (white-label)",
    voice="Calm, exact, decision-oriented. British English. Action titles that state the so-what. No hype, no emoji.",
    fonts=OrderedDict(display="Source Serif 4", body="Inter", mono="JetBrains Mono",
                      fallbacks="Georgia, 'Times New Roman', serif / system-ui, -apple-system, Segoe UI, Arial, sans-serif"),
    colors=OrderedDict(
        ink_900="#0E1A2B", ink_700="#26364D", ink_500="#56667E", ink_300="#C5CDD8", ink_100="#EEF1F5",
        paper="#FAFAF7", surface="#FFFFFF",
        accent_700="#0A5753", accent_600="#0F6E6A", accent_400="#2E9C93", accent_100="#DCEFEC",
        signal="#C2410C",
        rag_red="#B42318", rag_amber="#B54708", rag_green="#027A48", rag_grey="#8A94A6",
    ),
    dataviz_categorical=["#0F6E6A", "#1F3A5F", "#5B8DB8", "#C9A66B", "#B9573E", "#8A94A6"],
    maturity_scale_colors={"0": "#B42318", "1": "#E07A5F", "2": "#E9C46A", "3": "#7FB8A4", "4": "#0F6E6A"},
    rules=[
        "Every slide/page has an action title: one full sentence stating the so-what (max ~15 words).",
        "One message per slide; a tracker/section label top-left; source line bottom-left on any data slide.",
        "Client numbers carry an 'Illustrative' tag; vendor/survey numbers carry their source and type.",
        "Money as EUR with 'm'/'k' (EUR 9.3m, EUR 210k) or the euro sign; dates as 11 Dec 2027.",
        "RAG colours only for status; accent teal for emphasis; signal orange only for the binding constraint.",
        "No real company names for the client, no named individuals: roles only.",
    ],
)

storyline = OrderedDict(
    governing_thought=("The CRA turns product cybersecurity into a licence to sell in the EU. Example Group can be ready by "
                       "11 Dec 2027, but only if it secures third-party assessment capacity and builds shared compliance "
                       "infrastructure in the next two quarters."),
    scqa=OrderedDict(
        situation=("The Cyber Resilience Act (Regulation (EU) 2024/2847) has been in force since 10 Dec 2024. Article 14 "
                   "reporting has applied since 11 Sep 2026 to every in-scope product, including those already sold. "
                   "Everything else applies from 11 Dec 2027."),
        complication=("Three things make this harder than a normal compliance project: reporting is already live on a "
                      "24-hour clock; seven of Example Group's thirteen product families need a notified body or a cited "
                      "harmonised standard, and neither exists today; and compliance must be proven with evidence for "
                      "every product version for at least ten years."),
        question="What must Example Group do, by when and at what cost to keep selling in the EU after 11 Dec 2027?",
        answer=("Run a 14-month, three-wave programme (Project Rampart): build shared capabilities once (PSIRT, SBOM, "
                "secure updates, evidence system), apply them product by product, and lock in notified-body capacity by "
                "Q1 2027. Investment is about __ONEOFF__ to Dec 2027 and __RUN__ a year to run. The board is asked to take "
                "five decisions on 19 Nov 2026."),
    ),
    pillars=[
        OrderedDict(title="Reporting is already law", message="Every in-scope product — legacy included — is on a 24-hour reporting clock today.",
                    proof="Art 14 applies since 11 Sep 2026 (Art 69(3)); early warning 24h, notification 72h, final report 14 days / 1 month."),
        OrderedDict(title="Market access is the binding constraint", message="__EUNB__ of annual EU revenue sits in Class I and II products that need a notified body that does not yet exist.",
                    proof="No harmonised standard cited; no CRA notified body designated at checks to 8 Sep 2026; vendor estimates of 12-18 months per body."),
        OrderedDict(title="Compliance is an evidence system, not a project", message="Build once, apply per product version, sustain for ten years.",
                    proof="Annex VII file per version; retention 10 years or support period (Art 13(13)); PLD disclosure from 9 Dec 2026."),
    ],
)

# ---------------- Illustrative client ----------------
bus = [
    OrderedDict(id="HBS", name="Home & Building Solutions", revenue_m=520, eu_share=0.74,
                profile="Consumer and building connected devices sold through retail, installers and online; all radio products (RED/EN 18031 assessed 2025)."),
    OrderedDict(id="IC", name="Industrial Connectivity", revenue_m=560, eu_share=0.66,
                profile="Industrial networking and security appliances sold to OEMs, integrators and utilities; IEC 62443-4-1 certified development process (2024)."),
    OrderedDict(id="SS", name="Software & Services", revenue_m=120, eu_share=0.58,
                profile="Device-management software, configuration tools, SDK and a cloud platform (SaaS, EUR 30m) that is remote data processing for several products."),
]
bu_by_id = {b["id"]: b for b in bus}

families = [
 # id, name, bu, class, annex_item, rev, skus, wave, route, support_years, rdps, description
 ("T200", "T200 Smart Thermostat", "HBS", "Default", "-", 170, 6, "Wave 1 (pilot)", "Module A", 10,
  "Cloud control service; update service", "Thermostat, iOS/Android app and manufacturer cloud; the pilot family."),
 ("SSR", "S-Series Room Sensors", "HBS", "Default", "-", 80, 9, "Wave 2", "Module A", 8,
  "Via HomeHub H3 and cloud", "Battery room sensors (temperature, presence, air quality)."),
 ("H3", "HomeHub H3", "HBS", "Default (provisional)", "Under legal review vs Annex III Class I item 17 (optional alarm mode)", 95, 3, "Wave 2", "Module A (B+C if Class I)", 7,
  "Cloud control; remote access relay", "Smart-home hub bridging Zigbee/Thread devices to the app; its optional alarm mode makes the classification borderline."),
 ("V1", "V1 Video Doorbell", "HBS", "Class I", "Annex III Class I item 17 (security cameras)", 100, 4, "Wave 1", "Module B+C", 7,
  "Video cloud; event notification service", "Video doorbell with camera, two-way audio and cloud recording."),
 ("L2", "L2 Smart Lock", "HBS", "Class I", "Annex III Class I item 17 (smart door locks)", 75, 3, "Wave 1", "Module B+C", 10,
  "Access-management cloud", "Smart door lock with app keys and guest access."),
 ("IR500", "IR-500 Industrial Router", "IC", "Class I", "Annex III Class I item 12 (routers, modems, switches)", 165, 7, "Wave 1", "Module H", 12,
  "Optional FleetView Cloud management", "Cellular/fibre industrial routers for OT sites."),
 ("IS300", "IS-300 Managed Switch", "IC", "Class I", "Annex III Class I item 12 (routers, modems, switches)", 120, 10, "Wave 1", "Module H", 12,
  "Optional FleetView Cloud management", "Managed industrial Ethernet switches."),
 ("EG700", "EG-700 Edge Gateway", "IC", "Default (provisional)", "Under legal review vs Annex III Class I item 12 (cellular uplink routing)", 95, 4, "Wave 2", "Module A (H if Class I)", 10,
  "Cloud data connector; update service", "Edge gateway for protocol translation and edge compute; its cellular uplink routing makes the classification borderline."),
 ("SG900", "SG-900 Industrial Firewall/IDS", "IC", "Class II", "Annex III Class II item 2 (firewalls, IDS/IPS)", 110, 3, "Wave 1", "Module H", 10,
  "Threat-signature update service", "Industrial firewall with intrusion detection and prevention."),
 ("SLINK", "SecureLink Remote Access", "IC", "Class I", "Annex III Class I item 5 (VPN products)", 70, 2, "Wave 1", "Module H", 7,
  "Broker service; licence service", "Remote-access VPN software and appliance for machine builders."),
 ("FLEET", "FleetView Device Manager", "SS", "Class I", "Annex III Class I item 6 (network management systems)", 55, 2, "Wave 1", "Module H", 5,
  "None (on-prem); cloud edition is SaaS", "On-premises network and device management software (per-version support periods)."),
 ("CSTUDIO", "ConfigStudio", "SS", "Default", "-", 15, 1, "Wave 2", "Module A", 5,
  "Licence service", "Desktop configuration and commissioning tool."),
 ("SDK", "Example IoT SDK", "SS", "Default", "-", 20, 1, "Wave 2", "Module A", 5,
  "None", "SDK and libraries licensed to OEMs; integrated into third-party products."),
]
fam_list = []
for (fid, name, bu, cls, item, rev, skus, wave, route, sp, rdps, desc) in families:
    eu = round(rev * bu_by_id[bu]["eu_share"], 1)
    needs_nb = cls in ("Class I", "Class II")
    fam_list.append(OrderedDict(id=fid, name=name, bu=bu, bu_name=bu_by_id[bu]["name"], cra_class=cls, annex_item=item,
        revenue_m=rev, eu_revenue_m=eu, skus=skus, wave=wave, route=route, needs_notified_body=needs_nb,
        support_period_years=sp, rdps=rdps, description=desc))

legacy = [
    OrderedDict(id="T100", name="T100 Thermostat (gen 1)", bu="HBS", status="End of sale 2025; support ended Mar 2026", units_in_field_k=1100, still_sold_after_dec_2027=False, eu_revenue_m=0),
    OrderedDict(id="H2", name="HomeHub H2", bu="HBS", status="End of sale 2024; security fixes to Dec 2026", units_in_field_k=420, still_sold_after_dec_2027=False, eu_revenue_m=0),
    OrderedDict(id="V0", name="V0 Indoor Camera", bu="HBS", status="End of sale 2023; unsupported", units_in_field_k=260, still_sold_after_dec_2027=False, eu_revenue_m=0),
    OrderedDict(id="IR300", name="IR-300 Router", bu="IC", status="Still sold to two OEM customers", units_in_field_k=95, still_sold_after_dec_2027=True, eu_revenue_m=11),
    OrderedDict(id="IS200", name="IS-200 Switch", bu="IC", status="Still sold as low-cost option", units_in_field_k=140, still_sold_after_dec_2027=True, eu_revenue_m=7),
    OrderedDict(id="SL3", name="SecureLink 3.x", bu="IC", status="Support ends Jun 2027", units_in_field_k=18, still_sold_after_dec_2027=False, eu_revenue_m=0),
    OrderedDict(id="FV4", name="FleetView 4.x", bu="SS", status="Support ends Dec 2026", units_in_field_k=3, still_sold_after_dec_2027=False, eu_revenue_m=0),
]

total_rev = sum(b["revenue_m"] for b in bus)
eu_total = round(sum(b["revenue_m"] * b["eu_share"] for b in bus), 1)
rev_by_class = OrderedDict()
eu_by_class = OrderedDict()
for f in fam_list:
    k = "Default" if f["cra_class"].startswith("Default") else f["cra_class"]
    rev_by_class[k] = rev_by_class.get(k, 0) + f["revenue_m"]
    eu_by_class[k] = round(eu_by_class.get(k, 0) + f["eu_revenue_m"], 1)
eu_nb = round(sum(f["eu_revenue_m"] for f in fam_list if f["needs_notified_body"]), 1)

client = OrderedDict(
    name="Example Group",
    disclaimer="Fictional company used to illustrate the method. Replace with the client's data.",
    hq="Germany (main establishment; coordinator CSIRT is Germany's)",
    revenue_m=total_rev, eu_revenue_m=eu_total, eu_share=round(eu_total / total_rev, 3),
    employees=3800, engineers=920, suppliers_in_scope=41,
    installed_base_m=2.3,
    existing_assurance=["ISO/IEC 27001 (corporate IT scope only)", "IEC 62443-4-1 (Industrial Connectivity development process, 2024)",
                        "EN 18031-1 assessments for HBS radio products under the RED delegated act (2025)",
                        "Two-person PSIRT in Industrial Connectivity; no PSIRT in HBS or S&S before Sep 2026"],
    business_units=bus, product_families=fam_list, legacy_lines=legacy,
    counts=OrderedDict(
        families=len(fam_list), skus=sum(f["skus"] for f in fam_list),
        default=sum(1 for f in fam_list if f["cra_class"].startswith("Default")),
        class_i=sum(1 for f in fam_list if f["cra_class"] == "Class I"),
        class_ii=sum(1 for f in fam_list if f["cra_class"] == "Class II"),
        critical=0, provisional=sum(1 for f in fam_list if "provisional" in f["cra_class"]),
        legacy_lines=len(legacy), saas_revenue_m=30,
    ),
    revenue_by_class_m=rev_by_class, eu_revenue_by_class_m=eu_by_class,
    eu_revenue_in_scope_products_m=round(sum(eu_by_class.values()), 1),
    eu_revenue_saas_not_a_product_m=round(30 * bu_by_id["SS"]["eu_share"], 1),
    eu_revenue_needing_notified_body_m=eu_nb,
    eu_revenue_needing_notified_body_share_of_group=round(eu_nb / total_rev, 3),
    routes=OrderedDict(module_a=[f["id"] for f in fam_list if f["route"].startswith("Module A")],
                       module_bc=[f["id"] for f in fam_list if f["route"] == "Module B+C"],
                       module_h=[f["id"] for f in fam_list if f["route"] == "Module H"]),
)

exposure = OrderedDict(
    fine_tiers=[
        OrderedDict(tier="Tier 1 — Annex I essential requirements; Arts 13 and 14", fixed_m=15, pct=2.5,
                    example_group_max_m=max(15, 0.025 * total_rev), basis="Art 64(2)"),
        OrderedDict(tier="Tier 2 — other obligations (e.g. Arts 18-23, 28, 30-33)", fixed_m=10, pct=2.0,
                    example_group_max_m=max(10, 0.02 * total_rev), basis="Art 64(3)"),
        OrderedDict(tier="Tier 3 — incorrect, incomplete or misleading information", fixed_m=5, pct=1.0,
                    example_group_max_m=max(5, 0.01 * total_rev), basis="Art 64(4)"),
    ],
    note="Fines are the higher of the fixed amount and the percentage of worldwide annual turnover. Enforcement machinery applies from 11 Dec 2027; micro and small enterprises are exempt from fines for missing the 24-hour deadlines (Art 64(10)(a)).",
    market_access=OrderedDict(eu_revenue_needing_notified_body_m=eu_nb, families=[f["id"] for f in fam_list if f["needs_notified_body"]],
                              note="Products that cannot be assessed may not be placed on the EU market from 11 Dec 2027; authorities can order withdrawal or recall (Arts 54-58)."),
    product_liability="Directive (EU) 2024/2853 applies to products placed on the market from 9 Dec 2026: software is a product, a vulnerability can be a defect, non-compliance with mandatory safety requirements raises a presumption of defectiveness (Art 10(2)(b)), and courts can order disclosure of evidence (Art 9).",
    legacy_decision=OrderedDict(lines=["IR300", "IS200"], eu_revenue_m=18, remediation_cost_estimate_m=1.4,
                                recommendation="Withdraw IR-300 and IS-200 from EU sale before 11 Dec 2027 and migrate customers to IR-500/IS-300; remediation would cost about EUR 1.4m plus notified-body fees for EUR 18m of declining EU revenue."),
)

# ---------------- Diagnostic ----------------
scale = [
    OrderedDict(level=0, name="Not started", descriptor="Nothing exists yet."),
    OrderedDict(level=1, name="Initial", descriptor="Ad hoc or individual effort; not documented."),
    OrderedDict(level=2, name="Defined", descriptor="Documented and partly applied; gaps known."),
    OrderedDict(level=3, name="Implemented", descriptor="Applied consistently for this product, with evidence."),
    OrderedDict(level=4, name="Assured", descriptor="Measured, independently reviewed and audit-ready."),
]

Q = lambda qid, text, basis, evidence, action: OrderedDict(id=qid, text=text, basis=basis, evidence=evidence, action=action)
domains = [
 OrderedDict(id="D1", name="Governance and accountability", short="Governance", questions=[
  Q("Q1.1", "A named executive is accountable for CRA compliance, with written authority to block a release and to sign EU declarations of conformity.", "Art 13(1); Art 28(4)", "Board or ExCo instrument naming the accountable executive and the DoC signatory", "Execute a signing instrument naming the DoC signatory, alternate and scope; write release-blocking authority into the sponsor's mandate."),
  Q("Q1.2", "The core CRA roles (compliance lead, product security officer, PSIRT lead) are filled by named people with deputies.", "Art 13; BSI TR-03183-3 s4.3", "Role descriptions, appointments, deputy chain", "Appoint named role holders and deputies; publish the RACI with one accountable person per decision."),
  Q("Q1.3", "A written product-risk acceptance rule excludes cost, risk appetite and commercial strategy as reasons to leave risk unaddressed.", "Annex I Part I(1); guidance C(2026) 5252 paras 156-163", "Risk policy section for the product-risk category; acceptance log", "Add a product-risk category to the enterprise risk framework with its own acceptance authority and a non-cost appeal route."),
  Q("Q1.4", "A programme board reviews CRA readiness monthly against KPIs drawn from a system of record.", "Good practice; Annex VIII Module H pt 3.2", "Programme board minutes; KPI pack", "Run a monthly programme board with a standing agenda and KPIs read from the system of record."),
 ]),
 OrderedDict(id="D2", name="Scope, inventory and classification", short="Scope & class", questions=[
  Q("Q2.1", "Every product, version, variant, companion app and backend is in a register with a recorded scope decision.", "Art 2(1); Art 3(1); guidance paras 11-16", "Scope register extract; decision records", "Build the register from release, commercial and cloud systems, then record a dated scope decision per row."),
  Q("Q2.2", "Remote data processing boundaries are mapped per product function using the three-element test.", "Art 3(2); guidance paras 184-205", "Remote-function map per product", "Map every remote function to its service, developer and fallback; classify each as RDPS, component or out of scope."),
  Q("Q2.3", "Each product has a documented class (default, Class I, Class II or critical) with a core-functionality rationale.", "Arts 7-8; Annexes III-IV; Implementing Regulation (EU) 2025/2392", "Classification decision record citing the technical description", "Classify on core functionality against the Implementing Regulation's technical descriptions; take legal review on borderline cases."),
  Q("Q2.4", "The economic-operator role per market and the legacy status of each product line are recorded.", "Arts 18-22; Art 69(2)-(3)", "Role-per-market table; legacy flags in the register", "Record manufacturer, importer, distributor or representative per market; flag lines still sold after 11 Dec 2027."),
 ]),
 OrderedDict(id="D3", name="Risk assessment and secure by design", short="Risk & design", questions=[
  Q("Q3.1", "A documented cybersecurity risk assessment exists for the product or family, covering intended purpose, foreseeable use and expected time in use.", "Art 13(2)-(3); Annex VII point 3", "Signed risk assessment", "Run a TR-03183-1-style assessment on the representative product and sign it off through the second line."),
  Q("Q3.2", "The assessment states whether and how each Annex I Part I(2)(a)-(m) item applies, with a justification for every item marked not applicable.", "Art 13(3)-(4); Recital 55", "Applicability matrix with justifications", "Complete the 13-row applicability matrix; no row may be signed with a blank justification."),
  Q("Q3.3", "Threat models and data-flow diagrams are maintained and updated on defined triggers, not on a calendar.", "Art 13(3); Annex I Part II(3); guidance paras 238-240", "Threat model versions with change log", "Wire update triggers (security-relevant release, new vulnerability, new threat) into the release and PSIRT processes."),
  Q("Q3.4", "Secure-by-default configuration (no default credentials, minimal exposed services, reset to original state) is verified at every release.", "Annex I Part I(2)(b), (j)", "Default-configuration export; reset test record", "Add a secure-default configuration check and a reset test to the release gate."),
 ]),
 OrderedDict(id="D4", name="Secure development and testing", short="SDLC & testing", questions=[
  Q("Q4.1", "A documented secure development lifecycle with a release security gate applies to every release.", "Annex I Part I(1); Annex VIII Module H pt 3.2", "SDLC procedure; release gate records", "Define the release security gate and make its signed record a precondition for tagging a release."),
  Q("Q4.2", "Every release is checked for known exploitable vulnerabilities against EUVD, NVD and the CISA KEV catalogue before it ships.", "Annex I Part I(2)(a); guidance paras 230-237", "Scan reports and VEX tied to the release SBOM", "Automate a known-exploitable check that blocks the release unless each finding is fixed or carries a VEX justification."),
  Q("Q4.3", "Security testing (static analysis, fuzzing, dynamic testing, penetration tests) is risk-driven and evidenced per release.", "Annex I Part II(3); Annex VII point 6", "Test plan with review log; test reports", "Write a threat-driven test plan per product and keep a dated review log showing what was re-tested and why."),
  Q("Q4.4", "Each release records a substantial-modification decision using the four-question test.", "Art 3(30); guidance paras 103-124", "Security-delta assessment on the gate record", "Add the four guidance questions to the release gate and route positive answers to a new declaration."),
 ]),
 OrderedDict(id="D5", name="Supply chain, SBOM and open source", short="SBOM & supply chain", questions=[
  Q("Q5.1", "A machine-readable SBOM (CycloneDX 1.6+ or SPDX 3.0.1+) is generated from the shipped artefact for every release.", "Annex I Part II(1); Annex VII point 2(b); BSI TR-03183-2", "Signed SBOM per release with quality score", "Generate SBOMs at build from the artefact, enrich to TR-03183-2 fields, sign and store them with the release."),
  Q("Q5.2", "Third-party and open-source components pass a documented due-diligence gate before use.", "Art 13(5); Recital 34; guidance paras 167-173", "Component intake records", "Run an intake gate on every new dependency recording need, maintenance signals, licence, vulnerability history and exit plan."),
  Q("Q5.3", "Supplier contracts require vulnerability notification, SBOM delivery and support-period commitments.", "Art 13(5), (8); Art 23", "Contract clause register", "Add the CRA clause pack to master agreements, starting with suppliers of security-relevant components."),
  Q("Q5.4", "Vulnerabilities found in components are reported upstream and fixes are shared with maintainers.", "Art 13(6); guidance paras 222-229", "Upstream report log in PSIRT case files", "Give PSIRT or the OSPO ownership of upstream reporting, with a duplicate check and legal pre-clearance for fix sharing."),
 ]),
 OrderedDict(id="D6", name="Vulnerability handling and disclosure", short="Vulnerability handling", questions=[
  Q("Q6.1", "A coordinated vulnerability disclosure policy, a security.txt file and a non-automated contact channel are published.", "Annex I Part II(5)-(6); Art 13(17)", "Published CVD policy URL; security.txt; intake monitoring log", "Publish the CVD policy and security.txt, add an anonymous web form and a monitored human channel."),
  Q("Q6.2", "A PSIRT triages every report and monitoring hit for severity, reachability and active exploitation.", "Annex I Part II(2); Art 14(1)", "PSIRT procedure; case files with UTC timestamps", "Open a case for every report and hit; record reachability and the exploitation decision in UTC."),
  Q("Q6.3", "Fixed vulnerabilities are disclosed in public advisories, machine-readable where appropriate, with VEX for non-affected findings.", "Annex I Part II(4); BSI TR-03183-3", "Advisory index; CSAF documents; VEX files", "Stand up an advisory page and a CSAF provider; publish VEX statements for findings that do not affect the product."),
  Q("Q6.4", "Vulnerability case records are retained and response metrics are reported.", "Art 13(7), (13)", "Quarterly PSIRT metrics; retention rule", "Report acknowledgement and fix times quarterly and retain case files for 10 years or the support period."),
 ]),
 OrderedDict(id="D7", name="Updates and support period", short="Updates & support", questions=[
  Q("Q7.1", "Updates are signed, verified before install, protected against rollback and recoverable after a failed install.", "Annex I Part I(2)(c), (f); Annex I Part II(7)", "Update design note; acceptance tests", "Move signing keys into an HSM, add anti-rollback counters and atomic install with recovery."),
  Q("Q7.2", "Security updates install automatically by default where applicable, with user notification and a clear opt-out.", "Annex I Part I(2)(c); Recital 56", "Default configuration export; Annex II point 8(e) text", "Turn automatic security updates on by default, or record the Recital 56 carve-out in the risk assessment."),
  Q("Q7.3", "Security fixes can ship separately from feature releases and remain available for at least 10 years.", "Annex I Part II(2), (8); Art 13(9)", "Maintenance branch policy; update repository retention", "Run security-only maintenance branches and an immutable update repository retained for 10 years."),
  Q("Q7.4", "A support period is set per product from expected time in use, and the end date is shown at purchase.", "Art 13(8), (19); Annex II point 7", "Support-period determination record; product page", "Determine the support period from expected use time (five years is a floor) and publish the end month and year."),
 ]),
 OrderedDict(id="D8", name="Article 14 reporting readiness", short="Art 14 reporting", questions=[
  Q("Q8.1", "At least two Assigned Representatives are registered on the ENISA Single Reporting Platform with MFA, and the coordinator CSIRT is decided.", "Art 14(7); ENISA SRP FAQ 9, 18", "SRP roster; coordinator CSIRT decision record", "Register two or more personal EU Logins with MFA and record the main-establishment decision before any incident."),
  Q("Q8.2", "Written awareness criteria and a 24/7 on-call chain allow an early warning to be filed within 24 hours, including at weekends.", "Art 14(2)(a), (4)(a); guidance para 213", "PSIRT runbook; on-call rota; deputy chain", "Write the awareness test into the runbook and give the PSIRT lead and deputies authority to file without prior approval."),
  Q("Q8.3", "Templates for the 24-hour, 72-hour and final reports and for user notification exist and have been rehearsed.", "Art 14(2)-(4), (8); ENISA SRP glossary", "Templates; drill records", "Draft templates on the SRP glossary fields and run two paper drills a year, one vulnerability and one incident."),
  Q("Q8.4", "Legacy and end-of-support products are included in the reportable inventory.", "Art 69(3); guidance para 210", "Reportable inventory including legacy lines", "Add every in-scope product still in use to the reportable inventory, including lines no longer sold or supported."),
 ]),
 OrderedDict(id="D9", name="Documentation, user information and declaration", short="Documentation & DoC", questions=[
  Q("Q9.1", "An Annex VII technical file exists for each product version and is versioned with releases.", "Art 31; Art 13(12)-(13); Annex VII", "Technical file index per version", "Adopt the 13-part file outline and generate version-linked contents from the release pipeline."),
  Q("Q9.2", "Annex II user information, including the support end date and the vulnerability contact, is drafted and ready to publish.", "Art 13(18)-(19); Annex II", "Annex II document per product", "Draft the Annex II document per product family and publish it at a stable, versioned URL."),
  Q("Q9.3", "The EU declaration of conformity format, signing authority and CE marking placement are decided.", "Arts 28-30; Annexes V-VI", "DoC template; signing instrument; CE placement record", "Agree the DoC template and languages, the signing instrument and where the CE marking sits for hardware and software."),
  Q("Q9.4", "Evidence sits in a system of record with 10-year retention and can answer a reasoned request within 10 working days.", "Art 13(13), (22); Art 64(4)", "System of record; tested request export", "Select a system of record, compute retention per version and test an end-to-end reasoned-request export."),
 ]),
 OrderedDict(id="D10", name="Conformity assessment and market access", short="Conformity & access", questions=[
  Q("Q10.1", "The conformity route for the product (Module A, B+C or H) is decided, with a fallback.", "Art 32; Annex VIII", "Route decision record", "Decide the route per family; for Class I, plan third-party assessment until a harmonised standard is cited."),
  Q("Q10.2", "Candidate notified bodies are shortlisted and a pre-assessment is contracted where the route needs one.", "Art 32(2)-(3); Arts 35-43", "Shortlist; pre-assessment contract", "Shortlist three candidates, contract pre-assessments with conversion options, and check NANDO at every programme board."),
  Q("Q10.3", "A complete Module A internal-control record is kept for the product, even where a notified body will be used.", "Annex VIII Module A", "Internal-control record with evidence index", "Build the Module A record and evidence index now; it is the fallback and the body's application pack."),
  Q("Q10.4", "EU representation, importer and distributor duties and marketplace arrangements are settled for each market.", "Arts 18-20; Regulation (EU) 2019/1020 Art 4", "Representation decision per market; mandates", "Confirm the role per market, appoint an authorised representative where useful and brief importers on their checks."),
 ]),
]
qids = [q["id"] for d in domains for q in d["questions"]]

# Baseline generation (deterministic)
bu_base = {
 "HBS": {"D2": 1.1, "D3": 1.3, "D4": 0.9, "D5": 0.6, "D6": 0.6, "D7": 1.6, "D9": 0.6, "D10": 0.3},
 "IC":  {"D2": 1.5, "D3": 1.6, "D4": 2.3, "D5": 1.0, "D6": 1.8, "D7": 1.5, "D9": 0.8, "D10": 0.7},
 "SS":  {"D2": 1.3, "D3": 0.8, "D4": 1.8, "D5": 1.5, "D6": 0.8, "D7": 1.1, "D9": 0.6, "D10": 0.3},
}
fam_adj = {
 "T200": {"D2": 0.6, "D3": 0.6, "D5": 0.6, "D9": 0.5, "D10": 0.5},
 "SG900": {"D3": 0.3, "D4": 0.3, "D6": 0.3},
 "EG700": {"D2": -0.4},
 "H3": {"D2": -0.4},
 "SDK": {"D7": -0.6},
 "CSTUDIO": {"D7": -0.3},
 "V1": {"D10": -0.3}, "L2": {"D10": -0.3},
}
q_offset = {  # per question position within domain
 "D2": [0.3, -0.2, 0.2, -0.3], "D3": [0.4, -0.3, -0.2, 0.1], "D4": [0.3, 0.2, -0.1, -0.4],
 "D5": [0.2, -0.1, -0.3, 0.2], "D6": [0.4, 0.2, -0.3, -0.3], "D7": [0.3, 0.1, -0.3, -0.1],
 "D9": [-0.2, 0.0, 0.2, 0.0], "D10": [0.5, 0.0, -0.2, -0.3],
}
central = {"D1": [2, 2, 1, 2], "D8": [3, 2, 2, None]}
d8q4 = {"HBS": 1, "IC": 2, "SS": 2}
rng = random.Random(2847)
baseline = OrderedDict()
for f in fam_list:
    scores = OrderedDict()
    for d in domains:
        did = d["id"]
        for i, q in enumerate(d["questions"]):
            if did in central:
                v = central[did][i]
                if v is None:
                    v = d8q4[f["bu"]]
            else:
                base = bu_base[f["bu"]][did] + fam_adj.get(f["id"], {}).get(did, 0.0) + q_offset[did][i]
                v = base + rng.uniform(-0.45, 0.45)
                v = int(math.floor(v + 0.5))
            scores[q["id"]] = max(0, min(4, v))
    baseline[f["id"]] = scores

TARGET = 3
def readiness(scores):
    vals = [min(s, TARGET) / TARGET for s in scores]
    return sum(vals) / len(vals)

domain_scores = OrderedDict(); fam_index = OrderedDict()
for f in fam_list:
    ds = OrderedDict()
    for d in domains:
        vals = [baseline[f["id"]][q["id"]] for q in d["questions"]]
        ds[d["id"]] = round(sum(vals) / len(vals), 2)
    domain_scores[f["id"]] = ds
    fam_index[f["id"]] = round(readiness(list(baseline[f["id"]].values())), 3)
portfolio_index = round(sum(fam_index.values()) / len(fam_index), 3)
domain_avg = OrderedDict((d["id"], round(sum(domain_scores[f["id"]][d["id"]] for f in fam_list) / len(fam_list), 2)) for d in domains)
domain_index = OrderedDict((d["id"], round(sum(readiness([baseline[f["id"]][q["id"]] for q in d["questions"]]) for f in fam_list) / len(fam_list), 3)) for d in domains)
q_avg = OrderedDict((qid, round(sum(baseline[f["id"]][qid] for f in fam_list) / len(fam_list), 2)) for qid in qids)
weakest = sorted(q_avg.items(), key=lambda kv: kv[1])[:10]
qtext = {q["id"]: q for d in domains for q in d["questions"]}
bu_index = OrderedDict((b["id"], round(sum(fam_index[f["id"]] for f in fam_list if f["bu"] == b["id"]) / sum(1 for f in fam_list if f["bu"] == b["id"]), 3)) for b in bus)
class_index = OrderedDict()
for k in ["Default", "Class I", "Class II"]:
    ids = [f["id"] for f in fam_list if (f["cra_class"].startswith("Default") if k == "Default" else f["cra_class"] == k)]
    class_index[k] = round(sum(fam_index[i] for i in ids) / len(ids), 3)

diagnostic = OrderedDict(
    name="CRA Readiness Diagnostic",
    scale=scale, target_level=TARGET,
    readiness_index_definition="Mean over questions of min(score, 3) / 3. Level 4 does not offset gaps elsewhere. 100% means every question at level 3 or above.",
    domains=domains,
    baseline_date=fmt_date(dt.date(2026, 10, 28)),
    baseline_label="Illustrative baseline — Example Group, self-assessed by product teams and moderated by the programme, 28 Oct 2026",
    baseline_scores=baseline, domain_scores=domain_scores, family_readiness_index=fam_index,
    portfolio_readiness_index=portfolio_index, domain_average_level=domain_avg, domain_readiness_index=domain_index,
    bu_readiness_index=bu_index, class_readiness_index=class_index,
    weakest_questions=[OrderedDict(id=k, avg=v, text=qtext[k]["text"], action=qtext[k]["action"]) for k, v in weakest],
    targets=OrderedDict(by_jun_2027=0.70, by_nov_2027=0.90, art14_domain_now=1.0),
)

# ---------------- Cost model ----------------
A = OrderedDict(
    fte_cost_programme=150_000, fte_cost_psirt=130_000, fte_cost_engineering=120_000,
    programme_team_fte=5, programme_team_run_fte=2.5,
    psirt_incremental_fte=2, psirt_oncall_allowance=60_000,
    remediation_fte_years=OrderedDict(default=1.2, class_i=2.5, class_ii=4.0),
    remediation_phasing=OrderedDict(q4_2026=0.15, y2027=0.85),
    platforms_build=850_000, platforms_phasing=OrderedDict(q4_2026=0.25, y2027=0.75), platforms_run=210_000,
    platforms_build_detail=OrderedDict(sbom_vex_csaf_tooling=220_000, signing_hsm_update_infrastructure=380_000, system_of_record=160_000, psirt_tooling_advisory_portal=90_000),
    risk_assessment_per_family=45_000, risk_assessment_phasing=OrderedDict(q4_2026=0.30, y2027=0.70),
    testing_per_family_per_year=OrderedDict(default=35_000, class_i=60_000, class_ii=90_000),
    documentation_per_family=40_000, documentation_run_per_family=8_000,
    nb_pre_assessments=OrderedDict(count=3, unit=20_000, q4_2026=20_000, y2027=40_000),
    nb_module_b_examinations=OrderedDict(count=3, unit=40_000, note="V1 two types, L2 one type"),
    nb_module_h=OrderedDict(initial=115_000, extra_categories=3, per_extra_category=20_000),
    nb_surveillance_run=OrderedDict(module_h=35_000, module_b_audits=20_000),
    training=OrderedDict(q4_2026=30_000, y2027=110_000, run=40_000),
    legal=OrderedDict(external_q4_2026=60_000, external_2027=120_000, translations_per_family=6_000, run=50_000),
    supplier_programme=OrderedDict(y2027=90_000, run=30_000),
    contingency_rate=0.15,
)
nfam = len(fam_list)
n_def = client["counts"]["default"]; n_i = client["counts"]["class_i"]; n_ii = client["counts"]["class_ii"]
rem_fte_years = n_def * A["remediation_fte_years"]["default"] + n_i * A["remediation_fte_years"]["class_i"] + n_ii * A["remediation_fte_years"]["class_ii"]
testing_year = n_def * A["testing_per_family_per_year"]["default"] + n_i * A["testing_per_family_per_year"]["class_i"] + n_ii * A["testing_per_family_per_year"]["class_ii"]

def build_lines(m):
    """m: scenario multipliers dict"""
    prog_fte = m.get("programme_team_fte", A["programme_team_fte"])
    lines = []
    def L(ws, line, driver, q4, y27, run):
        lines.append(OrderedDict(workstream=ws, line=line, driver=driver, q4_2026=round(q4), y2027=round(y27), run_2028=round(run)))
    L("Programme & governance", "Programme team (director, compliance lead, product security officer, PMO)",
      f"{prog_fte} FTE x EUR {A['fte_cost_programme']:,} loaded; run {A['programme_team_run_fte']} FTE",
      prog_fte * A["fte_cost_programme"] * 0.25, prog_fte * A["fte_cost_programme"], A["programme_team_run_fte"] * A["fte_cost_programme"])
    psirt = A["psirt_incremental_fte"] * A["fte_cost_psirt"] + A["psirt_oncall_allowance"]
    L("Reporting & PSIRT", "Incremental PSIRT (lead + analyst) and 24/7 on-call allowance",
      f"{A['psirt_incremental_fte']} FTE x EUR {A['fte_cost_psirt']:,} + EUR {A['psirt_oncall_allowance']:,} on-call", psirt * 0.25, psirt, psirt)
    rem = rem_fte_years * A["fte_cost_engineering"] * m.get("engineering", 1.0)
    L("Secure engineering", "Engineering remediation of Annex I gaps",
      f"{rem_fte_years:.1f} FTE-years (default 1.2, Class I 2.5, Class II 4.0 per family) x EUR {A['fte_cost_engineering']:,}" + (f" x {m.get('engineering')}" if m.get("engineering", 1.0) != 1.0 else ""),
      rem * A["remediation_phasing"]["q4_2026"], rem * A["remediation_phasing"]["y2027"], 0)
    L("Shared platforms", "SBOM/VEX/CSAF tooling, signing HSM and update infrastructure, system of record, PSIRT tooling",
      "EUR 850k build (25% Q4 2026, 75% 2027); EUR 210k a year run from mid-2027",
      A["platforms_build"] * A["platforms_phasing"]["q4_2026"], A["platforms_build"] * A["platforms_phasing"]["y2027"] + A["platforms_run"] * 0.5, A["platforms_run"])
    ra = nfam * A["risk_assessment_per_family"]
    L("Secure engineering", "Risk assessments and threat models", f"{nfam} families x EUR {A['risk_assessment_per_family']:,}", ra * 0.30, ra * 0.70, 0)
    t = testing_year * m.get("testing", 1.0)
    L("Secure engineering", "Security testing (penetration tests, fuzzing, re-tests)",
      "Per family per year: default EUR 35k, Class I EUR 60k, Class II EUR 90k" + (f" x {m.get('testing')}" if m.get("testing", 1.0) != 1.0 else ""), 0, t, t)
    L("Documentation & evidence", "Technical files and Annex II user information", f"{nfam} families x EUR {A['documentation_per_family']:,}; run EUR {A['documentation_run_per_family']:,} per family",
      0, nfam * A["documentation_per_family"], nfam * A["documentation_run_per_family"])
    nbm = m.get("notified_body", 1.0)
    nb27 = A["nb_pre_assessments"]["y2027"] + A["nb_module_b_examinations"]["count"] * A["nb_module_b_examinations"]["unit"] + A["nb_module_h"]["initial"] + A["nb_module_h"]["extra_categories"] * A["nb_module_h"]["per_extra_category"]
    L("Conformity & market access", "Notified bodies: pre-assessments, Module B examinations, Module H approval",
      "3 pre-assessments x EUR 20k; 3 Module B examinations x EUR 40k; Module H EUR 115k + 3 categories x EUR 20k (vendor estimates)" + (f" x {nbm}" if nbm != 1.0 else ""),
      A["nb_pre_assessments"]["q4_2026"] * nbm, nb27 * nbm, (A["nb_surveillance_run"]["module_h"] + A["nb_surveillance_run"]["module_b_audits"]) * nbm)
    L("People & change", "Training and awareness", "Role-based training, drills, e-learning", A["training"]["q4_2026"], A["training"]["y2027"], A["training"]["run"])
    lm = m.get("legal", 1.0)
    L("Conformity & market access", "Legal, EU representation and translations",
      "External legal EUR 180k; DoC/Annex II translations 13 x EUR 6k" + (f" x {lm}" if lm != 1.0 else ""),
      A["legal"]["external_q4_2026"] * lm, (A["legal"]["external_2027"] + nfam * A["legal"]["translations_per_family"]) * lm, A["legal"]["run"] * lm)
    L("Supply chain", "Supplier contract remediation and questionnaire programme", "41 in-scope suppliers", 0, A["supplier_programme"]["y2027"], A["supplier_programme"]["run"])
    return lines

def totals(lines, cont_rate):
    q4 = sum(l["q4_2026"] for l in lines); y27 = sum(l["y2027"] for l in lines); run = sum(l["run_2028"] for l in lines)
    cq4 = q4 * cont_rate; c27 = y27 * cont_rate
    return OrderedDict(q4_2026=round(q4), y2027=round(y27), contingency_q4_2026=round(cq4), contingency_2027=round(c27),
                       q4_2026_incl_contingency=round(q4 + cq4), y2027_incl_contingency=round(y27 + c27),
                       one_off_total_incl_contingency=round(q4 + y27 + cq4 + c27), run_2028=round(run), contingency_rate=cont_rate)

scen_defs = OrderedDict(
    low=OrderedDict(label="Low", description="Harmonised standards cited mid-2027; less remediation than assessed; fewer notified-body days.",
                    multipliers=OrderedDict(engineering=0.8, notified_body=0.6, testing=0.9), contingency=0.10),
    base=OrderedDict(label="Base", description="Plan as assessed at the 28 Oct 2026 baseline.", multipliers=OrderedDict(), contingency=0.15),
    high=OrderedDict(label="High", description="Notified-body scarcity forces a second body and premium fees; remediation 30% above estimate; extra programme FTE.",
                     multipliers=OrderedDict(engineering=1.3, notified_body=1.6, programme_team_fte=6, legal=1.5), contingency=0.20),
)
scenarios = OrderedDict()
for k, s in scen_defs.items():
    lines = build_lines(s["multipliers"])
    scenarios[k] = OrderedDict(label=s["label"], description=s["description"], multipliers=s["multipliers"], lines=lines, totals=totals(lines, s["contingency"]))
base_lines = scenarios["base"]["lines"]; base_tot = scenarios["base"]["totals"]
by_ws = OrderedDict()
for l in base_lines:
    w = by_ws.setdefault(l["workstream"], OrderedDict(q4_2026=0, y2027=0, run_2028=0))
    w["q4_2026"] += l["q4_2026"]; w["y2027"] += l["y2027"]; w["run_2028"] += l["run_2028"]
for w in by_ws.values():
    w["one_off"] = w["q4_2026"] + w["y2027"]

# monthly plan (base, incl. contingency) and actuals
months = ["Oct 2026", "Nov 2026", "Dec 2026"] + [dt.date(2027, i, 1).strftime("%b %Y") for i in range(1, 13)]
q4w = [0.27, 0.33, 0.40]
y27w = [0.055, 0.065, 0.075, 0.085, 0.09, 0.095, 0.095, 0.09, 0.09, 0.09, 0.09, 0.08]
s27 = sum(y27w); y27w = [w / s27 for w in y27w]
monthly_plan = [base_tot["q4_2026_incl_contingency"] * w for w in q4w] + [base_tot["y2027_incl_contingency"] * w for w in y27w]
cum = []; c = 0
for v in monthly_plan:
    c += v; cum.append(round(c))
actual_oct = 410_000
cost_model = OrderedDict(
    label="Illustrative business case — Example Group (EUR, real 2026 terms, excl. VAT)",
    assumptions=A, engineering_fte_years=rem_fte_years, testing_per_year=testing_year,
    base_lines=base_lines, base_totals=base_tot, by_workstream=by_ws, scenarios=scenarios,
    one_off_pct_of_revenue=round(base_tot["one_off_total_incl_contingency"] / (total_rev * 1e6), 4),
    run_pct_of_revenue=round(base_tot["run_2028"] / (total_rev * 1e6), 4),
    monthly_plan=[OrderedDict(month=mo, plan=round(p), cumulative_plan=cp) for mo, p, cp in zip(months, monthly_plan, cum)],
    actual_to_date=OrderedDict(month="Oct 2026", actual=actual_oct, plan=round(monthly_plan[0])),
    benchmarks=[
        OrderedDict(item="Module B examination", value="EUR 20,000-60,000", source="CRA Decoded (commentary); sota.io gives EUR 15,000-80,000 (vendor, unsourced)"),
        OrderedDict(item="First Module H engagement", value="EUR 80,000-150,000; surveillance every 1-2 years", source="CRA Decoded (commentary)"),
        OrderedDict(item="Three default products, medium readiness", value="EUR 78,300 one-off; EUR 13,500 a year", source="cyberresilienceact.eu cost calculator (independent model, illustrative)"),
        OrderedDict(item="Expected cost increase", value="50% of 12 companies expect <20% cost increase", source="KONE-authored industrial study, 2024 (survey)"),
        OrderedDict(item="CRA team size", value="28% up to 10 people; 22% larger; 16% up to 3", source="ONEKEY, Sep 2026, 200 German industrial firms (vendor survey)"),
    ],
)

# ---------------- Programme ----------------
workstreams = [
 OrderedDict(id="WS1", name="Governance & PMO", lead="Programme director", rag="Green", note="Sponsor named; programme board running; signing instrument drafted for board approval."),
 OrderedDict(id="WS2", name="Portfolio & classification", lead="Compliance lead", rag="Amber", note="11 of 13 families classified; EG-700 and HomeHub H3 need legal opinion (borderline Class I)."),
 OrderedDict(id="WS3", name="Reporting & PSIRT", lead="PSIRT lead", rag="Green", note="SRP live with 3 Assigned Representatives; first drill filed early warning in 9h 40m."),
 OrderedDict(id="WS4", name="Secure engineering & SDLC", lead="Product security officer", rag="Amber", note="T200 pilot risk assessment in review; release gate designed, not yet enforced."),
 OrderedDict(id="WS5", name="SBOM & supply chain", lead="Head of platform engineering", rag="Red", note="Signed SBOMs on 38% of releases; HBS firmware builds lack binary SCA; 6 of 41 suppliers on CRA clauses."),
 OrderedDict(id="WS6", name="Documentation & evidence", lead="Compliance lead", rag="Amber", note="System of record not yet selected; Annex VII outline agreed."),
 OrderedDict(id="WS7", name="Conformity & market access", lead="Head of quality & regulatory", rag="Red", note="No CRA notified body designated (external); 3 candidates shortlisted; V1/L2 route undecided."),
 OrderedDict(id="WS8", name="People & change", lead="Head of engineering enablement", rag="Amber", note="140 of 920 engineers trained; works council consultation on PSIRT on-call opened."),
]
phases = [
 OrderedDict(id="P0", name="Reporting readiness", start="1 Sep 2026", end="30 Oct 2026", status="Complete", gate="Early warning can be filed within 24 hours on a weekend"),
 OrderedDict(id="P1", name="Inventory, scope and classification", start="2 Nov 2026", end="18 Dec 2026", status="In progress", gate="Every product has a class, a route and an owner"),
 OrderedDict(id="P2", name="Risk assessment and gap analysis", start="1 Dec 2026", end="26 Feb 2027", status="Planned", gate="Applicability matrices signed for Wave 1"),
 OrderedDict(id="P3", name="Remediation and SDLC changes", start="4 Jan 2027", end="31 Aug 2027", status="Planned", gate="Pipeline evidence generated automatically for one release per family"),
 OrderedDict(id="P4", name="Documentation and declarations", start="1 Jun 2027", end="30 Sep 2027", status="Planned", gate="Technical files complete and reviewed outside engineering"),
 OrderedDict(id="P5", name="Conformity assessment", start="1 Apr 2027", end="30 Nov 2027", status="Planned", gate="Certificate or internal-control record in hand per family"),
 OrderedDict(id="P6", name="Go-live and operations", start="11 Dec 2027", end="ongoing", status="Planned", gate="Only declared products placed on the EU market"),
]
waves = [
 OrderedDict(id="W1", name="Wave 1", families=["T200", "V1", "L2", "IR500", "IS300", "SG900", "SLINK", "FLEET"], window="Nov 2026 - Nov 2027",
             rationale="All seven families that need a notified body, plus T200 as the pilot that produces the templates."),
 OrderedDict(id="W2", name="Wave 2", families=["SSR", "H3", "EG700", "CSTUDIO", "SDK"], window="Jan 2027 - Oct 2027",
             rationale="Default families on Module A, reusing Wave 1 templates; H3 and EG-700 move to Wave 1 if classified Class I."),
 OrderedDict(id="W3", name="Wave 3", families=["T100", "H2", "V0", "IR300", "IS200", "SL3", "FV4"], window="Continuous",
             rationale="Legacy lines: Art 14 reporting only, plus end-of-sale decisions for lines still sold in the EU."),
]
milestones = [
 OrderedDict(id="M0", name="SRP registration and coordinator CSIRT decision", date="10 Sep 2026", status="Complete"),
 OrderedDict(id="M1", name="First Art 14 tabletop drill (actively exploited vulnerability)", date="22 Oct 2026", status="Complete"),
 OrderedDict(id="M2", name="Programme mobilised; SteerCo #1", date="30 Oct 2026", status="Complete"),
 OrderedDict(id="M3", name="Board decisions (budget, signing authority, notified-body strategy, legacy lines)", date="19 Nov 2026", status="Planned"),
 OrderedDict(id="M4", name="Scope and classification register baselined", date="18 Dec 2026", status="On track"),
 OrderedDict(id="M5", name="Notified-body pre-assessments contracted (3 candidates)", date="29 Jan 2027", status="At risk"),
 OrderedDict(id="M6", name="Wave 1 risk assessments signed", date="26 Feb 2027", status="On track"),
 OrderedDict(id="M7", name="Formal notified-body engagements contracted (Module H; Module B+C)", date="31 Mar 2027", status="At risk"),
 OrderedDict(id="M8", name="SBOM pipeline live on all Wave 1 release trains", date="31 Mar 2027", status="At risk"),
 OrderedDict(id="M9", name="Second Art 14 drill (weekend severe-incident scenario)", date="16 Apr 2027", status="Planned"),
 OrderedDict(id="M10", name="Update infrastructure hardened (HSM signing, anti-rollback)", date="30 Jun 2027", status="Planned"),
 OrderedDict(id="M11", name="Wave 1 technical files complete", date="30 Sep 2027", status="Planned"),
 OrderedDict(id="M12", name="Module H approval and Module B certificates", date="30 Nov 2027", status="Planned"),
 OrderedDict(id="M13", name="Declarations signed; CE marking; Annex II published", date="3 Dec 2027", status="Planned"),
 OrderedDict(id="M14", name="Full application of the CRA", date="11 Dec 2027", status="Fixed"),
]
T = lambda tid, ws, task, owner, start, end, status, dep="": OrderedDict(id=tid, workstream=ws, task=task, owner=owner, start=start, end=end, status=status, depends_on=dep)
mobilisation_plan = [
 T("T01", "WS1", "Board paper and pre-read issued", "Programme director", "2 Nov 2026", "12 Nov 2026", "In progress"),
 T("T02", "WS1", "Board decisions on budget, signing authority, NB strategy, legacy lines", "Executive sponsor", "19 Nov 2026", "19 Nov 2026", "Not started", "T01"),
 T("T03", "WS1", "DoC signing instrument executed", "General Counsel", "20 Nov 2026", "4 Dec 2026", "Not started", "T02"),
 T("T04", "WS1", "Product-risk acceptance rule added to enterprise risk framework", "Chief Risk Officer", "2 Nov 2026", "11 Dec 2026", "In progress"),
 T("T05", "WS1", "System-of-record selection (criteria, shortlist, decision)", "Compliance lead", "2 Nov 2026", "18 Dec 2026", "In progress"),
 T("T06", "WS2", "Reconcile release, commercial and cloud inventories into the scope register", "Compliance lead", "2 Nov 2026", "4 Dec 2026", "In progress"),
 T("T07", "WS2", "Legal opinion on EG-700 and HomeHub H3 classification", "General Counsel", "2 Nov 2026", "27 Nov 2026", "In progress"),
 T("T08", "WS2", "Remote-function maps for all 13 families", "Product security officer", "9 Nov 2026", "11 Dec 2026", "Not started", "T06"),
 T("T09", "WS2", "Scope and classification register baselined", "Compliance lead", "14 Dec 2026", "18 Dec 2026", "Not started", "T06,T07,T08"),
 T("T10", "WS3", "Distribution map per product refreshed for SRP 'Member States' field", "Product management", "2 Nov 2026", "20 Nov 2026", "In progress"),
 T("T11", "WS3", "Works council agreement on 24/7 PSIRT on-call", "HR business partner", "2 Nov 2026", "18 Dec 2026", "In progress"),
 T("T12", "WS3", "PSIRT lead hired; analyst seconded from IC", "PSIRT lead", "2 Nov 2026", "29 Jan 2027", "In progress"),
 T("T13", "WS3", "HBS and S&S security.txt and CVD policy published", "PSIRT lead", "9 Nov 2026", "4 Dec 2026", "Not started"),
 T("T14", "WS3", "Legacy reportable inventory completed (T100, H2, V0 fleets)", "PSIRT lead", "2 Nov 2026", "11 Dec 2026", "In progress"),
 T("T15", "WS4", "T200 pilot risk assessment signed (applicability matrix)", "Product security officer", "2 Nov 2026", "27 Nov 2026", "In progress"),
 T("T16", "WS4", "Release security gate enforced on T200 and IR-500 trains", "Product security officer", "16 Nov 2026", "22 Jan 2027", "Not started", "T15"),
 T("T17", "WS4", "Wave 1 threat-modelling sprints (7 families)", "Product security officer", "30 Nov 2026", "26 Feb 2027", "Not started", "T15"),
 T("T18", "WS5", "SBOM generation from artefact on HBS firmware builds (Yocto + binary SCA)", "Head of platform engineering", "2 Nov 2026", "15 Jan 2027", "In progress"),
 T("T19", "WS5", "Dependency-Track and EUVD watch for all supported versions", "Head of platform engineering", "9 Nov 2026", "18 Dec 2026", "Not started"),
 T("T20", "WS5", "CRA clause pack issued to top 15 security-relevant suppliers", "Head of procurement", "16 Nov 2026", "29 Jan 2027", "Not started"),
 T("T21", "WS5", "Supplier questionnaire sent to all 41 in-scope suppliers", "Head of procurement", "23 Nov 2026", "18 Dec 2026", "Not started"),
 T("T22", "WS6", "Annex VII 13-part file template and evidence index adopted", "Compliance lead", "2 Nov 2026", "4 Dec 2026", "In progress"),
 T("T23", "WS6", "Annex II user-information template drafted (T200 first)", "Technical writing lead", "16 Nov 2026", "18 Dec 2026", "Not started"),
 T("T24", "WS7", "Pre-assessment proposals from 3 candidate notified bodies", "Head of quality & regulatory", "2 Nov 2026", "11 Dec 2026", "In progress"),
 T("T25", "WS7", "Pre-assessment contracts signed with conversion options", "Head of quality & regulatory", "14 Dec 2026", "29 Jan 2027", "Not started", "T02,T24"),
 T("T26", "WS7", "Module H scope statement for IC + FleetView quality system", "Head of quality & regulatory", "16 Nov 2026", "22 Jan 2027", "Not started"),
 T("T27", "WS7", "Withdraw-or-remediate plan for IR-300 and IS-200 EU sales", "BU president IC", "20 Nov 2026", "18 Dec 2026", "Not started", "T02"),
 T("T28", "WS8", "Engineering awareness training to 400 engineers", "Head of engineering enablement", "2 Nov 2026", "29 Jan 2027", "In progress"),
 T("T29", "WS8", "Sales and support briefing and customer FAQ live", "Head of customer operations", "16 Nov 2026", "11 Dec 2026", "Not started"),
 T("T30", "WS8", "Staff awareness pulse survey #1", "Head of engineering enablement", "23 Nov 2026", "4 Dec 2026", "Not started"),
]

kpis = [
 OrderedDict(id="K01", name="Portfolio readiness index", value=portfolio_index, display=f"{portfolio_index*100:.0f}%", target="70% by Jun 2027; 90% by Nov 2027", rag="Amber", trend="Baseline", source="Readiness diagnostic, 28 Oct 2026"),
 OrderedDict(id="K02", name="Families with final scope and class decision", value=11, display="11 / 13", target="13 / 13 by 18 Dec 2026", rag="Amber", trend="New", source="Scope register"),
 OrderedDict(id="K03", name="Class I/II families with route and notified-body plan", value=5, display="5 / 7", target="7 / 7 by 19 Nov 2026", rag="Amber", trend="New", source="Scope register"),
 OrderedDict(id="K04", name="SRP Assigned Representatives registered", value=3, display="3", target=">= 2 at all times", rag="Green", trend="Stable", source="SRP roster"),
 OrderedDict(id="K05", name="Art 14 drill: time to early warning", value=9.67, display="9h 40m", target="< 24h incl. weekends", rag="Green", trend="First drill", source="Drill record 22 Oct 2026"),
 OrderedDict(id="K06", name="Art 14 cases assessed (reportable / not reportable)", value=4, display="0 / 4", target="100% decided with UTC timeline", rag="Green", trend="Stable", source="PSIRT case files"),
 OrderedDict(id="K07", name="Releases with signed SBOM (last 30 days)", value=0.38, display="38% (9 / 24)", target="100% by 31 Mar 2027", rag="Red", trend="Up from 21%", source="Build pipeline"),
 OrderedDict(id="K08", name="Families with signed risk assessment", value=0, display="0 / 13 (T200 in review)", target="Wave 1 (8) by 26 Feb 2027", rag="Green", trend="On plan", source="System of record"),
 OrderedDict(id="K09", name="In-scope suppliers on CRA clauses", value=6, display="6 / 41 (15%)", target="Top 15 by Jan 2027; all by Jun 2027", rag="Amber", trend="New", source="Contract register"),
 OrderedDict(id="K10", name="Engineers trained", value=140, display="140 / 920 (15%)", target="60% by Mar 2027", rag="Amber", trend="Up", source="LMS"),
 OrderedDict(id="K11", name="Spend to date vs plan", value=actual_oct, display=f"EUR {actual_oct/1e6:.2f}m vs EUR {monthly_plan[0]/1e6:.2f}m", target="Within +/-10% of plan", rag="Green", trend="Oct 2026", source="Finance"),
 OrderedDict(id="K12", name="Notified-body candidates", value=3, display="3 shortlisted; 1 proposal", target="3 pre-assessments contracted by 29 Jan 2027", rag="Amber", trend="New", source="Programme"),
]
plan_readiness = OrderedDict([("Oct 2026", 0.40), ("Nov 2026", 0.42), ("Dec 2026", 0.45), ("Jan 2027", 0.49), ("Feb 2027", 0.54), ("Mar 2027", 0.59),
                              ("Apr 2027", 0.63), ("May 2027", 0.67), ("Jun 2027", 0.71), ("Jul 2027", 0.75), ("Aug 2027", 0.79), ("Sep 2027", 0.84),
                              ("Oct 2027", 0.88), ("Nov 2027", 0.91), ("Dec 2027", 0.93)])
_mon = list(plan_readiness.keys())
_w = [0, 0.03, 0.08, 0.14, 0.21, 0.29, 0.37, 0.45, 0.54, 0.62, 0.70, 0.79, 0.87, 0.95, 1.0]
_end = 0.93
plan_readiness = OrderedDict((mo, round(portfolio_index + (_end - portfolio_index) * w, 3)) for mo, w in zip(_mon, _w))
plan_sbom = OrderedDict([("Sep 2026", 0.21), ("Oct 2026", 0.38), ("Nov 2026", 0.45), ("Dec 2026", 0.55), ("Jan 2027", 0.70), ("Feb 2027", 0.85), ("Mar 2027", 1.0)])
kpi_trajectories = OrderedDict(readiness_index_plan=plan_readiness, sbom_coverage_plan_and_actual=plan_sbom,
                               note="Oct 2026 values are actuals (illustrative); later months are plan. SBOM Sep 2026 is the pre-programme measurement.")

R = lambda rid, title, desc, L, I, owner, mitig, trend: OrderedDict(id=rid, title=title, description=desc, likelihood=L, impact=I, score=L*I,
        rating=("High" if L*I >= 12 else "Medium" if L*I >= 6 else "Low"), owner=owner, mitigations=mitig, trend=trend)
risks = [
 R("R01", "No notified-body capacity in time", "No CRA notified body is designated with capacity before Q2 2027, so Class I/II families cannot be certified by 11 Dec 2027.", 4, 5, "Head of quality & regulatory",
   "Pre-contract three candidates with conversion options; Module H for IC to cover five families with one body; check NANDO at every programme board; prioritise top-revenue SKUs.", "Rising"),
 R("R02", "Engineering capacity", "Remediation competes with the 2027 product roadmap for the same engineers.", 4, 4, "CTO",
   "Ring-fence 26 FTE-years in the 2027 plan; defer two roadmap features; contractors for documentation and testing.", "Stable"),
 R("R03", "No harmonised standard cited for Class I", "EN 304 6xx verticals are not cited in time, so Class I products cannot use Module A.", 4, 3, "Compliance lead",
   "Plan Class I on third-party routes; align files to draft clause structure; switch to Module A only if a citation lands before assessment.", "Stable"),
 R("R04", "SBOM and supplier transparency gaps", "Binary blobs and supplier components without SBOMs or vulnerability notification undermine Annex I Part II(1) and the 24-hour determination.", 3, 4, "Head of platform engineering",
   "Binary SCA on firmware images; clause pack to top 15 suppliers first; exit plans for refusers.", "Stable"),
 R("R05", "Legacy lines still sold after 11 Dec 2027", "IR-300 and IS-200 units placed after 11 Dec 2027 must comply with Annex I.", 3, 4, "BU president IC",
   "Board decision on 19 Nov 2026 to withdraw from EU sale and migrate customers; remediate only if the decision changes.", "New"),
 R("R06", "Late or wrong Art 14 filing", "Awareness misjudged or a stale distribution map delays the 24-hour early warning.", 2, 5, "PSIRT lead",
   "Written awareness criteria; deputies with authority to file; distribution map refresh (T10); two drills a year.", "Falling"),
 R("R07", "Scope undercount", "Versions, companion apps and backends found late enlarge the portfolio.", 3, 3, "Compliance lead",
   "Build the register from release and cloud systems; second reconciliation after the first gate run.", "Stable"),
 R("R08", "Key-person dependency in PSIRT", "Two people hold most PSIRT knowledge; on-call cannot be sustained.", 3, 3, "PSIRT lead",
   "Hire PSIRT lead; second analyst; documented runbook; cross-training from IC.", "Stable"),
 R("R09", "Guidance changes", "Formal adoption of C(2026) 5252 or later FAQ versions change scope or support-period decisions.", 3, 2, "Compliance lead",
   "Decision records cite the guidance version; quarterly standards and guidance review.", "Stable"),
 R("R10", "Product-liability disclosure", "From 9 Dec 2026 claimants can seek disclosure of technical files and update logs under the PLD.", 2, 4, "General Counsel",
   "Write records for disclosure; legal review of risk acceptances; align with product liability insurance.", "New"),
]
issues = [
 OrderedDict(id="I01", title="Distribution map stale", description="The 22 Oct drill showed the 'Member States where available' field could not be completed for two products from current data.", owner="Product management", due="20 Nov 2026"),
 OrderedDict(id="I02", title="Borderline classifications", description="EG-700 (cellular uplink routing) and HomeHub H3 (optional alarm mode) could be Class I; notified-body capacity planning includes them until the legal opinion lands.", owner="General Counsel", due="27 Nov 2026"),
 OrderedDict(id="I03", title="HBS firmware SBOM depth", description="Manifest-only SBOMs on HBS firmware miss vendored code; binary SCA needed.", owner="Head of platform engineering", due="15 Jan 2027"),
]
decisions = OrderedDict(
 steerco_1=[
  OrderedDict(id="SD1", decision="Endorse Module H as the route for Industrial Connectivity and FleetView (five families), using the IEC 62443-4-1 process as the base.", outcome="Endorsed (illustrative)"),
  OrderedDict(id="SD2", decision="Apply the stricter reading to EG-700 and HomeHub H3 until the legal opinion lands on 27 Nov 2026: include them in notified-body capacity planning, keep them in Wave 2 for remediation.", outcome="Endorsed (illustrative)"),
  OrderedDict(id="SD3", decision="Release EUR 0.75m of pre-approval spend ahead of the 19 Nov board.", outcome="Endorsed (illustrative)"),
  OrderedDict(id="SD4", decision="Approve system-of-record selection criteria.", outcome="Endorsed (illustrative)"),
 ],
 board=[
  OrderedDict(id="BD1", decision="Approve the Project Rampart investment envelope.", detail=f"EUR {base_tot['one_off_total_incl_contingency']/1e6:.1f}m one-off to Dec 2027 (incl. 15% contingency) and EUR {base_tot['run_2028']/1e6:.1f}m a year run from 2028."),
  OrderedDict(id="BD2", decision="Appoint the accountable executive and execute the DoC signing instrument.", detail="CTO as accountable executive; CEO signs declarations or delegates in writing; compliance lead counter-signs the pre-signature checklist."),
  OrderedDict(id="BD3", decision="Authorise notified-body pre-contracting.", detail="Pre-assessments with three candidate bodies (up to EUR 60k) and formal contracts by Q1 2027 (Module H for IC + FleetView; Module B+C for V1 and L2)."),
  OrderedDict(id="BD4", decision="Adopt the product-risk acceptance rule.", detail="Cost, risk appetite and commercial strategy are not grounds to leave product risk unaddressed (guidance paras 156-163); appeals go to the executive sponsor."),
  OrderedDict(id="BD5", decision="Withdraw IR-300 and IS-200 from EU sale before 11 Dec 2027.", detail="EUR 18m of declining EU revenue versus about EUR 1.4m remediation plus notified-body fees; migrate customers to IR-500 and IS-300."),
 ],
)

S = lambda sid, name, group, power, interest, stance_now, stance_target, concern, message, channel, owner, freq: OrderedDict(id=sid, name=name, group=group, power=power, interest=interest,
      stance_now=stance_now, stance_target=stance_target, key_concern=concern, key_message=message, channel=channel, owner=owner, frequency=freq)
stakeholders = [
 S("ST01", "Board of directors", "Internal - governance", 5, 3, "Aware", "Committed", "Liability, fines, market access, cost", "A funded 14-month programme protects __EUNB__ of EU revenue; five decisions now.", "Board paper and briefing", "Executive sponsor", "Quarterly"),
 S("ST02", "CEO and executive committee", "Internal - governance", 5, 4, "Supportive", "Committed", "Revenue at risk, roadmap impact", "Reporting is live; market access is the constraint; build once, apply per product.", "ExCo agenda item; monthly dashboard", "Executive sponsor", "Monthly"),
 S("ST03", "CTO (accountable executive)", "Internal - leadership", 5, 5, "Committed", "Leading", "Engineering capacity, release gates", "You own the release gate and the evidence; the programme gives you shared tooling.", "SteerCo; 1:1", "Programme director", "Fortnightly"),
 S("ST04", "General Counsel", "Internal - leadership", 4, 4, "Supportive", "Committed", "DoC liability, PLD disclosure, classification calls", "Decision records and the signing instrument limit personal and corporate exposure.", "SteerCo; legal working group", "Compliance lead", "Fortnightly"),
 S("ST05", "CISO", "Internal - leadership", 4, 5, "Committed", "Leading", "PSIRT vs CSIRT split, NIS2/GDPR overlap", "Product PSIRT is separate from the infrastructure CSIRT; one coordination cell for multi-regime incidents.", "SteerCo; incident cell", "PSIRT lead", "Weekly"),
 S("ST06", "BU presidents (HBS, IC, S&S)", "Internal - leadership", 5, 4, "Mixed", "Committed", "Margin, roadmap, legacy lines", "Your EU revenue depends on notified-body slots we must book now.", "BU reviews; SteerCo", "Executive sponsor", "Monthly"),
 S("ST07", "Engineering leads and developers", "Internal - delivery", 3, 4, "Unaware to aware", "Practising", "Extra process, release friction", "Evidence comes from the pipeline, not from paperwork; the gate checks what you already test.", "Engineering all-hands; training; Slack", "Product security officer", "Fortnightly"),
 S("ST08", "Product management", "Internal - delivery", 3, 4, "Aware", "Committed", "Support periods, roadmap trade-offs", "Support period and Annex II content are product decisions with legal weight.", "PM forum; briefing pack", "Compliance lead", "Monthly"),
 S("ST09", "PSIRT and on-call staff", "Internal - delivery", 2, 5, "Committed", "Committed", "Workload, 24/7 on-call, authority to file", "You may file an early warning without prior approval; legal reviews the 72-hour report.", "Runbook; drills", "PSIRT lead", "Weekly"),
 S("ST10", "Quality & regulatory (CE/RED team)", "Internal - delivery", 3, 5, "Supportive", "Leading", "Notified-body capacity, RED transition", "Your CE experience runs conformity; RED delegated act ends 11 Dec 2027.", "Workstream meetings", "Programme director", "Weekly"),
 S("ST11", "Procurement", "Internal - enabling", 3, 3, "Aware", "Committed", "Supplier pushback, contract renegotiation", "Clause pack and questionnaire; refusals go to the intake gate as high risk.", "Procurement council", "Head of procurement", "Monthly"),
 S("ST12", "Sales, key accounts and customer support", "Internal - enabling", 2, 3, "Unaware", "Informed", "Customer questions, competitive positioning", "Say what we do, not 'CRA certified'; use the FAQ; route vulnerability reports to PSIRT within the hour.", "Briefing; FAQ; LMS module", "Head of customer operations", "At launch, then quarterly"),
 S("ST13", "Works council", "Internal - employee representation", 4, 3, "Neutral", "Supportive", "On-call arrangements, training time, monitoring", "On-call is voluntary-rota based with allowances; training is in working time.", "Formal consultation", "HR business partner", "As required"),
 S("ST14", "All employees", "Internal - wider", 1, 2, "Unaware", "Informed", "What it means for me", "Security is now part of what we sell; know where to report a vulnerability.", "Intranet; town hall", "Internal communications", "Quarterly"),
 S("ST15", "B2B customers and integrators", "External - market", 4, 4, "Asking", "Confident", "Supply-chain evidence for their own NIS2/CRA duties", "Support periods, CVD contact, SBOM on request and declarations on a published timetable.", "Account letters; customer FAQ; trust page", "Head of customer operations", "Quarterly"),
 S("ST16", "Consumers (via retail and app)", "External - market", 2, 2, "Unaware", "Informed", "Updates, privacy, support length", "Automatic security updates by default and a clear support end date at purchase.", "Product pages; app notices", "Marketing", "At launch"),
 S("ST17", "Distributors, importers and retail partners", "External - channel", 3, 3, "Asking", "Confident", "Their Art 19-20 checks, labelling, stock after 11 Dec 2027", "We will supply DoCs, Annex II information and CE marking per product before 11 Dec 2027.", "Channel letter; partner portal", "Head of channel", "Quarterly"),
 S("ST18", "Suppliers (chipsets, modules, ODMs, software)", "External - supply chain", 3, 3, "Mixed", "Cooperative", "Contract changes, SBOM effort", "We need vulnerability notification, SBOMs and support commitments; here is the clause pack.", "Supplier letter; questionnaire", "Head of procurement", "Quarterly"),
 S("ST19", "Notified bodies (candidates)", "External - assurance", 5, 3, "Engaged", "Contracted", "Capacity, designation timing", "We are assessment-ready early and want a slot with conversion options.", "Pre-assessment meetings", "Head of quality & regulatory", "Monthly"),
 S("ST20", "Coordinator CSIRT and market surveillance (Germany)", "External - regulator", 5, 3, "Neutral", "Trusting", "Timely, accurate reporting", "We report on time with complete data and answer reasoned requests within 10 working days.", "SRP; formal correspondence", "PSIRT lead / Compliance lead", "As required"),
 S("ST21", "Open-source communities and maintainers", "External - ecosystem", 2, 3, "Neutral", "Collaborative", "Burden shifted to unpaid maintainers", "We report upstream through your CVD channel and share fixes; we do not demand compliance from you.", "OSPO; upstream channels", "OSPO lead", "As required"),
 S("ST22", "Insurers (product liability, cyber)", "External - finance", 3, 2, "Unaware", "Informed", "PLD exposure from 9 Dec 2026", "Our evidence system lowers defect and disclosure risk.", "Broker briefing", "CFO office", "At renewal"),
]

facts = [
 ("F01", "The CRA is Regulation (EU) 2024/2847; it entered into force on 10 Dec 2024.", "Art 71; EUR-Lex", "https://eur-lex.europa.eu/eli/reg/2024/2847/oj"),
 ("F02", "Article 14 reporting applies from 11 Sep 2026 to all in-scope products, including those placed on the market before 11 Dec 2027.", "Art 71(2); Art 69(3)", "https://eur-lex.europa.eu/eli/reg/2024/2847/oj"),
 ("F03", "Chapter IV (notification of conformity assessment bodies) applies from 11 Jun 2026; all other provisions from 11 Dec 2027.", "Art 71(2)", "https://eur-lex.europa.eu/eli/reg/2024/2847/oj"),
 ("F04", "Reporting clocks: actively exploited vulnerability 24h early warning, 72h notification, final report 14 days after a corrective measure is available; severe incident 24h, 72h, final report 1 month after the 72h notification.", "Art 14(2), (4)", "https://eur-lex.europa.eu/eli/reg/2024/2847/oj"),
 ("F05", "Reports go through ENISA's Single Reporting Platform to the coordinator CSIRT of the main-establishment Member State; the platform has been live since 11 Sep 2026 (web form, English only, no API).", "Art 14(7); ENISA", "https://www.enisa.europa.eu/topics/product-security/single-reporting-platform-srp"),
 ("F06", "Fines: up to EUR 15m or 2.5% of worldwide annual turnover (Annex I, Arts 13-14); EUR 10m or 2% (other obligations); EUR 5m or 1% (misleading information), whichever is higher.", "Art 64(2)-(4)", "https://eur-lex.europa.eu/eli/reg/2024/2847/oj"),
 ("F07", "No harmonised standard is cited in the OJ and no common specification is adopted (30 Oct 2026); Class I products cannot use Module A until one is cited and applied in full.", "Art 32(2); guidance para 149", "https://digital-strategy.ec.europa.eu/en/factpages/cyber-resilience-act-implementation"),
 ("F08", "No CRA notified body was verifiably designated in NANDO at checks to 8 Sep 2026; Member States must 'strive' for enough bodies by 11 Dec 2026.", "Art 35(2); Commission", "https://digital-strategy.ec.europa.eu/en/policies/cra-conformity-assessment"),
 ("F09", "Annexes III and IV list 19 Class I, 4 Class II and 3 critical categories (26 in total); Implementing Regulation (EU) 2025/2392 gives their technical descriptions (in force 21 Dec 2025).", "Art 7; Art 8", "https://eur-lex.europa.eu/eli/reg_impl/2025/2392/oj/eng"),
 ("F10", "Commission guidance C(2026) 5252 (content approved 27 Jul 2026) is non-binding and formally pending adoption in all languages; FAQ v1.4 is dated 4 Sep 2026.", "Art 26", "https://ec.europa.eu/newsroom/dae/redirection/document/131456"),
 ("F11", "Support period must reflect expected time in use and be at least five years unless the product is expected to be used for less; security updates stay available for at least 10 years or the rest of the support period.", "Art 13(8)-(9)", "https://eur-lex.europa.eu/eli/reg/2024/2847/oj"),
 ("F12", "Technical documentation and the declaration are kept for 10 years after placing on the market or the support period, whichever is longer.", "Art 13(13)", "https://eur-lex.europa.eu/eli/reg/2024/2847/oj"),
 ("F13", "The SBOM is part of the technical documentation; manufacturers are not obliged to make it public.", "Annex I Part II(1); Annex VII; Recital 77", "https://eur-lex.europa.eu/eli/reg/2024/2847/oj"),
 ("F14", "Manufacturer-built backends a product needs for a function are remote data processing and part of the product.", "Art 3(2); guidance paras 184-205", "https://ec.europa.eu/newsroom/dae/redirection/document/131456"),
 ("F15", "The Product Liability Directive (EU) 2024/2853 applies from 9 Dec 2026; software is a product and a vulnerability can be a defect.", "PLD Arts 4, 7, 9-10", "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024L2853"),
 ("F16", "National enforcement acts adopted by 30 Oct 2026: Finland (Act 439/2026), Hungary (Act CXXXV/2025), Malta (LN 238/2026); Germany's law passed the Bundestag plenary on 15 Oct 2026, promulgation pending. France has named ANSSI as notifying authority.", "KB: Enforcement", ""),
 ("F17", "The Digital Omnibus COM(2025) 837 does not amend the CRA; Council mandate agreed 21 Oct 2026 (ST 14756/26); not adopted.", "KB: Interplay", "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:52025PC0837"),
 ("F18", "RED cybersecurity delegated act 2022/30 is repealed with effect from 11 Dec 2027 by Delegated Regulation (EU) 2026/339.", "KB: Interplay", "https://eur-lex.europa.eu/eli/reg_del/2026/339/oj/eng"),
 ("F19", "EUCC: 111 valid certificates from 9 certification bodies on 30 Oct 2026; the Art 27(9) act that would let EUCC replace third-party assessment is planned, not adopted.", "KB: Standards; verification", ""),
 ("F20", "Open-source stewards have a light-touch regime (Art 24) and are exempt from fines (Art 64(10)(b)); integrating FOSS never transfers the manufacturer's duty (Art 13(5)).", "Arts 13(5), 24, 64(10)", "https://eur-lex.europa.eu/eli/reg/2024/2847/oj"),
]
facts = [OrderedDict(id=a, statement=b, basis=c, url=d) for a, b, c, d in facts]

research_datapoints = [
 OrderedDict(id="RD01", stat="German companies that know what the CRA means for them", value="29%", detail="67% have heard of it; 38% cannot assess it; 28% unaware", sample="1,003 German companies with 10+ employees", date="Apr-Jun 2026", source="Bitkom Research via IT Finanzmagazin, 11 Sep 2026", type="Survey", url="https://www.it-finanzmagazin.de/cyber-resilience-act-cra-nur-jedes-dritte-unternehmen-vorbereitet-250594/"),
 OrderedDict(id="RD02", stat="CRA-aware respondents unaware of CRA penalties", value="56%", detail="Only 34% identify 2027 as the compliance year; 66% of all 843 respondents are not or only slightly familiar with the CRA", sample="404 CRA-aware respondents (of 843 surveyed)", date="early 2026", source="Linux Foundation Research, CRA awareness report 2026", type="Survey", url="https://www.linuxfoundation.org/hubfs/Research%20Reports/lfr_2026_cra_awareness_report_060826.pdf?hsLang=en"),
 OrderedDict(id="RD03", stat="Manufacturers relying passively on upstream projects for security fixes", value="51%", detail="Separately, LF's 2025 Open Source ROI survey (n=236), cited in the 2026 report, found an average of 86 private forks per organisation at about 60 hours each per release cycle", sample="Manufacturer module (n=194-219) of the 843-respondent survey", date="early 2026", source="Linux Foundation Research 2026", type="Survey", url="https://www.linuxfoundation.org/hubfs/Research%20Reports/lfr_2026_cra_awareness_report_060826.pdf?hsLang=en"),
 OrderedDict(id="RD04", stat="SME manufacturers planning to raise prices to cover compliance", value="47%", detail="Stewards' top support needs in 2026: financial support 50%, legal guidance 39% (n=28); the 2025 legal-guidance figure was 47% (n=34)", sample="54 SME manufacturers", date="early 2026", source="Linux Foundation Research 2026", type="Survey (small subsample)", url="https://www.linuxfoundation.org/hubfs/Research%20Reports/lfr_2026_cra_awareness_report_060826.pdf?hsLang=en"),
 OrderedDict(id="RD05", stat="SMEs asking for technical documentation templates", value="73%", detail="13% rate their understanding of documentation requirements as good", sample="194 responses, not representative", date="Jun 2026 report", source="ENISA SME CRA survey", type="Survey (official)", url="https://www.enisa.europa.eu/sites/default/files/2026-06/SME%20CRA%20survey%20report.pdf"),
 OrderedDict(id="RD06", stat="Firms expecting longer product development under the CRA", value=">60%", detail="28% 'significantly longer'; 28% have CRA teams of up to 10 people, 22% larger, 16% up to 3", sample="200 German industrial firms", date="Sep 2026", source="ONEKEY IoT/OT Cybersecurity Report 2026", type="Vendor survey", url="https://www.onekey.com/press-release/onkey-iot-ot-cybersecurity-report-2026-half-of-all-companies-have-formed-cra-teams"),
 OrderedDict(id="RD07", stat="Respondents with partly or fully automated SBOM generation", value="74%", detail="Completeness is the top challenge (62%); 44% CycloneDX, 29% SPDX; 39% generate at build", sample="334 responses", date="Jun 2026", source="ENISA SBOM Adoption State of Play 2026", type="Survey (official)", url="https://www.enisa.europa.eu/sites/default/files/2026-06/SBOM%20Adoption%20State%20of%20Play%202026.pdf"),
 OrderedDict(id="RD08", stat="Companies expecting cost increase under 20%", value="50%", detail="25% expect 20-40%; 25% no impact", sample="12 companies", date="2024", source="KONE-authored industrial study (arXiv 2505.14325)", type="Survey (small sample)", url="https://arxiv.org/pdf/2505.14325"),
 OrderedDict(id="RD09", stat="Illustrative cost for three default products at medium readiness", value="EUR 78,300 one-off; EUR 13,500 a year", detail="At EUR 45 per hour; 'illustrative and intended for planning only'", sample="Model", date="2026", source="cyberresilienceact.eu cost calculator", type="Independent model", url="https://www.cyberresilienceact.eu/cra-compliance-cost-calculator/"),
 OrderedDict(id="RD10", stat="CRA notified bodies verifiably designated", value="0", detail="Checks to 8 Sep 2026; Brightsight (RvA accreditation, pending Dutch notification) and Applus+ in the pipeline per vendor statements", sample="NANDO / Single Market Compliance Space", date="8 Sep 2026", source="European Commission; vendor statements", type="Official + vendor", url="https://digital-strategy.ec.europa.eu/en/policies/cra-conformity-assessment"),
 OrderedDict(id="RD11", stat="Valid EUCC certificates", value="111 from 9 certification bodies", detail="EUCC is the only adopted EU cybersecurity certification scheme", sample="ENISA register", date="30 Oct 2026", source="ENISA EUCC register (fact-checked)", type="Official", url=""),
 OrderedDict(id="RD12", stat="Time to designate a notified body", value="12-18 months", detail="2-4 months to contract; 3-6 months per Module B+C engagement", sample="Commentary", date="2026", source="CRA Decoded", type="Commentary (unverified)", url="https://cra-decoded.com/blog/posts/cra-notified-body-capacity-crisis/"),
]

data = OrderedDict(meta=meta, brand=brand, storyline=storyline, client=client, exposure=exposure, diagnostic=diagnostic,
    cost_model=cost_model, programme=OrderedDict(name="Project Rampart", kickoff="5 Oct 2026", phases=phases, waves=waves, milestones=milestones,
    workstreams=workstreams, mobilisation_plan=mobilisation_plan, overall_rag="Amber",
    overall_status="Reporting capability on track; market access at risk because no notified body is designated (external dependency)."),
    kpis=kpis, kpi_trajectories=kpi_trajectories, risks=risks, issues=issues, decisions=decisions, stakeholders=stakeholders,
    facts=facts, research_datapoints=research_datapoints)

_eunb = f"EUR {eu_nb:.0f}m"
_oneoff = f"EUR {base_tot['one_off_total_incl_contingency']/1e6:.1f}m"
_run = f"EUR {base_tot['run_2028']/1e6:.1f}m"
def _fill(o):
    if isinstance(o, dict):
        return OrderedDict((k, _fill(v)) for k, v in o.items())
    if isinstance(o, list):
        return [_fill(v) for v in o]
    if isinstance(o, str):
        return o.replace("__EUNB__", _eunb).replace("__ONEOFF__", _oneoff).replace("__RUN__", _run)
    return o
data = _fill(data)
storyline = data["storyline"]
with open(OUT_JSON, "w") as fh:
    json.dump(data, fh, indent=1, ensure_ascii=False)

# ---------------- Markdown summary ----------------
def eur(x):
    return f"EUR {x/1e6:.2f}m" if abs(x) >= 1e6 else f"EUR {x/1e3:.0f}k"
md = []
md.append(f"# DATA SUMMARY — {meta['pack_name']} (v{meta['version']}, {meta['issue_date']})\n")
md.append(f"> {meta['classification_label']}. Source of truth: `pack/data/pack_data.json`. Never invent client numbers — use these.\n")
md.append("## Key numbers (use exactly)\n")
md.append(f"- Days from pack issue ({meta['issue_date']}) to full application (11 Dec 2027): **{meta['days_to_full_application_from_issue']}**; from board ({meta['board_meeting']}): **{meta['days_to_full_application_from_board']}**")
md.append(f"- Client: {client['name']} (fictional), HQ {client['hq']}; revenue EUR {total_rev}m; EU revenue EUR {eu_total}m ({client['eu_share']*100:.0f}%); {client['employees']:,} employees; {client['engineers']} engineers; {client['counts']['families']} product families / {client['counts']['skus']} SKUs in scope; {client['counts']['legacy_lines']} legacy lines; ~{client['installed_base_m']}m connected devices in the field")
md.append(f"- Classes: {client['counts']['default']} default (incl. {client['counts']['provisional']} provisional/borderline), {client['counts']['class_i']} Class I, {client['counts']['class_ii']} Class II, 0 critical")
md.append(f"- Revenue by class (EUR m): {dict(rev_by_class)}; EU revenue by class: {dict(eu_by_class)}")
md.append(f"- **EU revenue from the 13 in-scope product families: EUR {client['eu_revenue_in_scope_products_m']}m (show as EUR 807m)**. Total EU revenue EUR {eu_total}m also includes EUR {client['eu_revenue_saas_not_a_product_m']}m of EU SaaS revenue (the cloud platform is not itself a product; it is remote data processing for some products). Never call EUR 824m 'in scope'.")
md.append(f"- **EU revenue that needs a notified body (Class I+II): EUR {eu_nb}m ({client['eu_revenue_needing_notified_body_share_of_group']*100:.0f}% of group revenue; {eu_nb/client['eu_revenue_in_scope_products_m']*100:.0f}% of in-scope EU revenue)** — headline: '__EUNB__'")
md.append(f"- Max fine per tier for Example Group: Tier 1 EUR {exposure['fine_tiers'][0]['example_group_max_m']:.0f}m; Tier 2 EUR {exposure['fine_tiers'][1]['example_group_max_m']:.0f}m; Tier 3 EUR {exposure['fine_tiers'][2]['example_group_max_m']:.0f}m")
md.append(f"- Portfolio readiness index (baseline 28 Oct 2026): **{portfolio_index*100:.0f}%**; by BU {', '.join(f'{k} {v*100:.0f}%' for k,v in bu_index.items())}; by class {', '.join(f'{k} {v*100:.0f}%' for k,v in class_index.items())}")
md.append(f"- Investment (base): one-off **{eur(base_tot['one_off_total_incl_contingency'])}** to Dec 2027 incl. 15% contingency (Q4 2026 {eur(base_tot['q4_2026_incl_contingency'])}; 2027 {eur(base_tot['y2027_incl_contingency'])}); run **{eur(base_tot['run_2028'])}/yr** from 2028; one-off = {cost_model['one_off_pct_of_revenue']*100:.2f}% of annual revenue; run = {cost_model['run_pct_of_revenue']*100:.2f}%")
md.append(f"- Scenarios one-off: low {eur(scenarios['low']['totals']['one_off_total_incl_contingency'])}; base {eur(base_tot['one_off_total_incl_contingency'])}; high {eur(scenarios['high']['totals']['one_off_total_incl_contingency'])}. Run: low {eur(scenarios['low']['totals']['run_2028'])}; high {eur(scenarios['high']['totals']['run_2028'])}")
md.append(f"- Engineering remediation: {rem_fte_years:.1f} FTE-years. Spend to date: {eur(actual_oct)} (Oct 2026) vs plan {eur(monthly_plan[0])}.")
md.append(f"- Overall programme RAG: **Amber** — {data['programme']['overall_status']}\n")

md.append("## Product families\n")
md.append("| ID | Family | BU | Class | Annex item | Revenue EUR m | EU revenue EUR m | SKUs | Wave | Route | Support yrs | Readiness |")
md.append("|---|---|---|---|---|---|---|---|---|---|---|---|")
for f in fam_list:
    md.append(f"| {f['id']} | {f['name']} | {f['bu']} | {f['cra_class']} | {f['annex_item']} | {f['revenue_m']} | {f['eu_revenue_m']} | {f['skus']} | {f['wave']} | {f['route']} | {f['support_period_years']} | {fam_index[f['id']]*100:.0f}% |")
md.append("\nLegacy lines: " + "; ".join(f"{l['name']} ({l['status']}; {l['units_in_field_k']}k units)" for l in legacy) + "\n")

md.append("## Diagnostic heatmap (average level 0-4 per domain; target 3)\n")
md.append("| Family | " + " | ".join(d['short'] for d in domains) + " | Index |")
md.append("|---|" + "---|" * (len(domains) + 1))
for f in fam_list:
    md.append(f"| {f['name']} | " + " | ".join(f"{domain_scores[f['id']][d['id']]:.2f}" for d in domains) + f" | {fam_index[f['id']]*100:.0f}% |")
md.append("| **Portfolio average** | " + " | ".join(f"**{domain_avg[d['id']]:.2f}**" for d in domains) + f" | **{portfolio_index*100:.0f}%** |")
md.append("\nDomain readiness index: " + ", ".join(f"{d['short']} {domain_index[d['id']]*100:.0f}%" for d in domains))
md.append("\nTen weakest questions (portfolio average level):")
for w in diagnostic["weakest_questions"]:
    md.append(f"- {w['id']} ({w['avg']:.2f}): {w['text']} — Action: {w['action']}")

md.append("\n## Cost model — base case lines (EUR)\n")
md.append("| Workstream | Line | Q4 2026 | 2027 | Run 2028 |")
md.append("|---|---|---|---|---|")
for l in base_lines:
    md.append(f"| {l['workstream']} | {l['line']} | {l['q4_2026']:,} | {l['y2027']:,} | {l['run_2028']:,} |")
md.append(f"| | Subtotal | {base_tot['q4_2026']:,} | {base_tot['y2027']:,} | {base_tot['run_2028']:,} |")
md.append(f"| | Contingency 15% | {base_tot['contingency_q4_2026']:,} | {base_tot['contingency_2027']:,} | - |")
md.append(f"| | **Total** | **{base_tot['q4_2026_incl_contingency']:,}** | **{base_tot['y2027_incl_contingency']:,}** | **{base_tot['run_2028']:,}** |")
md.append("\nBy workstream (one-off excl. contingency / run): " + "; ".join(f"{k} {eur(v['one_off'])} / {eur(v['run_2028'])}" for k, v in by_ws.items()))
md.append("\nMonthly cumulative plan (incl. contingency): " + ", ".join(f"{m['month']} {eur(m['cumulative_plan'])}" for m in cost_model["monthly_plan"]))

md.append("\n## Programme\n")
md.append("Phases: " + "; ".join(f"{p['id']} {p['name']} ({p['start']} - {p['end']}, {p['status']})" for p in phases))
md.append("\nWaves: " + "; ".join(f"{w['name']}: {', '.join(w['families'])} ({w['window']})" for w in waves))
md.append("\nMilestones:")
for m_ in milestones:
    md.append(f"- {m_['id']} {m_['date']} — {m_['name']} [{m_['status']}]")
md.append("\nWorkstreams:")
for w in workstreams:
    md.append(f"- {w['id']} {w['name']} (lead: {w['lead']}) — {w['rag']}: {w['note']}")
md.append("\n## KPIs (SteerCo #1, as at 30 Oct 2026)\n")
md.append("| ID | KPI | Value | Target | RAG | Trend | Source |")
md.append("|---|---|---|---|---|---|---|")
for k in kpis:
    md.append(f"| {k['id']} | {k['name']} | {k['display']} | {k['target']} | {k['rag']} | {k['trend']} | {k['source']} |")
md.append("\n## Risks\n")
md.append("| ID | Risk | L | I | Score | Rating | Owner | Mitigation | Trend |")
md.append("|---|---|---|---|---|---|---|---|---|")
for r in risks:
    md.append(f"| {r['id']} | {r['title']}: {r['description']} | {r['likelihood']} | {r['impact']} | {r['score']} | {r['rating']} | {r['owner']} | {r['mitigations']} | {r['trend']} |")
md.append("\nIssues: " + "; ".join(f"{i['id']} {i['title']} — {i['description']} (owner {i['owner']}, due {i['due']})" for i in issues))
md.append("\n## Decisions\n")
md.append("SteerCo #1 (30 Oct 2026): " + " ".join(f"{d['id']} {d['decision']}" for d in decisions["steerco_1"]))
md.append("\nBoard (19 Nov 2026):")
for d in decisions["board"]:
    md.append(f"- {d['id']} {d['decision']} — {d['detail']}")
md.append("\n## Canonical regulatory facts\n")
for f in facts:
    md.append(f"- {f['id']}: {f['statement']} ({f['basis']}{'; ' + f['url'] if f['url'] else ''})")
md.append("\n## Research datapoints (label type exactly as given)\n")
for r in research_datapoints:
    md.append(f"- {r['id']}: {r['stat']} = {r['value']} ({r['detail']}; sample: {r['sample']}; {r['date']}; {r['source']}; type: {r['type']}{'; ' + r['url'] if r['url'] else ''})")
md.append("\n## Stakeholders\n")
md.append("| ID | Stakeholder | Power | Interest | Now | Target | Key concern | Key message | Channel | Owner | Frequency |")
md.append("|---|---|---|---|---|---|---|---|---|---|---|")
for s in stakeholders:
    md.append(f"| {s['id']} | {s['name']} | {s['power']} | {s['interest']} | {s['stance_now']} | {s['stance_target']} | {s['key_concern']} | {s['key_message']} | {s['channel']} | {s['owner']} | {s['frequency']} |")
with open(OUT_MD, "w") as fh:
    fh.write("\n".join(md).replace("__EUNB__", _eunb) + "\n")
print("ok")
print("portfolio index", portfolio_index, "bu", dict(bu_index), "class", dict(class_index))
print("domain avg", dict(domain_avg))
print("fam index", dict(fam_index))
print("eu_nb", eu_nb, "eu_total", eu_total, "rev_by_class", dict(rev_by_class))
for k in scenarios:
    print(k, dict(scenarios[k]["totals"]))
print("rem fte", rem_fte_years, "testing", testing_year)
print("days", meta["days_to_full_application_from_issue"], meta["days_to_full_application_from_board"])
print("monthly", [(m['month'], m['plan']) for m in cost_model['monthly_plan']][:4])
