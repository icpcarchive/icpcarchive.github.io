from PIL import Image

t = '/home/thaind/qwen_test/ICPC-World-Finals/2020-ICPC-World-Finals/.tmp'
for name in ['pg3-03.png', 'pg9-10.png']:
    im = Image.open(f'{t}/{name}').convert('RGB')
    w, h = im.size
    print(name, im.size)
    pts = [(5, 5), (w // 2, 5), (w - 5, 5), (5, h // 2), (w // 2, h // 2), (w - 5, h // 2), (5, h - 5), (w // 2, h - 5), (w - 5, h - 5)]
    for x, y in pts:
        print(f'  ({x},{y}) = {im.getpixel((x, y))}')
    # histogram of brightness buckets
    g = im.convert('L')
    hist = g.histogram()
    total = w * h
    nonwhite = sum(hist[:250])
    print(f'  non-white(>=250): {nonwhite/total:.3f}')
    print(f'  gray 200-250: {sum(hist[200:250])/total:.4f}')
    print(f'  dark <100: {sum(hist[:100])/total:.4f}')
