#!/usr/bin/env python3
import os, re, html, subprocess, difflib

BASE = "/home/thaind/qwen_test/ICPC-World-Finals"
YEAR = os.path.join(BASE, "2008-ICPC-World-Finals")
OUT = os.path.join(YEAR, "solutions")
LETTERS = list("ABCDEFGHK")  # placeholder, replaced below
LETTERS = "ABCDEFGHIJK"
ok = True

def fail(msg):
    global ok
    ok = False
    print("FAIL:", msg)

def norm(s):
    s = html.unescape(s)
    s = re.sub(r"<[^>]+>", " ", s)
    s = re.sub(r"\s+", " ", s).strip()
    return s

raw = subprocess.run(["pdftotext", os.path.join(YEAR, "finals2008solutions.pdf"), "-"],
                     capture_output=True, text=True).stdout
lines = raw.splitlines()
# drop bare page-number lines
clean = [ln for ln in lines if not re.fullmatch(r"\s*\d+\s*", ln)]
pdftext = "\n".join(clean)

# section boundaries
marks = [(m.start(), m.end(), m.group(1), m.group(2).strip())
         for m in re.finditer(r"Problem ([A-K]): ([^\n]+)\n", pdftext)]
if [m[2] for m in marks] != list(LETTERS):
    fail(f"problem markers: {[m[2] for m in marks]}")
for i, (s, e, L, title) in enumerate(marks):
    end = marks[i+1][0] if i+1 < len(marks) else len(pdftext)
    pdf_sec = pdftext[s:end]
    pdf_body = pdf_sec[pdf_sec.index(title) + len(title):]
    pdf_body = pdf_body.replace("•", "")
    pdf_body = re.sub(r"\s+", " ", pdf_body).strip()

    with open(os.path.join(OUT, f"{L}.html"), encoding="utf-8") as f:
        page = f.read()
    body = page.split("</header>", 1)[1].split("<body>", 1)
    # body after </header>
    body = page.split("</header>", 1)[1]
    body_norm = re.sub(r"\s+", " ", norm(body)).strip()
    if body_norm != pdf_body:
        fail(f"{L}: text mismatch")
        sm = difflib.SequenceMatcher(None, pdf_body, body_norm)
        for tag, i1, i2, j1, j2 in sm.get_opcodes():
            if tag != "equal":
                print(f"  {tag}: PDF[{i1}:{i2}]={pdf_body[i1:i2]!r} HTML[{j1}:{j2}]={body_norm[j1:j2]!r}")
        continue
    # title check
    h1 = re.search(r"<h1>Problem " + L + r": ([^<]+)</h1>", page).group(1)
    if h1 != title:
        fail(f"{L}: h1 {h1!r} != {title!r}")
    print(f"OK {L}: {title} (verbatim match)")

# index checks
with open(os.path.join(OUT, "index.html"), encoding="utf-8") as f:
    idx = f.read()
rows = re.findall(r'<tr><td><a href="([A-K])\.html">\1</a></td><td class="title"><a href="\1\.html">([^<]+)</a></td></tr>', idx)
if [r[0] for r in rows] != list(LETTERS):
    fail(f"index rows: {rows}")
else:
    pdf_titles = {m[2]: m[3] for m in marks}
    for L, t in rows:
        if t != pdf_titles[L]:
            fail(f"index title {L}: {t!r} != {pdf_titles[L]!r}")
    print(f"OK index: {len(rows)} rows, titles match PDF")
for token in ["11 solutions (A–K)", "← Per Austrin".replace("←", "—"), "austrin@kth.se",
              "These are unofficial descriptions", "Finally, I want to stress"]:
    if token not in idx:
        fail(f"index missing: {token!r}")
if "Summary" in idx:
    fail("index has Summary (should be omitted for 2008)")
if "images" in idx:
    fail("index references images")

# per-page images / page-number artifacts
for L in LETTERS:
    with open(os.path.join(OUT, f"{L}.html"), encoding="utf-8") as f:
        p = f.read()
    if "images" in p:
        fail(f"{L}.html references images")
    if re.search(r"<p>\s*[0-9]+\s*</p>", p):
        fail(f"{L}.html has bare-number paragraph")

# problems index checks
with open(os.path.join(YEAR, "problems/index.html"), encoding="utf-8") as f:
    p = f.read()
if p.count("solutions/index.html") != 1:
    fail(f"problems index solutions link count = {p.count('solutions/index.html')}")
for rule in [".sol { margin: 1.25rem 0 0; }",
             ".sol a { color: var(--accent); text-decoration: none; display: inline-block; padding: 0.25rem 0.6rem; font-size: 1.1rem; }",
             ".sol a:hover { text-decoration: underline; }",
             '<p class="sol"><a href="../solutions/index.html">Solutions</a></p>']:
    if rule not in p:
        fail(f"problems index missing: {rule!r}")
if p.index("</style>") >= p.index("<body>"):
    fail("style block after body start")
if not os.path.exists(os.path.join(OUT, "images")):
    print("OK no images/ dir (text-only year)")
else:
    fail("images/ dir exists unexpectedly")

# file count
files = sorted(f for f in os.listdir(OUT) if f.endswith(".html"))
if files != sorted([f"{L}.html" for L in LETTERS] + ["index.html"]):
    fail(f"files: {files}")
else:
    print(f"OK {len(files)} files: " + ", ".join(files))

print("\nRESULT:", "PASS" if ok else "FAIL")
