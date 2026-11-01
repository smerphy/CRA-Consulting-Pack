# Usage: python3 -I check_quotes.py claims.csv source/oj_L_2024_2847_EN.txt
# Prints OJ-text fragments in claims.csv that do not occur verbatim in the OJ text. Bracketed summaries, corrected text and quotes from other acts are expected to be listed.
import csv,re,sys
norm=lambda s: re.sub(r'\s+',' ',s.replace('’',"'").replace('‘',"'").replace('’',"'").replace('“','"').replace('”','"')).strip()
oj=norm(open(sys.argv[2],encoding='utf-8').read())
oj=oj.replace("( ","(")
bad=0
for r in csv.DictReader(open(sys.argv[1],encoding='utf-8')):
    if 'OJ L 2024/2847' not in r['source_used'] or not r['oj_text'] or r['oj_text'].startswith('['): continue
    for frag in re.split(r' \| | \.\.\. ',r['oj_text']):
        f=norm(frag)
        f=re.sub(r'^(Art(icle)? [0-9()a-z]+|Annex [IVX]+[^:]*|Recital \d+|Part [IVX]+ [0-9.]+|pt \d+|subpara \d+|\(\w+\)|\d+\.\d*|OJ as published|2026/881 recitals)[:\s]+','',f)
        f=re.sub(r'^\(\w+\) ','',f).strip(" '.;")
        f=f.replace('[corrected text]','').replace('  ',' ')
        if len(f)<8: continue
        if f not in oj:
            bad+=1; print(r['id'],'|',f[:140])
print('fragments not matched:',bad)
