# 1 · Product classification record

The product classification record fixes one product's boundary, its single core functionality and its class under Art 7, Art 8, Annex III and Annex IV. The class decides the Art 32 conformity route and whether a notified body is needed. Complete it at design stage, keep it at SKU level and file it in the technical documentation under Annex VII pt 1 (guidance para 144).

The companion interactive tool, CRA Product Classifier (D13), walks the same steps and produces a record in the same shape. Paste its output into this template and add the sign-off.

## At a glance

| Item | Detail |
| --- | --- |
| Legal basis | Art 2(1)-(7); Art 7(1)-(2); Art 8; Annex III; Annex IV; Implementing Regulation (EU) 2025/2392; Art 32 |
| Needed for | Choosing the Art 32 route; stating the core functionality (guidance para 144), recorded in the Annex VII pt 1 general description |
| Owner | Product security officer |
| Approver | Product owner and legal counsel |
| When to create | At concept or design gate, before the risk assessment and before booking a notified body |
| When to update | On any re-run trigger listed in the template |
| Retention | With the technical documentation: 10 years after placing or the support period, whichever is longer (Art 13(13)) |
| Feeds | Template 2 (intended purpose); Template 4 (Annex VII pt 1); Template 5 (Annex V pt 7 notified body); Template 10 (re-run on modification) |

## How to complete

1. Fix the product boundary: hardware, the software needed to use it, and manufacturer-built remote data processing. List separately sold modules as their own products.
2. Write one sentence of core functionality from the instructions, marketing and technical documentation.
3. Run the three Art 2(1) scope conditions, then check each exclusion in Art 2(2)-(7).
4. Compare the core functionality with the 26 technical descriptions in Implementing Regulation 2025/2392. For chips, use the designed AVA\_VAN level.
5. Apply the integration and ancillary rules, then the FOSS and AI overlays.
6. Record the result, route and notified-body need. Enter each SKU in the register below and obtain sign-off.

## Template

| Field | What to enter | Basis | Example: L2 Smart Lock (illustrative) |
| --- | --- | --- | --- |
| Record ID and version | \[CR-ID\], \[version\], \[date\] | Annex VII pt 1 | CR-L2-01 v1.0, 31 Oct 2026 |
| Product name and identifiers | \[Commercial name\], \[model\], \[SKU list\], \[type or serial scheme\] | Art 13(15) | L2 Smart Lock; 3 SKUs (see register); Home & Building Solutions |
| Boundary: hardware | \[Physical units and interfaces\] | Art 3(1), (5) | Lock body, motor, keypad, BLE and Wi-Fi radio |
| Boundary: software | \[Firmware, apps, drivers needed to use the product\] | Art 3(1); guidance para 25 | Lock firmware; iOS and Android companion app |
| Boundary: RDPS | \[Manufacturer-built backend functions the product cannot perform without\] | Art 3(2); guidance paras 184-196 | Access-management cloud: app keys, guest access, access-log sync |
| Third-party services | \[Licensed services treated as components\] | Art 13(5); guidance paras 197-202 | \[None recorded\] |
| Separately sold modules | \[Each module sold or licensed separately, with its own record\] | Guidance para 145, Example 61 | None; each SKU is a complete lock |
| Core functionality | \[One sentence; one core functionality only\] | Guidance paras 139, 144; recorded in the Annex VII pt 1 general description | Controls locking and unlocking of a residential door to protect physical access to the home |
| Intended purpose and foreseeable use | \[Purpose, users, environment, foreseeable use and misuse\] | Art 3(23)-(24) | Consumer homes; owner issues app keys and time-limited guest access; foreseeable use on small-office doors |
| Scope 1: product with digital elements | \[Yes or no, with reason\] | Art 2(1); Art 3(1) | Yes: hardware with firmware and an app |
| Scope 2: made available in a commercial activity | \[Yes or no, with reason\] | Art 2(1); Art 3(22) | Yes: sold at retail across the EU |
| Scope 3: data connection | \[Direct or indirect, logical or physical\] | Art 2(1); guidance paras 26-28 | Yes: BLE to the app; Wi-Fi to the cloud |
| Exclusions | \[Check medical (2(2)(a)-(b)), vehicles (2(2)(c), 2(5)), aviation (2(3)), marine (2(4)), spare parts (2(6)), defence (2(7))\] | Art 2(2)-(7); Delegated Regulation (EU) 2025/1535 | None applies |
| Category match | \[Annex III or IV item, or "default"; quote the matching description\] | Art 7(1); Implementing Regulation 2025/2392 | Annex III Class I item 17: smart home products with security functionalities, including smart door locks |
| Chip AVA\_VAN level | \[Designed level; chips only\] | Implementing Regulation 2025/2392; Annex III Class II items 3-4; Annex IV item 3 | Not applicable: not a chip product |
| Integration rule | \[Embedded important components; confirm host classified on its own core\] | Art 7(1); guidance Example 58 | MCU with secure boot is a component; it does not set the lock's class |
| Ancillary rule | \[Extra features that do not change the core\] | Implementing Regulation recitals; guidance Examples 59-60 | Auto-lock, activity log and battery alerts are ancillary |
| FOSS overlay | \[Is the product itself FOSS with public Annex VII documentation?\] | Art 32(5) | No: proprietary product with FOSS components |
| AI overlay | \[Is it a high-risk AI system?\] | Art 12; AI Act Art 6 | No |
| Result | \[Default / Class I / Class II / Critical\] | Art 7; Art 8 | Important, Class I |
| Route | \[Module A / B+C / H / certificate\] | Art 32; Annex VIII | Module B+C (planned); Module A closed because no harmonised standard is cited (Art 32(2)) |
| Notified body needed | \[Yes or no; candidate bodies\] | Art 32(2)-(4) | Yes; none designated at checks to 8 Sep 2026; three candidates shortlisted |
| Evidence consulted | \[Documents read, with versions\] | Guidance paras 142-143 | Product specification \[v\], user manual draft \[v\], retail listing copy, architecture document \[v\] |
| Rationale | \[Why the core matches, exceeds or falls short of the description\] | Annex VII pt 1 | Core purpose is physical access protection in homes, which item 17 names expressly |
| Re-run triggers | \[Events that reopen this record\] | Classification procedure step 8 | New variant or backend; modules sold separately; substantial modification; Art 7(3) act; OJ citation of a standard |
| Sign-off | \[Name, role, date\] for product owner, product security officer, legal | Governance | \[Name\], Product owner, \[date\]; \[Name\], Product security officer, \[date\]; \[Name\], Legal, \[date\] |

### SKU register

| SKU | Family | Core functionality | Class / category | Route | Rationale ref | Date | Owner |
| --- | --- | --- | --- | --- | --- | --- | --- |
| L2-STD (illustrative) | L2 Smart Lock | Residential door lock control | Class I, Annex III item 17 | Module B+C | CR-L2-01 | 31 Oct 2026 | Product security officer |
| L2-KEY (illustrative) | L2 Smart Lock | Residential door lock control | Class I, Annex III item 17 | Module B+C | CR-L2-01 | 31 Oct 2026 | Product security officer |
| L2-RTF (illustrative) | L2 Smart Lock | Residential door lock control | Class I, Annex III item 17 | Module B+C | CR-L2-01 | 31 Oct 2026 | Product security officer |
| \[SKU\] | \[Family\] | \[Core functionality\] | \[Class / item or default\] | \[Route\] | \[CR-ID\] | \[Date\] | \[Role\] |

Status at 30 Oct 2026: no harmonised standard is cited in the OJ, no Art 7(3) act amends Annex III, and no CRA notified body was found at checks to 8 Sep 2026. Guidance C(2026) 5252 is an approved draft, not yet formally adopted.

## Common mistakes

- Classifying from the marketing description. The test is objective (guidance para 142), and inconsistent documents indicate misrepresentation (para 143).
- Naming two core functionalities. A product has one for classification, and the technical documentation must state it (para 144).
- Treating an embedded important component as reclassifying the host, or an ancillary feature as declassifying it (Art 7(1); Examples 58-60).
- Keeping the register at family level when modules are sold separately. Each separately sold module is its own product (para 145).
- Assuming Module A for Class I. Art 32(2) needs a cited standard applied in full, and the wrong route can attract fines under Art 64(3) (para 146).

*Template 1 · v1.0 · 31 Oct 2026 · Not legal advice; confirm wording against the Official Journal text before use.*
