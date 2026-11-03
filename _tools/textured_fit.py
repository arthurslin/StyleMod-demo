"""Add textured quarter zips, and fit garments to measured landmarks on each dummy."""
import os, shutil
import numpy as np
from PIL import Image
from scipy import ndimage as ni

TR = chr(92) * 2 + '?' + chr(92) + os.path.normpath('C:/Users/assau/.claude/projects/C--Users-assau-AppData-Local-Claude-Data-claude-pzs8sxrjxfjjc-scratch-workspaces-8474f37f-6985-4bd0-95bb-6815984069ce-5469b8fd-b440-434a-8d03-7d8ef7a48bc6-scratch-2026-11-02-8ddb02/4f8ba79b-2c4f-4fb9-866f-a3d32b0037cf/tool-results')

def cut_to_webp(tag, name):
    src = [os.path.join(TR, f) for f in os.listdir(TR) if f.endswith(f'-{tag}.jpg')][0]
    shutil.copy(src, f'_gen/{name}.jpg')
    a = np.array(Image.open(src).convert('RGB')).astype('float32')
    lab, _ = ni.label(a.min(2) > 238)
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

cut_to_webp('3joj4a', 'quarter-zip-waffle')
cut_to_webp('ta3l4y', 'quarter-zip-cable')
cut_to_webp('07o2z3', 'quarter-zip-fleece')

p = 'index.html'
s = open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)

R('''  { id: "quarter-zip", slot: "top", name: "quarter zip",''', '''  { id: "quarter-zip-waffle", slot: "top", name: "waffle-knit quarter zip", fit: "regular", sil: EVEN, occ: ["casual", "work", "night", "athleisure", "gym", "weekend"], dept: BOTH, base: 80, colors: ALL, material: "cotton waffle knit", tags: ["durable", "trend"] },
  { id: "quarter-zip-cable", slot: "top", name: "cable-knit quarter zip", fit: "regular", sil: EVEN, occ: ["casual", "work", "night", "athleisure", "gym", "weekend"], dept: BOTH, base: 95, colors: ALL, material: "chunky wool-blend cable knit", tags: ["durable"] },
  { id: "quarter-zip-fleece", slot: "top", name: "ribbed fleece quarter zip", fit: "regular", sil: EVEN, occ: ["casual", "work", "night", "athleisure", "gym", "weekend"], dept: BOTH, base: 70, colors: ALL, material: "recycled ribbed fleece", tags: ["sustainable"] },
  { id: "quarter-zip", slot: "top", name: "quarter zip",''')
R('''  if (item.slot === "top") return item.id === "quarter-zip" && item.color === ctx.bread;''',
  '''  if (item.slot === "top") return item.id.startsWith("quarter-zip") && item.color === ctx.bread;''')
R('''${cap(COLORS[outfit.items.top.color].label.toLowerCase())} quarter-zip sandwich</h3>''', '''${cap(COLORS[outfit.items.top.color].label.toLowerCase())} ${outfit.items.top.name} sandwich</h3>''')
R('''The ${bread} quarter zip and ${bread} ${shoes.name}''', '''The ${bread} ${top.name} and ${bread} ${shoes.name}''')

# --- Placement by measured landmarks.
R('''  "quarter-zip": ["quarter-zip", .12, 1.66], "khakis": ["straight-trousers", .31, .92, .665], "slim-khakis": ["slim-jeans", .31, .84, .655],''',
  '''  "quarter-zip": ["quarter-zip", 0, 1.66], "quarter-zip-waffle": ["quarter-zip-waffle", 0, 1.66], "quarter-zip-cable": ["quarter-zip-cable", 0, 1.7],
  "quarter-zip-fleece": ["quarter-zip-fleece", 0, 1.66], "khakis": ["straight-trousers", 0, 1.15, "full"], "slim-khakis": ["slim-jeans", 0, 1.05, "full"],''')
import re
# Bottoms: [image, unused, ease over the hips, length].
lengths = {'midi-skirt': 'midi', 'maxi-skirt': 'ankle', 'gym-short': 'knee'}
ease = {'slim': 1.05, 'straight': 1.15, 'wide': 1.35}
def fix_bottom(m):
    sid, img = m.group(1), m.group(2)
    kind = 'wide' if any(k in sid for k in ('wide', 'parachute', 'cargo', 'gym-short', 'midi')) else 'slim' if any(k in sid for k in ('slim', 'cig', 'tapered', 'flare')) else 'straight'
    return f'"{sid}": ["{img}", 0, {ease[kind]}, "{lengths.get(sid, "full")}"]'
s = re.sub(r'"([a-z-]+)": \["([a-z-]+)", \.31, [\d.]+, \.\d+\]', fix_bottom, s)
assert '.31,' not in s.split('const WEAR = {')[1].split('};')[0]

R('''async function paintDummy(canvas, outfit) {''', '''/* Landmarks measured from the mannequin's own outline, so every garment lands on
   the right waist, hips and ankles for that form. */
const formMarks = {};
function alphaOf(img) {
  const c = document.createElement("canvas");
  c.width = img.width; c.height = img.height;
  const g = c.getContext("2d");
  g.drawImage(img, 0, 0);
  const data = g.getImageData(0, 0, c.width, c.height).data;
  return (x, y) => data[(Math.round(y) * c.width + Math.round(x)) * 4 + 3] > 128;
}
function measureForm(img) {
  const solid = alphaOf(img), W = img.width, H = img.height, cx = W / 2;
  const run = (y, from = cx) => {
    if (!solid(from, y)) return 0;
    let l = from, r = from;
    while (l > 0 && solid(l - 1, y)) l--;
    while (r < W - 1 && solid(r + 1, y)) r++;
    return r - l;
  };
  const rows = (a, b) => Array.from({ length: Math.round((b - a) * H) }, (_, i) => Math.round(a * H) + i);
  const neckY = rows(.08, .18).reduce((best, y) => run(y) && run(y) < run(best) ? y : best, Math.round(.14 * H));
  const waistY = rows(.27, .4).reduce((best, y) => run(y) < run(best) ? y : best, Math.round(.33 * H));
  const crotchY = rows(.4, .6).find(y => !solid(cx, y)) || Math.round(.48 * H);
  const hipW = Math.max(...rows(.38, crotchY / H).map(y => run(y)));
  const legX = cx - hipW / 4;
  const ankleY = rows(.84, .97).reduce((best, y) => run(y, legX) && run(y, legX) < run(best, legX) ? y : best, Math.round(.93 * H));
  const footY = rows(.9, 1).filter(y => solid(legX, y) || solid(legX - 8, y) || solid(legX + 8, y)).pop() || H - 1;
  return { neckY, waistY, waistW: run(waistY), hipW, crotchY, ankleY, footY };
}
const garmentMarks = new Map();
function waistbandWidth(img) {
  if (!garmentMarks.has(img)) {
    const solid = alphaOf(img), y = img.height * .03;
    let n = 0;
    for (let x = 0; x < img.width; x++) if (solid(x, y)) n++;
    garmentMarks.set(img, n);
  }
  return garmentMarks.get(img);
}

/* Bottoms keep their own proportions: height sets the scale, and width only
   stretches when the waistband would otherwise be narrower than the waist. */
function placeBottom(img, item, m) {
  const [, , ease, length] = WEAR[item.id];
  const top = m.waistY - (m.crotchY - m.waistY) * .12;
  const legSpan = m.ankleY - m.crotchY;
  const hem = { full: m.ankleY + (m.footY - m.ankleY) * .45, ankle: m.ankleY, midi: m.crotchY + legSpan * .72, knee: m.crotchY + legSpan * .42 }[length];
  const scale = (hem - top) / img.height;
  let width = img.width * scale;
  const band = waistbandWidth(img) * scale;
  const minBand = m.waistW * 1.04;
  if (band < minBand) width *= Math.min(1.25, minBand / band);
  width = Math.min(width, m.hipW * ease * 1.6);
  return { x: MID - width / 2, y: top, width, height: hem - top };
}

async function paintDummy(canvas, outfit) {''')

R('''  g.drawImage(dummy, MID - dummy.width / 2, 0);
  order.forEach((item, i) => {
    const [, topEdge, widthShare, heightShare, offset] = WEAR[item.id];
    const img = garments[i];
    // Under a jacket, the top is drawn narrower so its sleeves stay inside.
    const width = form.size * widthShare * (item === top && layer && JACKET_IDS.includes(layer.id) ? .8 : 1);
    const height = heightShare ? CANVAS_H * heightShare : img.height * width / img.width;
    const x = MID - width / 2 + (offset || 0) * form.size;
    g.drawImage(tinted(img, COLORS[item.color].hex), x, CANVAS_H * topEdge, width, height);
  });''', '''  g.drawImage(dummy, MID - dummy.width / 2, 0);
  const m = formMarks[form.src] || (formMarks[form.src] = measureForm(dummy));
  order.forEach((item, i) => {
    const [, topEdge, widthShare, , offset] = WEAR[item.id];
    const img = garments[i];
    let box;
    if (item.slot === "bottom") box = placeBottom(img, item, m);
    else {
      // Under a jacket, the top is drawn narrower so its sleeves stay inside.
      const width = form.size * widthShare * (item === top && layer && JACKET_IDS.includes(layer.id) ? .8 : 1);
      const height = img.height * width / img.width;
      const y = item.slot === "shoes" ? m.footY - height + 4
        : item.slot === "top" || JACKET_IDS.includes(item.id) || item.id === "scarf" ? m.neckY - CANVAS_H * .02
        : CANVAS_H * topEdge;
      box = { x: MID - width / 2 + (offset || 0) * form.size, y, width, height };
    }
    g.drawImage(tinted(img, COLORS[item.color].hex), box.x, box.y, box.width, box.height);
  });''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched')
