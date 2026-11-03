"""File the captured garments, and replace the drawn dummy with canvas compositing of real garment images."""
import glob, os, re, shutil
from PIL import Image

TR = chr(92)*2 + '?' + chr(92) + os.path.normpath('C:/Users/assau/.claude/projects/C--Users-assau-AppData-Local-Claude-Data-claude-pzs8sxrjxfjjc-scratch-workspaces-8474f37f-6985-4bd0-95bb-6815984069ce-5469b8fd-b440-434a-8d03-7d8ef7a48bc6-scratch-2026-11-02-8ddb02/4f8ba79b-2c4f-4fb9-866f-a3d32b0037cf/tool-results')
MAP = dict(beanie='oq7kq4', cap='gazs84', scarf='rwy69m', tote='sswf7a', **{'crossbody-bag': 'jvy1bo', 'block-heels': 'x5nhxk', 'chelsea-boots': 'c63g7n',
  'loafers': '6ax5ko', 'runners': 'mwb8rs', 'chunky-sneakers': 'd1c7jj', 'puffer': 'rfy5df', 'trench': '9fr6g9', 'track-jacket': 'shn6hg', 'chore-jacket': 'n3oode',
  'power-blazer': 'dcahe1', 'maxi-skirt': 'xv0xag', 'midi-skirt': 'qvda8i', 'shorts': 's63be5', 'parachute-pants': '4hlzh9', 'cargo-pants': '6kuiff',
  'wide-sweatpants': 'cc9lr3', 'wide-jeans': '0m0r9b', 'flared-leggings': 'x6szpi', 'track-pants': 'zruzcp', 'joggers': 'xpfszm', 'straight-trousers': '6k9n9d',
  'straight-jeans': 'xl17s7', 'slim-jeans': 'aj28qy', 'chunky-knit': 'j702c9', 'polo': 'uu2unx', 'sweatshirt': 'iunndl', 'peplum': 'ycyzcx'})
for name, tag in MAP.items():
    hit = [os.path.join(TR,f) for f in os.listdir(TR) if f.endswith(f'-{tag}.jpg')]
    assert hit, name
    shutil.copy(hit[0], f'_gen/{name}.jpg')
# The merged image: keep the shirt, above its hem.
hit = [os.path.join(TR,f) for f in os.listdir(TR) if f.endswith('-w2df13.jpg')][0]
im = Image.open(hit).convert('RGB')
big = Image.new('RGB', im.size, 'white')
big.paste(im.crop((0, 0, im.width, 446)), (0, 0))
big.save('_gen/big-shirt.jpg', quality=92)
shutil.move('_gen/fitted-tee.jpg', '_gen/crop-tee.jpg')

p = 'index.html'
s = open(p, encoding='utf-8').read()
start = s.index('/* ==========================================================================\n   DRESSED DUMMY')
end = s.index('function renderPhotos(present, outfit) {')
CODE = r'''/* ==========================================================================
   DRESSED DUMMY (canvas)
   Layers garment images onto a mannequin and tints each one to the listed color.
   The form comes only from the section the customer chose. Body type is never used.
   Garments and mannequins are AI-generated images (Google Gemini), not photos of
   real stock.

   GEN AI PLUG-IN POINT: a virtual try-on model could replace this, given the same
   item data and form, with its output checked for accurate color.
   ========================================================================== */

/* size: mannequin width at the shoulders. cx: its center. Pixels at 900px tall. */
const FORMS = {
  menswear:   { size: 231, src: "dummy-menswear" },
  womenswear: { size: 193, src: "dummy-womenswear" },
  unisex:     { size: 200, src: "dummy-unisex" }
};
const CANVAS_W = 520, CANVAS_H = 900, MID = CANVAS_W / 2;

/* For each style: image, top edge as a share of height, width against the shoulders,
   and for bottoms a set height, so legs always reach the same place on the form. */
const WEAR = {
  "crop-tee": ["crop-tee", .137, 1.42], "rib-tee": ["tee", .137, 1.42], "rib-tank": ["tank", .145, .92], "train-tank": ["tank", .145, .92],
  "knit-polo": ["polo", .13, 1.5], "tech-tee": ["tee", .137, 1.42], "peplum": ["peplum", .137, 1.42], "crew-tee": ["tee", .137, 1.55],
  "oxford": ["shirt", .13, 1.62], "fine-knit": ["sweater", .137, 1.62], "camp-shirt": ["camp-shirt", .13, 1.62], "drape-top": ["blouse", .13, 1.6],
  "crinkle-shirt": ["crinkle-shirt", .13, 1.62], "over-tee": ["oversized-tee", .137, 1.95], "pump-cover": ["oversized-tee", .137, 1.95],
  "boxy-sweat": ["sweatshirt", .137, 1.85], "chunky-knit": ["chunky-knit", .137, 1.85], "big-shirt": ["big-shirt", .13, 1.8],
  "slim-chino": ["slim-jeans", .31, .84, .655], "slim-jean": ["slim-jeans", .31, .84, .655], "cig-pant": ["straight-trousers", .31, .84, .655],
  "tapered-jog": ["joggers", .31, .9, .655], "flare-legging": ["flared-leggings", .31, .92, .67], "str-jean": ["straight-jeans", .31, .92, .665],
  "str-pant": ["straight-trousers", .31, .92, .665], "track-pant": ["track-pants", .31, .92, .665], "midi-skirt": ["midi-skirt", .31, 1, .42],
  "maxi-skirt": ["maxi-skirt", .31, .92, .64], "wide-pant": ["wide-trousers", .31, 1.08, .675], "pleat-wide": ["wide-trousers", .31, 1.08, .675],
  "wide-jean": ["wide-jeans", .31, 1.08, .67], "wide-sweat": ["wide-sweatpants", .31, 1.08, .67], "cargo": ["cargo-pants", .31, 1, .67],
  "parachute": ["parachute-pants", .31, 1.12, .67], "gym-short": ["shorts", .31, 1.1, .3],
  "chunky-snk": ["chunky-sneakers", .925, .86], "low-snk": ["sneakers", .925, .8], "runner": ["runners", .925, .82], "loafer": ["loafers", .925, .8],
  "chelsea": ["chelsea-boots", .89, .8], "strap-heel": ["block-heels", .91, .76],
  "blazer": ["blazer", .125, 1.82], "power-blazer": ["power-blazer", .12, 1.98], "chore": ["chore-jacket", .125, 1.9], "track-top": ["track-jacket", .125, 1.85],
  "trench": ["trench", .12, 1.95], "crop-puffer": ["puffer", .12, 1.98],
  "crossbody": ["crossbody-bag", .42, .5, null, -.72], "tote": ["tote", .5, .72, null, 1.02], "scarf": ["scarf", .125, .44], "cap": ["cap", 0, .55], "beanie": ["beanie", 0, .46]
};

const imageCache = {};
function loadImage(name) {
  if (!imageCache[name]) {
    imageCache[name] = new Promise((resolve, reject) => {
      const img = new Image();
      img.onload = () => resolve(img);
      img.onerror = reject;
      img.src = `images/wear/${name}.webp`;
    });
  }
  return imageCache[name];
}

/* Multiply keeps the real folds and texture while landing on the exact color. */
function tinted(img, hex) {
  const c = document.createElement("canvas");
  c.width = img.width; c.height = img.height;
  const g = c.getContext("2d");
  g.drawImage(img, 0, 0);
  g.globalCompositeOperation = "multiply";
  g.fillStyle = hex;
  g.fillRect(0, 0, c.width, c.height);
  const value = parseInt(hex.slice(1), 16);
  if (((value >> 16) & 255) + ((value >> 8) & 255) + (value & 255) < 240) {
    g.globalCompositeOperation = "screen";
    g.globalAlpha = .16;
    g.drawImage(img, 0, 0);
    g.globalAlpha = 1;
  }
  g.globalCompositeOperation = "destination-in";
  g.drawImage(img, 0, 0);
  return c;
}

async function paintDummy(canvas, outfit) {
  const form = FORMS[activeAnswers().dept];
  const { top, bottom, shoes, layer } = outfit.items;
  const order = [shoes, bottom, top, layer].filter(Boolean);
  const [dummy, ...garments] = await Promise.all([form.src, ...order.map(i => WEAR[i.id][0])].map(loadImage));
  const g = canvas.getContext("2d");
  g.clearRect(0, 0, CANVAS_W, CANVAS_H);
  g.drawImage(dummy, MID - dummy.width / 2, 0);
  order.forEach((item, i) => {
    const [, topEdge, widthShare, heightShare, offset] = WEAR[item.id];
    const img = garments[i];
    const width = form.size * widthShare;
    const height = heightShare ? CANVAS_H * heightShare : img.height * width / img.width;
    const x = MID - width / 2 + (offset || 0) * form.size;
    g.drawImage(tinted(img, COLORS[item.color].hex), x, CANVAS_H * topEdge, width, height);
  });
}

function dummyLabel(outfit) {
  const list = Object.values(outfit.items).filter(Boolean).map(i => `${COLORS[i.color].label.toLowerCase()} ${i.name}`);
  return `${DEPTS[activeAnswers().dept]} dummy wearing ${names(list)}`;
}

'''
s = s[:start] + CODE + s[end:]
s = s.replace('''${drawDummy(outfit)}
          <figcaption>${DEPTS[a.dept]} form, in your colors and proportions</figcaption>''', '''<canvas class="dummy-view" data-outfit="${index}" width="${CANVAS_W}" height="${CANVAS_H}" role="img" aria-label="${dummyLabel(outfit)}"></canvas>
          <figcaption>${DEPTS[a.dept]} form, in your colors. AI-generated garment images.</figcaption>''')
assert 'dummy-view' in s
s = s.replace('.dummy svg { display: block; width: 100%; max-width: 250px; height: auto; margin: 0 auto; }', '.dummy-view { display: block; width: 100%; max-width: 300px; height: auto; margin: 0 auto; }')
a = '''  paintRange();
  const target = focusTarget'''
assert a in s
s = s.replace(a, '''  paintRange();
  app.querySelectorAll(".dummy-view").forEach(canvas => paintDummy(canvas, outfits[Number(canvas.dataset.outfit)]).catch(() => {}));
  const target = focusTarget''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('patched')
