# Usage: python3 -I build_claims_enterprise.py            (from pack/enterprise/oj-verification/)
# Builds claims_enterprise.csv: every legal or guidance citation in the Enterprise papers (E1-E5, G, programme-case),
# with the exact source text relied on. Every quoted fragment is checked against the local copy of
# its source before the CSV is written; for guidance rows the fragment must occur inside the cited
# paragraph(s) or Example(s) of C(2026) 5252 (source/guidance/C_2026_5252_index.json), not merely
# somewhere in the document. The build fails if any fragment is not found.
import csv, json, re, sys

def norm(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-').replace('­', '')
    s = re.sub(r'(\w)- (\w)', r'\1-\2', s)
    s = re.sub(r'\s+', ' ', s).replace('( ', '(').strip()
    return s

def load(p):
    return norm(open(p, encoding='utf-8').read())

TXT = {
    'OJ': load('source/oj_L_2024_2847_EN.txt'),
    'G': load('source/guidance/C_2026_5252_annex_guidance_EN.txt'),
    'COMM': load('source/guidance/C_2026_5252_communication_EN.txt'),
    'FAQ': load('source/guidance/CRA_FAQ_v1.4_EN.md').replace('_', ''),
    'ENISA': load('source/guidance/ENISA_SRP_FAQ_2026-10-15.txt'),
    'IE': load('source/guidance/IE_NCSC_National_CRA_Guidelines_v1_2026-08-31.txt') + ' ' + load('source/guidance/IE_NCSC_CRA_page_2026-09-11.txt'),
    'IR': load('source/IR_2025_2392_EN.txt'),
    'PLD': load('source/PLD_2024_2853_EN.txt'),
}
IDX = json.load(open('source/guidance/C_2026_5252_index.json', encoding='utf-8'))

SRC = {
    'OJ': 'OJ L 2024/2847 EN (Publications Office cellar: PDF/A-2a edition and XHTML)',
    'OJC': 'OJ L 2024/2847 EN + corrigendum OJ L 2025/90555 (2.7.2025)',
    'G': 'Commission guidance C(2026) 5252 final, Annex, EN (27.7.2026), Commission PDF in source/guidance',
    'COMM': 'C(2026) 5252 final, Communication to the Commission (27.7.2026), source/guidance',
    'FAQ': 'Commission CRA FAQ v1.4 (4.9.2026), source/guidance',
    'ENISA': 'ENISA SRP FAQ (updated 15.10.2026), source/guidance',
    'IE': 'NCSC Ireland CRA page (11.9.2026) and National CRA Guidelines v1 (31.8.2026), source/guidance',
    'IR': 'OJ L 2025/2392 EN (cellar), source/IR_2025_2392_EN.txt',
    'PLD': 'OJ L 2024/2853 EN (cellar), source/PLD_2024_2853_EN.txt',
    'NONE': 'Not in E6 source set',
}

P = {
    'E1': 'pack/enterprise/evidence-as-code/paper.md',
    'E2': 'pack/enterprise/art14-operations/paper.md',
    'E3': 'pack/enterprise/portfolio-classification/paper.md',
    'E4': 'pack/enterprise/open-source-strategy/paper.md',
    'E5': 'pack/enterprise/global-control-set/paper.md',
    'G': 'pack/enterprise/google-outside-in/paper.md',
    'PCASE': 'pack/enterprise/programme-case/paper.md',
}

V, W, WA, NF, CNV = 'Verified', 'Verified with wording difference', 'Wrong article/point', 'Not found', 'Could not verify'

# Row: (id, claim, paper, location, cited, checks, source keys, status, correction)
# checks: list of (src, refs, fragment). refs: list of guidance refs like 'P13' or 'E2' (G rows only), or None.
R = []
def row(i, claim, paper, loc, cited, checks, srcs, status, corr=''):
    R.append((i, claim, P[paper] + ', ' + loc, cited, checks, srcs, status, corr))

g = lambda refs, frag: ('G', refs.split(), frag)
o = lambda frag: ('OJ', None, frag)
f = lambda src, frag: (src, None, frag)

# ---------------- E1 evidence-as-code ----------------
row('EAC-01', 'Placing on the market is judged per unit (Blue Guide, recalled by the guidance).', 'E1', 'table "Three rules", row 1', 'Guidance para 11',
    [g('P11', "to each individual product, not to a type of product")], 'G', V)
row('EAC-02', 'For standalone software, all copies of a version are deemed placed at its first commercial offering.', 'E1', 'table "Three rules", row 1', 'Guidance paras 13-14; Example 1',
    [g('P13', "the placing on the EU market is to be considered to have occurred at the moment of the first offering for distribution or use"),
     g('P14', "they are considered to be placed on the market at the same time, regardless of when possession or use of each individual copy is transferred"),
     g('E1', "Both copies of version 1.0.0 of software X are placed on the market on 1 January 2028")], 'G', V)
row('EAC-03', 'Non-substantial updates do not reset the placing date (cited as guidance paras 13-14).', 'E1', 'table "Three rules", row 1; field table row placing_on_market', 'Guidance paras 13-14 (as cited); correct: para 15 and Example 2',
    [g('P15', "Iterations that do not qualify as substantial modifications do not require the manufacturer to perform a new conformity assessment procedure and therefore do not modify that software's date of placement on the market"),
     g('E2', "Both copies of version 1.0.0 and 1.0.1 of software X are considered to be placed on the market on 1 January 2028")], 'G', WA,
    'Cite guidance paras 13-15 and Example 2. Paras 13-14 set the first-offering rule; the no-reset rule is para 15 and Example 2. Citation corrected in the paper (table row 1 and field table).')
row('EAC-04', 'Each new Lumen Browser, Lumen OS or app version is its own placing event; about 104,000 placing records a year; "placing on the market is judged per version for standalone software".', 'E1', 'executive answer; table "Three rules", row 1, effect column', 'Guidance paras 13-15; Example 2',
    [g('P15', "subsequent iterations of a software product with digital elements are considered as newly placed on the market when those iterations qualify as a 'substantial modification'"),
     g('E2', "issues an updated version 1.0.1 of software X that does not constitute a substantial modification"),
     g('P14', "those variants cannot be regarded as multiple copies of the same software product with digital elements")], 'G', NF,
    'The guidance says the opposite for non-substantial versions: they keep the placing date of the version they update (para 15, Example 2). New placings arise from a substantial modification (paras 15, 116, 122) or a distinct variant such as a build for another operating system (para 14). Keep one evidence record per version (technical documentation must stay up to date, Art 31(2); guidance para 113), but record non-substantial versions as "update to placed product" under the parent placing, and restate the 104,000 figure as version records, not placings. Substantive; not edited (see corrections_enterprise.md C-01 and legal-positions/positions.md, question B).')
row('EAC-05', 'Guidance point 110 sets four questions: new threat vectors, new attack scenarios, changed likelihood, changed impact.', 'E1', 'table "Three rules", row 2', 'Guidance para 110',
    [g('P110', "introduces new threat vectors"), g('P110', "enables new attack scenarios"), g('P110', "changes the likelihood of previously identified attack scenarios"), g('P110', "changes the potential impact of previously identified attack scenarios")], 'G', V,
    'Note the guidance frames these as factors manufacturers "may consider, in a non-exhaustive manner".')
row('EAC-06', 'All four answers negative means not substantial (points 111-112).', 'E1', 'table "Three rules", row 2', 'Guidance paras 111-112',
    [g('P111', "This may indicate that the update does not introduce new or increased cybersecurity risks, provided that the assumptions and mitigation measures relied upon in the risk assessment remain valid and effective. It is therefore likely that the update does not qualify as a substantial modification")], 'G', W,
    'The guidance says all-negative answers "may indicate" and make it "likely" that the update is not substantial, provided the risk-assessment assumptions remain valid. It is an indicator, not a rule.')
row('EAC-07', 'Security updates are "generally not" substantial (point 108).', 'E1', 'table "Three rules", row 2', 'Guidance para 108; Recital 39',
    [g('P108', "security updates are generally not to be regarded as substantial modifications"),
     o("Where a security update which is designed to decrease the level of cybersecurity risk of a product with digital elements does not modify the intended purpose of a product with digital elements, it is not considered to be a substantial modification")], 'G; OJ', V)
row('EAC-08', 'Changes of intended purpose or material boundary or dependency changes are substantial (point 109).', 'E1', 'table "Three rules", row 2', 'Guidance para 109',
    [g('P109', "a security update may qualify as a substantial modification where"), g('P109', "materially changes that product's boundaries or dependency structure in a way not foreseen in the risk assessment")], 'G', W,
    'Para 109 says such updates "may qualify", and only where the change was not foreseen in the risk assessment.')
row('EAC-09', 'A substantial modification is a new placing (point 116).', 'E1', 'table "Three rules", row 2; field table', 'Guidance para 116',
    [g('P116', "the act of making the substantially modified product available on the market constitutes a new placing on the market")], 'G', V)
row('EAC-10', 'A new placing needs a new or updated declaration (FAQ 6.8).', 'E1', 'table "Three rules", row 2; field table row declaration', 'FAQ 6.8; Art 28(2)',
    [f('FAQ', "a new version of the product might need a new declaration of conformity, especially when it implements a substantial modification"), o("Such a declaration shall be updated as appropriate")], 'FAQ; OJ', W,
    'FAQ 6.8 says a new version "might need" a new declaration, "especially" for a substantial modification; the binding rule is Art 28(2) ("updated as appropriate"). Art 28(2) added to the citation in the paper.')
row('EAC-11', 'Technical documentation and the declaration are kept 10 years after placing or for the support period, whichever is longer (Art 13(13)).', 'E1', 'table "Three rules", row 3; retention field; Q&A table', 'Art 13(13)',
    [o("for at least 10 years after the product with digital elements has been placed on the market or for the support period, whichever is longer")], 'OJ', V)
row('EAC-12', 'Annex II information follows the same retention rule (Art 13(18)).', 'E1', 'table "Three rules", row 3', 'Art 13(18)',
    [o("available online for at least 10 years after the product with digital elements has been placed on the market or for the support period, whichever is longer")], 'OJ', V)
row('EAC-13', 'Records must be retrievable for a market surveillance authority on reasoned request (Art 13(22)).', 'E1', 'table "Three rules", row 3; Q&A table', 'Art 13(22)',
    [o("upon a reasoned request from a market surveillance authority, provide that authority, in a language which can be easily understood by that authority")], 'OJ', V)
row('EAC-14', 'Product and version fields rest on Annex V pt 1, Annex VII pt 1, Annex II pt 3 and guidance paras 174-177.', 'E1', 'field table row product, version', 'Annex V pt 1; Annex VII pt 1(b); Annex II pt 3; guidance paras 174-177',
    [o("versions of software affecting compliance with essential cybersecurity requirements"), o("name and type and any additional information enabling the unique identification of the product with digital elements"),
     g('P175', "a single set of technical documentation")], 'OJ; G', V)
row('EAC-15', 'Placing field: Art 3(21); guidance paras 13-14; point 116.', 'E1', 'field table row placing_on_market', 'Art 3(21); guidance paras 13-15, Example 2; para 116',
    [o("the first making available of a product with digital elements on the Union market"), g('P15', "do not modify that software's date of placement on the market")], 'OJ; G', W,
    'Add para 15 and Example 2, which govern the placing date of non-substantial versions. Citation corrected in the paper.')
row('EAC-16', 'Classification field: Art 32(1)-(5); Annex VIII.', 'E1', 'field table row classification', 'Art 32(1)-(5)',
    [o("The manufacturer shall perform a conformity assessment of the product with digital elements")], 'OJ', V)
row('EAC-17', 'SBOM field: Annex I Part II(1); Annex VII pts 2(b) and 8; Art 13(24)-(25).', 'E1', 'field table row evidence.sbom', 'Annex I Part II(1); Annex VII pts 2(b), 8; Art 13(24)-(25)',
    [o("covering at the very least the top-level dependencies of the products"), o("including the software bill of materials, the coordinated vulnerability disclosure policy"),
     o("where applicable, the software bill of materials, further to a reasoned request from a market surveillance authority")], 'OJ', V)
row('EAC-18', 'Provenance field: Annex VII pt 2(c); Art 13(14).', 'E1', 'field table row evidence.provenance', 'Annex VII pt 2(c); Art 13(14)',
    [o("necessary information and specifications of the production and monitoring processes of the product with digital elements and the validation of those processes"),
     o("Manufacturers shall ensure that procedures are in place for products with digital elements that are part of a series of production to remain in conformity")], 'OJ', V,
    'Provisions exist; the provenance format is the paper\'s design choice, as it says.')
row('EAC-19', 'Vulnerability status field: Annex I Part I(2)(a); guidance paras 233-234; para 218.', 'E1', 'field table row evidence.vulnerability_status', 'Annex I Part I(2)(a); guidance paras 218, 233-234',
    [o("be made available on the market without known exploitable vulnerabilities"),
     g('P233', "A vulnerability should be regarded as known when it is listed in relevant publicly accessible vulnerability databases"),
     g('P234', "via coordinated disclosure by a security researcher or through the manufacturer's own internal testing")], 'OJ; G', V)
row('EAC-20', 'Tests field: Annex I Part II(3); Annex VII pt 6.', 'E1', 'field table row evidence.tests; Annex VII index', 'Annex I Part II(3); Annex VII pt 6',
    [o("apply effective and regular tests and reviews of the security of the product with digital elements"), o("reports of the tests carried out to verify the conformity")], 'OJ', V)
row('EAC-21', 'Risk assessment field: Art 13(2)-(4); Annex VII pt 3.', 'E1', 'field table row evidence.risk_assessment', 'Art 13(2)-(4); Annex VII pt 3',
    [o("The cybersecurity risk assessment shall be documented and updated as appropriate during a support period"), o("an assessment of the cybersecurity risks against which the product with digital elements is designed")], 'OJ', V)
row('EAC-22', 'User information, update design note and CVD policy fields: Annex II; Art 13(18); Annex VII pts 1(d), 2(b).', 'E1', 'field table', 'Annex II; Annex VII pts 1(d), 2(b)',
    [o("user information and instructions as set out in Annex II"), o("a description of the technical solutions chosen for the secure distribution of updates")], 'OJ', V)
row('EAC-23', 'Support period field: Art 13(8), 13(10), 13(19); guidance paras 125-128; Annex VII pt 4.', 'E1', 'field table row support_period', 'Art 13(8), (10), (19); guidance paras 125-128; Annex VII pt 4',
    [o("the support period shall be at least five years"), o("only for the version that it has last placed on the market"),
     o("relevant information that was taken into account to determine the support period pursuant to Article 13(8)"),
     g('P128', "Each substantially modified version of a software product with digital elements placed on the market has to have a declared support period that complies with Article 13(8)")], 'OJ; G', V)
row('EAC-24', 'Substantial-modification field: guidance points 104-112, 116, 122-123; Annex I Part II(2).', 'E1', 'field table row substantial_modification', 'Guidance paras 104-112, 116, 122-123; Annex I Part II(2)',
    [g('P122', "the substantially modified product with digital elements is to be considered as newly placed on the market"),
     g('P123', "the conformity assessment procedure should focus on the substantially modified parts"),
     o("where technically feasible, new security updates shall be provided separately from functionality updates")], 'G; OJ', V)
row('EAC-25', 'Declaration field: Art 13(12), 13(20), 28; Annex V.', 'E1', 'field table row declaration', 'Art 13(12), (20); Art 28; Annex V',
    [o("Before placing a product with digital elements on the market, manufacturers shall draw up the technical documentation referred to in Article 31"),
     o("it shall contain the exact internet address at which the full EU declaration of conformity can be accessed")], 'OJ', V)
row('EAC-26', 'Gate route rule: Class I on Module A needs a harmonised standard applied in full; Art 32(2) also allows a common specification or a "substantial" EU certification scheme.', 'E1', 'control table, row "Route and declaration"; decision 6', 'Art 32(2)',
    [o("has not applied or has applied only in part harmonised standards, common specifications or European cybersecurity certification schemes at assurance level at least 'substantial' as referred to in Article 27")], 'OJ', V,
    'Whether the scheme limb works before an Art 27(9) delegated act is open; the guidance reads it as requiring one (footnote 25 to para 148). See legal-positions question C.')
row('EAC-27', 'Gate blocks Class II products on Module A unless they use the FOSS route with public technical documentation (Art 32(5)), and blocks critical products on either Module A route.', 'E1', 'control table, row "Route and declaration"', 'Art 32(3)-(5); Art 8(1); guidance para 148',
    [o("Where the product is an important product with digital elements that falls under class II as set out in Annex III, the manufacturer shall demonstrate conformity"),
     o("shall be subject to the conformity assessment procedures referred to in Article 32(3)"),
     o("which fall under the categories set out in Annex III, shall be able to demonstrate conformity with the essential cybersecurity requirements set out in Annex I by using one of the procedures referred to in paragraph 1 of this Article, provided that the technical documentation referred to in Article 31 is made available to the public at the time of the placing on the market"),
     g('P148', "important products with digital elements of class II (with the exception of those qualifying as free and open-source software, in accordance with Article 32(5))")], 'OJ; G', V)
row('EAC-28', 'Module H quality-system audit looks for the trail of gate decisions (Annex VIII Module H pts 3-4).', 'E1', 'section on target architecture', 'Annex VIII Part IV pts 3-4',
    [o("The notified body shall assess the quality system to determine whether it satisfies the requirements referred to in point 3.2")], 'OJ', V)
row('EAC-29', 'Annex I Part II and the documentation duties apply from 11 Dec 2027; Art 14 reporting since 11 Sep 2026.', 'E1', 'rollout section', 'Art 71(2)',
    [o("This Regulation shall apply from 11 December 2027"), o("However, Article 14 shall apply from 11 September 2026")], 'OJ', V)
row('EAC-30', 'Each security update must stay available for at least 10 years or the rest of the support period, whichever is longer (Art 13(9)).', 'E1', 'storage sizing', 'Art 13(9)',
    [o("remains available after it has been issued for a minimum of 10 years or for the remainder of the support period, whichever is longer")], 'OJ', V)
row('EAC-31', 'Risks: "Guidance paras 13-14 make each software version a placing, while non-substantial updates \'do not reset\' the placing date."', 'E1', 'Risks and open questions, bullet 4', 'Guidance paras 13-15; Example 2',
    [g('P15', "therefore do not modify that software's date of placement on the market")], 'G', NF,
    'The quoted words "do not reset" are not in the guidance, and paras 13-15 do not make each version a placing. Proposed text: "Guidance paras 13-15 and Example 2 fix the placing date at the first offering of a version and keep it for later versions that are not substantially modified; only substantially modified versions and distinct variants are new placings." Not edited (substantive); corrections_enterprise.md C-02.')
row('EAC-32', 'A VEX "not_affected" statement is evidence that no Art 14 report was due (guidance para 218).', 'E1', 'Aldermoor assets table; Risks bullet 2', 'Guidance para 218',
    [g('P218', "cannot be exploited in its product with digital elements (e.g. because the vulnerable code is not reachable)"), g('P218', "it is not subject to mandatory reporting for that manufacturer")], 'G', V)
row('EAC-33', 'Guidance C(2026) 5252 was approved on 27 Jul 2026 but not formally adopted.', 'E1', 'Risks bullet 5', 'C(2026) 5252 Communication',
    [f('COMM', "The guidance in the Annex to the Communication will be formally adopted by the Commission at a later date, when all language versions are available. It is only from that moment that it will apply")], 'COMM', V,
    'No formal adoption found on the Commission CRA pages or in the OJ C series searched on 1 Nov 2026.')
row('EAC-34', 'Annex VII point 2(a) covers architecture drawings maintained outside the pipeline.', 'E1', 'Annex VII index excerpt', 'Annex VII pt 2(a)',
    [o("where applicable, drawings and schemes and a description of the system architecture")], 'OJ', V)

# ---------------- E2 art14-operations ----------------
row('A14-01', 'An actively exploited vulnerability is not limited to zero-days; n-day exploitation counts once there is reliable evidence (Art 3(42)).', 'E2', 'section 1, para 2', 'Art 3(42)',
    [o("a vulnerability for which there is reliable evidence that a malicious actor has exploited it in a system without permission of the system owner")], 'OJ', V)
row('A14-02', 'An upstream component vulnerability is reportable only where present, reachable and exploited in the product (guidance para 218).', 'E2', 'section 1, para 2; fan-out tier C', 'Guidance para 218',
    [g('P218', "if a manufacturer is aware that a third-party component contains a vulnerability, but that vulnerability either (i) cannot be exploited in its product with digital elements (e.g. because the vulnerable code is not reachable) or (ii) has not been exploited in its product with digital elements")], 'G', V)
row('A14-03', 'Same point under Commission FAQ 5.4.', 'E2', 'section 1, para 2; fan-out tier C', 'FAQ 5.4',
    [f('FAQ', "that vulnerability cannot be exploited in its product with digital elements, that vulnerability is not actively exploited, and therefore it is not subject to mandatory reporting")], 'FAQ', V)
row('A14-04', 'Art 14 has applied since 11 Sep 2026 to every in-scope product, including products already on the market (Art 69(3); Art 71(2)).', 'E2', 'section 2', 'Art 69(3); Art 71(2)',
    [o("However, Article 14 shall apply from 11 September 2026"), o("the obligations laid down in Article 14 shall apply to all products with digital elements that fall within the scope of this Regulation that have been placed on the market before 11 December 2027")], 'OJ', V)
row('A14-05', 'AEV clocks 24 h, 72 h and final report no later than 14 days after a corrective or mitigating measure is available (Art 14(2)(a)-(c)); both early clocks run from awareness.', 'E2', 'Exhibit 3', 'Art 14(2)(a)-(c)',
    [o("within 24 hours of the manufacturer becoming aware of it"), o("within 72 hours of the manufacturer becoming aware of the actively exploited vulnerability"), o("no later than 14 days after a corrective or mitigating measure is available")], 'OJ', V)
row('A14-06', 'Severe incident clocks 24 h, 72 h and final report within one month after submission of the 72 h notification (Art 14(4)(a)-(c)).', 'E2', 'Exhibit 3; Exhibit 4', 'Art 14(4)(a)-(c)',
    [o("within 72 hours of the manufacturer becoming aware of the incident"), o("within one month after the submission of the incident notification under point (b)")], 'OJ', V)
row('A14-07', 'Intermediate report on coordinator CSIRT request (Art 14(6)).', 'E2', 'Exhibit 3', 'Art 14(6)',
    [o("may request manufacturers to provide an intermediate report on relevant status updates")], 'OJ', V)
row('A14-08', 'Users must be informed "in a timely manner", failing which the coordinator CSIRT may inform them; "where appropriate, all users" (Art 14(8)).', 'E2', 'Exhibit 3; Exhibit 4', 'Art 14(8)',
    [o("the manufacturer shall inform the impacted users of the product with digital elements, and where appropriate all users"), o("Where the manufacturer fails to inform the users of the product with digital elements in a timely manner, the notified CSIRTs designated as coordinators may provide such information")], 'OJ', V)
row('A14-09', 'Awareness: the manufacturer "should assess the suspicious event immediately" and is aware once it has "a reasonable degree of certainty" (guidance para 213).', 'E2', 'section 2; Exhibit 4', 'Guidance para 213',
    [g('P213', "the manufacturer should assess the suspicious event immediately"), g('P213', "it has a reasonable degree of certainty")], 'G', V)
row('A14-10', 'The guidance remains an approved draft without formal adoption.', 'E2', 'section 2; Risks', 'C(2026) 5252 Communication',
    [f('COMM', "It is only from that moment that it will apply")], 'COMM', V)
row('A14-11', 'Good-faith research and bug-bounty findings without exploitation evidence are not reportable (FAQ 5.2).', 'E2', 'section 2', 'FAQ 5.2; Recital 68',
    [f('FAQ', "disclosed to the product's manufacturer as part of its bug-bounty programme (see Recital 76) is not an actively exploited vulnerability subject to mandatory reporting")], 'FAQ', V)
row('A14-12', 'Exploitation known before 11 Sep 2026 is not reported retroactively (guidance paras 217-218).', 'E2', 'section 2', 'Guidance para 217',
    [g('P217', "the manufacturer is not required to report vulnerabilities of whose active exploitation it had already become aware before 11 September 2026")], 'G', V,
    'The rule is in para 217; para 218 covers components.')
row('A14-13', 'The SRP 72-hour counter shows a due time 48 hours after the early warning (ENISA SRP FAQ 26).', 'E2', 'section 2; Risks', 'ENISA SRP FAQ 26',
    [f('ENISA', "the 72-hour counter displays a due date/time 48hrs after submission of the 24-hour Early Warning")], 'ENISA', V)
row('A14-14', 'Ireland\'s National CRA Guidelines describe the detailed notification as due "within 48 hours of the early warning".', 'E2', 'section 2; Exhibit 4; Risks', 'Irish National CRA Guidelines v1; NCSC CRA page',
    [f('IE', "the Detailed Notification must be submitted within 48hrs of the EW submission"), f('IE', "Must be submitted within 48 hours of the Early Warning submission (72 hours total from initial awareness)")], 'IE', W,
    'The Guidelines say "within 48hrs of the EW submission"; the quoted wording matches the NCSC web page, which adds "(72 hours total from initial awareness)". Cite the page for the quotation. Citation corrected in the paper.')
row('A14-15', 'ENISA: "Only one notification is required for any given actively exploited vulnerability (AEV) or severe incident (SI)", in the context of a manufacturer with several EU branches (FAQ 8).', 'E2', 'section 3', 'ENISA SRP FAQ 8',
    [f('ENISA', "Only one notification is required for any given actively exploited vulnerability (AEV) or severe incident (SI), even when a manufacturer has multiple branches or subsidiaries in the EU")], 'ENISA', V)
row('A14-16', 'A wrong choice of coordinator "may invalidate the notification" (FAQ 18).', 'E2', 'section 3; Risks', 'ENISA SRP FAQ 18',
    [f('ENISA', "If the wrong CDaC is selected, the notification may be invalidated and will need to be resubmitted to the correct CDaC")], 'ENISA', W,
    'ENISA wording: "the notification may be invalidated and will need to be resubmitted to the correct CDaC". Quotation corrected in the paper.')
row('A14-17', 'Art 14(8) is risk-based: detail may go first to affected customers, broader disclosure once mitigated (guidance paras 219-221).', 'E2', 'Exhibit 4; section on disclosure', 'Guidance paras 219-221',
    [g('P220', "is to be applied in a risk-based and proportionate manner"), g('P220', "manufacturers may limit the disclosure of detailed information to the relevant users or customers concerned"),
     g('P221', "Once the vulnerability has been adequately addressed or mitigated, broader disclosure may be appropriate")], 'G', V)
row('A14-18', 'Upstream report and fix share (Art 13(6); guidance 9.2.1).', 'E2', 'Exhibit 4', 'Art 13(6); guidance paras 222-229',
    [o("report the vulnerability to the person or entity manufacturing or maintaining the component"), g('P226', "are required to share that software modification ('security fix') with the person or entity manufacturing or maintaining the component")], 'OJ; G', V)
row('A14-19', 'Upstream duty is met internally when Aldermoor leads the project.', 'E2', 'disclosure rules, point 4', 'Guidance para 223',
    [g('P223', "manufacturers are not required to report upstream where they can confirm that the person or entity manufacturing or maintaining a component is aware of the existence of a vulnerability")], 'G', V,
    'Supported by para 223 where the steward is aware; the fix-sharing duty (para 226) still applies across legal entities.')
row('A14-20', 'Coordinator CSIRT under Art 14(7): main establishment where cybersecurity decisions are predominantly taken, then most employees; only with no EU main establishment the authorised representative, importer, distributor, most users.', 'E2', 'section 4', 'Art 14(7)',
    [o("where the decisions related to the cybersecurity of its products with digital elements are predominantly taken"), o("the establishment with the highest number of employees in the Union"),
     o("Where a manufacturer has no main establishment in the Union")], 'OJ', V)
row('A14-21', 'Ireland\'s NCSC fallback address is usable only once ENISA declares an outage.', 'E2', 'section 4', 'NCSC CRA page',
    [f('IE', "Submissions via email will ONLY be accepted when the SRP is officially declared offline by ENISA")], 'IE', V)
row('A14-22', 'Dissemination can be delayed under Art 14(9), Art 16(2) and Delegated Regulation (EU) 2026/881.', 'E2', 'disclosure section', 'Art 14(9); Art 16(2); Del. Reg. 2026/881',
    [o("specifying the terms and conditions for applying the cybersecurity-related grounds in relation to delaying the dissemination of notifications as referred to in Article 16(2)")], 'OJ', V,
    'Delegated Regulation (EU) 2026/881 verified in the base register (R14).')
row('A14-23', 'Steward duties under Art 24(3) apply from 11 Dec 2027.', 'E2', 'disclosure rules, point 4; Risks', 'Art 24(3); Art 71(2); FAQ 5.5',
    [f('FAQ', "In accordance with Article 71(2) of the CRA, Article 24(3) shall apply from 11 December 2027")], 'FAQ', V)
row('A14-24', 'NIS2 regulates entities and the CRA products; cloud services matter to the CRA only as remote data processing (KB 13).', 'E2', 'disclosure section', 'Recital 12',
    [o("Directive (EU) 2022/2555 applies to cloud computing services and cloud service models")], 'OJ', V)
row('A14-25', 'Digital Omnibus COM(2025) 837 and Council mandate ST 14756/26.', 'E2', 'disclosure section', 'COM(2025) 837; ST 14756/26',
    [], 'NONE', CNV, 'Proposal and Council mandate are outside the OJ; rely on reports/verification.md claim 20.')
row('A14-26', 'ENISA FAQ: "no Application Programming Interface (API) will be provided at the initial release of the SRP", API "may be considered in a future phase", "Since its launch, the platform is available in English only".', 'E2', 'tooling section', 'ENISA SRP FAQ 15, 24',
    [f('ENISA', "no Application Programming Interface (API) will be provided at the initial release of the SRP"), f('ENISA', "API functionality may be considered in a future phase of the SRP"), f('ENISA', "Since its launch, the platform is available in English only")], 'ENISA', V)
row('A14-27', 'One Primary and up to 20 Secondary Assigned Representatives; personal EU Login with MFA; up to 20 notifications before CSIRT verification; drafts visible only to their creator.', 'E2', 'Exhibit 6', 'ENISA SRP FAQ 9',
    [f('ENISA', "There can be only one Primary AR per manufacturer and up to 20 Secondary ARs"), f('ENISA', "may submit up to 20 notifications for that manufacturer before verification becomes mandatory"),
     f('ENISA', "Drafts are stored locally in the individual AR's account")], 'ENISA', V)
row('A14-28', 'SRP outages require waiting (FAQ 25).', 'E2', 'Risks', 'ENISA SRP FAQ 25',
    [f('ENISA', "manufacturers should wait until it becomes available again and then submit the required notification")], 'ENISA', V)
row('A14-29', 'Fines reach EUR 15m or 2.5% of worldwide turnover, whichever is higher (Art 64(2)); enforcement applies from 11 Dec 2027.', 'E2', 'Risks', 'Art 64(2); Art 71(2)',
    [o("administrative fines of up to EUR 15 000 000 or, if the offender is an undertaking, up to 2,5 % of the its total worldwide annual turnover for the preceding financial year, whichever is higher")], 'OJ', V)
row('A14-30', 'Whether one SRP record can carry several distinct products is not addressed by ENISA\'s FAQ (15 Oct 2026).', 'E2', 'Risks; section 3', 'ENISA SRP FAQ; guidance section 9.1',
    [], 'ENISA', V, 'Confirmed by reading the full ENISA FAQ (35 questions) and guidance paras 209-221: neither addresses several products of one manufacturer in one record. See legal-positions question A.')

# ---------------- E3 portfolio-classification ----------------
row('PC-01', 'A smartphone integrating an operating system is not an operating system (guidance Example 58).', 'E3', 'section 1; Exhibit 6 rank 2', 'Guidance Example 58',
    [g('E58', "The mere integration of an operating system does not mean that the smartphone has the core functionality of an operating system")], 'G', V)
row('PC-02', 'Browser-only software is not a product, so the cloud consoles are out (guidance paras 20-21, Examples 5-6).', 'E3', 'rule 1', 'Guidance paras 20-21; Examples 5-6',
    [g('P21', "software that executes remotely and is merely accessed by the user is not, on that basis alone, a product with digital elements"),
     g('E5', "a web application accessed by the user exclusively through a web browser is not a product with digital elements")], 'G', V)
row('PC-03', 'Hosted services fall to NIS2 unless an installed product needs them, when they become that product\'s remote data processing (recital 12; Art 3(2)).', 'E3', 'rule 1', 'Recital 12; Art 3(2)',
    [o("Directive (EU) 2022/2555 applies to cloud computing services and cloud service models"),
     o("data processing at a distance for which the software is designed and developed by the manufacturer, or under the responsibility of the manufacturer, and the absence of which would prevent the product with digital elements from performing one of its functions")], 'OJ', V)
row('PC-04', 'Each product has exactly one core functionality (guidance point 144).', 'E3', 'rule 2', 'Guidance para 144',
    [g('P144', "A product with digital elements may not have more than one core functionality for the purposes of determining the applicable conformity assessment regime")], 'G', V)
row('PC-05', 'Core functionality is read objectively from instructions, marketing and technical documentation; inconsistency indicates misrepresentation (points 142-143).', 'E3', 'rule 2', 'Guidance paras 139, 142-143',
    [g('P139', "manufacturer supplies in the instructions for use, promotional or sales materials and statements, as well as in the technical documentation"),
     g('P142', "considered objectively in light of its intended purpose, and not on the way in which the product with digital elements is described or marketed"),
     g('P143', "where there are clear inconsistencies between promotional materials, instructions for use, and technical documentation")], 'G', W,
    'The list of sources (instructions, marketing, documentation) is para 139; para 142 adds that marketing does not override actual technical characteristics. Citation corrected to "pts 139, 142-143".')
row('PC-06', 'Integration does not reclassify the host (Art 7(1); Example 58).', 'E3', 'rule 3; Exhibit 6 rank 8', 'Art 7(1); guidance para 141',
    [o("shall not in itself render the product in which it is integrated subject to the conformity assessment procedures referred to in Article 32(2) and (3)"),
     g('P141', "the mere integration of an important or critical product with digital elements does not in itself render the product with digital elements an important or critical product")], 'OJ; G', V)
row('PC-07', 'A router with a firewall stays a router (IR 2025/2392 recitals; guidance point 152, Example 63).', 'E3', 'rule 3', 'IR 2025/2392 recital 4; guidance para 152; Example 63',
    [f('IR', "a router integrating firewall functionality"), g('P152', "it is the core functionality of the product with digital elements as a whole"),
     g('E63', "A hardware product with digital elements has the core functionality of a router")], 'IR; G', V)
row('PC-08', 'A module sold or licensed separately takes its own class (guidance point 145, Example 61).', 'E3', 'rule 4; Exhibit 6 rank 7', 'Guidance para 145; Example 61',
    [g('P145', "those modules constitute standalone products with digital elements in their own right"),
     g('E61', "The intrusion detection system is subject to the conformity assessment regime for important products with digital elements of class II")], 'G', V)
row('PC-09', 'Open-source Cloud SDKs used to monetise cloud services make Aldermoor their manufacturer (guidance point 54).', 'E3', 'rule 5', 'Guidance para 54',
    [g('P54', "where it provides the software through which it monetises other products with digital elements or services")], 'G', V)
row('PC-10', 'Tensile LTS builds offered only to paying customers are placed on the market (point 57, Example 17).', 'E3', 'rule 5', 'Guidance para 57; Example 17; para 46',
    [g('P57', "access to a specific version of the product with digital elements including certain benefits such as technical assistance or performance optimisation, is conditioned on remuneration"),
     g('E17', "The paid version of the operating system is considered placed on the market"),
     g('P46', "software distributed under a free and open-source licence but whose source code is only shared (or allowed to be shared) with paying customers or a limited group of users is not to be considered FOSS")], 'G', V,
    'Add para 46: if LTS source is shared only with paying customers, the LTS build is not FOSS at all, so Art 32(5) would not be available for it.')
row('PC-11', 'Art 32(2) allows Module A for Class I only where harmonised standards, common specifications or certification schemes at "substantial" "as referred to in Article 27" are applied in full.', 'E3', 'route strategy section', 'Art 32(2)',
    [o("European cybersecurity certification schemes at assurance level at least 'substantial' as referred to in Article 27")], 'OJ', V)
row('PC-12', 'Whether a scheme can serve before an Art 27(9) act is an open interpretation (module E6).', 'E3', 'route strategy section', 'Art 32(2); Art 27(8)-(9); guidance para 148 footnote 25, para 153; recital 91',
    [g('P153', "if this has been specified via delegated acts in accordance with Article 27(9)"),
     f('G', "the same guidance also applies to common specifications adopted in accordance with Article 27(2) and to European cybersecurity certification schemes where specified by the Commission via delegated acts in accordance with Article 27(9)"),
     o("European cybersecurity certification schemes adopted pursuant to Regulation (EU) 2019/881 which have been identified by the Commission in an implementing act")], 'G; OJ', W,
    'Still open in law, but the Commission guidance now takes a side: the scheme limb applies only to schemes specified by an Art 27(9) delegated act (footnote 25; para 153). Recital 91 also speaks of schemes "identified by the Commission". Citation to footnote 25 added in the paper. See legal-positions question C.')
row('PC-13', 'Module A for Class I families where a cited vertical standard is applied in full and covers the core-functionality risks (guidance point 149).', 'E3', 'Exhibit 3', 'Guidance para 149',
    [g('P149', "all the applicable requirements of a relevant harmonised standard need to be applied; and (ii) the standard's scope needs to cover at least all the cybersecurity risks associated to that product's core functionality")], 'G', V)
row('PC-14', 'Module H suits frequent substantial modifications because new variants extend the approved system (FAQ 6.3).', 'E3', 'route strategy section', 'FAQ 6.3',
    [f('FAQ', "since it streamlines the relevant conformity assessment procedures for each new or substantially modified product"), f('FAQ', "The manufacturer can extend the scope of the described quality system to new or substantially modified products")], 'FAQ', V)
row('PC-15', 'Under Module H the notified body\'s number follows the CE marking (Art 30(4)); for software the CE marking goes on the declaration or website (Art 30(1)).', 'E3', 'route strategy section', 'Art 30(1), (4)',
    [o("The CE marking shall be followed by the identification number of the notified body"), o("the CE marking shall be affixed either to the EU declaration of conformity referred to in Article 28 or on the website")], 'OJ', V)
row('PC-16', 'Art 32(5) applies only to FOSS and requires the Annex VII documentation to be public at placing.', 'E3', 'route strategy section', 'Art 32(5)',
    [o("provided that the technical documentation referred to in Article 31 is made available to the public at the time of the placing on the market")], 'OJ', V)
row('PC-17', 'Type examination needs focused re-assessment for each substantial modification (guidance points 116, 122-123).', 'E3', 'notified-body demand section', 'Guidance paras 116, 122-123',
    [g('P123', "where a third-party conformity assessment is performed, the conformity assessment body should focus its assessment on the substantially modified parts")], 'G', V)
row('PC-18', 'Change notices (Annex VIII Module B pt 7) and periodic audits of vulnerability handling (pt 8).', 'E3', 'notified-body demand section', 'Annex VIII Part II pts 7-8',
    [o("Such modifications shall require additional approval in the form of an addition to the original EU-type examination certificate"), o("The notified body shall carry out periodic audits to ensure that the vulnerability handling processes")], 'OJ', V)
row('PC-19', 'Module H: one model\'s technical documentation per product category (pts 3.1(b), 3.3), surveillance audits (pt 4), change notices (pt 3.5).', 'E3', 'notified-body demand section; controls 3', 'Annex VIII Part IV pts 3.1(b), 3.5, 4',
    [o("the technical documentation for one model of each category of products with digital elements intended to be manufactured or developed"), o("informed of any intended change to the quality system")], 'OJ', V)
row('PC-20', 'Under Commission guidance (paras 13-14) placing on the market is per version for standalone software.', 'E3', 'notified-body demand section, "Version discipline"', 'Guidance paras 13-15; Example 2',
    [g('P15', "Iterations that do not qualify as substantial modifications do not require the manufacturer to perform a new conformity assessment procedure")], 'G', NF,
    'As EAC-04: non-substantial versions keep the original placing date. The paper\'s conclusion (the pt 110 test keeps examination cost down) still holds. Not edited (substantive); corrections_enterprise.md C-03.')
row('PC-21', 'Security updates are "generally not" substantial (point 108); four-question test (point 110).', 'E3', 'notified-body demand section', 'Guidance paras 108, 110',
    [g('P108', "security updates are generally not to be regarded as substantial modifications"), g('P110', "manufacturers may consider, in a non-exhaustive manner, whether the software update")], 'G', V)
row('PC-22', 'Art 35(2) only asks Member States to "strive" for sufficient notified bodies by 11 Dec 2026.', 'E3', 'notified-body demand section', 'Art 35(2)',
    [o("Member States shall strive to ensure, by 11 December 2026 that there is a sufficient number of notified bodies")], 'OJ', V)
row('PC-23', 'Module H bodies need ISO/IEC 17021-1 accreditation.', 'E3', 'notified-body demand section', 'None in the CRA',
    [], 'NONE', CNV, 'Not in the CRA text (as base register K25). Label as accreditation practice.')
row('PC-24', 'Notified bodies must be independent of Aldermoor (Art 39); a body selling Aldermoor consultancy is conflicted.', 'E3', 'notified-body demand section; decision 2', 'Art 39(3), (5)',
    [o("A conformity assessment body shall be a third-party body independent of the organisation or the product with digital elements it assesses"), o("This shall in particular apply to consultancy services")], 'OJ', V)
row('PC-25', 'Arc phones are default (Example 58; FAQ s.3; guidance Example 8).', 'E3', 'Exhibit 6, rank 2', 'Guidance Example 58; FAQ 3.2; Example 8 (as cited)',
    [g('E58', "the smartphone as a whole has a different core functionality"), g('E8', "A network printer is placed on the market as a hardware product with digital elements")], 'G', WA,
    'Example 8 is about a printer and its drivers forming one product; it does not support the default class. Replace with guidance para 141. Citation corrected in the paper.')
row('PC-26', 'Supply model, contracts and documentation must match (points 142-145).', 'E3', 'Exhibit 6, rank 1', 'Guidance paras 142-145',
    [g('P145', "Where a manufacturer also makes those modules available on the market separately")], 'G', V)
row('PC-27', 'Keystone: Annex IV item 3 if the secure element is designed to AVA_VAN.4 or higher and a USB key counts as a "carrier"; an Art 8(1) act could mandate EUCC with at least 6 months\' transition.', 'E3', 'Exhibit 6, rank 4', 'Annex IV pt 3; IR 2025/2392 Annex II pt 3; Art 8(1)',
    [o("Smartcards or similar devices, including secure elements"), f('IR', "Secure elements are designed to provide protection of at least AVA_VAN.4"),
     f('IR', "secure elements integrated into carrier materials taking other shapes"), o("shall provide for a minimum transitional period of six months")], 'OJ; IR', V,
    'IR 2025/2392 expressly includes secure elements "integrated into carrier materials taking other shapes"; see legal-positions question G.')
row('PC-28', 'Smoke and CO alarms default; alternative I.17 "alarm systems".', 'E3', 'Exhibit 6, rank 5', 'Annex III Class I pt 17',
    [o("Smart home products with security functionalities, including smart door locks, security cameras, baby monitoring systems and alarm systems")], 'OJ', V)
row('PC-29', 'Aldermoor Edge Class II.1 (virtualised execution); Edge Firewall add-on Class II.2 when sold separately (Example 61).', 'E3', 'Exhibit 6, rank 7', 'Annex III Class II pts 1-2; Example 61',
    [o("Hypervisors and container runtime systems that support virtualised execution of operating systems and similar environments"), o("Firewalls, intrusion detection and prevention systems")], 'OJ', V)
row('PC-30', 'Bastion integrated; host not reclassified (Art 7(1); FAQ laptop example).', 'E3', 'Exhibit 6, rank 8', 'Art 7(1); FAQ 3.2',
    [f('FAQ', "integrating a secure element into a laptop does not in itself render the laptop subject to the conformity assessment procedure")], 'FAQ', V)
row('PC-31', 'Families may share one risk assessment and technical file where architecture, security design, intended purpose and risks are the same (guidance points 174-177).', 'E3', 'controls, item 1', 'Guidance paras 174-177',
    [g('P174', "share the same architecture, security-relevant design and intended purpose, and are exposed to the same cybersecurity risks")], 'G', V)
row('PC-32', 'Core-functionality statement goes into Annex VII item 1(a).', 'E3', 'controls, item 1', 'Annex VII pt 1(a); guidance para 144',
    [o("its intended purpose"), g('P144', "The product's core functionality should therefore be clearly identified")], 'OJ; G', V)
row('PC-33', 'Wrong-route choices can attract fines under Art 64(3) (guidance point 146).', 'E3', 'controls, item 5', 'Art 64(3); guidance para 146',
    [g('P146', "Non-compliance with the obligations set out in Article 32 of the CRA may trigger administrative fines in accordance with Article 64(3)"), o("Article 32(1), (2) and (3)")], 'G; OJ', V)
row('PC-34', 'Module H surveillance: Annex VIII Part IV pt 4 gives site access and periodic audits (4.1-4.3), no unexpected-visit clause.', 'E3', 'Risks', 'Annex VIII Part IV pt 4',
    [o("Surveillance under the responsibility of the notified body")], 'OJ', V, 'As base register K11 and O08.')
row('PC-35', 'Free, unmonetised, non-FOSS company apps are a grey area (guidance points 40-41).', 'E3', 'Risks', 'Guidance paras 40-41',
    [g('P40', "can only be appreciated on a case- by-case basis")], 'G', V)
row('PC-36', 'A Pulse feature certified under Regulation (EU) 2017/745 takes that model out of CRA scope.', 'E3', 'Risks', 'Art 2(2)(a)',
    [o("This Regulation does not apply to products with digital elements to which the following Union legal acts apply"), o("Regulation (EU) 2017/745")], 'OJ', V)
row('PC-37', 'Annex III item numbers used in the register: I.1, I.2, I.5, I.11, I.12, I.16, I.17, I.19, II.1.', 'E3', 'Exhibits 2-3', 'Annex III',
    [o("Standalone and embedded browsers"), o("Operating systems"), o("Products with digital elements with the function of virtual private network (VPN)"), o("Smart home general purpose virtual assistants"),
     o("Routers, modems intended for the connection to the internet, and switches"), o("Personal wearable products to be worn or placed on a human body that have a health monitoring")], 'OJ', V)
row('PC-38', 'No CRA harmonised standard or common specification exists at 30 Oct 2026; no notified body at 8 Sep 2026.', 'E3', 'route strategy; Risks', 'None (status facts)',
    [], 'NONE', CNV, 'Outside the OJ text; rely on reports/verification.md claims 21-23.')

# ---------------- E4 open-source-strategy ----------------
row('OSS-01', 'Steward regime from 11 Dec 2027 with no administrative fines (Art 64(10)(b), as corrected by OJ L, 2025/90555).', 'E4', 'executive answer; Exhibit 2', 'Art 64(10)(b); corrigendum 2025/90555',
    [o("any infringement of this Regulation")], 'OJC', V, 'Corrected text "paragraphs 2 to 9" verified in base register F20b.')
row('OSS-02', 'Article 2 never mentions open source; the carve-out works through Art 3(22), read with recitals 15-20.', 'E4', 'section 1', 'Art 2; Art 3(22); recitals 15-20',
    [o("the supply of a product with digital elements for distribution or use on the Union market in the course of a commercial activity")], 'OJ', V, 'Checked: Art 2 contains no reference to open source.')
row('OSS-03', 'A steward is a legal person, other than a manufacturer, that systematically supports specific FOSS intended for commercial activities on a sustained basis (Art 3(14)).', 'E4', 'section 1', 'Art 3(14)',
    [o("a legal person, other than a manufacturer, that has the purpose or objective of systematically providing support on a sustained basis for the development of specific products with digital elements")], 'OJ', V)
row('OSS-04', 'Status is assessed per project; one company can be steward for one codebase and manufacturer for another (guidance points 69-74).', 'E4', 'section 1', 'Guidance paras 72-74',
    [g('P73', "A legal person may therefore simultaneously be a steward for one specific FOSS"), g('P74', "For each specific FOSS that it publishes, the legal person will need to ascertain whether that FOSS is considered to be placed on the market")], 'G', V)
row('OSS-05', 'Unmonetised FOSS a company also integrates: steward for the FOSS, manufacturer for its products (points 67-68, 76; Examples 25, 26, 29).', 'E4', 'Exhibit 1 row 1', 'Guidance paras 67-68, 76; Examples 25, 26, 29',
    [g('P76', "a legal entity that develops FOSS for integration into its own products with digital elements and then publishes it without placing it on the market"),
     g('E25', "The legal person that publishes it is its steward"), g('E29', "Company A is not its manufacturer, but is its steward")], 'G', V)
row('OSS-06', 'Charging for binaries, updates or a specific supported version, even with a free equivalent, makes the publisher the manufacturer of what is charged for (points 51, 57; Example 17).', 'E4', 'Exhibit 1 row 2', 'Guidance paras 51, 57; Example 17',
    [g('P51', "charges a price for the software itself (e.g. by charging a price for the pre-compiled binaries)"), g('P57', "irrespective of whether functionally equivalent software is also available free of charge")], 'G', V)
row('OSS-07', 'Open core: manufacturer for the paid edition, steward for the community edition (points 52-53; Example 30).', 'E4', 'Exhibit 1 row 3', 'Guidance paras 52-53; Example 30',
    [g('P52', "The version provided for free (or community version) is not monetised and therefore is not considered to be placed on the market"),
     g('P53', "that legal person is also subject to the obligations on stewards for the version it supplies for free")], 'G', V)
row('OSS-08', 'FOSS used to monetise other products or services is placed on the market (point 54; Examples 14-16).', 'E4', 'Exhibit 1 row 4', 'Guidance para 54; Examples 14-16',
    [g('E15', "That application allows that person to monetise other services offered through it")], 'G', V)
row('OSS-09', 'Donations or membership that gate access, essential functions or updates, or buy contractual benefits make the publisher a manufacturer (points 60-62; Examples 20-22).', 'E4', 'Exhibit 1 row 5', 'Guidance paras 60-62; Examples 20-22',
    [g('P62', "where access to the FOSS, to essential functionalities or to updates is conditioned in practice on making a donation, or where donations are associated with contractual benefits")], 'G', W,
    'Points 60-62 concern donations only; "membership" is not mentioned there. Membership fees paid to a not-for-profit are treated in para 66 and Example 33 (steward, not manufacturer).')
row('OSS-10', 'Paid consulting, training or support sold separately while software and maintenance stay free: not placed (points 55-56; Example 18).', 'E4', 'Exhibit 1 row 6', 'Guidance paras 55-56; Example 18',
    [g('P56', "The decisive factor is whether access to the FOSS itself (i.e. the provision of the product with digital elements), including its maintenance, is conditioned on remuneration")], 'G', V)
row('OSS-11', 'Not-for-profit foundation is steward; companies owe due diligence (points 66, 76-78; Examples 24, 28, 33).', 'E4', 'Exhibit 1 row 7; Exhibit 6', 'Guidance paras 66, 76-78; Examples 24, 28, 33',
    [g('P78', "Such foundations are to be considered stewards in relation to specific FOSS which are intended for commercial activities")], 'G', V)
row('OSS-12', 'Contributor with commit rights on a project it does not control is neither manufacturer nor steward (recital 18; points 48-49, 85-86; Example 13).', 'E4', 'Exhibit 1 row 8; Exhibit 6', 'Recital 18; guidance paras 48-49, 85-86; Example 13',
    [g('P49', "The mere existence of technical permissions, such as commit access, is not sufficient to establish that the FOSS is under that person's responsi")], 'G', V)
row('OSS-13', 'A steward that starts monetising becomes manufacturer from that date, not for earlier versions (point 84).', 'E4', 'Exhibit 1 row 9; section 3', 'Guidance para 84',
    [g('P84', "from the date on which it places it on the market (but not in respect of earlier versions for which it acted as a steward)")], 'G', V)
row('OSS-14', 'Financing and regular releases do not decide commerciality (recital 18).', 'E4', 'section 1', 'Recital 18',
    [o("how the development has been financed, should therefore not be taken into account"), o("the mere presence of regular releases should not in itself lead to the conclusion")], 'OJ', V)
row('OSS-15', 'Art 24(1) policy content; Art 24(2) cooperation and documentation on reasoned request.', 'E4', 'Exhibit 2', 'Art 24(1)-(2)',
    [o("put in place and document in a verifiable manner a cybersecurity policy"), o("promote the sharing of information concerning discovered vulnerabilities within the open-source community"),
     o("open-source software stewards shall provide that authority, in a language which can be easily understood by that authority, with the documentation referred to in paragraph 1")], 'OJ', V)
row('OSS-16', 'Infrastructure-support stewards notify severe incidents and inform users (Art 24(3) via Art 14(3), (8); point 81).', 'E4', 'Exhibit 2', 'Art 24(3); guidance para 81',
    [o("The obligations laid down in Article 14(3) and (8) shall apply to open-source software stewards to the extent that severe incidents"),
     g('P81', "it is required to notify ENISA and the CSIRTs, in accordance with Article 14(3) of any severe incidents related to that infrastructure")], 'OJ; G', V)
row('OSS-17', 'Engineering-support stewards notify AEVs (Art 24(3) via 14(1); point 82); Art 24(3) applies Art 14(8) only to the infrastructure limb, so informing users is guidance-led good practice.', 'E4', 'Exhibit 2', 'Art 24(3); guidance para 82',
    [o("The obligations laid down in Article 14(1) shall apply to open-source software stewards to the extent that they are involved in the development"),
     g('P82', "To the extent that the steward also has a direct relationship with impacted users, it is also required to inform them directly, in accordance with Article 14(8)")], 'OJ; G', V,
    'The paper reads the OJ correctly. Note that guidance para 82 goes further than Art 24(3) and calls user information "required"; the paper\'s caution is right, but say the guidance states it as a requirement.')
row('OSS-18', 'Stewards: no CE marking, conformity assessment, Annex I duties, technical documentation or SBOM; no fines under any Art 64 tier (recitals 19, 120; Art 64(10)(b)).', 'E4', 'Exhibit 2', 'Recitals 19, 120; Art 64(10)(b)',
    [o("they should not be permitted to affix the CE marking to the products with digital elements whose development they support"),
     o("nor to open-source software stewards for any infringement of this Regulation")], 'OJ', V)
row('OSS-19', 'Residual enforcement: an authority may require corrective action (Art 52(3)).', 'E4', 'Exhibit 2', 'Art 52(3)',
    [o("it shall require the open-source software steward to ensure that all appropriate corrective actions are taken")], 'OJ', V)
row('OSS-20', 'Steward duties start 11 Dec 2027; before then reports are voluntary (Art 71(2); Art 15).', 'E4', 'Exhibit 2; section 2', 'Art 71(2); Art 15; FAQ 5.5',
    [f('FAQ', "Article 24(3) shall apply from 11 December 2027"), o("may notify any vulnerability contained in a product with digital elements as well as cyber threats")], 'FAQ; OJ', V)
row('OSS-21', 'Integrating FOSS never transfers compliance responsibility to the project; the project never becomes responsible for the product (guidance points 86-88).', 'E4', 'section 3; section 5', 'Guidance paras 86-88',
    [g('P86', "also do not become responsible for such components' individual compliance with the CRA"), g('P87', "Maintainers of FOSS components that are not placed on the market do not bear obligations in relation to other entities")], 'G', V)
row('OSS-22', 'Due diligence (Art 13(5)); upstream report to "the person or entity manufacturing or maintaining the component" and fix sharing (Art 13(6)); documentation (Art 13(7)); SBOM need not be public (recital 77).', 'E4', 'section 3', 'Art 13(5)-(7); Annex I Part II(1); recital 77',
    [o("including when integrating components of free and open-source software that have not been made available on the market in the course of a commercial activity"),
     o("report the vulnerability to the person or entity manufacturing or maintaining the component"), o("Manufacturers should not be obliged to make the SBOM public")], 'OJ', V)
row('OSS-23', 'Annex III item numbers: Halo Wear OS item 11; Lumen browsers and WebView item 2; Edge Class II item 1.', 'E4', 'Exhibit 3', 'Annex III',
    [o("Operating systems"), o("Standalone and embedded browsers")], 'OJ', V)
row('OSS-24', 'Monetisation analysis: Tensile pt 57/Ex 17; HOSP pts 57, 60-62 by analogy and pt 54; Lumen Engine LTS pt 57; Examples 24, 33; Mooring pts 52-53, Example 30.', 'E4', 'Exhibit 4', 'Guidance paras 52-62; Examples 17, 24, 30, 33',
    [g('E24', "The browser is not considered to be placed on the market within the meaning of the CRA"), g('E33', "Funding is provided through membership fees paid to the not-for-profit entity")], 'G', V)
row('OSS-25', 'Art 32(5) lets FOSS in an Annex III category use Module A if the technical documentation is public at placing (recital 91); the FAQ extends this to Class II.', 'E4', 'section 4', 'Art 32(5); recital 91; FAQ 6.1',
    [o("should be able to follow the internal control procedure based on module A, provided that they make the technical documentation available to the public"),
     f('FAQ', "Important products with digital elements of class I or II, if they are free and open-source software provided that the technical documentation is made available to the public")], 'OJ; FAQ', V)
row('OSS-26', 'Fines exposure Art 64(2): EUR 15m or 2.5% of worldwide turnover.', 'E4', 'section 3', 'Art 64(2)',
    [o("up to EUR 15 000 000")], 'OJ', V)
row('OSS-27', 'Art 25 empowers the Commission to set up voluntary security attestation programmes by delegated act to ease Art 13(5) due diligence on FOSS.', 'E4', 'section 5', 'Art 25',
    [o("the Commission is empowered to adopt delegated acts in accordance with Article 61 to supplement this Regulation by establishing voluntary security attestation programmes")], 'OJ', V)
row('OSS-28', 'PLD applies to products placed on the market or put into service after 9 Dec 2026 (PLD Art 2(1)); software is a product (Art 4(1)).', 'E4', 'section 5, Liability', 'PLD Arts 2(1), 4(1)',
    [f('PLD', "This Directive shall apply to products placed on the market or put into service after 9 December 2026"), f('PLD', "it includes electricity, digital manufacturing files, raw materials and software")], 'PLD', V)
row('OSS-29', 'A cybersecurity vulnerability can make a product defective (PLD recital 32; Art 7(2)(f)).', 'E4', 'section 5, Liability', 'PLD recital 32; Art 7(2)(f)',
    [f('PLD', "A product can also be found to be defective on account of its cybersecurity vulnerability"), f('PLD', "relevant product safety requirements, including safety-relevant cybersecurity requirements")], 'PLD', V)
row('OSS-30', 'Non-compliance with mandatory safety requirements creates a rebuttable presumption of defect (PLD Art 10(2)(b)); lack of software updates removes the later-defect defence (Art 11(2)(c)); disclosure (Art 9).', 'E4', 'section 5, Liability', 'PLD Arts 9, 10(2)(b), 10(5), 11(2)(c)',
    [f('PLD', "the claimant demonstrates that the product does not comply with mandatory product safety requirements"), f('PLD', "a lack of software updates or upgrades necessary to maintain safety"),
     f('PLD', "the defendant is required to disclose relevant evidence")], 'PLD', V)
row('OSS-31', 'FOSS developed or supplied outside a commercial activity is excluded from the PLD (PLD Art 2(2)).', 'E4', 'section 5, Liability', 'PLD Art 2(2)',
    [f('PLD', "This Directive does not apply to free and open-source software that is developed or supplied outside the course of a commercial activity")], 'PLD', V)
row('OSS-32', 'Member fees fund LTS without making the foundation a manufacturer if releases stay public (point 66; Example 33); release authority must sit with the foundation (points 48-49).', 'E4', 'Exhibit 6', 'Guidance paras 48-49, 66; Example 33',
    [g('P66', "the FOSS it publishes is not considered to be placed on the market"), g('P49', "Persons who contribute source code but do not control releases, roadmaps, or governance decisions are considered 'contributors'")], 'G', V)
row('OSS-33', 'Guidance point and Example numbers are those of C(2026) 5252 "as mirrored by the ORC WG"; steward section is points 69-84; Section 3 is points 40-88 with Examples 13-34.', 'E4', 'intro note; Risks; Sources', 'Guidance section 3',
    [g('P69', "The CRA introduces the novel legal category of 'open-source software steward'"), g('P84', "triggering the manufacturer's obligations under the CRA")], 'G', V,
    'All E4 point and Example numbers were re-checked against the Commission PDF itself; the ORC WG numbering matches.')

# ---------------- E5 global-control-set ----------------
row('GCS-01', 'Annex I Part I has 13 product properties plus the risk-based design duty; Part II has 8 lifecycle duties.', 'E5', 'section 1', 'Annex I Parts I-II',
    [o("ensure an appropriate level of cybersecurity based on the risks"), o("securely and easily remove on a permanent basis all data and settings")], 'OJ', V, 'Count verified in base register A01 and B01.')
row('GCS-02', 'Conformity route: notified body for Class I unless standard, common specification or "substantial" scheme applied in full (Art 32(2)); Class II unless an Art 27(9) scheme (Art 32(3)); FOSS may self-assess with a public technical file (Art 32(5)).', 'E5', 'Exhibit 2', 'Art 32(2), (3), (5)',
    [o("a European cybersecurity certification scheme pursuant to Article 27(9) of this Regulation at assurance level at least 'substantial'"), o("is made available to the public at the time of the placing on the market")], 'OJ', V)
row('GCS-03', 'Reporting: AEVs 24 h / 72 h / 14 days after a fix; severe incidents 24 h / 72 h / 1 month after the incident notification.', 'E5', 'Exhibit 2', 'Art 14(2), (4)',
    [o("no later than 14 days after a corrective or mitigating measure is available"), o("within one month after the submission of the incident notification under point (b)")], 'OJ', V)
row('GCS-04', 'Penalties up to EUR 15m or 2.5% of worldwide turnover, whichever is higher.', 'E5', 'Exhibit 2', 'Art 64(2)',
    [o("whichever is higher")], 'OJ', V)
row('GCS-05', 'Key dates: in force 10 Dec 2024; reporting 11 Sep 2026; full application 11 Dec 2027.', 'E5', 'Exhibit 2; section 3', 'Art 71',
    [o("shall enter into force on the twentieth day following that of its publication"), o("However, Article 14 shall apply from 11 September 2026")], 'OJ', V)
row('GCS-06', 'Scope: products with a data connection, B2B and B2C; exclusions for certain sectoral law and non-commercial open source.', 'E5', 'Exhibit 2', 'Art 2(1)-(2); recital 18',
    [o("the intended purpose or reasonably foreseeable use of which includes a direct or indirect logical or physical data connection to a device or network"),
     o("the provision of products with digital elements qualifying as free and open-source software that are not monetised by their manufacturers should not be considered to be a commercial activity")], 'OJ', V)
row('GCS-07', 'Presumption of conformity comes only from harmonised standards, common specifications or EU certification schemes.', 'E5', 'section 3', 'Art 27(1), (5), (8)',
    [o("shall be presumed to be in conformity with the essential cybersecurity requirements set out in Annex I covered by those standards or parts thereof"),
     o("in so far as the EU statement of conformity or European cybersecurity certificate, or parts thereof, cover those requirements")], 'OJ', V)
row('GCS-08', 'CRA asks for the support end month and year at purchase (Art 13(19)); human-channel rule for the single point of contact (Art 13(17)).', 'E5', 'Exhibit 4', 'Art 13(17), (19)',
    [o("including at least the month and the year, is clearly and understandably specified at the time of purchase"), o("shall not limit such means to automated tools")], 'OJ', V)
row('GCS-09', 'Support period at least 5 years unless the product is expected to be in use for less (Art 13(8)).', 'E5', 'Exhibit 4 tensions', 'Art 13(8)',
    [o("Where the product with digital elements is expected to be in use for less than five years, the support period shall correspond to the expected use time")], 'OJ', V)
row('GCS-10', 'Exhibit 5 mappings: Annex I (2)(a), (2)(b), (2)(c), (2)(d), (2)(j); Part II (5)-(7).', 'E5', 'Exhibit 5', 'Annex I Part I(2)(a)-(d), (j); Part II(5)-(7)',
    [o("with a secure by default configuration"), o("including but not limited to authentication, identity or access management systems"), o("to limit attack surfaces, including external interfaces"),
     o("put in place and enforce a policy on coordinated vulnerability disclosure"), o("provide for mechanisms to securely distribute updates")], 'OJ', V)
row('GCS-11', 'Hearth cameras, doorbells and locks Class I item 17; assistants item 16; routers item 12; health-monitoring wearables Class I; browsers Class I.', 'E5', 'Exhibit 6', 'Annex III Class I pts 2, 12, 16, 17, 19',
    [o("Smart home general purpose virtual assistants"), o("including smart door locks, security cameras")], 'OJ', V)
row('GCS-12', '10-year update archive (UCS-22) and 24-hour authority reporting (UCS-32) are CRA-only duties.', 'E5', 'section 4', 'Art 13(9); Art 14(2)(a)',
    [o("for a minimum of 10 years or for the remainder of the support period"), o("in any event within 24 hours")], 'OJ', V)
row('GCS-13', 'UK PSTI: Act 2022 Part 1; SI 2023/1007 Sch 1 paras 1(3), 2, 3(5), Schs 2-4; SI 2025/211; SI 2025/1267; Windsor Framework routing (SI 2023/1007 Sch 3 para 1).', 'E5', 'Exhibits 2, 4; section 3', 'UK instruments',
    [], 'NONE', CNV, 'Non-EU instruments; outside the E6 source set. Module E5 opened legislation.gov.uk on 1 Nov 2026.')
row('GCS-14', 'US Cyber Trust Mark: FCC 24-26 (89 FR 61242) paras 27-28, 36, 48, 55, 78; DA 26-75; NIST IR 8425.', 'E5', 'Exhibits 2, 4', 'US instruments',
    [], 'NONE', CNV, 'Non-EU instruments; outside the E6 source set.')
row('GCS-15', 'Japan JC-STAR: STAR-1 criteria JST-CR-01-01-2024 (S1.1-01 to S1.1-16); STAR-3 JST-SR-03-01-2026.', 'E5', 'Exhibits 2, 4, 5', 'Japanese scheme documents',
    [], 'NONE', CNV, 'Scheme documents; outside the E6 source set.')
row('GCS-16', 'Australia Cyber Security (Security Standards for Smart Devices) Rules 2025 ss 2, 8-10, Sch 1 cl 2-4; Cyber Security Act 2024 Part 2; Singapore CLS(IoT).', 'E5', 'Exhibits 1, 4, 5; section 2', 'Australian and Singapore instruments',
    [], 'NONE', CNV, 'Non-EU instruments; outside the E6 source set.')

# ---------------- G google-outside-in ----------------
row('GOI-01', 'Integration does not reclassify the host (Art 7(1)); a smartphone with an operating system is not an operating system (guidance Example 58); browser-only software is not a product (guidance para 21).', 'G', 'section 1, rules', 'Art 7(1); Example 58; guidance para 21',
    [o("shall not in itself render the product in which it is integrated subject to the conformity assessment procedures referred to in Article 32(2) and (3)"),
     g('E58', "The mere integration of an operating system does not mean that the smartphone has the core functionality of an operating system"),
     g('P21', "This is typically the case for web applications, including progressive web apps, where they are accessed exclusively through a web browser")], 'OJ; G', V)
row('GOI-02', 'Annex items in Exhibit 1: III-I.1, I.2, I.11, I.12, I.16, I.17, I.19; II.1; IV.3.', 'G', 'Exhibit 1', 'Annex III; Annex IV',
    [o("Identity management systems and privileged access management software and hardware, including authentication and access control readers"), o("Hypervisors and container runtime systems")], 'OJ', V)
row('GOI-03', 'Titan Security Key: Class I.1 or Annex IV.3 "smartcards or similar devices, including secure elements".', 'G', 'borderline table', 'Annex IV pt 3',
    [o("Smartcards or similar devices, including secure elements")], 'OJ', V)
row('GOI-04', 'Annex IV is treated as Class II until an Art 8(1) act.', 'G', 'borderline table', 'Art 8(1)',
    [o("Where no delegated acts as referred to in the first subparagraph of this paragraph have been adopted, products with digital elements which have the core functionality of a product category as set out in Annex IV shall be subject to the conformity assessment procedures referred to in Article 32(3)")], 'OJ', V)
row('GOI-05', 'Class II would need a notified body or a "substantial" EUCC certificate once the Art 27(9) act exists.', 'G', 'borderline table', 'Art 32(3)(c)',
    [o("where available and applicable, a European cybersecurity certification scheme pursuant to Article 27(9) of this Regulation at assurance level at least 'substantial'")], 'OJ', V)
row('GOI-06', 'Titan M2 at AVA_VAN.5 is above the AVA_VAN.4 threshold IR 2025/2392 uses for Annex IV.3 secure elements.', 'G', 'section 1', 'IR 2025/2392 Annex II pt 3',
    [f('IR', "Secure elements are designed to provide protection of at least AVA_VAN.4")], 'IR', V)
row('GOI-07', 'Art 14(7): main establishment where decisions are "predominantly taken"; otherwise the establishment with most employees; with no EU main establishment, authorised representative first, then importer.', 'G', 'section 2', 'Art 14(7)',
    [o("are predominantly taken"), o("the Member State in which the authorised representative acting on behalf of the manufacturer"), o("the Member State in which the importer placing on the market the highest number")], 'OJ', V)
row('GOI-08', 'A wrong choice "may" invalidate a notification (ENISA SRP FAQ 18).', 'G', 'section 2', 'ENISA SRP FAQ 18',
    [f('ENISA', "the notification may be invalidated")], 'ENISA', V)
row('GOI-09', 'The SRP form asks for a single "Product Name" per notification (ENISA SRP glossary, S10).', 'G', 'section 3', 'ENISA SRP glossary',
    [], 'NONE', CNV, 'The glossary was not obtained for this module; the ENISA FAQ (obtained) does not address it.')
row('GOI-10', 'From 11 Dec 2027 Art 24(3) may add steward filings; no source says whether one legal person acting as both files once or twice.', 'G', 'section 3; Risks', 'Art 24(3); guidance para 216',
    [o("The obligations laid down in Article 14(1) shall apply to open-source software stewards"), g('P216', "open-source software stewards are also required to report actively exploited vulnerabilities in accordance with Article 24(3)")], 'OJ; G', V,
    'Absence confirmed: guidance section 9.1 and FAQ 5.5 do not address dual-role filing. See legal-positions question D.')
row('GOI-11', 'Awareness against the guidance test of reasonable certainty; Art 14(8) user notices.', 'G', 'section 3', 'Guidance para 213; Art 14(8)',
    [g('P213', "a reasonable degree of certainty")], 'G', V)
row('GOI-12', 'Annex I Part II(1) SBOM; Annex VII point 2 and point 6; "Art 13(6) and Annex I Part II(4) public disclosure of fixed vulnerabilities".', 'G', 'Exhibit 4', 'Annex I Part II(4) (correct); Art 13(6) (as cited)',
    [o("once a security update has been made available, share and publicly disclose information about fixed vulnerabilities"), o("report the vulnerability to the person or entity manufacturing or maintaining the component")], 'OJ', WA,
    'Art 13(6) is upstream reporting to a component maintainer, not public disclosure. Cite Annex I Part II(4) only. Citation corrected in the paper.')
row('GOI-13', 'CRA SBOMs need not be public.', 'G', 'Exhibit 4', 'Recital 77',
    [o("Manufacturers should not be obliged to make the SBOM public")], 'OJ', V)
row('GOI-14', 'Under Commission guidance (not the Regulation\'s text), each software version is a separate placing on the market (KB 03-scope.md).', 'G', 'section 4', 'Guidance paras 13-15; Example 2',
    [g('E2', "Both copies of version 1.0.0 and 1.0.1 of software X are considered to be placed on the market on 1 January 2028")], 'G', NF,
    'As EAC-04. Proposed text: "Under Commission guidance, a version that substantially modifies the software is a new placing; other versions keep the original placing date (paras 13-15, Example 2). At four-weekly majors, Chrome will often be substantially modified, so declarations and documentation must still be generated by the pipeline." Not edited (substantive); corrections_enterprise.md C-04.')
row('GOI-15', 'Art 32(5) is the only self-assessment route for an AOSP Class I.11 OS until a standard, common specification or substantial-level scheme can be applied in full (Art 32(2)).', 'G', 'section 5', 'Art 32(2), (5)',
    [o("or where such harmonised standards, common specifications or European cybersecurity certification schemes do not exist")], 'OJ', V)
row('GOI-16', 'End date shown at purchase (Art 13(19)); support duty does not reach units placed before 11 Dec 2027 (Art 69(2)); five-year floor unless shorter use is evidenced (Art 13(8)).', 'G', 'Exhibit 5; decision 4', 'Art 13(8), (19); Art 69(2)',
    [o("shall be subject to the requirements set out in this Regulation only if, from that date, those products are subject to a substantial modification"), o("the support period shall be at least five years")], 'OJ', V)
row('GOI-17', 'Whether the five-year floor runs from each unit\'s placing or from a model\'s first placing is not settled in the sources reviewed.', 'G', 'Exhibit 5; Risks', 'FAQ 4.5.3, 7.2; guidance para 11',
    [f('FAQ', "for units of that product that are newly placed on the market, manufacturers are required to set the support period"),
     f('FAQ', "The manufacturer is required to set a support period for those units, in accordance with Article 13(8) of the CRA"),
     f('FAQ', "Union harmonisation legislation including the CRA applies to individual products, and not product types")], 'FAQ', W,
    'Not settled in law, but the Commission FAQ points to a per-unit reading: units newly placed later must get a support period set under Art 13(8) (FAQ 4.5.3, 7.2). See legal-positions question F.')
row('GOI-18', '"Reliable evidence" bar (Art 3(42)); single core functionality per product (guidance para 144).', 'G', 'Risks; 90-day plan', 'Art 3(42); guidance para 144',
    [o("reliable evidence that a malicious actor has exploited it"), g('P144', "may not have more than one core functionality")], 'OJ; G', V)
row('GOI-19', 'Whether one SRP notification may cover several products is not answered in any source opened.', 'G', 'Risks', 'ENISA SRP FAQ; guidance section 9.1',
    [], 'ENISA', V, 'Absence confirmed in the ENISA FAQ (15 Oct 2026) and guidance paras 209-221. See legal-positions question A.')


# ---------------- programme-case (added 1 Nov 2026; module appeared during this verification) ----------------
row('PCS-01', 'About 200 product lines need Annex VII parts, Annex II user information and translations into 23 languages (Art 28; Art 13(18)).', 'PCASE', 'budget section, first bullet', 'Art 28(2); Art 13(18)',
    [o("It shall be made available in the languages required by the Member State in which the product with digital elements is placed on the market or made available on the market"),
     o("Such information and instructions shall be provided in a language which can be easily understood by users and market surveillance authorities")], 'OJ', W,
    'The CRA sets languages by Member State requirement (declaration) and by what users and authorities easily understand (Annex II information); it does not require 23 languages for every product line. The paper treats 23 as the conservative reading in its Risks; say so where the figure is first used.')
row('PCS-02', 'Art 14 has applied since 11 Sep 2026; full application 11 Dec 2027.', 'PCASE', 'budget section; reconciliation table', 'Art 71(2)',
    [o("However, Article 14 shall apply from 11 September 2026"), o("This Regulation shall apply from 11 December 2027")], 'OJ', V)
row('PCS-03', 'Lumen, as software, cannot bridge the deadline with stock: each new version after 11 Dec 2027 is a new placing under the Commission\'s draft guidance (E1).', 'PCASE', 'lever L2', 'Guidance paras 13-15; Example 2; para 108; Art 69(2)',
    [g('P15', "Iterations that do not qualify as substantial modifications do not require the manufacturer to perform a new conformity assessment procedure and therefore do not modify that software's date of placement on the market"),
     g('P108', "security updates are generally not to be regarded as substantial modifications"),
     o("shall be subject to the requirements set out in this Regulation only if, from that date, those products are subject to a substantial modification")], 'G; OJ', NF,
    'Under the guidance only substantially modified versions (and new variants) are new placings. A version placed before 11 Dec 2027 can keep receiving non-substantial and security updates after that date without a certificate (Art 69(2)); what a late certificate blocks is the next substantially modified version. The lever still matters if 4-weekly majors are substantial, but the paper overstates the exposure. Not edited (substantive); corrections_enterprise.md C-11.')
row('PCS-04', 'Hardware units placed before 11 Dec 2027 stay lawful, with only Art 14 applying to them.', 'PCASE', 'lever L2; decision 3', 'Art 69(2)-(3)',
    [o("the obligations laid down in Article 14 shall apply to all products with digital elements that fall within the scope of this Regulation that have been placed on the market before 11 December 2027")], 'OJ', V)
row('PCS-05', 'If every Lumen security release is a new placing after 11 Dec 2027, a late certificate stops EU releases, not just launches.', 'PCASE', 'Risks, per-version placing', 'Guidance paras 15, 108; Example 2',
    [g('E2', "Both copies of version 1.0.0 and 1.0.1 of software X are considered to be placed on the market on 1 January 2028")], 'G', W,
    'Correctly framed as a conditional, but the guidance answers it: security releases are generally not substantial (para 108) and non-substantial versions are not new placings (para 15, Example 2). Restate as a residual risk that the guidance changes on adoption. corrections_enterprise.md C-11.')
row('PCS-06', 'Check Art 39 independence before any letter of intent to a notified body.', 'PCASE', 'decision 2', 'Art 39(3)',
    [o("A conformity assessment body shall be a third-party body independent of the organisation or the product with digital elements it assesses")], 'OJ', V)
row('PCS-07', 'Member States to "strive" for sufficient notified bodies by 11 Dec 2026 (E6 K23).', 'PCASE', 'reconciliation table', 'Art 35(2)',
    [o("Member States shall strive to ensure, by 11 December 2026 that there is a sufficient number of notified bodies")], 'OJ', V)
row('PCS-08', 'Art 13(6) upstream reporting is not a legal duty before Dec 2027.', 'PCASE', 'module disagreements table', 'Art 13(6); Art 71(2)',
    [o("This Regulation shall apply from 11 December 2027")], 'OJ', V, 'Art 13 is not among the provisions applying earlier (only Art 14 and Chapter IV).')
row('PCS-09', 'Platforms inside the Lumen quality system needs one item 11 model review instead of its own approval (L4).', 'PCASE', 'lever L4', 'Annex VIII Part IV pt 3.1(b)',
    [o("the technical documentation for one model of each category of products with digital elements intended to be manufactured or developed")], 'OJ', V)
row('PCS-10', 'No CRA notified body was listed in NANDO at the last verified check (8 Sep 2026); JC-STAR STAR-1 fee JPY 198,000.', 'PCASE', 'Risks; reconciliation table', 'None (status and non-EU facts)',
    [], 'NONE', CNV, 'Outside the E6 source set; rely on reports/verification.md claim 23 and the IPA page cited by the module.')

# ---------------- build and check ----------------
bad = 0
out = []
for (i, claim, where, cited, checks, srcs, status, corr) in R:
    frags = []
    for (src, refs, frag) in checks:
        nf = norm(frag)
        if src == 'G' and refs:
            hay = ' '.join(norm(IDX['paragraphs' if r[0] == 'P' else 'examples'][r[1:]]['text']) for r in refs)
            ok = nf in hay
        else:
            ok = nf in TXT[src]
        if not ok:
            bad += 1
            print('NOT FOUND', i, src, refs, frag[:90])
        label = ('Guidance ' + '/'.join(('para ' + r[1:]) if r[0] == 'P' else ('Example ' + r[1:]) for r in refs) + ': ') if (src == 'G' and refs) else ''
        frags.append(label + frag)
    src_used = '; '.join(SRC[s.strip()] for s in srcs.split(';'))
    out.append({'id': i, 'claim': claim, 'where_used': where, 'article_annex_cited': cited, 'oj_text': ' | '.join(frags),
                'source_used': src_used, 'status': status, 'correction': corr})
if bad:
    sys.exit(f'{bad} fragment(s) not found; claims_enterprise.csv not written')
with open('claims_enterprise.csv', 'w', newline='', encoding='utf-8') as fh:
    w = csv.DictWriter(fh, fieldnames=['id', 'claim', 'where_used', 'article_annex_cited', 'oj_text', 'source_used', 'status', 'correction'])
    w.writeheader(); w.writerows(out)
from collections import Counter
c = Counter(r['status'] for r in out)
print(len(out), 'claims;', dict(c))
for k in ['E1', 'E2', 'E3', 'E4', 'E5', 'G', 'PCASE']:
    sub = [r for r in out if r['where_used'].startswith(P[k])]
    print(k, len(sub), dict(Counter(r['status'] for r in sub)))
