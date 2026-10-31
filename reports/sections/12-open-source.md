## Open-source software

Unmonetised free and open-source software (FOSS) is outside the [CRA](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) unless its publisher is an open-source software steward. Article 2 never mentions open source. The carve-out works through Art 3(22), which defines making available as supply "in the course of a commercial activity", read with recitals 15 to 20.

Section 3 (points 40 to 88, Examples 13 to 34) of the Commission guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) of 27 Jul 2026 applies that test case by case. The guidance is non-binding and formally still awaits adoption in all languages. Monetised FOSS makes its publisher a manufacturer with the full Regulation.

Stewards carry light duties under Art 24 from 11 Dec 2027. Manufacturers owe Art 13(5) due diligence on every open-source component they ship, whatever the component's own status.

### Who is caught

Point and Example numbers refer to C(2026) 5252 as mirrored by the [ORC WG](https://cra.orcwg.org/official-guidance/). The Commission PDF is authoritative. "Full CRA" means Annex I, Arts 13 and 14, conformity assessment and CE marking.

| Situation | Role under the CRA | Obligations | Source |
|---|---|---|---|
| Natural person publishes FOSS without monetising it; a donation link is fine | Outside the CRA; natural persons cannot be stewards | None | Pts 53, 58, 60-61; Ex 34 |
| Legal person publishes unmonetised FOSS and sustains it (hosting, governance, releases) | Steward | Art 24 only, from 11 Dec 2027 | Recital 19; pts 69-78 |
| Contributor submits code or holds commit rights on a project it does not publish or control | Neither manufacturer nor steward | None for that contribution | Recital 18; pts 48-49, 85-86; Ex 13 |
| Charging for binaries, updates or a specific supported version, even if a free equivalent exists | Manufacturer | Full CRA; fines possible | Pts 51, 57; Ex 17 |
| Open core: paid edition plus free community edition on near-identical code | Manufacturer for the paid edition; steward for the community edition if a legal person | Full CRA for the paid edition; Art 24 for the community edition | Pts 52-53; Ex 30 |
| Paid consulting, training or support sold separately; software and maintenance stay freely accessible | Not placed on the market; steward if a legal person sustains it | Art 24 if steward, else none | Pts 55-56; Ex 18 |
| Donations that gate access, essential functions or updates, or buy contractual benefits | Manufacturer; the donation is a de facto price | Full CRA | Pts 60-62; Ex 20-22 |
| Grants, bounties or paid development funding an openly shared feature | Not placed on the market by the developer | None for the developer; Art 13(5) for the integrator | Recital 18; pts 63-65; Ex 23, 27 |
| Not-for-profit whose earnings after costs go to not-for-profit aims, including search-partnership revenue | Not commercial; steward | Art 24 | Recital 18; pt 66; Ex 24 |
| Company publishes unmonetised FOSS it also integrates into its own products | Steward for the FOSS; manufacturer for its products | Art 24 for the FOSS; full CRA for the products | Pts 67-68, 76; Ex 25, 29 |
| Public administration supplies FOSS and charges only actual cost recovery | Not commercial on that ground alone | None on that basis | Recital 16 |
| Foundation sustains FOSS that companies use commercially | Steward; the companies owe due diligence | Art 24 | Pts 76-78; Ex 28, 33 |
| Repository, package manager or collaboration platform merely hosts FOSS | Not making available; not a distributor unless it supplies commercially | None | Recital 20; Ex 34 |
| Manufacturer integrates an unplaced FOSS component into a commercial product | Manufacturer for its own product; not responsible for the component's own compliance | Art 13(5), (6), (7); SBOM | Art 13; pts 86-88 |
| Manufacturer places FOSS on the market commercially and it is an Annex III important product | Manufacturer | Any Art 32(1) route, including Module A, if the Annex VII documentation is made public | Art 32(5); recital 91 |
| Dual licensing; paid hosting of FOSS as a service | Not addressed in the guidance | Treat the paid offering as a product and document the reasoning; unresolved as of 30 Oct 2026 | Nearest analogues pts 52-54 |

### Stewards (Art 24)

A steward is a legal person other than a manufacturer that systematically supports specific FOSS "intended for commercial activities" (Art 3(14)). Status is assessed per project: one entity can be steward for one codebase and manufacturer for another (pts 69-74). An OSPO is never the regulated entity; the company or foundation is.

| Item | What the CRA requires | Source |
|---|---|---|
| Cybersecurity policy | Documented and verifiable; covers secure development, vulnerability documentation and remediation, information sharing with the community, and promotion of voluntary Art 15 reporting | Art 24(1) |
| Cooperation | Cooperate with market surveillance authorities on request; supply the policy on reasoned request in a language they understand | Art 24(2) |
| Reporting with non-technical support only (branding, governance, donations) | No Art 14 reporting; share information per the policy | Art 24(3); pt 80 |
| Reporting with infrastructure support (repositories, CI, signing keys) | Notify severe incidents affecting that infrastructure; inform users | Art 24(3) via Art 14(3), (8); pt 81 |
| Reporting with engineering support (employed developers, releases, patches) | Notify actively exploited vulnerabilities; inform users directly where there is a direct relationship | Art 24(3) via Art 14(1); pt 82 |
| Exemptions | No CE marking (recital 19), no conformity assessment, no Annex I, no technical documentation, no SBOM; no administrative fines under Art 64(10)(b) | Recitals 19, 120; [ORC FAQ](https://cra.orcwg.org/faq/stewards/) |
| Residual enforcement | A market surveillance authority may require corrective action | Art 52(3) |
| Status changes | Monetising a project makes the steward its manufacturer from that date, not for earlier versions; ceasing systematic support ends steward status | Pts 83-84; [LF Stewards Playbook](https://policy.openssf.org/CRA/stewards-playbook.html) |
| Applies from | 11 Dec 2027 under Art 71(2); the 11 Sep 2026 reporting start created no steward duty | [OpenSSF, 11 Sep 2026](https://openssf.org/blog/2026/09/11/a-community-guide-to-the-eu-cra-september-11-deadline-for-manufacturers/) |

Which CSIRT a non-EU steward reports to is "pending guidance" (ORC WG FAQ). Nobody can be forced into the role. [FSFE's](https://fsfe.org/news/2026/news-20260224-01.html) FOSDEM 2026 Q&A records the Commission and the German authority saying a manufacturer may fork or find alternatives instead.

### Contributors and maintainers

Recital 18 excludes anyone who contributes source code to FOSS "not under their responsibility". The guidance ties responsibility to publishing and controlling releases, so commit rights alone are not enough (pts 48-49, Ex 13). Integrators who contribute upstream do not become responsible for the component (pts 85-86).

A natural person who does not monetise has no obligations and cannot be a steward (pt 53). Recovering actual costs including "reasonable living expenses" is not monetisation (pt 58).

Residual exposure is confined to two cases. One is monetising access, updates or support in a way the table treats as a price. The other is substantially modifying FOSS for a customer under Art 22 (pt 59).

The revised Product Liability Directive is a separate question; see Interplay with other law, the Digital Omnibus and the UK position.

### Manufacturers consuming open source

Integrating FOSS never transfers compliance responsibility to the project. Art 13(5) requires due diligence on third-party components, expressly including FOSS never placed on the market. Art 13(6) requires the manufacturer to report a vulnerability it finds to the maintainer and to share any fix, machine-readable where appropriate.

Art 13(7) requires systematic documentation of vulnerabilities and third-party information. Components belong in the SBOM under Annex I Part II(1), which recital 77 says need not be public.

Guidance Section 7.3 (pts 167-173) frames due diligence as defining what the product needs from the component and verifying it by documentation, assurance evidence or tests. Recital 21 lets Art 25 attestations serve as that evidence once they exist. Section 9.2.1 upstream-reporting rules and SBOM depth are covered in Annex I Part II: vulnerability handling and lifecycle duties. The Art 32(5) route is in Conformity assessment and documentation.

### Art 25 attestation programmes

Nothing is adopted or launched as of 30 Oct 2026. Art 25 empowers the Commission to adopt delegated acts under Art 61 establishing voluntary attestation programmes; recital 21 also allows a Cybersecurity Act certification scheme. The Commission's [FOSDEM 2026 slides](https://archive.fosdem.org/2026/events/attachments/EERURR-implementing_the_cyber_resilience_act_-_engaging_with_open_source/slides/267519/slides-cr_pyebtat.pdf) (1 Feb 2026) mention only a study.

FSFE's community survey closed 28 Feb 2026. The ORC WG [two-tier draft](https://github.com/orcwg/cra-attestations/blob/main/overview.md) (Tier 1 self-declaration aligned to BSI TR-03185-2, Tier 2 undecided) is a working document, not a programme.

### Ecosystem resources

| Resource | Body | Status or date | What it gives you |
|---|---|---|---|
| [Steward white paper V1.0](https://orcwg.org/files/cra/resources/white-paper-on-open-source-software-stewards-and-cra.pdf) | ORC WG (Eclipse Foundation) | Shipped Jan 2026; marked "not legal guidance" | Art 24(1) policy content, evidence kept in SECURITY.md and advisories, open questions on CSIRT routing |
| [Due-diligence white paper D3.2](https://orcwg.org/cra/resources/) | ORC WG | Work in progress, Sep 2026 | Manufacturer side of Art 13(5) |
| D4.1 vulnerability-management spec; D4.2-D4.4 steward specs | ORC WG | D4.1 work in progress; D4.2-D4.4 no status shown, Sep 2026 | Future templates; none final |
| [Attestations white paper D3.3](https://orcwg.org/cra/resources/d3-3-white-paper-on-security-attestations/) | ORC WG | Planned; no date | Shape of a future Art 25 programme |
| [ORC Learning Hub](https://orcwg.org/cra/) | ORC WG | Live; two introductory courses | Open-source-focused CRA training |
| [OSPS Baseline](https://openssf.org/wp-content/uploads/2026/01/OpenSSF-OSPS-Baseline.pdf) | OpenSSF | Jan 2026 PDF; 41 requirements, 3 levels, 6 lifecycle stages | Project security controls; OpenSSF puts coverage of manufacturer duties at about 35% ([Tech Talk recap](https://openssf.org/?p=11738)) |
| [Stewards Playbook](https://policy.openssf.org/CRA/stewards-playbook.html) and [One Pager](https://policy.openssf.org/CRA/stewards-one-pager.html) | Linux Foundation / OpenSSF | Living documents | Monetisation triggers, reporting clocks, per-project steward entity check |
| Maintainer readiness guide; manufacturer checklist | OpenSSF | Linked from the 11 Sep 2026 guide | Plain-language duties for each side |
| [LF Research 2025](https://www.linuxfoundation.org/blog/unaware-and-uncertain-is-the-open-source-community-prepared-for-the-new-regulatory-reality-of-the-cyber-resilience-act) | Linux Foundation | 27 Mar 2025; survey | 62% unfamiliar with the CRA; 74% of stewards have policies; steward gaps funding 50%, legal 47%, technical 44% |
| [LF Research 2026](https://www.linuxfoundation.org/hubfs/Research%20Reports/lfr_2026_cra_awareness_report_060826.pdf?hsLang=en) | Linux Foundation | Jun 2026; 843 respondents; survey | Manufacturers: 32% produce SBOMs for all products; 51% rely passively on upstream fixes; 41% expect compliance by 2027 |
| [FSFE FOSDEM Q&A](https://fsfe.org/news/2026/news-20260224-01.html) | FSFE | 24 Feb 2026 | "No one has to become a steward"; attestation survey |
| [Commission FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307), guidance Section 3 and the [CRA open-source page](https://digital-strategy.ec.europa.eu/en/policies/cra-open-source) | European Commission | 4 Sep 2026; 27 Jul 2026 | Official interpretation of monetisation, stewards and contributors |
