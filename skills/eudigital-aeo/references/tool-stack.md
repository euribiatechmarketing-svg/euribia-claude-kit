# Стек от инструменти (проверено по GitHub README, 11.11.2026)

Преди инсталация на клиентски данни: проверете лиценза и датата на последния commit в GitHub. README страниците не показват дата на последния commit, затова я гледайте в историята на commit-ите.

## Следене на видимостта в AI

**Основен инструмент от 11.11.2026: нашият `aeo-tracker`** (`~/Euribiatech/internal projects/AEO-SEO Service/aeo-tracker/`, вижте `operator-runbook.md`). Пита ChatGPT, Perplexity и Claude през OpenRouter (един ключ, вградено търсене на доставчика) и Gemini директно с Google Search. Мери споменаване, цитиране, конкуренти и с TypeSafe Jev "препоръчан". Без Docker и сървър, плащане на заявка, около 2-3 цента на отговор. Elmo остава опция, ако ни трябва уеб интерфейс за много марки.

| Инструмент | Лиценз | Как работи | Реална цена и риск |
|---|---|---|---|
| **Elmo** (`elmohq/elmo`) | MIT | `npm install -g @elmohq/cli`, после `elmo init`, после `elmo compose up -d`. Нужни са Docker и PostgreSQL. Следи ChatGPT, Google AI Mode, AI Overviews, Gemini, Perplexity, Copilot (през Cloro) и Claude, Grok през API. Агенции могат да следят много марки на едно място | Безплатният код не е безплатно ползване: препоръчаната настройка иска платени ключове за **Cloro** (скрейпва асистентите) и **OpenRouter** (оценка на споменавания и тон). Цени не са публикувани в README. Облачната версия Elmo Cloud започва от 29 $ на месец |
| **OneGlanse** (`aryamantodkar/oneglanse`) | MIT | Пуска въпросите през истинските сайтове на асистентите (Camoufox с Playwright), с ваши собствени акаунти. `cp .env.example .env`, ключ за модел за анализ, `pnpm local` на машина с работен плот. За сървър: `pnpm self-host` | Иска собствени акаунти във всеки асистент и резидентен прокси за сървърно пускане. README споменава "bot-detection handling", а за условията на ползване на доставчиците не казва нищо. Автоматизирано пускане през потребителски интерфейс може да нарушава условията им. Не го пускаме върху клиентски акаунти. Преди продуктово ползване: прочитаме условията на OpenAI, Google, Anthropic, Perplexity |
| limelit-co/open | Apache-2.0 | Един Go файл | Резервен вариант, да се провери README |
| danishashko/geo-aeo-tracker | MIT | ChatGPT, Perplexity, Gemini, Copilot, Google AI Mode | Да се провери README |

**Решение за пилота:** Elmo е основният кандидат, защото ползва платени API за скрейпване, а не наши акаунти. Пилотираме го с 3 клиента и записваме реалния месечен разход на Cloro и OpenRouter на клиент. Ако разходът е неприемлив, остава ръчно пускане на ядрото (30 въпроса × 5 пъти × 6 асистента е твърде много за ръка, така че режем до 10 ключови въпроса) или платен тракер за клиенти, на които се струва. OneGlanse се тества само на нашите собствени сайтове с наши акаунти, докато не изясним условията.

## Одит

| Инструмент | Лиценз | Команди |
|---|---|---|
| **geo-optimizer-skill** (`Auriti-Labs`) | MIT | Без инсталация: `uvx --from geo-optimizer-skill geo audit --url https://сайт`. Резултат 0-100 в девет категории (Google AI readiness, robots.txt, schema, съдържание, марка и ентитет, мета тагове, llms.txt, сигнали, AI discovery). `geo fix --url …` показва какво ще генерира, `--apply` записва. `geo citations --brand "…" --domain …` иска собствен API ключ. Като MCP: `pip install "geo-optimizer-skill[mcp]"` и `claude mcp add geo-optimizer -- geo-mcp`, или като плъгин чрез `uv` |
| geo-lint | MIT | 92 правила за SEO, GEO и качество на съдържанието |
| SiteOne Crawler, SEOnaut, LibreCrawl | отворен код | Технически обход на целия сайт. Съпоставяме с `seo-audit` |
| Lighthouse | Apache-2.0 | Скорост, достъпност, Core Web Vitals |

Резултатът на geo-optimizer е сигнал, не цел. Не обещаваме клиент "86 точки", а затваряме конкретните проблеми от доказателствата.

Известни грешки на geo-optimizer (пилот 11.11.2026):
- Отчита "AI crawlers blocked by CDN" дори когато ботът получава HTTP 200, само защото размерът на отговора е различен. Всяко такова предупреждение се проверява с `curl -A "<бот>" -o /dev/null -w "%{http_code}"` и сравнение на заглавието.
- Препоръчва `/.well-known/ai.txt`, `/ai/summary.json`, `/ai/faq.json`, `/ai/service.json`. Това не са установени стандарти. Не ги правим и не ги продаваме.
- На тази машина няма uv по подразбиране: `pip3 install --user uv`, после `export PATH=$(python3 -m site --user-base)/bin:$PATH`. Системният Python е 3.9 и дава предупреждение за LibreSSL, което не пречи.

## Файлове и schema

- `llms.txt`: спецификация на llmstxt.org. Не е изискване на Google. Правим го, защото е евтино и помага на част от асистентите и агентите.
- `pricing.md`: само ако клиентът има публични цени и ги поддържа актуални.
- aeo.js няма лиценз в GitHub: само вътрешно ползване, не го доставяме на клиенти.
- JSON-LD: skill `schema`. Проверка с Rich Results Test.

## Позиции и анализ

Google Search Console (единственият официален източник за Google, без специален отчет за AI), Bing Webmaster Tools с IndexNow, SerpBear за позиции, Umami или Plausible за трафик. В анализа има отделен канал за AI асистентите.

## Хостинг

Docker сървър (Hostinger или Hetzner) за Elmo и SerpBear. Секретите (OpenRouter, Cloro, API ключове) идват от променливи на средата или Keychain, никога във файл в репото.
