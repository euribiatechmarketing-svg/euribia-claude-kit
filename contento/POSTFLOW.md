# PostFlow delivery contract (Euribia posts)

Where a finished carousel GOES. Figma stays the build surface; **PostFlow is the delivery target**.
Every post lands in PostFlow as a **DRAFT assigned to Dimitar for approval**. The engine never
publishes to a social channel — approval + publish happen inside PostFlow, by a human.

## Auth
- Token: `POSTFLOW_API_TOKEN` in `~/.config/euribia/api-keys.env`
  (`source ~/.config/euribia/api-keys.env` — never hard-code it, never print it in a report).
- Header on every call: `Authorization: Bearer $POSTFLOW_API_TOKEN`
  plus `Accept: application/json`.
- Generated in PostFlow → account settings → API. If the token is missing or returns 401, that is a
  **blocking failure for delivery only** — the Figma build still counts; see "Failure modes".

## Two base URLs (they are different hosts — this is the #1 mistake)
| Purpose | Base |
|---|---|
| Posts, accounts, groups | `https://api.postflow.app/v1` |
| Media upload | `https://media.postflow.app/api/v1` |

## Pipeline (after the Figma frames pass their screenshot gate)

### 1. Export the 5 frames as PNG
Export from Figma at 2x into `assets/exports/<YYYY-MM-DD>-<slug>/` as `01.png … 05.png`.
Order matters — it becomes the carousel order.

### 2. Upload each PNG → media id
```
POST https://media.postflow.app/api/v1/upload
-H "Authorization: Bearer $POSTFLOW_API_TOKEN"
-F "file=@01.png"
```
Response is a MediaData object → take `id`. Collect the five ids **in slide order**.
Accepted: png/jpg/jpeg/webp/gif/heic/avif/mp4/mov/… (max 2048 MB).

### 3. Resolve the target accounts (once per run, cheap)
```
GET https://api.postflow.app/v1/social-accounts
```
Pick the Euribia Digital Instagram + LinkedIn (+ Facebook if connected) ids.
Cache the resolved ids in `state/postflow.json` so later runs skip this call; re-resolve if a
POST fails with an unknown-account error.

### 4. Create the DRAFT post
```
POST https://api.postflow.app/v1/posts
{
  "content": "<the Bulgarian caption incl. hashtags>",
  "selectedAccountIds": ["<ig>", "<li>"],
  "selected_media_ids": ["<01>","<02>","<03>","<04>","<05>"],
  "publication_date": "<next working day 10:00 +03:00>",
  "isDraft": true,
  "isPublishNow": false,
  "name": "<тема — кратко>",
  "note": "Contento auto-run <дата>. Източник: <линк>.",
  "assigneesIds": ["<Dimitar's PostFlow user id>"],
  "notify_assignee": true,
  "ig_post_type": 1,
  "li_post_type": 3,
  "li_carousel_title": "<до 58 знака>"
}
```
- **`isDraft: true` is non-negotiable.** `isPublishNow` must be `false` or absent.
- `publication_date` is a **proposal**, not a commitment — Dimitar can move it when approving.
  RFC 3339 with offset (`2026-09-08T10:00:00+03:00`). No offset = UTC, which is the wrong hour.
- All PostFlow ids are **strings**. Never let a JSON number swallow the precision.
- Per-network copy differences go in `customized: { instagram: {...}, linkedin: {...} }`.

### 5. Verify (mandatory — tool success is not evidence)
```
GET https://api.postflow.app/v1/posts/<id>
```
Confirm: the post exists, `isDraft` is true, **5 media** attached in the right order, the caption is
intact (Bulgarian, no mojibake), the accounts are the intended ones, the assignee is set.
Only then report it as delivered.

### 6. Report + log
The report gives the PostFlow link and one line: „остава само да го одобриш в PostFlow".
Ledger entry gets `postflow_post_id` and `postflow_media_ids` next to the Figma frame ids.

## Failure modes
| Failure | What to do |
|---|---|
| `POSTFLOW_API_TOKEN` missing / 401 | Do NOT retry blindly. Deliver the Figma frames + caption as usual, and put "PostFlow: не е доставено — липсва/невалиден токен" in the **first two lines** of the report. |
| Media upload fails on one file | Retry that file once. Still failing → do not create a partial post; report which slide failed. |
| Unknown account id | Re-resolve via `GET /social-accounts`, refresh `state/postflow.json`, retry once. |
| Post created but verification mismatches | Fix via `PATCH /v1/posts/<id>` (partial update) and re-verify. Never leave a wrong draft standing silently. |

## Hard rule
The engine's reach stops at a PostFlow **draft**. `isPublishNow`, un-drafting, or publishing to a
channel is Dimitar's action, in PostFlow's own UI. No exceptions, no "it was obviously ready".
