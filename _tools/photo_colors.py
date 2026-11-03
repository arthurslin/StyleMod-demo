p = 'index.html'
s = open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)

R('/* One record per style + color + price tier. */', '''/* The color each style photo actually shows, tagged by eye. A photo appears only
   on a piece in this color, so what's pictured always matches what's listed. */
const PHOTO_COLORS = {
  "crop-tee": "rust", "rib-tee": "white", "rib-tank": "white", "train-tank": "white", "knit-polo": "grey", "tech-tee": "white",
  "peplum": "white", "crew-tee": "white", "oxford": "sage", "fine-knit": "beige", "camp-shirt": "slate", "drape-top": "white",
  "crinkle-shirt": "white", "over-tee": "slate", "pump-cover": "black", "boxy-sweat": "grey", "chunky-knit": "beige", "big-shirt": "white",
  "slim-chino": "black", "slim-jean": "navy", "cig-pant": "black", "tapered-jog": "beige", "flare-legging": "black", "str-jean": "slate",
  "str-pant": "red", "track-pant": "camel", "midi-skirt": "rust", "maxi-skirt": "beige", "wide-pant": "olive", "pleat-wide": "olive",
  "cargo": "olive", "parachute": "camel", "wide-jean": "slate", "wide-sweat": "grey", "gym-short": "grey", "chunky-snk": "beige",
  "low-snk": "white", "runner": "white", "loafer": "black", "chelsea": "camel", "strap-heel": "beige", "blazer": "black",
  "power-blazer": "black", "chore": "camel", "track-top": "cobalt", "trench": "beige", "crop-puffer": "black", "crossbody": "black",
  "tote": "beige", "scarf": "rust", "cap": "white", "beanie": "olive"
};

/* One record per style + color + price tier. */''')
R('''const CATALOG = STYLES.flatMap(style => style.colors.flatMap(color =>''', '''const CATALOG = STYLES.flatMap(style => [...new Set([...style.colors, PHOTO_COLORS[style.id]])].flatMap(color =>''')
R('''  photo: `images/${style.id}.jpg`,
''', '''  photo: color === PHOTO_COLORS[style.id] ? `images/${style.id}.jpg` : "",
''')
R('''  if (a.trend && item.color === "cobalt") total += 1;
''', '''  if (a.trend && item.color === "cobalt") total += 1;
  if (item.photo) total += 3;
''')
R('''  return present.map(slot => {
    const item = outfit.items[slot];
    return `<figure class="tile">''', '''  return present.filter(slot => outfit.items[slot].photo).map(slot => {
    const item = outfit.items[slot];
    return `<figure class="tile">''')
R('''Yours: ${COLORS[item.color].label}</figcaption>''', '''${COLORS[item.color].label} ${item.name}</figcaption>''')
R('''<p class="fine">Photos show the style, which may be in a different color. Your color is marked on each one.</p>''', '''<p class="fine">Photos appear only for pieces shown in the listed color. The dummy shows every piece.</p>''')
R('''  .tile figcaption { position: absolute; left: 6px; bottom: 6px; display: inline-flex;''', '''  .tile figcaption { position: absolute; left: 6px; right: 6px; bottom: 6px; line-height: 1.25; display: flex; width: fit-content;''')
R('''padding: 3px 8px 3px 4px; border-radius: 999px;''', '''padding: 3px 8px 3px 4px; border-radius: 10px;''')
R('''  .tile figcaption i { width: 14px;''', '''  .tile figcaption i { flex: none; width: 14px;''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
