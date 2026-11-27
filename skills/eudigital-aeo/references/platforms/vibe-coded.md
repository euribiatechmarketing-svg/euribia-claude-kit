# Vibe-coded сайтове (Lovable, Bolt, v0, Replit, Cursor + Vite): playbook за AI видимост

Последна проверка: 11.11.2026

Тук основният проблем е един: сайтът се рендерира в браузъра. Сървърът връща празен `<div id="root"></div>` и JavaScript файл. Google в повечето случаи изпълнява JavaScript (със закъснение), но OAI-SearchBot, PerplexityBot, Claude-SearchBot и потребителските ботове често не го правят. За тях сайтът е празна страница. Докато това не е поправено, всичко останало (schema, llms.txt, съдържание) дава малко.

Затова редът е: 1) тест на рендерирането, 2) поправка, 3) всичко останало.

## 1. Тест на рендерирането (първите 10 минути)

```bash
URL="https://example.bg/uslugi"
PHRASE="дума, която виждаш на страницата в браузъра"

for ua in "Mozilla/5.0" OAI-SearchBot ChatGPT-User PerplexityBot Claude-SearchBot Claude-User ClaudeBot Googlebot bingbot; do
  n=$(curl -sL -A "$ua" "$URL" | grep -c "$PHRASE")
  printf "%-16s %s\n" "$ua" "$n"
done

# Title и description: еднакви ли са на всички страници?
for p in / /uslugi /ceni /kontakti; do curl -sL "https://example.bg$p" | grep -o '<title>[^<]*</title>'; done
```

Как да четеш резултата:
- 0 за всички: чист CSR. Отиди на т. 2.
- 0 за `Mozilla/5.0`, но 1+ за ботовете: има prerendering за ботове (Lovable, Netlify Prerender, Prerender.io). Провери ВСЕКИ AI бот поотделно: prerender услугите разпознават списък от ботове и някои не са в него (в Netlify форума има случай с ClaudeBot, който не получава prerender версията).
- Еднакъв `<title>` на всички страници: meta таговете се сменят само в браузъра (react-helmet и подобни). Ботовете виждат едно заглавие за целия сайт.

## 2. Поправка: варианти по ред на предпочитание

| Вариант | Кога | Усилие |
|---|---|---|
| A. Lovable: миграция към TanStack Start (SSR) | Lovable проект, създаден преди 13.05.2026 | Ниско: `/migrate` в чата, бутон Migrate в project settings или помоли агента. Харчи кредити. Live сайтът не се сменя, докато не публикуваш. |
| B. Статично генериране при build (SSG/prerender) | Сайт с под ~100 страници, съдържанието се сменя рядко (визитка, услуги) | Средно: инструмент, който отваря всеки route при build и записва HTML. |
| C. React Router v7 framework mode с `prerender` | Проектът вече ползва React Router | Средно |
| D. Миграция към Next.js или Astro | Сайт, който ще расте (блог, много страници), или B не става | Високо, но трайно |
| E. Prerendering само за ботове (Netlify Prerender extension, Prerender.io) | Временно, докато се направи A до D | Ниско. Google нарича dynamic rendering заобиколно решение, не дългосрочно. |

Детайли:
- **Lovable**: нови проекти от 13.05.2026 са на TanStack Start със SSR, безплатно на всички планове (по страницата на Lovable). По-старите React + Vite проекти получават автоматични статични снимки за проверени търсачки, social preview ботове и "поддържани AI crawlers"; кои точно AI ботове: непроверено, затова тестът от т. 1 е задължителен. Ако в project settings няма бутон Migrate, проектът вече е на новия engine. Lovable има и вграден SEO/AI Search преглед, който отбелязва липсващи meta тагове и structured data.
- **Vite SSG инструменти**: `vite-react-ssg`, `snappy-prerender` (CLI или Vite plugin, отваря всеки route в headless браузър), `vite-plugin-ssg-spa`. `react-snap` не се поддържа активно от години, не го ползвай. Избери един, пусни го на копие, сравни HTML-а с curl.
- **Netlify**: Prerender extension е GA от 16.12.2025, безплатен за всички планове, заменя стария вграден prerendering (изключен през 2026). Prerender.io е отделно платено разширение.
- **Vercel**: няма вграден prerendering за Vite SPA. Вариантите са B, C, D или Prerender.io през middleware (настройката за Vercel: непроверено).
- **v0**: обикновено генерира Next.js. Ако страниците са server components, проблемът го няма. Провери с curl.
- **Bolt, Replit**: обикновено Vite + React SPA. Изтегли кода в GitHub и приложи B или D. Хостинг опциите на Bolt за SSR: непроверено.

## 3. robots.txt и AI ботове

- Файлът е `public/robots.txt`. Lovable шаблоните често идват с готов robots.txt, който изброява Googlebot, Bingbot и social ботове; провери дали `User-agent: *` разрешава останалите.
- **SPA rewrite капан**: Vercel/Netlify правило "всичко към `/index.html`" (`"rewrites": [{"source": "/(.*)", "destination": "/index.html"}]` или `/* /index.html 200`) връща 200 и HTML за `/robots.txt`, `/sitemap.xml`, `/llms.txt`, ако файлът липсва. Ботът получава HTML вместо текст. Провери: `curl -sI https://example.bg/sitemap.xml | grep -i content-type` трябва да е XML.
- Същото правило прави всяка несъществуваща страница 200 (soft 404). Добави истинска 404 страница.
- Cloudflare пред сайта: AI Crawl Control > Security > Actions, виж `custom.md`. Vercel Firewall има managed правила за ботове; дали има отделно "AI bots" правило и какво е по подразбиране: непроверено, провери в Firewall таба на проекта.

## 4. llms.txt, sitemap, meta, hreflang

- `public/llms.txt`: статичен файл, формат както в `custom.md`. Няма автоматично генериране, освен ако не го напишеш в build скрипта.
- `public/sitemap.xml`: генерирай при build от списъка с routes (повечето SSG инструменти го правят). Ръчен sitemap остарява при всяка нова страница от AI агента.
- Meta по страница: работи надеждно само след поправката от т. 2. С SSR/SSG всеки route има собствени `<title>`, `description`, `canonical`.
- hreflang и `<html lang="bg">`: шаблоните идват с `lang="en"`. Сменете го.
- IndexNow: ключ файл в `public/` + POST при deploy (пример в `custom.md`).
- GSC: DNS TXT запис при регистратора (не зависи от кода и от хостинга). Bing: импорт от GSC.

## 5. Structured data

След т. 2 добави JSON-LD като `<script type="application/ld+json">` в HTML-а, който сървърът връща (в layout компонента при SSR, в `index.html` за Organization, в шаблона на route при SSG). JSON-LD, добавен само с JavaScript след зареждане, има същия проблем като текста. Примерите за Organization и LocalBusiness са в `custom.md` и `wix.md`.

## 6. Съдържание, което се цитира

Vibe-coded сайтовете често са една дълга landing страница с анимации. Асистентите цитират страници, които отговарят на един въпрос. Затова:
- Отделни routes: `/ceni`, `/uslugi/<usluga>`, `/vaprosi`, `/sravnenie`, с текст, а не само карти и икони.
- Първият абзац отговаря на въпроса. Числата (цени в EUR, срокове) са в текст.
- Таблиците са истински `<table>`. Lovable/Bolt агентът може да го направи, ако му кажеш изрично "semantic HTML table".
- Дата "Актуализирано: 11.2026" и автор на статиите.
- Промпт за Lovable/Bolt агента (пример): "Добави страница /ceni с H1 'Цени', таблица с колони Услуга, Какво включва, Цена в EUR, и абзац с дата на актуализация. Използвай semantic HTML, без изображения за текста."

## 7. Какво прави агентът и какво човек

| Задача | Агент (Claude Code) | Човек |
|---|---|---|
| Тестове с curl, одит | Да | |
| SSG/prerender, robots, sitemap, llms.txt, meta, schema, нови страници | Да, като PR в GitHub repo-то | Собственик: merge и publish |
| Lovable миграция (`/migrate`) | Не (става в Lovable UI) | Собственикът на проекта, след като одобри разхода на кредити |
| Netlify/Vercel настройки, Cloudflare, DNS, GSC | Подготвя точната стъпка | Собственик на акаунта |

Lovable има синхронизация с GitHub. Ако е включена, агентът работи в repo-то и промените се връщат в Lovable. Внимание: ако едновременно някой пише промпти в Lovable, ще има конфликти. Договорете кой работи кога.

Достъп (минимум): GitHub repo с права за branch и PR. Не искаме login в Lovable/Bolt/Replit и не искаме Vercel/Netlify Owner. Ако трябва настройка на хостинга, клиентът ни кани като член с ограничена роля или прави стъпката по нашия списък.

## 8. Чеклист

**Ден 1** (~2 ч)
- [ ] Тест от т. 1 за 5 страници и 9 user-agent-а (30 мин)
- [ ] Определи инструмента (Lovable, Bolt, v0...), хостинга и има ли GitHub (20 мин)
- [ ] Проверка на `robots.txt`, `sitemap.xml`, `llms.txt`: content-type, не HTML (15 мин)
- [ ] Избери вариант A до E, напиши го на клиента с 2 изречения защо (30 мин)
- [ ] Поискай GitHub достъп (15 мин)

**Седмица 1** (~10 ч)
- [ ] Приложи поправката от т. 2 на копие/branch (4 до 6 ч)
- [ ] Повтори теста: текстът и уникалните title-и са в HTML за всички ботове (1 ч)
- [ ] robots, sitemap, llms.txt, 404 страница (1,5 ч)
- [ ] Organization JSON-LD в server HTML, GSC и Bing (1,5 ч)

**Месец 1** (~12 ч)
- [ ] Раздели landing страницата на отделни routes за услуги, цени, въпроси (6 ч)
- [ ] Сравнителна страница с таблица (2 ч)
- [ ] IndexNow при deploy (1 ч)
- [ ] Повторен одит и проверка в GSC > Pages и URL Inspection (1 ч)

## 9. Капани

- Тест само с браузъра. В браузъра всичко изглежда наред. Винаги curl.
- Prerender услуга, която покрива Googlebot, но не и ClaudeBot или Perplexity.
- SPA rewrite, който сервира `index.html` вместо sitemap/robots/llms.txt.
- Един и същ `<title>` за всички страници.
- Lovable агентът "поправя" SEO с react-helmet: в браузъра изглежда готово, в curl не се вижда.
- Сайтът е на `*.lovable.app` / `*.vercel.app` и на собствен домейн едновременно: дублирано съдържание. Пренасочи (301) поддомейна на платформата към собствения домейн, ако платформата позволява, и сложи canonical към собствения домейн.
- Съдържание, заредено от Supabase или друг API при отваряне на страницата: не е в HTML, освен ако не е включено в SSR/SSG.

## Източници

- https://lovable.dev/en/seo-aeo
- https://docs.lovable.dev/
- https://www.netlify.com/changelog/2025-12-16-prerender-extension-ga/
- https://www.netlify.com/changelog/2026-01-08-prerenderio-support-updates/
- https://answers.netlify.com/t/claudebot-claude-web-is-not-triggering-prerendering-even-with-the-prerender-extension-enabled/160918
- https://developers.google.com/search/docs/crawling-indexing/javascript/dynamic-rendering
- https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics
- https://reactrouter.com/how-to/pre-rendering
- https://github.com/337547038/vite-plugin-seo-prerender
- https://www.producthunt.com/p/snappy-prerender/snappy-prerender
- https://developers.openai.com/api/docs/bots
- https://docs.perplexity.ai/guides/bots
- https://developers.google.com/search/docs/appearance/ai-features
