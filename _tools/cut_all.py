"""Cut every generated garment off its white background and normalize it for tinting.

Output: images/wear/<name>.webp, transparent, with mid-fabric brightness near white
so that canvas multiply lands on the true catalog color. Dummies are cut too.
"""
import glob, json, os
import numpy as np
from PIL import Image
from scipy import ndimage as ni

OUT = 'images/wear'
os.makedirs(OUT, exist_ok=True)

def cut(path, thresh=238):
    a = np.array(Image.open(path).convert('RGB')).astype('float32')
    near = a.min(2) > thresh
    lab, _ = ni.label(near)
    edge = np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])
    bg = np.isin(lab, edge[edge > 0])
    fg = ni.binary_erosion(ni.binary_fill_holes(~bg), iterations=2)
    keep, n = ni.label(fg)
    if n > 1:
        sizes = ni.sum(fg, keep, range(1, n + 1))
        fg = np.isin(keep, [i + 1 for i, s in enumerate(sizes) if s > sizes.max() * .03])
    return a, ni.gaussian_filter(fg.astype('float32'), .9)

info = {}
for path in sorted(glob.glob('_gen/*.jpg')):
    name = os.path.splitext(os.path.basename(path))[0]
    a, al = cut(path, 205 if name.startswith('dummy') else 238)
    if name.startswith('dummy'):
        rgb = a
    else:
        gray = a.mean(2)
        mid = np.median(gray[al > .9])
        v = np.clip(gray / mid * 225, 0, 255)
        rgb = np.dstack([v, v, v])
    im = Image.fromarray(np.dstack([rgb, al * 255]).astype('uint8'), 'RGBA')
    box = im.getbbox()
    im = im.crop(box)
    if im.height > 900:
        im = im.resize((int(im.width * 900 / im.height), 900), Image.LANCZOS)
    im.save(f'{OUT}/{name}.webp', quality=82, method=6)
    info[name] = {'w': im.width, 'h': im.height}
json.dump(info, open('_tools/wear.json', 'w'), indent=0)
print(len(info), sum(os.path.getsize(f) for f in glob.glob(OUT + '/*')) // 1024, 'KB')
