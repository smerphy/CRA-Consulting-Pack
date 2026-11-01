# 10 · Substantial modification assessment

This record decides whether a change to a product already on the market is a substantial modification under Art 3(30). A positive decision makes the changed version a new placing on the market (guidance pt 116). Complete it at the release gate for every release, and file it with that release's technical documentation.

## At a glance

| Item | Detail |
| --- | --- |
| Legal basis | Art 3(30); guidance C(2026) 5252 pts 104-123; Annex VIII Module B pt 7 and Module H pt 3.5; FAQ 6.3 and 6.8; Art 69(2) |
| Needed for | Every release or change to a product already placed, including products placed before 11 Dec 2027 |
| Owner | Product security officer |
| Approver | Compliance lead; notified-body liaison where the route is Module B+C or H |
| When to create | At the release gate, before tagging the release |
| When to update | When the change scope grows before release, or when the notified body disagrees |
| Retention | 10 years after placing or the support period, whichever is longer (Art 13(13)) |
| Feeds | Template 1 (re-classification), Template 2 (risk delta), Template 3 (support period), Template 4 (file version), Template 5 (declaration), Template 6 (user information) |

## How to complete

1. Fill the change record header and link the change ticket and release.
2. Check the current risk assessment (Template 2). A change it already foresaw and assessed is not substantial.
3. Answer the four questions from guidance pt 110, each with evidence from the threat model delta.
4. Apply the decision logic. Send borderline cases to the compliance lead.
5. Run every action in the consequence table for your outcome.
6. Sign off and file the record with the release gate record.

## Template

### Change record header

| Field | What to enter | Basis | Example: L2 Smart Lock (illustrative) |
| --- | --- | --- | --- |
| Product and variants | Name, type and SKUs covered | Annex V pt 1 | L2 Smart Lock, 3 SKUs |
| Version on the market | Current version and first placing date | Art 3(21); guidance pts 13-15, Example 2 | Firmware 3.4, placed \[date\] |
| Proposed release | Version and planned release date | Annex VII pt 1 | Firmware 4.0, planned \[Q2 2028\] |
| Change summary | One line per change; ticket link | Art 13(7) | Remote unlock through the access-management cloud |
| Change type | Security update, functionality update, or both | Annex I Part II(2) | Functionality update |
| Separable? | Can the security fixes ship apart from the feature? | Annex I Part II(2) | Yes; 3.4.2 ships first |
| Conformity route and body | Module and notified body, with certificate ID | Art 32; Annex VIII | Module B+C; \[body, certificate ID\] |
| Legacy status | Placed before 11 Dec 2027? | Art 69(2) | Yes; 3.x units placed before that date |
| Risk assessment version | Version the test runs against | Annex VII pt 3; Template 2 | RA v2.3 |
| Assessor and date | Name, role, date | Art 13(7) | \[Name\], product security officer, \[date\] |

### Four-question test (guidance pt 110)

| # | Question | Answer (yes/no) | Evidence | Notes |
| --- | --- | --- | --- | --- |
| 0 | Does the change alter the intended purpose, or materially change boundaries or dependencies? | \[yes/no\] | \[Architecture diff; marketing copy\] | Pt 109 exception to the security-update rule; Art 3(30) |
| 1 | Does it introduce new threat vectors? | \[yes/no\] | \[New interfaces, ports, protocols, remote services\] | Pt 110 |
| 2 | Does it create new attack scenarios? | \[yes/no\] | \[Threat model delta\] | Pt 110 |
| 3 | Does it change the likelihood of known attack scenarios? | \[yes/no\] | \[Reachability, exposure, attacker effort\] | Pt 110 |
| 4 | Does it change the impact of known attack scenarios? | \[yes/no\] | \[Assets, data, safety, scale\] | Pt 110 |
| 5 | Was the change foreseen and assessed in the current risk assessment? | \[yes/no\] | \[Template 2 row IDs\] | Foreseen changes are not substantial |

### Decision logic

1. If the release is a security update that reduces risk and keeps the intended purpose, it is generally not substantial, even if technically large (pt 108). Go to step 2 only for the pt 109 check.
2. If question 0 is yes, the pt 108 presumption for security updates does not apply (pt 109). A changed intended purpose is substantial (Art 3(30)); otherwise continue to the next steps.
3. If question 5 is yes and that assessment remains valid, the change is not substantial.
4. If questions 1-4 are all no and the risk assessment stays valid, the change is not substantial (pts 111-112).
5. If any of questions 1-4 is yes, test whether the changed risk affects Annex I Part I compliance. If it does, or you cannot show it does not, record the change as substantial. This step is a kit rule, not guidance text.
6. Record the outcome, the reasoning and the approver. Borderline negatives also go to the notified body under Module B.

Art 3(30) (OJ text): a change after placing on the market "which affects the compliance of the product with digital elements with the essential cybersecurity requirements set out in Part I of Annex I or which results in a modification to the intended purpose for which the product with digital elements has been assessed".

### Consequence table

| Action | Not substantial | Substantial modification | Basis |
| --- | --- | --- | --- |
| Placing on the market | Original placing date stands | New placing on the market for the changed version | Guidance pt 116; scope pts 13-15, Example 2 |
| Risk assessment (Template 2) | Record this assessment; update any affected row | Re-assess, focused on the modified parts; reuse unaffected rows | Pts 122-123; Annex VII pt 3 |
| Technical file (Template 4) | Update software versions and the SBOM for the release | New file version; earlier versions retained | Annex VII pts 1, 2(b); Art 13(13) |
| Declaration (Template 5) | Update "as appropriate" if identification changes | New or updated declaration for the new version | Art 28; FAQ 6.8 |
| Notified body | Module B: inform of any change that may affect conformity | Module B: inform and seek approval as an addition to the certificate; Module H: extend the approved system through the same body | Annex VIII Module B pt 7; Module H pt 3.5; FAQ 6.3 |
| Classification (Template 1) | No action unless core functionality changes | Re-run classification for the new version | Art 7; Annex III |
| Support period (Template 3) | Unchanged | Declare a period for the new version; earlier units keep theirs | Guidance pts 132-135; Art 13(8) |
| Testing | Regression tests | Penetration test of the product and its remote data processing | Annex I Part II(3) |
| User information (Template 6) | Update if security properties or update instructions change | Update for the new version | Annex II |
| Legacy products | Art 14 reporting already applies (Art 69(3)) | Full CRA applies to the modified version | Art 69(2) |

No CRA notified body was designated at checks to 8 Sep 2026. Plan any Module B+C or H change around body availability.

### Worked example: L2 Smart Lock (illustrative)

Two releases are assessed separately. Release 3.4.2 fixes a BLE pairing \[flaw\] and rewrites much of the pairing code. Release 4.0 adds remote unlock from the app through the access-management cloud. Today unlock works only over local BLE.

| Question | 3.4.2 security patch | 4.0 remote unlock |
| --- | --- | --- |
| 0 Intended purpose, boundaries or dependencies | No; same purpose and interfaces | Yes; the unlock path now crosses the internet and depends on the cloud |
| 1 New threat vectors | No | Yes; internet-reachable unlock command path |
| 2 New attack scenarios | No | Yes; account takeover or cloud API abuse leads to unlock |
| 3 Likelihood of known scenarios | No; replay likelihood falls | Yes; remote attackers no longer need proximity |
| 4 Impact of known scenarios | No | Yes; unauthorised entry across the installed base at once |
| 5 Foreseen in RA v2.3 | Yes; pairing replay row | No |
| Outcome | Not substantial (pt 108) | Substantial modification (pts 109-110) |

Actions for 4.0: re-assess the unlock and cloud rows only; issue a new technical file version and declaration; seek the notified body's approval as an addition to the Module B certificate; re-run Template 1 and record that L2 stays Annex III Class I item 17; declare a 10-year support period for 4.0 in Template 3; penetration test the lock and the access-management cloud. 4.0 units are in scope because they are placed after 11 Dec 2027. Pushing 4.0 to 3.x units placed before that date brings those units under the CRA (Art 69(2)).

Actions for 3.4.2: record this assessment, update the SBOM and version list, and log the release in the change list shared with the body.

## Common mistakes

- Judging by the size of the code change. The test is risk-based; large security updates are generally not substantial (pt 108).
- Bundling a new feature into a security release and treating it as a patch. Assess the feature itself and ship it separately where feasible (Annex I Part II(2)).
- Missing small features that add unassessed risk, such as "remember me" token storage or unencrypted log export (Examples 44-45).
- Assuming a substantial modification resets or extends earlier units' support period. It does not (pts 132-135).
- Telling the notified body only about positive decisions. The Module B pt 7 duty covers any change that may affect conformity.

*Template 10 · v1.0 · 31 Oct 2026 · Not legal advice; confirm wording against the Official Journal text before use.*
