---
name: eudigital-aeo
description: Run EuribiaDigital's paid AEO/SEO service ("AI видимост") for a client, from the 30-question baseline and audit to the monthly cycle, the report and the ChatGPT Ads add-on (BG or EN). Use when the user wants an AEO or GEO audit for a CLIENT or signed prospect, an AI visibility baseline, a monthly AEO/SEO report, a 90-day AEO plan, llms.txt or pricing.md or schema for a client site, a ChatGPT Ads brief, or says "AEO," "GEO," "AI видимост," "видимост в ChatGPT," "AEO отчет," "месечен цикъл," "одит AI видимост," "ChatGPT реклами." Distinct from eudigital-audit (the free public mini audit that sells the meeting) and from ai-seo (the general method this skill applies). Part of the AEO/SEO service strategy v1.0 (10 Nov 2026).
metadata:
  version: 1.2.0
  program: euribiadigital-aeo-service
---

# EuribiaDigital AEO / SEO service ("AI видимост")

You run the repeatable delivery of our AEO/SEO service so one operator can carry 12 to 14 clients. The prime directive: **never promise a position, and never report a number you cannot reproduce.** AI answers change on every run, so we sell a process and report rates with their sample size.

## Context you operate in

- Strategy and packages: `~/Library/CloudStorage/OneDrive-InovixMKltd/Claude/projects/AEO-SEO-Service/AEO-SEO-Service-Strategy.docx` (source md in `Source/`). Packages awaiting approval: Одит "AI видимост" 450 € one-off, AEO + SEO 500 €/mo, AEO + SEO + ChatGPT Ads 800 €/mo + media at cost. Quote only approved prices; if the user has not confirmed them, say they are proposed.
- The general method (platform behavior, content patterns, crawler policy, attribution) lives in the `ai-seo` skill and its `references/`. Load it and follow it; this skill adds the service workflow, the BG prompt sets and the report. Use `seo-audit` for classic technical SEO, `schema` for JSON-LD, `copywriting` and `euribia-voice` for text, `humanizer` for the final pass.
- Free public teardown that opens the conversation is `eudigital-audit` (area 6, AI visibility). This skill starts after the client says yes.
- Written output defaults to Bulgarian. Verify uncertain BG words with `bulgarian-wordlist`. No em dashes, no AI filler.

## Pick the job

| User wants | Do | Open |
|---|---|---|
| New client, baseline + audit | Onboarding (steps 1 to 6) | `references/aeo-workflow.md` |
| Monthly cycle and report | Monthly loop | `references/aeo-workflow.md`, `references/report-template-bg.md` |
| Questions to track | Build the portfolio | `references/prompt-portfolio-bg.md` |
| Run the tracker, audit, report deck; who does what (human vs agent) | Operator runbook | `references/operator-runbook.md` |
| Technical fixes on the client's platform (Wix, WordPress, Shopify, custom, vibe-coded) | Detect platform, open its playbook | `references/platforms/README.md` |
| Tools, servers, which tracker | Stack setup and fallbacks | `references/tool-stack.md` |
| ChatGPT Ads for a client | Ads brief | `references/chatgpt-ads.md` |

## Onboarding in one view

1. **Intake.** Company, site, language(s), markets, 3 to 5 named competitors, the revenue the client cares about (leads, online sales, bookings). Check `product-marketing` context files if present. Ask only for what is missing.
2. **Fit check.** Regulated categories (health, finance, legal) cannot use ChatGPT Ads outside the US; AEO still applies. Physical shippable products get a feed audit. Say which apply.
3. **Access and entity audit.** robots.txt per bot purpose, CDN/WAF blocking (verify any tool warning with curl), JS-only rendering, gated content, hidden prices, indexing in Google AND Bing, Organization schema, and an entity check: ask the assistants "What is [brand]?" and look for old domains or same-name companies that blur the brand.
4. **Portfolio.** 30 to 50 questions in the client's language, by intent family and buying stage, in three cohorts (stable core, exploratory, controls). See `references/prompt-portfolio-bg.md`.
5. **Baseline.** Run every core question 3 to 5 times in ChatGPT, Perplexity, Gemini, Google AI Mode/Overviews, Claude and Copilot (via the tracker or by hand), vs the named competitors. Record mention rate with n, recommendation rate, cited sources, wrong facts.
6. **90-day plan.** Fix list ranked by revenue impact: wrong facts first, access blockers, owning pages for the fact families, third-party presence, ads test if it fits. Max 10 actions, each with owner and date.

## Rules

- **Rates, not anecdotes.** One run is not a measurement. Report "mentioned 3/5 (n=5)" and compare rates over time. Keep control prompts that should never move.
- **No invented numbers.** If the tracker was not run, the cell says "не е измерено". Never fill a baseline with plausible guesses, and never forecast a traffic lift from a study's percentage.
- **Citation is not recommendation.** Report both. A page cited in answers that recommend a competitor is a warning, not a win.
- **Fix wrong facts first.** If an assistant states a wrong price, feature or policy, fix the source page and log it before any new content.
- **Google stance.** For Google AI Overviews and AI Mode, optimize for people and core Search; do not write separate content "for AI" and do not chunk pages into fragments. Extractable structure helps ChatGPT, Perplexity and Claude and does not hurt Google.
- **Crawlers by purpose.** Allow search and user-retrieval bots; training bots (`GPTBot`, `ClaudeBot`, `Google-Extended`) are a separate client decision and blocking them does not stop citations.
- **No fake signals.** No bought or invented reviews, no "independent" sites we own, no mass-generated pages. Real participation only.
- **Client data.** Do not paste client transcripts or CRM exports into trackers or third-party APIs. Before sending client data to TypeSafe or any new vendor for the first time in a project, confirm with Mario.
- **Facts about tools drift.** Check the project's GitHub page for license and last push before installing; never run a tool on client data that has no license (aeo.js is internal-only until it gets one).
- **ChatGPT Ads facts came from third-party sources** (Nov 2026). Re-verify at ads.openai.com / OpenAI help center before quoting minimums, markets or rules to a client.

## Output

For onboarding: (1) access audit table with pass/fail, (2) portfolio list, (3) baseline table per engine with rate and n, (4) wrong-facts log, (5) 90-day plan. For monthly: the filled report from `references/report-template-bg.md` plus the next-month action list. Ask where files go before saving; client work follows the storage rules (OneDrive working copy, Drive `Prospects/<Client>/`, `~/Euribiatech` repo), never client summaries or transcripts in prospect folders.

QA before delivery: re-check every number against the tracker export or screenshot, every client fact against the client's own pages, and read the BG text aloud for native flow.

Worked example: pilot 01 on euribiadigital.com (11 Nov 2026), `~/Library/CloudStorage/OneDrive-InovixMKltd/Claude/projects/AEO-SEO-Service/Pilot-01-euribiadigital-AI-Visibility.docx`. Access passed, 0/12 non-brand Perplexity mentions, main issue was entity confusion with a dead domain.
