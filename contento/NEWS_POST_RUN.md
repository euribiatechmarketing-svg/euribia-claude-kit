# Weekly News post: run brief (Agent OS schedule "News posts Euribiadigital")

One run = one Euribia news carousel (5 frames, 1080×1350) for euribiadigital, handed to Dimitar for review.
Read `ENGINE_RULES.md` first, then the **AURA NEWS TEMPLATE** section of `POSTS_PLAYBOOK.md`. Both win over this file on detail.

## Steps

1. **Pick the story.** Pull the last ~72h from the feeds in `TOPIC_ENGINE.md` (full browser User-Agent, count `<item>|<entry>`).
   Only AI, search, ads, social platforms, e-commerce. It must matter to a Bulgarian SME owner.
   Skip anything in `state/ledger.json` from the last 90 days.
2. **Verify facts at the primary source** (the company's own blog, help centre or status page). Every number on a slide
   needs a source URL. If a fact can't be confirmed, drop it. Never invent numbers.
3. **Write the copy in Bulgarian:** a cover headline (3 lines), 3 slides (2-line heading + body of no more than 3 sentences), and a CTA question.
   The news is the hook. The post answers "what does this mean for your business?". No em-dashes, no clichés.
4. **Generate 4 images that fit the story** (cover 4:3, slides 16:9) with Higgsfield `gpt_image_2_6` (batch).
   Fallback: Magnific `imagen-nano-banana-2-1`. Each image must show something a reader links to this story.
   Follow the composition rules in the playbook. Prompts always end with "No text, no letters, no logos".
5. **Build in Figma** (`fwTWYozj0aTtlTMvKtVJRR`, page Posts `0:1`): clone the 5 `AURA News · …` masters from Reference
   into Results `11:133` as a new row below the last one, set the copy and images, and pick slide types A/B/C to fit the story.
6. **Verify every frame by screenshot.** Check for overlaps, single words alone on a line, unreadable text and missing images. Fix, then screenshot again.
7. **Export** 01–05.png and caption.txt (caption ends with the source line) to `~/Documents/01-Euribia/posts/<YYYY-MM-DD>-<slug>/`.
8. **Hand over:** call `submit_for_review` with the PNG paths, the caption, the Figma link and one line of notes. Publish nothing yourself.
9. **Write the ledger** entry (topic, date, sources, Figma ids, image hashes) to `state/ledger.json`.

If a step fails twice, finish what you can and say in the first line exactly what did not get done.
