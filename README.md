# StyleMod Outfit Builder

A concept mockup for a marketing case study on responsible Gen AI personalization. The live site is the five-question presentation version: gender, age range, color palette, style and accessory, which returns three quarter-zip outfits on a dressed dummy. The original full quiz lives on the [`full-quiz`](../../tree/full-quiz) branch.

**Live demo:** https://arthurslin.github.io/StyleMod-demo/

StyleMod is a theoretical product. Product data is placeholder, brand names are illustrative with no affiliation or endorsement, and the app runs in the browser in memory only.

The app lives in [`index.html`](index.html), with style photos in [`images/`](images). Comments marked `GEN AI PLUG-IN POINT` show where a real model would connect to the rules-based mock engine.

Photos come from Unsplash under the Unsplash License and are listed in [`credits.html`](credits.html). They show each style, not the mock products, and appear only on pieces listed in the color pictured. Dummies show every outfit using AI-generated garment images from Google Gemini (in `images/wear/`), tinted in the browser to the exact listed color. The catalog reflects trend coverage as of November 2026, and the sources are linked on the results page.
