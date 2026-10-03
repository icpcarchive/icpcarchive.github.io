# PDF → HTML conversion conventions (ICPC World Finals)

Converts each problem of a year's statement PDF (`icpc<year>.pdf`) into a standalone
HTML file in `<year-folder>/problems/`, with extracted images in
`<year-folder>/problems/images/`.

## Files
- Problem page: `<year-folder>/problems/<LETTER>.html` (e.g. `2024-ICPC-World-Finals/problems/A.html`)
- **Index page: `<year-folder>/problems/index.html`** — one per year, listing ALL problems in
  contest order. Each table row MUST link to its problem page: the letter cell AND the title
  cell are both `<a href="<LETTER>.html">` (plus `tr:hover` highlighting). Columns: letter,
  title, time limit. Header: championship name
  (from the PDF footer) + year + problem count. **Only verifiable data** — no host city or other
  details unless they appear in the PDF itself. To build it: extract the INNER CSS from the
  template's style tag with `re.search(r'<style>(.*?)</style>', html, re.S).group(1)` (NOT the
  whole tag) and append index-specific table rules INSIDE the single `<style>...</style>` block
  before `</head>`. Reference implementation: `2024-ICPC-World-Finals/problems/index.html`.
  Written after the year's problems are done; verify `page.index('</style>') < page.index('<body>')`.
  Starts with a back link to the root archive index:
  `<p class="backlink"><a href="../../index.html">← All editions</a></p>` (same `.backlink`
  rules as problem pages).
  If `<year-folder>/test_data.txt` exists (2011–2025; one exact icpc.global archive URL per
  line), the header's "x problems" meta line ends with a right-aligned test-data link —
  `<p class="meta">x problems (A–L)<span class="testdata"><a href="<URL>"
  target="_blank" rel="noopener">Test data (<archive filename>)</a></span></p>` — plus rules
  making `header .meta` a flex row (`justify-content: space-between`) and `.testdata a`
  an accent link (1.1rem, padded). Years without a `test_data.txt` (1991–2010) get NO
  test-data link.
- **Archive index: `index.html` at the repo root** — one page listing EVERY year, newest first.
  Each row links the year AND the competition name to `<year-folder>/problems/index.html`;
  columns: year, competition, problem count. Competition name is NORMALIZED to
  `{ordinal} ICPC World Championship ({year})` with ordinal = year − 1976 (the series formula
  consistent with every verifiable ordinal in the PDFs, e.g. 1994 = 18th, 2010 = 34th,
  2025 = 49th); use proper suffixes (21st, 22nd, 31st, 41st). No meta/stats lines under the
  header. Built by the same inner-CSS extraction as the per-year index, plus a
  `table.archive` rule set. Regenerate it whenever a year is added/removed.
  Reference: `ICPC-World-Finals/index.html`.
- Images: `<year-folder>/problems/images/<LETTER>-<n>.png` (n = 1,2,... in page order;
  the first/thematic illustration is `<LETTER>-1.png`)
- Images are referenced with relative paths: `images/A-1.png`

## Image extraction
- To see what's on the problem's pages use `pdfimages -list <pdf>` (whole document, with page
  column) — NOTE: `pdfimages -list -f/-l` is BROKEN in this poppler build (exit 99); never use it.
  (type `image` = base, `smask` = alpha mask, `jpeg`/`image` encodings).
- `pdfimages -png -f <start> -l <end> <pdf> <tmp-prefix>` extracts them as `<tmp-prefix>-000.png`,
  `-001.png`, ... in the same order shown by `-list`.
- When a base `image` is immediately followed by an `smask` of the same size, combine them into
  RGBA with Pillow:
  ```python
  from PIL import Image
  base = Image.open('base.png').convert('RGB')
  a = Image.open('smask.png').convert('L')
  rgba = base.convert('RGBA')
  rgba.putalpha(a)
  rgba.save('out.png')
  ```
- JPEG images need no smask handling.
- **Vector figures** (diagrams drawn with PDF vector art — `pdfimages` shows NO image for them):
  detect via `pdftotext -bbox` (a large text-free gap between paragraphs where a "Figure X.N:"
  caption sits) and capture with the same render-and-crop recipe below. A problem can have BOTH
  a raster photo AND a vector figure — check each "Figure X.N" reference individually.
- **Composite figures** (many small images forming one figure, e.g. multi-panel illustrations):
  don't try to reassemble the tiles blindly — render the page and crop the figure region instead:
  1. `pdftotext -f <p> -l <p> -bbox <pdf> /tmp/bbox.html` gives per-word boxes (`<word xMin yMin xMax yMax>`),
     y measured from the TOP in points (page height ~841.89).
  2. Find the y of the line just above the figure (e.g. "...See Figure X.1...") and the first
     caption line ("Figure X.1: ...") — the figure lies between them.
  3. `pdftoppm -f <p> -l <p> -png -r 200 <pdf> /tmp/page` → crop with Pillow between those y
     values (×200/72 scale, x from ~85 to ~510 pt), then auto-trim white margins
     (scan for non-white bbox, add ~10 px padding).
- **Decorative banners:** some older PDFs repeat an identical header/footer strip image on many
  pages (detected: same size on ≥5 different pages — e.g. 2144×361 in 2021, 4601×881 in 2020,
  3693×423 in 2012, 885×100 in 2010). These are NOT problem figures — skip them. (Do NOT
  confuse with many small tiles of the same size on ONE page — that is a composite figure.)
- Only include images that belong to this problem's page range.
- The model has NO vision: never describe an image's pixel content. Captions come from the
  statement's `Figure X.N: ...` lines and the page→problem mapping only.

## HTML structure (preserve the statement's structure)
Standalone page, inline `<style>`, no external resources.
STYLE CONSISTENCY: copy the entire `<style>` block verbatim from
`/home/thaind/qwen_test/ICPC-World-Finals/2024-ICPC-World-Finals/problems/A.html` (the
reference template) into every problem page — change only the content. Keep the statement text verbatim
(dehyphenate line-break hyphenation like `Con-` + `test` → `Contest`; keep real hyphens like
`real-time`). Sections in statement order:

```
<header>  Problem <LETTER> · <Title>   (time limit if given)
<body>
  intro/description paragraphs (with <figure> illustrations in-flow)
  <h2>Input</h2>
  <h2>Output</h2>          (or <h2>Interaction</h2> for interactive problems)
  sample blocks: <h3>Sample Input <i>1</i></h3><pre>...</pre> etc. (2-column samples in the PDF
  become stacked blocks: Sample Input 1, Sample Output 1, Sample Input 2, ...)
  <h2>Notes</h2> / explanation notes if present
<footer>  original footer line, e.g. "48th ICPC World Championship Problem A: Billboards © ICPC Foundation"
```

- **Back link:** every problem page starts (right after `<body>`) with
  `<p class="backlink"><a href="index.html">← All problems</a></p>` and carries these CSS rules
  (appended inside the `<style>` block, same on every page):
  ```css
  .backlink { margin: 0 0 1.25rem; font-family: "Helvetica Neue", Arial, sans-serif; font-size: 1.1rem; }
  .backlink a { color: var(--accent); text-decoration: none; display: inline-block; padding: 0.25rem 0.6rem; }
  .backlink a:hover { text-decoration: underline; }
  ```
- Figures: `<figure><img src="images/A-1.png" alt=""><figcaption>Figure A.1: Sample Input 1</figcaption></figure>`.
  Captions are taken from the statement text (`Figure X.N: ...` lines).
- If the statement has an "Image credits" line, add it as a credits footer. Check each problem
  individually — do not assume one exists.
- Math: keep as Unicode plain text (the PDF text layer already contains Unicode math).
- Sample input/output must be in `<pre>` blocks with the exact content (no reformatting).

## Verification
After writing the HTML: confirm every `images/...` file referenced actually exists, and spot-check
the sample input blocks against the extracted text.
