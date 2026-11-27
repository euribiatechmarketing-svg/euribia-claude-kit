# McVitie's — brand kit (extracted from the client's Figma file)

This is the worked example bundled with the skill. Every value here was pulled from the
real McVitie's design file, not invented. Reuse these files directly; do not redraw the logo.

**Source Figma file:** `gr9HeKKhGEj5l055TmOdEn` (the "Post-Structure" file).

## Colors (sampled from the real brand pieces)
| Token | Hex | Notes |
|---|---|---|
| Royal blue (bright) | `#122AB1` | gradient start; sampled `#0018A8` |
| Deep navy | `#071A79` | gradient end; sampled `#001878` |
| Logo banner navy | `#21306E` | the wordmark plate |
| Indigo accent | `#252F7F` | used for text-on-light (e.g. "АПРИЛ") |
| Golden yellow | `#FAC710` | sunburst core; sampled `#F0C000` |
| Sunburst orange | `#F39200` | ray tips; sampled `#F09000` |
| Red | `#C8102E` | sport/accent; sampled `#C01830` |
| Biscuit wheat | `#D9A24E` | digestive body |
| Milk chocolate | `#5A2D0C` | coated biscuit |
| White | `#FFFFFF` | primary type on blue |

**Signature background = radial gradient**, center `#122AB1` → edge `#071A79`
(Figma color style `McVitie's/Gradient/McVities`). The red logo uses linear styles
`McVitie's/logo/linear 1…5`.

## Fonts
- **Display / headlines:** `Asgard Trial` (weight *Fit Bold*) — a heavy condensed display.
  If unavailable, substitute a heavy condensed sans (Montserrat Black / Anton / a similar
  geometric heavy) and flag the substitution.
- **Body / info / numbers:** `Montserrat` (Bold, SemiBold, Regular).

## Bundled assets (in this folder)
| File | What it is | Px |
|---|---|---|
| `mcvities-logo.svg` | Official logo, vector (navy banner, gold flame, ®) | 969×429 |
| `mcvities-logo.png` | Same, transparent raster | 2907×1287 |
| `biscuit-digestive.png` | Hero milk-chocolate Digestive cut-out, transparent | 1181×944 |
| `pack-digestives-box.png` | Digestives Milk Chocolate pack shot, transparent | 2048×1438 |
| `biscuit-perspective-1.png` | Small biscuit shot | 296×236 |
| `biscuit-perspective-2.png` | Small biscuit shot | 512×360 |

## Where each element lives in the client file (to re-pull / get more)
- **Logo:** node `611:492` (`Layer_1` / `RGB_LIGHT`) → export as SVG via `download_assets`.
- **Product photography:** node `611:491` (Digestives post) and `611:382` (Tartlets post) →
  `download_assets` returns the raw pack-shot + biscuit PNGs in `rawImages`.
- **Sunburst + scattered-biscuit arc + game props:** event banners
  `7661:16493`, `7656:509`, `7656:105`, `7661:15599`, `7661:16046`, `7656:3748`.
- **Biscuit "crumb" arc:** the many small `Vector` nodes inside `611:491` (rotated ~-43°/-52°).

## Headline copy (placeholders — confirm with Dimitar before final)
The voucher is the **prize** in the "ИГРАЙ И СПЕЧЕЛИ С McVitie's" campaign. Options used in review:
- Warmth: `ИЗЖИВЕЙ МИГ НА УЮТ` (ties to McVitie's уют/топлина positioning)
- Campaign: `ИГРАЙ · СПЕЧЕЛИ · ИЗЖИВЕЙ`
- Celebratory: `ТИ СПЕЧЕЛИ ПРЕЖИВЯВАНЕ`
