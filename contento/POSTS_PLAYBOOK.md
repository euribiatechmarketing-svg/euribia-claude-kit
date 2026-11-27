# Euribia POSTS playbook (News carousel + story)

The repeatable process for building a "Posts" piece (informative/news carousel + story) in the OFFICIAL-EURIBIA brand. Read this **and** `EURIBIA_DESIGN_SYSTEM.md` before any Posts work.

## Where everything lives
- **File:** `fwTWYozj0aTtlTMvKtVJRR`, page **"Posts"** (`0:1`). Read the WHOLE file first.
- Three sections on the page:
  - **Reference** (`10:162`) — source templates. Duplicate from them; only edit them when the user explicitly wants to change the template itself.
  - **Tokens** (`10:163`) — brand/logo tokens. Don't touch.
  - **Results** (`11:133`) — the OUTPUT target. Everything you build goes here.
- **Photos in:** the user keeps a permanent PUBLIC Drive inbox: `https://drive.google.com/drive/folders/1jCa_YcwYPLzWVx2VSkIUoqGM4dR5sdts` (folderId `1jCa_YcwYPLzWVx2VSkIUoqGM4dR5sdts`). Pull NEW photos only (skip ones already used in a prior post): `search_files parentId='<folderId>'` → `curl -sL "https://drive.google.com/uc?export=download&id=<id>"`. Convert HEIC, dedupe by md5, register each in `assets/manifest.md`.

## Where a finished post GOES
Figma is the **build** surface; **PostFlow is the delivery target**. Once the 5 frames pass their
screenshot gate, export them (2x PNG, slide order) and push them into PostFlow as a **DRAFT
assigned to Dimitar**, caption included — full contract in `POSTFLOW.md`. Scheduled runs must do
this; a manual run does it whenever the post is meant to ship rather than just be reviewed in Figma.
The engine publishes to **no** social channel — approval and publishing happen in PostFlow, by hand.

## Default workflow ("quick confirm")
Give the user ONE message with: proposed topic + full Bulgarian copy + cover choice. They tap OK once. Then build end-to-end with NO mid-build stops and show the finished post. Build directly in the main thread (clone → text → layout standard → images via the use_figma fill method → screenshot-verify every frame) — faster and more reliable than dispatching a sub-agent. One approval at the end.


# ★★ AURA NEWS TEMPLATE: THE DEFAULT FOR NEWS POSTS (locked 11.11.2026)

Approved direction: AURA+GLASS look, but the image in every slot is an **AI image generated for
THIS story** (Higgsfield or Magnific), never a generic painterly field. Masters live in
Reference `10:162` at y=11100 (find by NAME, ids drift):

| Frame | Layout |
|---|---|
| `AURA News · Cover` | logo row → 3-line headline (Mulish Black, max 84, one size, ragged right) → `image` block from headline.bottom+42 to y=1144 → footer |
| `AURA News · Slide A (number + subject)` | `image` 920×465 @ y201: giant white number LEFT (`ui_big`, Mulish Black ~220, shadow) + label under it (`ui_biglbl`, Mulish ExtraBold 26, lowercase) + small glass chip (`ui_glass` + green dot + Mulish Bold 19 fact). Story subject sits in the RIGHT 45% of the image. |
| `AURA News · Slide B (glass card + subject)` | glass card LEFT (x40 y60, 400×280: header, pill, 3 label/value rows). Subject in the RIGHT 55% of the image. |
| `AURA News · Slide C (empty state)` | soft abstract aura + dashed rings + centred glass card with em-dash metrics. Use for "wait / no data yet / don't do X" slides. |
| `AURA News · CTA` | 3-line question headline, purple accent rule, black pill with the email, one hint line. |

Under every slide `image`: `headline-1/2` (Mulish Black max 76, one size) and `body` (Mulish Regular 29,
fixed box 920×180, starts heading.bottom+34). Slides A/B/C can be reordered or repeated; 3 info slides is the norm.

**Image generation (one image per slot, 4 per post):**
- Higgsfield `generate_image_batch`, model `gpt_image_2_6`; cover `4:3`, slides `16:9`. Magnific
  `imagen-nano-banana-2-1` is the alternative. (11.11.2026: Higgsfield ultimate plan, ~600 credits.)
- The image must SHOW the story: an object or scene a reader links to the news at a glance
  (hourglass for "2 weeks", shopping bags for Black Friday, reshuffling result cards for a ranking update).
- Painterly / editorial, warm light, hand-painted texture. Always end the prompt with
  "No text, no letters, no logos". Never draw a company's real logo or product UI; real logos come from the company's own site.
- Composition is part of the prompt: Slide A/B → "subject on the right third, the left half is a calm,
  softly blurred field". Slide C → abstract aura, no objects. Cover → subject filling the frame.
- `sips -s format jpeg -s formatOptions 88 -Z 2000`, then upload with `upload_assets` (no nodeIds) → POST bytes → keep `imageHash`
  → delete the auto-created frames → set `image.fills=[{type:'IMAGE',scaleMode:'FILL',imageHash}]`.

**Type rules:** Mulish only. No Azeret Mono or other monospace text anywhere (labels, footer, email). The footer
`euribiadigital.com` is Mulish SemiBold 24, ink, left at x=80. No em-dashes in copy. No single orphan word on the last line.

**First build on the template:** `Core Update · Cover/01/02/03/CTA` in Results, row y=32500 (Google November 2026 core update).
PNGs: `~/Documents/01-Euribia/posts/<YYYY-MM-DD>-<slug>/` (01–05.png + caption.txt).

---

# ★ v2 NEWS TEMPLATE — THE DEFAULT (use this, not the old one)

Modern editorial system: paper surface, oversized headline, the image as a **contained block**
rather than a full-bleed photo behind text. Everything sits on one grid. Adopted 02.09.2026.

## Where the masters live
Page **Posts** `0:1`, section **Reference** `10:162`:

| Set | Frames (left → right) |
|---|---|
| Carousel 1080×1350 @ y≈6900 | `v2 News Cover` · `v2 News Slide 1-3` · `v2 News Back` |
| Story 1080×1920 @ y≈8900 | `v2 Story Cover` · `v2 Story Slide 1-3` · `v2 Story Back` |

Duplicate these into **Results** `11:133`. Never edit the masters unless changing the template itself.

## The grid (identical in both formats)
- Margin **80**, content width **920**. Nothing crosses these.
- **Eyebrow row** — Azeret Mono Medium 20, ls 2.6, UPPER, muted. Left = section or slide number
  (`Новини`, `01`); right = subject/date, or the subject's logo. Hairline directly under it
  (carousel y=136 · story y=162).
- **Footer** — hairline (carousel y=1216 · story y=1780), Euribia logo left at 34px tall,
  `euribiadigital.com` right in mono 18, purple accent dot 9px at the far right.
- Palette: paper `#f7f7f5`, ink `#0d0d0d`, body `#3a3a38`, muted `#8a8a86`, hairline `#d8d8d4`,
  dark hairline `#2b2b2b`, accent `#bf40ff`. Covers/slides are paper; the back cover is ink.

## Named layers — set content by NAME, never by node id
`eyebrow-left` · `eyebrow-right` · `headline-1..N` · `heading` · `body` · `image` ·
`rule-top` · `rule-bottom` · `accent-dot` · `accent-rule` · `cta-email` · `euribia logo`

## Headline rule (the one that breaks if you skip it)
Headlines are **one uniform size, left aligned, ragged right** — NOT stretched to equal widths like
the old template. Each line is its own node; a line must never wrap.

    1. one node per line, textAutoResize = WIDTH_AND_HEIGHT, fontSize = max
    2. set characters, measure every node, keep the WIDEST width
    3. if widest > 920 → size = floor(max * 920 / widest), clamped to min
    4. apply that ONE size to all lines, stack by round(size * lineHeight/100)

Sizes: cover max **112** (min 56, lh 94, ls −3.2) · slide heading max **76** carousel / **80** story
(min 44, lh 98, ls −2) · back cover max **104** (min 50).
Skipping the measure step is what pushed a headline into the image block on the first build.

## Flow rules
- Cover: the image block starts at `headline.bottom + 42` (story +60) and runs to the footer
  margin — so a longer headline shrinks the image, never overlaps it.
- Slide: body starts at `heading.bottom + 34`. Image block is fixed (carousel y=176 h=496 ·
  story y=220 h=800), radius 10.
- Back cover: accent rule at `headline.bottom + 46`, email at `+96`.

## The `image` placeholder is a FRAME, not a rectangle
Every image slot is a **FRAME** named `image`, `clipsContent = true`, cornerRadius 10, with the photo
as its fill. That is deliberate: the designer can drag a picture straight onto it in Figma and it
replaces/clips without any resizing fuss. Keep it a frame — if you rebuild the template, do not
regress it to a rectangle.

Carousel: cover block flows under the headline; slides fixed at y=176 h=496.
Story: cover block flows; slides fixed at y=220 h=800.

## Data graphics
Draw them INSIDE the `image` frame as its CHILDREN, with coordinates relative to the frame
(subtract the block's x/y). The block is clean and ungraded, so the old "safe zone" limit no longer
applies. Set the block fill to `#fbfbf9` and the graphic reads as a white data card.

## Painterly background on slides
Slides carry a full-bleed painterly background image as the FRAME fill; the cover stays on paper so
the hero image leads. Master asset: `assets/brand/bg-painterly-yellow-blue.jpg`.

⚠️ **Retune the chrome whenever a slide sits on colour.** The muted greys are tuned for paper and
disappear over yellow. On any coloured slide set:
- `eyebrow-left` · `eyebrow-right` · `footer-url` → ink `#0d0d0d` at opacity **0.62**
- `rule-top` · `rule-bottom` → ink `#0d0d0d` at opacity **0.20**
Headline and body stay solid ink; the white data card carries its own contrast.

## Third-party logo
Place the subject's real wordmark in the eyebrow row, right-aligned to x = 80+920−width, and blank
the `eyebrow-right` text. See the third-party logo notes further down for the SVG import gotcha.

---

## LEGACY — the original News template (scrim + dark card)
Kept for reference only. Do not start new posts from it.

## The News template (what to copy)
Two formats — build BOTH every time:
- **Carousel** 1080×1350: `News Cover` `10:81` → `Slide 1` `10:106` → `Slide 2` `11:97` → `Slide 3` `11:102` → `News Back cover` `11:107`
- **Story** 1080×1920: `News Cover` `10:216` → `Slide 1` `10:241` → `Slide 2`/`3` (IDs drift — find story `News Slide` frames ≥1800px tall by name) → `Back cover` `11:72`

Per-frame layers (map BY NAME after duplicating — node IDs change on copy):
- Cover: image placeholder `image 43`; black `Legibility Scrim` (bottom gradient); centered logo at TOP; 3 headline text lines.
- Slides: image placeholder `hf_...`; white/dark card `Rectangle 912`; heading text; body text.
- Back cover: centered logo (upper); heading text; `Cover CTA` email text. NO image.
- **NO accents.** The old `Vector 2/3/4` shapes were removed from the template — do not re-add them.

## Pipeline (every time)

> **Image source:** do NOT assume Higgsfield. Walk the IMAGE SOURCE LADDER in `ENGINE_RULES.md` §8 (real photo → **Magnific** → Higgsfield → native Figma art) and say in the report which rung produced the visuals. Magnific is the preferred generator when its plan is live — verify with a cheap `images_models_list` before writing prompts.

1. **Read** design system + whole Figma file.
2. **Photos in:** HEIC (iPhone) → `sips -s format jpeg in.heic --out out.jpg`; downsize `sips -Z 2400 -s formatOptions 85`. Figma takes PNG/JPG/GIF/WebP, ≤10MB.
3. **Duplicate** the 5 carousel + 5 story frames into **Results**, two rows, ~150px gaps. 
   - **CRITICAL — right page + right parent.** `frame.clone()` lands on `figma.currentPage`, often NOT Posts. Always `await figma.setCurrentPageAsync(<Posts 0:1>)`, then `section.appendChild(frame)` into Results (`11:133`) and set `frame.x/frame.y` relative to the section. Verify parent chain `FRAME < SECTION(11:133) < PAGE(0:1)` before reporting. Stack new posts BELOW existing (cols rel x 247,1477,2707,3937,5167).
4. **Copy + layout standard** (see below): set text, then apply the cover / slide / back-cover layout.
5. **Place photos** (working method below) — VERIFY by screenshot.
6. **Verify** EVERY frame by screenshot before reporting. Never trust a tool/agent "success" — look at it.

## LAYOUT STANDARD (LOCKED — match this every time)
**ALL HEADLINES ARE UPPERCASE** — set `node.textCase = 'UPPER'` on every cover line, slide heading, and back-cover heading (NOT the body paragraphs, NOT the email). Apply UPPER BEFORE the full-width scaling below, because uppercase is wider and changes the measured width.

**Full-width line scaling** (used on cover + back-cover headlines): split the headline into separate one-line text nodes (clone the base node). For each line (ROBUST order — the naive way leaves the box fixed-width and the text wraps):
1. `n.textAlignHorizontal=...; n.lineHeight={value:100,unit:'PERCENT'}; n.textCase='UPPER';`
2. `n.textAutoResize='NONE'; n.resize(3200,240);` (wide box so nothing wraps)
3. `n.fontSize=120; n.characters=<line>;`
4. `n.textAutoResize='WIDTH_AND_HEIGHT';` (now the box hugs the text)
5. measure `n.width`; `size=size*(target/n.width)`; set; measure+repeat once. Cap ≈185–205.
Result: every line is the SAME width (edges align). Stack tight (gap ≈4). Cover target ≈980 CENTER; back-cover target ≈860 LEFT (x=80). Carousel-photo source for the demo = Pictures/**Meta** `16OPeCUgrH41mGlkZEm6S7aRtA2b0nd1X`.
**Figma text auto-height is unreliable** — for any multi-line body/caption, set `textAutoResize='NONE'` + a FIXED estimated height, then position what's below by `node.y + height + gap` (don't trust `.height` right after setting characters).

- **COVER** — logo centered, positioned DIRECTLY ABOVE the headline (gap ≈40), NOT at the frame top. Headline = 3 lines, **centered**, full-width-scaled (target ≈980), stacked to FILL the bottom band over the scrim. (Set the headline first, then place the logo just above its top line.) The headline must fill the page — you MAY add/rephrase words to achieve the fill (user-sanctioned). Keep the black `Legibility Scrim` (linear gradient transparent→~0.85 black over the bottom ~56%) for text legibility — it is NOT a colored accent.
- **SLIDES** — photo top; heading + body bottom-aligned as a tight block on the dark card. Headings get **balanced manual line breaks** — never leave a short word alone on a line; reduce size to fit cleanly. Body right under the heading (gap ≈34).
- **BACK COVER** — black, no photo. Logo centered, UPPER (y≈300 carousel / 450 story). Heading = full-width-scaled lines, **left-anchored at x=80** (target ≈860), placed in the upper-middle (headY ≈470 carousel / 700 story). Email `Пиши ни: sales@euribiadigital.com` left-aligned at x=80, right below the heading. The group sits in the upper half; bottom half stays empty.

## Placing a photo into a placeholder (THE WORKING METHOD)
`upload_assets` with a `nodeId` UPLOADS the image but its **placement silently fails** (`commit` → `"Failed to place assets"`; node keeps old fill). So:
1. `upload_assets` (count 1, target nodeId) → POST the JPG bytes to the submitUrl → **capture the `imageHash`** (blob commits even though placement fails).
2. Set the fill via `use_figma`: `node.fills = [{ type:'IMAGE', scaleMode:'FILL', imageHash:'<hash>' }]`.
3. Screenshot to CONFIRM. Reuse hashes across matching carousel+story frames; an already-uploaded hash stays in the file's blob store.

## Text rules
- **No overlapping** text/elements — check every frame visually.
- **No single short word alone on a line**, no mid-word hyphenation — adjust size / line breaks until lines break between whole words.
- Bulgarian copy used EXACTLY as supplied (no paraphrase, no added em-dashes) — EXCEPT cover headlines, where you may add/rephrase words to fill the frame.
- Setting characters / fontSize / lineHeight / textAutoResize requires the font loaded first: `for (const f of node.getRangeAllFontNames(0, node.characters.length)) await figma.loadFontAsync(f)`. A thrown error rolls back the WHOLE use_figma call — keep deletes separate from font ops.

## Brand lock
Mulish + Azeret Mono, purple/black/white, real euribia logo. No accent shapes. Recolor nothing except via the locked standard; never distort the logo.

## DATA GRAPHICS in the image band (informative slides)

When a slide should carry information rather than mood, build the graphic natively instead of
generating it — AI models render numbers and labels unreliably, and these need exact figures.

- **Safe zone: the top ~70% of the image band only.** Below that the frame fades toward the dark
  card and any label there becomes unreadable. Compute `SAFE = bandH * 0.70` and keep every element
  above it — including axis labels, which is where this first went wrong.
- Set the placeholder fill to flat paper `#f7f7f5`, then insert `viz_*` layers above it.
- Palette: ink `#0d0d0d`, muted `#8a8a86`, hairline `#d2d2ce`. Azeret Mono for figures and labels.
- Patterns that worked: code grid with one item highlighted in a dark pill; descending bar chart with
  the value above each bar and the period above that; empty metrics table with em-dashes for "no data".

## Third-party logos (editorial use)

Fetch the real asset — never hand-draw a trademark. `openai.com/favicon.svg` is the blossom mark and
the site header carries the wordmark path (viewBox `0 0 292 78`). Prefer the **wordmark**: legible at
small sizes and unambiguous.

⚠️ An SVG uploaded via `upload_assets` imports as a **FRAME wrapping a VECTOR**. Colouring every node
with `"fills" in n` paints the wrapper too and you get a solid rectangle. Clear the wrapper
(`frame.fills = []`) and paint only `type === "VECTOR"` children.

Placement convention: subject brand at the TOP, Euribia at the BOTTOM as publisher. Keeps the piece
clearly ours and avoids implying endorsement.

## UI mockups instead of flat charts (preferred for informative slides)

A slide reads far better as a **fragment of real product UI** than as a bare chart. Build it inside
the `image` frame as children, using this kit:

**Window chrome** (every mockup): a `#f6f6f4` bar 66px tall with a 1px `#ededea` bottom rule, three
10px traffic-light dots at x=26/44/62, a SemiBold 19 title at x=96, and an optional mono label
right-aligned. It is what makes the graphic read as a screen rather than a diagram.

**Kit tokens:** card `#ffffff` · well `#f6f6f4` · hairline `#ededea` · ink `#0d0d0d` ·
sub `#6f6f6b` · muted `#a3a39e` · success `#0f9d58` on `#e8f5ee` · highlight row `#f4e9ff`.
Radius 10–16. Mulish for labels, Azeret Mono for codes and figures.

**Three patterns that worked (OpenAI Ads post, 02.09.2026):**
1. **Availability table** — rows of name + mono country code + green `Available` pill, with the row
   that matters tinted lilac and set ExtraBold. Instantly shows both scale and the specific fact.
2. **Settings panel** — a big Black-weight value with a status pill beside it, then a change-history
   list underneath where superseded values are **struck through**. The strike does the storytelling.
3. **Empty dashboard** — a row of metric tiles all showing an em-dash, then a bordered chart area with
   a dashed baseline and a centred "no data" line. Says "nothing to compare against" better than prose.

**Fill the card.** Count rows against the block height rather than hardcoding: `rh = (H − bar − pad) / rows`.
Four rows in a 496px block leaves a dead band at the bottom; five fills it. Story blocks (800px) take
one or two more rows than carousel blocks (496px) — same code, different count.

**Em-dashes need weight.** `#c9c9c4` disappears at feed size; `#9a9a95` reads.

## ★ AURA + GLASS style (adopted 02.09.2026 — preferred over flat UI mockups)

The OpenAI-announcement look: painterly field, ONE giant white figure, a frosted-glass UI card
floating over it. Built inside the `image` frame; carries the same real facts, reads instantly.

**The three layers:**
1. **Field** — painterly canvas as the frame's IMAGE fill. Library: `brand/bg-painterly-yellow-blue.jpg`
   (blue/yellow), `bg-painterly-gold.jpg` (gold swirl), `bg-painterly-aura.jpg` (pastel bloom).
   Generate more with Magnific `imagen-nano-banana-2-flash`, prompt "painterly abstract background,
   hand-painted canvas texture: …, no text, no objects". ⚠️ Gold-type renders can include a painted
   canvas border — center-crop ~7% (`sips -c`) before upload.
2. **Giant figure** — ONE fact as huge white Mulish Black ("52", "$0"), soft shadow
   (y8 r26 a0.18), mono UPPER label under it with a crisp shadow (y2 r8 a0.38) or it drowns
   in light areas. Size so it CLEARS the card: measure `big.width`, keep `x+width < card.x`
   — at 300px "$0" overlapped the story card, 250px cleared it.
3. **Glass card** — white fill **a0.76–0.85**, cornerRadius 22, stroke white a0.7,
   effects `BACKGROUND_BLUR 32` + warm `DROP_SHADOW y16 r38 a0.24`. No window chrome — chromeless.
   Content patterns: model-picker rows with a RADIO (ring+dot, no ✓ glyph — Mulish may lack it) and
   a black TOGGLE pill; settings card with struck-through superseded values; empty-state card with
   em-dash metrics (dash color ≥ `#82827d`).

**Tick ring** (empty-state slides): dashed-stroke ellipse — `dashPattern [3,17]`, ink a0.42 — NOT
individual rotated rects. ⚠️ Ring radius must EXCEED the card's half-diagonal
(√((w/2)²+(h/2)²)), else it hides entirely behind the card. 560×196 card → r≥310.
