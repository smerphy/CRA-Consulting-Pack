## 3. Threat modelling and the Article 13 risk assessment

The Art 13 risk assessment decides which Annex I Part I items apply, so build it as a living engineering artefact. It rests on intended purpose, foreseeable use, conditions of use and expected time in use (Art 13(2)-(3)). It states per item whether and how 2(a) to 2(m) apply, justifies every "not applicable" and is updated through the support period (Art 13(3)-(4)).

The legal reading is in Annex I Part I: essential requirements for product properties; this section gives the method.

No methodology is mandated ([Commission FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307) section 4.1). Whatever method you choose, a market surveillance authority must be able to follow the trail from asset to threat to decision to evidence.

### Method options

| Method | Fits | What it gives the file | Reference |
|---|---|---|---|
| STRIDE on data-flow diagrams | Software products, apps, backends | Per-flow threats across six classes; trust boundaries; a diagram the ENISA Playbook calls for | [ENISA Playbook v1.0](https://www.enisa.europa.eu/sites/default/files/2026-07/ENISA_Secure_By_Design_and_Default_Playbook_v1.pdf) section 2.3 (illustrative method; Shostack four questions; "minimum viable model" for SMEs) |
| IEC 62443-3-2 zones and conduits | OT and industrial devices, gateways | Zone partitioning, conduit risk, security-level targets reusable in 62443-4-2 control selection | JRC-ENISA mapping places it against Part I point (1); IACS-scoped, not expected to be cited |
| BSI TR-03183-1 v1.0.0 method | Any product; teams without a mature process | ISO 31000-style flow: RH_RA.1 assets and threat modelling, RH_RA.1.2 impact 1-5 by likelihood, RH_RT.1 treatment, RH_DOC.1, RH_UPD.1; PASS, FAIL or N/A verdicts per control; section 4.8 report skeleton | [BSI TR-03183-1](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-1_v1_0_0.pdf?__blob=publicationFile&v=3) (non-binding, living document) |
| EN 18031 decision trees | Radio equipment already assessed under RED | Decision record per requirement: asset, interface, path, rationale, evidence; same control families reused in draft EN 40000-1-4 | EN 18031-1:2024 (cited under RED only) |

Combine them freely. A common pattern is BSI TR-03183-1 for structure and verdicts, with STRIDE on the data-flow diagram for threat discovery. Add 62443-3-2 zoning where the product sits in an industrial network, and record the method and the reason in the assessment header.

### Inputs

1. The product definition record from section 2: boundary, remote-function map, variants, intended purpose, foreseeable use and misuse, expected time in use (Art 13(3)).
2. Conditions of use: operational environment, user capability, who administers it, network exposure, physical access.
3. Asset list in the three BSI classes. Data assets: credentials, keys, personal data. Functional assets: control functions, the update path. Security assets: root of trust, signing keys, audit log.
4. Architecture and data-flow diagrams showing every interface, including the product-to-RDPS boundary and each third-party service.
5. Component inventory with due-diligence status (section 9), because recital 58 asks for supplier dependencies to appear in the assessment.
6. Threat intelligence relevant to the product class, including EUVD and vendor advisories for the components used.

For critical-infrastructure products the model must include capable adversaries; for consumer products a different model is acceptable (FAQ section 4.1). Write the attacker profile down.

### Procedure

1. Draw the data-flow diagram and mark trust boundaries, including the RDPS endpoints on both sides.
2. Enumerate assets per class and attach each to the components and flows that hold or move it.
3. Run the threat method against each flow and asset; record threats with an identifier, the affected component and the attack path.
4. Rate impact on confidentiality, integrity and availability and likelihood from interface exposure, access restriction and user capability (TR-03183-1 RH_RA.1.2 style).
5. Evaluate each risk against acceptance criteria written for this product, not a corporate appetite table (see residual risk below).
6. Select controls and trace each to the Annex I Part I item it serves; populate the applicability matrix.
7. Record residual risk per item and the "other means" relied on, such as user information or intended-use limits.
8. State how Part I point (1) and the Part II processes are applied, as Art 13(3) requires.
9. Sign off, version, and register the update triggers.

Where a companion app or RDPS serves several products, model it once and reference it, as TR-03183-1 section 5.8.1.2 suggests.

### The applicability matrix

Art 13(3) requires a statement per item. Art 13(4) and recital 55 require a justification for each item not applied, plus treatment of the residual risk by other means. Keep one row per item and one matrix per product or family.

| Item | Applies? | Implementation (control, component, version) | Evidence (test, config export, report, location) | Justification if not applicable and residual-risk treatment |
|---|---|---|---|---|
| 2(a) no known exploitable vulnerabilities | | | | |
| 2(b) secure by default and reset | | | | |
| 2(c) security updates, automatic where applicable | | | | |
| 2(d) access control and unauthorised-access reporting | | | | |
| 2(e) confidentiality | | | | |
| 2(f) integrity and corruption reporting | | | | |
| 2(g) data minimisation | | | | |
| 2(h) availability and DoS resilience | | | | |
| 2(i) limit impact on other networks | | | | |
| 2(j) limit attack surfaces | | | | |
| 2(k) exploitation mitigation | | | | |
| 2(l) logging with user opt-out | | | | |
| 2(m) secure erase and transfer | | | | |

Expect a heavy justification burden for marking (a), (b), (d) or (l) not applicable. The ETSI drafts treat them as near-universal (see Annex I Part I: essential requirements for product properties). Legitimate cases include 2(g) with no personal data processed, 2(c) automatic installation under the recital 56 carve-out, and 2(m) transfer with nothing transferable.

### Residual-risk treatment

Residual risk is judged against "an appropriate level of cybersecurity based on the risks". Guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) paras 156-163 state that cost, commercial strategy and internal risk tolerance "are not relevant". Risk cannot be shifted to users to cover a design shortcoming; an unaddressable risk means the design, functionality or intended purpose must change.

Recital 55 allows residual risk on a non-applicable item to be addressed by other means, such as limiting intended use or informing users. A documented real deployment environment can form part of the intended purpose; a vague disclaimer cannot. Every such reliance must appear in the Annex II document (point 5) so it reaches the user.

Write acceptance criteria per product in terms of impact to users, data and connected systems. A row reading "accepted, business decision" fails. A row reading "accepted: physical access required, documented in Annex II 8(a), re-test on new interface" passes.

### Update triggers

Art 13(3) requires the assessment "updated as appropriate during a support period". Part II point 3 requires updates after regular tests and reviews, and BSI TR-03183-1 RH_UPD.1 names the minimum triggers. Wire these into the PSIRT and release processes rather than a calendar.

- A security-relevant release, including any release that changes interfaces, dependencies, the update path or RDPS boundaries.
- A newly known vulnerability in the product or a component (section 8 triage output).
- A newly known threat or attack technique relevant to the product class.
- Results of security tests, reviews or penetration tests that reveal new information.
- A substantial-modification assessment at the release gate (section 5), which re-runs the affected rows only (guidance paras 122-123).

Each update is a new version of the assessment with a change log. Keep old versions, because the technical file must reflect every version placed on the market (Art 13(13)).

### Where it lives

The assessment is Annex VII point 3, with the support-period rationale beside it in point 4 (see Conformity assessment and documentation). The BSI TR-03183-1 section 4.8 report structure is a usable container, and section 11 of this guide adopts it. Store the diagrams, threat list, matrix and change log together under version control, linked from the evidence index (section 12).

### Worked mini-example

Three rows for a connected device with a companion app and a manufacturer cloud, written to the standard an assessor should see.

| Threat and asset | Risk and rating | Item and control | Evidence | Residual risk and treatment |
|---|---|---|---|---|
| T-07: attacker on the home network replays a captured remote command to the device (functional asset: actuator control) | Integrity high; likelihood medium (remote interface, no physical access needed) | 2(f): commands carry a device-bound signature and monotonic nonce; device rejects stale or unsigned commands; rejection logged under 2(l) | Protocol design note v3; negative test NT-12 (replay rejected); log sample L-04 | Low; residual depends on device clock integrity, covered by signed time sync; no user action needed |
| T-11: factory-default credential reused across units lets an attacker log in to the local admin interface (data asset: admin credential) | Confidentiality and integrity high; likelihood high if defaults exist | 2(b) and 2(d): per-unit credential provisioned at manufacture, printed on the unit, forced change at first login; lockout after 10 failures | Provisioning record P-02; firmware config export FC-09 showing no default account; test NT-03 | Low; residual is sticker loss, treated by Annex II 8(a) guidance and in-app reset flow |
| T-19: OSS TLS library in firmware carries CVE listed in EUVD at release candidate time (security asset: TLS stack) | Severity depends on reachability; the vulnerable code path is not compiled in | 2(a): reachability analysis shows function excluded by build flags; VEX statement "not_affected" with justification; upgrade scheduled for next security release | SBOM hash S-2026.10; VEX V-031; build-flag evidence BF-02 | Accepted as not exploitable in this product (guidance para 218); re-test trigger if library configuration changes |

Each row names an item, a control, an evidence identifier and a treatment that is not cost. That is the decision trail authorities and notified bodies will ask for.

The signed assessment closes the Annex I Part I and Article 13 lines in the Requirement checklists tab (checklists 2 and 4).
