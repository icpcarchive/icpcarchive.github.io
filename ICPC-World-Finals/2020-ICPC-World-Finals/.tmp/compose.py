from PIL import Image
import os

base_dir = '/home/thaind/qwen_test/ICPC-World-Finals/2020-ICPC-World-Finals'
t = f'{base_dir}/.tmp'
out = f'{base_dir}/problems/images'


def rgba(base, smask, dest):
    b = Image.open(base).convert('RGB')
    a = Image.open(smask).convert('L')
    out_img = b.convert('RGBA')
    out_img.putalpha(a)
    out_img.save(dest)
    print(dest, out_img.size)


def plain(src, dest):
    im = Image.open(src).convert('RGB')
    im.save(dest)
    print(dest, im.size)


# J: page 19 base+smask
rgba(f'{t}/ex19-002.png', f'{t}/ex19-003.png', f'{out}/J-1.png')
# K: page 21 base+smask
rgba(f'{t}/ex21-002.png', f'{t}/ex21-003.png', f'{out}/K-1.png')
# N: page 27 JPEG, no smask
plain(f'{t}/ex27-002.png', f'{out}/N-1.png')
# O: page 29 base+smask
rgba(f'{t}/ex29-002.png', f'{t}/ex29-003.png', f'{out}/O-1.png')
# C: page 5 two photos
plain(f'{t}/ex5-002.png', f'{out}/C-1.png')
plain(f'{t}/ex5-003.png', f'{out}/C-2.png')
