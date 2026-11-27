# Shopify: playbook за AI видимост

Последна проверка: 11.11.2026

Shopify прави много сам: sitemap, canonical, Product markup в повечето теми, hreflang с Markets, и от май 2026 сервира `/agents.md`, `/llms.txt` и `/llms-full.txt` по подразбиране. Нашата работа: да проверим, че нищо не е блокирано, да поправим продуктовите текстове (най-често копирани от доставчика) и да добавим страниците, които AI асистентите цитират: цени, доставка, връщане, сравнения.

## 1. robots.txt и AI ботове

Shopify генерира `/robots.txt` сам. Той вече забранява кошница, checkout, акаунт и admin. По третични източници основните AI ботове не са блокирани по подразбиране, но това се проверява на живо за всеки магазин: `curl -s https://магазин.bg/robots.txt`.

Промяна става само с шаблон `robots.txt.liquid`:
1. Admin > **Online Store** > **Themes** > при активната тема **...** > **Edit code**.
2. **Add a new template** > тип **robots** > създава `templates/robots.txt.liquid`.
3. Преди публикуване запази копие на текущия `/robots.txt` и сравни с новия резултат (така препоръчва Shopify).

Пример: запазваме всички правила на Shopify и отказваме само обучението.

```liquid
{% for group in robots.default_groups %}
  {{- group.user_agent }}
  {%- for rule in group.rules -%}
    {{ rule }}
  {%- endfor -%}
  {%- if group.sitemap != blank -%}
    {{ group.sitemap }}
  {%- endif -%}
{% endfor %}

User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Google-Extended
User-agent: Applebot-Extended
Disallow: /
```

Ако клиентът не иска да отказва нищо, НЕ създавай шаблона. Шаблонът изключва автоматичните бъдещи промени на Shopify в robots.txt и трябва да се поддържа.

CDN: Shopify стои зад собствената си инфраструктура и магазинът не управлява WAF. Ако домейнът е проксиран през Cloudflare акаунт на клиента (рядко), провери AI Crawl Control там. Отделно: Shopify има "Agentic Storefronts" настройки за участие в AI канали; те не заместват robots.txt. Наличност и меню за български магазини: непроверено.

## 2. llms.txt и agents.md

От changelog-а на Shopify (28.05.2026): магазинът сервира `/agents.md` по подразбиране, а `/llms.txt` и `/llms-full.txt` показват същото съдържание.

Шаблони (Online Store > Themes > Edit code > Add a new template):

| Шаблон | Управлява | Ред на търсене |
|---|---|---|
| `templates/agents.md.liquid` | `/agents.md` и по подразбиране другите два | основен |
| `templates/llms.txt.liquid` | само `/llms.txt` | ако липсва, ползва agents.md шаблона, после default на Shopify |
| `templates/llms-full.txt.liquid` | само `/llms-full.txt` | същото |

Нашата препоръка:
1. Първо прочети какво сервира Shopify: `curl -s https://магазин.bg/llms.txt`.
2. Ако съдържанието е вярно, остави го.
3. Ако липсват важни страници (доставка, връщане, цени, гаранция) или има грешни факти, редактирай `agents.md.liquid`, така трите файла остават еднакви. Отделен `llms.txt.liquid` само ако наистина трябва различно съдържание.

Алтернативи без код: Yoast SEO for Shopify (Settings > Advanced > llms.txt) или приложения като "LLMs, Robots and Agents Editor". Старите съвети за "app proxy" хакове вече не са нужни.

## 3. Structured data

- **Product**: Online Store 2.0 темите (Dawn и наследниците) пускат Product JSON-LD чрез Liquid филтъра `structured_data`. Провери с Rich Results Test на 3 продукта: цена, валута, наличност, марка, GTIN ако има.
- **Organization**: някои теми го пускат на началната страница, други не. Ако липсва, добави snippet в `layout/theme.liquid` само при `template.name == 'index'`.
- **FAQ, Article**: блогът на Shopify има автор и дата; Article markup зависи от темата. FAQ: секция в темата или приложение, само с видими въпроси.
- Приложения за schema има много. Слагай приложение само ако темата не покрива нужното, и провери, че няма двоен Product.

Пример за допълване на Product (ако темата няма brand/gtin), в `sections/main-product.liquid` или snippet:

```liquid
<script type="application/ld+json">
{
  "@context": "https://schema.org",
  "@type": "Product",
  "name": {{ product.title | json }},
  "brand": {"@type": "Brand", "name": {{ product.vendor | json }}},
  "sku": {{ product.selected_or_first_available_variant.sku | json }},
  "description": {{ product.description | strip_html | truncate: 500 | json }},
  "offers": {
    "@type": "Offer",
    "price": {{ product.selected_or_first_available_variant.price | money_without_currency | replace: ',', '.' | json }},
    "priceCurrency": {{ cart.currency.iso_code | json }},
    "availability": "https://schema.org/{% if product.available %}InStock{% else %}OutOfStock{% endif %}",
    "url": {{ request.origin | append: product.url | json }}
  }
}
</script>
```

Внимание: формат на цената зависи от настройките за валута (EUR от 01.01.2026). Тествай в Rich Results Test, преди да пуснеш. Ако темата вече има Product markup, не добавяй втори, а поправи съществуващия.

## 4. Title, meta, canonical, hreflang, sitemap, индексиране

- Начална страница: **Online Store** > **Preferences** > Title and meta description.
- Продукт, колекция, страница, статия: долу в редактора секция **Search engine listing** > **Edit** (title, description, URL handle).
- H1: в темата обикновено е името на продукта/колекцията. Провери с curl, че логото не е H1.
- Canonical: Shopify го слага сам. URL-и от типа `/collections/x/products/y` сочат към `/products/y`. Не пипай.
- hreflang: автоматично с Shopify Markets + превод (Translate & Adapt). Провери на живо, че BG и EN версиите се сочат взаимно.
- Sitemap: `/sitemap.xml`, автоматично.
- IndexNow: вградена поддръжка не е потвърдена (източниците се разминават: непроверено). Има приложения, напр. "InstaIndex: IndexNow for Bing". Не е приоритет.
- Google Search Console: ако домейнът е при Shopify, DNS TXT запис от **Settings** > **Domains**; иначе meta таг в `layout/theme.liquid`. Bing: импорт от GSC.

## 5. Рендериране

Темите на Shopify рендерират на сървъра (Liquid). Рискове:
- Ревюта (Judge.me, Loox и др.), размери, FAQ и "свързани продукти" от приложения, които се зареждат с JavaScript. Ревютата често не са в HTML.
- Headless магазини (Hydrogen или друг frontend): там важи `custom.md` или `vibe-coded.md`.

```bash
curl -sL -A "OAI-SearchBot" https://магазин.bg/products/primer | grep -c "текст от описанието"
```

## 6. Съдържание, което се цитира (без разработчик)

- Продуктово описание: първите 2 изречения казват какво е, за кого, основната разлика. Не копирай текста на доставчика.
- Страници (Online Store > Pages): "Доставка и срокове", "Връщане", "Гаранция", "Как да изберем ...". Ясни числа: срок в дни, цена на доставка в EUR, праг за безплатна доставка.
- Сравнителна таблица: в редактора на страници има бутон за таблица (rich text editor). Сравнявай честно, с дата.
- Блог: статии "Как да изберем X", "X срещу Y", с автор и дата.
- Metafields + секции в темата за FAQ на продукт, ако темата позволява (зависи от темата).

## 7. Какво прави агентът и какво човек

| Задача | Агент | Човек |
|---|---|---|
| Одит с curl, четене на `/products.json`, robots, llms.txt | Да | |
| Текстове на продукти, SEO полета (Admin GraphQL `productUpdate`) | Да, след одобрение на таблица | Одобрява |
| Страници и статии като чернова/скрити | Да | Публикува |
| Шаблони (`robots.txt.liquid`, `agents.md.liquid`, schema snippet) | Да, в КОПИЕ на темата (Shopify CLI `shopify theme push --unpublished`) | Преглежда и публикува темата |
| Инсталиране на приложения, Markets, домейни, GSC | | Да |

Достъп (минимум права):
- От 01.01.2026 не могат да се създават нови "legacy custom apps" от админа. Нов достъп до Admin API става с приложение от Shopify Dev Dashboard и OAuth/client credentials, не със статичен токен. Scopes само каквото трябва: `read_products`, `write_products`, `read_content`, `write_content`, `read_themes`, `write_themes` (точните имена на scopes за страници/блог в текущата API версия: непроверено, провери в документацията преди заявка).
- За работа по темата: collaborator request от наш Partner акаунт само с права за Themes, Products, Pages/Blog posts. Без Orders, Customers, Finances.
- GSC "Full" и Bing достъп.

## 8. Чеклист

**Ден 1** (~2 ч)
- [ ] `/robots.txt`, `/llms.txt`, `/agents.md`: прочети и запиши какво има (20 мин)
- [ ] Тест с 9 user-agent-а и curl за 3 продукта и 2 колекции (30 мин)
- [ ] Rich Results Test на 3 продукта и началната (20 мин)
- [ ] Проверка: магазинът не е с парола, няма noindex в темата (10 мин)
- [ ] Поискай достъпи (collaborator, GSC, Bing) (20 мин)

**Седмица 1** (~8 ч)
- [ ] Organization markup на началната, ако липсва (1 ч)
- [ ] SEO полета за топ 20 продукта и топ 5 колекции (3 ч)
- [ ] Страници "Доставка", "Връщане" с числа (2 ч)
- [ ] agents.md.liquid, ако автоматичното съдържание е непълно (1 ч)
- [ ] Bing импорт, sitemap в GSC (30 мин)

**Месец 1** (~12 ч)
- [ ] Пренапиши описанията на топ 20 продукта (6 ч)
- [ ] 2 ръководства за избор + 1 сравнение (4 ч)
- [ ] Ревютата: провери дали са в HTML; ако не, говори с клиента за приложение с server-side ревюта (1 ч)
- [ ] Повторен одит (1 ч)

## 9. Капани

- Шаблон `robots.txt.liquid` без нужда: спира автоматичните корекции на Shopify.
- Двоен Product markup (тема + приложение).
- Описания, копирани от доставчика: еднакви на десетки сайтове, асистентите цитират другите.
- Цени и наличности само в JavaScript от приложения (варианти, B2B цени).
- Магазин с парола (Online Store > Preferences > Password protection) при "soft launch".
- Markets с подпапки (`/en/`) без превод на SEO полетата: EN страници с BG title.
- Много приложения, които инжектират JS и забавят страницата.

## Източници

- https://shopify.dev/docs/storefronts/themes/seo/robots-txt
- https://shopify.dev/changelog/customize-llmstxt-llms-fulltxt-and-agentsmd
- https://shopify.dev/docs/storefronts/themes/architecture/templates/llms-txt-liquid
- https://yoast.com/help/enable-llms-txt-yoast-seo-shopify/
- https://shopify.dev/docs/api/liquid/filters/structured_data
- https://community.shopify.dev/t/starting-january-1-2026-you-will-not-be-able-to-create-new-legacy-custom-apps-this-will-not-impact-any-existing-apps/26798
- https://shopify.dev/docs/api/admin-graphql
- https://apps.shopify.com/instaindex
- https://developers.google.com/search/docs/appearance/ai-features
