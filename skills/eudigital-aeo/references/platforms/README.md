# Платформени playbook-и за AI видимост: кой файл да отвориш

Последна проверка: 11.11.2026

Тази папка казва КАК да направим техническата част от AEO/GEO на конкретната платформа на клиента. КАКВО правим (портфолио от въпроси, baseline, отчет) е в `../aeo-workflow.md`.

## Стъпка 1: разпознай платформата за 1 минута

Пусни двете команди от терминала (смени адреса):

```bash
URL="https://example.bg"

# 1) Хедъри: кой сървър, CDN, платформа
curl -sIL "$URL" | grep -iE '^(server|x-powered-by|powered-by|x-wix|x-shopid|x-shopify|link|x-vercel|x-nf-request-id|cf-ray|x-generator)'

# 2) HTML маркери
curl -sL "$URL" -o home.html
grep -oiE 'name="generator" content="[^"]+"|wp-content|wp-json|cdn\.shopify\.com|Shopify\.theme|static\.wixstatic\.com|__NEXT_DATA__|self\.__next_f|/_next/static|id="root"></div>|id="app"></div>|/assets/index-[a-zA-Z0-9_-]+\.js|lovable|gptengineer' home.html | sort -u

# 3) Има ли текст в суровия HTML (без JavaScript)?
sed 's/<[^>]*>/ /g' home.html | tr -s ' \n' | wc -w
```

Ако третата команда връща под ~100 думи за начална страница, която в браузъра е пълна с текст, сайтът най-вероятно се рендерира в браузъра (CSR). Това е най-важният сигнал в цялата таблица.

## Стъпка 2: таблица за решение

| Какво виждаш | Платформа | Отвори |
|---|---|---|
| `<meta name="generator" content="Wix.com Website Builder">`, хедър `x-wix-request-id`, картинки от `static.wixstatic.com` | Wix / Wix Studio | `wix.md` |
| `generator` = `WordPress 6.x`, пътища `/wp-content/`, хедър `link: <.../wp-json/>; rel="https://api.w.org/"` | WordPress (вкл. WooCommerce) | `wordpress.md` |
| `cdn.shopify.com`, `Shopify.theme` в JS, хедъри `x-shopid` / `x-shopify-stage` / `powered-by: Shopify` | Shopify | `shopify.md` |
| `__NEXT_DATA__` или `self.__next_f`, `/_next/static/`, `x-powered-by: Next.js`, и думите от страницата СА в HTML | Next.js, правен от разработчици | `custom.md` |
| Laravel (`laravel_session` бисквитка, `XSRF-TOKEN`), чист PHP, статичен HTML, Astro, Hugo, Nuxt с SSR | Custom / класически framework | `custom.md` |
| Празен `<div id="root"></div>` или `<div id="app"></div>`, един `/assets/index-xxxx.js`, почти няма текст в HTML | Vibe-coded SPA (Lovable, Bolt, v0, Replit, Cursor + Vite) | `vibe-coded.md` |
| Домейн `*.lovable.app`, `*.replit.app`, `*.vercel.app`, `*.netlify.app`, или следи от `lovable` / `gptengineer` в HTML | Vibe-coded, дори да е на собствен домейн | `vibe-coded.md` |
| Next.js, но текстът липсва в HTML (всичко е `"use client"` и се зарежда с fetch) | Третирай като vibe-coded | `vibe-coded.md` (поправката) + `custom.md` (останалото) |

Хедъри, които казват кой е отпред (CDN/хостинг), без значение от платформата:

| Хедър | Какво значи | Какво проверяваш |
|---|---|---|
| `server: cloudflare`, `cf-ray` | Cloudflare отпред | AI Crawl Control и Security settings, виж по-долу |
| `server: Vercel`, `x-vercel-id` | Хостинг Vercel | Firewall правила, SPA rewrites |
| `server: Netlify`, `x-nf-request-id` | Хостинг Netlify | Prerender extension, redirects |

Ако нищо не съвпада (Squarespace, Webflow, Tilda, Odoo Website и т.н.): няма отделен playbook. Ползвай принципите от `custom.md`, а менютата търси в официалната документация на платформата и пиши "непроверено" за всичко, което не си видял с очите си.

## Обща политика за AI ботовете (важи за всички платформи)

Ботовете са три вида и ги третираме различно:

| Вид | Ботове | Нашата позиция |
|---|---|---|
| Търсене (индекс за AI отговори) | `OAI-SearchBot`, `PerplexityBot`, `Claude-SearchBot`, `Bingbot` (Copilot, Bing), `Googlebot` (AI Overviews и AI Mode) | Винаги разрешени. Без тях няма цитати. |
| Заявка на потребител (live fetch) | `ChatGPT-User`, `Perplexity-User`, `Claude-User` | Разрешени. OpenAI и Perplexity казват, че тези може да не спазват robots.txt, защото действат по заявка на човек. |
| Обучение на модели | `GPTBot`, `ClaudeBot`, `Google-Extended`, `Applebot-Extended` | Бизнес решение на клиента. По подразбиране препоръчваме да са разрешени за МСП, които искат да бъдат познати. Блокирането им не спира цитатите. |

Важно за Google: AI Overviews и AI Mode се управляват от `Googlebot`, не от `Google-Extended`. Google казва, че не са нужни специални файлове, специална schema или "AI текст": страницата трябва да е индексирана и да може да показва snippet. Не пишем отделно съдържание "за AI".

Правило за robots.txt: ако `User-agent: *` вече разрешава всичко, не е нужно да изброяваме AI ботовете. Именувана група (`User-agent: GPTBot`) правим само когато искаме различно поведение. Внимание: бот със собствена група игнорира `*` групата, така че служебните `Disallow` редове трябва да се повторят и в нея.

Бърз тест за блокиране на ниво сървър/WAF:

```bash
for ua in OAI-SearchBot ChatGPT-User GPTBot PerplexityBot Perplexity-User Claude-SearchBot Claude-User ClaudeBot bingbot; do
  printf "%-18s " "$ua"; curl -s -o /dev/null -w "%{http_code}\n" -A "$ua" "$URL/"
done
```

200 навсякъде е добър знак, но не е доказателство: WAF-овете често проверяват IP адреса, а не user-agent. Окончателната проверка е в логовете на CDN-а (Cloudflare: AI Crawl Control) или в сървърните логове.

## Какво НЕ правим (на никоя платформа)

- Не слагаме `/.well-known/ai.txt`, `/ai/*.json` и подобни нестандартни файлове.
- Не правим масово генерирани страници (по една за всеки град или ключова дума с подменено име).
- Не купуваме и не пишем фалшиви ревюта, не правим "независими" сайтове, които са наши.
- Не обещаваме позиция в ChatGPT или в Google.
- llms.txt е предложение, не стандарт. Правим го, защото е евтино, но не го продаваме като фактор за класиране.

## Източници

- https://developers.google.com/search/docs/appearance/ai-features
- https://developers.openai.com/api/docs/bots
- https://docs.perplexity.ai/guides/bots
- https://support.claude.com/en/articles/8896518-does-anthropic-crawl-data-from-the-web-and-how-can-site-owners-block-the-crawler
- https://developers.cloudflare.com/ai-crawl-control/features/manage-ai-crawlers/
- https://www.rfc-editor.org/rfc/rfc9309
- https://llmstxt.org/
