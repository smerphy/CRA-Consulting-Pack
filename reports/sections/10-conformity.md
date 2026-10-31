## Conformity assessment and documentation

The conformity route under Art 32 of the [CRA](https://eur-lex.europa.eu/eli/reg/2024/2847/oj) depends on the product's class (see Product classification), and as of 30 Oct 2026 an important Class I product cannot use self-assessment. Art 32(2) allows Module A only where an OJ-cited harmonised standard, common specification or Art 27(9) scheme is fully applied, and none is cited. The third-party alternative is blocked too, because no CRA notified body has been designated.

Art 13(12) sequences the work: technical documentation, then the Art 32 procedure, then the EU declaration and CE marking, all before placing on the market. [Guidance C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) pt 137 lets any manufacturer choose a stricter route than its class requires.

### Routes by class

| Class | Permitted routes (Art 32) | Notified body needed today? | What changes later |
|---|---|---|---|
| Default (no Annex III or IV core functionality) | Module A; stricter routes optional (guidance pt 137) | No | Nothing; a cited standard adds presumption of conformity for the risks it covers |
| Important Class I | Module A only if a cited harmonised standard, common specification or "substantial"-level scheme is applied in full and covers all core-functionality risks (guidance pt 149); otherwise B+C or H | Yes in practice, and none exists | First OJ citations (2027 at the earliest) reopen Module A; the Art 27(9) EUCC act would let a "substantial" certificate replace third-party assessment for covered requirements |
| Important Class II | B+C, H, or an Art 27(9) scheme at "substantial" or higher (Art 32(3)) | Yes, or an EUCC certificate once the Art 27(9) act exists | Art 27(9) act planned Q4 2026, not adopted |
| Critical (Annex IV) | An Art 8(1) mandatory scheme if adopted; otherwise any Art 32(3) route (Art 32(4)) | Yes | No Art 8(1) act adopted or consulted; a future one carries at least 6 months' transition |
| FOSS in Annex III | Any Art 32(1) route, including Module A, if the Annex VII documentation is public at placing (Art 32(5)) | No, if documentation is published | Nothing changes |
| High-risk AI system (AI Act Art 6) | AI Act Art 43 procedure covers the CRA requirements (Art 12(2)), except important or critical products under AI Act Annex VI internal control, which follow the CRA routes (Art 12(3)) | Per the AI Act route | No sequencing guidance yet; CRA-AI Act interplay guidance targeted for end-2026 |

### Annex VIII modules

| Module | Manufacturer does | Notified body does | Ongoing surveillance | Retention | CE mark and notified-body number |
|---|---|---|---|---|---|
| A, internal control | Annex VII documentation; measures so design, production and vulnerability handling meet Annex I; declaration on sole responsibility | Not involved | No surveillance | Declaration and documentation 10 years or the support period | CE mark only |
| B, EU-type examination | Application to one body with technical documentation, risk analysis and supporting evidence; inform the body of modifications affecting conformity (pt 7) | Examines design and vulnerability-handling processes; tests specimens; issues the EU-type examination certificate stating its own validity (pt 6) | Monitors the state of the art (pt 7); periodic audits of vulnerability handling (pt 8) | Certificate and additions 10 years or the support period (pt 10) | No number requirement |
| C, conformity to type | Keeps production conforming to the approved type and Part II processes; declaration per model | None in the production phase ([Commission FAQ](https://ec.europa.eu/newsroom/dae/redirection/document/123307) 6.2) | None beyond Module B | Declaration 10 years or the support period | CE mark only |
| H, full quality assurance | Operates an approved quality system covering design, development, final inspection, testing and vulnerability handling (pt 3.2); notifies intended changes (pt 3.5) | Audits the quality system, including one model's technical documentation per product category, with a product-experienced assessor and a site visit (pt 3.3) | Periodic audits with reports, plus site access (pt 4); whether pt 4 also allows unexpected visits is disputed between the two mirrors read and is not verified against the OJ text | Quality-system documentation, approved changes and body decisions 10 years or the support period (pt 6) | CE mark followed by the notified body's identification number (pt 5.1; Art 30(4)) |

The FAQ (6.2-6.3) describes B+C as one body doing documentation review and its own tests, with the certificate valid for a period the body defines. Module H suits portfolios with frequent substantial modifications because new variants extend the approved system; ISO 9000 certification alone does not satisfy it. Non-binding [BSI TR-03183-H v1.1.0](https://www.bsi.bund.de/SharedDocs/Downloads/EN/BSI/Publications/TechGuidelines/TR03183/BSI-TR-03183-H_v1_1_0.pdf?__blob=publicationFile&v=3) (30 May 2026) shows how an ISO/IEC 27001 ISMS can be extended to carry Module H.

### Technical documentation (Annex VII)

Art 31 requires the dossier before placing on the market, kept current at least through the support period. Art 13(13) sets retention at 10 years after placing or the support period, whichever is longer. It may be written in any language.

On reasoned request it must reach an MSA "in a language which can be easily understood by that authority" (Art 13(22); FAQ 6.6). Guidance pts 174-177 allow one dossier for a product family with the same architecture, security-relevant design, intended purpose and risks.

- [ ] Point 1, general description: intended purpose; software versions affecting compliance; for hardware, photographs or illustrations of external features, markings and internal layout; the Annex II user information
- [ ] Point 2(a), design and development: drawings and a system architecture description showing how software components build on or feed into each other
- [ ] Point 2(b), vulnerability handling: the SBOM, the CVD policy, evidence of the vulnerability-reporting contact address, and the technical solutions for secure update distribution
- [ ] Point 2(c), production and monitoring processes with validation evidence
- [ ] Point 3, the Art 13 cybersecurity risk assessment, including how each Part I requirement applies and justifications for any not applied
- [ ] Point 4, the information used to determine the support period (Art 13(8))
- [ ] Point 5, harmonised standards, common specifications or certification schemes applied in full or in part; where not applied, descriptions of the solutions adopted and other specifications used
- [ ] Point 6, test reports on the product and on the vulnerability-handling processes against Annex I Parts I and II
- [ ] Point 7, a copy of the EU declaration of conformity
- [ ] Point 8, the SBOM, where applicable, supplied on an MSA's reasoned request

Guidance pts 37-39 relieve products designed before 11 Dec 2027 of test evidence for the original design phases where the risk assessment shows existing measures adequate; Part II evidence is still required. The dossier is not owed to customers or the public, except for FOSS manufacturers self-attesting under Art 32(5) (FAQ 6.6).

### EU declaration of conformity and CE marking

Art 28 requires one declaration per product following the Annex V structure, "updated as appropriate", in the languages of the Member States of sale. The FAQ (6.8) ties it to the individual product rather than the type, and says a new version "might need a new declaration" after a substantial modification. One declaration may cover several Union acts (Art 28(3)).

- [ ] Annex V point 1: name, type and information enabling unique identification
- [ ] Point 2: name and address of the manufacturer or authorised representative
- [ ] Point 3: statement that the declaration is "issued under the sole responsibility of the provider"
- [ ] Point 4: object of the declaration allowing traceability, optionally with a photograph
- [ ] Point 5: statement of conformity with the relevant Union harmonisation legislation
- [ ] Point 6: references to harmonised standards, common specifications or certifications used
- [ ] Point 7: where applicable, notified body name and number, procedure performed and certificate identification
- [ ] Point 8: additional information; signed for and on behalf of, with place, date, name and function

The Annex VI simplified form reads "Hereby, [manufacturer] declares that the product with digital elements type [...]" complies with Regulation (EU) 2024/2847, and must give "the exact internet address" of the full declaration (Art 13(20)). The declaration accompanies the product; Annex II point 6 carries its address, and a copy sits in the technical file.

CE marking (Arts 29-30) goes "visibly, legibly and indelibly" on the product, else on the packaging and the declaration. For software it goes "either to the EU declaration of conformity" or on the accompanying website, in a section consumers can reach directly (Art 30(1)).

It must be affixed before placing on the market and takes the notified body's number only under Module H (Art 30(4)). Market surveillance may request the declaration and all conformity documentation on reasoned request (Art 13(22)).

### Notified bodies

Chapter IV (Arts 35-51) applies since 11 Jun 2026, yet no CRA notified body appeared in NANDO at the last verified checks on 8 Sep 2026. The [Commission conformity-assessment page](https://digital-strategy.ec.europa.eu/en/policies/cra-conformity-assessment), updated 31 Jul 2026, still says "once available". Art 35(2) only asks Member States to "strive" for sufficient bodies by 11 Dec 2026; the zero count is not verified past 8 Sep 2026.

Accreditation runs against EN ISO/IEC 17065 for Modules B+C and EN ISO/IEC 17021-1 for Module H. The Art 43 objection window is 2 weeks for accredited bodies and 2 months otherwise. Notifying authorities documented so far: Germany, [BSI](https://www.bsi.bund.de/EN/Themen/Unternehmen-und-Organisationen/Informationen-und-Empfehlungen/Cyber_Resilience_Act/Notifizierung-CRA/notifizierung-cra.html) with DAkkS accreditation; Finland, [Traficom](https://kyberturvallisuuskeskus.fi/en/our-activities/regulation-and-supervision/cyber-resilience-act-cra/apply-become-notified-body-under-cra) with FINAS; Malta, MDIA (Legal Notice 238 of 2026); Hungary, SZTFH (Act CXXXV of 2025).

France named ANSSI as notifying authority only, by Décret 2026-944 of 9 Oct 2026. ENISA published [technical competence requirements](https://www.enisa.europa.eu/publications/technical-competence-requirements-for-cra-notified-bodies) for CRA notified bodies on 4 Jun 2026.

In the pipeline: [Brightsight](https://www.brightsight.com/cra-notified-body-services) holds RvA ISO/IEC 17065 accreditation for Module B pending Dutch notification, and [Applus+](https://www.appluslaboratories.com/global/en/what-we-do/service-sheet/cyber-resilience-act-notified-body) is "progressing through" accreditation (both vendor statements). Vendor estimates, unverified: 12-18 months per body to designation; 2-4 months to contract a body; 3-6 months per Module B+C engagement; EUR 20,000-60,000 per Module B examination; EUR 80,000-150,000 for a first Module H engagement ([CRA Decoded](https://cra-decoded.com/blog/posts/cra-notified-body-capacity-crisis/), commentary).

### Substantial modification and re-assessment

A substantial modification is a new placing on the market (guidance pt 116). It is re-assessed with focus on the modified parts, reusing unaffected documentation (pts 122-123).

Guidance pt 110 gives a four-question test: new threat vectors, new attack scenarios, changed likelihood of known scenarios, or changed impact. All negative answers mean no substantial modification (pts 111-112).

Security updates are "generally not" substantial modifications, even with large technical changes (pt 108). The exception is an update that alters intended purpose or "materially" changes boundaries or dependencies, such as moving encryption to a remote service (pt 109). Under Module B the body must be told of any change that may affect conformity (Annex VIII pt 7); under Module H scope extensions go to the same body (FAQ 6.3).

Art 69(1) keeps existing EU type-examination certificates on cybersecurity requirements under other Union law valid until 11 Jun 2028. These are chiefly RED Delegated Regulation (EU) 2022/30 certificates; they evidence RED compliance, not CRA conformity.

### SMEs (Art 33)

Art 33(5) lets micro and small enterprises use a simplified Annex VII format once the Commission specifies it by implementing act. No such act has been adopted, drafted or scheduled per the [Commission MSME page](https://digital-strategy.ec.europa.eu/en/policies/cra-msmes), so small manufacturers must build the full dossier now. Fees must be reduced proportionately for SMEs (Art 32(6)); no Art 33(2) regulatory sandbox was identified.
