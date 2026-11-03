"""Cut real-color shoe images off a grey background with GrabCut. Usage: cut_shoes.py tag:name [tag:name ...]"""
import os, sys
import cv2
import numpy as np
from PIL import Image
from scipy import ndimage as ni

TR = chr(92) * 2 + '?' + chr(92) + os.path.normpath('C:/Users/assau/.claude/projects/C--Users-assau-AppData-Local-Claude-Data-claude-pzs8sxrjxfjjc-scratch-workspaces-8474f37f-6985-4bd0-95bb-6815984069ce-5469b8fd-b440-434a-8d03-7d8ef7a48bc6-scratch-2026-11-02-8ddb02/4f8ba79b-2c4f-4fb9-866f-a3d32b0037cf/tool-results')
os.makedirs('images/shoes', exist_ok=True)

OUT = os.environ.get('OUT', 'images/shoes')
os.makedirs(OUT, exist_ok=True)
ACCESSORY = OUT.endswith('accessories')
for pair in sys.argv[1:]:
    tag, name = pair.split(':')[:2]
    flip = pair.endswith(':flip')
    src = [os.path.join(TR, f) for f in os.listdir(TR) if f.endswith(f'-{tag}.jpg')][0]
    rgb = np.array(Image.open(src).convert('RGB'))
    h, w, _ = rgb.shape
    bgr = rgb[..., ::-1].copy()
    # Seed: obvious background is low-saturation and close to the margin grey.
    a = rgb.astype('float32')
    margin = np.concatenate([a[:, :w // 14], a[:, -w // 14:]], axis=1)
    bg = np.median(margin, axis=1)[:, None, :]
    dist = np.sqrt(((a - bg) ** 2).sum(2))
    mask = np.full((h, w), cv2.GC_PR_BGD, np.uint8)
    mask[dist > 45] = cv2.GC_PR_FGD
    mask[dist < 8] = cv2.GC_BGD
    mask[:, :w // 14] = cv2.GC_BGD
    mask[:, -w // 14:] = cv2.GC_BGD
    mask[:h // 10] = cv2.GC_BGD
    cv2.grabCut(bgr, mask, None, np.zeros((1, 65), np.float64), np.zeros((1, 65), np.float64), 6, cv2.GC_INIT_WITH_MASK)
    fg = np.isin(mask, [cv2.GC_FGD, cv2.GC_PR_FGD])
    # Accessories have real gaps (chain loops, belt coils), so their holes stay open.
    fg = ni.binary_opening(fg if ACCESSORY else ni.binary_fill_holes(fg), iterations=1 if ACCESSORY else 2)
    # Shadow on the outer sides is floor too: drop columns at the edges that are mostly empty.
    # The strip between the two shoes is only floor and shadow: in the middle of the
    # frame, clear columns that hold far less than a shoe's height of foreground.
    counts = fg.sum(0)
    mid = slice(int(w * .35), int(w * .65))
    gap = np.zeros(w, bool)
    gap[mid] = (counts[mid] < counts.max() * float(os.environ.get('GAP', '.55'))) & (not ACCESSORY)
    fg[:, gap] = False
    if os.environ.get('SHADOWFREE'):
        # A floor shadow is the grey floor made darker: low colour, and between about
        # 45% and 97% of the floor's brightness. White shoes are brighter, black shoes
        # darker, brown shoes coloured, so none of them match.
        lum = a.mean(2)
        sat = a.max(2) - a.min(2)
        ratio = lum / np.maximum(bg.mean(2), 1)
        shadow = (sat < 16) & (ratio > .42) & (ratio < .97)
        fg &= ~shadow
        fg = ni.binary_opening(fg, iterations=2)
        keep2, n2 = ni.label(fg)
        if n2:
            sizes2 = ni.sum(fg, keep2, range(1, n2 + 1))
            fg = np.isin(keep2, [i + 1 for i, s2 in enumerate(sizes2) if s2 > sizes2.max() * .25])
        fg = ni.binary_fill_holes(ni.binary_closing(fg, iterations=3))
    if pair.endswith(':noshadow'):
        # White shoes: floor shadow is grey and darker than the shoe, so drop it.
        lum = a.mean(2)
        sat = a.max(2) - a.min(2)
        fg &= ~((sat < 12) & (lum < bg.mean(2) - 6))
    keep, n = ni.label(fg)
    sizes = ni.sum(fg, keep, range(1, n + 1))
    fg = np.isin(keep, [i + 1 for i, s in enumerate(sizes) if s > sizes.max() * (.02 if ACCESSORY else .25)])
    al = ni.gaussian_filter(fg.astype('float32'), .8)
    im = Image.fromarray(np.dstack([rgb, al * 255]).astype('uint8'), 'RGBA')
    im = im.crop(im.getbbox())
    if flip: im = im.transpose(Image.FLIP_TOP_BOTTOM)
    im.save(f'{OUT}/{name}.webp', quality=86, method=6)
    print(name, im.size)

names = [p.split(':')[1] for p in sys.argv[1:]]
sheet = Image.new('RGB', (360 * len(names), 300), '#e9e3d6')
for i, n in enumerate(names):
    im = Image.open(f'{OUT}/{n}.webp'); im.thumbnail((340, 290)); sheet.paste(im, (i * 360 + 10, 5), im)
sheet.save(f"_tools/{os.path.basename(OUT)}_review.png")
