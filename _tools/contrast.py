"""Light-dark contrast looks with complementary colors and three distinct recipes."""
import re
p = 'index.html'
s = open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)

start = s.index('/* The sandwich method:')
end = s.index('/* Hard rules. Department comes only')
s = s[:start] + '''/* Simple contrast: a light top gets dark pants and light shoes, and a dark top
   gets light pants and dark shoes. Pants come from colors that pair well with the
   top, and each of the three looks changes the texture, cut and shoes. */
const LIGHT = ["white", "beige", "grey", "sage", "camel", "mustard"];
const PAIRS = {
  white: ["navy", "black", "olive"], beige: ["navy", "black", "olive"], grey: ["black", "navy"],
  sage: ["navy", "black", "slate"], camel: ["navy", "black"], mustard: ["navy", "black", "slate"],
  black: ["beige", "grey", "white"], navy: ["beige", "white", "grey"], olive: ["beige", "white"],
  slate: ["beige", "white"], rust: ["beige", "white"], red: ["beige", "white", "grey"], cobalt: ["white", "beige", "grey"]
};
const JEANS = ["str-jean", "slim-jean"];
const KHAKIS = ["khakis", "slim-khakis"];
const LOOKS = [
  { tops: ["quarter-zip"], dark: ["str-jean", "slim-jean"], light: ["khakis", "slim-khakis"], shoes: ["low-snk", "chunky-snk"], lightShoes: ["white"], darkShoes: ["black"] },
  { tops: ["quarter-zip-waffle", "quarter-zip-fleece"], dark: ["str-pant", "cig-pant"], light: ["str-jean", "slim-khakis"], shoes: ["loafer", "chelsea"], lightShoes: "top", darkShoes: "top" },
  { tops: ["quarter-zip-cable"], dark: ["wide-pant", "cargo"], light: ["wide-pant", "khakis"], shoes: ["chelsea", "chunky-snk"], lightShoes: ["beige", "camel"], darkShoes: ["camel", "black"] }
];
const isLight = color => LIGHT.includes(color);

function fitsFormula(item, ctx) {
  const look = LOOKS[ctx.look === undefined ? 0 : ctx.look];
  const light = isLight(ctx.bread);
  if (item.slot === "top") return item.color === ctx.bread && (ctx.look === undefined ? item.id.startsWith("quarter-zip") : look.tops.includes(item.id));
  if (item.slot === "bottom") {
    const ids = ctx.look === undefined ? LOOKS.flatMap(l => light ? l.dark : l.light) : light ? look.dark : look.light;
    return ids.includes(item.id) && PAIRS[ctx.bread].includes(item.color);
  }
  if (item.slot === "shoes") {
    const ids = ctx.gym ? ["runner", "chunky-snk"] : ctx.look === undefined ? LOOKS.flatMap(l => l.shoes) : look.shoes;
    const colors = ctx.look === undefined ? [ctx.bread, ...(light ? ["white", "beige", "camel"] : ["black", "camel"])]
      : (light ? look.lightShoes : look.darkShoes) === "top" ? [ctx.bread] : light ? look.lightShoes : look.darkShoes;
    return ids.includes(item.id) && colors.includes(item.color);
  }
  return false;
}

''' + s[end:]

R('''function pool(slot, ctx) {
''', '''function pool(slot, ctx) {
  // These looks have no layer, so there's nothing to relax.
  if (slot === "layer") return [];
''')
R('''    bread: a.favorite || "navy",
    jeans: index % 2 === 0
  };''', '''    bread: a.favorite || "navy",
    look: index % LOOKS.length,
    gym: ctx_gym(a)
  };''')
R('''/* Simple contrast:''', '''const ctx_gym = a => a.occasions.includes("gym");

/* Simple contrast:''')
R('''    hero: null, tier: budgetTier(a), usedColors: new Set(), bread: a.favorite || "navy",''', '''    hero: null, tier: budgetTier(a), usedColors: new Set(), bread: a.favorite || "navy", look: outfit.look, gym: ctx_gym(a),''')
R('''  return {
    id: nextId++, silhouette, occasion: ctx.occasion, items,''', '''  return {
    id: nextId++, silhouette, occasion: ctx.occasion, items, look: ctx.look,''')
# Pants for a contrasting pick: make sure the light trousers can be light.
R('''  { id: "str-pant",   slot: "bottom", name: "straight trousers", fit: "regular", sil: EVEN, occ: ["work", "night"],''',
  '''  { id: "str-pant",   slot: "bottom", name: "straight trousers", fit: "regular", sil: EVEN, occ: ["work", "night", "casual", "weekend"],''')

# Plain-language explanation, no "sandwich".
start = s.index('  const bread = COLORS[top.color].label.toLowerCase();')
end = s.index('\n', s.index('return `This uses the sandwich method.'))
s = s[:start] + '''  const c = label => COLORS[label].label.toLowerCase();
  const pattern = isLight(top.color) ? "Light on top, dark in the middle, light at your feet." : "Dark on top, light in the middle, dark at your feet.";
  return `${pattern} The ${c(bottom.color)} ${bottom.name} make the ${c(top.color)} ${top.name} and ${c(shoes.color)} ${shoes.name} stand out. ${cap(c(bottom.color))} and ${c(top.color)} are an easy, classic pairing.`;''' + s[end:]
R('''${cap(COLORS[outfit.items.top.color].label.toLowerCase())} ${outfit.items.top.name} sandwich</h3>''', '''Look ${index + 1}: ${COLORS[outfit.items.top.color].label} ${outfit.items.top.name}</h3>''')
R('''<p class="eyebrow">Outfit ${index + 1} of ${outfits.length}</p>''', '''<p class="eyebrow">${isLight(outfit.items.top.color) ? "Light · dark · light" : "Dark · light · dark"}</p>''')
R('''Answer three taps and get three quarter-zip outfits, each styled with the sandwich method and a plain-language reason it was chosen for you.''',
  '''Answer three quick questions and get three quarter-zip outfits with easy, high-contrast color pairings.''')
R('''hint: "Your quarter zip and shoes will match it.",''', '''hint: "Your quarter zip will be this color.",''')
assert 'sandwich' not in s.lower().replace('sandwich-', ''), [m.start() for m in re.finditer('sandwich', s, re.I)]
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
