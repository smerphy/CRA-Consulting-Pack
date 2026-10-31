# 3 · Support period determination

The support period determination records how long the manufacturer will handle vulnerabilities for a product, and why. Art 13(8) requires at least five years unless the product is expected to be in use for less, and Annex VII pt 4 requires the information used to set it. Complete it before placing on the market and file it with the technical documentation.

## At a glance

| Item | Detail |
| --- | --- |
| Legal basis | Art 13(8); Art 13(9)-(11); Art 13(19); Annex VII pt 4; Annex II pt 7 |
| Needed for | Annex VII pt 4; the end date shown at purchase; the period over which Annex I Part II applies |
| Owner | Product manager |
| Approver | Compliance lead, with legal counsel |
| When to create | At design, once intended purpose and expected time in use are agreed (Template 1, Template 2) |
| When to update | For each new variant and each substantially modified version; when expected-use evidence changes |
| Retention | 10 years after placing or the support period, whichever is longer (Art 13(13)) |
| Feeds | Template 4 (Annex VII pt 4); Template 6 (Annex II pt 7 end date); Template 2 (expected time in use); Template 9 (supplier support commitments) |

## How to complete

1. State the expected time in use from Template 1 and Template 2.
2. Gather evidence for each Art 13(8) factor and enter it in the evidence table.
3. Set the period. Treat five years as a floor, not a default (guidance paras 125-128).
4. Convert the period to an end month and year per variant and, for software, per version.
5. Record how the end date is shown at purchase and how users are told when support ends.
6. Enter each version in the version-support register and obtain sign-off.

## Template

### Part A: determination

| Field | What to enter | Basis | Example: L2 Smart Lock (illustrative) |
| --- | --- | --- | --- |
| Determination ID and version | \[SP-ID\], \[version\], \[date\] | Annex VII pt 4 | SP-L2-01 v1.0, 31 Oct 2026 |
| Product and variants | \[Family, variants, SKUs; Template 1 reference\] | Art 13(8) | L2 Smart Lock, 3 SKUs; CR-L2-01 |
| Expected time in use | \[Years and the reason\] | Art 13(8) | 10 years: a door lock stays fitted until the door or owner changes |
| Reasonable user expectations | \[What buyers expect, with evidence\] | Art 13(8) | Buyers expect a lock to outlast a phone; see evidence table |
| Nature of the product | \[Hardware, software or both; long-lived category?\] | Art 13(8); recital 60 | Hardware with firmware, app and cloud; physical security function |
| Relevant Union law | \[Other acts setting lifetimes or duties\] | Art 13(8) | \[None identified\] |
| Shorter than five years? | \[Only if expected use is shorter; give the evidence\] | Art 13(8) | No |
| Declared support period | \[Years\] | Art 13(8) | 10 years |
| End month and year | \[Per variant, or per batch for hardware placed unit by unit\] | Art 13(19); Annex II pt 7 | First batch placed under the CRA \[Dec 2027\]: end \[Dec 2037\] |
| Update availability | \[Each update kept available 10 years or the rest of the period, whichever is longer\] | Art 13(9) | Signed-artefact repository budgeted for 10 years after last release |
| Latest-version-only patching | \[Yes or no; free upgrade path without added hardware or software cost\] | Art 13(10) | No; all firmware versions in support receive fixes |
| Archives of old versions | \[Public archive with risk warnings, if offered\] | Art 13(11) | Archive page with warning text |
| Sign-off | \[Name\], \[role\], \[date\] | Governance | \[Name\], Product manager; \[Name\], Compliance lead |

The order of the Art 13(8) factors follows the Commission FAQ and is not verified against the OJ text. No delegated act on minimum periods exists as of 30 Oct 2026.

### Part B: expected-use evidence

| Evidence source | What it shows | Factor | Example: L2 Smart Lock (illustrative) |
| --- | --- | --- | --- |
| Installed-base and field data | Age of units still connected | Expected time in use | \[% of earlier-generation locks active after 7 years\] |
| Warranty, returns and replacement data | When users replace the product | Expected time in use | \[Median replacement age\] |
| Comparable products | Periods declared for similar products | Reasonable user expectations | \[Competitor periods, with source\] |
| Customer research and complaints | What buyers assume about support | Reasonable user expectations | \[Survey reference\] |
| Product category | Whether the category is typically used for longer | Nature of the product; recital 60 | Long-lived home hardware |
| Supplier support commitments | Whether chipset, OS and library support covers the period | Feasibility | \[BLE stack and MCU vendor commitments; Template 9\] |
| Other Union law | Lifetimes or duties set elsewhere | Relevant Union law | \[None identified\] |

### Part C: decision and publication

| Field | What to enter | Basis |
| --- | --- | --- |
| Where shown at purchase | \[Product, packaging or digital means; retail listing\] | Art 13(19) |
| Annex II entry | \[Annex II pt 7 text and URL; Template 6\] | Annex II pt 7 |
| End-of-support notice | \[In-product or in-app notice where technically feasible; content: date, risk of continued use, upgrade path\] | Art 13(19) |
| Annex VII filing | \[Location of this record in the technical documentation; Template 4\] | Annex VII pt 4 |

### Part D: version-support register

Each substantially modified version carries its own declared period. A modification does not reset or extend an existing period (guidance paras 132-135). For standalone software, every version is placed at its first offering.

| Version | Placing date | Declared end (month, year) | Shown at purchase | Update channel | Migration path | Legacy-version owner |
| --- | --- | --- | --- | --- | --- | --- |
| L2 firmware \[x.y\] (illustrative) | \[Dec 2027\] | \[Dec 2037\] | Packaging and app store listing | Automatic OTA | Free OTA to latest | Product manager, HBS |
| \[Version\] | \[Date\] | \[Month, year\] | \[Where\] | \[Channel\] | \[Path\] | \[Role\] |

## Common mistakes

- Declaring five years by default. It "operates only as a safeguard" and is not the default (guidance paras 125-128).
- No per-version declaration for software, so nobody knows which versions get fixes. Keep the version-support register.
- Showing a duration instead of an end date. Art 13(19) requires at least the month and the year at purchase.
- Assuming a substantial modification extends the period for earlier versions. It does not (paras 132-135).
- Setting a period that component suppliers cannot support. Secure supplier commitments first (Template 9).

*Template 3 · v1.0 · 31 Oct 2026 · Not legal advice; confirm wording against the Official Journal text before use.*
