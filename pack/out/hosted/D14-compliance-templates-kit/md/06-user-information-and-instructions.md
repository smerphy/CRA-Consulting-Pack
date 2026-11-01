# 6 · User information and instructions

The user information document carries the security facts a user needs to buy, commission, run and retire the product safely. Art 13(18) and Annex II require the listed information to accompany every product "at minimum" (Annex II), "in paper or electronic form" (Art 13(18)). Write one versioned document per product or family, publish it at a stable URL, and file a copy in the technical documentation (Annex VII pt 1).

## At a glance

| Item | Detail |
| --- | --- |
| Legal basis | Art 13(18); Annex II pts 1-9; Art 13(16) (manufacturer contact), 13(17) (single point of contact), 13(19) (end date at purchase), 13(11) (archive warnings) |
| Needed for | Every product with digital elements, whatever its class. No Commission or ENISA template exists |
| Owner | Technical writing lead, with the product security officer |
| Approver | Compliance lead |
| When to create | Before placing on the market; freeze the text per version at the release gate |
| When to update | Each new version or substantial modification; any change of contact, support end date, update method or decommissioning steps. Publish a new version page and keep the old one |
| Retention | Available for 10 years or the support period, whichever is longer; information provided online stays online (Art 13(18)) |
| Feeds | Template 4, Annex VII pt 1; Template 5, Annex II pt 6 carries the declaration address; Template 7, pt 2 carries the CVD contact; Template 3, pt 7 carries the end date; Template 8, user-notice channels |

## How to complete

1. Pull intended purpose, foreseeable misuse and residual risks from the product definition record and Template 2.
2. Take the support end month and year that applies to each version from Template 3, and the contact and policy URL from Template 7.
3. Fill one row per Annex II point below. Write concrete steps, not disclaimers.
4. Publish at a versioned URL such as `/security/<product>/<version>/` with a `latest` alias. Never delete a version page while its retention runs.
5. Place each item where the table says: manual, website, packaging, product label or app.
6. Check the text against the shipped behaviour, especially the automatic-update opt-out (pt 8(e)).
7. Use language easily understood by users and by market surveillance authorities in the Member States of sale.

## Template

| Annex II point | What to write | Where it appears | Example: L2 Smart Lock (illustrative) |
| --- | --- | --- | --- |
| 1. Manufacturer | Manufacturer name; postal address; email or other digital contact; website where available. Art 13(16) also requires identity and contact on the product, packaging or accompanying document | Product label or packaging; manual; website | Example Group \[legal entity\], Home & Building Solutions, \[street\], \[postcode\] \[city\], Germany; support@example.com; www.example.com |
| 2. Vulnerability contact | Single point of contact for vulnerability reports and where the CVD policy is found. Same contact as security.txt. Not limited to automated tools (Art 13(17)) | Manual; website; app (Settings > About) | psirt@example.com; web form www.example.com/security/report; phone \[+49 number\], staffed \[hours\]. Policy: www.example.com/security/cvd-policy |
| 3. Product identification | Name, type and information enabling unique identification | Product label; packaging; manual; app | L2 Smart Lock, type L2, SKUs L2-STD, L2-KEY, L2-RTF; serial on rear plate; firmware version in app (Settings > About) |
| 4. Intended purpose and security | Intended purpose; the security environment the manufacturer assumes; essential functionalities; security properties | Manual; website | Residential front-door lock for consumers. Assumes a home Wi-Fi network, a supported smartphone and the Example Group access-management cloud. Functions: lock, unlock, app keys, guest access, access log. Properties: per-device credentials, signed firmware, encrypted app and cloud traffic |
| 5. Use and misuse risks | Known or foreseeable circumstances of use or misuse that may lead to significant cybersecurity risks, each with the compensating measure | Manual; website | Guest keys shared without an expiry date: set an end date for every guest key. Phone with an outdated operating system: keep the phone updated. Automatic updates turned off: unpatched locks can be opened by known attacks |
| 6. Declaration address | Internet address of the EU declaration of conformity, where applicable | Manual; packaging (with Annex VI text); website | www.example.com/security/l2/declaration/ |
| 7. Support type and end date | Type of technical security support and the end date of the support period. Art 13(19) requires at least the month and year at the time of purchase | Packaging; point of sale and web shop; manual; website; app | Free security updates installed automatically over the air until \[month year\] (10-year support period from first placing) |
| 8(a). Secure use | Measures at initial commissioning and throughout the lifetime | Quick-start guide; manual; app onboarding | Install the latest firmware during set-up; set the owner account with two-step sign-in; review the access log monthly; revoke unused keys |
| 8(b). Changes and data security | How changes to the product can affect the security of data | Manual; website | Linking a third-party smart home bridge or adding users widens who can unlock. A factory reset removes all keys and pairings |
| 8(c). Installing updates | How security-relevant updates can be installed | Manual; app; website | Updates install automatically overnight. Manual check: app > Settings > Firmware > Check now |
| 8(d). Decommissioning | Secure decommissioning, including secure removal of user data | Manual; website; app | Remove the lock from your account in the app, then hold the reset button for \[10\] seconds. This erases keys, logs and the cloud binding |
| 8(e). Turning off automatic updates | How to turn off default automatic installation of security updates (Annex I Part I pt 2(c)), with the risk of doing so | Manual; app; website | App > Settings > Updates > Automatic security updates: Off. Postpone allows up to \[n\] days. Without updates the lock stays exposed to fixed vulnerabilities |
| 8(f). Integration | For products intended for integration: what integrators need to meet Annex I and Annex VII | Integrator guide; website | Not applicable: L2 is a finished product. If \[the integration API\] is offered to integrators, document it here |
| 9. SBOM access | Where users can access the SBOM. Optional: include only if the manufacturer chooses to offer it | Website, if offered | Not offered to users. The SBOM is held in the technical file for market surveillance requests (Annex VII pt 8) |

### Publication checklist

| Item | Rule | Basis |
| --- | --- | --- |
| Form | Paper or electronic; a versioned documentation URL satisfies it | Art 13(18) |
| Availability | 10 years or the support period, whichever is longer; online copies kept online | Art 13(18) |
| End date at purchase | At least the month and year, on the product, packaging or digitally at the time of purchase; end-of-support notice in the product where feasible | Art 13(19) |
| Archive warnings | Public archives of old versions only with clear risk warnings | Art 13(11) |
| One page | The versioned security page can host the CE marking for software, the declaration, the advisory index and archive warnings | Art 30(1); Annex VI; Annex II |

## Common mistakes

- Point 5 written as a disclaimer. Write concrete conditions and compensating measures, carried over from residual risks in the risk assessment.
- A point 2 contact that differs from security.txt, or a chatbot as the only channel (Art 13(17)).
- No end month and year at the point of sale, or, for software, no record of which declared end date applies to each version (Art 13(19)).
- Point 8(e) text that does not match the real opt-out, postponement and notification behaviour.
- A logging opt-out that silently disables security events without saying so in the user information.

*Template 6 · v1.0 · 31 Oct 2026 · Not legal advice; confirm wording against the Official Journal text before use.*
