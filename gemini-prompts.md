# Gemini image prompts for StyleMod

Start with the **pilot batch** (5 images). I'll use those to confirm the clothes line up on the dummy before you generate the rest.

Generate each image in a new chat if you can, so the styles don't drift. Use the portrait 2:3 ratio, and save each image with the file name shown.

## Pilot batch

### 1. Dummy: `dummy-womenswear.png`

> Studio product photograph of a full-body female retail display mannequin, matte warm-grey finish, smooth abstract egg-shaped head with no face and no hair, no clothing. Standing perfectly straight facing the camera, symmetrical, feet slightly apart, arms straight and held about 15 degrees away from the body, palms facing inward. The whole figure is in frame from head to toes with a small margin. Pure white seamless background, soft even lighting, no shadows on the background, no stand, no text, no logos. Portrait 2:3.

### 2 to 5. Garments

Paste the base prompt below, replacing `[ITEM]` with the description from the table.

**Garment base prompt**

> Professional e-commerce "ghost mannequin" product photograph of [ITEM]. The garment appears worn by an invisible person, with natural 3D volume and realistic fabric folds, seen from directly in front, perfectly symmetrical and centered. Any sleeves hang straight down, about 15 degrees away from the body. The fabric is a solid light neutral grey with no color tint, no pattern, and clear visible texture and fold shading. Nobody is visible: no mannequin, no hanger, no skin. Pure white seamless background, soft even studio lighting, no cast shadow, no text, no logos, no labels. The whole garment is in frame with a small margin. Portrait 2:3.

| File name | [ITEM] |
|---|---|
| `tee.png` | a classic crew-neck short-sleeve t-shirt, regular fit, hem at the hip |
| `wide-trousers.png` | a pair of high-waisted wide-leg trousers with a clean front crease, full length, legs falling straight down side by side |
| `blazer.png` | a single-breasted unstructured blazer worn open at the front, regular fit, hem at the upper thigh, the inside of the jacket left empty |

**Shoe prompt: `sneakers.png`**

> Professional e-commerce product photograph of a pair of plain low-top lace-up sneakers, seen from directly in front, side by side with toes pointing toward the camera and slightly outward, symmetrical and centered. Solid light neutral grey upper and sole with no color tint, clear visible texture and shading. No feet, no socks, no logos, no labels, no text. Pure white seamless background, soft even lighting, no cast shadow. Square 1:1.

## Full batch, after the pilot works

### Other dummies

Use the dummy prompt above, changing "female" and the file name.

| File name | Change |
|---|---|
| `dummy-menswear.png` | male retail display mannequin, broader shoulders |
| `dummy-unisex.png` | gender-neutral retail display mannequin, straight balanced proportions |

### Tops: garment base prompt

| File name | [ITEM] |
|---|---|
| `crop-tee.png` | a fitted cropped short-sleeve t-shirt, hem above the navel |
| `fitted-tee.png` | a fitted ribbed crew-neck short-sleeve t-shirt |
| `tank.png` | a fitted ribbed sleeveless tank top |
| `polo.png` | a fine-knit short-sleeve polo shirt with a collar and two buttons |
| `peplum.png` | a fitted short-sleeve top with a flared peplum at the waist |
| `shirt.png` | a long-sleeve button-up oxford shirt, collar and buttons fastened, untucked |
| `camp-shirt.png` | a short-sleeve camp-collar button-up shirt |
| `blouse.png` | a drapey long-sleeve satin blouse with a soft V-neck |
| `crinkle-shirt.png` | a long-sleeve button-up shirt in crinkle-textured fabric |
| `sweater.png` | a fine-gauge long-sleeve crew-neck sweater |
| `oversized-tee.png` | an oversized boxy short-sleeve t-shirt with dropped shoulders, hem at mid-thigh |
| `sweatshirt.png` | an oversized boxy crew-neck sweatshirt with dropped shoulders |
| `chunky-knit.png` | an oversized chunky cable-knit sweater |
| `big-shirt.png` | an oversized long-sleeve poplin button-up shirt, hem at mid-thigh |

### Bottoms: garment base prompt

| File name | [ITEM] |
|---|---|
| `slim-pants.png` | a pair of slim tapered chino trousers, full length |
| `slim-jeans.png` | a pair of slim jeans, full length, with denim texture |
| `straight-jeans.png` | a pair of straight-leg jeans, full length, with denim texture |
| `straight-trousers.png` | a pair of straight-leg tailored trousers, full length |
| `joggers.png` | a pair of tapered joggers with a drawstring waist and cuffed ankles |
| `track-pants.png` | a pair of straight-leg track pants with an elastic waist |
| `flared-leggings.png` | a pair of high-waisted flared leggings, fitted to the knee, then flared |
| `wide-jeans.png` | a pair of wide-leg jeans, full length, with denim texture |
| `wide-sweatpants.png` | a pair of wide-leg sweatpants with a drawstring waist |
| `cargo-pants.png` | a pair of relaxed cargo pants with large side pockets |
| `parachute-pants.png` | a pair of baggy nylon parachute pants with a drawstring waist |
| `shorts.png` | a pair of loose athletic training shorts, knee length |
| `midi-skirt.png` | a midi slip skirt, hem below the knee |
| `maxi-skirt.png` | a long column maxi skirt, hem at the ankle |

### Layers: garment base prompt

Add "worn open at the front, the inside left empty" to each jacket except the cropped puffer if it looks better closed.

| File name | [ITEM] |
|---|---|
| `power-blazer.png` | an oversized blazer with strong structured shoulders |
| `chore-jacket.png` | a canvas chore jacket with patch pockets |
| `track-jacket.png` | a zip-front track jacket with a stand collar |
| `trench.png` | a long slouchy belted trench coat, hem below the knee, belt hanging loose |
| `puffer.png` | a cropped quilted puffer jacket |

### Shoes: shoe prompt, replacing "plain low-top lace-up sneakers"

| File name | Replace with |
|---|---|
| `chunky-sneakers.png` | plain chunky sneakers with a thick layered sole |
| `runners.png` | plain lightweight running shoes |
| `loafers.png` | plain leather penny loafers |
| `chelsea-boots.png` | plain leather Chelsea boots |
| `block-heels.png` | plain strappy block-heel sandals |

### Accessories

Use this prompt, replacing `[ITEM]`, then square 1:1.

> Professional e-commerce product photograph of [ITEM], seen from directly in front, centered. Solid light neutral grey with no color tint, clear visible texture and shading. No person, no logos, no labels, no text. Pure white seamless background, soft even lighting, no cast shadow.

| File name | [ITEM] |
|---|---|
| `crossbody-bag.png` | a small crossbody bag with a long strap |
| `tote.png` | a slouchy canvas tote bag |
| `scarf.png` | a wool scarf, folded and hanging straight |
| `cap.png` | a plain six-panel baseball cap |
| `beanie.png` | a ribbed beanie |
