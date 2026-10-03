import re, html as htmlmod

lines = open('/tmp/icpc2025/full_plain.txt').read().split('\n')
BASE = '/home/thaind/qwen_test/ICPC-World-Finals/2025-ICPC-World-Finals/problems/'

def norm(s):
    s = htmlmod.unescape(s)
    for ch in ('\u00a0', '\u2009', '\u202f'):
        s = s.replace(ch, ' ')
    for ch, rep in (('\u2018', "'"), ('\u2019', "'"), ('\u201c', '"'), ('\u201d', '"')):
        s = s.replace(ch, rep)
    s = re.sub(r'\s+', ' ', s)
    return s.replace(' \u00b7 ', '\u00b7')

starts = {}
for i, ln in enumerate(lines):
    m = re.match(r'^Problem ([A-L])$', ln.strip())
    if m:
        starts[m.group(1)] = i
letters = sorted(starts)

def diverge(sent, page):
    lo, hi, best = 0, len(sent), 0
    while lo <= hi:
        mid = (lo + hi) // 2
        if sent[:mid] in page:
            best = mid
            lo = mid + 1
        else:
            hi = mid - 1
    return best

for k, L in enumerate(letters):
    end = starts[letters[k + 1]] if k + 1 < len(letters) else len(lines)
    seg = lines[starts[L]:end]
    bs = next(i for i, l in enumerate(seg) if l.strip().startswith('Time limit')) + 1
    be = len(seg)
    for i in range(bs, len(seg)):
        t = seg[i].strip()
        if re.match(r'^Sample (Input|Interaction)', t) or '49th ICPC World Championship Problem' in seg[i]:
            be = i
            break
    raw = seg[bs:be]
    body = norm(raw[0])
    for l in raw[1:]:
        l = norm(l)
        if body.endswith('-'):
            body = body[:-1] + l
        else:
            body = body + ' ' + l
    page = norm(re.sub(r'<[^>]+>', '', open(BASE + L + '.html').read()))
    sents = re.split(r'(?<=\.) (?=[A-Z0-9"\'])', body)
    nfail = 0
    for s in sents:
        s = s.strip()
        if len(s.split()) < 6 or s in page:
            continue
        nfail += 1
        b = diverge(s, page)
        print('=== %s at %d/%d' % (L, b, len(s)))
        print('  PDF : ...%s' % s[max(0, b - 45):b + 55])
        pfx = s[:b - 5] if b > 5 else s[:b]
        idx = page.find(pfx)
        print('  PAGE: ...%s' % (page[max(0, idx - 45):idx + 95] if idx >= 0 else 'NOT FOUND'))
    if nfail == 0:
        print('%s: all clean' % L)
