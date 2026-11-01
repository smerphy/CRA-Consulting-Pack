# Usage: python3 -I guidance_index.py source/guidance/C_2026_5252_annex_guidance_EN.layout.txt out.json
# Splits the C(2026) 5252 annex (pdftotext -layout) into numbered paragraphs and Examples,
# recording the section heading and PDF page of each, so citations can be checked by number.
import json, re, sys
lines = open(sys.argv[1], encoding='utf-8').read().split('\n')
paras, examples, cur, page, section = {}, {}, None, 1, ''
start = next(i for i, l in enumerate(lines) if re.match(r'^1 Introduction\s*$', l.replace('\f','')))
for l in lines[:start]:
    page += l.count('\f')
for l in lines[start:]:
    page += l.count('\f'); l = l.replace('\f', '')
    h = re.match(r'^(\d(?:\.\d){0,2})\s+([A-Z].{3,})$', l.strip())
    if h and not re.match(r'^\s{3,}', l) and len(l.strip()) < 140:
        section = h.group(1) + ' ' + h.group(2).strip()
    m = re.match(r'^\s{0,8}(\d{1,3})\.\s{2,}(\S.*)$', l)
    e = re.match(r'^\s*Example (\d{1,2})\s*:\s*(.*)$', l)
    if m and int(m.group(1)) == (max(paras) + 1 if paras else 1):
        cur = ('p', int(m.group(1))); paras[cur[1]] = {'section': section, 'page': page, 'text': m.group(2)}
        continue
    if e and int(e.group(1)) not in examples:
        cur = ('e', int(e.group(1))); examples[cur[1]] = {'section': section, 'page': page, 'in_para': max(paras) if paras else None, 'text': e.group(2)}
        continue
    s = l.strip()
    if not s or re.match(r'^\d{1,3}$', s): continue
    if re.match(r'^\d{1,3} ?[A-Z(]', s) and len(l) - len(l.lstrip()) < 2: # footnote lines at left margin
        continue
    if cur:
        tgt = paras[cur[1]] if cur[0] == 'p' else examples[cur[1]]
        tgt['text'] += ' ' + s
json.dump({'paragraphs': paras, 'examples': examples}, open(sys.argv[2], 'w'), indent=1, ensure_ascii=False)
print('paragraphs', len(paras), 'max', max(paras), 'examples', len(examples), 'max', max(examples))
