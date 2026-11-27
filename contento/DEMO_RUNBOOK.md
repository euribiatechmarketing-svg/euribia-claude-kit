# DEMO RUNBOOK — autonomous "демо" workflow

When the user types **`демо`** (or „пусни демото"), run this END-TO-END in the MAIN thread, no stops, then present. Theme = the latest script in Drive. Build it like the clean run on 2026-06-09. Goal: fast, zero bugs.

## Folders (Drive)
- **Script:** `1ksAYAgxjWIK87TJ2UOAAm0Q_X8JDYS0o` — latest file = the topic (read with `read_file_content`).
- **Carousel photos:** Pictures/**Meta** `16OPeCUgrH41mGlkZEm6S7aRtA2b0nd1X`.
- **LinkedIn photo:** Pictures/**LinkedIn** `1r9r6n6PBIemtFrc7NcTBcQ0ZzNH-l0kS`.
- **Article photo:** **Articles/Pictures** `1tivaKNc37IEf9jverlVl1ahLtuNDkXDC`.
- Download any Drive file: `curl -sL "https://drive.google.com/uc?export=download&id=<id>" -o f.heic`; HEIC → `sips -s format jpeg`; web-optimize `sips -Z 2000 -s formatOptions 85`.

## Deliverables (build ALL, MAIN thread)
1. **Carousel + Story** — clone News template into Posts Results (`11:133`); photos from Meta; copy in NATURAL Bulgarian; per the locked style (no accents, UPPERCASE cover headline full-width + logo above, slides bottom + UPPERCASE headings, back cover full-width heading + `Пиши ни: sales@euribiadigital.com`). See POSTS_PLAYBOOK.
2. **2 ads × 3 sizes** — Higgsfield-generated (nano_banana_pro), 2 concepts × {9:16, 4:5, 1:1}, real euribia logo (clone `81:5016`) on top; into Ads Results (`11:4709`). See ADS_PLAYBOOK.
3. **LinkedIn post** — feed-card mockup on the Posts page; photo from Pictures/LinkedIn (face-crop the avatar); author **Димитър Зафиров, Head of Product and Design**; natural-BG caption on the topic.
4. **Article** — Wix DRAFT on euribiadigital.com (siteId `02bdf931-...`, member `9aab3157-...`, language bg), REAL photo from Articles/Pictures, locked article format (in-body hero + cover + „Бързи факти" + sections + CTA).

## Order (parallel where safe)
1. Read script → derive the one idea + the copy for every piece (natural Bulgarian).
2. **Kick off async:** submit the 6 Higgsfield ad generations; download+convert the Meta + Articles photos.
3. **Build carousel+story** (main thread) while ads render. Verify every frame by screenshot.
4. **Build LinkedIn** card. Verify.
5. **Ads:** poll Higgsfield → download → create 6 frames+logos → upload+fill → verify.
6. **Article:** create the Wix draft (image flow below). 
7. Present all + the blog preview link.

## CRITICAL technical recipes (these are the bug-fixes — follow exactly)
- **Image fill into Figma:** `upload_assets`(nodeId) → `curl -F file=@x.jpg <submitUrl>` → capture `imageHash` → `use_figma`: `node.fills=[{type:'IMAGE',scaleMode:'FILL',imageHash}]` → screenshot to confirm. NEVER trust upload_assets placement. (Sub-agents have no Bash → the orchestrator does ALL image fills.)
- **Wix article image (HEIC/Drive fails):** Drive HEIC URL → Wix = 400. Fix: download HEIC → `sips` to JPG → upload to a public host via Higgsfield: `media_upload`(filename, image/jpeg) → `curl -X PUT -H 'Content-Type: image/jpeg' --data-binary @x.jpg '<upload_url>'` → use the returned `url` (cloudfront) as `download_url` in `UploadImageToWixSite` → get the Wix media id → use as cover + in-body hero.
- **Figma text auto-height is unreliable** (`textAutoResize='HEIGHT'` often stays at the set value). For multi-line text (LinkedIn caption, article-less): set `textAutoResize='NONE'` and a FIXED estimated height (e.g. LinkedIn caption ≈740 at 26px/150%), then place the image below by `cap.y + height + gap`.
- **Full-width cover/back headline (per-line scaling):** for each line node — `textAutoResize='NONE'; n.resize(3200,240)` (wide, no wrap); set fontSize 120 + characters; THEN `textAutoResize='WIDTH_AND_HEIGHT'`; measure `n.width`; `size = size*(target/width)`, repeat once (cap ~185–205). Cover target ≈980 CENTER; back target ≈860 LEFT x80. Logo sits directly above the cover headline (`y = topLine.y - 40 - logo.height`).
- **Clone-lands-on-wrong-page:** always `await figma.setCurrentPageAsync(<target page>)` before clone/create; `appendChild` into the right Results section; verify the parent chain before reporting.
- **Node IDs remap on commit** (e.g. 120:* → 81:*): if `getNodeByIdAsync` returns null, find the node by name/characters via `page.findAll`.

## Voice
NATURAL, native Bulgarian everywhere — write like a Bulgarian marketer, not a translation. Cut clichés/AI phrasings. The user (author of personal posts) is Dimitar Zafirov, Head of Product and Design.
