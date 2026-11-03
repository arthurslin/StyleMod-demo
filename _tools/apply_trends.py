"""Swap in fixed photos, add trend-led styles, replace illustrations with photos, write credits.html."""
import io, json, re, urllib.request
from PIL import Image

UA = {'User-Agent': 'Mozilla/5.0 (StyleMod demo)'}
def get(url):
    with urllib.request.urlopen(urllib.request.Request(url, headers=UA), timeout=40) as r:
        return r.read()

def photo(pid, w=520, h=650):
    return f'https://images.unsplash.com/photo-{pid}?w={w}&h={h}&fit=crop&crop=entropy&fm=jpg&q=70'

credits = json.load(open('_tools/credits.json', encoding='utf-8'))
for sid, pid, slug in [
    ('parachute', '1686577670399-da59d48d5f70', 'a-man-with-tattoos-standing-on-a-wooden-platform-6SralrPEEEg'),
    ('gym-short', '1683848644075-82eb557b8623', 'a-woman-in-a-sports-bra-top-and-shorts-JFkKunpjiwA'),
]:
    open(f'images/{sid}.jpg', 'wb').write(get(photo(pid)))
    credits[sid]['page'] = f'https://unsplash.com/photos/{slug}'

# Crop to the garment: the sneakers without the logo bag, the tank above the waistband.
im = Image.open(io.BytesIO(get('https://images.unsplash.com/photo-1652370658121-cd0060db5fa9?w=1100&fm=jpg&q=80'))).convert('RGB')
W, H = im.size
im.crop((0, int(H * .62), W, H)).resize((520, int(520 * (H * .38) / W))).save('images/chunky-snk.jpg', quality=75)
im = Image.open(io.BytesIO(get('https://images.unsplash.com/photo-1714269083381-7c50384205ff?w=900&fm=jpg&q=80'))).convert('RGB')
W, H = im.size
top = int(H * .05); bottom = top + int(H * .55)
im.crop((int(W * .1), top, int(W * .9), bottom)).save('images/train-tank.jpg', quality=75)

p = 'index.html'
s = open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)

# --- data
s = re.sub(r' shape: "[a-z]+",\s*', ' ', s)
s = re.sub(r', detail: "[a-z]+"', '', s)
R('''  casual:     "Everyday casual",''', '''  casual:     "Everyday casual",''')
R('''  athleisure: "Athleisure",
''', '''  athleisure: "Athleisure",
  gym:        "Gym / training",
''')
R('''  trend:       { label: "Trend-forward",         desc: "Favor newer shapes and details" }
''', '''  trend:       { label: "Trend-forward",         desc: "Favor what's showing up on runways, streets and gym floors now" },
  kstyle:      { label: "Korean street style",   desc: "Favor Seoul-led shapes: wide legs, long hems and easy layers" }
''')
R('''budget: [100, 400], sustainable: false, durable: false, trend: false,''', '''budget: [100, 400], sustainable: false, durable: false, trend: false, kstyle: false,''')

new_tops = '''  { id: "train-tank", slot: "top", name: "second-skin training tank", fit: "slim", sil: SMALL_TOP, occ: ["gym", "athleisure"], dept: BOTH, base: 40, colors: ALL, material: "recycled nylon blend", tags: ["sustainable"] },
  { id: "peplum",     slot: "top", name: "peplum top", fit: "slim", sil: SMALL_TOP, occ: ["work", "night"], dept: W, base: 65, colors: ALL, material: "cotton poplin", tags: [] },
  { id: "crinkle-shirt", slot: "top", name: "crinkle-texture shirt", fit: "regular", sil: EVEN, occ: ["work", "weekend", "night"], dept: BOTH, base: 65, colors: ALL, material: "crinkled cotton", tags: [] },
  { id: "pump-cover", slot: "top", name: "boxy gym tee", fit: "relaxed", sil: BIG_TOP, occ: ["gym", "athleisure", "casual"], dept: BOTH, base: 40, colors: ALL, material: "heavyweight cotton", tags: ["durable"] },

  // Bottoms
'''
R('\n  // Bottoms\n', '\n' + new_tops)
new_bottoms = '''  { id: "flare-legging", slot: "bottom", name: "flared leggings", fit: "slim", sil: BIG_TOP, occ: ["gym", "athleisure"], dept: W, base: 65, colors: ["black", "grey", "navy", "slate", "olive", "rust"], material: "recycled nylon jersey", tags: ["sustainable"] },
  { id: "maxi-skirt", slot: "bottom", name: "long column skirt", fit: "regular", sil: EVEN, occ: ["casual", "night", "work"], dept: W, base: 70, colors: ALL, material: "crinkled viscose", tags: [] },
  { id: "pleat-wide", slot: "bottom", name: "pleated wide trousers", fit: "relaxed", sil: SMALL_TOP, occ: ["work", "night", "casual"], dept: BOTH, base: 85, colors: ALL, material: "fluid crepe", tags: [] },
  { id: "parachute",  slot: "bottom", name: "parachute pants", fit: "relaxed", sil: SMALL_TOP, occ: ["casual", "night", "weekend"], dept: BOTH, base: 75, colors: ALL, material: "recycled nylon", tags: ["sustainable"] },
  { id: "gym-short",  slot: "bottom", name: "loose training shorts", fit: "relaxed", sil: SMALL_TOP, occ: ["gym", "athleisure"], dept: BOTH, base: 40, colors: ["black", "grey", "navy", "slate", "olive", "red", "cobalt"], material: "recycled polyester", tags: ["sustainable"] },

  // Shoes
'''
R('\n  // Shoes\n', '\n' + new_bottoms)
new_layers = '''  { id: "power-blazer", slot: "layer", name: "strong-shoulder blazer", fit: "regular", sil: EVEN, occ: ["work", "night"], dept: BOTH, base: 140, colors: LAYER_COLORS, material: "wool blend", tags: ["durable"] },
  { id: "trench",     slot: "layer", name: "slouchy trench coat", fit: "regular", sil: EVEN, occ: ["work", "casual", "weekend"], dept: BOTH, base: 150, colors: ["beige", "camel", "black", "olive", "navy"], material: "cotton gabardine", tags: ["durable"] },
  { id: "crop-puffer", slot: "layer", name: "cropped puffer jacket", fit: "regular", sil: EVEN, occ: ["casual", "weekend"], dept: BOTH, base: 110, colors: LAYER_COLORS, material: "recycled down", tags: ["sustainable"] },
  { id: "tote",       slot: "layer", name: "slouchy tote bag", fit: "regular", sil: EVEN, occ: ["casual", "work", "weekend"], dept: BOTH, base: 55, colors: LAYER_COLORS, material: "organic cotton canvas", tags: ["sustainable"] },
  { id: "beanie",     slot: "layer", name: "ribbed beanie", fit: "regular", sil: EVEN, occ: ["casual", "weekend"], dept: BOTH, base: 25, colors: LAYER_COLORS, material: "recycled wool", tags: ["sustainable"] },
'''
R('  { id: "crossbody",', new_layers + '  { id: "crossbody",')

# Existing pieces that belong on the gym floor.
for sid in ('tech-tee', 'rib-tank', 'boxy-sweat', 'over-tee', 'wide-sweat', 'tapered-jog', 'track-pant', 'runner', 'cap', 'track-top', 'chunky-snk'):
    m = re.search(r'id: "' + sid + r'".*?occ: \[', s)
    assert m, sid
    s = s[:m.end()] + '"gym", ' + s[m.end():]

trends = '''/* What's showing up now, as of November 2026. GEN AI PLUG-IN POINT: a real system
   would refresh this from a maintained trend feed, reviewed by a merchandiser.
   k marks pieces tied to Korean street style. */
const TRENDS = {
  "wide-pant":     { k: true, note: "Wide legs are the defining K-fashion shape this year" },
  "pleat-wide":    { k: true, note: "Structured, pleated wide trousers are a Korean staple right now" },
  "parachute":     { k: true, note: "Relaxed parachute pants are a Musinsa favorite" },
  "wide-jean":     { k: true, note: "Wide denim is a Seoul street staple" },
  "cargo":         { k: true, note: "Cargos remain a key shape on Korean platforms" },
  "trench":        { k: true, note: "Trench coats stood out at Seoul Fashion Week SS27, and models wear them slouchy off duty" },
  "power-blazer":  { k: true, note: "Strong shoulders kept returning at Seoul Fashion Week SS27" },
  "maxi-skirt":    { k: true, note: "Long hems were a repeat detail at Seoul Fashion Week SS27" },
  "crinkle-shirt": { k: true, note: "Crinkled fabric was a repeat detail at Seoul Fashion Week SS27" },
  "crop-puffer":   { k: true, note: "Shorter outerwear is a focus on Korean platforms" },
  "beanie":        { k: true, note: "Beanies are a steady best-seller category in K-fashion" },
  "tote":          { k: true, note: "Large, slouchy bags showed up at Seoul Fashion Week SS27" },
  "peplum":        { note: "Peplum was the headline shape of the SS27 runways" },
  "blazer":        { note: "A generous blazer is a core part of the model off-duty uniform" },
  "crew-tee":      { note: "A clean white tee anchors the model off-duty formula" },
  "str-jean":      { note: "Relaxed denim is the other half of the model off-duty formula" },
  "over-tee":      { note: "Baggy tops over fitted bottoms are the current gym-floor look" },
  "pump-cover":    { note: "Boxy tees over fitted pieces are the current gym-floor look" },
  "boxy-sweat":    { note: "Oversized sweatshirts over fitted pieces are all over gyms now" },
  "train-tank":    { note: "Second-skin tanks pair with baggy layers on the gym floor" },
  "wide-sweat":    { note: "Baggy sweatpants with a fitted top lead current gym style" },
  "flare-legging": { note: "Flares are taking over from skinny gym leggings" },
  "gym-short":     { note: "Many younger gym-goers are swapping leggings for bigger shorts" }
};

/* One record per style + color + price tier. */'''
R('/* One record per style + color + price tier. */', trends)
R('''  tags: tier === "premium" ? [...new Set([...style.tags, "durable"])] : style.tags
}))));''', '''  photo: `images/${style.id}.jpg`,
  trendNote: TRENDS[style.id] ? TRENDS[style.id].note : "",
  korean: !!(TRENDS[style.id] && TRENDS[style.id].k),
  tags: [...new Set([
    ...style.tags,
    ...(tier === "premium" ? ["durable"] : []),
    ...(TRENDS[style.id] ? ["trend"] : []),
    ...(TRENDS[style.id] && TRENDS[style.id].k ? ["kstyle"] : [])
  ])]
}))));''')
R('''const BY_KEY = new Map''', '''/* Style groups get their own illustrative brands. Same caveats as BRANDS. */
const BRANDS_KOREAN = { value: "Musinsa Standard, 8Seconds, Spao", mid: "Covernat, thisisneverthat, Mardi Mercredi", premium: "Andersson Bell, Ader Error, Wooyoungmi" };
const BRANDS_GYM = { value: "Old Navy, Decathlon, Uniqlo", mid: "Gymshark, Nike, Under Armour", premium: "Lululemon, Alo Yoga, Rhone" };
const brandsFor = item => item.korean ? BRANDS_KOREAN : item.occ[0] === "gym" && item.slot !== "shoes" ? BRANDS_GYM : BRANDS[item.slot];

const BY_KEY = new Map''')
R('''<span>${BRANDS[slot][tier]}</span>''', '''<span>${brandsFor(item)[tier]}</span>''')

# --- engine + copy
R('''  if (item.id === "chunky-snk" && ctx.silhouette === "small-top") total += 2;
''', '''  if (item.id === "chunky-snk" && ctx.silhouette === "small-top") total += 2;
  if (a.trend && item.color === "cobalt") total += 1;
''')
R('''    if (pref === "trend") parts.push(`For trend-forward: the ${match.name} brings in a newer shape.`);
''', '''    if (pref === "trend") parts.push(`For trend-forward: the ${match.name}. ${match.trendNote || "It brings in a newer shape"}.`);
    if (pref === "kstyle") parts.push(`For Korean street style: the ${match.name}. ${match.trendNote || "It suits the Seoul look"}.`);
''')
R('''  return [proportionText(outfit), colorText(outfit, a), detailsText(outfit, a)];
''', '''  const onTrend = Object.values(outfit.items).find(i => i && i.trendNote);
  const trendLine = onTrend && !a.trend && !a.kstyle ? ` On trend: ${onTrend.trendNote.charAt(0).toLowerCase()}${onTrend.trendNote.slice(1)}.` : "";
  return [proportionText(outfit), colorText(outfit, a), detailsText(outfit, a) + trendLine];
''')

# --- photos replace the illustrations
start = s.index('/* ==========================================================================\n   FLAT ILLUSTRATIONS')
end = s.index('/* ==========================================================================\n   VIEWS')
s = s[:start] + '''function renderPhotos(present, outfit) {
  return present.map(slot => {
    const item = outfit.items[slot];
    return `<figure class="tile">
      <img src="${item.photo}" alt="Example photo of a ${item.name}" loading="lazy" width="520" height="650">
      <figcaption><i style="background:${COLORS[item.color].hex}" aria-hidden="true"></i>${COLORS[item.color].label}</figcaption>
    </figure>`;
  }).join("");
}

''' + s[end:]
R('''<div class="lay">${drawOutfit(outfit)}</div>''', '''<div class="lay">${renderPhotos(present, outfit)}</div>
        <p class="fine">Real photos show the style. Your color is marked on each one.</p>''')
R('''  .lay { background: var(--lay); border-radius: var(--radius); padding: 10px; }
  .lay svg { display: block; width: 100%; max-width: 330px; height: auto; margin: 0 auto; }
''', '''  .lay { display: grid; grid-template-columns: 1fr 1fr; gap: 8px; }
  .tile { position: relative; margin: 0; border-radius: var(--radius); overflow: hidden; background: var(--sunken); }
  .tile img { display: block; width: 100%; height: auto; aspect-ratio: 4 / 5; object-fit: cover; }
  .tile figcaption { position: absolute; left: 6px; bottom: 6px; display: inline-flex; align-items: center; gap: 5px; padding: 3px 8px 3px 4px; border-radius: 999px; background: var(--surface); color: var(--ink); font-size: .78rem; }
  .tile figcaption i { width: 14px; height: 14px; border-radius: 50%; border: 1px solid var(--swatch-line); }
  .trends ul { margin: 8px 0 0; padding-left: 20px; }
  .trends li + li { margin-top: 6px; }
''')
R('''  --lay: #eae5d9;
''', '') if False else None
R('''    ${saved.length ? `<section class="saved"''', '''    <details class="panel trends" style="margin-top:24px">
      <summary>What's shaping these picks</summary>
      <ul>
        <li><strong>Seoul:</strong> trench coats, cobalt, strong shoulders, long hems, crinkled fabric and wide, relaxed legs (<a href="https://koreaherald.com/article/10860284">Korea Herald</a>, <a href="https://fashionunited.uk/news/fashion/seoul-fashion-week-ss27-trends-from-re-rhee-lie-sang-bong-and-more/2026091590294">FashionUnited</a>).</li>
        <li><strong>Runways:</strong> peplum, softer tailoring and statement skirts, with blue as a lead color (<a href="https://fashionunited.uk/news/fashion/spotted-on-the-catwalk-the-wgsn-spring-summer-2027-colours/2025101484366">WGSN via FashionUnited</a>).</li>
        <li><strong>Models off duty:</strong> a slouchy trench or generous blazer over a white tee and relaxed denim, in neutral tones (<a href="https://www.runwaylive.com/model-off-duty-style-is-driving-global-fashion-trends.html">Runway Magazine</a>).</li>
        <li><strong>Gym influencers:</strong> baggy tops and sweats over fitted pieces, bigger shorts, flared leggings, and mixed rather than matching sets (<a href="https://www.whowhatwear.com/fashion/trends/activewear-trends-2026">Who What Wear</a>, <a href="https://www.bahrain-confidential.com/oversized-gym-shirts-summer-style/">Bahrain Confidential</a>).</li>
      </ul>
      <p class="fine">Read as of November 2026 from editorial and retail coverage, not sales data. It shapes which pieces are in the catalog. It only ranks your results if you turn on Trend-forward or Korean street style.</p>
    </details>
    ${saved.length ? `<section class="saved"''')
R('''Brand names are illustrative mock data, with no affiliation or endorsement.</p>''', '''Brand names are illustrative mock data, with no affiliation or endorsement. Photos are style examples from Unsplash, not the listed products, and the people in them don't endorse StyleMod. <a href="credits.html">Photo credits</a>.</p>''')
R('''  .site-foot { border-top''', '''  a { color: var(--accent); }
  .site-foot { border-top''')
open(p, 'w', encoding='utf-8', newline='').write(s)

rows = ''.join(f'<li><a href="{v["page"]}">{k.replace("-", " ")}</a></li>' for k, v in sorted(credits.items()))
open('credits.html', 'w', encoding='utf-8').write(f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>StyleMod Photo Credits</title>
<style>
:root {{ color-scheme: light dark; --bg:#f4f1ea; --ink:#2a3429; --link:#3f5a3c; }}
@media (prefers-color-scheme: dark) {{ :root {{ --bg:#171c16; --ink:#f4f1ea; --link:#b4c79a; }} }}
body {{ margin:0 auto; max-width:680px; padding:28px 16px; background:var(--bg); color:var(--ink); font:1rem/1.6 system-ui,sans-serif; }}
a {{ color:var(--link); }} ul {{ columns:2; padding-left:20px; }} h1 {{ font:500 2rem Georgia,serif; }}
</style></head><body>
<h1>Photo credits</h1>
<p>All style photos are from <a href="https://unsplash.com">Unsplash</a> under the <a href="https://unsplash.com/license">Unsplash License</a>, and each link goes to the photo and its photographer. They are style examples, not the mock products, and the people shown don't endorse StyleMod.</p>
<ul>{rows}</ul>
<p><a href="index.html">Back to StyleMod</a></p>
</body></html>
''')
print('ok', len(credits))
