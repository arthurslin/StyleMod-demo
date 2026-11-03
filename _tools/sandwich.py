"""Easy quiz: every result is a quarter zip with jeans or khakis, styled with the sandwich method."""
import os, re, shutil
import numpy as np
from PIL import Image
from scipy import ndimage as ni

TR = chr(92) * 2 + '?' + chr(92) + os.path.normpath('C:/Users/assau/.claude/projects/C--Users-assau-AppData-Local-Claude-Data-claude-pzs8sxrjxfjjc-scratch-workspaces-8474f37f-6985-4bd0-95bb-6815984069ce-5469b8fd-b440-434a-8d03-7d8ef7a48bc6-scratch-2026-11-02-8ddb02/4f8ba79b-2c4f-4fb9-866f-a3d32b0037cf/tool-results')
src = [os.path.join(TR, f) for f in os.listdir(TR) if f.endswith('-xg4bvj.jpg')][0]
shutil.copy(src, '_gen/quarter-zip.jpg')
a = np.array(Image.open('_gen/quarter-zip.jpg').convert('RGB')).astype('float32')
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
im.save('images/wear/quarter-zip.webp', quality=84, method=6)
print(im.size)

p = 'index.html'
s = open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)

R('''  // Bottoms
  { id: "slim-chino",''', '''  { id: "quarter-zip", slot: "top", name: "quarter zip", fit: "regular", sil: EVEN, occ: ["casual", "work", "night", "athleisure", "gym", "weekend"], dept: BOTH, base: 75, colors: ALL, material: "merino-cotton knit", tags: ["durable", "trend"] },

  // Bottoms
  { id: "khakis",     slot: "bottom", name: "khakis", fit: "regular", sil: EVEN, occ: ["casual", "work", "night", "athleisure", "gym", "weekend"], dept: BOTH, base: 65, colors: ["beige", "camel"], material: "cotton twill", tags: ["durable"] },
  { id: "slim-khakis", slot: "bottom", name: "slim khakis", fit: "slim", sil: EVEN, occ: ["casual", "work", "night", "athleisure", "gym", "weekend"], dept: BOTH, base: 65, colors: ["beige", "camel"], material: "stretch cotton twill", tags: ["durable"] },
  { id: "slim-chino",''')
R('''const CATALOG = STYLES.flatMap(style => [...new Set([...style.colors, PHOTO_COLORS[style.id]])].flatMap(color =>''',
  '''const CATALOG = STYLES.flatMap(style => [...new Set([...(style.slot === "shoes" ? ALL : style.colors), PHOTO_COLORS[style.id]])].filter(Boolean).flatMap(color =>''')
R('''const WEAR = {
''', '''const WEAR = {
  "quarter-zip": ["quarter-zip", .12, 1.66], "khakis": ["straight-trousers", .31, .92, .665], "slim-khakis": ["slim-jeans", .31, .84, .655],
''')

# The outfit formula replaces the fit and silhouette rules.
start = s.index('    if (slot === "top" || slot === "bottom") {\n      if (!item.sil.includes(silhouette))')
end = s.index('    return true;\n  };\n  const allowed')
s = s[:start] + '    return fitsFormula(item, ctx);\n' + s[end + len('    return true;\n'):]
R('''/* Hard rules. Department comes only from the customer's explicit choice. */''', '''/* The sandwich method: the same color at the top and the feet (the bread), with
   contrasting jeans or khakis in the middle (the filling). */
const JEANS = ["str-jean", "slim-jean"];
const KHAKIS = ["khakis", "slim-khakis"];
const DENIM_COLORS = ["navy", "slate", "black"];

function fitsFormula(item, ctx) {
  if (item.slot === "top") return item.id === "quarter-zip" && item.color === ctx.bread;
  if (item.slot === "shoes") return item.color === ctx.bread;
  if (item.slot === "bottom") {
    if (item.color === ctx.bread) return false;
    const isJeans = JEANS.includes(item.id) && DENIM_COLORS.includes(item.color);
    const isKhakis = KHAKIS.includes(item.id);
    return ctx.jeans === undefined ? isJeans || isKhakis : ctx.jeans ? isJeans : isKhakis;
  }
  return false;
}

/* Hard rules. Department comes only from the customer's explicit choice. */''')
R('''  const { a, silhouette } = ctx;
''', '''  const { a } = ctx;
''')
R('''    tier: budgetTier(a)
  };

  const items = {};
  Object.keys(SLOTS).forEach(slot => {
    items[slot] = pickBest(slot, ctx);
    ctx.chosen.push(items[slot]);
  });''', '''    tier: budgetTier(a),
    bread: a.favorite || "navy",
    jeans: index % 2 === 0
  };

  const items = {};
  Object.keys(SLOTS).forEach(slot => {
    items[slot] = pickBest(slot, ctx);
    if (items[slot]) ctx.chosen.push(items[slot]);
  });''')
R('''    hero: null, tier: budgetTier(a), usedColors: new Set(),''', '''    hero: null, tier: budgetTier(a), usedColors: new Set(), bread: a.favorite || "navy",''')
R('''dept: "unisex", occasions: [], palettes: [], avoid: [],
  body: "unsure", fit: "regular", silhouette: "surprise",''', '''dept: "unisex", occasions: [], palettes: [], avoid: [],
  body: "unsure", fit: "regular", silhouette: "balanced",''')
R('''    const colors = [...new Set([top.color, bottom.color])];
    colors.forEach''', '''    const colors = [bottom.color];
    colors.forEach''')
R('''  return `The ${top.name} and ${bottom.name} carry a similar amount of volume, so neither half dominates. That gives you an even, balanced line from shoulder to hem. ${close}`;''',
  '''  const bread = COLORS[top.color].label.toLowerCase();
  const filling = `${COLORS[bottom.color].label.toLowerCase()} ${bottom.name}`;
  return `This uses the sandwich method. The ${bread} quarter zip and ${bread} ${shoes.name} are the bread, and the ${filling} are the filling. Repeating one color at the top and at your feet ties the outfit together, while the contrast in the middle keeps it interesting.`;''')
R('''  const { top, bottom, shoes } = outfit.items;
  const close = `The ${shoes.name} ${shoes.note}.`;
''', '''  const { top, bottom, shoes } = outfit.items;
''')
s = re.sub(r'  if \(outfit\.silhouette === "small-top"\) \{\n    return `The \$\{top\.name\} stays.*?\n  \}\n  if \(outfit\.silhouette === "big-top"\) \{.*?\n  \}\n', '', s, flags=re.S)
R('''id="outfit-title-${index}" tabindex="-1">${SILHOUETTES[outfit.silhouette].label}</h3>''', '''id="outfit-title-${index}" tabindex="-1">${cap(COLORS[outfit.items.top.color].label.toLowerCase())} quarter-zip sandwich</h3>''')
R('''Answer a short quiz and get three complete looks, each with a plain-language reason it was chosen for you.''', '''Answer three taps and get three quarter-zip outfits, each styled with the sandwich method and a plain-language reason it was chosen for you.''')
R('''hint: "We'll build your outfits around it.",''', '''hint: "Your quarter zip and shoes will match it.",''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched')
