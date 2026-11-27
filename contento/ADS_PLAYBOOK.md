# Euribia ADS playbook (promo/advertising posts)

The process for building Euribia **advertising creatives** in the OFFICIAL-EURIBIA brand. Read this **and** `EURIBIA_DESIGN_SYSTEM.md` before any Ads work. Same engine mechanics as `POSTS_PLAYBOOK.md`, different page + templates — BUT a different creative philosophy.

## Creative philosophy — ARTISTIC, Higgsfield-generated, variant-driven (unlike Posts/Articles)

> **Image source:** do NOT assume Higgsfield. Walk the IMAGE SOURCE LADDER in `ENGINE_RULES.md` §8 (real photo → **Magnific** → Higgsfield → native Figma art) and say in the report which rung produced the visuals. Magnific is the preferred generator when its plan is live — verify with a cheap `images_models_list` before writing prompts.

Ads are artistic and exploratory — **do NOT just fill the Reference template** (that reads as a copy). Instead:
- **Higgsfield generates the whole creative** (concept, scene, composition, graphic treatment, background) as a full-frame image in the target aspect ratio. Use Higgsfield for the idea, the elements, and the final art.
- **Only the TEXT and the real euribia LOGO stay editable** Figma layers on top — everything else is generated.
- **Brand spine is mandatory** in the generated art and the overlays: Euribia palette (deep violet/purple + black + white), brand fonts **Mulish** (display) + **Azeret Mono** (mono), and the **real euribia logo** (the asset, never generated).
- **Default 3–5 genuinely different variants** (different concept/composition/hook), labelled for A/B testing. Draw on strong real-world ads for inspiration; don't repeat one layout.
The Reference templates below are a **fallback / brand-placement reference only**, not the creative.

## Where everything lives
- **File:** `fwTWYozj0aTtlTMvKtVJRR`, page **"Ads"** (`3:5`). Read the whole page first.
- Sections on the Ads page:
  - **Reference** (`11:4346`) — the ad templates. Duplicate from them; don't edit unless changing the template.
  - **Tokens** (`11:4657`) — brand/logo tokens. Don't touch.
  - **Results** (`11:4709`) — OUTPUT target. Everything you build goes here.
- Photos: user's choice per ad — **Higgsfield generation** (on-brand, purple/violet) OR a **real photo** from the Drive `Pictures`/`Articles` folders. Ask if unspecified.

## The 3 ad templates (build the size(s) the user asks for)
- **`04 - 9:16`** `81:4959` — 1080×1920 (story / reel ad)
- **`04 - 4:5`** `81:5007` — 1080×1350 (feed ad — the default)
- **`04 - 1:1`** `81:5055` — 1080×1080 (square ad)

Per-template layers (map BY NAME after cloning — IDs change). For the 4:5 (`81:5007`): label `Нашият метод (бърз)` `81:5051`; big **stat** `300%` `81:5054`; **subline** `1 ДЕН СНИМКИ = 30 ДНИ CONTENT…` `81:5052`; `повече съдържание` `81:5053`; **CTA button** = `Rectangle 909` `81:5013` + text `Стартирай сега →` `81:5014`; **image placeholder** `image 48` `81:5015`; logo `81:5016`; bg card `Rectangle 907` `81:5012`; accent vectors `Group 699` `81:5008` (Vector 2/3/4). The 9:16 and 1:1 frames have the SAME named layers (e.g. 9:16 stat `81:5006`, CTA text `81:4969`, image `81:4970`; 1:1 stat `81:5099`, CTA text `81:5101`, image `81:5102`).

## Copy shape (a punchy STARTING template — vary it per variant)
- Small **label** (the offer/method).
- A big **stat / number** (the hook — e.g. `300%`, `30 дни`, `1 ден`).
- A one-line **subline** (what it means, 3 short benefit words).
- A short benefit phrase under the stat.
- **CTA button** text ending with ` →` (e.g. `Стартирай сега →`, `Пиши ни →`).
- Bulgarian, Euribia voice, UPPERCASE where the template uses it. The human imprint still applies.

## Build process (Higgsfield-first)
1. Read the design system (palette/fonts/logo) + the Ads page.
2. **Ideate** the concept + hook per variant (Bulgarian, Euribia voice); take inspiration from strong ads.
3. **Generate the creative with Higgsfield** (`generate_image` → poll `job_status`/`show_generations` for the URL) in the target aspect ratio (4:5 / 9:16 / 1:1). Prompt for the concept + **Euribia palette** (deep violet/purple, black, clean white) + premium modern ad look + **clear negative space** for the headline/CTA. Generate supporting elements too when useful.
4. **Place in Figma:** `figma.setCurrentPageAsync(<Ads 3:5>)`; create a frame at the aspect ratio in **Results `11:4709`** (`appendChild`, set x/y; verify chain `FRAME < SECTION(11:4709) < PAGE(3:5)`); fill it with the generated image via the WORKING method — `upload_assets` → POST bytes (Bash/curl; a sub-agent may lack Bash → the orchestrator finishes the fill) → capture `imageHash` → `node.fills=[{type:'IMAGE',scaleMode:'FILL',imageHash}]` via `use_figma` → screenshot ([[figma-image-fill-gotcha]]).
5. **Overlay editable layers** on top: headline/hook, subline, CTA as real Figma TEXT (load fonts first: `getRangeAllFontNames` → `loadFontAsync`; Mulish/Azeret Mono, brand colors) and the **real euribia logo** asset. Keep these editable; no overlap, no orphan-word wraps; add a subtle scrim only if needed for legibility over the art.
6. Verify EVERY variant by screenshot before reporting. Note what's editable (text + logo) vs generated (everything else).

## Brand lock
Mulish + Azeret Mono, purple/black/white, real euribia logo. The ad templates DO use the purple accent shapes (Group 699) — keep them. Don't distort the logo.
