# Print specs — sizes, bleed, and Figma → Illustrator export

The whole point of the set is that it exports from Figma and lands at **exact millimetres** in
Illustrator for print. Get the canvas sizes right and everything else follows.

## The unit trick: 1 px = 1 pt
Figma exports treat **1 px as 1 pt** (1/72 inch). So if a Figma frame is `W px × H px`, a
PDF/SVG export is `W pt × H pt`. Convert mm → pt with **1 mm = 2.834645 pt** and build the frame
at that pt value in pixels. Then the export is true-to-size with zero scaling in Illustrator.

## The three deliverables
| # | Piece | Trim (mm) | Bleed | Figma frame (px = pt) |
|---|---|---|---|---|
| 1 | Tube label (wrap) | 201 × 156 | bleed **already in** the 201×156 working file | **569.76 × 442.21** |
| 2 | Voucher — front | 130 × 300 | +3 mm all sides → 136 × 306 | **385.51 × 867.40** |
| 3 | Voucher — back | 130 × 300 | +3 mm all sides → 136 × 306 | **385.51 × 867.40** |

Helper: trim 130×300 = `368.50 × 850.39 pt`; 3 mm = `8.50 pt`.

### Tube label notes
- The 201×156 master **is the full bleed canvas** — do not add more bleed. Keep the logo, the
  `gift-tube.com` line and any must-read text **≥ 6 mm inside** the edges (safe area ≈ 189×144).
- It wraps a ~64 mm-diameter tube (201 mm ≈ circumference). Center the "front panel" composition
  (logo → headline → badge → lockup) and let pattern/biscuits/rays bleed off both sides so the
  wrap reads continuously. The left and right 3 mm edges should meet seamlessly — keep the
  background continuous there, no hard objects crossing the seam.

### Voucher notes
- Build at **136 × 306 mm** (bleed included). Put a **trim guide** rectangle at 130×300 centered
  (inset 3 mm) and a **safe margin** ~5 mm inside trim. Keep all text inside safe.
- The **back** is only needed for **physical** vouchers. Digital vouchers = front only, no back.

## Mandatory light zone (do not skip)
Gift Tube's system overprints the validity date and unique code in **dark text** that cannot be
changed. The `ВАЛИДЕН ДО:` and `УНИКАЛЕН КОД:` fields — and the gap beneath them — **must sit on a
light background** and keep their relative position + spacing. See `adaptation-rules.md`.

## Color
- Design in Figma in **RGB** (Figma is RGB only). Treat the hexes as the on-screen target.
- Convert to **CMYK in Illustrator** at the print stage. Warn the user that saturated RGB blues
  (`#122AB1`) and yellows shift in CMYK; ask the printer for a profile if critical.
- Rich black for large dark fills: suggest `C60 M40 Y40 K100` in Illustrator (not 4×100).

## Export procedure (from Figma)
1. Select the frame. Export settings: **PDF** (vector, keeps text + vectors editable) at **1×**.
   Add an **SVG** export too as a fallback. (Placed raster photos export embedded at their native
   resolution — keep them ≥ 300 ppi at final size; see build notes.)
2. Ensure **Clip content** is ON for the frame so bleed objects don't leak past the canvas.
3. In Illustrator: open the PDF → artboard is exact mm. Re-link/optimize photos, convert to CMYK,
   outline or package fonts, verify bleed + trim marks, then hand to the printer.
4. If fonts aren't installed for the printer, **outline the display type** before sending (keep an
   editable copy).
