import re, sys
base = '/home/thaind/qwen_test/ICPC-World-Finals/2020-ICPC-World-Finals/.tmp'
for p in [int(x) for x in sys.argv[1:]]:
    html = open(f'{base}/bbox{p}.html').read()
    words = re.findall(r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="([\d.]+)">([^<]*)</word>', html)
    words = [(float(a), float(b), float(c), float(d), t) for a, b, c, d, t in words]
    # cluster into lines by yMin proximity
    words.sort(key=lambda w: (w[1], w[0]))
    lines = []
    for w in words:
        if lines and abs(w[1] - lines[-1][0]) < 4:
            lines[-1][1].append(w)
        else:
            lines.append([w[1], [w]])
    print(f"=== PAGE {p} ===")
    for y, ws in lines:
        y2 = max(w[3] for w in ws)
        x = min(w[0] for w in ws)
        x2 = max(w[2] for w in ws)
        txt = ' '.join(w[4] for w in sorted(ws, key=lambda w: w[0]))
        print(f"y={y:7.1f}-{y2:7.1f} x={x:6.1f}-{x2:6.1f} | {txt[:95]}")
