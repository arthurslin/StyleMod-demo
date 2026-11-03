"""Royal (jewel-tone) main colors, and shoes in white, brown leather or black."""
p = 'index.html'
s = open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)

R('''  mustard: { label: "Mustard", hex: "#d7a11d", family: "bold" }''', '''  mustard: { label: "Mustard", hex: "#d7a11d", family: "bold" },
  wine:    { label: "Wine",    hex: "#6b1d2f", family: "bold" },
  emerald: { label: "Emerald", hex: "#0f5c46", family: "bold" },
  plum:    { label: "Plum",    hex: "#4d2147", family: "bold" }''')
R('''  slate: ["beige", "white"], rust: ["beige", "white"], brown: ["beige", "white", "grey"],''', '''  slate: ["beige", "white"], rust: ["beige", "white"], brown: ["beige", "white", "grey"],
  wine: ["beige", "grey", "white", "camel"], emerald: ["beige", "white", "grey"], plum: ["grey", "beige", "white"],''')
R('''  black: ["beige", "grey", "white"], navy: ["beige", "white", "grey"],''', '''  black: ["beige", "grey", "white"], navy: ["beige", "white", "grey", "camel"],''')
R('''cobalt: ["white", "beige", "grey"]''', '''cobalt: ["white", "beige", "grey", "camel"]''')
R('''const isLight = color => LIGHT.includes(color);''', '''const isLight = color => LIGHT.includes(color);
/* The quiz offers royal, jewel-tone colors for the quarter zip. */
const ROYAL = ["wine", "cobalt", "emerald", "plum", "navy"];
const PANTS_CHOICES = ["beige", "camel", "white", "grey", "black", "navy", "slate", "olive"];''')

# Shoes: white sneakers, brown leather, or black, sometimes chunky.
R('''    shoes: ["low-snk", "chunky-snk"], lightShoes: ["white"], darkShoes: ["black"] },''', '''    shoes: ["low-snk", "chunky-snk"], lightShoes: ["white"], darkShoes: ["white"] },''')
R('''    shoes: ["loafer", "chelsea"], lightShoes: ["beige", "grey"], darkShoes: ["brown", "black"] },''', '''    shoes: ["loafer", "chelsea"], lightShoes: ["brown"], darkShoes: ["brown"] },''')
R('''    shoes: ["chelsea", "chunky-snk"], lightShoes: ["white", "beige"], darkShoes: ["black", "brown"] }''', '''    shoes: ["chelsea", "chunky-snk", "loafer"], lightShoes: ["black"], darkShoes: ["black"] }''')
R('''    const colors = ctx.look === undefined ? (light ? ["white", "beige", "grey"] : ["black", "brown"]) : light ? look.lightShoes : look.darkShoes;''',
  '''    const colors = ctx.gym ? ["white", "black"] : ctx.look === undefined ? ["white", "brown", "black"] : light ? look.lightShoes : look.darkShoes;''')

# Step 1 offers the royal colors, and pants from a short neutral list.
R('''<div class="color-picks">${ALL.map(c => `<label class="color-pick"><input type="radio" name="favorite"''', '''<div class="color-picks">${ROYAL.map(c => `<label class="color-pick"><input type="radio" name="favorite"''')
R('''          ${ALL.filter(c => c !== answers.favorite).map(c => {''', '''          ${PANTS_CHOICES.filter(c => c !== answers.favorite).map(c => {''')
R('''hint: "First your quarter zip, then your pants.",''', '''hint: "Pick a royal color for your quarter zip, then a color for your pants.",''')

# Describe the actual tones, since white sneakers can follow a dark top.
R('''<p class="eyebrow">${isLight(outfit.items.top.color) ? "Light · dark · light" : "Dark · light · dark"}</p>''',
  '''<p class="eyebrow">${["top", "bottom", "shoes"].map(k => isLight(outfit.items[k].color) ? "Light" : "Dark").join(" · ")}</p>''')
R('''  const pattern = isLight(top.color) ? "Light on top, dark in the middle, light at your feet." : "Dark on top, light in the middle, dark at your feet.";''',
  '''  const tone = item => isLight(item.color) ? "light" : "dark";
  const pattern = `${cap(tone(top))} on top, ${tone(bottom)} in the middle, ${tone(shoes)} at your feet.`;''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
