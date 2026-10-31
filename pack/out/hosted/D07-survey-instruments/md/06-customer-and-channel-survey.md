# Customer and channel survey

Twelve questions ask B2B customers, integrators and channel partners which CRA evidence they will request, by when and through which contract clauses. The answers shape the customer FAQ, the trust page, the support-period evidence and any extended-support offer.

## Design

A short, confidential survey tells the programme which evidence to publish first, and gives product management direct data on how long customers keep products in use.

| Item | Design |
| --- | --- |
| Purpose | Learn which CRA evidence customers and channel partners will request and when, to set the customer FAQ, the trust page and the information published with each product |
| Audience | B2B customers (OEMs, integrators, utilities, installers) and channel partners (distributors, importers, retailers, marketplace sellers). Consumers are reached through product pages instead (ST16) |
| Sampling | Key accounts covering 80% of each BU's EU B2B revenue, plus all EU channel partners; planning assumption about 80 invitations and 40 completes. Each response links to its account through the invitation token, so answers can be read by the product families the account buys |
| Timing | 23 Nov – 11 Dec 2026, after the board; one reminder from the account manager |
| Length | 12 questions, about 8 minutes |
| Approvals | General Counsel approves the text, as for any external statement on compliance. Wording follows the Communication Pack: "preparing to meet the CRA by 11 Dec 2027", never "CRA certified" |
| Data protection | Business contact data only; company-level answers stay with customer operations unless the company consents; raw data deleted after 24 months |

## Survey text

Paste the introduction as the form description; every question offers "Don't know" where a respondent may not have decided yet.

**Introduction screen**

> **Preparing for the EU Cyber Resilience Act: 8 minutes.** Example Group is preparing to meet the EU Cyber Resilience Act (CRA) by 11 Dec 2027. To plan the information we provide with our products, we would like to know what you will need from us and when. Your answers are confidential and used only for this planning. Questions: \[account manager\].

**CUS-01** Which best describes your organisation's relationship with Example Group? *Single choice, required.*

- OEM or system integrator
- Utility or infrastructure operator
- Installer or building-services contractor
- Distributor or wholesaler
- Importer into the EU
- Retailer or online marketplace seller
- Other (please specify)

**CUS-02** In which EU Member States do you sell, install or operate our products? *Multiple choice of the 27 Member States, plus "All EU Member States"; required.*

**CUS-03** Is your organisation an essential or important entity under NIS2? *Single choice, optional.*

- Yes, an essential entity
- Yes, an important entity
- No
- Don't know

**CUS-04** Which of the following will you ask us to provide for the products you buy from us? *Multiple choice, required.*

- EU declaration of conformity
- Confirmation of CE marking under the CRA
- Support period end date for each product
- Security update policy
- Contact for reporting vulnerabilities, and our disclosure policy
- Access to the software bill of materials (SBOM)
- Security advisories in machine-readable form (CSAF)
- Statements on whether a known vulnerability affects the product (VEX)
- User information on secure set-up, use and decommissioning (Annex II)
- Test reports or certificates
- None of these
- Don't know yet

**CUS-05** When will you first need this information? *Single choice, required.*

- Before 30 Jun 2027
- 1 Jul to 30 Nov 2027
- 1 to 31 Dec 2027
- 2028 or later
- Don't know

**CUS-06** How would you prefer to receive it? *Multiple choice, up to two; optional.*

- A public security or trust web page
- A customer or partner portal
- With each delivery
- On request through my account manager
- A machine-readable feed

**CUS-07** Do you plan to add CRA requirements to your purchase contracts or supplier conditions? *Single choice, required.*

- Already added
- Planned within 12 months
- Under consideration
- No plans
- Don't know

**CUS-08** Which commitments will those requirements cover? *Multiple choice; shown if CUS-07 is already added, planned or under consideration.*

- Notification of vulnerabilities within a set time
- SBOM delivery
- A minimum support period
- Right to request evidence or to audit
- Notification of security incidents
- Liability or indemnity for vulnerabilities
- Other (please specify)

**CUS-09** How long do you usually keep our products in operation? *Single choice, required.*

- Under 5 years
- 5 to 7 years
- 8 to 10 years
- 11 to 15 years
- More than 15 years
- Don't know

**CUS-10** Would your organisation pay for security updates beyond a product's declared support period? *Single choice, required.*

- Yes
- Possibly, depending on price
- No
- Don't know

**CUS-11** What annual price, as a share of the product's purchase price, would you consider reasonable for that extended support? *Single choice; shown if CUS-10 is yes or possibly.*

- Under 5%
- 5% to 10%
- 11% to 15%
- More than 15%
- Don't know

**CUS-12** What CRA questions do you expect your own customers, auditors or regulators to ask you about our products? *Open text, optional.*

**Completion screen**

> Thank you. We will publish answers to common questions on \[trust page\] by \[date\]. To report a vulnerability in one of our products, use \[vulnerability contact\].

## Analysis and how results feed the programme

Every question maps to a decision; segments with fewer than 5 respondents are merged before reporting.

| Questions | Analysis | Feeds |
| --- | --- | --- |
| CUS-01 to CUS-03 | Respondents by segment; Member State coverage per segment | Distribution map (issue I01) and the "Member States where available" field in Article 14 early warnings |
| CUS-04 to CUS-06 | % requesting each item, by segment; timing and channel preference | Order and content of the customer FAQ and trust page; Annex II drafting priority; whether to offer SBOM access, which Annex II point 9 leaves optional |
| CUS-07 and CUS-08 | % with CRA clauses already added or planned; clause types | Standard sales and legal positions on notification times, SBOM delivery and liability |
| CUS-09 | Expected time in use, by product family and segment | Support-period determinations, which must reflect expected time in use (Art 13(8); Annex VII point 4) |
| CUS-10 and CUS-11 | % willing to pay; price bands | Extended-support offer; not part of the base-case business case |
| CUS-12 | Themes coded and counted | Customer FAQ in the Communication Pack (D05) |

No published survey is directly comparable. The Linux Foundation found 47% of SME manufacturers expect to raise prices to cover compliance (RD04: survey, small subsample of 54 SME manufacturers); treat it as context for CUS-10, not as a benchmark.

*Project Rampart · Survey and Interview Instruments (D07) · Illustrative · 31 Oct 2026*
