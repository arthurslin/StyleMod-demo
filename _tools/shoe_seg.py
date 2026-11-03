"""Cut shoes from their source photos with clothing segmentation, keeping the whole shoe
and none of the floor shadow. Usage: shoe_seg.py tag:name [tag:name ...]"""
import os, sys
import numpy as np, torch
from PIL import Image
from scipy import ndimage as ni
from transformers import AutoImageProcessor, AutoModelForSemanticSegmentation

TR = chr(92) * 2 + '?' + chr(92) + os.path.normpath('C:/Users/assau/.claude/projects/C--Users-assau-AppData-Local-Claude-Data-claude-pzs8sxrjxfjjc-scratch-workspaces-8474f37f-6985-4bd0-95bb-6815984069ce-5469b8fd-b440-434a-8d03-7d8ef7a48bc6-scratch-2026-11-02-8ddb02/4f8ba79b-2c4f-4fb9-866f-a3d32b0037cf/tool-results')
MODEL = 'mattmdjaga/segformer_b2_clothes'
proc = AutoImageProcessor.from_pretrained(MODEL)
net = AutoModelForSemanticSegmentation.from_pretrained(MODEL).eval()

names = []
for pair in sys.argv[1:]:
    tag, name = pair.split(':')
    src = [os.path.join(TR, f) for f in os.listdir(TR) if f.endswith(f'-{tag}.jpg')][0]
    im = Image.open(src).convert('RGB')
    with torch.no_grad():
        logits = net(**proc(images=im, return_tensors='pt')).logits
    up = torch.nn.functional.interpolate(logits, size=im.size[::-1], mode='bilinear', align_corners=False)
    prob = up.softmax(1)[0]
    shoe = (prob[9] + prob[10]).numpy()  # left-shoe + right-shoe
    fg = shoe > .5
    fg = ni.binary_fill_holes(ni.binary_closing(fg, iterations=2))
    keep, n = ni.label(fg)
    if n:
        sizes = ni.sum(fg, keep, range(1, n + 1))
        fg = np.isin(keep, [i + 1 for i, s in enumerate(sizes) if s > sizes.max() * .2])
    al = ni.gaussian_filter(fg.astype('float32'), 1.0)
    out = Image.fromarray(np.dstack([np.array(im), (al * 255).astype('uint8')]), 'RGBA')
    out = out.crop(out.getbbox())
    out.save(f'images/shoes/{name}.webp', quality=88, method=6)
    names.append(name)
    print(name, out.size, 'coverage', round(float(fg.mean()), 3))

sheet = Image.new('RGB', (300 * len(names), 260), '#ecebf4')
for i, n in enumerate(names):
    t = Image.open(f'images/shoes/{n}.webp'); t.thumbnail((290, 250)); sheet.paste(t, (i * 300 + 5, 5), t)
sheet.save('_tools/shoe_seg_review.png')
