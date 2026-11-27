# CONTENTO TOPIC ENGINE — where a topic comes from when nobody gives one

Used by every scheduled run. Deterministic, deduped, never repeats itself.

## Priority order (first hit wins)

1. **The user named a topic** in the request → use it verbatim. Stop here.
2. **`state/TOPICS.md` has an unused entry** → take the top unchecked one, mark it `[x]` when the
   piece ships. This is the manual override queue — the user can drop ideas in any time.
3. **Alternate news ↔ pillar** based on the ledger. Look at `published[]` in `state/ledger.json`:
   if the last piece of this type came from `news`, take a `pillar` this time, and vice versa.
   This is what keeps the feed from being all-news or all-evergreen.

## A. News radar (timely half)

Pull the last ~48h from these feeds (ported from the retired `euribia-news-carousel` task):

**Tech**
- https://techcrunch.com/feed/
- https://www.theverge.com/rss/index.xml
- https://feeds.arstechnica.com/arstechnica/technology-lab

**Innovation / AI / startups**
- https://venturebeat.com/feed
- https://www.wired.com/feed/rss
- https://news.crunchbase.com/feed/
- https://www.technologyreview.com/feed/

**Marketing / SEO / martech**
- https://www.marketingdive.com/feeds/news/
- https://www.socialmediatoday.com/feeds/news/
- https://searchengineland.com/feed
- https://www.searchenginejournal.com/feed/
- https://martech.org/feed/

> All 13 verified live on 2026-08-31.
> ⚠️ `contentmarketinginstitute.com/feed` was in the old list and is **dead** — it now returns an
> HTML page, not RSS. Removed; replaced by Search Engine Land / SEJ / MarTech.

**Fetching gotchas (learned the hard way):**
- **Send a full browser User-Agent.** `news.crunchbase.com` returns **403** to a bare UA and **200**
  to a real one. Use:
  `curl -sL -m 25 -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126 Safari/537.36" '<feed>'`
- **Count items by occurrence, not by line.** Several feeds ship minified XML on a single line, so
  `grep -c '<item>'` reports `1` and looks broken. Use `grep -o '<item>\|<entry>' | wc -l`.
- **Check you got XML, not HTML.** A dead feed often returns HTTP 200 with an HTML page. If the body
  starts with `<!DOCTYPE html`, treat the feed as down and skip it.
- A couple of dead feeds is normal — proceed as long as you have enough stories. If *no* feed
  yields anything usable, fall back to the pillar rotation (never skip the run).

**Selection rules**
- In scope: AI, tech, digital marketing, e-commerce, startups, innovation. Nothing else.
- Prefer a story a **Bulgarian SME owner** would actually care about — not US funding-round gossip.
- Reject anything already in the ledger (match on the story's core subject, not the exact headline).
- **The news is the hook, not the content.** Every news post must answer *"и какво значи това за
  твоя бизнес?"* — Euribia's angle is the payload; the story is just the door in.
- Never fabricate a detail the source doesn't contain. If facts are thin, dispatch
  `contento-research` for verification before writing.

## B. Pillar rotation (evergreen half)

Take the next pillar from `state/PILLARS.md` using `pillar_pointer` in the ledger, then advance the
pointer (wrap to 0 at the end). Each pillar entry carries its own angle bank so the same pillar
never produces the same post twice — pick an angle not yet logged for that pillar.

## C. Dedupe rule

Before committing to a topic, scan `published[]` in the ledger:
- Same core subject within **90 days** → reject, take the next candidate.
- Same pillar+angle pair ever → reject, take the next angle.

## D. Post vs blog framing of the same topic

A topic can serve both formats in the same week — that is intentional (long → short, the reservoir
principle). When it does:
- **Blog** = the reservoir. Full argument, sources, structure, SEO.
- **Posts** = cut from the reservoir. One direction each, never a summary of the whole article.
Log both against the same topic id in the ledger so the pairing is visible.
