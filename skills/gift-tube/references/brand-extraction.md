# Pulling a client's REAL brand out of their Figma file

Never approximate a client's identity with CSS look-alikes or a redrawn logo. Extract the actual
assets and tokens from their file, bundle them, and place those. McVitie's is done already
(`assets/examples/mcvities/`); this is the recipe for the next client.

## 0. Get the file key + a few node URLs
From any `figma.com/design/<fileKey>/...?node-id=<n>` link the client/Dimitar shares. The
whole-page `get_metadata` on a big marketing file often **times out** — don't fight it. Work from
the specific node IDs you're given and drill outward.

## 1. Logo → real vector
- Find the logo node (often named like `Logo`, `Layer_1`, `RGB_LIGHT`, or a component).
- `download_assets(fileKey, nodeId, defaultFormat: "svg")` → save the SVG. Render a PNG preview
  (`fitz`/pymupdf) and **eyeball it** to confirm it's the clean logo, not a fragment.
- Keep a transparent PNG too (scale 3–4) for quick placement.

## 2. Photography / product shots → raw source images
- `download_assets(fileKey, nodeId)` on a **post/frame** that contains the photos. The response's
  `rawImages[]` are the **original uploaded photos** (transparent PNGs/JPEGs) — exactly what you
  want for print, not the flattened frame render. Save each, check dimensions, downscale anything
  over ~3–4 MP that will only appear small.

## 3. Palette → sample, don't guess
- Render the client's strongest brand pieces to PNG, then sample dominant colors:
  ```python
  import fitz; from collections import Counter
  pm = fitz.Pixmap(path)
  if pm.n >= 4: pm = fitz.Pixmap(fitz.csRGB, pm)
  c = Counter()
  for y in range(0, pm.height, max(1, pm.height//120)):
      for x in range(0, pm.width, max(1, pm.width//120)):
          c[tuple((v//24)*24 for v in pm.pixel(x,y)[:3])] += 1
  for col, n in c.most_common(12): print('#%02X%02X%02X'%col, n)
  ```
- Cross-check against the file's **color styles**: `get_variable_defs(fileKey, nodeId)` lists named
  styles (e.g. `McVitie's/Gradient/McVities`, `McVitie's/logo/linear 1…5`). Gradients return empty
  hex — read the actual stops from a `get_design_context` of a node that uses them (the background
  `radialGradient` stops appear inline in the returned code).

## 4. Fonts
- `get_design_context` lists font families per text node (e.g. `Asgard Trial:Fit Bold`,
  `Montserrat:Bold`). Record display vs body. Trial/licensed fonts may not be installed — note a
  heavy substitute and **flag the substitution** to the user rather than silently swapping.

## 5. Write a `brand.md`
Mirror `assets/examples/mcvities/brand.md`: colors table, fonts, an asset manifest with pixel
sizes, and the **source node IDs** so anyone can re-pull. Save the assets under
`assets/examples/<client>/`.

## What "use the real elements" means in the build
- Place the **logo SVG/PNG** — never type the brand name in a font.
- Place the **real product photos** for the hero biscuits / pack shot — like Nestea uses real fruit.
- Recreate only the cheap generative bits (sunburst rays, color fields, the biscuit "scatter" arc)
  as native Figma vectors — those are patterns, not assets.
