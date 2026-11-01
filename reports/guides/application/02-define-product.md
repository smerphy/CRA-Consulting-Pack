## 2. Define the product

Every later artefact depends on an agreed product boundary, so fix it first and write it down. The boundary decides what the risk assessment covers and what the SBOM lists. It also decides which backend the declaration speaks for and whether one file can serve several variants.

Early adopters report inventories growing five-fold once versions, apps and cloud pieces are counted ([OmniTrust](https://omnitrust.com/blog/eu-cra-tales-from-the-trenches-2-the-first-problem-isnt-security-its-scope/), consultancy).

The legal tests are in Scope: what the CRA covers and Product classification. This section turns them into a procedure and a record.

### Step 1: list the elements

Start from what the user receives and what it talks to. Include hardware, firmware, embedded operating system, host software, drivers, companion mobile and desktop apps, browser front-ends, cloud services and third-party services. For each element record who develops it, who operates it and which product functions depend on it.

Software needed to use the hardware is part of the product even when downloaded later from an app store. Guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) para 25 and Examples 8 and 9 make a printer and its drivers, or a wearable and its app, one product. Software the product merely redirects to, such as an informational website, is not (para 194).

### Step 2: apply the remote-data-processing test

A backend element is remote data processing (RDPS), and therefore part of the product, when three elements hold together (paras 184-188). Elements (ii) and (iii) are "decisive and cumulative".

1. The processing happens at a distance, which includes edge, on-premises and private-cloud deployments as much as public cloud.
2. Without it the product cannot perform one of its functions. "Functions" is wider than core functionality: sending commands, synchronising files, onboarding, configuration, identity and access management, and automated update distribution all count (paras 189-192). A function offered both remotely and manually still counts.
3. The software was designed and developed by the manufacturer or built solely for it to its specifications (paras 195-196). Licensing an existing third-party service, even slightly modified, fails this element; who operates it is "not a decisive factor".

The guidance examples anchor the boundary. For a mobile banking app, the bank's own API is RDPS; the ledger systems the app never talks to are not (section 8.3, para 205). An authentication portal issuing the tokens the product needs is RDPS; an informational website is not (para 194).

A smart thermostat's manufacturer-built cloud functions on third-party IaaS are RDPS (section 8.3).

Third-party SaaS integrated into the product, such as a support-chat widget or a generic storage service, is not RDPS. Treat it as a component under Art 13(5) due diligence with product-level mitigations (paras 197-202).

Telemetry analysed purely for statistics or future development is not RDPS (para 192). The data still counts for Annex I Part I item 2(g).

Write the result as a remote-function map: function, dependent service, developer, operator, local fallback behaviour, RDPS yes or no. Draft [ETSI EN 304 621](https://labs.etsi.org/rep/stan4cra/en-304-621/-/raw/main/EN-304-621.md) MAS_TECH-2 (draft) adds that the product must not connect to undocumented remote services, so the map must be complete.

### Step 3: decide variants and families

Variants sharing architecture, security-relevant design, intended purpose and risks may share one risk assessment, one technical file and one declaration (guidance paras 174-177). The declaration must list the variants. Differences in interfaces, software stacks, update mechanisms or remote connectivity must be reflected, and usually split the family.

Modules sold or licensed separately are separate products (para 145).

Record a family only when an engineer can name the shared security architecture document. A shared brand is not a family.

### Step 4: write the intended-purpose statement

Intended purpose drives the risk assessment (Art 13(3)), the Annex II document (point 4) and classification. Write one paragraph covering what the product does, for whom, in what environment, with what connectivity and for how long. Add a foreseeable-use list, including misuse the design should tolerate, and the security environment the user is assumed to provide.

Where the product is tailor-made for one business user, record the contract clause that varies secure-by-default or free updates. The [Commission FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307) section 4.2 limits the carve-out to those two items. Minor customisation of a multi-tenant product does not qualify.

### Step 5: name the core functionality and classify

State the single core functionality, then compare it against the technical descriptions in [Implementing Regulation (EU) 2025/2392](https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32025R2392). Follow the eight-step self-classification procedure in Product classification; ignore embedded important components and ancillary functions, and classify from documentation and behaviour rather than marketing. Record "default", Class I, Class II or critical with the rationale and evidence consulted.

### Step 6: select the route

Default products use Module A. Class I products cannot use Module A until a cited harmonised standard, common specification or "substantial" EU certification scheme can be applied in full (Art 32(2)), so plan for Module B+C or H and pre-contract candidate bodies. Class II and critical products need a notified body now.

A FOSS product in Annex III may use Module A if the technical file is published (Art 32(5)). The route table is in Conformity assessment and documentation; the preparation steps are in section 12.

### Step 7: apply the per-version placing rule

For standalone software, every copy of a version is deemed placed on the market at its first offering (guidance paras 11-16, Example 1). Each substantially modified version is a new placing with its own declaration and declared support period. Non-substantial updates do not reset the date (Example 2), so the release process must record which releases cross the security-delta threshold (section 5).

For hardware with software, placing happens unit by unit when the hardware ships (para 25). Companion software released later is placed when the units are. Record both rules in the definition record so release engineering applies the right one.

### Output: the product definition record

| Field | Content | Source |
|---|---|---|
| Product name and identifiers | Commercial name, model, SKU list, type or serial scheme (Art 13(15)) | Product management |
| Elements in the boundary | Hardware, firmware, host software, apps, RDPS modules and interfaces | Step 1 |
| Remote-function map | Function, service, developer, operator, fallback, RDPS decision | Step 2 |
| Third-party services as components | Service, provider, function served, due-diligence owner | Step 2 |
| Family and variants | Variant list, shared architecture document, differences recorded | Step 3 |
| Intended purpose and foreseeable use | One paragraph plus misuse list and assumed security environment | Step 4 |
| Expected time in use and support period | Years, rationale, end month and year per variant and version (Art 13(8), (19)) | Product management |
| Core functionality and class | Statement, Implementing Regulation category or "default", rationale | Step 5 |
| Conformity route | Module A, B+C, H or certificate; candidate bodies if needed | Step 6 |
| Placing rule | Per-version software or per-unit hardware; substantial-modification trigger owner | Step 7 |
| Economic-operator roles | Manufacturer, importer, distributor, authorised representative per market | Who the CRA regulates |
| Legacy status | Placed before 11 Dec 2027 yes or no; Art 69(2)-(3) consequences | Transition |
| Tailor-made terms | Contract reference for any 2(b) or Part II(8) variation, else "none" | Step 4 |
| Review triggers | New variant, new backend, new sales model, substantial modification | Classification procedure step 8 |
| Approvals | Product owner, product security, legal; date; version of this record | Governance |

Keep the record under version control beside the technical file. It is the first entry in the Requirement checklists tab, checklist 1 scope gate, and it feeds checklist 10 transition.
