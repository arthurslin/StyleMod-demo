"""Rework outfits around stylist fundamentals: three distinct shapes per style,
curated color stories per knit color, and new trend pieces."""
p = 'index.html'
s = open(p, encoding='utf-8').read()
start = s.index('/* Pants that come in every color, so a pairing is always possible. */')
end = s.index('  if (item.slot === "accessory") {')
NEW = r'''/* Pants that come in every color, so a pairing is always possible. */
const ANY_CUT = ["str-pant", "wide-pant", "cargo", "track-pant"];

/* Proportion, per stylists: put volume in one place. Each style has three shapes,
   so the three outfits never share a silhouette:
   - solo: the knit on its own as the hero piece, a tee hem at the waist;
   - short: a waist or hip-length jacket over a fuller leg (about a third over two thirds);
   - long: a knee-length coat over a straighter, narrower leg.
   On womenswear, `skirt` replaces the pants where a skirt suits the look. */
const look = (shape, tops, pants, shoes, layers, inspo = "", skirt = null) => ({ shape, tops, pants, shoes, layers, inspo, skirt });
const STYLE_LOOKS = {
  classic: [
    look("solo", ["quarter-zip"], ["str-pant", "khakis"], ["loafer"], [], "The Manual's knit-and-tailored-trousers formula", ["midi-skirt"]),
    look("short", ["quarter-zip-cable"], ["str-jean", "wide-pant"], ["chelsea"], ["barn"], "fall 2026's barn jacket over a chunky knit"),
    look("long", ["quarter-zip"], ["cig-pant", "str-pant"], ["loafer"], ["overcoat", "trench"], "a roomy raglan coat over slim tailoring")
  ],
  athleisure: [
    look("solo", ["quarter-zip-fleece"], ["wide-sweat", "track-pant"], ["runner"], [], "track pants worn as a real outfit"),
    look("short", ["quarter-zip-short"], ["track-pant", "wide-sweat"], ["chunky-snk"], ["crop-puffer", "shell"], "Musinsa's short outerwear"),
    look("long", ["quarter-zip"], ["tapered-jog", "track-pant"], ["runner"], ["overcoat"], "a wool coat over track pants and runners")
  ],
  minimalist: [
    look("solo", ["quarter-zip"], ["wide-pant", "pleat-wide"], ["low-snk", "loafer"], [], "one clean knit over one clean wide leg", ["midi-skirt"]),
    look("short", ["quarter-zip-short"], ["wide-pant", "extra-wide-jean"], ["loafer"], ["moto", "suede"], "a cropped jacket over a wide leg"),
    look("long", ["quarter-zip-cable"], ["cig-pant", "slim-jean"], ["chelsea"], ["overcoat"], "a long coat over a narrow trouser")
  ],
  streetwear: [
    look("solo", ["quarter-zip-waffle"], ["extra-wide-jean", "cargo"], ["chunky-snk"], [], "Musinsa's extra-wide denim"),
    look("short", ["quarter-zip-short-waffle"], ["cargo", "parachute"], ["chunky-snk"], ["crop-puffer", "moto"], "a short puffer over baggy cargos"),
    look("long", ["quarter-zip"], ["stacked-jean", "str-jean"], ["low-snk"], ["overcoat"], "Fashion Nova's stacked denim under a long coat")
  ],
  bohemian: [
    look("solo", ["quarter-zip-cable"], ["wide-pant", "pleat-wide"], ["chelsea"], [], "a chunky knit over fluid wide trousers", ["maxi-skirt"]),
    look("short", ["quarter-zip-waffle"], ["wide-pant", "pleat-wide"], ["loafer"], ["suede"], "chocolate suede, fall 2026's key jacket"),
    look("long", ["quarter-zip-cable"], ["str-pant", "str-jean"], ["chelsea"], ["trench", "overcoat"], "a slouchy trench with the belt left loose", ["midi-skirt"])
  ]
};

/* Color, per stylists: the chosen color plus two neutrals, never more than three.
   Each knit color has a curated list of pants and outer-layer colors, best first:
   brown worn as a neutral, camel and grey coats over strong colors, navy and
   indigo under pastels (Opumo, Mr Porter, Who What Wear, fall 2026). */
const STORIES = {
  wine:     { pants: ["grey", "ivory", "navy", "beige"],  outer: ["camel", "grey", "brown", "black"] },
  cobalt:   { pants: ["grey", "ivory", "beige", "brown"], outer: ["camel", "grey", "brown", "black"] },
  emerald:  { pants: ["ivory", "beige", "grey", "navy"],  outer: ["camel", "brown", "black", "navy"] },
  plum:     { pants: ["grey", "ivory", "beige", "black"], outer: ["camel", "grey", "black"] },
  navy:     { pants: ["beige", "ivory", "grey", "camel"], outer: ["camel", "brown", "olive", "grey"] },
  black:    { pants: ["grey", "ivory", "beige", "black"], outer: ["camel", "grey", "brown", "black"] },
  brown:    { pants: ["ivory", "beige", "navy", "grey"],  outer: ["camel", "navy", "black", "olive"] },
  camel:    { pants: ["navy", "ivory", "brown", "black"], outer: ["brown", "navy", "black", "olive"] },
  ivory:    { pants: ["brown", "navy", "black", "grey"],  outer: ["camel", "brown", "navy", "black"] },
  grey:     { pants: ["black", "navy", "ivory"],          outer: ["camel", "navy", "black", "brown"] },
  lavender: { pants: ["grey", "navy", "ivory"],           outer: ["grey", "navy", "black", "camel"] },
  powder:   { pants: ["navy", "grey", "beige"],           outer: ["camel", "navy", "brown"] },
  mint:     { pants: ["navy", "ivory", "grey"],           outer: ["navy", "black", "camel"] },
  blush:    { pants: ["grey", "navy", "ivory", "black"],  outer: ["camel", "grey", "black"] },
  butter:   { pants: ["navy", "brown", "grey", "ivory"],  outer: ["brown", "navy", "camel"] }
};
const storyFor = color => STORIES[color] || { pants: PAIRS[color] || ["navy", "beige"], outer: ["camel", "black", "navy"] };
const JEAN_IDS = ["str-jean", "slim-jean", "wide-jean"];
/* Denim comes in fewer colors: ecru (white) denim stands in for ivory and beige. */
const storyRank = (list, item) => {
  const at = list.indexOf(item.color);
  if (at >= 0) return at;
  return item.color === "white" && JEAN_IDS.includes(item.id) ? Math.max(list.indexOf("ivory"), list.indexOf("beige")) : -1;
};
const lumGap = (x, y) => Math.abs(luminance(x) - luminance(y));
function recipeFor(ctx) {
  const looks = STYLE_LOOKS[ctx.style] || STYLE_LOOKS.classic;
  return looks[ctx.look === undefined ? 0 : ctx.look];
}
const bottomIds = (recipe, ctx) => ctx.a.dept === "womenswear" && recipe.skirt ? recipe.skirt : recipe.pants;

function luminance(color) {
  const v = parseInt(COLORS[color].hex.slice(1), 16);
  const lin = c => { c /= 255; return c <= .03928 ? c / 12.92 : ((c + .055) / 1.055) ** 2.4; };
  return .2126 * lin((v >> 16) & 255) + .7152 * lin((v >> 8) & 255) + .0722 * lin(v & 255);
}

/* Layering, per Mr Porter, Marie Claire and Who What Wear: an outer layer sits at a
   clearly different depth from the knit, and the outfit always has one light and one
   dark piece, so it never reads as one flat block. */
function outerFits(top, bottom, color) {
  if (color === top || color === bottom) return false;
  if (lumGap(color, top) < .1) return false;
  return !(isLight(top) === isLight(bottom) && isLight(bottom) === isLight(color));
}

/* Shoes: leather goes brown with warm colors and black with cool or black ones;
   sneakers echo the knit, white under light knits and black under dark ones. */
const LEATHER = ["loafer", "chelsea"];
function shoeColor(id, top, bottom) {
  if (LEATHER.includes(id)) return [top, bottom].includes("black") || ["grey", "plum", "lavender", "blush"].includes(top) ? "black" : "brown";
  return isLight(top) ? "white" : "black";
}

function fitsFormula(item, ctx) {
  const looks = STYLE_LOOKS[ctx.style] || STYLE_LOOKS.classic;
  const recipe = recipeFor(ctx);
  const all = ctx.look === undefined;
  const story = storyFor(ctx.bread);
  const topPick = ctx.chosen && ctx.chosen.find(i => i.slot === "top");
  const bottomPick = ctx.chosen && ctx.chosen.find(i => i.slot === "bottom");
  const shoes = ctx.chosen && ctx.chosen.find(i => i.slot === "shoes");
  if (item.slot === "top") return item.color === ctx.bread && (all ? item.id.startsWith("quarter-zip") : recipe.tops.includes(item.id));
  if (item.slot === "bottom") {
    const ids = ctx.anyCut ? ANY_CUT : all ? looks.flatMap(l => bottomIds(l, ctx)) : bottomIds(recipe, ctx);
    if (!ids.includes(item.id) || storyRank(story.pants, item) < 0) return false;
    // With no outer layer, the pants alone carry the contrast against the knit.
    if (!all && recipe.shape === "solo" && (isLight(item.color) === isLight(ctx.bread) || lumGap(item.color, ctx.bread) < .1)) return false;
    // The pants never repeat the shoe color, so the leg stands apart from the foot.
    return all || ctx.anyCut || recipe.shoes.some(id => shoeColor(id, ctx.bread, item.color) !== item.color);
  }
  if (item.slot === "shoes") {
    const ids = all ? looks.flatMap(l => l.shoes) : recipe.shoes;
    if (!ids.includes(item.id)) return false;
    if (all) return ["white", "brown", "black"].includes(item.color);
    return item.color === shoeColor(item.id, ctx.bread, bottomPick && bottomPick.color) && !(bottomPick && bottomPick.color === item.color);
  }
  if (item.slot === "layer") {
    const ids = all ? looks.flatMap(l => l.layers) : recipe.layers;
    if (!ids.includes(item.id) || !topPick || !shoes) return false;
    return story.outer.includes(item.color) && outerFits(topPick.color, bottomPick && bottomPick.color, item.color);
  }
'''
s = s[:start] + NEW + s[end:]

# Rank colors by the story, best first, so the stylist's first choice usually wins.
old = "  if (item.photo) total += 3;\n"
assert old in s
s = s.replace(old, old + '''  if (item.slot === "bottom" || item.slot === "layer") {
    const story = storyFor(ctx.bread);
    const at = storyRank(item.slot === "bottom" ? story.pants : story.outer, item);
    if (at >= 0) total += 3 - at;
  }
''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
