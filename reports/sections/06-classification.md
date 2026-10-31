## Product classification

Twenty-six named categories decide the conformity route under the [CRA](https://eur-lex.europa.eu/eli/reg/2024/2847/oj). Annex III holds 19 Class I and 4 Class II "important" categories; Annex IV holds 3 "critical" categories. Everything else is a default product and may always self-assess under Module A.

[Commission Implementing Regulation (EU) 2025/2392](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32025R2392) of 28 Nov 2025, in force 21 Dec 2025, gives each category a technical description with non-exhaustive examples. A product is in a category when its core functionality matches that description (Art 7(1)).

Annex III categories meet one of two criteria in Art 7(2). Either the product "primarily performs functions critical to the cybersecurity of other products", or it can disrupt or damage many other products "through direct manipulation". Annex IV adds critical dependency of NIS2 essential entities, or supply-chain disruption potential (Art 8(2)).

The route pointers below reflect 30 Oct 2026. No harmonised standard is cited in the OJ, no Art 27(9) delegated act recognises a certification scheme, and no notified body is designated. The full route table is in Conformity assessment and documentation.

### Table A: Annex III Class I (19 categories)

| Annex III Class I category | Technical-description highlights from 2025/2392 | Typical products | Route pointer |
|---|---|---|---|
| 1. Identity management systems and privileged access management software and hardware, including authentication and access control readers, including biometric readers | Systems providing authentication or authorisation; privileged-access software; SSO, federated identity, OTP and MFA software; biometric readers | IdP and SSO platforms, PAM suites, MFA apps, badge and fingerprint readers | Module B+C or H until a cited standard allows Module A |
| 2. Standalone and embedded browsers | Software for accessing and rendering web content, including browsers with AI-agent integration | Desktop and mobile browsers, embedded webview engines | Module B+C or H until a cited standard allows Module A |
| 3. Password managers | Products storing passwords locally or remotely, including browser extensions and hardware-based managers | Password vault apps, browser extensions, hardware key stores | Module B+C or H until a cited standard allows Module A |
| 4. Software that searches for, removes, or quarantines malicious software | Detection, removal or quarantine of malicious code, including rootkit detection and rescue disks | Anti-malware, EDR agents, rescue media | Module B+C or H until a cited standard allows Module A |
| 5. Products with digital elements with the function of virtual private network (VPN) | Products creating encrypted logical tunnels: VPN clients, servers and gateways | VPN clients, concentrators, SD-WAN tunnel endpoints | Module B+C or H until a cited standard allows Module A |
| 6. Network management systems | Systems that monitor and configure network elements, including SDN controllers | NMS platforms, controllers, orchestration consoles | Module B+C or H until a cited standard allows Module A |
| 7. Security information and event management (SIEM) systems | Products that collect and correlate security data into actionable information | SIEM platforms; log tools without correlation fall short (guidance Example 60) | Module B+C or H until a cited standard allows Module A |
| 8. Boot managers | Software managing system start-up, including UEFI firmware and boot loaders | UEFI firmware, GRUB-type loaders, secure-boot chains | Module B+C or H until a cited standard allows Module A |
| 9. Public key infrastructure and digital certificate issuance software | Products managing certificates or cryptographic keys, including key management systems and OCSP responders | CA software, KMS, OCSP and CRL services | Module B+C or H until a cited standard allows Module A |
| 10. Physical and virtual network interfaces | Hardware or software connecting devices to networks: NICs, Wi-Fi, Bluetooth, virtual NICs, VPN interfaces | Network cards, radio modules, virtual switches and adapters | Module B+C or H until a cited standard allows Module A |
| 11. Operating systems | Software that abstracts hardware and manages execution, real-time and general-purpose | Desktop, server, mobile, embedded and real-time OS | Module B+C or H until a cited standard allows Module A |
| 12. Routers, modems intended for the connection to the internet, and switches | Routers select paths; modems convert signals; switches forward packets and have a management plane; access points acting as bridges included | Home and enterprise routers, DSL and fibre modems, managed switches, access points | Module B+C or H until a cited standard allows Module A |
| 13. Microprocessors with security-related functionalities | Central processing ICs that also provide security features such as encryption or secure boot | Application processors with crypto engines or secure boot | Module B+C or H until a cited standard allows Module A |
| 14. Microcontrollers with security-related functionalities | Programmable ICs with similar security features | MCUs with hardware crypto, secure boot or key storage | Module B+C or H until a cited standard allows Module A |
| 15. Application specific integrated circuits (ASIC) and field-programmable gate arrays (FPGA) with security-related functionalities | Custom or reprogrammable ICs with similar security features | Security ASICs, FPGAs with crypto or secure configuration | Module B+C or H until a cited standard allows Module A |
| 16. Smart home general purpose virtual assistants | Products processing natural-language requests and controlling connected home devices, including smart speakers with integrated assistants | Smart speakers, voice hubs | Module B+C or H until a cited standard allows Module A |
| 17. Smart home products with security functionalities, including smart door locks, security cameras, baby monitoring systems and alarm systems | Products protecting physical security in homes, including central control hardware and software | Smart locks, cameras, baby monitors, alarm panels and apps | Module B+C or H until a cited standard allows Module A |
| 18. Internet connected toys covered by Directive 2009/48/EC that have social interactive features (e.g. speaking or filming) or that have location tracking features | Toys with microphone, camera, speaker or location tracking; proximity sensing alone is not location tracking | Talking or filming connected toys, GPS-tracked toys | Module B+C or H until a cited standard allows Module A |
| 19. Personal wearable products to be worn or placed on a human body that have a health monitoring (such as tracking) purpose and to which Regulation (EU) 2017/745 or (EU) 2017/746 do not apply, or personal wearable products intended for the use by and for children | Health-monitoring wearables that are not medical devices; wearables for children under 14; fitness trackers and smartwatches | Fitness bands, smartwatches, children's wearables | Module B+C or H until a cited standard allows Module A |

### Table B: Annex III Class II (4 categories)

| Annex III Class II category | Technical-description highlights from 2025/2392 | Typical products | Route pointer |
|---|---|---|---|
| 1. Hypervisors and container runtime systems that support virtualised execution of operating systems and similar environments | Type 1, type 2 and hybrid hypervisors; container runtime systems | Bare-metal and hosted hypervisors, container runtimes | Module B+C or H; a "substantial" certificate once an Art 27(9) act names the scheme |
| 2. Firewalls, intrusion detection and prevention systems | Network and application firewalls including web application firewalls and anti-spam gateways; network- and host-based IDS and IPS | Next-generation firewalls, WAFs, IDS and IPS appliances and software | Module B+C or H; a "substantial" certificate once an Art 27(9) act names the scheme |
| 3. Tamper-resistant microprocessors | Class I.13 microprocessors with tamper features, designed to AVA_VAN level 2 or 3 | Hardened application processors | Module B+C or H; a "substantial" certificate once an Art 27(9) act names the scheme |
| 4. Tamper-resistant microcontrollers | Class I.14 microcontrollers with tamper features, designed to AVA_VAN level 2 or 3 | Hardened MCUs for payment, automotive or industrial use | Module B+C or H; a "substantial" certificate once an Art 27(9) act names the scheme |

### Table C: Annex IV critical (3 categories)

| Annex IV category | Technical-description highlights from 2025/2392 | Typical products | Route pointer |
|---|---|---|---|
| 1. Hardware Devices with Security Boxes | Multi-component hardware storing or processing sensitive data inside a tamper-protecting physical enclosure | Payment terminals, HSMs, tachographs | As Class II until an Art 8(1) delegated act mandates certification |
| 2. Smart meter gateways within smart metering systems as defined in Article 2, point (23) of Directive (EU) 2019/944 and other devices for advanced security purposes, including for secure cryptoprocessing | Gateways controlling smart-metering communication, handling encryption, firewalling and device control; electricity, and gas and heat where the description fits | Smart meter gateways, secure cryptoprocessing devices | As Class II until an Art 8(1) delegated act mandates certification |
| 3. Smartcards or similar devices, including secure elements | Secure elements are tamper-protected microcontrollers or microprocessors designed to at least AVA_VAN.4, including TPMs and embedded UICCs; smartcards are secure elements in card or other carrier form | Payment, ID and access cards, TPMs, eUICCs, tachograph cards | As Class II until an Art 8(1) delegated act mandates certification |

For hardware teams the Common Criteria vulnerability-assurance target is the discriminator. AVA_VAN 2-3 with tamper features puts a chip in Class II, and AVA_VAN.4 or higher makes it an Annex IV secure element. A chip with security functions below those levels is Class I.

[Guidance C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) para 146 notes that choosing the wrong Art 32 route can attract fines under Art 64(3). Draft vertical standards exist for most categories but none is cited; see Standards and guidance map.

### Core-functionality rules

Core functionality is the set of main features without which the product "would not be able to meet its intended purpose" (guidance para 139). It is read from instructions, marketing and technical documentation. The recitals of Implementing Regulation 2025/2392 and guidance section 6.1 fix five rules.

- One core functionality per product. A product "may not have more than one core functionality" for classification, and the technical documentation must identify it (para 144).
- Integration does not reclassify the host. Embedding an important or critical component does not make the host important or critical (Art 7(1)). A smartphone with an OS is not an OS (Example 58), but the host must still assess the integrated component's security.
- Ancillary functions do not declassify. An operating system with a calculator is still an OS; a router with firewall functions is still a router (Implementing Regulation recitals).
- A product that could perform a category's function but has a different core is not in the category. SOAR software exceeds SIEM and is not a SIEM (Example 59); log collection without correlation falls short (Example 60).
- Separately sold modules are separate products. Sold separately, a suite's SIEM module is Class I, its IDS module Class II and its analytics module default (para 145, Example 61). Supplied only as parts of one integrated product, they take the product's class.

The test is objective. Classification does not depend on "the way in which the product ... is described or marketed" (para 142). Inconsistency between marketing, instructions and technical documentation is an indicator of misrepresentation (para 143).

Packaging and licensing decisions therefore change classification. Keep the register at SKU level.

### Self-classification procedure

1. Fix the product boundary. One product means the hardware, the software needed to use it, and manufacturer-built remote data processing (see Scope: what the CRA covers). List modules sold or licensed separately as their own products.
2. State the single core functionality. Derive it from the intended purpose in instructions, marketing and the technical documentation, and write it into Annex VII item 1(a).
3. Compare against the 26 technical descriptions in Implementing Regulation 2025/2392 Annex I (Class I and II) and Annex II (critical). For chips, use the designed AVA_VAN level.
4. Apply the integration and ancillary rules. Ignore embedded important components and extra features; ask whether the product's own core matches, exceeds or falls short of the description.
5. Check the overlays. A FOSS product in an Annex III category may use any Art 32(1) route if its technical documentation is public (Art 32(5)). A high-risk AI system follows Art 12 (below).
6. Record the result. Enter the category or "default", the rationale and the evidence consulted in a SKU-level classification register, and keep it with the technical documentation.
7. Choose the route from the table in Conformity assessment and documentation. Book notified-body capacity early for Class I, Class II and critical products.
8. Re-run steps 1-7 on any substantial modification, new variant or change in how modules are sold.

### Status of the lists and the AI Act overlay

No Art 7(3) delegated act changing the Annex III lists has been adopted or put to consultation as of 30 Oct 2026. None under Art 8(1) makes certification mandatory for a critical category. The Commission told its Expert Group on 12 Feb 2025 that it "was not working on" such acts ([Expert Group minutes](https://ec.europa.eu/transparency/expert-groups-register/core/api/front/document/115256/download)).

A future Art 7(3) act must give at least 12 months' transition, and an Art 8(1) act at least 6 months, barring urgency. The Commission's [implementation factpage](https://digital-strategy.ec.europa.eu/en/factpages/cyber-resilience-act-implementation) lists only the planned Q4 2026 Art 27(9) delegated act recognising EUCC; see Open questions and watchlist.

High-risk AI systems that are products with digital elements get a deemed-compliance rule (CRA Art 12(1)). The product meets Annex I Part I, the processes meet Part II, and the EU declaration shows the AI Act Art 15 protection level. The product is then "deemed to comply" with AI Act Art 15 cybersecurity; [Regulation (EU) 2026/1744](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32026R1744) mirrors this in AI Act Art 42(3).

The AI Act Art 43 procedure then governs conformity assessment (Art 12(2)). The exception is an important or critical product under AI Act Annex VI internal control, which follows the CRA routes instead (Art 12(3)). No Commission guidance on sequencing the two assessments exists; CRA-AI Act interplay guidance is targeted for end-2026.
