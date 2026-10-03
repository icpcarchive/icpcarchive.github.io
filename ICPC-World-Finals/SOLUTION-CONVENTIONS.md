# Solution-sketch PDF → HTML conversion conventions (ICPC World Finals)

Converts a year's solution-sketch PDF (`<year>/…solutions.pdf`) into per-problem HTML
under `<year>/solutions/`, plus a "Solutions" link on the year's problem index.

## Deliverables (per year)
1. One page per problem: `<year>/solutions/<LETTER>.html` (e.g. `2018-…/solutions/D.html`).
2. A solutions index: `<year>/solutions/index.html` (lists ALL problems, contest order).
3. A "Solutions" link added below the last problem in `<year>/problems/index.html`.
4. (Only some years) reference the pre-extracted figures already in `<year>/solutions/images/`.

## Reference templates — copy the `<style>` block VERBATIM
- Solutions index: `2017-ICPC-World-Finals/solutions/index.html`
- Solution page:   `2017-ICPC-World-Finals/solutions/A.html`
- Problems index (`.sol` link pattern): `2017-ICPC-World-Finals/problems/index.html`

Extract the INNER css with `re.search(r'<style>(.*?)</style>', html, re.S).group(1)`
from the matching reference and reuse it verbatim in the new pages (do not add/remove rules
except where stated).

## `solutions/index.html`
```
<title>Solution sketches — <competition name></title>
<p class="backlink"><a href="../problems/index.html">← Problem set</a></p>
<header>
  <p class="kicker"><competition name — verbatim first header line of the PDF></p>
  <h1>Solution sketches</h1>
  <p class="meta">N solutions (A–X)</p>          <!-- N = problem count, X = last letter -->
</header>
<p><strong>Disclaimer</strong> <verbatim disclaimer paragraph(s), dehyphenated></p>
<p>— <verbatim author line></p>
<table class="problems">
  <tbody>
    <tr><td><a href="A.html">A</a></td><td class="title"><a href="A.html">Title</a></td></tr>
    …one row per problem, contest order…
  </tbody>
</table>
[optional <h2>Summary</h2> — see below]
<footer>© ICPC Foundation — solution sketches converted from the official PDF.</footer>
```
Both the letter cell and the title cell link to `<LETTER>.html`.
The `<style>` block is the 2017 index's inner css (it already includes `table.problems` rules).

### Summary section (index only)
If the PDF contains a "Summary" section (contest narrative, solve/submission stats tables,
language notes, graphs), reproduce it verbatim AFTER the problems table, starting with
`<h2>Summary</h2>`.
- Stats tables → `<table class="problems">` (reuse that CSS).
- Graph figures → `<figure><img src="images/summary-n.png" alt=""></figure>` — only if the
  file exists in `solutions/images/`.
- NEVER put summary content in the per-problem pages.
- Some years have NO summary (e.g. 2008) — omit the section entirely.

## Per-problem page `<LETTER>.html`
```
<title>Problem <L>: <Title> (Solution) — <competition name></title>
<p class="backlink"><a href="index.html">← All solutions</a></p>
<header>
  <p class="kicker"><competition name></p>
  <h1>Problem <L>: <Title></h1>
</header>
[per-problem metadata paragraphs, verbatim, e.g.
  "Shortest judge solution: NNNN bytes." / "Shortest team solution (during contest): NNNN bytes."
  / "Solved by N teams." / "First solved after N minutes." / "Python solutions by the judges: …"]
[solution body — verbatim paragraphs]
[figures: <figure><img src="images/<L>-n.png" alt=""></figure> where the PDF shows a diagram;
  add <figcaption> only if the PDF has a caption line]
```
- Use the 2017 `A.html` inner css.
- NO `<footer>` on individual problem pages (the 2017 reference has none).

## Text fidelity
- Keep text VERBATIM from the PDF.
- Dehyphenate line-break hyphenation (`Con-` + `test` → `Contest`); keep real hyphens (`real-time`).
- Keep Unicode math as-is (the PDF text layer already has it).
- The `Problem X: Title` line becomes the `<h1>`; the title in the index table comes from the same line.
- REMOVE page-number artifacts: bare numbers on their own line that pdftotext emits (e.g. a lone
  `2` or `3`) are page numbers, not content — drop them.
- No vision: never describe image pixel content. Reference figures by their pre-extracted
  filenames only.

## Figures / images (only 2018 and 2022 have any)
- All other years are text-only: no `images/` folder, no `<figure>`, no `images/…` references.
- 2018: pre-extracted `images/I-1.png`, `images/J-1.png`, `images/J-2.png`. Put I-1 in problem I
  and J-1/J-2 in problem J at the spot the PDF shows the diagram.
- 2022: pre-extracted problem figures `images/P-1.png` … `images/Z-1.png` (U has U-1,U-2,U-3)
  plus summary graphs `images/summary-1.png`, `images/summary-2.png`. Reference each problem
  figure in its problem page; reference the two summary graphs in the index Summary section.
- Only reference an image if the file actually exists. Never reference a missing file.

## Adding the "Solutions" link to `problems/index.html`
- Read `<year>/problems/index.html`. If it already contains `solutions/index.html`, skip.
- Inside its single existing `<style>` block, before `</style>`, append:
  ```
  .sol { margin: 1.25rem 0 0; }
  .sol a { color: var(--accent); text-decoration: none; display: inline-block; padding: 0.25rem 0.6rem; font-size: 1.1rem; }
  .sol a:hover { text-decoration: underline; }
  ```
- After the problems table `</table>` and before `<footer>`, insert:
  `<p class="sol"><a href="../solutions/index.html">Solutions</a></p>`
- After editing, verify `page.index('</style>') < page.index('<body>')`.

## Problem letters / count
- The authoritative problem set (letters + titles) comes from the year's `problems/index.html`.
- The solutions PDF contains a solution for EVERY problem in that set — produce one page each.
- WARNING: `Problem <L>:` headers in the PDF may carry leading whitespace or be separated by
  blank lines. Do NOT rely on a `^Problem [A-Z]:` regex. Extract the full text and locate every
  `Problem <L>:` marker for a letter in the year's set to find section boundaries, then
  cross-check you got exactly one section per problem letter.
- Titles: use the title verbatim from the solution PDF's `Problem X: Title` line. Minor spelling
  differences from the problems index (e.g. "Archeological" vs "Archaeological") are acceptable
  because the solutions source is authoritative for these pages.

## Verification (do this before reporting done)
- Every `<img src="images/…">` referenced exists on disk.
- Number of `<LETTER>.html` files == number of problems in the set; index table has exactly one
  row per problem, all links correct.
- `problems/index.html` has exactly ONE `solutions/index.html` link and the `.sol` rules present.
- No stray page-number artifacts remain in the body text.
- Spot-check 2–3 problems' text against the PDF for fidelity.
