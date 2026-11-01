## Annex I Part I: essential requirements for product properties

Annex I Part I of the [CRA](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) sets one absolute obligation, point (1), and thirteen risk-qualified requirements, points (2)(a) to (2)(m). All thirteen sit under one chapeau: "On the basis of the cybersecurity risk assessment referred to in Article 13(2) and where applicable". The Art 13(2)-(4) risk assessment therefore decides which items apply and must justify every item not applied.

Point (1) requires products designed, developed and produced to ensure "an appropriate level of cybersecurity based on the risks". Items (c) and (m) carry a second internal qualifier, and (b) a tailor-made carve-out.

The drafting bodies still treat (a), (b), (d) and (l) as near-universal. Draft [ETSI EN 304 621](https://labs.etsi.org/rep/stan4cra/en-304-621/-/raw/main/EN-304-621.md) applies access control at every risk tier and calls logging essential in every use case.

### Requirement-by-requirement reference

The mapping column cites these sources as the research notes give them:

- [JRC-ENISA standards mapping](https://www.enisa.europa.eu/sites/default/files/2024-11/Cyber%20Resilience%20Act%20Requirements%20Standards%20Mapping%20-%20final_with_identifiers_0.pdf), 4 Apr 2024
- [EN 18031-1:2024](https://www.nek.no/wp-content/uploads/2025/02/nek-en-18031-1_2024_en_001.pdf) control IDs and [ETSI EN 303 645 V3.1.3](https://www.etsi.org/deliver/etsi_en/303600_303699/303645/03.01.03_60/en_303645v030103p.pdf) provisions
- IEC 62443-4-2:2019 component requirements (CRs) and ISO/IEC 27002:2022
- [OWASP ISVS Appendix B](https://owasp.org/IoT-Security-Verification-Standard-ISVS/en/Appendix_B-Compliance_Mapping.html), a community crosswalk, and [NIST SP 800-213A](https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-213A.pdf) capabilities
- [ENISA Secure by Design and Default Playbook v1.0](https://www.enisa.europa.eu/sites/default/files/2026-07/ENISA_Secure_By_Design_and_Default_Playbook_v1.pdf), July 2026, principles 4.1-4.22
- Draft EN 304 621 (v1.0.4, 20 Jul 2026) and the CEN-CENELEC [EN 40000-1-4 slides](https://www.cencenelec.eu/media/CEN-CENELEC/Events/Webinars/2026/2026-03-05_cra_unlocked_pt2_stan4cr_slides.pdf) of 5 Mar 2026, both marked "draft"

Nothing marked draft is cited in the OJ as of 30 Oct 2026 (see Standards and guidance map).

| Item | What the law requires | Engineering controls | Technical-file evidence | Standards mapping |
|---|---|---|---|---|
| (1), absolute | Design, develop and produce to ensure "an appropriate level of cybersecurity based on the risks" (point 1) | Secure development lifecycle; threat modelling; risk treatment selecting (2)(a)-(m) controls; component due diligence | Art 13(3) risk assessment with per-item applicability; architecture diagrams; residual-risk register | EN 40000-1-2; BSI TR-03183-1 RH_RA, RH_RT; ISO/IEC 27002, 27005; IEC 62443-4-1; Playbook 4.1 |
| (2)(a) | Made available "without known exploitable vulnerabilities" (point 2(a)) | SBOM scanning against EUVD, CVE and KEV lists; SAST, fuzzing, pen test; fix or document before release; update at first use | Scan and pen-test reports; KEV list with fix status; release checklist | EN 304 621 cl 5.3 (draft); EN 40000-1-4 GEC-1 (draft); EN 303 645 5.2, 5.3; ISVS 1.2.3, 3.2.4; Playbook 4.9, 4.14 |
| (2)(b) | "Secure by default configuration", with a tailor-made carve-out, "including the possibility to reset the product to its original state" (point 2(b)) | No default credentials; per-device secrets; optional services off; debug interfaces disabled; enforced onboarding; factory reset to baseline | Default-configuration export; interface inventory; onboarding and reset tests | EN 304 621 cl 5.4 (draft); EN 40000-1-4 GEC-9/10/12 (draft); EN 18031-1 GEC, AUM; EN 303 645 5.1, 5.6; IEC 62443-4-2 CR 7.6, 7.7; ISVS 2.1.6, 5.1.5; Playbook 4.15-4.22 |
| (2)(c) | Updatable; "where applicable" automatic updates by default, with "a clear and easy-to-use opt-out mechanism", notification and postponement (point 2(c)) | Signature check before install; anti-rollback; recovery image; auto-install by default for consumer products, scheduling for managed estates; separate security train | Update design note; signature and rollback tests; default-config proof; opt-out UI evidence | EN 304 621 cl 5.5 (draft); EN 40000-1-4 SUM-1..4, UNM-4 (draft); EN 18031-1 SUM-1..3; EN 303 645 5.3; IEC 62443-4-2 EDR 3.10; NIST SU; ISVS 3.4; Playbook 4.20 |
| (2)(d) | Protection from unauthorised access by "authentication, identity or access management systems"; "report on possible unauthorised access" (point 2(d)) | Authentication on every interface; MFA for privileged roles; RBAC; lockout; expiring machine credentials; intrusion alerts | Access model; negative tests; audit-log samples; alert catalogue | EN 304 621 cl 5.6 (draft); EN 40000-1-4 ACM, AUM, GEC-13 (draft); EN 18031-1 ACM-1/2, AUM-1..6; EN 303 645 5.1, 5.5; IEC 62443-4-2 CR 1.1-1.14, 2.1; NIST LA; ISVS 2.1, 2.2; Playbook 4.3, 4.16 |
| (2)(e) | Confidentiality of stored, transmitted or processed data, "such as by encrypting relevant data at rest or in transit" (point 2(e)) | TLS 1.3 or equivalent; at-rest encryption with protected keys; approved algorithms; no plaintext fallback | Cryptographic inventory; downgrade tests; key-management design | EN 304 621 cl 5.7, Annex K (draft); EN 18031-1 SCM, SSM, CCK, CRY-1; EN 303 645 5.4, 5.5, 5.8; IEC 62443-4-2 CR 4.1, 4.3; NIST DP; ISVS 2.4, 3.5; Playbook 4.17 |
| (2)(f) | Integrity of data, "commands, programs and configuration"; "report on corruptions" (point 2(f)) | Verified boot and signed software; signed configuration; integrity monitoring; anti-tamper; W^X and CFI | Boot-chain tests; signature tests; corruption-detection test | EN 304 621 cl 5.8 (draft); EN 18031-1 SUM, SCM; EN 303 645 5.4, 5.7; IEC 62443-4-2 CR 3.1, 3.4, 3.8, EDR 3.11-3.14; ISVS 3.1; Playbook 4.11 |
| (2)(g) | Process only data "adequate, relevant and limited to what is necessary" (point 2(g)) | Per-function data inventory; telemetry off by default; defined retention; no personal data in logs | Data list for the default configuration; retention schedule | EN 304 621 cl 5.9 (draft); EN 40000-1-4 DTM-1..3 (draft); EN 18031-2; EN 303 645 5.8, cl 6; ISO/IEC 27701, 29100; ISVS 1.3.14; Playbook 4.2 |
| (2)(h) | Availability of "essential and basic functions, also after an incident", with DoS mitigation (point 2(h)) | Rate limiting; graceful degradation; watchdog; local operation without the backend; backup and failover | Essential-function list with mitigations; stress reports; recovery tests | EN 304 621 cl 5.10 (draft); EN 40000-1-4 RLM-1..6 (draft); EN 18031-1 RLM-1; EN 303 645 5.9; IEC 62443-4-2 CR 7.1-7.4; NIST DS:RSC; Playbook 4.5, 4.12 |
| (2)(i) | Minimise negative impact on services of other devices or networks (point 2(i)) | Documented emitters; egress control; no amplification; retry with back-off; no open relays | Emitter inventory; external port scans; amplification calculations | EN 304 621 cl 5.11 (draft); EN 40000-1-4 TCM-1, NMM-1, LIM-1/2 (draft); EN 18031-1 TCM-1, NMM-1; EN 303 645 5.6, 5.13; IEC 62443-4-2 CR 5.1, 5.2; JRC-ENISA: "minimal"; ISVS: none |
| (2)(j) | "Limit attack surfaces, including external interfaces" (point 2(j)) | Minimal services in every state; JTAG and debug ports disabled or protected; development tooling stripped; default deny | Interface inventory per state; port scans; hardware photographs; debug-lock evidence | EN 304 621 cl 5.12 (draft); EN 18031-1 GEC; EN 303 645 5.6; IEC 62443-4-2 CR 7.7, EDR 2.13; NIST DC:INT; ISVS 1.1.2, 1.2.4; Playbook 4.4 |
| (2)(k) | Reduce incident impact "using appropriate exploitation mitigation mechanisms and techniques" (point 2(k)) | Memory-safe languages or hardened builds (ASLR, W^X, CFI); sandboxing; privilege separation; input validation | Compiler-flag evidence; binary-hardening scan; fuzzing reports | EN 304 621 cl 5.13 (draft); IEC 62443-4-2 CR 3.5, 3.6, FR5; ISO/IEC 27034; NIST DS:EXE; ISVS 1.3.7-1.3.11; Playbook 4.5, 4.9 |
| (2)(l) | "Recording and monitoring relevant internal activity", including access to or modification of data, services or functions, "with an opt-out mechanism for the user" (point 2(l)) | Security event logging; structured fields; tamper-evident retention; SIEM export; user opt-out | Event catalogue; sample logs; opt-out evidence | EN 304 621 cl 5.14 (draft); EN 18031-1 NMM-1; EN 303 645 5.9-5.11; IEC 62443-4-2 CR 2.8-2.12, 6.1, 6.2; NIST CS; ISVS 1.4.1-1.4.7; Playbook 4.10 |
| (2)(m) | Users can "securely and easily remove on a permanent basis" all data and settings; secure transfer "where such data can be transferred" (point 2(m)) | Secure erase by overwrite or key destruction across storage, credentials and cloud bindings; authenticated export; ownership transfer | Write-erase-read test per data type; export test; Annex II point 8(d) text | EN 304 621 cl 5.15, transfer not required (draft); EN 40000-1-4 SO.FactoryReset (draft); EN 303 645 5.11; IEC 62443-4-2 CR 4.2; NIST EA:EOL; ISVS 1.4.6, 2.2.3; Playbook 4.7, 4.22 |

### Known exploitable vulnerabilities

No legal text defines "known exploitable vulnerability". Recital 54 makes avoiding such vulnerabilities the goal of the risk assessment. Recital 38 expects each product to have received "all security patches or updates available to address relevant security issues" when placed on the market.

The [Commission guidance C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) (paras 233-234) treats a vulnerability as known once it is in the EUVD or another prominent database. Private disclosure, internal testing and prominent media reporting also count.

Draft EN 304 621 clause 5.3 passes a product with no known exploitable vulnerabilities. It also passes one whose vulnerabilities were reported within 14 days or its CVD window, or carry a documented public mitigation.

Draft [ETSI EN 304 626](https://labs.etsi.org/rep/stan4cra/en-304-626/-/raw/main/EN-304-626.md) (operating systems, v0.0.11) tests "at first use" with five mitigations. Practical release gate: correlate the release SBOM with the EUVD, CVE/NVD and the CISA KEV catalogue. Apply every available patch, document a mitigation for anything unpatched, and test update at first use.

### The Art 13 risk assessment

Art 13(3) requires the assessment documented and "updated as appropriate during a support period". It rests on intended purpose, reasonably foreseeable use, conditions of use and expected time in use. It must state whether, how and with what implementation each Part I point (2) item applies.

Art 13(4) places it in the Annex VII technical documentation (point 3) with "a clear justification" for each item not applied. Recital 55 requires residual risk to be addressed by other means, such as limiting intended use or informing users.

Guidance paras 156-163 add that "internal risk tolerance, commercial strategy or mere cost considerations are not relevant". Risk cannot be shifted to users to cover design shortcomings.

Paras 174-177 allow one assessment, one documentation set and one declaration for a product family sharing architecture, security-relevant design, intended purpose and risks. Update triggers are security-relevant changes, new vulnerabilities, new threats and regular-test results (Art 13(7); Part II point 3); no source sets a cadence.

No methodology is mandated ([Commission FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307), section 4.1). [BSI TR-03183-1 v1.0.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-1_v1_0_0.pdf?__blob=publicationFile&v=3) offers a non-binding ISO 31000-style method and a section 4.8 report skeleton usable as the technical file.

### Special items

Point (2)(b) is a state requirement: the product ships secure and returns to that state on reset. The tailor-made carve-out needs a product fitted to a particular business user and terms both parties "explicitly agreed" (Recital 64; FAQ). A multi-tenant platform with minor customisation does not qualify, and draft EN 304 621 notes the carve-out does not remove the reset duty.

Point (2)(c) is a capability requirement. The matching process duties sit in Part II points 2, 7 and 8 (see Annex I Part II: vulnerability handling and lifecycle duties).

Recital 56 excuses products primarily intended as components and professional, critical or industrial environments where users would not expect automatic updates. Those products must still notify users and make updates available without delay.

Point (2)(l) requires a user opt-out from logging; no official text says how a component without a user interface provides one. Point (2)(m) requires permanent, easy removal of all data and settings, with secure transfer only where transfer is possible.

### Scope extensions

Remote data processing: Art 3(2) brings the manufacturer's own backend into the product where a product function depends on it (Recitals 11-12; guidance paras 184-205). The boundary test is in Scope: what the CRA covers. Annex I then applies at the product-to-cloud boundary.

Draft EN 304 621 [Annex R](https://labs.etsi.org/rep/stan4cra/en-304-621/-/raw/main/EN-304-621_AnnexR.md) applies clause 5 to the product as a whole and adds boundary requirements on both endpoints. The underlying third-party infrastructure stays outside.

Indirect connection: Recital 9 keeps in scope products connected only indirectly, logically or physically, including logical connection "via network sockets, pipes, files, application programming interfaces or any other types of software interface".

Components and microcontrollers: a separately sold MCU or module with a foreseeable data connection is a product with digital elements (see Product classification). Vendor papers from [TI (STDA050, Oct 2026)](https://www.ti.com/lit/pdf/STDA050) and [Microchip (DS00006536A, Aug 2026)](https://www.microchip.com/content/dam/mchp/documents/MCU32/ProductDocuments/SupportingCollateral/An-Embedded-Engineers-Guide-to-the-EU-Cyber-Resilience-Act-DS00006536.pdf) describe an integrator pattern.

The chip vendor documents silicon-level evidence and integration assumptions; the integrator owns defaults, reset, logging and the technical file. Both are vendor interpretations; draft EN 304 621 Annex K and EN 304 626 MI-PDDI-1 formalise the same split.

### Guidance state

C(2026) 5252 (approved 27 Jul 2026; formal adoption pending language versions) does not walk through Annex I items. The ENISA Playbook v1.0 (July 2026) gives 22 principles with minimum evidence and release gates. Its Annex B reproduces Annex I verbatim and Annex C maps principles to items indicatively.

BSI TR-03183-1 v1.0.0 (PDF dated 31 Jul 2026, announced 5 Aug 2026) carries no presumption of conformity. EN 40000-1-4, the horizontal standard for (2)(a)-(m), is due 30 Oct 2027 ([DKE project list, Oct 2026](https://www.dke.de/resource/blob/2435170/a4c8225091ac18023516487e3e55cb23/normungsprojekte-zum-cra-data.pdf)) and absorbed the discontinued TR 40000-1-5. ETSI's 17 final-draft EN 304 6xx verticals (Aug 2026) map clause 5.x one-to-one to (2)(a)-(m) in their Table A.1.
