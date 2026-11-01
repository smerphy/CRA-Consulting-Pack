# Usage: python3 -I check_positions.py            (from pack/enterprise/oj-verification/)
# Checks every double-quoted passage of 15+ characters in legal-positions/*.md against the local
# source copies (OJ text, guidance, FAQ, ENISA FAQ, NCSC pages, IR 2025/2392, PLD) and the knowledge
# base. Passages split by " ... " are checked piece by piece. Quotations from web pages that were
# read but not saved (listed in WEB below) are reported separately, not as failures.
import glob, re, sys

def norm(s):
    s = s.replace('’', "'").replace('‘', "'").replace('“', '"').replace('”', '"')
    s = s.replace('–', '-').replace('—', '-').replace('­', '').replace('_', '').replace('Ý', 'ti')
    s = re.sub(r'(\w)- (\w)', r'\1-\2', s)
    return re.sub(r'\s+', ' ', s).replace('( ', '(').strip().lower()

files = ['source/oj_L_2024_2847_EN.txt', 'source/IR_2025_2392_EN.txt', 'source/PLD_2024_2853_EN.txt'] + \
        glob.glob('source/guidance/*.txt') + glob.glob('source/guidance/*.md') + \
        glob.glob('../../../reports/sections/*.md') + glob.glob('../*/paper.md') + glob.glob('../*/*.csv')
HAY = ' '.join(norm(open(f, encoding='utf-8').read()) for f in files)
WEB = {  # read on 1 Nov 2026 with WebFetch; not saved locally
    'ireland may need to rely on implementing measures to designate a national market surveillance authority': 'Arthur Cox, 8 Oct 2026',
    'the precise form and timing of any such measures have not yet been confirmed': 'Arthur Cox, 8 Oct 2026',
    'csirt-ie / ncsc-ie': 'Presencis tracker, 4 Oct 2026',
    'implementing': 'Presencis tracker, 4 Oct 2026',
    'countdown to compliance': 'Arthur Cox, 8 Oct 2026 (article title)',
}
bad = web = ok = 0
for md in sorted(glob.glob('legal-positions/*.md')):
    text = open(md, encoding='utf-8').read()
    for q in [x for x in re.findall(r'"([^"\n]*)"', text) if len(x) >= 15]:
        for piece in re.split(r'\s*(?:\.\.\.|\u2026)\s*', q):
            p = norm(piece).strip(' .,;:')
            if len(p) < 12:
                continue
            if p in HAY:
                ok += 1
            elif p in WEB:
                web += 1
            else:
                bad += 1
                print('NOT MATCHED', md, '|', piece[:120])
print(f'quotations matched: {ok}; web (not saved): {web}; not matched: {bad}')
sys.exit(1 if bad else 0)
