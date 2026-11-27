# CONTENTO ENGINE RULES — read this before ANY contento work

This is the reliability layer. The playbooks say *what* to build; this says *how not to break it*.
Every silent-failure mode we have hit is listed here with its exact fix. **If a rule here conflicts
with any other contento doc, this file wins.**

---

## 1. EXECUTION MODEL (the rule that was contradicting itself)

**Build in the MAIN thread. Delegate only thinking, never making.**

Sub-agents have **no Bash tool**. Every image path in this system needs Bash
(`curl` to POST image bytes, `sips` to convert HEIC). So a sub-agent that "places an image"
reports success and produces an empty frame. This was the single biggest source of broken runs.

| Work | Who |
|---|---|
| Figma builds (clone, text, image fills, screenshots) | **MAIN thread** |
| Wix draft creation + media upload | **MAIN thread** |
| Drive downloads, `sips`, `curl` | **MAIN thread** |
| Fact-finding with sources | `contento-research` sub-agent (safe — no Bash needed) |
| Copy multiplication / directions | `contento-content` sub-agent (safe) |
| Anything else | **MAIN thread** |

Sub-agents may be dispatched **in parallel with** main-thread building (research runs while you
clone frames), never **instead of** it. If a sub-agent returns "image placed" — do not believe it;
verify or redo it yourself.

---

## 2. PREFLIGHT (run before every build, especially unattended)

1. **Figma reachable** — `get_metadata` on the target page. If it errors, STOP and report; do not
   half-build.
2. **Right page is current** — `await figma.setCurrentPageAsync(<target page>)`. `clone()` and
   `createFrame()` land on `figma.currentPage`, which is frequently NOT the page you want.
3. **Ledger read** — `state/ledger.json`. Never repeat a topic or reuse a photo already logged.
4. **Fonts** — Mulish + Azeret Mono must load. Load per node:
   `for (const f of n.getRangeAllFontNames(0, n.characters.length)) await figma.loadFontAsync(f)`.
5. **Assets present** — if the run needs photos, confirm the source folder actually returned files
   before cloning frames. Empty inbox → switch to the generated-image fallback (§6), don't proceed
   with empty placeholders.

---

## 3. THE SILENT-FAILURE CATALOG (memorise these five)

### 3.1 `upload_assets` placement silently fails
`upload_assets` with a `nodeId` uploads the blob but the placement step fails
(`commit` → `"Failed to place assets"`) while the node keeps its old fill — **and the tool still
reads as success.**
**Fix (the only method that works):**
1. `upload_assets` (count 1, target nodeId) → POST the bytes to the returned `submitUrl` with Bash
   `curl -F file=@x.jpg '<submitUrl>'` → **capture the `imageHash`** (the blob commits even though
   placement failed).
2. Set the fill through `use_figma`:
   `node.fills = [{ type:'IMAGE', scaleMode:'FILL', imageHash:'<hash>' }]`
3. **Screenshot to confirm.** Reuse the same hash across matching carousel/story frames.

### 3.2 Clone lands on the wrong page / wrong parent
`frame.clone()` attaches to `figma.currentPage`. Always:
`setCurrentPageAsync(page)` → `section.appendChild(frame)` → set `frame.x/frame.y` **relative to the
section** → verify the chain `FRAME < SECTION < PAGE` before reporting.

### 3.3 Node IDs remap on commit
IDs shift (e.g. `120:*` → `81:*`). If `getNodeByIdAsync` returns null, **find by name or by
`characters`** via `page.findAll`. Never hard-code an ID you got earlier in the same run without a
null check.

### 3.4 Figma text auto-height is unreliable
`textAutoResize='HEIGHT'` often leaves `.height` at the stale value, so anything positioned by
`node.y + node.height` lands on top of the text.
**Fix:** for multi-line body copy set `textAutoResize='NONE'` and a **fixed estimated height**, then
position the next element from that number.

### 3.5 A thrown error rolls back the ENTIRE `use_figma` call
One bad font load undoes the whole batch, including work that succeeded. Keep deletes separate from
font ops; wrap risky work in try/catch; build in small committed steps rather than one mega-call.

### 3.6 Bonus — page-scan timeout
Scanning a whole large page with `use_figma` can time out. Target sections/frames by ID, not
`page.findAll` over everything, on big files.

---

## 4. THE VERIFICATION GATE (non-negotiable)

**Nothing is "done" until it has been looked at.** A tool returning success is not evidence.

Before reporting any build:
- [ ] `get_screenshot` on **every single frame** produced — not a sample, not the page thumbnail.
- [ ] Every image placeholder shows a real photo (not grey, not the old fill).
- [ ] No text overlaps another element.
- [ ] No line ends in a single orphan word; no mid-word hyphenation.
- [ ] Headlines are UPPERCASE where the locked style requires it, and full-width lines really are
      equal width.
- [ ] Parent chain verified (§3.2).
- [ ] Bulgarian reads natively — not translationese. Clichés cut.

If a check fails: fix it and re-screenshot. Do **not** report with a caveat like "the image may not
have applied" — go and look.

---

## 5. BULGARIAN VOICE GATE

Every piece of copy passes this before it ships:
- Written **as a Bulgarian writes**, not as a translation of English marketing copy.
- **No em-dashes ANYWHERE in Euribia copy — authored or supplied.** Dimitar, 02.09.2026: „the long
  dashes make it look AI written". Use a colon, a comma, or a new sentence instead. Numeric ranges
  are written with words („от $25 до $45"). If the user supplied exact Bulgarian text, it is used
  **verbatim** — the only exception is cover headlines, where words may be added/rephrased to fill
  the frame (user-sanctioned).
- At least **one human imprint per piece**: a real number, a clear opinion, or a concrete example.
- Banned openers: "В днешния дигитален свят", "Не е тайна, че", "В забързаното ежедневие", and any
  sentence that could open any agency's post.

---

## 6. FALLBACKS (so an unattended run never stalls silently)

| Failure | Fallback |
|---|---|
| Photo inbox empty / no new photos | Walk the IMAGE SOURCE LADDER in §8. Always note in the report which rung produced the visuals. |
| News radar returns nothing usable | Fall back to the next evergreen pillar (`state/PILLARS.md`). Never skip the run. |
| Higgsfield returns a white-padded image | Check edge pixels (middle row L/R, middle col T/B). If RGB all >245, crop the white band with a small margin, keep a `*_padded.png` backup, re-verify edges. |
| Wix media import fails on a HEIC/Drive URL (400) | `sips` HEIC→JPG → host via Higgsfield `media_upload` + `curl -X PUT --data-binary` → use the returned cloudfront URL as `download_url` for `UploadImageToWixSite`. |
| Figma unreachable | Abort the visual half, still produce the copy + the article draft, and report clearly what did not get built. |
| PostFlow token missing / 401 | Delivery-only failure. Ship the Figma frames + caption as usual and put „PostFlow: не е доставено" in the first two lines of the report. Never retry blindly against auth errors. |
| Blog verification gate fails on any item | Do NOT publish. Leave the Wix draft, name the failed item in the first two lines. A held article beats a wrong live one. |
| A live article needs a fix | `PATCH` the draft → re-publish (`/publish` updates the existing post). Never delete and re-create — the URL and any shares die with it. |
| Any step fails twice | Stop that deliverable, finish the others, and report the failure explicitly. **Never report a partial build as complete.** |

---

## 7. UNATTENDED-RUN CONTRACT (scheduled tasks)

- **Destination is per-deliverable — know which one you are running.**
  - **Posts:** Figma Results section → **PostFlow DRAFT** assigned to Dimitar (`POSTFLOW.md`).
    The engine never publishes to a social channel; `isPublishNow` stays false, always.
  - **Blog:** created as a Wix draft, then **published live** on euribiadigital.com — but only
    after the `ARTICLES_PLAYBOOK.md` verification gate passes in full. A failed gate holds it as a
    draft and says so in the first two lines of the report. Never publish an unverified article,
    and never delete a published one to fix it — patch the draft and re-publish.
- **Always write to the ledger** (`state/ledger.json`) at the end of a run: topic, type, date,
  source, links, photos consumed. The next run reads it to avoid repeats.
- **Always notify** via `PushNotification` with a one-line result, then leave a full report.
- **Report honestly.** If two of three frames worked, say that. A scheduled run that lies is worse
  than one that fails.

---

## 8. IMAGE SOURCE LADDER (try in this order, report which rung you used)

Never assume a generator is available — they fail for *account* reasons, not just transient ones,
and both failed on 2026-09-02 in the same run. Check, then fall through.

| # | Source | How to call | Known failure |
|---|---|---|---|
| 1 | **Real photos** — Drive inbox / `assets/` | `search_files` → `curl` → `sips` | Inbox empty; photo already in `ledger.used_photos` |
| 2 | **Magnific** | `images_generate` (server `c5b95154…`), then `creations_wait` → `creations_get` for the URL | **`Magnific MCP requires a premium account`** — returned by EVERY tool on that server, including the read-only `images_models_list`. That is a PLAN gate, not credits: nothing you can retry around. |
| 3 | **Higgsfield** | `generate_image_batch` → `jobs_wait` → `show_generation_by_ids` | **`Out of credits on <plan> in Private workspace`** — top up at higgsfield.ai |
| 4 | **Native Figma art** | build gradient fills + blurred shapes in `use_figma` | none — always available, needs no account |

**Rung 2 — Magnific specifics.** Preferred generator when the plan allows it: better photoreal output
than rung 3 and it takes a `brandKitId` so brand palette/logo/typography are applied automatically
(when a kit exists — do NOT restate brand identity in the prompt when using one). Model choice:
leave `mode` at `auto` unless a specific model is wanted. Chain image→anything by passing the
returned creation `identifier`, never the `webUrl`. Confirm the plan is live with a cheap
`images_models_list` BEFORE writing prompts — it fails instantly and saves the wasted prompt work.

**Rung 4 — native Figma art** is a legitimate deliverable, not a stub. Recipe that worked:
stack 2 gradient fills on the placeholder (a base linear for the field + a radial for the glow),
then insert blurred (`LAYER_BLUR` 30–70) rectangles/ellipses directly above it in z-order to give
the composition structure — beams, bands, converging rays, rising dots. Give each slide its OWN
motif so the set does not read as one repeated blob. **Compute the visible band from the image
placeholder's own extent (`ph.y + ph.height`), NOT from where the dark card starts** — the
placeholder sits ABOVE the card, so using the card top confines the art to the wrong region.

**Whichever rung you land on, say so in the report.** "Images are native Figma art because both
generators were account-blocked" is a fine outcome; silently shipping it as if it were photography
is not.
