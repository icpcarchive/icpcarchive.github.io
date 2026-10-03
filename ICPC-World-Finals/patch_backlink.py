#!/usr/bin/env python3
"""Add the back-link to index.html into problem pages that lack it.

Usage: python3 patch_backlink.py <problems-dir> [more-dirs ...]
"""
import sys
from pathlib import Path

CSS = """
  .backlink { margin: 0 0 1.25rem; font-family: "Helvetica Neue", Arial, sans-serif; font-size: 0.85rem; }
  .backlink a { color: var(--accent); text-decoration: none; }
  .backlink a:hover { text-decoration: underline; }
"""
LINK = '<p class="backlink"><a href="index.html">\u2190 All problems</a></p>\n'

for arg in sys.argv[1:]:
    d = Path(arg)
    for f in sorted(d.glob("*.html")):
        if f.name == "index.html":
            continue
        page = f.read_text(encoding="utf-8")
        changed = False
        if 'class="backlink"' not in page:
            assert "</style>" in page and "<body>" in page, f.name
            page = page.replace("</style>", CSS.rstrip("\n") + "\n</style>", 1)
            page = page.replace("<body>", "<body>\n" + LINK, 1)
            changed = True
        # keep single style block invariant
        assert page.count("<style>") == 1 and page.count("</style>") == 1, f.name
        assert page.index("</style>") < page.index("<body>"), f.name
        if 'href="index.html"' in page:
            if changed:
                f.write_text(page, encoding="utf-8")
                print(f"patched {f}")
            else:
                print(f"ok      {f}")
        else:
            print(f"MISSING {f}")
