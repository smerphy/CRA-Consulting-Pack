# Open-source strategy under the CRA for Aldermoor Platforms

**Executive answer.** Aldermoor's CRA role is decided per project and per product, not per company. For the five open-source projects it leads, Aldermoor is an open-source software steward as long as it does not monetise them: a light Art 24 regime from 11 Dec 2027 with no administrative fines (Art 64(10)(b), as corrected by corrigendum OJ L, 2025/90555). For every product it sells on the same code, such as Arc phones, Lumen Browser, Lumen OS and Halo Wear, Aldermoor is the manufacturer with the full Regulation, and Art 14 reporting has applied since 11 Sep 2026. Three current or proposed arrangements could make Aldermoor the manufacturer of its own open-source code. The first is Tensile LTS builds sold only to paying cloud customers, which already places them on the market. The second is the Halo partner early-access programme, which ties earlier security patches to a commercial licence. The third is demand from device makers for a paid Lumen Engine LTS branch. We recommend staying steward for the Halo Open Source Project (HOSP) and Lumen Engine. Move Kite and the Mooring community edition to independent foundations, and open Tensile LTS to everyone. Downstream manufacturers should get Aldermoor's evidence (advisories, SBOMs, provenance, stated support windows) but not its promises: no warranties, service levels, indemnities or "CRA compliant" claims for free code. From 9 Dec 2026 the Product Liability Directive turns those promises and Aldermoor's patch record into evidence.

Project facts are illustrative for a fictional client and are recorded in `projects.yaml`. Legal points cite the knowledge base (KB). Guidance point and Example numbers refer to Commission guidance C(2026) 5252, an approved draft not yet formally adopted (verification.md claim 15), as mirrored by the ORC WG.

## Aldermoor's role is set per project and per product

Article 2 never mentions open source. The carve-out works through Art 3(22): making available means supply "in the course of a commercial activity", read with recitals 15-20. Monetisation, not the licence, decides the outcome (12-open-source.md). A steward is a legal person, other than a manufacturer, that systematically supports specific FOSS intended for commercial activities on a sustained basis (Art 3(14)). Status is assessed per project, so one company can be steward for one codebase and manufacturer for another (guidance pts 69-74; 05-roles.md).

**Exhibit 1: The role rules that matter for Aldermoor**

| Situation | Role | Source |
|---|---|---|
| Company publishes unmonetised FOSS that it also integrates into its own products | Steward for the FOSS; manufacturer for its products | Pts 67-68, 76; Examples 25, 26, 29 |
| Charging for binaries, updates or a specific supported version, even with a free equivalent | Manufacturer of what is charged for | Pts 51, 57; Example 17 |
| Open core: paid edition and free community edition on near-identical code | Manufacturer for the paid edition; steward for the community edition | Pts 52-53; Example 30 |
| FOSS used to monetise other products or services | Placed on the market | Pt 54; Examples 14-16 |
| Donations that gate access, essential functions or updates, or buy contractual benefits | Manufacturer; the payment is a de facto price. Note: membership fees paid to a not-for-profit steward do not make it a manufacturer (pt 66, Example 33) | Pts 60-62, 66; Examples 20-22, 33 |
| Paid consulting, training or support sold separately while software and maintenance stay free | Not placed on the market | Pts 55-56; Example 18 |
| Not-for-profit foundation sustaining FOSS that companies use commercially | Foundation is steward; companies owe due diligence | Pts 66, 76-78; Examples 24, 28, 33 |
| Contributor with commit rights on a project it does not publish or control | Neither manufacturer nor steward | Recital 18; pts 48-49, 85-86; Example 13 |
| Steward that starts monetising | Manufacturer from that date, not for earlier versions | Pt 84; LF Stewards Playbook |

Sources: 12-open-source.md; research notes open_source.md KQ1, KQ2, KQ7.

Two consequences follow. An OSPO is never the regulated entity; the legal person is, so each project's policy should name the Aldermoor entity that acts as steward (12-open-source.md). And being a for-profit group does not by itself make Aldermoor's open-source code commercial: financing and regular releases do not decide the question (recital 18). What decides it is whether access to the code or its maintenance depends on payment.

## Steward duties are light and start on 11 Dec 2027, but engineering support brings real reporting

**Exhibit 2: What the steward role requires of Aldermoor**

| Item | Requirement | Source |
|---|---|---|
| Cybersecurity policy | Documented and verifiable; covers secure development, documenting and remediating vulnerabilities, sharing information with the community, and promoting voluntary Art 15 reporting | Art 24(1) |
| Cooperation | Cooperate with market surveillance authorities on request; supply the policy on reasoned request | Art 24(2) |
| Reporting, infrastructure support | Notify severe incidents affecting the repositories, CI or signing infrastructure Aldermoor provides; inform users | Art 24(3) via Art 14(3), (8); pt 81 |
| Reporting, engineering support | Notify actively exploited vulnerabilities in the project. Art 24(3) applies Art 14(8) user information only to the infrastructure-incident limb, so informing users here is guidance-led good practice, not a steward duty (guidance para 82 nonetheless describes informing users as "required" where the steward has a direct relationship with them; follow it as practice) | Art 24(3) via Art 14(1); pt 82 |
| Exemptions | No CE marking, conformity assessment, Annex I duties, technical documentation or SBOM; no administrative fines under any Art 64 tier | Recitals 19, 120; Art 64(10)(b), as corrected by OJ L, 2025/90555 ("paragraphs 2 to 9") |
| Residual enforcement | An authority may require corrective action | Art 52(3) |
| Start date | 11 Dec 2027; the 11 Sep 2026 reporting start created no steward duty | Art 71(2); OpenSSF, 11 Sep 2026 |

Sources: 12-open-source.md; 05-roles.md; verification.md claims 3 and 5 (Art 24 reporting is paragraph 3).

Aldermoor provides engineering support to all five projects: it employs the maintainers, manages releases and writes the patches. So from 11 Dec 2027 Aldermoor must notify actively exploited vulnerabilities in each project as steward. That includes exploitation seen only in another vendor's product, such as a third-party browser built on Lumen Engine or an OEM phone built on HOSP. Before that date such reports are voluntary (Art 15). Which CSIRT a non-EU steward reports to is still "pending guidance" (12-open-source.md). Naming Aldermoor Ireland Ltd as the steward entity in each policy would align steward reporting with the Irish CSIRT that already coordinates Aldermoor's manufacturer reports. That is our inference, not settled law.

## When the same code ships inside Aldermoor products, Aldermoor owes the full Regulation

Integrating FOSS never transfers compliance responsibility to the project, and the project never becomes responsible for the product (guidance pts 86-88). Aldermoor's own code gets no special treatment inside Aldermoor products.

- **Due diligence (Art 13(5)).** The product's risk assessment must cover HOSP inside Arc phones and Lumen Engine inside Lumen Browser, just as it would third-party code. The fact that Aldermoor wrote the code shortens the evidence trail. It does not remove the duty.
- **Upstream reporting and fix sharing (Art 13(6)).** A vulnerability found in a component goes to "the person or entity manufacturing or maintaining the component", and any fix is shared, machine-readable where appropriate (05-roles.md). For HOSP and Lumen Engine that maintainer is Aldermoor acting as steward. In practice this means product teams must land fixes in the public project. A private patch that ships in Lumen Browser but never reaches Lumen Engine fails Art 13(6) in substance and leaves downstream browsers exposed.
- **Documentation and SBOM (Art 13(7); Annex I Part II(1)).** Components belong in the product SBOM, which need not be public (recital 77; 12-open-source.md).
- **Reporting (Art 14).** One exploited Lumen Engine bug can create two duties: a manufacturer notification for Lumen Browser, in force since 11 Sep 2026, and from Dec 2027 a steward notification for the engine. Lumen has historically seen about 10 in-the-wild exploited vulnerabilities a year (brief). The KB does not say whether one ENISA Single Reporting Platform filing can discharge both roles. The E2 case engine should record the role for each notification and file both until ENISA says otherwise.

**Exhibit 3: Aldermoor's two roles for the same code**

| Code | Steward for | Manufacturer of products containing it (E3 family) |
|---|---|---|
| HOSP | HOSP source releases | Arc phones and tablets (F01, F02; default); Halo Wear OS (F07; Class I item 11); Halo Services runs on it (F06; default) |
| Lumen Engine | Engine releases | Lumen Browser desktop and mobile, Lumen WebView (F11-F13; Class I item 2); Lumen OS (F14; Class I item 11) |
| Kite | Toolchain, standard library, registry | Aldermoor apps and services compiled with Kite (default) |
| Mooring | Community edition | Mooring Enterprise (F39; default); Aldermoor Edge tooling (F33; Class II item 1) |
| Tensile | Community releases | Tensile LTS builds (F40; default) today; on-device ML in Arc and Hearth products |

## Three monetisation choices could make Aldermoor the manufacturer of its own open-source code

**Exhibit 4: Monetisation triggers and recommendations**

| Project | Arrangement | Why it matters | Consequence if it counts as monetisation | Recommendation |
|---|---|---|---|---|
| Tensile | LTS builds only for paying cloud customers | Paid access to a specific supported version places it on the market (pt 57, Example 17) | Already a manufacturer of Tensile LTS, a default-class product: Module A, technical file, support period, Art 14 since 11 Sep 2026 | Open LTS branches to everyone; keep the paid value in the managed cloud service |
| HOSP | Security patches about 30 days early for partners who sign the Halo Services agreement | Access to updates conditioned on a commercial agreement resembles a price for updates (pts 57, 60-62 by analogy); pt 54 also catches FOSS used to monetise services | Manufacturer of an Annex III Class I item 11 operating system; full CRA for HOSP releases | Decouple: offer embargoed early access to any HOSP device maker on free, objective criteria. The guidance does not address embargoed disclosure, so record the reasoning |
| Lumen Engine | Device makers want a paid LTS branch for 5-10 year support periods | Selling LTS places those versions on the market (pt 57) | Manufacturer of an Annex III Class I item 2 embedded browser; Art 32(5) would allow Module A with public technical documentation | Prefer public LTS branches run by a member-funded not-for-profit, with releases open to all (Examples 24, 33). Member-only releases would be a de facto price (pts 60-62) |
| Mooring | Paid Enterprise edition beside the free community edition | Open core is accepted (pts 52-53, Example 30) as long as the community edition is genuinely free | Enterprise is already a manufactured product; risk only if community security fixes lag | Same-day security releases across editions |

Monetising is not forbidden; it means accepting manufacturer duties for the monetised version from that date (pt 84). The costs are fines exposure (Art 64(2): EUR 15m or 2.5% of worldwide turnover), Art 14 reporting for every downstream exploitation, product liability and, for Annex III code, the conformity route.

## Art 32(5) makes monetised important FOSS manageable, at the price of publishing the technical file

A manufacturer of a product that qualifies as FOSS and falls in an Annex III category may use any Art 32(1) route, including Module A. The condition is that the Annex VII technical documentation is public when the product is placed on the market (Art 32(5); recital 91; verification.md claim 9). The Commission FAQ confirms this extends to Class II FOSS (research notes classification_and_conformity.md KQ4).

This matters in three places.

1. **A paid Lumen Engine LTS.** As an embedded browser it would be Class I item 2. Today, without a cited standard or a notified body, it could not self-assess, except under Art 32(5). That route requires publishing the risk assessment, architecture and test reports for an engine that attackers already study closely.
2. **HOSP, if the early-access arrangement were held to be monetisation.** It would be an Annex III item 11 operating system, with the same Art 32(5) option and the same disclosure cost.
3. **Downstream browser makers.** A browser maker whose shipped product is entirely FOSS and built on Lumen Engine can use Art 32(5). An engine-level architecture and threat-model document from Aldermoor would strengthen their public technical file. It is the most useful single thing Aldermoor can publish for the Lumen ecosystem.

Art 32(5) does not help Aldermoor's shipped products. Lumen Browser and Halo builds contain proprietary code, so they do not qualify as FOSS (E3 paper).

## Downstream manufacturers can rely on Aldermoor's evidence, not on its promises

Manufacturers that build on HOSP or Lumen Engine are manufacturers of their own products, and Aldermoor is not responsible for their compliance (pts 86-88). They owe Art 13(5) due diligence on Aldermoor's code, Art 13(6) reports back to Aldermoor, and their own Art 14 notifications. They cannot force a project into the steward role, but may fork instead (FSFE FOSDEM Q&A; 12-open-source.md). They will ask Aldermoor for whatever helps them pass their own conformity assessment.

**Exhibit 5: What Aldermoor should and should not offer downstream**

| Offer (evidence, voluntary) | Do not offer for free code (promises) |
|---|---|
| Public Art 24(1) security policy and coordinated vulnerability disclosure process | CE marking or EU declarations of conformity for the projects (stewards cannot CE mark; recital 19) |
| CSAF security advisories with VEX status for each release | Statements that a project is "CRA compliant" or meets Annex I |
| Release SBOMs and signed build provenance from the existing hermetic build (see E1) | Contractual patch service levels, warranties or indemnities |
| Support windows per branch, stated as intent with a notice period before end of support | Early access, LTS or fixes conditioned on a commercial relationship |
| Engine and OS architecture and threat-model documents downstream makers can cite | Paid support for a specific version, unless the manufacturer role is chosen |
| Self-declaration against the OpenSSF OSPS Baseline, labelled voluntary | Any claim of an Art 25 attestation (none exists) |
| Security notification list with free, objective admission criteria | Private fixes that ship in Aldermoor products before they reach the public project |

**Attestations.** Art 25 empowers the Commission to set up voluntary security attestation programmes by delegated act to ease Art 13(5) due diligence on FOSS. Nothing is adopted or launched as of 30 Oct 2026. The Commission's FOSDEM 2026 slides mention only a study. The ORC WG two-tier framework is a working document: Tier 1 is a self-declaration aligned to BSI TR-03185-2, and Tier 2 is undecided (12-open-source.md). Aldermoor should prepare Tier 1-style self-declarations so it can join a programme quickly, without calling them attestations.

**Liability.** The Product Liability Directive (EU) 2024/2853 applies to products placed on the market or put into service after 9 Dec 2026 (PLD Art 2(1)). Software is a product, and a cybersecurity vulnerability can make a product defective (recital 32; Art 7(2)(f)). Non-compliance with mandatory safety requirements creates a rebuttable presumption of defect (Art 10(2)(b)). A lack of software updates needed to maintain safety removes the later-defect defence (Art 11(2)(c)). Technical files and update logs can be ordered disclosed (Art 9) (verification.md claim 19; 13-interplay.md). Free and open-source software developed or supplied outside a commercial activity is excluded (PLD Art 2(2); research notes timeline_enforcement_interplay_uk.md). For Aldermoor this means three things.

- Aldermoor's own products built on HOSP and Lumen Engine are fully exposed. Once Annex I applies (11 Dec 2027), a breach supports the presumption of defect, so patch cadence on the projects is also a liability control for Arc and Lumen products.
- The unmonetised projects themselves probably sit outside the PLD under Art 2(2). The KB did not research how the PLD treats FOSS later integrated by a third party, or whether a for-profit group's strategic FOSS counts as "outside a commercial activity" under the PLD. Counsel should confirm. Monetising a project removes the argument.
- Promises to downstream makers can become evidence in their recourse claims. Keep commitments public, voluntary and stated as intent.

## Foundation governance moves the steward role, not the dependency

**Exhibit 6: Company stewardship versus foundation stewardship**

| Criterion | Aldermoor as steward | Independent foundation as steward |
|---|---|---|
| Who carries Art 24 | Aldermoor | The foundation (Examples 28, 33); Aldermoor is a contributor (recital 18; pts 48-49) |
| Art 14 reporting for the project | Aldermoor, through engineering and infrastructure support | Foundation, to the extent it provides that support; Aldermoor still reports as manufacturer of its products |
| Control of roadmap and releases | Full | Shared; release authority must sit with the foundation for the contributor position to hold (pts 48-49) |
| Downstream trust and contribution | Lower for competitors | Higher; neutral governance attracts co-maintainers |
| Monetisation flexibility | Any monetisation flips Aldermoor to manufacturer | Member fees fund LTS without making the foundation a manufacturer if releases stay public (pt 66; Example 33) |
| Cost | All on Aldermoor | Shared, but Aldermoor usually remains the largest funder |
| Fit | Strategic platforms where control is essential | Ecosystem projects where neutrality drives adoption |

Foundation transfer does not remove Aldermoor's dependency: it still owes Art 13(5) due diligence on the code inside its products. It removes the steward duties and makes neutral, shared-cost long-term support possible.

**Exhibit 7: Decision matrix per project**

| Project | Governance today | Monetisation today | Role today | Main trigger risk | Recommended role | Governance move | Decision owner |
|---|---|---|---|---|---|---|---|
| HOSP | Aldermoor-controlled | None directly; Halo Services licensed separately | Steward (at risk) | Partner early access tied to services licence | Steward | Stay company-governed; publish charter and policy; decouple early access | General Counsel with VP Platforms |
| Lumen Engine | Aldermoor-led, multi-vendor committers | None | Steward | Paid LTS demanded by device makers | Steward | Keep the engine; put LTS in a member-funded not-for-profit with public releases | CTO |
| Kite | Aldermoor-led, advisory council | None; registry hosted by Aldermoor | Steward (engineering and infrastructure) | Supported distribution or paid registry features | Contributor after transfer | Transfer to a Kite Foundation including registry and release authority | Head of OSPO |
| Mooring | Aldermoor-led; open core | Mooring Enterprise | Steward (community); manufacturer (Enterprise) | Community security fixes lagging Enterprise | Contributor (community); manufacturer (Enterprise) | Contribute community edition to a neutral foundation | Head of OSPO |
| Tensile | Aldermoor-led | LTS only for paying cloud customers | Steward (community); manufacturer (LTS) | Current LTS gating; model weights unresolved | Steward | Stay company-led; open LTS to all | VP Engineering, ML with General Counsel |

## Recommended public statement: Aldermoor's CRA open-source posture (draft)

> **How Aldermoor approaches the EU Cyber Resilience Act for the open-source projects we lead**
>
> Aldermoor leads the Halo Open Source Project, Lumen Engine, Kite, Mooring and Tensile. We publish these projects free of charge under open-source licences. Under Regulation (EU) 2024/2847 we act as the open-source software steward for the projects we sustain and do not monetise. Where a project moves to an independent foundation, the foundation takes that role and we remain a contributor.
>
> As steward we will publish, for each project, a cybersecurity policy covering secure development, vulnerability handling and information sharing. We will cooperate with market surveillance authorities. From 11 December 2027 we will notify actively exploited vulnerabilities and severe incidents affecting project infrastructure as Article 24 requires, and we will share such information voluntarily before then.
>
> Security fixes for our open-source projects are available to everyone. When we share fixes in advance under embargo to coordinate disclosure, access does not depend on any commercial agreement with Aldermoor.
>
> To help manufacturers who build on our projects, we publish security advisories, software bills of materials, signed build provenance and the support windows we intend for each release branch. These are voluntary and provided without warranty. Our open-source projects do not carry CE marking or EU declarations of conformity. Manufacturers remain responsible for their own products, including due diligence on the components they integrate.
>
> Where Aldermoor sells a product or edition, such as Mooring Enterprise or devices and software built on these projects, Aldermoor is the manufacturer of that product and meets the Regulation's requirements for it.
>
> Please report vulnerabilities through each project's security policy. We welcome reports and fixes from manufacturers under Article 13(6), and we credit them.

The statement avoids promises that would create monetisation triggers or contractual liability. Publish it only after decisions 2 and 3 below, because it commits Aldermoor to decoupled early access and open Tensile LTS.

## Decisions for the executive team

1. **Confirm the steward role for HOSP and Lumen Engine and name the steward legal entity (recommended: Aldermoor Ireland Ltd) in each project's policy.** Owner: General Counsel. Timing: by Mar 2027; policies published by Jun 2027, six months before Art 24 applies.
2. **Decouple Halo partner early access from the Halo Services agreement.** Owner: General Counsel with VP Platforms. Timing: contract changes by Jun 2027.
3. **Open Tensile LTS to all users, or confirm it as a manufactured product with full CRA treatment.** Owner: VP Engineering, ML. Timing: decision by Mar 2027; in either case list Tensile LTS in the E2 case engine now.
4. **Choose the Lumen Engine LTS model.** Recommended: public LTS run by a member-funded not-for-profit. Alternative: Aldermoor-sold LTS under Art 32(5) with a published technical file. Owner: CTO. Timing: by Mar 2027, before device makers lock in their 2027 platform choices.
5. **Transfer Kite and the Mooring community edition to independent foundations, with release authority and infrastructure.** Owner: Head of Open Source Programme Office. Timing: Kite by Sep 2027; Mooring by Dec 2027.
6. **Adopt the downstream evidence pack and the public posture statement, and ban downstream warranties and "CRA compliant" claims for free code.** Owner: CISO with Communications. Timing: publish with the policies in Jun 2027.

## Risks and open questions

- **Embargoed early access.** The guidance does not address coordinated-disclosure embargoes limited to a group of device makers. Free, objective admission reduces but does not remove the monetisation argument.
- **Dual-role reporting.** The KB does not say whether one ENISA filing can serve both the manufacturer and the steward role, or which CSIRT a steward reports to when its main establishment is outside the EU ("pending guidance").
- **Guidance status.** C(2026) 5252 is an approved draft. The steward section (pts 69-84) is the only official steward guidance, and point numbers could change on adoption.
- **PLD and FOSS.** PLD Art 2(2) excludes FOSS supplied outside a commercial activity. How that interacts with a for-profit group's strategic projects, and with FOSS integrated by others, was not researched in the KB.
- **Paid hosting, dual licensing and model weights.** None is addressed in the guidance (12-open-source.md; 03-scope.md). Document Aldermoor Cloud's managed Kite, Mooring and Tensile offerings as services, and record the reasoning.
- **Foundation transfer and control.** If Aldermoor employees keep release authority in practice, an authority may still see Aldermoor as the publisher (pts 48-49).
- **Art 25 timing.** No attestation programme exists. Downstream makers will rely on self-declarations until one does.
- **Downstream pressure.** Large device makers may ask for contractual commitments as a condition of adopting HOSP or Lumen Engine. Each such request is a monetisation and liability decision, not a sales concession.

## Sources

- Knowledge base: reports/sections/05-roles.md (roles, Art 13(6), PLD Art 8); 06-classification.md (Annex III items 2 and 11); 10-conformity.md (Art 32 routes, Art 32(5)); 12-open-source.md (monetisation table, steward duties, Art 25, ecosystem resources); 13-interplay.md (PLD); reports/verification.md (claims 3, 5, 9, 15, 19).
- Research notes: research_notes/EU CRA engineering compliance/open_source.md (KQ1-KQ7); timeline_enforcement_interplay_uk.md (PLD Arts 2, 4, 7, 9, 10, 11); classification_and_conformity.md (KQ4, FAQ s.6.1 on Class II FOSS).
- [Regulation (EU) 2024/2847](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) (Arts 3(14), 3(22), 13(5)-(7), 14, 15, 24, 25, 32(5), 52(3), 64(10)(b), 71; recitals 15-21, 77, 91, 120).
- [Commission guidance C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456), as mirrored by the [ORC WG](https://cra.orcwg.org/official-guidance/) (Section 3, pts 40-88; Examples 13-34).
- [Commission CRA FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307) and [CRA open-source page](https://digital-strategy.ec.europa.eu/en/policies/cra-open-source).
- [Product Liability Directive (EU) 2024/2853](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32024L2853).
- [ORC WG steward FAQ](https://cra.orcwg.org/faq/stewards/), [steward white paper V1.0](https://orcwg.org/files/cra/resources/white-paper-on-open-source-software-stewards-and-cra.pdf) and [attestations working document](https://github.com/orcwg/cra-attestations/blob/main/overview.md).
- [Linux Foundation / OpenSSF Stewards Playbook](https://policy.openssf.org/CRA/stewards-playbook.html), [OpenSSF guide of 11 Sep 2026](https://openssf.org/blog/2026/09/11/a-community-guide-to-the-eu-cra-september-11-deadline-for-manufacturers/) and [OSPS Baseline](https://openssf.org/wp-content/uploads/2026/01/OpenSSF-OSPS-Baseline.pdf).
- [Commission FOSDEM 2026 slides](https://archive.fosdem.org/2026/events/attachments/EERURR-implementing_the_cyber_resilience_act_-_engaging_with_open_source/slides/267519/slides-cr_pyebtat.pdf) (Art 25 study) and [FSFE FOSDEM Q&A](https://fsfe.org/news/2026/news-20260224-01.html).
- Module data: `projects.yaml`; E3 classification register `../portfolio-classification/classification.csv`.
