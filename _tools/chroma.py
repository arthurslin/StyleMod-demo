"""Key shoes off a chroma-green background. Usage: chroma.py tag:name [tag:name ...]"""
import os, sys
import numpy as np
from PIL import Image
from scipy import ndimage as ni

TR = chr(92) * 2 + '?' + chr(92) + os.path.normpath('C:/Users/assau/.claude/projects/C--Users-assau-AppData-Local-Claude-Data-claude-pzs8sxrjxfjjc-scratch-workspaces-8474f37f-6985-4bd0-95bb-6815984069ce-5469b8fd-b440-434a-8d03-7d8ef7a48bc6-scratch-2026-11-02-8ddb02/4f8ba79b-2c4f-4fb9-866f-a3d32b0037cf/tool-results')
names = []
for pair in sys.argv[1:]:
    tag, name = pair.split(':')
    src = [os.path.join(TR, f) for f in os.listdir(TR) if f.endswith(f'-{tag}.jpg')][0]
    a = np.array(Image.open(src).convert('RGB')).astype('float32')
    r, g, b = a[..., 0], a[..., 1], a[..., 2]
    greenness = g - np.maximum(r, b)
    # Crop to the green field (the capture has a white letterbox around it).
    field = greenness > 40
    ys, xs = np.where(field)
    y0, y1, x0, x1 = ys.min() + 4, ys.max() - 4, xs.min() + 4, xs.max() - 4
    a, greenness = a[y0:y1, x0:x1], greenness[y0:y1, x0:x1]
    # Soft key: fully transparent when strongly green, fully opaque when not green at all.
    alpha = np.clip(1 - (greenness - 18) / 40, 0, 1)
    fg = alpha > .5
    keep, n = ni.label(fg)
    sizes = ni.sum(fg, keep, range(1, n + 1))
    fg = np.isin(keep, [i + 1 for i, s in enumerate(sizes) if s > sizes.max() * .25])
    fg = ni.binary_fill_holes(fg)
    alpha = np.where(fg, np.maximum(alpha, ni.binary_erosion(fg, iterations=2)), 0)
    alpha = ni.gaussian_filter(alpha, .7)
    # Despill: pull green back to the level of red and blue at the edges.
    rgb = a.copy()
    rgb[..., 1] = np.minimum(rgb[..., 1], np.maximum(rgb[..., 0], rgb[..., 2]) + 6)
    im = Image.fromarray(np.dstack([rgb, alpha * 255]).astype('uint8'), 'RGBA')
    im = im.crop(im.getbbox())
    im.save(f'images/shoes/{name}.webp', quality=88, method=6)
    names.append(name)
    print(name, im.size)

sheet = Image.new('RGB', (320 * len(names), 270), '#ecebf4')
for i, n in enumerate(names):
    t = Image.open(f'images/shoes/{n}.webp'); t.thumbnail((310, 260)); sheet.paste(t, (i * 320 + 5, 5), t)
sheet.save('_tools/chroma_review.png')
