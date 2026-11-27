# Custom сайтове (PHP, Laravel, статични, Next.js от екип): playbook за AI видимост

Последна проверка: 11.11.2026

Тук няма админ панел с менюта. Всичко е в кода, на сървъра или в CDN-а. Плюсът: агентът може да направи почти всичко сам като Pull Request. Минусът: нищо не става автоматично, всяка промяна минава през разработчика или deploy процеса на клиента. Правило: ние пращаме PR, разработчикът на клиента го одобрява и deploy-ва. Не пипаме production директно.

## 1. robots.txt и AI ботове

Къде е файлът:

| Стек | Файл |
|---|---|
| Статичен сайт, PHP | `robots.txt` в web root (`public_html/`, `public/`) |
| Laravel | `public/robots.txt` |
| Next.js App Router | `app/robots.ts` (генерира `/robots.txt`) или `public/robots.txt` |
| Next.js Pages Router | `public/robots.txt` |
| Astro, Hugo, Nuxt | `public/` или `static/` |

Пример за Next.js App Router:

```ts
// app/robots.ts
import type { MetadataRoute } from 'next'

export default function robots(): MetadataRoute.Robots {
  return {
    rules: [
      { userAgent: '*', allow: '/', disallow: ['/admin/', '/api/'] },
      // само ако клиентът откаже обучението; тук забраняваме всичко, затова служебните пътища не се повтарят
      { userAgent: ['GPTBot', 'ClaudeBot', 'Google-Extended', 'Applebot-Extended'], disallow: '/' },
    ],
    sitemap: 'https://example.bg/sitemap.xml',
  }
}
```

Блокиране извън robots.txt (по-често от очакваното):
- **Cloudflare**: AI Crawl Control > таб Security > колона Actions; Block създава WAF custom rule. От 15.09.2026 новите домейни блокират training и agent ботове на страници с реклами по подразбиране. Провери и Security settings, Bot Fight Mode и custom WAF правила с `user-agent contains "bot"`.
- **Сървър**: nginx/Apache правила по user-agent, ModSecurity, fail2ban, rate limits в хостинг панела.
- **Приложение**: Laravel middleware или Next.js middleware, които връщат 403 на "непознати" ботове.

Проверка: тестът с 9 user-agent-а от README, после логовете на сървъра или Cloudflare (Security events, AI Crawl Control) за реални посещения на OAI-SearchBot, PerplexityBot, Claude-SearchBot.

## 2. llms.txt

Статичен файл в корена, в Markdown по предложението на llmstxt.org. Пиши го на езика на сайта; за BG/EN сайт един файл с двата раздела е достатъчен.

```markdown
# Пример ООД

> Счетоводна кантора в Пловдив за малки фирми и ЕТ. Абонаментно счетоводство от 120 EUR месечно, ДДС регистрация, ТРЗ.

## Услуги
- [Абонаментно счетоводство](https://example.bg/uslugi/abonamentno-schetovodstvo): пакети, цени, какво включват
- [ТРЗ и личен състав](https://example.bg/uslugi/trz): цена на служител, срокове

## Цени и условия
- [Цени](https://example.bg/ceni): всички пакети в EUR, актуални към 11.2026
- [Как работим](https://example.bg/kak-rabotim): срокове, документи, договор

## За нас
- [Екип](https://example.bg/ekip): счетоводители и квалификации
- [Контакти](https://example.bg/kontakti): адрес, телефон, работно време
```

Всеки факт в llms.txt трябва да съвпада със страницата, към която сочи. Ако цените се сменят, файлът се сменя в същия PR.

## 3. Structured data

Слагаме JSON-LD в общия layout (Organization/LocalBusiness) и в шаблоните (Article, Product, FAQPage).

Next.js (App Router, server component):

```tsx
const org = {
  '@context': 'https://schema.org',
  '@type': 'AccountingService',
  '@id': 'https://example.bg/#business',
  name: 'Пример ООД',
  url: 'https://example.bg/',
  telephone: '+359 32 000 000',
  address: { '@type': 'PostalAddress', addressLocality: 'Пловдив', addressCountry: 'BG' },
}

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="bg">
      <body>
        <script type="application/ld+json" dangerouslySetInnerHTML={{ __html: JSON.stringify(org) }} />
        {children}
      </body>
    </html>
  )
}
```

Laravel Blade:

```blade
<script type="application/ld+json">
{!! json_encode($schema, JSON_UNESCAPED_UNICODE | JSON_UNESCAPED_SLASHES) !!}
</script>
```

Article шаблонът трябва да има `author` (Person с име), `datePublished`, `dateModified`. Данните идват от CMS-а, не се хардкодват.

## 4. Title, meta, canonical, hreflang, sitemap, индексиране

- Един `<title>` и един `<meta name="description">` на страница, уникални. Next.js: `export const metadata` или `generateMetadata`.
- Canonical: абсолютен URL, без параметри. Next.js: `alternates.canonical`.
- hreflang за BG/EN:

```html
<link rel="alternate" hreflang="bg" href="https://example.bg/uslugi" />
<link rel="alternate" hreflang="en" href="https://example.bg/en/services" />
<link rel="alternate" hreflang="x-default" href="https://example.bg/uslugi" />
```

  Next.js: `alternates.languages`. Всяка версия сочи към себе си и към другата.
- `<html lang="bg">` на BG страниците (често е забравено `lang="en"` от шаблона).
- Sitemap: Next.js `app/sitemap.ts`; Laravel пакет `spatie/laravel-sitemap`; статичен: генериран при build. С `lastmod` от реалната дата на промяна.
- IndexNow: ключ файл `https://example.bg/<key>.txt` и POST при публикуване:

```bash
curl -s -X POST "https://api.indexnow.org/indexnow" -H "Content-Type: application/json" \
  -d '{"host":"example.bg","key":"<key>","keyLocation":"https://example.bg/<key>.txt","urlList":["https://example.bg/ceni"]}'
```

- GSC: DNS TXT верификация (най-устойчива, не зависи от кода). Bing: импорт от GSC.

## 5. Рендериране

PHP, Laravel, статичните генератори и Next.js със server components връщат HTML с текста. Рискът е в Next.js/Nuxt, където страници са изцяло `"use client"` и четат данни с `useEffect`. Тогава текстът липсва в HTML и важат поправките от `vibe-coded.md`.

```bash
curl -sL -A "PerplexityBot" https://example.bg/ceni | grep -c "120 EUR"
curl -sL https://example.bg/ceni | grep -o '<title>[^<]*</title>'
```

## 6. Съдържание, което се цитира

Без разработчик става само ако сайтът има CMS (headless или админ панел). Ако няма, всеки текст е PR. Затова:
- Предложи на клиента прост CMS за страниците, които се сменят (цени, FAQ, блог), или Markdown файлове в repo-то, които агентът редактира.
- Шаблон за услуга: отговор в 2 до 3 изречения, таблица "какво включва / цена / срок", FAQ, дата на актуализация, автор.
- Сравнителни страници с истинска HTML таблица (`<table>`), не с div-ове и не с картинка.

## 7. Какво прави агентът и какво човек

| Задача | Агент | Човек |
|---|---|---|
| Одит с curl, четене на кода | Да | |
| robots, llms.txt, sitemap, schema, meta, hreflang, нови страници | Да, като PR в отделен branch | Разработчик: review, merge, deploy |
| Cloudflare / сървърни правила | Предлага точната промяна | Собственик на акаунта |
| GSC, Bing, DNS | | Да |

Достъп (минимум): GitHub/GitLab с права да прави branch и PR (не admin, не push в main), без production secrets и без SSH до сървъра. Ако repo-то не е в git, искаме копие и пращаме patch файлове. Cloudflare: само ако е нужно, роля с достъп до Security/AI Crawl Control на конкретната зона, не Super Administrator.

## 8. Чеклист

**Ден 1** (~2 ч)
- [ ] Определи стека и кой deploy-ва (15 мин)
- [ ] robots.txt + тест с 9 user-agent-а + проверка на Cloudflare (45 мин)
- [ ] curl на 5 ключови страници: текст, title, canonical, lang (30 мин)
- [ ] Поискай repo достъп и контакт с разработчика (15 мин)

**Седмица 1** (~8 ч)
- [ ] PR 1: robots, llms.txt, sitemap с lastmod, Organization JSON-LD (3 ч)
- [ ] PR 2: meta/canonical/hreflang/lang поправки (3 ч)
- [ ] IndexNow ключ и извикване при deploy (1 ч)
- [ ] GSC и Bing (30 мин)

**Месец 1** (~12 ч)
- [ ] Страници "Цени", FAQ, сравнение (6 ч)
- [ ] Article шаблон с автор и дати (2 ч)
- [ ] Предложение за CMS за често сменяните страници (2 ч)
- [ ] Повторен одит след deploy (1 ч)

## 9. Капани

- PR-ът стои седмици без deploy. Договори срок за review с клиента още на старта.
- Staging без защита се индексира (или обратното: production е с `noindex` от staging конфигурацията).
- Cloudflare правила, писани преди години от друг човек, режат ботове по user-agent.
- Hardcoded цени в 5 различни файла. Направи един източник.
- `lang="en"` на български сайт и hreflang, сочещ към 404.
- Next.js `"use client"` страници с данни от API: празен HTML за ботовете.

## Източници

- https://www.rfc-editor.org/rfc/rfc9309
- https://nextjs.org/docs/app/api-reference/file-conventions/metadata/robots
- https://nextjs.org/docs/app/api-reference/file-conventions/metadata/sitemap
- https://nextjs.org/docs/app/guides/json-ld
- https://nextjs.org/docs/app/api-reference/functions/generate-metadata
- https://llmstxt.org/
- https://www.indexnow.org/documentation
- https://developers.cloudflare.com/ai-crawl-control/features/manage-ai-crawlers/
- https://www.helpnetsecurity.com/2026/07/02/cloudflare-ai-crawler-controls/
- https://developers.google.com/search/docs/specialty/international/localized-versions
- https://developers.google.com/search/docs/appearance/ai-features
