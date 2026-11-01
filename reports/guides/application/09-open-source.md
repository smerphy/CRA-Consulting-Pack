## 9. Open-source components and open-source products

Treat every open-source component as a supplier you cannot contract with, and every open-source product you sell as a product like any other. Art 13(5) requires due diligence on third-party components, expressly including FOSS never placed on the market. Art 13(6) requires upstream reporting and fix sharing, and Annex I Part II(1) puts every component in the SBOM.

The legal position on who is caught, stewards and attestations is in Open-source software; this section is the engineering procedure.

### Component selection due diligence

Run a component intake gate before a dependency enters the product, scaled to the component's risk (recital 34).

The [Commission FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307) lists acceptable actions. They include software composition analysis, sandboxing critical components, reviewing the component's SBOM and support period, and checking its intended purpose fits yours. It adds assessing the supplier's posture and testing by fuzzing or penetration testing.

Guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) section 7.3 frames due diligence as defining what the product needs from the component. That need is then verified by documentation, assurance evidence or tests.

| Field | What to record | Signal sources |
|---|---|---|
| Need statement | The function the product takes from the component and the security properties it relies on | Architecture; applicability matrix rows served |
| Maintenance signals | Release cadence, time to fix past CVEs, active maintainers, security policy present, bus factor | Repository history; SECURITY.md; OpenSSF Scorecard; Security Insights |
| Assurance | OpenSSF Scorecard result; OSPS Baseline level claimed or assessed; any published self-attestation; conformity evidence where the component is itself a CRA product | [OSPS Baseline](https://openssf.org/wp-content/uploads/2026/01/OpenSSF-OSPS-Baseline.pdf) (41 requirements, 3 levels); Scorecard |
| Licence | SPDX identifier; compatibility with your distribution; obligations triggered by shipping fixes upstream | Licence scanner output |
| Vulnerability history | Open and historical entries in EUVD, NVD and OSV; whether fixes shipped in supported branches | EUVD, NVD, OSV, GHSA |
| Support horizon | Upstream support period against your declared support period; what happens at upstream end of life | Project release policy |
| Exit plan | Replacement candidates; effort to swap; isolation measures if it must stay | Architecture review |
| Decision | Approved, approved with conditions, rejected; owner; date; review trigger | Intake gate record |

A component whose upstream support ends inside your support period needs an exit plan at intake. The FAQ requires you to replace or patch an unsupported component yourself. Recording dependencies on high-risk suppliers in the risk assessment is good practice (recital 58 asks the Commission and MSAs to weigh such non-technical risks); link the intake record to section 3.

### Inventory and monitoring

Every component, including transitive ones to the depth chosen in section 6, appears in the release SBOM with purl, version, licence and hash. Dependency-Track or an equivalent watches NVD, GHSA, OSV and the EUVD for every supported version and feeds PSIRT triage (section 8). Pin versions and verify hashes or signatures at build; a lockfile without hash verification is an inventory, not a control.

### Forking and patching strategy

When upstream will not fix in time, fix it yourself and share the fix. Keep patches as discrete commits on a vendor branch tracking upstream, named by CVE or EUVD identifier. The SBOM can then record pedigree and the patch can be dropped when upstream catches up.

Avoid silent forks. The [Linux Foundation 2026 report](https://www.linuxfoundation.org/hubfs/Research%20Reports/lfr_2026_cra_awareness_report_060826.pdf?hsLang=en) cites LF's 2025 Open Source ROI survey (n=236): an average of 86 private forks per organisation at about 60 hours per fork per release cycle. Its own 2026 survey finds 51% of manufacturers rely passively on upstream for fixes.

For each fork record the upstream commit, the patches carried, the reason, the owner and the re-sync cadence. A fork that drifts from upstream becomes your component with your vulnerability-handling burden.

### Contributing fixes upstream

Art 13(6) requires sharing the code or documentation of a fix with the maintainer, "where appropriate in a machine-readable format". Guidance section 9.2.1 (paras 222-229) sets the mechanics. Report the vulnerability through the project's CVD channel for the version you integrate, after checking databases, advisories and issue trackers to avoid duplicates.

Submit the fix as a patch or pull request in the project's format under a compatible licence and contributor agreement. There is no duty that it is merged and no duty to accept the project's own fix.

Contributing code to a project you do not control does not make you its manufacturer or steward (recital 18; guidance paras 48-49, 85-86). Log every upstream report and contribution in the PSIRT case file.

### Unmaintained components and replacement

Where a component has no maintainer, Art 13(6) imposes no upstream duty, but the product duty remains. Document the finding, the risk, the mitigation (isolation, feature removal, own patch) and a dated replacement plan. Add a review trigger to the risk assessment; the guidance encourages informing the community through public vulnerability records even without a maintainer.

### When the product itself is open source

A monetised open-source product makes its publisher a manufacturer with the full CRA. An unmonetised one from a legal person makes the publisher a steward with Art 24 duties only; non-monetising natural persons have no obligations. The tests are in Open-source software; two engineering consequences follow.

First, Art 32(5): a FOSS product in an Annex III category may use any conformity route, including Module A. The condition is that the Annex VII technical documentation is made public when the product is placed on the market. Publishing the technical file means publishing the risk assessment, the SBOM, the test reports and the vulnerability-handling description.

Decide what the risk assessment can say in public before relying on this route. Redact nothing that the file needs to be complete.

Second, the open-core split. The paid edition is placed on the market and the free community edition is not, even on a near-identical codebase (guidance paras 52-53).

The company is manufacturer for the paid edition and steward for the community edition, per project. Keep one codebase but two sets of records.

The paid edition needs a full Annex VII file and declaration. The community edition needs an Art 24(1) cybersecurity policy.

### The project's SECURITY.md and policy

For the community edition, the steward's Art 24(1) policy must be documented "in a verifiable manner". It covers secure development, vulnerability documentation and remediation, voluntary reporting under Art 15 and information sharing within the community. For the paid edition, the same file doubles as the Part II point 5 CVD policy.

The ORC WG steward white paper V1.0 (January 2026, marked "not legal guidance") recommends keeping the evidence in version-controlled files.

- [ ] Reporting channel, PGP key and expected response times (section 8 targets)
- [ ] Supported versions and the fix policy per branch, with end-of-support dates
- [ ] Disclosure timeline, embargo rules and the accelerated path for actively exploited vulnerabilities
- [ ] Where advisories are published (GitHub Security Advisories, CSAF endpoint) and how CVE and EUVD IDs are obtained
- [ ] Secure-development practices: review requirements, signed releases, SBOM per release, dependency policy
- [ ] How the project shares information with downstream manufacturers and upstream dependencies
- [ ] For the steward: the legal entity acting as steward, the type of support it provides and the Art 24(3) reporting consequence
- [ ] Review date and owner

Stewards cannot CE-mark, need no SBOM or technical file, and are exempt from fines. Art 24 applies only from 11 Dec 2027, and a steward that starts monetising becomes a manufacturer from that date (guidance para 84).

### References and open points

Use the [ORC WG](https://orcwg.org/cra/) deliverables with care. The steward white paper is shipped, the due-diligence white paper D3.2 is work in progress, and the D4.x specifications are not shipped. OpenSSF resources are the [Stewards Playbook](https://policy.openssf.org/CRA/stewards-playbook.html), the OSPS Baseline and the manufacturer checklist linked from its [11 Sep 2026 guide](https://openssf.org/blog/2026/09/11/a-community-guide-to-the-eu-cra-september-11-deadline-for-manufacturers/).

OpenSSF itself puts the Baseline's coverage of manufacturer duties at about 35% ([Tech Talk recap](https://openssf.org/?p=11738)).

Two monetisation patterns are unresolved in the guidance: dual licensing and paid hosting of an otherwise free project. The nearest analogues are the open-core treatment and the rule that monetising services around the software can place it on the market (para 54). Record a FOSS determination memo per project, note the reliance on Commission interpretation, and take legal advice before relying on either pattern.

The due-diligence records and FOSS determination memo serve checklists 3, 4 and 9 in the Requirement checklists tab.
