---
name: awesome-design-md
description: Library of 74 ready-made DESIGN.md design systems inspired by real brands' websites (Stripe, Linear, Vercel, Apple, Notion, Airbnb, Figma, Framer, Supabase, Spotify, Tesla, Nike, Revolut, Wise and more) — colors, typography, spacing, radii, buttons, components and layout rules. Use when the user wants a UI/website/landing page that looks like a specific brand ("make it look like Linear", "Stripe-style pricing page", "Apple-like hero"), wants a DESIGN.md for a project, or needs a concrete, non-generic design system to build against instead of default AI styling.
---

# Awesome DESIGN.md

Source: [VoltAgent/awesome-design-md](https://github.com/VoltAgent/awesome-design-md) (MIT, see `LICENSE`).

Each folder in `designs/<brand>/` holds a `DESIGN.md` (frontmatter tokens + prose rules) and a `README.md`.

## How to use

1. Pick the brand closest to what the user asked for. List options with `ls designs/`.
2. Read `designs/<brand>/DESIGN.md` in full before writing any UI code.
3. Copy it into the project root as `DESIGN.md` (or merge its tokens into the project's theme) and build strictly against it: its colors, type scale, spacing, radii, button and card rules.
4. Several brands can be blended (e.g. Linear layout + Stripe color), but say which tokens came from where.

## Rules

- These are *inspired* analyses, not official brand assets. Never ship another company's logo, name or proprietary font in client work; swap to a licensed/free lookalike font the DESIGN.md suggests or the closest Google Font.
- For Euribia or client work, the client's own brand always wins; use a DESIGN.md only for structure, rhythm and component rules.
- Pair with `impeccable` / `taste-skill` for design quality and `playwright-cli` for screenshot checks.

## Available designs

airbnb, airtable, apple, binance, bmw, bmw-m, bugatti, cal, claude, clay, clickhouse, cohere, coinbase, composio, cursor, dell-1996, elevenlabs, expo, ferrari, figma, framer, hashicorp, hp, ibm, intercom, kraken, lamborghini, linear.app, lovable, mastercard, meta, minimax, mintlify, miro, mistral.ai, mongodb, nike, nintendo-2001, notion, nvidia, ollama, opencode.ai, pinterest, playstation, posthog, raycast, renault, replicate, resend, revolut, runwayml, sanity, sentry, shopify, slack, spacex, spotify, starbucks, stripe, supabase, superhuman, tesla, theverge, together.ai, uber, vercel, vodafone, voltagent, warp, webflow, wired, wise, x.ai, zapier
