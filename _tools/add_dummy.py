p = 'index.html'
s = open(p, encoding='utf-8').read()
def R(a, b):
    global s
    assert a in s, a
    s = s.replace(a, b)

CODE = r'''/* ==========================================================================
   DRESSED DUMMY (inline SVG)
   Shows each outfit's real proportions in the customer's actual colors. The form
   comes only from the section they chose. Body type is never used here.

   GEN AI PLUG-IN POINT: an image model or 3D try-on service could replace this,
   given the same item data and form, with its output checked for accurate color.
   ========================================================================== */

const FORMS = {
  menswear:   { sh: 60, chest: 47, waist: 38, hip: 41, neck: 15 },
  womenswear: { sh: 47, chest: 41, waist: 28, hip: 46, neck: 12 },
  unisex:     { sh: 53, chest: 44, waist: 33, hip: 43, neck: 13 }
};
const MX = 150, RISE = 196, FORM_FILL = "#bdb3a1", FORM_LINE = "#94897a";

const GARMENTS = {
  "crop-tee": "crop", "rib-tee": "tee", "rib-tank": "tank", "train-tank": "tank", "knit-polo": "tee", "tech-tee": "tee",
  "peplum": "peplum", "crew-tee": "regtee", "oxford": "shirt", "fine-knit": "knit", "camp-shirt": "regtee", "drape-top": "shirt",
  "crinkle-shirt": "shirt", "over-tee": "overtee", "pump-cover": "overtee", "boxy-sweat": "sweat", "chunky-knit": "sweat", "big-shirt": "bigshirt",
  "slim-chino": "slim", "slim-jean": "slim", "cig-pant": "slim", "tapered-jog": "slim", "flare-legging": "flare",
  "str-jean": "straight", "str-pant": "straight", "track-pant": "straight", "midi-skirt": "midi", "maxi-skirt": "maxi",
  "wide-pant": "wide", "pleat-wide": "wide", "wide-jean": "wide", "wide-sweat": "wide", "cargo": "cargo", "parachute": "cargo", "gym-short": "short",
  "chunky-snk": "chunky", "low-snk": "sneaker", "runner": "sneaker", "loafer": "loafer", "chelsea": "boot", "strap-heel": "heel"
};
const SHIRTS = ["oxford", "camp-shirt", "drape-top", "crinkle-shirt", "big-shirt"];
const TOP_CUTS = {
  crop: { ease: 3, hem: 186, sleeve: .24 }, tee: { ease: 3, hem: 238, sleeve: .24 }, tank: { ease: 2, hem: 236, sleeve: 0 },
  peplum: { ease: 3, hem: 248, sleeve: .28 }, regtee: { ease: 10, hem: 252, sleeve: .28 }, shirt: { ease: 10, hem: 258, sleeve: .92 },
  knit: { ease: 10, hem: 250, sleeve: .95 }, overtee: { ease: 26, hem: 284, sleeve: .4 }, sweat: { ease: 26, hem: 272, sleeve: .96 },
  bigshirt: { ease: 24, hem: 296, sleeve: .96 }
};
const LEG_CUTS = { slim: [14, 11], straight: [20, 19], wide: [28, 44], cargo: [26, 34], flare: [14, 34] };
const JACKETS = {
  "blazer": { hem: 268 }, "power-blazer": { hem: 272, shoulder: 10 }, "chore": { hem: 258 },
  "track-top": { hem: 246 }, "trench": { hem: 420 }, "crop-puffer": { hem: 222, puff: 8 }
};

function shade(hex, amount) {
  const value = parseInt(hex.slice(1), 16);
  const channel = shift => Math.max(0, Math.min(255, Math.round(((value >> shift) & 255) * (1 + amount))));
  return `rgb(${channel(16)},${channel(8)},${channel(0)})`;
}
const lineFor = hex => {
  const value = parseInt(hex.slice(1), 16);
  const light = ((value >> 16) & 255) + ((value >> 8) & 255) + (value & 255) > 390;
  return light ? shade(hex, -0.32) : shade(hex, 0.6);
};

const toPath = points => `M${points.map(([x, y]) => `${MX + x} ${y}`).join(" L")} Z`;
const shape = (points, fill, line) => `<path d="${toPath(points)}" fill="${fill}" stroke="${line}" stroke-width="1.2" stroke-linejoin="round"/>`;
const mirrored = points => [...points, ...points.slice().reverse().filter(([x]) => x !== 0).map(([x, y]) => [-x, y])];
const bothSides = markup => `${markup}<g transform="translate(${MX * 2},0) scale(-1,1)">${markup}</g>`;

function limb(from, to, width, fill, line) {
  const d = `M${MX + from[0]} ${from[1]} L${MX + to[0]} ${to[1]}`;
  return `<path d="${d}" stroke="${line}" stroke-width="${width + 2.4}" stroke-linecap="round" fill="none"/><path d="${d}" stroke="${fill}" stroke-width="${width}" stroke-linecap="round" fill="none"/>`;
}
const armEnd = (f, t) => [f.sh - 3 + 25 * t, 98 + 200 * t];

function drawForm(f) {
  const leg = [[f.hip - 1, 240], [f.hip - 5, 325], [37, 400], [34, 504], [18, 504], [13, 400], [3, 278]];
  return `<ellipse cx="${MX}" cy="548" rx="46" ry="5" fill="${FORM_LINE}" opacity=".45"/>
    <ellipse cx="${MX}" cy="42" rx="21" ry="26" fill="${FORM_FILL}" stroke="${FORM_LINE}"/>
    <rect x="${MX - f.neck + 3}" y="62" width="${(f.neck - 3) * 2}" height="28" fill="${FORM_FILL}"/>
    ${bothSides(limb([f.sh - 3, 98], armEnd(f, 1), 17, FORM_FILL, FORM_LINE) + `<circle cx="${MX + armEnd(f, 1)[0] + 2}" cy="310" r="9" fill="${FORM_FILL}" stroke="${FORM_LINE}"/>`)}
    ${bothSides(shape(leg, FORM_FILL, FORM_LINE))}
    ${shape(mirrored([[f.neck, 84], [f.sh, 92], [f.chest, 135], [f.waist, RISE - 1], [f.hip, 245], [0, 282]]), FORM_FILL, FORM_LINE)}`;
}

function drawShoes(item) {
  const hex = COLORS[item.color].hex, line = lineFor(hex);
  const kind = GARMENTS[item.id];
  const uppers = {
    sneaker: "M2 34 L2 16 Q14 10 22 16 L34 24 Q48 26 52 34 Z",
    chunky:  "M2 34 L2 12 Q14 6 22 12 L34 22 Q50 24 54 34 Z",
    loafer:  "M2 34 L3 22 Q14 19 24 22 L36 26 Q48 28 52 34 Z",
    boot:    "M3 34 L3 -8 H23 L25 16 Q46 22 52 34 Z",
    heel:    "M8 32 L14 8 L22 8 L24 18 L46 28 Q52 30 52 34 H26 L22 22 Z"
  };
  const soles = {
    sneaker: `<rect x="0" y="34" width="54" height="6" rx="2" fill="#f8f6f1" stroke="#8a8378"/>`,
    chunky:  `<path d="M0 34 H56 L58 44 Q58 48 54 48 H3 Q-1 48 0 44 Z" fill="#f8f6f1" stroke="#8a8378"/>`,
    loafer:  `<rect x="0" y="34" width="54" height="4" rx="1" fill="${shade(hex, -0.4)}"/>`,
    boot:    `<rect x="0" y="34" width="54" height="5" rx="1" fill="${shade(hex, -0.4)}"/>`,
    heel:    `<rect x="9" y="32" width="9" height="16" fill="${shade(hex, -0.3)}"/><rect x="28" y="34" width="26" height="3" rx="1" fill="${shade(hex, -0.3)}"/>`
  };
  const foot = `<path d="${uppers[kind]}" fill="${hex}" stroke="${line}" stroke-width="1.2" stroke-linejoin="round"/>${soles[kind]}`;
  return bothSides(`<g transform="translate(${MX + 15},502) scale(.86)">${foot}</g>`);
}

function drawBottom(item, f) {
  const hex = COLORS[item.color].hex, line = lineFor(hex);
  const kind = GARMENTS[item.id];
  const hipLine = [[f.waist + 1, RISE], [f.hip + 3, 245]];
  if (kind === "midi" || kind === "maxi") {
    const hem = kind === "midi" ? 415 : 505;
    return shape(mirrored([[0, RISE], ...hipLine, [f.hip + (kind === "midi" ? 14 : 10), hem], [0, hem]]), hex, line);
  }
  if (kind === "short") {
    return shape(mirrored([[0, RISE], ...hipLine, [f.hip + 12, 345], [6, 345], [0, 282]]), hex, line);
  }
  const [knee, hem] = LEG_CUTS[kind];
  const bottom = kind === "wide" ? 518 : 506;
  const legs = shape(mirrored([[0, RISE], ...hipLine, [25 + knee, 400], [26 + hem, bottom], [Math.max(2, 26 - hem), bottom], [Math.max(3, 25 - knee), 400], [0, 282]]), hex, line);
  const pockets = kind === "cargo" ? bothSides(`<rect x="${MX + 34}" y="335" width="26" height="30" rx="2" fill="${hex}" stroke="${line}"/>`) : "";
  return legs + pockets;
}

const bodyWidthAt = (f, y) => y <= RISE ? f.waist + (f.chest - f.waist) * (RISE - y) / (RISE - 135) : f.waist + (f.hip - f.waist) * Math.min(1, (y - RISE) / 49);

function drawTop(item, f) {
  const hex = COLORS[item.color].hex, line = lineFor(hex);
  const kind = GARMENTS[item.id];
  const { ease, hem, sleeve } = TOP_CUTS[kind];
  const boxy = ease >= 20;
  const side = [[0, kind === "tank" ? 106 : 92]];
  if (kind === "tank") side.push([f.neck + 9, 82], [f.sh - 9, 92], [f.chest + ease, 135]);
  else side.push([f.neck + 1, 80], [f.sh + ease * .4, 92], [f.chest + ease, 135]);
  if (boxy) side.push([f.chest + ease, hem]);
  else if (kind === "peplum") side.push([f.waist + ease, RISE], [f.hip + 18, hem]);
  else {
    if (hem > RISE) side.push([f.waist + ease, RISE]);
    side.push([bodyWidthAt(f, hem) + ease, hem]);
  }
  side.push([0, hem]);
  let detail = "";
  if (SHIRTS.includes(item.id)) detail = `<path d="M${MX} 92 V${hem}" stroke="${line}" fill="none"/><path d="M${MX - 13} 80 L${MX} 97 L${MX + 13} 80" stroke="${line}" fill="none" stroke-width="1.6"/>`;
  if (item.id === "knit-polo") detail = `<path d="M${MX - 13} 80 L${MX} 100 L${MX + 13} 80" stroke="${line}" fill="none" stroke-width="1.6"/>`;
  const arms = sleeve ? bothSides(limb([f.sh - 3, 99], armEnd(f, sleeve), 21 + ease * .55, hex, line)) : "";
  return arms + shape(mirrored(side), hex, line) + detail;
}

function drawLayer(item, top, f) {
  if (!item) return "";
  const hex = COLORS[item.color].hex, line = lineFor(hex);
  const jacket = JACKETS[item.id];
  if (jacket) {
    const room = TOP_CUTS[GARMENTS[top.id]].ease + 9 + (jacket.puff || 0);
    const shoulder = f.sh + room * .4 + (jacket.shoulder || 0);
    const panel = [[7, 88], [f.neck + 2, 78], [shoulder, 91], [f.chest + room, 135], [f.chest + room + (jacket.hem > 300 ? 12 : 0), jacket.hem], [9, jacket.hem], [4, 150]];
    const sleeve = limb([shoulder - 5, 101], armEnd(f, .97), 25 + room * .45, hex, line);
    return bothSides(sleeve + shape(panel, hex, line));
  }
  if (item.id === "crossbody") {
    return `<path d="M${MX + f.sh - 12} 90 L${MX - f.hip - 8} 236" stroke="${line}" stroke-width="3" fill="none"/>
      <rect x="${MX - f.hip - 34}" y="228" width="50" height="38" rx="6" fill="${hex}" stroke="${line}"/>`;
  }
  if (item.id === "tote") {
    const x = MX + armEnd(f, 1)[0] + 2;
    return `<path d="M${x - 14} 332 Q${x} 296 ${x + 14} 332" stroke="${line}" stroke-width="3" fill="none"/>
      <path d="M${x - 28} 330 H${x + 28} L${x + 32} 396 H${x - 32} Z" fill="${hex}" stroke="${line}" stroke-linejoin="round"/>`;
  }
  if (item.id === "scarf") {
    return `<rect x="${MX - f.neck - 7}" y="68" width="${(f.neck + 7) * 2}" height="24" rx="11" fill="${hex}" stroke="${line}"/>
      <rect x="${MX + 3}" y="88" width="24" height="100" rx="3" fill="${hex}" stroke="${line}"/>`;
  }
  if (item.id === "cap") {
    return `<path d="M${MX - 22} 34 Q${MX} -4 ${MX + 22} 34 Z" fill="${hex}" stroke="${line}"/><path d="M${MX + 10} 34 H${MX + 44} Q${MX + 42} 42 ${MX + 10} 40 Z" fill="${hex}" stroke="${line}"/>`;
  }
  return `<path d="M${MX - 23} 36 Q${MX} -14 ${MX + 23} 36 Z" fill="${hex}" stroke="${line}"/><rect x="${MX - 24}" y="28" width="48" height="13" rx="4" fill="${hex}" stroke="${line}"/>`;
}

function drawDummy(outfit) {
  const dept = activeAnswers().dept;
  const f = FORMS[dept];
  const { top, bottom, shoes, layer } = outfit.items;
  const label = names([top, bottom, shoes, layer].filter(Boolean).map(i => `${COLORS[i.color].label.toLowerCase()} ${i.name}`));
  const underTop = JACKETS[layer && layer.id] ? "" : drawLayer(layer, top, f);
  const overTop = JACKETS[layer && layer.id] ? drawLayer(layer, top, f) : "";
  // Bags, scarves and hats sit over the top; jackets sit over everything too.
  return `<svg viewBox="0 0 300 556" role="img" aria-label="${DEPTS[dept]} dummy wearing ${label}">
    ${drawForm(f)}${drawShoes(shoes)}${drawBottom(bottom, f)}${drawTop(top, f)}${overTop}${underTop}
  </svg>`;
}

'''
R('function renderPhotos(present, outfit) {', CODE + 'function renderPhotos(present, outfit) {')
R('''<div class="lay">${renderPhotos(present, outfit)}</div>''', '''<figure class="dummy">
          ${drawDummy(outfit)}
          <figcaption>${DEPTS[a.dept]} form, in your colors and proportions</figcaption>
        </figure>
        <div class="lay">${renderPhotos(present, outfit)}</div>''')
R('''  .lay { display: grid;''', '''  .dummy { margin: 0 0 8px; padding: 10px 10px 6px; border-radius: var(--radius); background: var(--lay); text-align: center; }
  .dummy svg { display: block; width: 100%; max-width: 300px; height: auto; margin: 0 auto; }
  .dummy figcaption { margin-top: 4px; font-size: .8rem; color: #3a4438; }
  .lay { display: grid;''')
R('''  // Bags, scarves and hats sit over the top; jackets sit over everything too.
''', '')
R('''const underTop = JACKETS[layer && layer.id] ? "" : drawLayer(layer, top, f);
  const overTop = JACKETS[layer && layer.id] ? drawLayer(layer, top, f) : "";
''', '')
R('''${drawTop(top, f)}${overTop}${underTop}''', '''${drawTop(top, f)}${drawLayer(layer, top, f)}''')
open(p, 'w', encoding='utf-8', newline='').write(s)
print('ok')
