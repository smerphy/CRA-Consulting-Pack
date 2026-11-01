import sys, html.parser, re
class P(html.parser.HTMLParser):
    def __init__(s): super().__init__(); s.out=[]; s.skip=0
    def handle_starttag(s,t,a):
        if t in('style','script','head'): s.skip+=1
        if t in('p','div','tr','br','h1','h2','h3','li'): s.out.append('\n')
        if t=='td': s.out.append(' ')
    def handle_endtag(s,t):
        if t in('style','script','head'): s.skip-=1
    def handle_data(s,d):
        if not s.skip: s.out.append(d)
p=P(); p.feed(open(sys.argv[1],encoding='utf-8').read())
t=''.join(p.out); t=re.sub(r'[ \t ]+',' ',t); t=re.sub(r'\n\s*\n+','\n',t)
open(sys.argv[2],'w',encoding='utf-8').write(t)
