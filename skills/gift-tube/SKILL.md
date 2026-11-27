---
name: gift-tube
description: >-
  Design a co-branded GIFT TUBE experience-voucher set — the cardboard gift tube label plus the
  two-sided voucher (ваучер за преживяване) — in a client's real brand, print-ready for Illustrator.
  Use this whenever the user wants to make, adapt, or print a Gift Tube voucher/tube/tubus for a
  brand (e.g. "make a gift tube like the Nestea one for <brand>", "брандиран ваучер за преживяване",
  "gift-tube.com voucher", "tube label 201x156", "voucher 130x300"), or to co-brand the Gift Tube
  templates with a client identity pulled from their Figma file. Builds in Figma at exact print
  sizes with 3 mm bleed using the client's REAL logo + product photos (never CSS look-alikes).
---

You produce **Gift Tube** co-branded gift sets: a brand sponsors an "experience voucher"
(ваучер за преживяване) that ships inside a printed cardboard tube. You adapt Gift Tube's fixed
templates into the **client's identity**, following the printer's hard rules, and deliver three
print-ready Figma frames that export straight to Illustrator at exact millimetres.

Reference model: the **Nestea × Gift Tube** tube (orange brand field, sunburst, big headline, the
Gift Tube sunburst badge, „ПОДАРИ ПРЕЖИВЯВАНЕ / gift-tube.com" lockup). You keep that *arrangement*
and pour the client's brand into it.

## The three deliverables (always these sizes)
| Piece | Trim | Figma frame (px = pt) |
|---|---|---|
| Tube label (wrap) | 201 × 156 mm (bleed in canvas) | 569.76 × 442.21 |
| Voucher — front | 130 × 300 mm + 3 mm bleed | 385.51 × 867.40 |
| Voucher — back (physical only) | 130 × 300 mm + 3 mm bleed | 385.51 × 867.40 |

Full detail in `references/print-specs.md`. Don't deviate from the pt sizes — that's what makes the
Illustrator export true-to-size.

## Non-negotiables (the printer's rules)
- `ВАЛИДЕН ДО:` and `УНИКАЛЕН КОД:` keep their position + spacing and sit on a **light background**
  (the system overprints them in dark text you can't restyle).
- Keep the **GIFT TUBE logo**, the **`gift-tube.com`** site, and the wording **„Ваучер за
  преживяване"** (logo/site may move, not disappear).
- QR + contacts stay on the **front**. The old „Специално за" + „Пожелание от сърце" may become one
  shared `Пожелание:` field. 3 mm bleed. **Back only for physical vouchers** (digital = front only).
- Bulgarian copy is used **verbatim** — never paraphrase or translate it.

Everything (and the verbatim copy) is in `references/adaptation-rules.md`. Read it before designing.

## Use the client's REAL elements — not approximations
The brand must be built from the client's actual assets: place the **real logo** (vector) and
**real product photos**, recreate only cheap patterns (sunburst, color field, biscuit scatter) as
native vectors. How to pull them from a client's Figma file is in `references/brand-extraction.md`.

The **McVitie's** client is already extracted and bundled — start from it for any McVitie's job:
- `assets/examples/mcvities/brand.md` — colors, fonts, asset manifest, source node IDs.
- Real assets in that folder: `mcvities-logo.svg`, `biscuit-digestive.png`,
  `pack-digestives-box.png`, biscuit shots.
- Source file: `gr9HeKKhGEj5l055TmOdEn`. Signature look: royal-blue radial `#122AB1→#071A79`,
  golden-yellow `#FAC710` sunburst, red `#C8102E`, `Asgard Trial` display + `Montserrat` body.

## Gift Tube chrome (shared across all clients)
`assets/gift-tube-chrome/` holds the master templates and reusable vector chrome:
- `masters/GT_Voucher_130x300mm.pdf`, `masters/GT_TubeLabel_201x156mm.pdf` — the print masters.
- `voucher-front.svg`, `tube-label.svg` — vector chrome (GIFT TUBE emblem, field layout, lockup).
- `*.png` — flat previews of the general (unbranded) templates for layout reference.

## Workflow
1. **Frame the job.** Which client? Physical or digital (digital ⇒ no back)? Confirm the headline
   copy — it's the one real creative choice; offer the options in the client's `brand.md`.
2. **Get the brand.** If the client is McVitie's, use the bundled kit. Otherwise run
   `references/brand-extraction.md` to pull logo + photos + palette + fonts and write a new
   `assets/examples/<client>/brand.md`.
3. **Preview first.** Mock the three artboards (correct proportions + bleed) with the
   `mcp__visualize__show_widget` tool so the user approves layout/copy/colour **before** Figma.
   Treat it as a product render (hardcoded brand hex, real logo/photo where embeddable).
4. **Build in Figma.** Follow `references/figma-build.md` (read `/figma-use` first; create the three
   frames at the pt sizes; `upload_assets` the real logo + photos; recreate sunburst/scatter as
   vectors; add trim/safe guides; mind the image-fill gotcha — verify fills actually render).
5. **Export.** Set PDF + SVG export per frame at 1×; hand off per `print-specs.md` (CMYK conversion,
   outline fonts, check bleed/seam) for Illustrator → print.
6. **QC the export.** Verify each PDF's real size + embedded-image DPI and declare bleed/trim, per
   `references/print-qc.md`. Catch low-res placed photos (upscale in-place, no regen) and the Figma
   144 dpi effect-rasterization floor before anything goes to the printer.

## Quality bar
- The light zone under `ВАЛИДЕН ДО:` / `УНИКАЛЕН КОД:` is genuinely light. Bleed is a true 3 mm.
- The tube-label seam (left/right edges) is continuous — no object straddles it awkwardly.
- The logo and biscuits are the **placed real assets**, confirmed by screenshot — not fonts/redraws.
- Copy matches the verbatim Bulgarian exactly. Headline confirmed with the user.
