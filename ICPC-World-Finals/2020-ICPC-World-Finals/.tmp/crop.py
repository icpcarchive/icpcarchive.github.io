from PIL import Image

base_dir = '/home/thaind/qwen_test/ICPC-World-Finals/2020-ICPC-World-Finals'
t = f'{base_dir}/.tmp'
out = f'{base_dir}/problems/images'
S = 200.0 / 72.0


def px(v):
    return int(round(v * S))


def trim(im, pad=10, thresh=250):
    w, h = im.size
    mask = im.convert('L').point(lambda p: 255 if p < thresh else 0)
    bbox = mask.getbbox()
    if bbox is None:
        raise SystemExit('no non-white content found')
    left, top, right, bottom = bbox
    left = max(0, left - pad)
    top = max(0, top - pad)
    right = min(w, right + pad)
    bottom = min(h, bottom + pad)
    return im.crop((left, top, right, bottom))


# regions: (page-image, x0pt, y0pt, x1pt, y1pt, dest)
jobs = [
    (f'{t}/pg3-03.png', 66, 456, 530, 629, f'{out}/B-1.png'),
    (f'{t}/pg5-05.png', 405, 545, 530, 672, f'{out}/C-3.png'),
    (f'{t}/pg9-09.png', 100, 312, 500, 418, f'{out}/E-1.png'),
    (f'{t}/pg9-10.png', 100, 116, 500, 226, f'{out}/E-2.png'),
]

for src, x0, y0, x1, y1, dest in jobs:
    im = Image.open(src).convert('RGB')
    crop = im.crop((px(x0), px(y0), px(x1), px(y1)))
    res = trim(crop)
    res.save(dest)
    print(dest, res.size)
