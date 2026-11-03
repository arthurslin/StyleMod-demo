"""Real shoe images, an outer layer that matches the shoes, and torso-based fitting."""
p = 'index.html'
s = open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)

# Shoes and layers can be any color in this version.
R('''[...(style.slot === "shoes" ? ALL : style.colors), PHOTO_COLORS[style.id]]''', '''[...(style.slot === "shoes" || style.slot === "layer" ? ALL : style.colors), PHOTO_COLORS[style.id]]''')

# Layers per look, in the shoe color.
R('''    shoes: ["low-snk", "chunky-snk"], lightShoes: ["white"], darkShoes: ["white"] },''', '''    shoes: ["low-snk", "chunky-snk"], lightShoes: ["white"], darkShoes: ["white"], layers: ["chore", "crop-puffer"] },''')
R('''    shoes: ["loafer", "chelsea"], lightShoes: ["brown"], darkShoes: ["brown"] },''', '''    shoes: ["loafer", "chelsea"], lightShoes: ["brown"], darkShoes: ["brown"], layers: ["trench", "chore"] },''')
R('''    shoes: ["chelsea", "chunky-snk", "loafer"], lightShoes: ["black"], darkShoes: ["black"] }''', '''    shoes: ["chelsea", "chunky-snk", "loafer"], lightShoes: ["black"], darkShoes: ["black"], layers: ["blazer", "crop-puffer"] }''')
R('''  return false;
}

/* Hard rules''', '''  if (item.slot === "layer") {
    // The outer layer repeats the shoe color, so the look is framed top to bottom.
    const shoes = ctx.chosen && ctx.chosen.find(i => i.slot === "shoes");
    const ids = ctx.look === undefined ? LOOKS.flatMap(l => l.layers) : look.layers;
    return !ctx.gym && !!shoes && ids.includes(item.id) && item.color === shoes.color;
  }
  return false;
}

/* Hard rules''')
R('''  // These looks have no layer, so there's nothing to relax.
  if (slot === "layer") return [];
''', '')
R('''  const allowed = CATALOG.filter(item => matches(item) && !a.avoid.includes(item.color));''', '''  const allowed = CATALOG.filter(item => matches(item) && !a.avoid.includes(item.color));
  if (slot === "layer") return allowed;''')
# Real shoe photos win over tinted drawings when both fit.
R('''  if (item.photo) total += 3;''', '''  if (item.photo) total += 3;
  if (item.slot === "shoes" && REAL_SHOES[`${item.id}|${item.color}`]) total += 10;''')
# Keep the layer in step when the shoes are swapped.
R('''  outfit.items[slot] = ranked[0][1];
  outfit.savedId = null;''', '''  outfit.items[slot] = ranked[0][1];
  const coat = outfit.items.layer;
  if (slot === "shoes" && coat) outfit.items.layer = BY_KEY.get(`${coat.id}|${outfit.items.shoes.color}|${coat.tier}`) || coat;
  outfit.savedId = null;''')
R('''    hero: null, tier: budgetTier(a), usedColors: new Set(), bread: a.favorite || "navy", look: outfit.look, gym: ctx_gym(a), pants: a.pants,''',
  '''    hero: null, tier: budgetTier(a), usedColors: new Set(), bread: a.favorite || "navy", look: outfit.look, gym: ctx_gym(a), pants: a.pants,''')
R('''  return `${pattern} The ${c(bottom.color)} ${bottom.name} make the ${c(top.color)} ${top.name} and ${c(shoes.color)} ${shoes.name} stand out. ${cap(c(bottom.color))} and ${c(top.color)} are an easy, classic pairing.`;''',
  '''  const coat = outfit.items.layer;
  const coatLine = coat ? ` The ${c(coat.color)} ${coat.name} matches your ${shoes.name}, which ties the look together.` : "";
  return `${pattern} The ${c(bottom.color)} ${bottom.name} make the ${c(top.color)} ${top.name} and ${c(shoes.color)} ${shoes.name} stand out. ${cap(c(bottom.color))} and ${c(top.color)} are an easy, classic pairing.${coatLine}`;''')

# --- Real shoe images and body-based fitting.
R('''const JACKET_IDS = [''', '''/* Shoes photographed in their real color. These are drawn as-is, never tinted. */
const REAL_SHOES = { "low-snk|white": "low-snk-white", "loafer|brown": "loafer-brown" };
function loadShoe(name) {
  const key = "shoe:" + name;
  if (!imageCache[key]) {
    imageCache[key] = new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = `images/shoes/${name}.webp`;
    });
  }
  return imageCache[key];
}

const JACKET_IDS = [''')
R('''const garmentMarks = new Map();''', '''/* A top's own body width, measured below the sleeves' reach. */
const torsoMarks = new Map();
function torsoWidth(img) {
  if (!torsoMarks.has(img)) {
    const solid = alphaOf(img), y = img.height * .62, cx = img.width / 2;
    let l = cx, r = cx;
    while (l > 0 && solid(l - 1, y)) l--;
    while (r < img.width - 1 && solid(r + 1, y)) r++;
    torsoMarks.set(img, r - l);
  }
  return torsoMarks.get(img);
}

const garmentMarks = new Map();''')
R('''  const armSpan = Math.max(...rows(.3, .42).map(spanAt));
  return { neckY, waistY, waistW: run(waistY), hipW, crotchY, ankleY, footY, armSpan };''', '''  const armSpan = Math.max(...rows(.3, .42).map(spanAt));
  // Chest: below the armpits, where the arms have separated from the body.
  const chestY = Math.round(neckY + (waistY - neckY) * .6);
  const chestRun = run(chestY);
  const chestW = chestRun && chestRun < hipW * 1.3 ? chestRun : run(waistY) * 1.2;
  const feetW = spanAt(footY - 14);
  return { neckY, waistY, waistW: run(waistY), hipW, crotchY, ankleY, footY, armSpan, chestW, feetW };''')
R('''  const [dummy, ...garments] = await Promise.all([form.src, ...order.map(i => WEAR[i.id][0])].map(loadImage));''', '''  const real = item => item.slot === "shoes" && REAL_SHOES[`${item.id}|${item.color}`];
  const [dummy, ...garments] = await Promise.all([loadImage(form.src), ...order.map(i => real(i) ? loadShoe(real(i)) : loadImage(WEAR[i.id][0]))]);''')
R('''    let box;
    if (item.slot === "bottom") box = placeBottom(img, item, m);
    else {''', '''    let box;
    const jacket = JACKET_IDS.includes(item.id);
    if (item.slot === "bottom") box = placeBottom(img, item, m);
    else if (item.slot === "top" || jacket) {
      // The garment's own body width lands on the dummy's chest, plus room to wear it.
      const ease = jacket ? 1.38 : item.id === "quarter-zip-cable" ? 1.2 : 1.14;
      const under = item === top && layer && JACKET_IDS.includes(layer.id) ? .94 : 1;
      const width = img.width * (m.chestW * ease * under / torsoWidth(img));
      const height = img.height * width / img.width;
      box = { x: MID - width / 2, y: m.neckY - CANVAS_H * (jacket ? .03 : .022), width, height };
    } else if (item.slot === "shoes") {
      const width = m.feetW * (real(item) ? 1.32 : 1.25);
      const height = img.height * width / img.width;
      box = { x: MID - width / 2, y: m.footY - height + 6, width, height };
    } else {''')
R('''    g.drawImage(tinted(img, COLORS[item.color].hex), box.x, box.y, box.width, box.height);''', '''    g.drawImage(real(item) ? img : tinted(img, COLORS[item.color].hex), box.x, box.y, box.width, box.height);''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
