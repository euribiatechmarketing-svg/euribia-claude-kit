# Euribia ARTICLES playbook (Wix blog, euribiadigital.com)

The repeatable process for a Euribia article. Read this **and** `ENGINE_RULES.md` before any blog
work. Same reliability rules as Posts; different target.

## Target (LOCKED — do not re-derive these)
- **Wix site:** the site named **"Digital"** = **euribiadigital.com** —
  `siteId 02bdf931-3165-4e4b-b0f8-008f1d1cdf0a`.
  ⚠️ NOT the site named "Euribia Digital" (`88206d7a…`) — that one is euribiatech.com.
- **Multilingual**: en primary, bg secondary → set `language:'bg'`. BG posts live at `/bg/post/...`.
- **Author:** Dimitar Zafirov — `memberId 9aab3157-5799-48ae-bcdf-550ae89d50a0` (per-site id).
- **Mode: AUTO-PUBLISH, gated.** The draft is created first, checked against the verification gate
  at the bottom of this file, and then published with
  `POST /blog/v3/draft-posts/{draftPostId}/publish` → `{postId}`.
  A draft that fails any gate item is **held as a draft** and reported loudly — never published "anyway".
- ⚠️ **A BG draft is invisible in the Wix dashboard unless the language toggle is set to Bulgarian**
  (default view is English → BG drafts look "missing"). Always say this in the handoff message.

## Pipeline
1. **Topic** — from `TOPIC_ENGINE.md` (override queue → news ↔ pillar alternation). Check the ledger.
2. **Research** — if the piece makes any factual claim, dispatch `contento-research` for stats with
   sources. Never invent a number or a citation.
3. **Write** — Bulgarian, Euribia voice, SEO-structured: title (H1), slug, meta description ~150
   chars, scannable H2/H3, short paragraphs, one clear takeaway + CTA.
   Passes the **Bulgarian voice gate** in `ENGINE_RULES.md` §5.
   Length: **900–1400 words** — enough to rank, short enough to finish.
4. **Image** — user's choice per article; default for scheduled runs = **Higgsfield generated**

> **Image source:** do NOT assume Higgsfield. Walk the IMAGE SOURCE LADDER in `ENGINE_RULES.md` §8 (real photo → **Magnific** → Higgsfield → native Figma art) and say in the report which rung produced the visuals. Magnific is the preferred generator when its plan is live — verify with a cheap `images_models_list` before writing prompts.

   (on-brand: purple/violet, clean, modern, minimal, no stock clutter, no text, no logos).
   Real-photo source when asked: Drive `Articles` folder `1Fh8Mpti9mAkLV296gUHH2ncXi-wSNqJW`.
5. **Image → Wix Media** (need a Wix `file.id`):
   - **From a URL** (Higgsfield): `POST https://www.wixapis.com/site-media/v1/files/import`
     with `{url, mediaType:"IMAGE", displayName}` → `file.id` (bare id, no `wix:image://` prefix).
     `operationStatus:"PENDING"` is usable immediately.
   - **From a local file** (Drive photo): `UploadImageToWixSite`.
   - **HEIC gotcha:** a Drive HEIC URL → `UploadImageToWixSite` = **400**. Fix: `sips` HEIC→JPG →
     Higgsfield `media_upload` → `curl -X PUT -H 'Content-Type: image/jpeg' --data-binary @x.jpg
     '<upload_url>'` → use the returned cloudfront `url` as `download_url`.
6. **Create the draft (staging):** `POST https://www.wixapis.com/blog/v3/draft-posts?fieldsets=URL`
   ```
   { draftPost: { title, excerpt, memberId:"9aab3157-5799-48ae-bcdf-550ae89d50a0",
     language:"bg", richContent:<Ricos JSON>,
     media:{ wixMedia:{ image:{ id:"<fileId>" } }, displayed:true, custom:true } } }
   ```
   **Omit `publish` here** — creation is staging, so the gate can run before anything is public.
   Response `url` = `{base, path}` → URL = `https://www.euribiadigital.com/bg` + path.
7. **Publish (gate passed):** `POST https://www.wixapis.com/blog/v3/draft-posts/{draftPostId}/publish`
   → `{postId}`. Then confirm the live article loads at its public URL, in BG, with its cover image.
   `?publish=true` on creation exists but is **not** used — it skips the gate.
8. **Report** — title, meta, slug, **live URL**, image, post id. If the gate held it as a draft, say so
   in the first two lines and add the "switch the dashboard to Bulgarian" note.

## ★ COVER SYSTEM (locked 12.11.2026, v3): real photo + UI cards with real text
History: v1 lilac 3D dioramas were rejected ("AI-generated, too much lilac, all the same, cartoonish"). v2 plain photos were rejected ("too generic").
v3 = Dimitar: "It can be UI elements with text as well."
A cover is a **real photo background** (blurred and dimmed) with **2–3 product-style UI cards** in front. The cards show the article's
real facts in Bulgarian. They are rendered from HTML, so every letter is correct (never AI-drawn text).
Sample + example spec: `~/Documents/01-Euribia/Website/euribiadigital-blog/cover-system-2026-11-12/cover-v3-*`.

**1. Pick the facts:** the 3–6 most concrete facts of the article (dates, numbers, names, a status) → 2–3 cards + optional chip.
Card types in `blog_cover_ui.py`: `status` (label/value rows, coloured state dots or pills), `ranking` (list with ▲/▼ deltas),
`metric` (one big number), `bars` (small bar chart), `chat` (question + AI answer), `notice` (app notification), `chip`.
Real facts only. Illustrative rows (e.g. example domains in a ranking) must read as examples ("твоят-магазин.bg", "конкурент-1.bg"), never as real brands or invented statistics.

**2. Background photo:** a real scene that fits the topic (e.g. a person working on a laptop for SEO, a shop counter for e-commerce, a phone in hand for social).
- First choice: Magnific `stock_search` with `content_type:"photo"`, `ai_generated:"excluded"`, `orientation:"landscape"` (free ≈40 credits) → `stock_download`.
- Fallback: Magnific `imagen-nano-banana-2-1`, 16:9, 2k, "Real photograph, …". Text on screens doesn't matter because the background gets blurred.
- The photo sets the colours, so they change with each topic. No lilac brand tint.

**3. Render:** write a spec JSON (see the example) → `python3 ~/.claude/contento/tools/blog_cover_ui.py spec.json cover.jpg --preview`
→ 2752×1536 with the real `euribia digital` logo top-right. Keep all cards inside x 220–1150 of the 1376×768 canvas (the `/blog` grid crops to 4:3).
Default `bg_blur` 5, `bg_dim` 0.3, `scale` 1.15.

**4. Check by eye** `cover.jpg` AND `cover_grid.jpg`: no card covering another card's text, nothing cut by the grid crop, no orphan words, Bulgarian reads naturally.

**5. Upload** the JPG (Higgsfield `media_upload` + `curl -X PUT` → cloudfront URL → Wix `files/import`). One file is both the cover and the first body image.
(`blog_cover.py` is the older photo-only compositor. Use it only if a plain photo cover is explicitly asked for.)

## Article FORMAT (LOCKED — matches the live blog)
1. **In-body hero IMAGE at the very top** — `IMAGE` node, CENTER,
   `containerData.width.size:"CONTENT"`, real `width`+`height`, `altText`.
   The same image is BOTH the cover (`media.displayed:true`) AND the first body node.
2. **Intro paragraph** — the hook, 1–2 sentences, no heading before it.
3. **H2 „Бързи факти"** + a `BULLETED_LIST` of **3** one-line takeaways.
4. **H2 sections** (level 2), each followed by short paragraphs. H3 for sub-points.
5. **H2 „Свържи се с нас"** + CTA paragraph mentioning `sales@euribiadigital.com`.
6. **Spacing:** an EMPTY paragraph `{type:'PARAGRAPH', nodes:[], paragraphData:{}}` AFTER every
   block (image, paragraph, heading, list). The live articles use these as air.
Optional tail: `DIVIDER` → H2 „Прочети следващото" → related post (image + H3 + teaser).

## Ricos rules (the ones that throw)
- Every TEXT node MUST sit inside a PARAGRAPH node.
- BLOCKQUOTE / LIST_ITEM contain PARAGRAPH → TEXT, never TEXT directly.
- Types in use: `PARAGRAPH`, `HEADING`, `IMAGE` (needs Wix media id + width + height),
  `ORDERED_LIST` / `BULLETED_LIST` + `LIST_ITEM`, `BLOCKQUOTE`, `DIVIDER`.
- Confirm shapes from the docs rather than guessing:
  https://dev.wix.com/docs/api-reference/business-solutions/blog/skills/how-to-create-blog-posts

## Tools
Connected Wix MCP: `ExecuteWixAPI` / `CallWixSiteAPI`, `UploadImageToWixSite`,
`SearchWixRESTDocumentation`, `ReadFullDocsArticle`. Pass the `siteId` for site-scoped calls.

## Verification gate (BEFORE publishing — this is what decides whether it goes live)
All boxes ticked → publish. Any box failing → stay a draft, report why. No partial credit.
- [ ] Draft exists and is retrievable by id.
- [ ] Cover image renders AND appears as the first body node.
- [ ] `language:'bg'`, author set, slug sane, meta ~150 chars.
- [ ] Preview URL opens.
- [ ] Voice gate passed (§5 of ENGINE_RULES) — no AI tells, ≥1 human imprint.
- [ ] Ledger updated (`post_id`, `live_url`, `published`).

## After publishing
- [ ] The public URL loads, in Bulgarian, cover image rendering.
- [ ] To correct a live article: `PATCH` the draft and re-publish. **Never delete** the published post.
