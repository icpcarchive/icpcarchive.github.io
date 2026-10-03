#!/usr/bin/env python3
"""Verify that every <pre> block in a year's problem HTML matches the PDF text layer.

Usage: python3 verify_samples.py <year-dir> <pdf>

For every line of every <pre> block in <year-dir>/problems/*.html, find the PDF
line (from `pdftotext -bbox` word boxes) whose word sequence contains the line's
tokens as a contiguous run, then compare token column positions (x0 divided by a
6.012pt monospace grid, relative to the first matched token) against the HTML
column positions.

Reports:
  MISMATCH — same tokens, different spacing (real sample-spacing error)
  NO-MATCH — token sequence not found anywhere (two-column merge is handled;
             remaining NO-MATCH lines need manual review: tokenization quirks
             like curly braces/apostrophes, or genuinely wrong text)

Known limitation: ambiguous short token sequences (e.g. '0 0 0') can match the
wrong source line; treat such MISMATCHes by reconstructing the specific sample
region manually (see git history / 2008 J+K fix).
"""
import re
import subprocess
import html as h
import sys
from collections import defaultdict

FALLBACK_W = 6.012  # default monospace char width in pt (2008-era PDFs)


def pdf_rows(pdf):
    n = int(subprocess.run(
        ['pdfinfo', pdf], capture_output=True, text=True
    ).stdout.split('Pages:')[1].split()[0])
    rows = []
    for p in range(1, n + 1):
        out = subprocess.run(
            ['pdftotext', '-f', str(p), '-l', str(p), '-bbox', pdf, '-'],
            capture_output=True, text=True).stdout
        ws = []
        for m in re.finditer(
                r'<word xMin="([\d.]+)" yMin="([\d.]+)" xMax="([\d.]+)" yMax="[\d.]+">(.*?)</word>',
                out):
            ws.append((float(m.group(2)), float(m.group(1)),
                       float(m.group(3)), h.unescape(m.group(4))))
        ws.sort()
        cur, lasty = [], None
        for y0, x0, x1, t in ws:
            if lasty is None or y0 - lasty <= 2.5:
                cur.append((x0, x1, t))
                lasty = y0
            else:
                rows.append((p, sorted(cur)))
                cur, lasty = [(x0, x1, t)], y0
        if cur:
            rows.append((p, sorted(cur)))
    return rows


def row_width(r, i, n):
    """Median char width of the matched token run (monospace rows are
    consistent; proportional text varies widely)."""
    widths = sorted((x1 - x0) / len(t)
                    for x0, x1, t in r[i:i + n] if x1 > x0)
    if not widths:
        return FALLBACK_W
    return widths[len(widths) // 2]


def check(line, rows):
    toks = line.split()
    if not toks:
        return None
    html_cols = [m.start() for m in re.finditer(r'\S+', line)]
    best = None
    for p, r in rows:
        seq = [t for _, _, t in r]
        for i in range(len(seq) - len(toks) + 1):
            if seq[i:i + len(toks)] != toks:
                continue
            W = row_width(r, i, len(toks))
            origin = r[i][0]
            cols = [round((r[j][0] - origin) / W)
                    for j in range(i, i + len(toks))]
            if line[:1] in ' \t':
                # Indented line: compare relative structure (a uniform
                # leading-indent shift cannot be seen from the token run
                # alone; verify indents manually via the block's margin).
                if [c - cols[0] for c in cols] == \
                   [c - html_cols[0] for c in html_cols]:
                    return None
            elif cols == html_cols:
                return None  # at least one PDF line matches exactly
            best = (p, W, cols)  # keep the first mismatching candidate
    if best is None:
        return ('NO-MATCH', 'token sequence not found in any PDF line')
    p, W, cols = best
    return ('MISMATCH', f'p{p} W={W:.3f} pdf={cols} html={html_cols}')


def main():
    year_dir, pdf = sys.argv[1], sys.argv[2]
    rows = pdf_rows(pdf)
    problems = sorted(
        f for f in __import__('os').listdir(year_dir + '/problems')
        if re.fullmatch(r'[A-Z]+\.html', f))
    mismatches = nomatch = 0
    for name in problems:
        page = open(year_dir + '/problems/' + name).read()
        for bi, pre in enumerate(re.findall(r'<pre>(.*?)</pre>', page, re.S)):
            for li, line in enumerate(pre.split('\n')):
                r = check(line, rows)
                if r is None:
                    continue
                kind, detail = r
                if kind == 'MISMATCH':
                    mismatches += 1
                    print(f'{name} pre{bi} line{li}: {detail}  line={line!r}')
                else:
                    nomatch += 1
                    print(f'{name} pre{bi} line{li}: NO-MATCH (manual review)  line={line!r}')
    print(f'\nMISMATCHES: {mismatches}   NO-MATCH (review): {nomatch}')


if __name__ == '__main__':
    main()
