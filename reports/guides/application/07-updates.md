## 7. Secure update mechanism

The update mechanism keeps every other Annex I item true after shipment, so design it as a security product in its own right. It serves Part I items 2(c) and 2(f) and Part II points 2, 7 and 8. The legal detail is in Annex I Part I: essential requirements for product properties and Annex I Part II: vulnerability handling and lifecycle duties.

ENISA's [draft Technical Advisory on Secure Update Mechanisms](https://www.enisa.europa.eu/sites/default/files/2026-05/Draft%20-%20ENISA%20Technical%20Advisory%20-%20Update%20Mechanisms%20-%20v0.6.pdf) (v0.1, May 2026, draft) is the reference used here. It is technology-agnostic and "consistent with" TUF, Uptane and NIST SP 800-40.

### Architecture

| Element | Pattern | Why |
|---|---|---|
| Signing keys | Offline root key; online operational signing key; both in an HSM or cloud KMS with role separation between build, release approval and key custody | ENISA section 4.1 (secure signing, key protection, separation of duties); draft EN 304 621 threat list names revoked and compromised signing keys |
| Metadata | TUF-style roles (root, targets, snapshot, timestamp) or Uptane director and image repositories for fleets; metadata carries version, expiry and a monotonic counter | Freshness and anti-rollback (ENISA 4.2, 4.3); TUF and Uptane are the named patterns |
| Transport | TLS to a trusted source, with trust placed in the signature not the download location; controlled redirects | ENISA 4.2 trust model |
| Verification | Verify signature, applicability (model, hardware revision, current version) and freshness before any write to the active partition | ENISA 4.3; draft EN 304 621 SU_UPDATES-4 to -6 |
| Anti-rollback | Reject any image whose counter is below the installed one; an intentional downgrade needs explicit authorisation and an auditable event | ENISA 4.3; draft EN 304 621 SU-6 |
| Install | Atomic A/B slots or transactional package install; power loss at any point leaves a bootable, secure unit; recovery image retained | ENISA 4.3, 4.4; Playbook 4.20 release gate "failed updates do not leave the system insecure or unusable" |
| Observability | Record start, finish, outcome and failure reason per unit; secure logging; corruption handling; trust-anchor recovery path | ENISA 4.4; draft EN 304 621 SU-12 |

For software products the same pattern applies with package signatures, a signed manifest and transactional installation. For app-store distribution the store's signing is the transport; the manufacturer still verifies and logs applicability and version on first run.

### Default-on automatic security updates

Part I item 2(c) requires, where applicable, automatic security updates installed within an appropriate timeframe and enabled by default. It adds a clear and easy opt-out, user notification and temporary postponement; consumer products are the primary case (recital 56). Implement a check-and-install cycle that runs unattended and notifies the user with the advisory text.

Allow postponement for a bounded period. Let the user disable automatic installation in a clearly labelled setting documented in Annex II point 8(e).

Managed estates implement "where applicable" through scheduling rather than unattended installation. Maintenance windows, staged rollout and an administrator approval step are the pattern (draft EN 304 621 Annex G on cluster and MDM-managed deployments). The product must still notify and must still make the update available without delay.

Recital 56 carves out products primarily intended as components and products in professional, critical or industrial environments where users would not expect automatic updates. Claim the carve-out only in the risk assessment row for 2(c), with the deployment context as justification, and keep notification and timely availability regardless. A consumer device sold through a professional channel does not qualify by sales channel alone.

### Separating security from functionality updates

Part II point 2 requires security updates provided separately from functionality updates "where technically feasible". Run maintenance branches per supported version with a security-only hotfix channel, and keep feature releases on a separate train.

The [Commission FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307) section 4.3 gives the examples. A certificate-validation fix ships alone; bundling is defensible where the fix needs a functional change, such as a stricter parser. It is also defensible where disabling the vulnerable interface is itself the fix.

Record every bundling decision with the reason on the release gate (section 5). A device with one monolithic firmware image can still separate by cutting a security-only image from the maintenance branch. The exception is rare and must be argued per case.

### Advisory messages with each update

Part II point 8 requires security updates "accompanied by advisory messages" with the action users should take. Attach a short advisory to each security update: what was fixed, affected versions, severity and any restart or configuration step. Link it to the full CSAF advisory (section 8).

Devices show it in the app or admin interface; software shows it at install time and in release notes.

### Availability for 10 years and public archives

Each security update must remain available for at least 10 years after issue, or the rest of the support period if longer (Art 13(9)). Design the update repository as a long-lived signed-artefact store with immutable storage and metadata that survives key rotation. Budget for it beyond the product's commercial life.

Art 13(11) permits public archives of old versions if users are "clearly informed in an easily accessible manner" of the risks. Put a warning banner on every archive page and in the package metadata.

### The latest-version rule

Where successive substantially modified software versions are placed on the market, Art 13(10) allows patching only the latest version. The condition is that users can upgrade free of charge without additional hardware or infrastructure costs. Guidance paras 129-131 exclude normal operational effort from "additional costs" and include mandatory new hardware.

Maintain a version-support matrix stating, per version, whether it receives fixes, the free upgrade path and the end-of-support month and year. The CVD policy and information sharing continue for all versions.

### Update at first use for stock units

Units sit in warehouses and on shelves while vulnerabilities are disclosed. Draft EN 304 621 SU_UPDATES-3 (draft) expects the product to attempt installation of security updates released since placing at first use. Draft EN 304 626 frames item 2(a) "at first use" with the same mitigation.

Build the first-boot flow to check for and install security updates before onboarding completes. Document a manual path where no connectivity exists at first use.

### Design note contents

The Annex VII technical documentation must describe "the technical solutions chosen for the secure distribution of updates" (point 2(b)). Write one update design note per product or family. Cover trust model and key hierarchy, metadata and anti-rollback, transport and sources, verification and installation flow, recovery and observability.

Add default behaviour and user controls, release trains and separation policy, repository retention and the version-support matrix. Reference the test records below.

### Acceptance tests

- [ ] Unsigned, wrongly signed and expired-metadata images are rejected and logged
- [ ] An image with a lower rollback counter is rejected; an authorised downgrade produces an audit event
- [ ] Power loss injected at each stage of install leaves a bootable unit on the previous or new image, never a broken one
- [ ] Recovery image restores a unit after a corrupted active slot
- [ ] Factory-fresh unit with the release-time image installs the latest security update before onboarding completes
- [ ] Default configuration has automatic security updates enabled, or the recital 56 carve-out is justified in the risk assessment
- [ ] Notification, postponement and opt-out work and match the Annex II 8(e) text
- [ ] A security-only release installs on the maintenance branch without the latest feature release
- [ ] Every update event appears in the device log with outcome and reason
- [ ] Signing key rotation and trust-anchor update succeed on fielded units without manual intervention
- [ ] Update server test from a separate network confirms TLS, no plaintext fallback and controlled redirects
- [ ] Archive page for an unsupported version shows the risk warning before download

Keep the test records with the design note; they are Annex VII point 6 evidence and feed the evidence index in section 12.

The design note and test records serve checklist 2 (item 2(c)) and checklist 3 (points 7 and 8) in the Requirement checklists tab.
