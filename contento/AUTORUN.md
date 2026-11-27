# CONTENTO AUTORUN — the unattended run

Followed by the scheduled tasks `contento-posts` (Tue & Thu — tech-news carousel) and `contento-blog` (Wed).
A scheduled run is a **fresh session with no memory of any conversation**. Everything it needs is in
these files. Read in this order:

1. `ENGINE_RULES.md` ← reliability layer, wins every conflict
2. `TOPIC_ENGINE.md` ← where the topic comes from
3. `EURIBIA_DESIGN_SYSTEM.md` ← brand
4. `POSTS_PLAYBOOK.md` (post runs) / `ARTICLES_PLAYBOOK.md` (blog runs)
5. `state/ledger.json` ← what already shipped

---

## RUN A — TECH-NEWS CAROUSEL (Tue & Thu)

**Deliverable:** 1 carousel (1080×1350, 5 frames) in the AURA+GLASS style, built in the Figma Posts
page Results section, **then delivered into PostFlow as a draft assigned to Dimitar for approval**
(`POSTFLOW.md`), plus the caption. Story only when Dimitar asks — the weekly deliverable is the
carousel alone.

1. **Preflight** — `ENGINE_RULES.md` §2. Read the ledger.
2. **Topic** — `TOPIC_ENGINE.md`: override queue first, else the tech/AI news radar. Pillar rotation
   is the fallback only when the radar is dry. News is a hook, never the payload — every post must
   answer „и какво значи това за твоя бизнес?".
3. **RESEARCH — mandatory for news.** Dispatch `contento-research` for verified facts with sources
   BEFORE writing copy. Check the actual date of the "news": if the event is months old, find the
   fresh angle (the OpenAI-ads post: the ads were 7 months old — the real news was that BULGARIA
   got self-serve access 2 days prior). No number goes on a slide without a source. If OpenAI/vendor
   states no benchmarks exist, say exactly that — it is a stronger slide than an invented average.
4. **Visual fields** — walk the IMAGE SOURCE LADDER (`ENGINE_RULES.md` §8). Painterly fields for
   the aura+glass style live in `assets/brand/bg-painterly-*.jpg`; generate a new field with
   Magnific (`imagen-nano-banana-2-flash`, ~75 credits, unlimited does NOT apply via MCP) when the
   topic wants a different mood — always relevant to the story, never generic.
5. **Copy** — natural Bulgarian, voice gate §5. Cover headline (3 lines) + 3 slides (heading +
   body) + back-cover CTA.
6. **Build** — MAIN thread, per `POSTS_PLAYBOOK.md`:
   - **Structural source: the NEWEST approved carousel row in Results** (the ledger's last `post`
     entry names its frame ids). Clone those 5 frames — that way every run inherits the latest
     approved layout automatically. Fall back to the v2 masters in Reference (`10:162`, y≈6900)
     only if Results has no approved row.
   - Strip everything post-specific from the clones: previous copy, previous card contents
     (`ui_*` children), the previous subject's wordmark. Keep layout, chrome, Euribia marks.
   - Slides = AURA+GLASS (see POSTS_PLAYBOOK): painterly field as the `image` frame fill, ONE giant
     white figure (the story's key number), frosted-glass card with the real detail (picker rows /
     settings with struck values / empty-state with dash metrics + tick rings outside the card).
   - Subject's logo: fetch the REAL asset from their site (wordmark preferred), never redraw;
     mind the SVG wrapper-fill gotcha in POSTS_PLAYBOOK.
   - Placement: `nextY = max(child.y + child.height) + 400` in Results `11:133`; columns
     247/1477/2707/3937/5167. Never hard-code a Y.
7. **Verify** — §4 gate. Screenshot **all 5 frames**. Giant figure must CLEAR the glass card;
   labels over light paint need their crisp shadow; ring radius > card half-diagonal.
8. **Caption** — Instagram/LinkedIn, Bulgarian, hashtags.
9. **Log** — ledger: date, type `post`, style `aura-glass`, topic, source, frame ids, fields used
   (+ any new field added to `assets/brand/` and the manifest), Magnific credits spent.
10. **Notify** — `PushNotification`: `✅ Contento: постът за <тема> е готов за преглед`. Then the
    full report: topic + source, the Bulgarian copy, screenshots, caption, what's left for Dimitar.

---

## RUN B — BLOG (Wed)

**Deliverable:** one **published** BG article on euribiadigital.com with an on-brand image —
published automatically once the `ARTICLES_PLAYBOOK.md` verification gate passes in full.

1. **Preflight** — Wix reachable, ledger read.
2. **Topic** — `TOPIC_ENGINE.md`. If Tuesday's post came from a topic worth going deep on, the blog
   may be its long-form reservoir — log both against the same topic id.
3. **Research** — dispatch `contento-research` if the piece makes factual claims. Sources required.
4. **Write + build the draft** — `ARTICLES_PLAYBOOK.md`, format LOCKED, 900–1400 words.
5. **Verify** — the gate at the bottom of `ARTICLES_PLAYBOOK.md`. This gate decides publication.
6. **Publish** — gate fully passed → `POST /blog/v3/draft-posts/{id}/publish`, then confirm the live
   URL loads. Any gate item failed → hold it as a draft and report why, in the first two lines.
7. **Log** — ledger: date, type `blog`, topic, source, slug, draft id, post id, live URL, published.
8. **Notify** — `PushNotification`: `✅ Contento: статията „<заглавие>" е публикувана` (or `⚠️ … е
   задържана като чернова`). The report carries the live link; if it was held, add the reminder that
   the Wix dashboard needs its language toggle set to Bulgarian to show BG drafts.

---

## HARD RULES FOR EVERY UNATTENDED RUN
- **Two different destinations, two different rules:**
  - **Posts → PostFlow DRAFT**, assigned to Dimitar. The engine never publishes to a social channel.
  - **Blog → LIVE on euribiadigital.com**, but only through the verification gate. Gate fails → the
    article stays a draft and the report says so. Never publish an unverified article.
- **No silent partial success.** If something failed, the report says so in the first two lines.
- **Always write the ledger**, even on a partial run — record what did ship.
- **Always notify**, success or failure.
- If the whole run is blocked (Figma down, no MCP auth), still produce the **copy** as a text
  deliverable so the slot isn't wasted, and say plainly what could not be built.
