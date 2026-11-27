# Wix и Wix Studio: playbook за AI видимост

Последна проверка: 11.11.2026

Добрата новина: Wix рендерира страниците на сървъра, прави sitemap, canonical и hreflang сам, праща IndexNow към Bing и на част от сайтовете генерира llms.txt. Нашата работа тук е основно проверка, structured data и съдържание. Лошата новина: менютата се преименуват често (старо "Marketing & SEO > SEO Tools", ново "SEO & GEO"), а Wix Studio и класическият Editor изглеждат различно. Ако не намираш меню, търси го по име в Wix Help Center, не гадай.

## 1. robots.txt и AI ботове

Къде: таблото на сайта > **SEO & GEO** > превърти до **Tools and settings** > **Robots.txt Editor** > **View File**.

- По подразбиране Wix разрешава всички ботове. Ако клиентът (или предишна агенция) е ползвал статията на Wix "Blocking AI crawlers", ще видиш редове `User-agent: GPTBot` / `Disallow: /`. Махни блокирането за търсещите и потребителските ботове (виж README за политиката).
- Бутон **Reset to Default** връща оригиналния файл. Ползвай го, ако файлът е объркан.
- Проверка на ниво страница: в SEO настройките на всяка важна страница (Advanced) има отметка **nosnippet**. Ако е включена, Google не ползва съдържанието като вход за AI Overviews. Трябва да е изключена.
- Wix сам не стои зад Cloudflare на клиента, така че WAF блокиране е рядко. Ако домейнът е проксиран през собствен Cloudflare акаунт на клиента (виж `cf-ray` в хедърите), провери AI Crawl Control там.

Пример, ако клиентът иска да откаже само обучението:

```
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
Disallow: /
```

Останалото оставяме както го е генерирал Wix (включително `Sitemap:` реда).

## 2. llms.txt

Wix генерира llms.txt автоматично, но не на всички сайтове. Условия по помощната статия на Wix: сайтът е с платен план и свързан собствен домейн, и индексирането от търсачки е включено. Блог на Wix споменава първо премиум eCommerce планове, затова наличността за конкретен план е "непроверено" докато не видиш менюто.

- Преглед: **SEO & GEO** > **Tools and settings** > **Go to llms.txt** > **View File**. Файлът е на `https://домейн.bg/llms.txt`.
- Редакция: **More Actions** > **Edit file** > **Continue** > **Save Changes**. Внимание: след ръчна редакция Wix спира да го обновява автоматично. **Reset to Default** връща автоматичния режим.
- Изключване: превключвател **Use your llms.txt file**.
- Нашата препоръка: остави автоматичния файл. Редактирай само ако има грешен факт или липсват ключови страници (цени, услуги, контакти), и тогава си запиши в задачите на клиента, че файлът вече е ръчен и трябва да се поддържа.
- Ако менюто липсва: няма как да качиш файл в корена на Wix сайт. В Wix App Market има приложения за llms.txt, но не ги слагаме без нужда.
- За агента: Wix има Llms Txt API (виж източниците), т.е. файлът може да се чете и сменя през API.

## 3. Structured data (JSON-LD)

Wix добавя автоматична markup за част от типовете страници (продукти, блог постове, събития). Ние добавяме Organization / LocalBusiness на началната страница и FAQ където има истински въпроси.

- Една страница: в Editor отвори страницата > **SEO** панела > таб **Advanced** > **Structured data markup** > **Add New Markup**. По-новите статии на Wix описват пътя през **SEO & GEO** > **SEO Settings** > **Edit by page type**.
- Ограничения по Wix: само JSON-LD, до 5 markup-а на страница, под 7000 знака всеки, без други HTML тагове освен `<script>` в началото и края.
- За шаблонни страници (продукти, блог): **SEO Settings** > тип страница > **Preview preset** > **Convert to custom markup**, ако трябва да промениш автоматичната markup. Custom markup замества тази на Wix.
- AI-генерирана structured data в Wix работи само за Wix Blog постове.
- Дали "Business Info" от Settings автоматично става LocalBusiness markup: непроверено. Провери с Rich Results Test преди да добавяш втора.

Пример за LocalBusiness (дентален кабинет, сложи го само на началната страница):

```json
{
  "@context": "https://schema.org",
  "@type": "Dentist",
  "@id": "https://example.bg/#business",
  "name": "Дентален център Пример",
  "url": "https://example.bg/",
  "telephone": "+359 56 000 000",
  "address": {
    "@type": "PostalAddress",
    "streetAddress": "ул. Александровска 1",
    "addressLocality": "Бургас",
    "postalCode": "8000",
    "addressCountry": "BG"
  },
  "openingHours": "Mo-Fr 09:00-19:00",
  "priceRange": "€€",
  "sameAs": [
    "https://www.facebook.com/example",
    "https://www.google.com/maps?cid=000000"
  ]
}
```

Правило: всичко в markup-а трябва да го има и във видимия текст на страницата (адрес, телефон, часове). Google изисква това изрично.

## 4. Title, meta, canonical, hreflang, sitemap, индексиране

- Title и meta description: в Editor > страницата > **SEO** панела > **SEO basics**. За масови промени: **SEO & GEO** > **SEO Settings** > **Edit by page type** (шаблони/patterns).
- H1: Wix шаблоните често ползват стил "Heading 1" за декоративен текст. Провери с `curl -sL URL | grep -o '<h1[^>]*>.*</h1>'`, че има точно един H1 и той казва какво продава страницата.
- Canonical: Wix го слага сам. Ръчна промяна е в Advanced SEO на страницата; пипаме само при дубли.
- Custom meta тагове: до 10 на страница, само `<meta>` и `<link>`.
- hreflang: с Wix Multilingual Wix сам добавя hreflang и x-default. SEO basics (title, description) се превеждат отделно за всеки език. Ръчно override на hreflang: непроверено.
- Sitemap: автоматично на `/sitemap.xml`. Не се пипа.
- IndexNow: Wix го поддържа по подразбиране за премиум сайтове (обявено с Bing, 2023). Нищо не правим.
- Google Search Console и Bing Webmaster Tools: Wix SEO Setup Checklist свързва Google и подава sitemap. Ако клиентът вече има GSC, искаме достъп като потребител там (виж т. 7). Ръчна верификация с meta таг: в **Tools and settings** има инструмент за верификация на сайта (точното име: непроверено). Bing: най-бързо е **Import from Google Search Console** в Bing Webmaster Tools.

## 5. Рендериране

Wix връща HTML със съдържанието от сървъра. Все пак проверяваме всяка ключова страница:

```bash
curl -sL -A "OAI-SearchBot" https://example.bg/uslugi | grep -c "фраза от страницата"
```

Ако е 0, причината обикновено е: текстът е картинка (често в Wix шаблоните), съдържанието е в lightbox или в приложение от App Market, което зарежда данни с JavaScript.

## 6. Съдържание, което се цитира (без разработчик)

- Отговор първо: всяка услуга започва с 2 до 3 изречения, които отговарят на "какво е, за кого, колко струва, къде". Пиши в текстово поле, не в картинка.
- Страница "Цени": истински цени в EUR в текст, с дата "Цени към 11.2026". Ако цената е "от", напиши от колко и от какво зависи.
- Сравнителни таблици: Wix има елемент за таблици/CMS таблици (точното име в Studio: непроверено). Ако няма, ползвай колони с текст. Таблица като картинка не върши работа.
- FAQ: Wix FAQ приложението или обикновени заглавия + текст. FAQ markup слагаме само ако въпросите са видими на страницата. Google показва FAQ rich results само за ограничен кръг сайтове, но структурата помага на ChatGPT и Perplexity.
- Блог: Wix Blog има автор и дата по подразбиране. Попълни профила на автора с истинско име и роля.

## 7. Какво прави агентът (Claude Code) и какво човек

| Задача | Агент | Човек |
|---|---|---|
| Четене на HTML, robots.txt, llms.txt, schema, тестове с curl | Да | |
| llms.txt през Wix Llms Txt API (Wix MCP: `CallWixSiteAPI`) | Да, след одобрение | |
| Чернови на блог постове през Wix Blog API | Да (като чернова) | Публикува |
| Robots.txt Editor | Чрез API: непроверено | Да, по нашия текст |
| Structured data markup на страница | | Да, поставя нашия JSON-LD |
| SEO basics (title/description) | Чрез API: непроверено | Да, по нашата таблица |
| Свързване на GSC / Bing | | Да |

Какво искаме от клиента (минимум права): покана като **Site Collaborator** с роля, която дава достъп до SEO и блога, но не до плащания и собственост (напр. "Website Manager"; точните имена на ролите: непроверено, виж екрана при поканата). Отделно: потребител в Google Search Console с права "Full" (не Owner) и достъп до Bing Webmaster Tools. Никога не искаме паролата на собственика.

## 8. Чеклист

**Ден 1** (общо ~2 ч)
- [ ] Разпознай платформата и плана (Premium? собствен домейн?) (10 мин)
- [ ] Robots.txt Editor: прочети, махни блокиране на търсещи ботове (20 мин)
- [ ] Тест с curl за 5 ключови страници и 9 user-agent-а (20 мин)
- [ ] Провери nosnippet и noindex на ключовите страници (20 мин)
- [ ] llms.txt: има ли меню, отвори файла, запиши какво липсва (15 мин)
- [ ] Поискай достъп: Collaborator, GSC, Bing (15 мин)

**Седмица 1** (общо ~6 ч)
- [ ] Organization/LocalBusiness JSON-LD на началната, проверка в Rich Results Test (1 ч)
- [ ] Таблица title/meta/H1 за топ 10 страници и поправки (2 ч)
- [ ] Bing Webmaster Tools: импорт от GSC, проверка на индексирани страници (30 мин)
- [ ] Поправи грешните факти, намерени в baseline (1 до 2 ч)

**Месец 1** (общо ~10 ч)
- [ ] Страница "Цени" в текст, с дата (2 ч)
- [ ] 3 страници за услуги с отговор първо + FAQ (4 ч)
- [ ] 1 сравнителна страница (ние срещу алтернативата, честно) (2 ч)
- [ ] Повторен тест с curl и проверка в GSC > Pages (1 ч)

## 9. Капани

- Безплатен план или без собствен домейн: няма llms.txt, а индексирането е по-слабо. Първо ъпгрейд.
- Ръчна редакция на llms.txt спира автоматичното обновяване. Записвай кога е редактиран.
- Текст в картинки и в банери: невидим за ботовете.
- Няколко H1 от шаблона.
- Приложения от App Market за ревюта/FAQ, които зареждат съдържанието с JavaScript: провери с curl.
- Wix Studio и класическият Editor имат различни менюта. Помощните статии понякога описват другия.
- "SEO Assistant"/AI подсказките на Wix пишат общи meta описания. Преглеждай ги.

## Източници

- https://support.wix.com/en/article/understanding-your-sites-llms-txt-file
- https://www.wix.com/studio/ai-search-lab/llms-txt
- https://dev.wix.com/docs/api-reference/business-management/marketing/seo/txt-file-server/llms-txt/introduction
- https://support.wix.com/en/article/editing-your-sites-robotstxt-file
- https://support.wix.com/en/article/blocking-ai-crawlers-from-your-site
- https://support.wix.com/en/article/adding-structured-data-markup-to-your-sites-pages-2546962
- https://support.wix.com/en/article/using-ai-generated-structured-data-for-blog-posts
- https://support.wix.com/en/article/wix-multilingual-seo
- https://support.wix.com/en/article/customizing-your-seo-settings-1420929
- https://blogs.bing.com/webmaster/september-2023/Wix-now-supports-IndexNow-for-Faster-Content-Indexing
- https://developers.google.com/search/docs/appearance/ai-features
