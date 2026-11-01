# Operator roles and supply chain: working checklists

Three tools for Aldermoor teams: pre-listing checks for third-party products (importer and distributor), ODM and Tier 1 supplier onboarding, and CRA due diligence for acquisitions. Article references are to Regulation (EU) 2024/2847 as published in the Official Journal. Items marked "policy" are Aldermoor choices, not legal requirements. Not legal advice; counsel confirms before use.

## 1. Third-party product pre-listing checks (EU stores and Cloud Marketplace)

Applies to units placed on or after 11 Dec 2027 (Art 69(2), Art 71(2)). Run once per SKU or listing, again when the manufacturer issues a new declaration, and on any trigger in section 1.4.

### 1.1 Decide the role first

- [ ] Does the product carry Aldermoor's name or trademark, or will Aldermoor change it in a way that may be a substantial modification? If yes: stop. Aldermoor is the manufacturer (Art 3(13) or Art 21). Route to product compliance for a full conformity assessment.
- [ ] Is the name or trademark on the product that of a person established outside the EU, and is Aldermoor Ireland the first to make it available in the EU? If yes: Aldermoor Ireland is the importer (Art 3(16)). Complete 1.2 and 1.3.
- [ ] Was the product bought from an EU manufacturer, importer or distributor? If yes: Aldermoor is a distributor (Art 3(17)). Complete 1.3.
- [ ] Is Aldermoor only intermediating (agent, not seller of record, no change to the product)? If yes: online-marketplace provider (recital 78); no CRA operator checks, but the DSA listing fields still apply (policy: collect the 1.3 fields anyway).
- [ ] Is the listing browser-only SaaS with no installed component? If yes: not a product with digital elements; record and close.

### 1.2 Importer-only checks (Art 19)

- [ ] Conformity assessment procedure carried out by the manufacturer, with the route named (Module A, B+C, H, or certification) and, for Class I or II products, the notified-body certificate number (Art 19(2)(a)).
- [ ] Manufacturer confirms in writing that the Annex VII technical documentation exists and will be supplied on an authority's request for 10 years after placing or the support period, whichever is longer (Art 19(2)(b), 19(6)).
- [ ] Aldermoor Ireland's name, registered trade name or trademark, postal address, email or digital contact and website added on the product, its packaging or an accompanying document, in an understood language (Art 19(4)).
- [ ] Copy of the EU declaration of conformity filed with a retain-until date of placing + 10 years or support end, whichever is later (Art 19(6)).
- [ ] Evidence pack stored so Aldermoor Ireland "can provide the necessary documents" for each check (Art 19(2), last subparagraph).
- [ ] Non-technical risk screen: any reason to believe the product presents a significant cybersecurity risk from non-technical factors? If yes, inform market surveillance authorities (Art 19(3), second subparagraph).

### 1.3 Checks for importers and distributors

- [ ] CE marking visible on the product, or for software on the declaration or accompanying website (Art 19(2)(c); Art 20(2)(a); Art 30).
- [ ] EU declaration of conformity, full or simplified with the exact internet address of the full one, accompanies the product (Art 13(20)).
- [ ] Annex II information and instructions in a language users and authorities in each target Member State understand (Art 13(18)).
- [ ] Type, batch or serial number, or equivalent on packaging or document (Art 13(15)).
- [ ] Manufacturer name, trade name or trademark, postal address, email or digital contact, website (Art 13(16)).
- [ ] Single point of contact for vulnerability reports, not limited to automated tools, included in the Annex II information (Art 13(17)) (policy check; not in the Art 20(2) list).
- [ ] Support-period end date, at least month and year, captured as a structured field and shown on the Aldermoor product page at the point of purchase (Art 13(19)).
- [ ] Importer details present where the manufacturer is outside the EU and Aldermoor is a distributor (Art 19(4) via Art 20(2)(b)).
- [ ] Supplier identity recorded for Art 23: name and address of the operator that supplied Aldermoor, retained 10 years.
- [ ] Nothing in Aldermoor's possession gives reason to believe the product or the manufacturer's processes do not conform (open advisories, PSIRT findings, authority notices). If there is: do not list (Art 19(3); Art 20(3)).

### 1.4 After listing: triggers and actions

| Trigger | Action | Basis | Internal target (policy) |
|---|---|---|---|
| Aldermoor becomes aware of a vulnerability in the product | Inform the manufacturer | Art 19(5); Art 20(4) "without undue delay" | 5 business days; same day if exploited |
| Product presents a significant cybersecurity risk | Inform the market surveillance authorities of each Member State where sold, with non-compliance and corrective measures | Art 19(5); Art 20(4) "immediately" | Same business day |
| Reason to believe the product does not conform | Ensure corrective measures, withdrawal or recall | Art 19(5); Art 20(4) | Delist within 24 hours pending review |
| Manufacturer ceases operations | Inform authorities and, as far as possible, users | Art 19(8); Art 20(6) | Within 5 business days |
| Reasoned request from an authority | Provide information and cooperate | Art 19(7); Art 20(5) | Evidence pack within 5 business days |
| Support end date reached | Product may still be sold (FAQ, guidance); flag the listing | Art 13(19) | Banner on listing |
| Commercial model changes (reseller, own brand, code change) | Re-run 1.1 | Arts 3, 21, 22; recital 78 | Before the change goes live |

## 2. ODM and Tier 1 supplier onboarding

Uses the base pack's Template 9 supplier CRA clause pack (`pack/out/hosted/D14-compliance-templates-kit/md/09-supplier-cra-clause-pack.md`). Aldermoor is the manufacturer of every ODM-built Aldermoor product (Art 3(13)); the ODM's compliance is evidence, not a transfer of duty.

### 2.1 Before award

- [ ] Tier assigned from the component's role and risk (Tier 1: firmware, security functions, remote data processing, complete ODM products) (Art 13(5); recital 34).
- [ ] Secure development framework named and evidenced (IEC 62443-4-1, NIST SSDF or equivalent) (Template 9 cl. 5.1).
- [ ] Supplier's own CRA role confirmed: does it place the component on the EU market itself (then ask for its declaration) or supply only to Aldermoor?
- [ ] Support commitment covers the support period of the last Aldermoor unit placed with this component, or escrow of source, build tooling and signing arrangements is agreed (Art 13(8); Template 9 cl. 3, 7).
- [ ] Sub-suppliers of security-relevant parts listed (Template 9 cl. 9).
- [ ] US label eligibility screen run where the product may carry a US label (module E5, UCS-05).

### 2.2 Contract terms (Template 9 plus ODM annex)

- [ ] All 12 Template 9 clauses accepted, or fallbacks recorded with a named compensating control.
- [ ] Notification: exploited vulnerability or severe incident within 12 h of supplier awareness; affected versions and mitigations within 36 h; root cause and fix details within 7 days of the fix (policy targets feeding Art 14(2) and (4)).
- [ ] Advisories never published before Aldermoor is told; embargo never blocks a legal report (Template 9 cl. 2.4, 11.3).
- [ ] Audit right yearly and after any exploited vulnerability, with the notified body named as a permitted auditor for Module H organisations (Template 9 cl. 5.3).
- [ ] Reasoned-request turnaround of 5 business days (Template 9 cl. 5.2).
- [ ] 90-day notice of security-relevant changes; 24-month end-of-support notice (Template 9 cl. 7, 8).

### 2.3 ODM firmware SBOM annex (policy, beyond the Annex I Part II(1) minimum)

- [ ] One SBOM per firmware build in CycloneDX 1.6+ or SPDX 3.0.1+, bound to the image by SHA-512.
- [ ] Full transitive depth for source-built code; per-blob identity (name, supplier, version, hash) and the blob vendor's SBOM where it exists; known unknowns marked.
- [ ] Coverage includes boot chain, TEE and trusted apps, baseband and modem, Wi-Fi and Bluetooth firmware, DSP, GPU and sensor-hub firmware, kernel version and config, vendor HALs, toolchain.
- [ ] Vulnerability status delivered separately as CSAF 2.0 with VEX.
- [ ] Aldermoor binary SCA run on each drop and reconciled; unexplained gaps block the build at the E1 release gate.

### 2.4 First delivery and ongoing

- [ ] First firmware drop passes binary SCA reconciliation, secure-boot and update-signature tests, and an interface and debug-port check (Annex I Part I(2)(c), (f), (j)).
- [ ] Supplier PSIRT contact tested with a drill notification; response within 4 h (Template 9 cl. 6.2).
- [ ] Supplier record in the intake gate: tier, clauses, response score, review date (Template 9 scoring).
- [ ] Yearly review: notification performance, SBOM quality trend, support-period headroom, audit findings.

## 3. M&A CRA due diligence

Run before signing for any target with products made available in the EU. The CRA has no M&A provision; the rules on who is manufacturer after closing are derived from Art 3(13), Art 21 and Art 22 and need counsel's confirmation.

### 3.1 Scope and classification

- [ ] Product inventory: every product with digital elements the target makes available in the EU, with brand, legal entity named as manufacturer, and EU importer or authorised representative.
- [ ] Class per product (default, Class I, Class II, critical) with the core-functionality statement (module E3 method).
- [ ] Conformity route planned for units placed from 11 Dec 2027; notified-body contract status for Class I and II.
- [ ] Radio products: RED Art 3(3)(d)-(f) declarations since 1 Aug 2025 and the EN 18031 evidence behind them; any RED type-examination certificates and their expiry (Art 69(1)).
- [ ] Products in Art 2 exclusions (medical devices, vehicles, national security) recorded with reasons.
- [ ] Tailor-made contracts that vary secure defaults or free updates, with the evidence of explicit agreement (Annex I Part I(2)(b), Part II(8)).

### 3.2 Technical files and support commitments

- [ ] Annex VII technical documentation exists or is planned for each product: risk assessment, SBOM, test evidence.
- [ ] Published support-period end dates per product and their basis (Art 13(8), 13(19)); cost to honour them for units already sold.
- [ ] Security-update archive meets the 10-year availability rule for updates already issued (Art 13(9)).
- [ ] Release cadence and substantial-modification practice (guidance pt 110 test) for software products.

### 3.3 Reporting and vulnerability history

- [ ] Art 14 notifications filed since 11 Sep 2026: count, timeliness against 24 h, 72 h and final deadlines, coordinator CSIRT used.
- [ ] Known exploited vulnerabilities in the target's products since 11 Sep 2026 that were not notified (potential Art 64(2) exposure).
- [ ] CVD policy, single point of contact and advisory history (Annex I Part II(5)-(6); Art 13(17)).
- [ ] Main establishment for Art 14(7) after closing if the target entity stays the manufacturer.

### 3.4 Supply chain and open source

- [ ] Supplier contracts with notification, SBOM, support and audit terms (Template 9 gap list).
- [ ] ODM relationships and their firmware SBOM depth.
- [ ] Open-source projects the target maintains: steward or manufacturer role, monetisation, public policy (Art 24; module E4).
- [ ] Open-source licence obligations and any upstream-reporting practice (Art 13(6)).

### 3.5 Integration rules (policy)

- [ ] Day of closing: target PSIRT connected to the Art 14 case engine (module E2); awareness rules shared.
- [ ] Within 30 days: products in the classification register and evidence store.
- [ ] Within 90 days: substantial-modification gate on all target releases.
- [ ] Before the first Aldermoor-branded unit: Aldermoor's own conformity assessment complete and declaration issued in Aldermoor's name.
- [ ] Asset deals: contract for the seller's support and Art 14 cooperation for units it placed, and a plan for cessation notices (Art 13(23); Art 19(8); Art 20(6)).

*v1.0 · 1 Nov 2026 · Aldermoor Platforms is a fictional reference client.*
