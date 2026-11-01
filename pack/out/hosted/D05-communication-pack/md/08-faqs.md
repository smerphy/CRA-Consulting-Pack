# FAQs

**Thirty-five approved answers: 20 for staff and 15 for customers. Answer from these words; send anything they do not cover to \[CRA questions mailbox\].**

## Internal staff FAQ

- **Owner:** internal communications, with the compliance lead for accuracy
- **Approver:** executive sponsor; General Counsel reviews
- **Publish:** intranet, Fri 20 Nov 2026; reviewed monthly after SteerCo

### The law

1. **What is the Cyber Resilience Act?** An EU regulation (Regulation (EU) 2024/2847) that sets cybersecurity requirements for hardware and software products sold in the EU. It entered into force on 10 Dec 2024 and brings product cybersecurity under CE marking.
2. **When does it apply?** In stages. Reporting of actively exploited vulnerabilities and severe incidents has applied since 11 Sep 2026. The rules for notified bodies have applied since 11 Jun 2026. Everything else, including the product requirements, applies from 11 Dec 2027.
3. **Which of our products does it cover?** All of them: 13 product families and 55 SKUs, together with their companion apps and the cloud services we build that they need to work. Products we no longer sell are still covered by the reporting duty.
4. **Could the deadline move?** Plan on the dates in the law. The Digital Omnibus proposal now under discussion does not amend the CRA, and it has not been adopted (as at 30 Oct 2026).
5. **What happens if we get it wrong?** From 11 Dec 2027 authorities can order corrective action, withdrawal or recall, and fine up to EUR 15m or 2.5% of worldwide turnover, whichever is higher; Finland can already enforce Article 14 breaches. For products placed on the market or put into service after 9 Dec 2026, the Product Liability Directive also treats software as a product and a vulnerability as a possible defect.

### Project Rampart

6. **What is Project Rampart?** Our 14-month programme to keep selling in the EU after 11 Dec 2027. It runs in three waves: it builds shared capabilities once (PSIRT, SBOM pipeline, secure updates, evidence system), applies them product by product, and books notified-body capacity by Q1 2027. The CTO is accountable.
7. **Why do some products need a notified body?** The CRA lists categories of important products. Seven of our families fall into them: V1, L2, IR-500, IS-300, SecureLink and FleetView (Class I) and SG-900 (Class II). A Class I product may self-assess only by applying in full a cited harmonised standard, a common specification or a ‘substantial’ EU certification scheme (Art 32(2)), and none is available as at 30 Oct 2026. A Class II product always needs a third party.
8. **Are any notified bodies ready?** Not yet. No CRA notified body was verifiably designated at checks to 8 Sep 2026, and Member States must only ‘strive’ for enough bodies by 11 Dec 2026. We have shortlisted three candidates and are arranging pre-assessments.
9. **Will our products be ‘CRA certified’?** No: there is no general CRA certificate. Each product will have an EU declaration of conformity, signed by us, and CE marking. For important products a notified body first assesses the product or our quality system, but conformity is still declared by us. Please never use the phrase ‘CRA certified’.

### Reporting and incidents

10. **What is an actively exploited vulnerability?** A weakness for which there is reliable evidence that an attacker has used it against a system without permission. A published exploit, a proof of concept or a researcher’s finding without evidence of exploitation is not enough on its own.
11. **What is a severe incident?** An incident that affects, or could affect, a product’s ability to protect sensitive data or functions, or that leads to malicious code running in the product or in users’ systems, such as a compromise of our update service or signing keys. A ransomware attack on our office IT counts only if it reaches product security.
12. **I think one of our products is being attacked. What do I do?** Tell PSIRT within the hour at \[PSIRT contact\], day or night. Say which product and version, what you saw, when (in UTC if you can) and where the evidence is. Preserve logs, do not investigate alone, and do not discuss it with customers, in tickets or on social media.
13. **Who decides whether we report, and does it need approval?** The PSIRT lead, or a named deputy, decides when we are ‘aware’ and whether a case is reportable. The 24-hour early warning needs no approval; General Counsel reviews the 72-hour notification and the final report.
14. **Do we report problems in products we no longer sell?** Yes. Reporting covers every product we have placed on the EU market, including discontinued lines such as the T100 thermostat (1.1m units in the field), HomeHub H2 and the V0 camera, and it continues after support ends.

### Products and engineering

15. **Does our SBOM have to be public?** No. The SBOM is part of our technical documentation, and the law says manufacturers should not be obliged to make it public. Authorities can ask for it, and B2B customers can request it under \[terms\].
16. **How long must we support our products?** For the support period we declare: at least five years, unless the product is expected to be used for less, and longer where customers reasonably expect it. Our planned periods run from 5 to 12 years by family. Each security update must stay available for at least 10 years, or for the rest of the support period if that is longer.
17. **What is the release gate, and will it slow us down?** A check before each release that the evidence exists: a signed SBOM, no open high-risk findings, an up-to-date risk assessment and a signed update. It is enforced on the T200 and IR-500 trains by 22 Jan 2027, then on every Wave 1 train. It checks what good teams already produce; the friction falls on releases without evidence.
18. **Do the open-source projects we use now have to comply?** No. We are responsible for every component we ship, open source included. From 11 Dec 2027 we must report vulnerabilities we find to the projects’ maintainers and share our fixes; we will not push compliance demands onto them.

### Talking about it

19. **What training do I need?** It depends on your role and takes place in working time, from two hours for sales and support to a full day for PSIRT. So far 140 of 920 engineers have completed it; the target is 60% by March 2027. Book at \[link\].
20. **What can I say to customers, friends or on social media?** Use the customer FAQ. Say ‘we are preparing every product family to meet the CRA by 11 Dec 2027’. Never say ‘CRA certified’ or ‘fully compliant’, never share details of an unfixed vulnerability, and pass any security report to PSIRT within the hour.

## Customer FAQ

- **Owner:** Head of customer operations, with the compliance lead for accuracy
- **Approver:** General Counsel and executive sponsor (external, and states compliance status)
- **Publish:** trust page and support knowledge base, Tue 8 Dec 2026; reviewed monthly and whenever a declaration is published

### The Act and our position

1. **What is the EU Cyber Resilience Act?** An EU regulation (Regulation (EU) 2024/2847) that sets cybersecurity requirements for hardware and software products sold in the EU and brings them under CE marking. It entered into force on 10 Dec 2024.
2. **When does it apply?** Reporting of actively exploited vulnerabilities and severe incidents has applied since 11 Sep 2026. All other requirements apply from 11 Dec 2027.
3. **Do Example Group products comply with the CRA?** The product requirements apply from 11 Dec 2027, and we are preparing every product family to meet them by then. Each product will carry an EU declaration of conformity and CE marking under the CRA, published at \[trust page\] on a timetable we will share. For the duty that already applies, we are registered to report to EU authorities as the law has required since 11 Sep 2026.
4. **Are your products ‘CRA certified’?** There is no general CRA certificate. Under the Act the manufacturer declares conformity in an EU declaration of conformity and affixes CE marking. For the product categories the Act lists as important, an independent notified body first assesses the product or the manufacturer’s quality system.
5. **Which of your products need a notified body?** Those in categories the Act lists as important, such as our industrial routers and switches, firewall, remote-access VPN, device-management software, smart lock and video doorbell. We engaged candidate notified bodies early; EU Member States are still designating them.

### Updates and support

6. **How long will you provide security updates for my product?** For the support period we declare for each product: at least five years unless the product is expected to be used for less, and longer where customers reasonably expect it. From 11 Dec 2027 the end month and year is shown at the time of purchase. Our planned support periods are published at \[trust page\].
7. **Will security updates be free?** Yes. From 11 Dec 2027 the CRA requires security updates to be free of charge, accompanied by advisory information, unless otherwise agreed for a tailor-made product.
8. **Will updates install automatically?** For consumer products, security updates install automatically by default \[from date or version\], and you can switch this off in \[settings\]. For business products, \[describe how customers schedule or approve updates\].
9. **Can I get a software bill of materials (SBOM)?** We keep an SBOM for every release in our technical documentation; the Act does not require it to be published. Business customers can request it under \[terms\] at \[address\].

### Vulnerabilities and incidents

10. **How do I report a vulnerability in your products?** Through \[security page\] or \[PSIRT email\]. Our coordinated vulnerability disclosure policy at \[link\] explains what happens next; we acknowledge reports within \[5\] working days.
11. **How will you tell me about vulnerabilities and incidents?** We notify affected customers directly and without undue delay, with the steps to take, and we publish advisories in human-readable form and as machine-readable CSAF documents at \[advisory page\]. While no fix exists, we may share details only with affected customers, and publish more widely once a fix or mitigation is available.
12. **Do you report vulnerabilities to the authorities?** Yes, whenever the law requires: actively exploited vulnerabilities and severe incidents go to Germany’s coordinator CSIRT and ENISA within 24 hours of our becoming aware. If your products are affected, we tell you directly.

### Evidence for your own obligations

13. **Will you provide EU declarations of conformity?** Yes: one for each product, before 11 Dec 2027, at \[trust page\]. Each names the product and the versions it covers.
14. **We are subject to NIS2 or DORA. What can you provide for our supply-chain assessment?** Our declared support periods, vulnerability disclosure policy and contact, security advisories (including CSAF), the SBOM on request, and declarations of conformity once signed. Send questionnaires to \[address\]; we answer from our published material.
15. **What about products I bought before 11 Dec 2027?** They remain supported on the terms stated for each product, and our reporting duty already covers them. The Act’s design requirements apply to products placed on the market from 11 Dec 2027, so products you already own do not need to be modified because of it.

Source: knowledge base (Executive summary, Reporting obligations, Annex I Part II, Conformity), facts as at 30 Oct 2026; Illustrative

*Project Rampart · Communication Pack (D05) · Illustrative · v1.0 · 31 Oct 2026*
