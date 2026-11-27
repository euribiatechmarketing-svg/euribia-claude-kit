# Euribiatech posts: technical showcase template (locked 12.11.2026)

Euribiatech = the software division (custom software, platforms, business systems, AI, Odoo).
It is NOT Euribia Digital: different brand, different voice, different template. Posts show **systems we
built**, using the real screens.

## Where
- Figma file `fwTWYozj0aTtlTMvKtVJRR`, page **Euribiatech Posts** (`422:2`).
  - Section **Reference** (`422:3`): 6 masters `ET Master · …` plus the logo assets (white / dark).
  - Section **Results** (`422:4`): finished posts. New post = new row 1550 px below the last one.
- First post: **Onfile** (`Onfile · Cover … CTA`, Results row y=200).
- PNGs: `~/Documents/01-Euribia/posts/euribiatech/<YYYY-MM-DD>-<slug>/` (01–06.png + caption.txt).

## Brand (from euribiatech.com / OFFICIAL-EURIBIA "Tech rebrand")
- Montserrat only: Bold for headlines, SemiBold for labels and pills, Regular/Medium for body. **No monospace anywhere.**
- Colours: navy `#040638`, ink `#15153B`, blue `#236AF8`, sky `#4FB1FD`, paper `#F4F6FB`, line `#DCE3F0`, body `#3A4060`, muted `#6B7393`.
- Hero gradient `#040638 → #236AF8 (51%) → #4FB1FD`. Glass pill = white gradient 10/22/10% + white stroke 40%, radius 34.5.
- Headlines are sentence case (not uppercase), with ONE accent word in sky (dark slides) or blue (light slides).
- Blueprint grid: 1 px lines every 60 px, white 5% on dark and blue 6% on light, plus one blurred glow ellipse.
- Real logo: clone `asset · euribiatech logo white/dark`, 150 px wide at x80 y66. Tag pill top right (e.g. "Система · Onfile", "Проблемът", "Как работи", "Под капака", "Мобилно").
- Footer: hairline at y1240, `euribiatech.com` in Montserrat SemiBold 22 at x80 y1268. No slide counters.

## The 6 slide types (1080×1350, margin 80)
1. **Cover (product hero)**: gradient, 2-line headline, 1-line sub, real desktop screen in a browser frame bleeding off the right side, phone overlapping bottom-left.
2. **Problem (big number + specs)**: light. Giant blue number, label, 3 sentences, "file chaos" chips (or another concrete artefact of the pain), 3 spec cards: Type / Platforms / Stack.
3. **System map (pipeline)**: dark. 3 numbered glass node cards on a gradient connector line (step, one sentence, 3 chips), one sky kicker line under them.
4. **Under the hood (annotated screen)**: dark. One real screen in a browser frame with 2–3 numbered markers placed NEXT TO the detail (never on top of it) and a numbered legend underneath.
5. **Mobile + metrics**: light. Phone on the right; left = 2 big blue metrics with labels, one feature sentence, and a footnote on how it was measured.
6. **CTA**: gradient card (radius 43, grid inside): question headline, one-sentence promise, white pill `sales@euribiatech.com`, "before → after" flow tiles, service pills.

Pick 5–7 slides per post: types 3, 4 and 5 can repeat or be dropped to fit the project.

## Rules
- **Only real screens** from the project (Figma Portfolio file, the project's own repo or deck). Never AI-generated UI. Demo data only, never real client data.
- Every number and claim must come from the project's own README/deck or the portfolio PDF. A measured number gets its footnote.
- Copy in Bulgarian, technical but readable by a business owner. No em-dashes, no single word alone on a line, no lorem ipsum (some Figma frames, e.g. Eastvantage V2, still contain lorem: crop around it or skip).
- Uploads: convert WebP to PNG first (`sips -s format png`). Use `upload_assets` without nodeIds only to get the hash, then set fills on your own rectangles and delete the auto-created frames.
- Screenshot every frame before calling it done.

## Project catalogue (rotate; log each in `state/ledger.json` with type "euribiatech-post")
| Project | What it is | Screens |
|---|---|---|
| Onfile | Workforce-compliance system for labour migration (Python, PostgreSQL, Claude) | `~/Developer/projects/onfile-deck/assets/img/*.webp`; Portfolio Figma `12:276` desktop, `16:276` mobile. Facts: onfile-deck `index.html`, worker-docs README. **Done 12.11.2026** |
| MobileBids | Car marketplace platform (classifieds, dealer portal, auctions later) | Portfolio Figma `22:276`/`27:276` desktop dark/light, `25:276`/`31:276` mobile |
| SYNCHRO Engineering | Manufacturer website, precision gears | Portfolio Figma `7:276` |
| Eastvantage | Corporate website for an outsourcing partner | Portfolio Figma `1:352` desktop, `1:7257` mobile (contains lorem: crop) |
| Pharmalyze, FlyCI, MacStadium, EventAT, TripTransfer, Ameru, Tribuna | see `~/Downloads/Portfolio_Selected_Work_2026.pdf` (51 pages, one overview page per project) | pages in the PDF; render with PDFKit (`swift` script) since poppler is not installed |

Check with Dimitar before showing a client project that may be under NDA. Internal products (Onfile, MobileBids, Elevate, Agent OS) are safe to show.
