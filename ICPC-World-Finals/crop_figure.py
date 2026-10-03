#!/usr/bin/env python3
"""Crop a figure region from a single PDF page by y-bounds (points from the TOP).

Usage:
  crop_figure.py <pdf> <page> <y_top> <y_bottom> <out.png>
                 [x_left=85] [x_right=510] [dpi=200] [pad=10]

y_top / y_bottom are PDF points measured from the TOP of the page, matching the
coordinates produced by `pdftotext -bbox` (page height ~792 for letter). The page
is rendered at `dpi`, the rectangle [x_left..x_right] x [y_top..y_bottom] is
cropped, and any white margin is auto-trimmed (keeping `pad` px of padding).

This is the recipe used for vector/composite figures in HTML-CONVENTIONS.md.
"""
import sys
import os
import glob
import subprocess
import tempfile
from PIL import Image


def main():
    if len(sys.argv) < 6:
        sys.exit(__doc__)
    pdf = sys.argv[1]
    page = int(sys.argv[2])
    y_top = float(sys.argv[3])
    y_bottom = float(sys.argv[4])
    out = sys.argv[5]
    x_left = float(sys.argv[6]) if len(sys.argv) > 6 else 85.0
    x_right = float(sys.argv[7]) if len(sys.argv) > 7 else 510.0
    dpi = int(sys.argv[8]) if len(sys.argv) > 8 else 200
    pad = int(sys.argv[9]) if len(sys.argv) > 9 else 10

    s = dpi / 72.0
    tmpdir = tempfile.mkdtemp(prefix="cropfig_")
    base = os.path.join(tmpdir, "page")
    try:
        subprocess.run(
            ["pdftoppm", "-f", str(page), "-l", str(page), "-png",
             "-r", str(dpi), pdf, base],
            check=True,
        )
        cand = sorted(glob.glob(base + "-*.png"))
        if not cand:
            sys.exit("render failed: no page image produced")
        img = Image.open(cand[0])
        box = (int(x_left * s), int(y_top * s), int(x_right * s), int(y_bottom * s))
        crop = img.crop(box)
        gray = crop.convert("L")
        bbox = gray.point(lambda v: 0 if v > 245 else 255).getbbox()
        if bbox:
            x0, y0, x1, y1 = bbox
            x0 = max(0, x0 - pad)
            y0 = max(0, y0 - pad)
            x1 = min(crop.width, x1 + pad)
            y1 = min(crop.height, y1 + pad)
            crop = crop.crop((x0, y0, x1, y1))
        os.makedirs(os.path.dirname(os.path.abspath(out)), exist_ok=True)
        crop.save(out)
        print(out, crop.size)
    finally:
        for f in glob.glob(os.path.join(tmpdir, "*")):
            try:
                os.unlink(f)
            except OSError:
                pass
        try:
            os.rmdir(tmpdir)
        except OSError:
            pass


if __name__ == "__main__":
    main()
