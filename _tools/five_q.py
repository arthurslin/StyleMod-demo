"""Five-question quiz: gender, age range, palette, style, accessory."""
import re
p = 'index.html'
s = open(p, encoding='utf-8').read()
def R(a, b, count=1):
    global s
    assert a in s, a
    s = s.replace(a, b, count)

# ---------- Colors
R('''  plum:    { label: "Plum",    hex: "#4d2147", family: "bold" }''', '''  plum:    { label: "Plum",    hex: "#4d2147", family: "bold" },
  ivory:   { label: "Ivory",   hex: "#efe8d6", family: "neutral" },
  lavender:{ label: "Lavender", hex: "#c4b5e3", family: "pastel" },
  powder:  { label: "Powder blue", hex: "#b5cde8", family: "pastel" },
  mint:    { label: "Mint",    hex: "#b9e0cb", family: "pastel" },
  blush:   { label: "Blush",   hex: "#efc3cc", family: "pastel" },
  butter:  { label: "Butter",  hex: "#f2e1a2", family: "pastel" },
  gold:    { label: "Gold",    hex: "#c9a33a", family: "neutral" },
  silver:  { label: "Silver",  hex: "#b9bec4", family: "neutral" }''')

# ---------- Recipes
start = s.index('const ctx_gym = a => a.occasions.includes("gym");')
end = s.index('/* Hard rules. Department comes only')
s = s[:start] + '''const ctx_gym = () => false;

/* Contrast: a light top gets dark pants, and a dark top gets light pants, in
   colors that pair well. Each style has three looks that set the cut, the shoes
   and an outer layer in the same color as the shoes. */
const LIGHT = ["white", "beige", "ivory", "grey", "sage", "camel", "mustard", "lavender", "powder", "mint", "blush", "butter"];
const PAIRS = {
  white: ["navy", "black", "olive"], beige: ["navy", "black", "olive"], ivory: ["navy", "black", "olive"], grey: ["black", "navy"],
  sage: ["navy", "black", "slate"], camel: ["navy", "black"], mustard: ["navy", "black", "slate"],
  black: ["beige", "grey", "white"], navy: ["beige", "white", "grey", "camel"], olive: ["beige", "white"],
  slate: ["beige", "white"], rust: ["beige", "white"], brown: ["beige", "white", "grey"],
  wine: ["beige", "grey", "white", "camel"], emerald: ["beige", "white", "grey"], plum: ["grey", "beige", "white"],
  red: ["beige", "white", "grey"], cobalt: ["white", "beige", "grey", "camel"],
  lavender: ["navy", "black", "slate"], powder: ["navy", "black", "slate"], mint: ["navy", "black", "olive"],
  blush: ["navy", "black", "slate"], butter: ["navy", "black", "olive"]
};
const JEANS = ["str-jean", "slim-jean"];
const KHAKIS = ["khakis", "slim-khakis"];
const isLight = color => LIGHT.includes(color);

const QUIZ_PALETTES = {
  bold:    { label: "Bold",    colors: ["wine", "cobalt", "emerald", "plum", "navy"] },
  neutral: { label: "Neutral", colors: ["black", "brown", "camel", "ivory", "grey"] },
  pastel:  { label: "Pastel",  colors: ["lavender", "powder", "mint", "blush", "butter"] }
};
const AGES = ["18–24", "25–34", "35–44", "45–54", "55+"];
const STYLE_OPTIONS = {
  classic:    { label: "Classic",    desc: "Tailored pieces and leather shoes" },
  athleisure: { label: "Athleisure", desc: "Sporty, comfortable and easy to move in" },
  minimalist: { label: "Minimalist", desc: "Clean lines and simple shapes" },
  streetwear: { label: "Streetwear", desc: "Relaxed cuts and chunky sneakers" },
  bohemian:   { label: "Bohemian",   desc: "Soft textures, wide legs and warm leather" }
};
const ACCESSORIES = {
  none:    { label: "None",    ids: [] },
  hat:     { label: "Hat",     ids: ["cap", "beanie"] },
  jewelry: { label: "Jewelry", ids: ["chain"] },
  bag:     { label: "Bag",     ids: ["crossbody", "tote"] },
  belt:    { label: "Belt",    ids: ["belt"] },
  watch:   { label: "Watch",   ids: ["watch"] }
};
/* Pants that come in every color, so a pairing is always possible. */
const ANY_CUT = ["str-pant", "wide-pant", "cargo", "track-pant"];
const look = (tops, dark, light, shoes, shoeColor, layers) => ({ tops, dark, light, shoes, shoeColor, layers });
const STYLE_LOOKS = {
  classic: [
    look(["quarter-zip"], ["str-pant", "cig-pant"], ["khakis", "str-pant"], ["loafer"], "brown", ["blazer", "trench"]),
    look(["quarter-zip-cable"], ["str-jean", "str-pant"], ["slim-khakis", "khakis"], ["chelsea"], "black", ["trench", "blazer"]),
    look(["quarter-zip-short"], ["cig-pant", "slim-jean"], ["slim-khakis", "str-pant"], ["low-snk"], "white", ["chore"])
  ],
  athleisure: [
    look(["quarter-zip-fleece"], ["tapered-jog", "track-pant"], ["track-pant", "tapered-jog"], ["runner"], "white", ["track-top"]),
    look(["quarter-zip-short"], ["track-pant"], ["track-pant"], ["chunky-snk"], "white", ["track-top"]),
    look(["quarter-zip"], ["tapered-jog"], ["tapered-jog"], ["runner"], "black", ["crop-puffer"])
  ],
  minimalist: [
    look(["quarter-zip"], ["cig-pant", "slim-jean"], ["str-pant", "slim-khakis"], ["low-snk"], "white", ["chore"]),
    look(["quarter-zip-short"], ["str-pant"], ["str-pant"], ["loafer"], "black", ["blazer"]),
    look(["quarter-zip-fleece"], ["slim-jean", "cig-pant"], ["str-pant"], ["chelsea"], "black", ["blazer"])
  ],
  streetwear: [
    look(["quarter-zip-waffle"], ["cargo", "wide-jean"], ["cargo", "parachute"], ["chunky-snk"], "white", ["crop-puffer"]),
    look(["quarter-zip-short-waffle"], ["parachute", "wide-jean"], ["cargo"], ["chunky-snk"], "black", ["crop-puffer"]),
    look(["quarter-zip"], ["wide-jean", "cargo"], ["wide-sweat", "cargo"], ["low-snk"], "white", ["track-top"])
  ],
  bohemian: [
    look(["quarter-zip-cable"], ["wide-pant"], ["wide-pant"], ["chelsea"], "brown", ["trench"]),
    look(["quarter-zip-waffle"], ["wide-pant", "cargo"], ["wide-pant"], ["loafer"], "brown", ["chore"]),
    look(["quarter-zip-short-waffle"], ["str-pant", "wide-pant"], ["wide-pant"], ["loafer"], "brown", ["chore"])
  ]
};

function fitsFormula(item, ctx) {
  const looks = STYLE_LOOKS[ctx.style] || STYLE_LOOKS.classic;
  const recipe = looks[ctx.look === undefined ? 0 : ctx.look];
  const all = ctx.look === undefined;
  const light = isLight(ctx.bread);
  const shoes = ctx.chosen && ctx.chosen.find(i => i.slot === "shoes");
  if (item.slot === "top") return item.color === ctx.bread && (all ? item.id.startsWith("quarter-zip") : recipe.tops.includes(item.id));
  if (item.slot === "bottom") {
    const ids = ctx.anyCut ? ANY_CUT : all ? looks.flatMap(l => light ? l.dark : l.light) : light ? recipe.dark : recipe.light;
    return ids.includes(item.id) && PAIRS[ctx.bread].includes(item.color);
  }
  if (item.slot === "shoes") {
    const ids = all ? looks.flatMap(l => l.shoes) : recipe.shoes;
    return ids.includes(item.id) && (all ? ["white", "brown", "black"].includes(item.color) : item.color === recipe.shoeColor);
  }
  if (item.slot === "layer") {
    // The outer layer repeats the shoe color, so the look is framed top to bottom.
    const ids = all ? looks.flatMap(l => l.layers) : recipe.layers;
    return !!shoes && ids.includes(item.id) && item.color === shoes.color;
  }
  if (item.slot === "accessory") {
    const pick = ACCESSORIES[ctx.accessory] || ACCESSORIES.none;
    if (!pick.ids.includes(item.id)) return false;
    if (item.id === "chain") return item.color === (ctx.style === "bohemian" ? "gold" : "silver");
    if (item.id === "watch") return item.color === (ctx.style === "bohemian" || ctx.style === "classic" ? "gold" : "silver");
    if (item.id === "cap") return ["athleisure", "streetwear"].includes(ctx.style) && !!shoes && item.color === shoes.color;
    if (item.id === "beanie") return !["athleisure", "streetwear"].includes(ctx.style) && !!shoes && item.color === shoes.color;
    return !!shoes && item.color === shoes.color;
  }
  return false;
}

''' + s[end:]

# Accessories get their own slot.
R('''const SLOTS = { top: "Top", bottom: "Bottom", shoes: "Shoes", layer: "Layer or accessory" };''', '''const SLOTS = { top: "Top", bottom: "Bottom", shoes: "Shoes", layer: "Outer layer", accessory: "Accessory" };''')
for sid in ('crossbody', 'tote', 'scarf', 'cap', 'beanie'):
    s, n = re.subn(r'(\{ id: "' + sid + r'",\s+slot: )"layer"', r'\1"accessory"', s)
    assert n == 1, sid
R('''  { id: "crossbody",''', '''  { id: "chain",      slot: "accessory", name: "chain necklace", fit: "regular", sil: EVEN, occ: ["casual", "work", "night", "athleisure", "gym", "weekend"], dept: BOTH, base: 45, colors: ["gold", "silver"], material: "recycled sterling silver or gold vermeil", tags: ["durable"] },
  { id: "belt",       slot: "accessory", name: "leather belt", fit: "regular", sil: EVEN, occ: ["casual", "work", "night", "athleisure", "gym", "weekend"], dept: BOTH, base: 50, colors: ["brown", "black", "white"], material: "full-grain leather", tags: ["durable"] },
  { id: "watch",      slot: "accessory", name: "minimal watch", fit: "regular", sil: EVEN, occ: ["casual", "work", "night", "athleisure", "gym", "weekend"], dept: BOTH, base: 120, colors: ["gold", "silver"], material: "stainless steel", tags: ["durable"] },
  { id: "crossbody",''')
R('''[...(style.slot === "shoes" || style.slot === "layer" ? ALL : style.colors), PHOTO_COLORS[style.id]]''',
  '''[...(["shoes", "layer"].includes(style.slot) || ["cap", "beanie", "crossbody", "tote"].includes(style.id) ? ALL : style.colors), PHOTO_COLORS[style.id]]''')
R('''  if (slot === "layer") return allowed;''', '''  if (slot === "layer" || slot === "accessory") return allowed;
  if (slot === "bottom" && !allowed.length && !ctx.anyCut) { ctx.anyCut = true; return pool(slot, ctx); }''')
R('''  layer:  { value: "Uniqlo, Gap, H&M",             mid: "Patagonia, Carhartt WIP, Coach",    premium: "Arc'teryx, Reiss, Longchamp" }''',
  '''  layer:  { value: "Uniqlo, Gap, H&M",             mid: "Patagonia, Carhartt WIP, Coach",    premium: "Arc'teryx, Reiss, Longchamp" },
  accessory: { value: "H&M, Mango, Fossil",         mid: "Coach, Madewell, Timex",            premium: "Mejuri, Tumi, Longines" }''')

# Outfit context.
R('''    look: index % LOOKS.length,
    pants: a.pants,''', '''    look: index % 3,
    style: a.style,
    accessory: a.accessory,''')
R('''bread: a.favorite || "navy", look: outfit.look, gym: ctx_gym(a), pants: a.pants,''', '''bread: a.favorite || "navy", look: outfit.look, gym: false, style: a.style, accessory: a.accessory,''')
R('''    id: nextId++, silhouette, occasion: ctx.occasion, items, look: ctx.look,''', '''    id: nextId++, silhouette, occasion: ctx.occasion, items, look: ctx.look, style: a.style,''')
# Age only nudges ties; it never removes options.
R('''  if (item.slot === "shoes" && REAL_SHOES[`${item.id}|${item.color}`]) total += 10;''', '''  if (item.slot === "shoes" && REAL_SHOES[`${item.id}|${item.color}`]) total += 10;
  if (a.age <= 1 && item.tags.includes("trend")) total += 1.5;
  if (a.age >= 3 && item.tags.includes("durable")) total += 1.5;''')

# Answers.
R('''  favorite: "", pants: "",''', '''  favorite: "", pants: "", age: 1, style: "classic", accessory: "none",''')

# ---------- Steps
R('const STEP_COUNT = 3;', 'const STEP_COUNT = 5;')
start = s.index('const STEP_VIEWS = {')
end = s.index('function budgetLabel() {')
s = s[:start] + '''const pick = (name, c) => `<label class="color-pick"><input type="radio" name="${name}" value="${c}" ${answers.favorite === c ? "checked" : ""}><span><i style="background:${COLORS[c].hex}" aria-hidden="true"></i>${COLORS[c].label}</span></label>`;
const STEP_VIEWS = {
  1: () => ({
    title: "Who are we dressing?",
    hint: "This sets the section and the dummy. We never infer it.",
    body: `<fieldset class="section"><legend class="sr">Gender</legend>
        <div class="opts">${Object.entries(DEPTS).map(([k, v]) => option("radio", "dept", k, v, "", answers.dept === k)).join("")}</div>
      </fieldset>`
  }),
  2: () => ({
    title: "What's your age range?",
    hint: "Only used to lean a little more trend-led or a little more classic. It never limits what you see.",
    body: `<div class="section">
        <p class="budget-value" id="ageValue">${AGES[answers.age]}</p>
        <input class="age-range" type="range" name="age" min="0" max="${AGES.length - 1}" step="1" value="${answers.age}" aria-label="Age range" aria-valuetext="${AGES[answers.age]}">
        <div class="range-ends"><span>${AGES[0]}</span><span>${AGES[AGES.length - 1]}</span></div>
      </div>`
  }),
  3: () => ({
    title: "Pick your palette",
    hint: "Choose a palette, then the shade for your quarter zip.",
    body: Object.entries(QUIZ_PALETTES).map(([k, pal]) => `<fieldset class="section palette-row"><legend>${pal.label}</legend>
        <div class="color-picks">${pal.colors.map(c => pick("favorite", c)).join("")}</div>
      </fieldset>`).join("")
  }),
  4: () => ({
    title: "What's your style?",
    hint: "Each style gets three looks of its own.",
    body: `<fieldset class="section"><legend class="sr">Style</legend>
        <div class="opts">${Object.entries(STYLE_OPTIONS).map(([k, v]) => option("radio", "style", k, v.label, v.desc, answers.style === k)).join("")}</div>
      </fieldset>`
  }),
  5: () => ({
    title: "Add an accessory?",
    hint: "It's matched to your shoes or your style.",
    body: `<fieldset class="section"><legend class="sr">Accessory</legend>
        <div class="opts three">${Object.entries(ACCESSORIES).map(([k, v]) => option("radio", "accessory", k, v.label, "", answers.accessory === k)).join("")}</div>
      </fieldset>`
  })
};

''' + s[end:]
R('''    <p class="eyebrow">Three quick questions</p>''', '''    <p class="eyebrow">Five quick questions</p>''')
R('''Answer three quick questions and get three quarter-zip outfits with easy, high-contrast color pairings.''', '''Answer five quick questions and get three quarter-zip outfits in your style, with easy color pairings.''')
R('''      <li><b>1</b> Pick a color</li>
      <li><b>2</b> Choose a section</li>
      <li><b>3</b> Pick an occasion</li>''', '''      <li><b>1</b> Gender</li>
      <li><b>2</b> Age range</li>
      <li><b>3</b> Color palette</li>
      <li><b>4</b> Style</li>
      <li><b>5</b> Accessory</li>''')
start = s.index('function describeAnswers() {')
end = s.index('function option(type, name, value, label, desc, checked')
s = s[:start] + '''function describeAnswers() {
  const a = answers;
  return [
    ["Shopping in", DEPTS[a.dept]],
    ["Age range", AGES[a.age]],
    ["Color", a.favorite ? COLORS[a.favorite].label : "Not picked yet"],
    ["Style", STYLE_OPTIONS[a.style].label],
    ["Accessory", ACCESSORIES[a.accessory].label]
  ];
}

''' + s[end:]

# Inputs.
R('''app.addEventListener("input", event => {
  const input = event.target;
  if (input.type !== "range") return;''', '''app.addEventListener("input", event => {
  const input = event.target;
  if (input.type !== "range") return;
  if (input.name === "age") {
    answers.age = Number(input.value);
    document.getElementById("ageValue").textContent = AGES[answers.age];
    input.setAttribute("aria-valuetext", AGES[answers.age]);
    return;
  }''')
R('''    if (view === 3 && !answers.occasions.length) answers.occasions = ["casual"];''', '''    if (view === 3 && !answers.favorite) { toast("Pick a color to continue."); return; }
    if (!answers.occasions.length) answers.occasions = ["casual"];''')
R('''    render(`[name="favorite"][value="${input.value}"]`);''', '')

# Results copy.
R('''        <p class="item-meta">${OCCASIONS[outfit.occasion]}</p>''', '''        <p class="item-meta">${(STYLE_OPTIONS[outfit.style] || STYLE_OPTIONS.classic).label} look</p>''')
R('''  if (a.occasions.length && outfit.items.top.occ.includes(outfit.occasion)) {
    parts.push(`Chosen with ${OCCASIONS[outfit.occasion].toLowerCase()} in mind.`);
  }''', '''  if (STYLE_OPTIONS[a.style]) parts.push(`Styled ${STYLE_OPTIONS[a.style].label.toLowerCase()}.`);''')
R('''  const coatLine = coat ? ` The ${c(coat.color)} ${coat.name} matches your ${shoes.name}, which ties the look together.` : "";''',
  '''  const coatLine = coat ? ` The ${c(coat.color)} ${coat.name} matches your ${shoes.name}, which ties the look together.` : "";
  const extra = outfit.items.accessory;
  const extraLine = extra ? ` A ${c(extra.color)} ${extra.name} finishes it.` : "";''')
R('''pairing.${coatLine}`;''', '''pairing.${coatLine}${extraLine}`;''')

R('''  .color-pick input:disabled + span {''', '''  .age-range { width: 100%; margin: 14px 0 6px; accent-color: var(--accent); }
  .palette-row legend { font-weight: 600; margin-bottom: 8px; }
  .color-pick input:disabled + span {''')

# ---------- Dummy: accessories, and real images for any slot.
R('''const REAL_SHOES = { "low-snk|white": "low-snk-white", "loafer|brown": "loafer-brown" };''',
  '''const REAL_SHOES = { "low-snk|white": "low-snk-white", "loafer|brown": "loafer-brown" };
/* Accessories photographed in their real color, drawn as-is. */
const REAL_ACCESSORIES = {};''')
R('''  const order = [shoes, bottom, top, layer].filter(Boolean);
  const real = item => item.slot === "shoes" && REAL_SHOES[`${item.id}|${item.color}`];''', '''  const extra = outfit.items.accessory;
  const realAcc = item => item.slot === "accessory" && REAL_ACCESSORIES[`${item.id}|${item.color}`];
  // Belts and watches sit under the sweater or are too small to read, so they show in the list only.
  const drawable = item => item.slot !== "accessory" || (WEAR[item.id] && !["belt", "watch"].includes(item.id)) || (item.id === "chain" && realAcc(item));
  const order = [shoes, bottom, top, layer, extra].filter(Boolean).filter(drawable);
  const real = item => (item.slot === "shoes" && REAL_SHOES[`${item.id}|${item.color}`]) || realAcc(item);''')
R('''...order.map(i => real(i) ? loadShoe(real(i)) : loadImage(WEAR[i.id][0]))''', '''...order.map(i => realAcc(i) ? loadShoe("../accessories/" + realAcc(i)) : real(i) ? loadShoe(real(i)) : loadImage(WEAR[i.id][0]))''')
R('''    } else if (item.slot === "shoes") {''', '''    } else if (item.id === "chain") {
      const width = m.chestW * .5;
      box = { x: MID - width / 2, y: m.neckY + CANVAS_H * .005, width, height: img.height * width / img.width };
    } else if (item.slot === "shoes") {''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
