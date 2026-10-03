import re, sys
base = '/home/thaind/qwen_test/ICPC-World-Finals/2020-ICPC-World-Finals/.tmp'
p = int(sys.argv[1])
ymin = float(sys.argv[2]); ymax = float(sys.argv[3])
html = open(f'{base}/bbox{p}.html').read()
words = re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', html)
words = [(float(a), float(b), float(c), float(d), t) for a, b, c, d, t in words]
sel = [w for w in words if ymin <= w[1] <= ymax]
sel.sort(key=lambda w: (w[1], w[0]))
cur = None
line = []
for w in sel:
    if cur is None or abs(w[1] - cur) > 4:
        if line:
            print(' '.join(f'[{x0:.0f}]{t}' for x0, t in line))
        cur = w[1]
        line = [(w[0], w[4])]
    else:
        line.append((w[0], w[4]))
if line:
    print(' '.join(f'[{x0:.0f}]{t}' for x0, t in line))
