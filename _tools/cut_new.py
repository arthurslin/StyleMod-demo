"""Cut new garment captures off white and normalize them for tinting, like cut_all.py.
Usage: cut_new.py tag:name [tag:name ...]  (tag is the capture's file suffix)"""
import os, shutil, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ni

TR = chr(92) * 2 + '?' + chr(92) + os.path.normpath('C:/Users/assau/.claude/projects/C--Users-assau-AppData-Local-Claude-Data-claude-pzs8sxrjxfjjc-scratch-workspaces-8474f37f-6985-4bd0-95bb-6815984069ce-5469b8fd-b440-434a-8d03-7d8ef7a48bc6-scratch-2026-11-02-8ddb02/4f8ba79b-2c4f-4fb9-866f-a3d32b0037cf/tool-results')

names = []
for pair in sys.argv[1:]:
    tag, name = pair.split(':')
    src = [os.path.join(TR, f) for f in os.listdir(TR) if f.endswith(f'-{tag}.jpg')][0]
    shutil.copy(src, f'_gen/{name}.jpg')
    a = np.array(Image.open(src).convert('RGB')).astype('float32')
    near = a.min(2) > 236
    lab, _ = ni.label(near)
    edge = np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])
    fg = ni.binary_erosion(ni.binary_fill_holes(~np.isin(lab, edge[edge > 0])), iterations=2)
    keep, n = ni.label(fg)
    if n > 1:
        sizes = ni.sum(fg, keep, range(1, n + 1))
        fg = np.isin(keep, [i + 1 for i, s in enumerate(sizes) if s > sizes.max() * .03])
    al = ni.gaussian_filter(fg.astype('float32'), .9)
    gray = a.mean(2)
    v = np.clip(gray / np.median(gray[al > .9]) * 225, 0, 255)
    im = Image.fromarray(np.dstack([v, v, v, al * 255]).astype('uint8'), 'RGBA')
    im = im.crop(im.getbbox())
    if im.height > 900:
        im = im.resize((int(im.width * 900 / im.height), 900), Image.LANCZOS)
    im.save(f'images/wear/{name}.webp', quality=82, method=6)
    names.append(name)
    print(name, im.size)

sheet = Image.new('RGB', (320 * len(names), 440), '#ecebf4')
for i, n in enumerate(names):
    t = Image.open(f'images/wear/{n}.webp'); t.thumbnail((310, 430)); sheet.paste(t, (i * 320 + 5, 5), t)
sheet.save('_tools/new_wear_review.png')
