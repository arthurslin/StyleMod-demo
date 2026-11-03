"""Pilot: cut garments from white, tint to catalog colors, and fit them on the dummy."""
import numpy as np
from PIL import Image
from scipy import ndimage as ni

def cut(name, thresh=236):
    a = np.array(Image.open(f'_gen/{name}.jpg').convert('RGB')).astype('float32')
    near = a.min(2) > thresh
    lab, _ = ni.label(near)
    edge = np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])
    bg = np.isin(lab, edge[edge > 0])
    fg = ni.binary_fill_holes(~bg)
    fg = ni.binary_erosion(fg, iterations=2)
    al = ni.gaussian_filter(fg.astype('float32'), 1.0)
    rgba = np.dstack([a, al * 255]).astype('uint8')
    im = Image.fromarray(rgba, 'RGBA')
    return im.crop(im.getbbox())

def tint(im, hex_):
    a = np.array(im).astype('float32')
    gray = a[..., :3].mean(2)
    base = np.median(gray[a[..., 3] > 200])
    shade = np.clip(gray / base, 0, 1.5)
    c = np.array([int(hex_[i:i + 2], 16) for i in (1, 3, 5)], 'float32')
    # Very dark colors need lifted shading so folds still read.
    lum = c.mean() / 255
    shade = 1 + (shade - 1) * (1.6 if lum < .3 else 1)
    out = np.clip(c[None, None] * shade[..., None] + (shade[..., None] - 1) * 40 * (lum < .3), 0, 255)
    return Image.fromarray(np.dstack([out, a[..., 3]]).astype('uint8'), 'RGBA')

dummy = Image.open('_gen/dummy-womenswear.jpg').convert('RGBA')
print('dummy size', dummy.size)
CX = 420

def place(canvas, im, cx, top, width):
    h = int(im.height * width / im.width)
    t = im.resize((width, h), Image.LANCZOS)
    canvas.alpha_composite(t, (int(cx - width / 2), int(top)))

def outfit(top, bottom, shoes, jacket=None):
    c = dummy.copy()
    place(c, tint(cut('sneakers'), shoes), CX, 1120, 190)
    place(c, tint(cut('wide-trousers'), bottom), CX, 478, 300)
    place(c, tint(cut('tee'), top), CX, 258, 410)
    if jacket: place(c, tint(cut('blazer'), jacket), CX, 248, 400)
    return c

looks = [outfit('#a64b24', '#d9c8ad', '#f8f6f1'), outfit('#f8f6f1', '#5f6336', '#1f1f21'), outfit('#f8f6f1', '#1f2d4d', '#b98a4f', '#1f1f21'), outfit('#d7a11d', '#1e4fc2', '#c8242f', '#9b9c9e')]
s = Image.new('RGB', (4 * 340, 510), 'white')
for i, l in enumerate(looks):
    t = l.convert('RGB'); t.thumbnail((336, 506)); s.paste(t, (i * 340 + 2, 2))
s.save('_tools/pilot_comp.jpg', quality=88)
