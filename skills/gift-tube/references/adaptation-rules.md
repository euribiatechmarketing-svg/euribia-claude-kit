# Gift Tube adaptation rules + layout

These are the printer's hard rules (from Gift Tube's brief) plus the layout pattern. Keep the Gift
Tube "chrome" intact, pour the client brand into everything else.

## Hard rules — the VOUCHER (must follow, the brief is explicit)
1. **`ВАЛИДЕН ДО:` and `УНИКАЛЕН КОД:` keep their position and the spacing beneath them.** The
   system prints the date + code there in **dark text you cannot restyle**, so these fields and the
   gap under them **must be on a light background**. This is non-negotiable.
2. **QR code + contacts stay on the front.** You may shrink or rearrange them, but they stay on
   the face.
3. **Keep the GIFT TUBE logo** — it may be moved, not removed.
4. **Keep the wording „Ваучер за преживяване".**
5. The two fields **„Специално за"** and **„Пожелание от сърце"** may be merged into **one** shared
   message field (e.g. a single `Пожелание:` with writing lines).
6. **3 mm bleed** on the voucher.
7. **Back is for physical vouchers only.** Digital = front only, no back design.

## Hard rules — the TUBE LABEL (physical only)
1. **Respect the bleeds already in the working file** (the 201×156 canvas) — see `print-specs.md`.
2. **Keep the GIFT TUBE logo and the `gift-tube.com` site** — they may be moved, not removed.

## Gift Tube chrome to preserve (lives in `assets/gift-tube-chrome/`)
- **GIFT TUBE circular emblem** (the line-art square monogram in a ring). Reuse the vector from
  `voucher-front.svg` / `tube-label.svg`, or the client's own copy if cleaner.
- **Lockup „ПОДАРИ ПРЕЖИВЯВАНЕ" + `gift-tube.com`** — bottom of the tube label and voucher footer.
- **Footer line „сбъдва мечти"** under the small Gift Tube logo on the voucher front (optional but
  on-brand).
- **The functional voucher content** (rebuild it, branded — don't copy the teal pixels):
  - `ВАУЧЕР ЗА ПРЕЖИВЯВАНЕ` title
  - one `Пожелание:` field (3 writing lines)
  - `ВАЛИДЕН ДО:` + `УНИКАЛЕН КОД:` on a light panel (rule #1)
  - `КАК ДА ИЗПОЛЗВАШ ТОЗИ ВАУЧЕР?` + 3 numbered steps (verbatim below)
  - QR + caption „Сканирай, регистрирай… и изживей"
  - contacts: `office@gift-tube.com`, `gift-tube.com`

### Verbatim Bulgarian copy (use exactly — do not paraphrase/translate)
Steps:
1. `Регистрирай уникалния код в меню „моят ваучер" на gift-tube.com`
2. `Получи сертификат с контактите на изпълнителя`
3. `Резервирай ден и час, като се свържеш с изпълнителя`

QR caption: `Сканирай, регистрирай… и изживей`
Tube + footer lockup: `ПОДАРИ ПРЕЖИВЯВАНЕ` / `gift-tube.com`

## The arrangement (taken from the Nestea × Gift Tube tube)
Top → bottom, centered on the front panel:
1. **Client logo** (real asset, top)
2. **Big headline** — 2–3 lines, mostly white with one word in the brand's accent (yellow for
   McVitie's). Heavy display type.
3. **Gift Tube sunburst badge** — the GIFT TUBE emblem on a small rayed/badge disc (echoes Nestea).
4. **Lockup** „ПОДАРИ ПРЕЖИВЯВАНЕ" + `gift-tube.com`.
Behind it all: the brand's signature background (McVitie's = royal-blue radial), a **sunburst** of
rays from the top, and **scattered product** (biscuits / pack shot) bleeding off the sides — the
same energy as the brand's own posters.

## Voucher front — vertical order (130×300, portrait)
1. **Header band** (brand color): client logo, eyebrow `ВАУЧЕР ЗА ПРЕЖИВЯВАНЕ`, headline.
2. **Light body panel** (cream/white — satisfies rule #1): `Пожелание:` lines → `ВАЛИДЕН ДО:` /
   `УНИКАЛЕН КОД:` fields → `КАК ДА ИЗПОЛЗВАШ…` + 3 steps → QR + caption.
3. **Footer band** (brand color): small GIFT TUBE logo + „сбъдва мечти" + contacts.

## Voucher back — physical only
Brand background + one large **client medallion** (e.g. hero biscuit ringed by the Gift Tube
emblem), client logo, small GIFT TUBE logo, `gift-tube.com`. Mirrors the general template's back.

## Issuing facts (for talking to the client, from the brief)
- Branded vouchers: **3 working days** after design sign-off. Unbranded: **1 day**.
- Voucher prices are final, **no VAT** added. Two formats: **physical** and **digital**.
