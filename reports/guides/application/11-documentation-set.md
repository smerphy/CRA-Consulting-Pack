## 11. The documentation set per product

Three documents leave the engineering process for every product version: the Annex VII file, the Annex II user information and the declaration of conformity. Their legal contents are in Conformity assessment and documentation and Annex I Part II: vulnerability handling and lifecycle duties. This section gives the file structure, the publication mechanics and the versioning rules.

### The Annex VII file structure

No authority publishes an Annex VII template. [BSI TR-03183-1 v1.0.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-1_v1_0_0.pdf?__blob=publicationFile&v=3) section 4.8 lists the minimum content of an assessment report, which "can therefore form part of the technical documentation". The outline below uses it as the skeleton and maps each part to the Annex VII point it satisfies.

1. **Cover and control.** Product name, model and variants; file version; date; author and approver; retention date (Art 13(13)). Language note: any language internally, translatable for an authority on reasoned request (Art 13(22)).
2. **Product identification.** Intended purpose and foreseeable use from the product definition record (section 2); hardware and software versions affecting compliance. For hardware, photographs or illustrations of external features, markings and internal layout. The remote-function map and the family variant list. Annex VII point 1(a)-(c).
3. **Risk context.** Operational environment, user profile, assets in the three classes, attacker profile, expected time in use. Feeds Annex VII point 3.
4. **Risk assessment.** Threat model and data-flow diagrams; evaluated risks; accepted risks with treatment. The Annex I Part I applicability matrix with justifications, and the Part I point (1) and Part II application statements (section 3). Annex VII point 3.
5. **Design documentation.** Architecture including network and physical interfaces and how software components build on each other. Selected controls with the risk each mitigates and the Annex I item each serves. Non-applicable items with justification; implementation description; verification approach. Annex VII point 2(a).
6. **Vulnerability handling.** The SBOM reference and hash per version; CVD policy; evidence of the reporting contact (security.txt and Annex II point 2). The update design note (section 7), the PSIRT process description (section 8) and upstream reporting records. Annex VII point 2(b).
7. **Production and monitoring.** Build and release process, signing, gate records, series-production conformity measures (Art 13(14)). Annex VII point 2(c).
8. **Support period.** Declared period per variant and version with the information used to determine it under Art 13(8); the version-support matrix; end-of-support communication plan. Annex VII point 4.
9. **Standards and specifications.** Harmonised standards, common specifications or certification schemes applied in full or in part. Where none applies, the solutions adopted and the specifications used, labelled draft where they are drafts. Annex VII point 5.
10. **Test reports.** Product tests against Part I and process tests against Part II, indexed by requirement (section 12 evidence index). Annex VII point 6.
11. **User documentation.** The Annex II document and its published URL. Annex VII point 1(d).
12. **Declaration.** Copy of the EU declaration of conformity. Annex VII point 7.
13. **SBOM annex.** The SBOM itself, held for supply on a market surveillance authority's reasoned request. Annex VII point 8.

Products designed before 11 Dec 2027 may state where historical design evidence is replaced by the risk assessment (guidance paras 37-39). Say so in part 5.

### The Annex II user-information document

Annex II lists what must accompany the product "at minimum", in paper or electronic form (Art 13(18)). It stays available for 10 years or the support period and is kept online where provided online. The point-by-point checklist is in Annex I Part II: vulnerability handling and lifecycle duties; write it as one versioned document per product or family.

- Publish at a stable URL of the form `/security/<product>/<version>/` with a `latest` alias, and never delete a version page while its retention runs.
- Point 2 carries the same contact and policy URL as security.txt; point 6 carries the exact declaration URL.
- Point 7 carries the end month and year per version.
- Point 8(e) explains the opt-out from automatic security updates; point 9 appears only if you choose to give users the SBOM.
- Point 5 is where residual-risk treatment by user information lands (section 3); write it as concrete conditions and compensating measures, not a disclaimer.
- Point 8(f) applies to components intended for integration. It must give integrators what they need for their own Annex I and Annex VII work (section 4 integrator pattern).
- Language: easily understood by users and by market surveillance authorities in the Member States of sale.

The same page can host the CE marking for software, the declaration, the advisory index and the archive warnings. That satisfies Art 30(1), Annex VI, Annex II and the public-page expectations of BSI TR-03183-3 in one place.

### The EU declaration of conformity

Draw up one declaration per product following the Annex V structure, with the eight elements listed in Conformity assessment and documentation. Keep it "updated as appropriate" and in the languages required by the Member States of sale (Art 28). Element 6 cites standards used, which today means none cited and possibly drafts named as specifications.

Element 7 names the notified body, procedure and certificate where Module B+C or H applies.

Signing: the person signing acts for the manufacturer and assumes responsibility for compliance (Art 28(4)). Name the function, place and date, and keep the signing authority with the executive sponsor or a written delegate. Where several Union acts apply, one declaration or a dossier of declarations covers all of them (Art 28(3)).

The simplified Annex VI form reads "Hereby, [manufacturer] declares that the product with digital elements type [...]" complies with Regulation (EU) 2024/2847. It then gives "the exact internet address" of the full declaration (Art 13(20)). Use it in packaging and in-app screens; the full declaration lives at that address and a copy sits in the technical file.

A product family may share one declaration that "clearly identifies the product variants" (guidance paras 174-177).

### CE marking placement

Hardware carries the CE marking visibly, legibly and indelibly on the product, else on the packaging and the declaration. It may be under 5 mm where the product's nature warrants it (Art 30(1)-(2)). Software carries it on the declaration or on the accompanying website, in a section consumers can reach directly (Art 30(1)).

For app-store software no authority has said how the store listing should present it. Put it on the declaration and the security page.

Affix it before placing on the market and only after a positive conformity assessment ([Commission FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307) section 6.7). The notified body's identification number follows the CE marking only under Module H (Art 30(4)).

### Support-period declaration and end-of-support notice

Declare the support period per variant and, for software, per substantially modified version. Show the end month and year at the time of purchase on the product, packaging or digitally (Art 13(19)). Five years is a floor, not a default (guidance paras 125-128).

Design an in-product or in-app end-of-support notification where technically feasible. Plan the notice content now: date reached, risk of continued use, upgrade path, archive warning text under Art 13(11).

Keep a version-support register: version, placing date, declared end date, what was shown at purchase, update channel, migration path, legacy-version owner. It feeds Annex VII part 8, Annex II point 7 and the Art 13(10) decision.

### Versioning and retention tied to each placing

Every placing on the market freezes a document set. For hardware that is each unit shipment against the file version current at the time.

For software it is the first offering of each version (guidance paras 11-16). Record the mapping from product version to file, Annex II and declaration versions in the release gate record (section 5).

Retention runs 10 years from placing or the support period, whichever is longer. It covers the file and declaration (Art 13(13)) and the Annex II information (Art 13(18)).

A substantial modification produces a new placing, a new declaration and a new file version while the earlier versions stay retained. Store the set under version control with signed tags, mirrored to immutable storage independent of any repository provider.

### Product-family variant list

One file, one assessment and one declaration may cover a family that shares architecture, security-relevant design, intended purpose and risks (guidance paras 174-177). Maintain a variant list inside the file and the declaration.

| Variant | Model and SKU | Differences from the reference variant | Interfaces, stack, update path or connectivity differences | Affected matrix rows | Separate evidence | Declared end of support |
|---|---|---|---|---|---|---|
| Reference | | None | None | None | Full set | |
| Variant A | | For example, no cellular modem | Interface removed; emitter inventory differs | 2(i), 2(j) | Port scan for variant A | |
| Variant B | | For example, retail firmware with cloud onboarding | Additional RDPS function | 2(d), 2(e), 2(h) boundary rows | Boundary tests for variant B | |

A difference in the update mechanism or remote connectivity usually means a new family rather than a variant; when in doubt, split.

The three documents close checklists 6, Annex II, and 7, documentation and declaration, in the Requirement checklists tab.
