## 2. Governance: roles, decision rights and cadence

Every CRA decision needs one accountable person, and three of them cannot wait for a committee. Those three are the Art 14 awareness declaration, the acceptance of residual product risk and the signature on the EU declaration of conformity. This section fixes who holds each decision, how often the governing bodies meet and how disputes escalate.

The role descriptions themselves are in the knowledge base, Engineering compliance programme (Roles table). This section adds the decision rights and the cadence around them.

### RACI

R is responsible for the work, A is accountable for the outcome, C is consulted before the decision and I is informed after it. One A per row, always a named individual, never a team.

| Decision | Executive sponsor | Compliance lead | Product security officer | PSIRT lead | Engineering lead | Legal | Procurement | Product management |
|---|---|---|---|---|---|---|---|---|
| Scope and classification decision per product (Arts 2-3, 7; IR 2025/2392) | I | A | C | I | R | C | I | R |
| Risk assessment sign-off (Art 13(2)-(4)) | I | C | A | C | R | I | I | C |
| Release gate (Annex I Part I(2)(a); guidance paras 230-237) | I | I | A | C | R | I | I | C |
| Declaration of conformity signature (Art 28; Annex V) | A | R | C | I | C | C | I | I |
| Art 14 awareness decision (guidance para 213) | I | I | C | A | R | I | I | I |
| Notified-body relationship (Art 32; Annex VIII) | C | A | R | I | C | C | R | I |
| Supplier terms (Art 13(5); Art 23) | I | C | C | I | C | R | A | I |
| Support period and end-of-support decision (Art 13(8), (19)) | I | C | C | C | C | C | I | A |
| Steward determination for published FOSS (Arts 3(14), 24) | I | C | C | I | R | A | I | C |
| Budget (Section 11) | A | R | C | C | C | I | C | C |

Two rows deserve comment. Product management is accountable for the support period because Art 13(8) ties it to expected use time, a commercial judgement with engineering inputs. Legal is accountable for steward determinations because the per-project monetisation test in guidance [C(2026) 5252](https://ec.europa.eu/newsroom/dae/redirection/document/131456) paras 69-84 is a legal reading of business facts.

### Decision rights that must sit with named individuals

| Decision | Holder | Deputy chain | Written rule |
|---|---|---|---|
| Declaring "awareness" of an actively exploited vulnerability or severe incident, including at 03:00 on a Sunday | PSIRT lead | Two named deputies on the on-call rota | Awareness is a "reasonable degree of certainty" after an immediate initial assessment (guidance para 213); no approval step may precede it |
| Submitting the 24-hour early warning | The on-call Primary or Secondary Assigned Representative | Any other registered Assigned Representative | Legal reviews the 72-hour and final reports, not the early warning |
| Signing the EU declaration of conformity | Executive sponsor, or a delegate named in a signed instrument | One named alternate | The signatory assumes responsibility for compliance (Art 28(4)); no delegation by email |
| Accepting residual product risk | Product security officer | Executive sponsor on appeal | Judged against "appropriate level of cybersecurity"; cost, appetite or commercial strategy are "not relevant" (guidance paras 156-163) |
| Approving a non-applicable Annex I Part I(2) item | Product security officer | None | Justification recorded in the risk assessment (Art 13(3)-(4); Recital 55) |
| Blocking a release | Product security officer | Executive sponsor | Release-blocking authority is written into the sponsor's mandate |
| Choosing the main-establishment Member State and coordinator CSIRT | Compliance lead with legal | None | Decided and recorded before any incident (Art 14(7)); see the knowledge base, Reporting obligations |

The residual-risk rule needs emphasis because it breaks enterprise habit. Most risk frameworks let a risk owner accept a risk above appetite with a business case. Guidance paras 156-163 say that for product risk "internal risk tolerance, commercial strategy or mere cost considerations" do not count.

If a risk cannot be addressed, the design, functionality or intended purpose may have to change instead. Section 5 explains how to carry this into the enterprise risk framework.

### Making the DoC signature a controlled authority

1. Record the signing authority in a board or executive-committee instrument naming the signatory, alternate and scope (product families, markets).
2. Require a completed pre-signature checklist. It covers the Annex VII file, the assessment record or certificate, the signed risk assessment, the release gate and the Annex II information.
3. Make the compliance lead counter-sign the checklist, so the sponsor signs on evidence they did not assemble.
4. Log every signature in the system of record (Section 8) with the DoC id, product versions covered and the checklist reference.
5. Review the authority annually and on any change of signatory. An incorrect or absent DoC is a formal non-compliance under Art 58.

Commission [FAQ v1.4](https://ec.europa.eu/newsroom/dae/redirection/document/123307) Section 6.8 says a DoC cannot be signed without a positive conformity assessment. It adds that a new version "might need a new declaration". The checklist step above is where both are enforced.

### Steering cadence

| Forum | Frequency | Chair | Standing agenda | Decisions taken |
|---|---|---|---|---|
| PSIRT review | Weekly, plus ad hoc on any awareness declaration | PSIRT lead | Open vulnerability cases, reporting clocks, upstream reports owed, advisory backlog, on-call rota | Case closure, disclosure timing, Art 14(8) user notification |
| Programme board | Monthly | Compliance lead; executive sponsor attends | Scope register changes, classification decisions, risk assessments awaiting sign-off, technical-file completeness, notified-body status, KPIs (Section 11) | Wave priorities, budget drawdown, escalations |
| Standards and guidance review | Quarterly | Compliance lead | OJ citations, FAQ and guidance versions, ENISA and BSI publications, delegated and implementing acts, Member State enforcement laws, notified-body designations | Re-mapping decisions, policy updates |
| Executive review | Quarterly, aligned to board reporting | Executive sponsor | Portfolio status, residual-risk appeals, DoC pipeline, exposure under Art 64 | Risk appeals, resourcing |

The quarterly review exists because the authority stack moves. The Commission FAQ reached v1.4 within nine months, and the Art 26 guidance of 27 Jul 2026 formally remains a draft. The knowledge base, Open questions and watchlist, lists the dates to track.

### Escalation paths

- Engineering disagrees with a release block: engineering lead to product security officer, then to the executive sponsor within two working days. The block stands until overturned in writing.
- Residual risk the product security officer will not accept: to the executive sponsor. The sponsor may only overturn with a written basis that is not cost or appetite (guidance paras 156-163).
- Dispute over classification or scope: compliance lead to legal; if unresolved, the stricter reading applies until the programme board decides.
- Awareness contested after the fact: never reopened to delay a filing; reviewed at the next PSIRT review and the lesson recorded.
- Supplier refuses CRA clauses: procurement to compliance lead; the component enters the intake gate (Section 6) as high risk with a documented exit plan.
- Notified-body slot at risk: compliance lead to programme board; fallback is a second pre-contracted body (Section 10).

### Governance checklist

- [ ] RACI adopted and published, with one named individual per A
- [ ] Awareness authority and deputy chain written into the PSIRT runbook and the on-call rota
- [ ] DoC signing instrument executed; pre-signature checklist and counter-signature in use
- [ ] Residual-risk rule from guidance paras 156-163 written into the product-risk category (Section 5)
- [ ] Four forums scheduled with chairs and standing agendas
- [ ] Escalation paths published with working-day limits
- [ ] Annual review date set for the RACI, signing authority and on-call roster
