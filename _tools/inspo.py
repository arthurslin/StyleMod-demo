"""Musinsa and Fashion Nova pieces: cut the images and add them to the style recipes."""
import os, re
import numpy as np
from PIL import Image
from scipy import ndimage as ni

TR = chr(92) * 2 + '?' + chr(92) + os.path.normpath('C:/Users/assau/.claude/projects/C--Users-assau-AppData-Local-Claude-Data-claude-pzs8sxrjxfjjc-scratch-workspaces-8474f37f-6985-4bd0-95bb-6815984069ce-5469b8fd-b440-434a-8d03-7d8ef7a48bc6-scratch-2026-11-02-8ddb02/4f8ba79b-2c4f-4fb9-866f-a3d32b0037cf/tool-results')

def cut(tag, name):
    src = [os.path.join(TR, f) for f in os.listdir(TR) if f.endswith(f'-{tag}.jpg')][0]
    a = np.array(Image.open(src).convert('RGB')).astype('float32')
    lab, _ = ni.label(a.min(2) > 232)
    edge = np.unique(np.r_[lab[0], lab[-1], lab[:, 0], lab[:, -1]])
    fg = ni.binary_erosion(ni.binary_fill_holes(~np.isin(lab, edge[edge > 0])), iterations=2)
    keep, n = ni.label(fg)
    sizes = ni.sum(fg, keep, range(1, n + 1))
    fg = keep == (int(np.argmax(sizes)) + 1)
    al = ni.gaussian_filter(fg.astype('float32'), .9)
    gray = a.mean(2)
    v = np.clip(gray / np.median(gray[al > .9]) * 225, 0, 255)
    im = Image.fromarray(np.dstack([v, v, v, al * 255]).astype('uint8'), 'RGBA')
    im = im.crop(im.getbbox())
    im.save(f'images/wear/{name}.webp', quality=84, method=6)
    print(name, im.size)

for tag, name in [('pf2b1x', 'shell-jacket'), ('161dfo', 'fleece-jacket'), ('48cuxp', 'extra-wide-jeans'),
                  ('nuz8f0', 'moto-jacket'), ('jek04s', 'stacked-jeans'), ('1yh5q0', 'hobo-bag')]:
    cut(tag, name)

p = 'index.html'
s = open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)

ALLOCC = '["casual", "work", "night", "athleisure", "gym", "weekend"]'
R('''  { id: "chain",''', f'''  {{ id: "shell",      slot: "layer", name: "technical shell jacket", fit: "regular", sil: EVEN, occ: {ALLOCC}, dept: BOTH, base: 140, colors: ALL, material: "recycled waterproof nylon", tags: ["trend", "durable"] }},
  {{ id: "fleece-jacket", slot: "layer", name: "high-pile fleece jacket", fit: "relaxed", sil: EVEN, occ: {ALLOCC}, dept: BOTH, base: 90, colors: ALL, material: "recycled polyester fleece", tags: ["trend", "sustainable"] }},
  {{ id: "moto",       slot: "layer", name: "faux-leather moto jacket", fit: "slim", sil: EVEN, occ: {ALLOCC}, dept: BOTH, base: 85, colors: ALL, material: "vegan leather", tags: ["trend"] }},
  {{ id: "extra-wide-jean", slot: "bottom", name: "extra-wide jeans", fit: "relaxed", sil: SMALL_TOP, occ: {ALLOCC}, dept: BOTH, base: 80, colors: ALL, material: "rigid cotton denim", tags: ["trend"] }},
  {{ id: "stacked-jean", slot: "bottom", name: "stacked flare jeans", fit: "slim", sil: BIG_TOP, occ: {ALLOCC}, dept: BOTH, base: 60, colors: ALL, material: "stretch denim", tags: ["trend"] }},
  {{ id: "hobo",       slot: "accessory", name: "leather hobo bag", fit: "regular", sil: EVEN, occ: {ALLOCC}, dept: BOTH, base: 90, colors: ALL, material: "soft pebbled leather", tags: ["trend"] }},
  {{ id: "chain",''')
R('''  "quarter-zip": ["quarter-zip", 0, 1.66],''', '''  "shell": ["shell-jacket", 0, 1.9], "fleece-jacket": ["fleece-jacket", 0, 1.9], "moto": ["moto-jacket", 0, 1.8],
  "extra-wide-jean": ["extra-wide-jeans", 0, 1.35, "full"], "stacked-jean": ["stacked-jeans", 0, 1.05, "full"], "hobo": ["hobo-bag", .5, .62, null, 1.0],
  "quarter-zip": ["quarter-zip", 0, 1.66],''')
R('''const JACKET_IDS = [''', '''const JACKET_IDS = ["shell", "fleece-jacket", "moto", ''')
R('''        "trench": m.crotchY + legSpan * .5,''', '''        "trench": m.crotchY + legSpan * .5, "shell": m.crotchY + CANVAS_H * .03, "fleece-jacket": m.crotchY + CANVAS_H * .01, "moto": m.waistY + CANVAS_H * .07,''')
R('''[...(["shoes", "layer"].includes(style.slot) || ["cap", "beanie", "crossbody", "tote"].includes(style.id)''', '''[...(["shoes", "layer"].includes(style.slot) || ["cap", "beanie", "crossbody", "tote", "hobo"].includes(style.id)''')
R('''  bag:     { label: "Bag",     ids: ["crossbody", "tote"] },''', '''  bag:     { label: "Bag",     ids: ["crossbody", "tote", "hobo"] },''')
R('''    if (item.id === "chain")''', '''    // Hobo bags suit softer styles, crossbody bags the sportier ones.
    if (["hobo", "crossbody", "tote"].includes(item.id)) {
      const bag = { bohemian: "hobo", classic: "hobo", minimalist: "crossbody", streetwear: "crossbody", athleisure: "tote" }[ctx.style] || "crossbody";
      return item.id === bag && !!shoes && item.color === shoes.color;
    }
    if (item.id === "chain")''')

# Recipes: Musinsa wide denim, shell and fleece; Fashion Nova stacked jeans, moto jacket, matching sets.
R('''const look = (tops, dark, light, shoes, shoeColor, layers) => ({ tops, dark, light, shoes, shoeColor, layers });''',
  '''const look = (tops, dark, light, shoes, shoeColor, layers, inspo = "", match = false) => ({ tops, dark, light, shoes, shoeColor, layers, inspo, match });''')
start = s.index('  athleisure: [')
end = s.index('  bohemian: [')
s = s[:start] + '''  athleisure: [
    look(["quarter-zip-fleece"], ["tapered-jog", "track-pant"], ["track-pant", "tapered-jog"], ["runner"], "white", ["track-top"]),
    look(["quarter-zip-short"], ["track-pant"], ["track-pant"], ["chunky-snk"], "white", ["fleece-jacket"], "Musinsa's fleece outerwear"),
    look(["quarter-zip"], ["tapered-jog"], ["tapered-jog"], ["runner"], "black", ["track-top"], "Fashion Nova's matching sets", true)
  ],
  minimalist: [
    look(["quarter-zip"], ["cig-pant", "slim-jean"], ["str-pant", "slim-khakis"], ["low-snk"], "white", ["chore"]),
    look(["quarter-zip-short"], ["str-pant"], ["str-pant"], ["loafer"], "black", ["shell"], "Musinsa's technical shells"),
    look(["quarter-zip-fleece"], ["extra-wide-jean", "cig-pant"], ["str-pant", "extra-wide-jean"], ["chelsea"], "black", ["blazer"], "Musinsa's extra-wide denim")
  ],
  streetwear: [
    look(["quarter-zip-waffle"], ["extra-wide-jean", "cargo"], ["extra-wide-jean", "cargo"], ["chunky-snk"], "white", ["shell"], "Musinsa's extra-wide denim and shells"),
    look(["quarter-zip-short-waffle"], ["stacked-jean"], ["stacked-jean"], ["chunky-snk"], "black", ["moto"], "Fashion Nova's stacked jeans and moto jackets"),
    look(["quarter-zip"], ["cargo", "wide-jean"], ["cargo", "wide-sweat"], ["low-snk"], "white", ["fleece-jacket"], "Musinsa's fleece outerwear")
  ],
''' + s[end:]
R('''    const ids = ctx.anyCut ? ANY_CUT : all ? looks.flatMap(l => light ? l.dark : l.light) : light ? recipe.dark : recipe.light;
    return ids.includes(item.id) && PAIRS[ctx.bread].includes(item.color);''', '''    const ids = ctx.anyCut ? ANY_CUT : all ? looks.flatMap(l => light ? l.dark : l.light) : light ? recipe.dark : recipe.light;
    // A matching set repeats the top's color; every other look contrasts it.
    if (!all && recipe.match && !ctx.anyCut) return ids.includes(item.id) && item.color === ctx.bread;
    return ids.includes(item.id) && PAIRS[ctx.bread].includes(item.color);''')
R('''  return {
    id: nextId++, silhouette, occasion: ctx.occasion, items, look: ctx.look, style: a.style,''', '''  return {
    id: nextId++, silhouette, occasion: ctx.occasion, items, look: ctx.look, style: a.style,
    inspo: ((STYLE_LOOKS[a.style] || [])[ctx.look] || {}).inspo || "",''')
R('''  const pattern = `${cap(tone(top))} on top, ${tone(bottom)} in the middle, ${tone(shoes)} at your feet.`;''', '''  const matched = top.color === bottom.color;
  const pattern = matched ? `A matching ${c(top.color)} set, finished with ${c(shoes.color)} ${shoes.name}.` : `${cap(tone(top))} on top, ${tone(bottom)} in the middle, ${tone(shoes)} at your feet.`;''')
R('''pairing.${coatLine}${extraLine}`;''', '''pairing.${coatLine}${extraLine}${outfit.inspo ? ` Inspired by ${outfit.inspo}.` : ""}`;''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
