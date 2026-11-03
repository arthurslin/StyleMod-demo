"""Segment garments out of the style photos and build a sheet to judge cutout quality."""
import glob, os
import numpy as np, torch
from PIL import Image, ImageDraw
from transformers import AutoImageProcessor, AutoModelForSemanticSegmentation

MODEL = 'mattmdjaga/segformer_b2_clothes'
proc = AutoImageProcessor.from_pretrained(MODEL)
net = AutoModelForSemanticSegmentation.from_pretrained(MODEL).eval()

TOPS = 'crop-tee rib-tee rib-tank train-tank knit-polo tech-tee peplum crew-tee oxford fine-knit camp-shirt drape-top crinkle-shirt over-tee pump-cover boxy-sweat chunky-knit big-shirt blazer power-blazer chore track-top trench crop-puffer'.split()
BOTTOMS = 'slim-chino slim-jean cig-pant tapered-jog flare-legging str-jean str-pant track-pant wide-pant pleat-wide cargo parachute wide-jean wide-sweat gym-short midi-skirt maxi-skirt'.split()
def classes(sid):
    if sid in TOPS: return {4, 7}
    if sid in BOTTOMS: return {5, 6, 7}
    return None

os.makedirs('_tools/cut', exist_ok=True)
sheet_items = []
for sid in TOPS + BOTTOMS:
    im = Image.open(f'images/{sid}.jpg').convert('RGB')
    with torch.no_grad():
        out = net(**proc(images=im, return_tensors='pt')).logits
    up = torch.nn.functional.interpolate(out, size=im.size[::-1], mode='bilinear', align_corners=False)
    seg = up.argmax(1)[0].numpy()
    mask = np.isin(seg, list(classes(sid)))
    rgba = np.dstack([np.array(im), (mask * 255).astype('uint8')])
    cut = Image.fromarray(rgba, 'RGBA')
    box = cut.getbbox()
    if box: cut = cut.crop(box)
    cut.save(f'_tools/cut/{sid}.png')
    sheet_items.append((sid, cut, mask.mean()))
    print(sid, round(float(mask.mean()), 3), flush=True)

W, H = 140, 190
cols = 10
sheet = Image.new('RGB', (W * cols, H * ((len(sheet_items) + cols - 1) // cols)), (120, 150, 200))
d = ImageDraw.Draw(sheet)
for n, (sid, cut, _) in enumerate(sheet_items):
    t = cut.copy(); t.thumbnail((W - 6, H - 18))
    x, y = n % cols * W, n // cols * H
    sheet.paste(t, (x + 3, y + 15), t); d.text((x + 3, y + 2), sid, fill='white')
sheet.save('_tools/cut_review.jpg', quality=85)
