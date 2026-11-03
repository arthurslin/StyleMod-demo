"""Short-sleeve zips, realistic shoes drawn over the pants, and a pants color pick."""
import os, shutil
import numpy as np
from PIL import Image
from scipy import ndimage as ni

TR = chr(92) * 2 + '?' + chr(92) + os.path.normpath('C:/Users/assau/.claude/projects/C--Users-assau-AppData-Local-Claude-Data-claude-pzs8sxrjxfjjc-scratch-workspaces-8474f37f-6985-4bd0-95bb-6815984069ce-5469b8fd-b440-434a-8d03-7d8ef7a48bc6-scratch-2026-11-02-8ddb02/4f8ba79b-2c4f-4fb9-866f-a3d32b0037cf/tool-results')

def cut_to_webp(tag, name):
    src = [os.path.join(TR, f) for f in os.listdir(TR) if f.endswith(f'-{tag}.jpg')][0]
    shutil.copy(src, f'_gen/{name}.jpg')
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

cut_to_webp('4uhh54', 'quarter-zip-short')
cut_to_webp('4rgbgx', 'quarter-zip-short-waffle')

p = 'index.html'
s = open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)

# Brown, mainly for leather shoes.
R('''  camel:   { label: "Camel",   hex: "#b98a4f", family: "earth" },''', '''  camel:   { label: "Camel",   hex: "#b98a4f", family: "earth" },
  brown:   { label: "Brown",   hex: "#5a3a26", family: "earth" },''')
R('''  slate: ["beige", "white"], rust: ["beige", "white"],''', '''  slate: ["beige", "white"], rust: ["beige", "white"], brown: ["beige", "white", "grey"],''')

R('''  { id: "quarter-zip", slot: "top", name: "quarter zip",''', '''  { id: "quarter-zip-short", slot: "top", name: "short-sleeve quarter zip", fit: "regular", sil: EVEN, occ: ["casual", "work", "night", "athleisure", "gym", "weekend"], dept: BOTH, base: 60, colors: ALL, material: "fine cotton knit", tags: ["trend"] },
  { id: "quarter-zip-short-waffle", slot: "top", name: "short-sleeve waffle quarter zip", fit: "regular", sil: EVEN, occ: ["casual", "work", "night", "athleisure", "gym", "weekend"], dept: BOTH, base: 65, colors: ALL, material: "cotton waffle knit", tags: ["trend"] },
  { id: "quarter-zip", slot: "top", name: "quarter zip",''')
R('''  "quarter-zip": ["quarter-zip", 0, 1.66],''', '''  "quarter-zip": ["quarter-zip", 0, 1.66], "quarter-zip-short": ["quarter-zip-short", 0, 1.5], "quarter-zip-short-waffle": ["quarter-zip-short-waffle", 0, 1.5],''')

# Looks: more tops, cuts that always exist in every pairing color, and real shoe colors.
start = s.index('const LOOKS = [')
end = s.index('];', start) + 2
s = s[:start] + '''const LOOKS = [
  { tops: ["quarter-zip", "quarter-zip-short"], dark: ["str-jean", "slim-jean", "cig-pant"], light: ["khakis", "slim-khakis", "str-pant"],
    shoes: ["low-snk", "chunky-snk"], lightShoes: ["white"], darkShoes: ["black"] },
  { tops: ["quarter-zip-waffle", "quarter-zip-fleece", "quarter-zip-short-waffle"], dark: ["str-pant", "cig-pant"], light: ["str-jean", "slim-khakis", "str-pant"],
    shoes: ["loafer", "chelsea"], lightShoes: ["beige", "grey"], darkShoes: ["brown", "black"] },
  { tops: ["quarter-zip-cable"], dark: ["wide-pant", "cargo"], light: ["wide-pant", "khakis"],
    shoes: ["chelsea", "chunky-snk"], lightShoes: ["white", "beige"], darkShoes: ["black", "brown"] }
];''' + s[end:]
start = s.index('  if (item.slot === "shoes") {\n    const ids = ctx.gym')
end = s.index('  return false;\n}', start)
s = s[:start] + '''  if (item.slot === "shoes") {
    // Shoes stay in real shoe colors, light or dark to match the top.
    const ids = ctx.gym ? ["runner", "chunky-snk"] : ctx.look === undefined ? LOOKS.flatMap(l => l.shoes) : look.shoes;
    const colors = ctx.look === undefined ? (light ? ["white", "beige", "grey"] : ["black", "brown"]) : light ? look.lightShoes : look.darkShoes;
    return ids.includes(item.id) && colors.includes(item.color);
  }
''' + s[end:]
R('''    return ids.includes(item.id) && PAIRS[ctx.bread].includes(item.color);''', '''    const colors = ctx.pants && PAIRS[ctx.bread].includes(ctx.pants) ? [ctx.pants] : PAIRS[ctx.bread];
    return ids.includes(item.id) && colors.includes(item.color);''')
R('''    look: index % LOOKS.length,''', '''    look: index % LOOKS.length,
    pants: a.pants,''')
R('''bread: a.favorite || "navy", look: outfit.look, gym: ctx_gym(a),''', '''bread: a.favorite || "navy", look: outfit.look, gym: ctx_gym(a), pants: a.pants,''')
R('''  favorite: "",''', '''  favorite: "", pants: "",''')

# Shoes are drawn after the pants, so they sit in front of the hem.
R('''const order = [shoes, bottom, top, layer].filter(Boolean);''', '''const order = [bottom, shoes, top, layer].filter(Boolean);''')

# Step 1: pick a main color, then a pants color; pairs that don't work are greyed out.
R('''    body: `<fieldset class="section"><legend class="sr">Favorite color</legend>
        <div class="color-picks">${ALL.map(c => `<label class="color-pick"><input type="radio" name="favorite" value="${c}" ${answers.favorite === c ? "checked" : ""}><span><i style="background:${COLORS[c].hex}" aria-hidden="true"></i>${COLORS[c].label}</span></label>`).join("")}</div>
      </fieldset>`''', '''    body: `<fieldset class="section"><legend class="sr">Main color</legend>
        <div class="color-picks">${ALL.map(c => `<label class="color-pick"><input type="radio" name="favorite" value="${c}" ${answers.favorite === c ? "checked" : ""}><span><i style="background:${COLORS[c].hex}" aria-hidden="true"></i>${COLORS[c].label}</span></label>`).join("")}</div>
      </fieldset>
      ${answers.favorite ? `<fieldset class="section"><legend>Pants color</legend>
        <p class="hint">Only colors that pair with ${COLORS[answers.favorite].label.toLowerCase()} can be picked. The rest are greyed out.</p>
        <div class="color-picks">
          <label class="color-pick"><input type="radio" name="pants" value="" ${!answers.pants ? "checked" : ""}><span><i class="any" aria-hidden="true"></i>Any match</span></label>
          ${ALL.filter(c => c !== answers.favorite).map(c => {
            const ok = PAIRS[answers.favorite].includes(c);
            return `<label class="color-pick"><input type="radio" name="pants" value="${c}" ${ok ? "" : "disabled"} ${answers.pants === c ? "checked" : ""}><span><i style="background:${COLORS[c].hex}" aria-hidden="true"></i>${COLORS[c].label}${ok ? "" : '<span class="sr"> (does not pair)</span>'}</span></label>`;
          }).join("")}
        </div>
      </fieldset>` : ""}`''')
R('''  else if (input.name === "favorite") {
    answers.favorite = input.value;
    answers.palettes = [...new Set([COLORS[input.value].family, "neutral"])];
  }''', '''  else if (input.name === "favorite") {
    answers.favorite = input.value;
    answers.palettes = [...new Set([COLORS[input.value].family, "neutral"])];
    if (!PAIRS[input.value].includes(answers.pants)) answers.pants = "";
    render(`[name="favorite"][value="${input.value}"]`);
  }''')
R('''  .color-pick input:focus-visible + span {''', '''  .color-pick input:disabled + span { opacity: .35; filter: grayscale(1); cursor: not-allowed; }
  .color-pick input:disabled { cursor: not-allowed; }
  .color-pick i.any { background: conic-gradient(#1f2d4d 0 25%, #d9c8ad 0 50%, #1f1f21 0 75%, #f8f6f1 0); }
  .color-pick input:focus-visible + span {''')
R('''title: "Pick a color",''', '''title: "Pick your colors",''')
R('''hint: "Your quarter zip will be this color.",''', '''hint: "First your quarter zip, then your pants.",''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
