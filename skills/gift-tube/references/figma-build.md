# Building the set in Figma (print-ready, real assets)

Goal: three frames at the exact pt sizes from `print-specs.md`, with the client's real logo and
photos placed (not redrawn), exportable straight to Illustrator.

## Before any `use_figma` call
Read the **`/figma-use`** skill first — it is mandatory before `use_figma` and explains the batched
node-creation API. This skill never bypasses it.

## Frames (px = pt)
- `GiftTube / <Client> / Tube label` — **569.76 × 442.21**
- `GiftTube / <Client> / Voucher — front` — **385.51 × 867.40**
- `GiftTube / <Client> / Voucher — back` — **385.51 × 867.40**

Put them on their own page (e.g. a page named `Gift Tube — <Client>`). Default to the **client's
own Figma file** so brand styles/components are reachable; if the client prefers a clean handoff
file, `create_new_file`. Confirm the destination with the user if unsure.

Add inside each voucher frame: a **trim** rectangle (130×300 → 368.50×850.39, centered, no fill,
0.5pt magenta stroke, locked) and a **safe** rectangle ~5 mm inside. Mark them non-printing /
delete before final export. For the tube label, add the safe rect only (bleed is in the canvas).

## Placing real assets
- **Logo:** `upload_assets` the client logo SVG/PNG into the file, place it, scale by width. Keep it
  vector (SVG) where possible so it stays crisp in Illustrator.
- **Photos (biscuits / pack shot):** `upload_assets` the transparent PNGs, place as image fills on
  rectangles or as image nodes. **Watch the resolution gotcha** (see memory `figma-image-fill-gotcha`):
  setting fills via `upload_assets` placement can silently fail — after placing, **verify** the node
  actually shows the image (screenshot) and if not, set `node.fills` via `use_figma`.
  Ensure each photo is ≥ 300 ppi at its placed size: placed width(mm)/25.4×300 ≤ source px width.
- **Gift Tube emblem + lockup:** reuse the vector from `assets/gift-tube-chrome/*.svg`
  (`upload_assets` the SVG), or rebuild the emblem from the client's own Gift Tube copy.

## Recreate (native vectors, not assets)
- **Background:** rectangle filled with the brand's signature gradient (McVitie's = radial
  `#122AB1` center → `#071A79` edge).
- **Sunburst:** a group of thin triangles fanned from a top point, or an ellipse with an
  angular-gradient/!repeating ray fill, low-opacity yellow `#FAC710`→`#F39200`, masked to fade out.
- **Biscuit scatter:** duplicate 1–2 real biscuit PNGs along an arc at varied scale/rotation
  (the client file's own arc uses ~-43°/-52° rotations) — bleed them off the edges.
- **Light body panel** (voucher): cream `#FBF5E7` rectangle holding the functional content so the
  `ВАЛИДЕН ДО:` / `УНИКАЛЕН КОД:` fields sit on light (hard rule).

## Type
- Headlines in the brand display face (McVitie's: `Asgard Trial Fit Bold`; substitute a heavy
  condensed + flag if missing). Body/steps/fields in `Montserrat`.
- Bulgarian copy **verbatim** from `adaptation-rules.md` — no paraphrase, no translation.

## Layer order (bottom → top), per frame
`background gradient → sunburst → biscuit scatter / pack shot → [voucher: light body panel] →
content (logo, headline, fields, steps, QR, lockup) → trim/safe guides (non-printing)`.

## Finish
- Screenshot each frame (`get_screenshot`) and compare against the approved preview.
- Confirm the `ВАЛИДЕН ДО:`/`УНИКАЛЕН КОД:` light zone, the 3 mm bleed, the seam continuity on the
  tube label, and that the logo/photos are the real placed assets (not fonts/redraws).
- Set PDF + SVG export on each frame at 1×. Hand off per `print-specs.md`.
