# WordPress (и WooCommerce): playbook за AI видимост

Последна проверка: 11.11.2026

WordPress рендерира на сървъра и има плъгин за почти всичко. Проблемите идват от плъгините, не от WordPress: два SEO плъгина едновременно, security плъгин, който реже ботове, кеш, който показва стара версия, и page builder, който крие текста. Първата задача винаги е: кой SEO плъгин е активен? Работим с ЕДИН (Yoast, Rank Math или AIOSEO), не слагаме втори.

Бърза проверка кой е: `curl -sL URL | grep -oiE 'yoast|rank-math|rankmath|aioseo|all in one seo' | sort -u`

## 1. robots.txt и AI ботове

WordPress сервира виртуален robots.txt. Ако в корена на сървъра има истински файл `robots.txt`, той печели и плъгинът не може да го смени.

Къде се редактира:
- **Yoast:** Yoast SEO > Tools > File editor (иска права за запис върху файловете; изключено е, ако `DISALLOW_FILE_EDIT` е true).
- **Rank Math:** Rank Math SEO > General Settings > Edit robots.txt.
- **AIOSEO:** All in One SEO > Tools > Robots.txt Editor.
- Без плъгин: файл `robots.txt` в корена през FTP/файловия мениджър на хостинга.

Задължително провери:
- **Settings > Reading > Search engine visibility**: отметката "Discourage search engines from indexing this site" трябва да е ИЗКЛЮЧЕНА. Това е най-честата причина сайт да изчезне (остава след разработка).
- Security плъгини (Wordfence и подобни) и хостинг панели понякога блокират непознати ботове или имат опция "block AI bots". Някои SEO плъгини също добавят такива опции (за кои версии: непроверено). Търси настройки с "bot", "crawler", "AI".
- Cloudflare пред сайта (хедър `cf-ray`): **AI Crawl Control** > таб **Security** > колона **Actions** трябва да е **Allow** за търсещите и потребителските ботове. Блок там създава WAF правило. От 15.09.2026 Cloudflare блокира по подразбиране training и agent ботове на страници с реклами за нови домейни; multi-purpose ботове като Bingbot и Applebot могат да бъдат засегнати, ако training е блокиран. Провери и **Security settings**.

Типичен robots.txt за WordPress:

```
User-agent: *
Disallow: /wp-admin/
Allow: /wp-admin/admin-ajax.php

Sitemap: https://example.bg/sitemap_index.xml
```

AI ботовете не е нужно да се изброяват, ако `*` ги пуска. Ако клиентът иска да откаже обучението, добави отделна група за `GPTBot`, `ClaudeBot`, `Google-Extended`, `Applebot-Extended` с `Disallow: /`.

## 2. llms.txt

| Плъгин | Къде | Бележки |
|---|---|---|
| Yoast SEO | Yoast SEO > Settings > Site features > AI tools > llms.txt (в по-стари версии: Settings > Advanced > llms.txt) | Не работи на multisite. Има ръчен избор на страници ("Manual page selection"). |
| Rank Math | Rank Math SEO > Dashboard > модул **LLMS Txt** (toggle); после General Settings > Edit llms.txt | Избираш post types; noindex страниците се изключват. |
| AIOSEO | All in One SEO > Sitemaps > таб **LLMs.txt** | Включен по подразбиране. llms-full.txt и markdown опциите са в Pro. Има поле за изключване на страници. |

Ако менюто липсва: обнови плъгина. Ако имаш ръчно качен `llms.txt` в корена и плъгин, който генерира същия файл, ще се бият (има съобщения, че AIOSEO презаписва ръчен файл). Избери едното.

Какво да има в llms.txt: начална, услуги/категории, цени, за нас, контакти, 5 до 10 най-полезни статии. Без тагове, архиви, кошница, акаунт.

## 3. Structured data

- **Yoast** прави автоматично граф: Organization (или Person), WebSite, WebPage, Article с автор и дати. Настрой: Yoast SEO > Settings > **Site representation** (име, лого, социални профили). LocalBusiness иска платения Yoast Local SEO.
- **Rank Math**: Titles & Meta > Local SEO / Knowledge Graph за Organization/LocalBusiness; Schema генератор във всеки пост (Article, Product, FAQ и др.).
- **AIOSEO**: Search Appearance > Knowledge Graph; Schema генератор по страница.
- **FAQ**: Yoast FAQ блокът в Gutenberg и Rank Math FAQ блокът пускат FAQPage markup автоматично. Слагай го само при истински въпроси, видими на страницата.
- **WooCommerce**: WooCommerce и SEO плъгините правят Product markup. Провери, че цената, наличността и валутата (EUR) са верни в Rich Results Test.
- Custom JSON-LD без плъгин за schema: WPCode (или подобен) > нов snippet в `<head>` само за конкретната страница.

Пример за Organization (за услуги, B2B), ако плъгинът не го покрива:

```html
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "@id": "https://example.bg/#organization",
  "name": "Пример ООД",
  "url": "https://example.bg/",
  "logo": "https://example.bg/wp-content/uploads/logo.png",
  "email": "office@example.bg",
  "telephone": "+359 2 000 0000",
  "address": {"@type": "PostalAddress", "addressLocality": "София", "addressCountry": "BG"},
  "sameAs": ["https://www.linkedin.com/company/example"]
}
</script>
```

Не дублирай: ако Yoast вече пуска Organization, не добавяй втори. Провери с `curl -sL URL | grep -c 'application/ld+json'` и Rich Results Test.

## 4. Title, meta, canonical, hreflang, sitemap, индексиране

- Title, meta description, canonical: в кутията на SEO плъгина под всеки пост/страница. Шаблони за масови промени: Yoast > Settings > Content types; Rank Math > Titles & Meta.
- H1: обикновено заглавието на страницата. Page builder-ите (Elementor, Divi) често добавят втори H1 в hero секцията. Провери с curl.
- hreflang: прави го плъгинът за езици (WPML, Polylang, TranslatePress). Провери, че всяка BG страница сочи към EN двойката си и обратно.
- Sitemap: Yoast и Rank Math на `/sitemap_index.xml`, AIOSEO на `/sitemap.xml`. Вграденият `/wp-sitemap.xml` обикновено се изключва от плъгина.
- IndexNow: официалният плъгин "IndexNow" от Microsoft Bing, или модулът Instant Indexing в Rank Math. Yoast има IndexNow само в Premium (непроверено за текущата версия). Слагай само един.
- Google Search Console: най-лесно с плъгина Site Kit by Google; или meta таг в Yoast > Settings > General > Site connections; Rank Math > General Settings > Webmaster Tools. Bing: импорт от GSC.

## 5. Рендериране

WordPress почти винаги е ОК. Проверявай особено:
- Табове, акордеони, слайдери и "Load more", които зареждат текст с AJAX.
- Ревюта и цени от външни widget-и (iframe или JS).
- Cookie банери, които покриват съдържанието за ботове (не трябва да спират HTML-а).

```bash
curl -sL -A "Claude-SearchBot" https://example.bg/uslugi/ | grep -c "фраза от акордеона"
```

## 6. Съдържание, което се цитира (без разработчик)

- Gutenberg блокове: **Table** за сравнения и ценови таблици, **Details** за FAQ, **Heading** за въпроси като заглавия.
- Започвай всяка страница с отговор в 2 до 3 изречения, после детайлите.
- Цени в текст, в EUR, с "Актуално към: 11.2026". Ако цената е по оферта, напиши диапазон и от какво зависи.
- Автор с истинско име и био страница; видима дата на последна редакция (повечето теми показват "Updated").
- Страница за всеки отделен въпрос, който клиентите задават, а не 50 почти еднакви страници за градове.

## 7. Какво прави агентът и какво човек

Агентът работи през REST API с Application Password:

```bash
# Създава чернова; човек публикува
curl -s -u "euribia-agent:xxxx xxxx xxxx xxxx xxxx xxxx" \
  -X POST "https://example.bg/wp-json/wp/v2/posts" \
  -H "Content-Type: application/json" \
  -d '{"title":"Колко струва ...","content":"<p>Отговор...</p>","status":"draft"}'
```

| Задача | Агент | Човек |
|---|---|---|
| Одит с curl, четене на `/wp-json/wp/v2/pages` | Да | |
| Чернови на постове/страници в Gutenberg | Да | Преглед и Publish |
| Редакция на страници, правени с Elementor/Divi | Не (съдържанието е в meta полета) | Да |
| SEO полета (title/meta) на плъгина през REST | Непроверено, зависи от плъгина | Да, по таблица |
| Настройки на плъгини, robots.txt, llms.txt | | Администратор |
| Cloudflare, хостинг, GSC | | Да |

Какво искаме (минимум права): отделен потребител `euribia-agent` с роля **Editor** (не Administrator) и Application Password за него (Users > Profile > Application Passwords; иска HTTPS, някои security плъгини го изключват). Настройките на плъгините ги прави човек от екипа с временен Administrator или клиентът по наш списък. Плюс GSC "Full" и Bing достъп. Паролата за Application Password не я пишем в чата и в repo; пазим я в Keychain.

## 8. Чеклист

**Ден 1** (~2,5 ч)
- [ ] Кой SEO плъгин, кой кеш, кой security плъгин, Cloudflare ли е (15 мин)
- [ ] Settings > Reading: индексирането е разрешено (5 мин)
- [ ] robots.txt и тест с 9 user-agent-а (30 мин)
- [ ] Cloudflare AI Crawl Control, ако има (20 мин)
- [ ] llms.txt: включи в активния плъгин, прегледай списъка (30 мин)
- [ ] Поискай достъпи (15 мин)

**Седмица 1** (~7 ч)
- [ ] Site representation / Knowledge Graph и Organization/LocalBusiness (1 ч)
- [ ] Title/meta/H1 за топ 15 страници (3 ч)
- [ ] hreflang проверка при BG/EN (1 ч)
- [ ] IndexNow плъгин + Bing импорт (30 мин)
- [ ] Поправи грешните факти от baseline (1 до 2 ч)

**Месец 1** (~12 ч)
- [ ] Страница с цени, FAQ блок, сравнителна таблица (5 ч)
- [ ] 2 до 3 статии с отговор първо, автор и дата (5 ч)
- [ ] Изчисти дублиращи плъгини, прочисти кеша, повтори теста (2 ч)

## 9. Капани

- "Discourage search engines" остава включено след смяна на хостинг или staging.
- Два SEO плъгина = двойни title, двойна schema, два llms.txt.
- Кеш плъгин или Cloudflare показва стар robots.txt / llms.txt. Прочисти кеша след промяна.
- Физически robots.txt в корена бие настройките на плъгина.
- Elementor съдържанието не се вижда в REST `content`. Агентът не трябва да го презаписва.
- Staging копия (`staging.example.bg`) без noindex, които се индексират и дублират сайта.
- WooCommerce филтри и параметри (`?orderby=`) създават хиляди URL-и. Остави ги на canonical и noindex от плъгина.

## Източници

- https://yoast.com/help/enable-llmstxt/
- https://developer.yoast.com/features/llms-txt/functional-specification/
- https://yoast.com/help/yoast-seo-settings-site-features/
- https://rankmath.com/kb/llms-txt/
- https://aioseo.com/docs/how-to-create-an-llms-txt-using-all-in-one-seo/
- https://wordpress.org/support/topic/missing-llms-txt-option/
- https://developer.wordpress.org/rest-api/reference/posts/
- https://make.wordpress.org/core/2020/11/05/application-passwords-integration-guide/
- https://wordpress.org/plugins/indexnow/
- https://developers.cloudflare.com/ai-crawl-control/features/manage-ai-crawlers/
- https://www.helpnetsecurity.com/2026/07/02/cloudflare-ai-crawler-controls/
- https://developers.google.com/search/docs/appearance/ai-features
