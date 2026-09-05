# Task 8: Контент-заміна плейсхолдерів і реліз — план реалізації

> **Для агентних воркерів:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) або superpowers:executing-plans. Кроки — checkbox (`- [ ]`). **Код у цей план не входить** — лише процедури заміни контенту, деплою, QA та приймання. Реалізація сайту вже виконана в Tasks 1–7.

**Goal:** Підставити всі відкриті плейсхолдери реальними даними замовника, прогнати pre-release content QA, задеплоїти обидва домени (`fidesa.com.ua` + `fidesa.agency`) з DNS/HTTPS/hreflang і закрити Definition of Done з `about.md` §9 та майстер-плану §10.

**Architecture:** Статичний білд уже зібраний (Tasks 1–7). Task 8 — операційний релізний шар: контент-гейты → dual-domain publish → Search Console / smoke / rollback. Без зміни стеку, без CMS, без нових фіч.

**Tech Stack (контекст релізу):** статичний HTML/CSS/JS у `public/uk-site/` і `public/en-site/` (або еквівалент після збірки); CDN-хостинг (Cloudflare Pages / Netlify / S3+CloudFront — як зафіксовано в Task 1/7); DNS у реєстраторі доменів; Google Search Console.

**Джерела правди:**

| Документ | Що брати |
|---|---|
| `about.md` §9 | Результат розробки (приймання замовником) |
| Майстер-план §8 | Контент-активи і статуси |
| Майстер-план §9 Task 8 | Короткий чекліст задачі |
| Майстер-план §10 | DoD (10 пунктів) |
| Майстер-план §12 | Відкриті плейсхолдери |
| Майстер-план §0A.7 | Диференціація vs конкурентів (має бути вже checked у Task 7) |
| `logo.svg` | Бренд-кольори вже зафіксовані — **не блокує** |

## Global Constraints (успадковані)

- Бренд **Fidesa** only; **жодних** згадок DNA325 / материнських структур.
- Конверсія B2B — **лише Calendly**; **немає** публічних цін/пакетів/%.
- `fidesa.com.ua` = UK only; `fidesa.agency` = `/en/` (+ redirect з `/`).
- Testimonials лишаються **порожньою заглушкою** (не вигадувати відгуки на релізі).
- Логотип і HEX уже є — не чекати на них.
- Не чіпати Tasks 1–7, крім точкових правок контенту/URL плейсхолдерів.

---

## 0. Передумови (вхід у Task 8)

Перед стартом підтвердити, що Tasks 1–7 закриті:

- [ ] Task 7 Done: Lighthouse mobile ≥ 95 / desktop ≥ 98 на staging; §0A.7 усі пункти checked; axe smoke OK.
- [ ] Staging URL(и) доступні для UK і EN білдів окремо.
- [ ] У репозиторії є робочі плейсхолдери з §12 (пошук по коду/контенту: `EMAIL_PLACEHOLDER`, `CALENDLY`, демо-вакансії).
- [ ] Замовник (або власник бренду) доступний для надання: email, Calendly URL, фото Валерії, рішення по вакансіях, юр. дані для Privacy (якщо потрібні).

**Блокери релізу vs non-блокери** — див. §1–§2 нижче.

---

## 1. Таблиця всіх плейсхолдерів

> Статуси на момент написання плану. Оновлювати колонку «Статус» у ході Task 8.

| # | Плейсхолдер / актив | Де використовується | Статус зараз | Хто надає / підставляє | Блокує прод? | Примітка |
|---|---|---|---|---|---|---|
| P1 | `[EMAIL_PLACEHOLDER]` | Contacts (UK+EN), Privacy, `llms.txt` (обидва домени), можливо footer / mailto apply | **Відкритий** | **Замовник** надає адресу → **агент/підрядник** підставляє в усі входження одним проходом | **Так** | Один і той самий робочий email на обох доменах, якщо не сказано інакше |
| P2 | `[CALENDLY_URL]` / Calendly event link | Primary CTA, lazy widget Contacts, fallback `<a>` без JS, sticky mobile CTA | **Відкритий** | **Замовник** створює/дає публічний URL → **агент** підставляє в конфіг/partials/`calendly-lazy.js` data-атрибути | **Так** | Перевірити, що лінк відкривається без логіну; тип event = discovery/call |
| P3 | Фото Валерії | Секція Team (UK+EN): 1x/2x WebP (+ fallback), `alt` | **Потрібне** (майстер §8) | **Замовник** надає оригінал → **агент** стискає ≤80 KB WebP, кладе в `assets/images/`, оновлює `src`/`srcset` | **Так** (для приймання §9 / about §7) | `alt`: UK `Валерія, засновниця Fidesa` / EN `Valeriia, Founder of Fidesa` |
| P4 | Фінальне біо Валерії | Team UK+EN | **Чернетка** з §3.1/§3.2 | **Замовник** затверджує або править → **агент** синхронізує UA↔EN | Бажано перед прод | Не вигадувати факти поза затвердженим текстом |
| P5 | Реальні вакансії (заміна 3 демо) | `content/uk/vacancies/*`, `content/en/vacancies/*`, list/detail, JobPosting, sitemap | **Демо-плейсхолдери** (§3.3) | **Замовник** дає реальні ролі **або** письмово дозволяє залишити/прибрати демо → **агент** замінює/видаляє | **Так** (рішення обов’язкове) | Варіанти: A) 1–N реальних; B) прибрати всі й empty state; C) тимчасово лишити демо з явним маркуванням — **не рекомендується** без згоди |
| P6 | Юридична назва / ЄДРПОУ / реквізити | Privacy UK+EN, опційно footer | **Відкритий** (§12) | **Замовник** — якщо юрособа вже є; якщо ні — Privacy лишає «Fidesa» + email без ЄДРПОУ | Умовно | Не вигадувати ЄДРПОУ. Якщо даних немає — короткий Privacy без фейкових реквізитів |
| P7 | CTO ПІБ / фото | Team | **Не обов’язково** на старті | Замовник пізніше | **Ні** | Trust line без ПІБ уже в копірайті; місце reserved |
| P8 | Testimonials контент | Модуль-заглушка | **Порожній — так і треба** | — | **Ні** | Не заповнювати вигаданими відгуками |
| P9 | Wordmark «Fidesa» у SVG | Header / hero | **Текстовий UI** (§12) | Дизайн-гайд пізніше | **Ні** | Знак з `logo.svg` + CSS wordmark |
| P10 | Hero visual (якщо ще плейсхолдер) | Hero background | Залежить від Task 2/7 | Замовник / агент | Якщо на staging уже фінальний — **Ні** | Не стокові «солдати»; якщо тимчасовий navy gradient прийнятий у Task 7 — зафіксувати як v1 |

### Правила підстановки

1. **Один прохід grep/search** по всьому репо після отримання значень: жодного залишку `PLACEHOLDER`, `example.com`, `calendly.com/acme`, `you@email`.
2. **UA і EN одночасно** — ніколи не підставляти email/Calendly лише на одному домені.
3. **Не комітити** зайві персональні дані поза узгодженим публічним email/фото/біо.
4. Після підстановки — перезбірка статичного білду (якщо контент іде з MD/JSON у `content/`).

---

## 2. Що вже готове (не блокує реліз)

| Актив | Статус | Дія в Task 8 |
|---|---|---|
| `logo.svg` (корінь) + копії в `assets/brand/` (favicon, on-dark) | **Готово** з Task 1 | Лише візуальний smoke: logo у header/hero на прод |
| HEX токени `#2E4259` / `#424443` (+ похідні §0) | **Готово** | Не змінювати палітру «на всяк випадок» |
| Дизайн-токени / шрифт / layout | Tasks 1–2 | Без редизайну в Task 8 |
| Копірайт секцій (робочі тексти) | Tasks 2–3 | Редагувати лише за правками замовника (біо, Privacy) |
| Blog 3 пости | Task 5 | Не блокує; контент-QA на термінологію |
| Privacy / llms / robots / sitemap каркас | Task 6 | Підставити email (+ юр. дані за наявності) |
| Perf / §0A.7 / a11y | Task 7 | Повторити короткий smoke на **проді**, не переробляти оптимізації |

**Висновок:** відсутність фінального SVG-wordmark, CTO-фото, testimonials і (за згодою) розширеного юрблоку **не зупиняє** реліз. Блокують лише P1–P3 і чітке рішення по P5.

---

## 3. Dual-domain deploy checklist

### 3.1. Артефакти білду

| Домен | Корінь деплою | Очікувана мова / URL |
|---|---|---|
| `fidesa.com.ua` | `public/uk-site/` (або еквівалент) | `lang="uk"`, `/`, `/vacancies/`, `/blog/`, … |
| `fidesa.agency` | `public/en-site/` | `/` → **302/301** на `/en/`; контент під `/en/…` |

- [ ] Окремі два проєкти/сайти в CDN (не один root з плутаниною мов).
- [ ] Після content-замін — чистий production build без source maps у публічному HTML (якщо так налаштовано в Task 7).
- [ ] Перевірити, що `robots.txt` і `sitemap.xml` у **кожному** корені вказують абсолютні URL **свого** домену.

### 3.2. DNS

- [ ] `fidesa.com.ua` — A/AAAA або CNAME на CDN згідно інструкції хостингу.
- [ ] `fidesa.agency` — окремий CNAME/A на другий проєкт.
- [ ] `www` — політика: або redirect `www` → apex, або навпаки; **однаково** для обох доменів; один canonical host.
- [ ] TTL: перед зміною можна знизити; після стабілізації — стандартний.
- [ ] Дочекатися пропагації; перевірити `dig` / DNS checker з кількох резолверів.

### 3.3. HTTPS / TLS

- [ ] Сертифікати видані для apex + www (якщо www використовується) на обох доменах.
- [ ] Force HTTPS (HTTP → HTTPS 301).
- [ ] HSTS увімкнено на CDN (після впевненості в HTTPS) — як у майстер-плані §6.3.
- [ ] Немає mixed content (http:// у CSS/JS/img на HTTPS-сторінках).

### 3.4. Redirects і canonical поведінка

| З | На | Тип | Домен |
|---|---|---|---|
| `http://…` | `https://…` | 301 | обидва |
| `www` ↔ apex | обраний canonical | 301 | обидва |
| `https://fidesa.agency/` | `https://fidesa.agency/en/` | 302 або 301 (як у Task 3) | agency |
| Застарілі staging URL | не індексувати | robots/noindex на staging | staging |

- [ ] UA↔EN лінки в header/footer зберігають path (`/vacancies/foo` ↔ `/en/vacancies/foo`).
- [ ] Canonical на кожній сторінці вказує на «свій» фінальний URL (не staging, не протилежний домен).
- [ ] Немає ланцюжків redirect > 1 зайвого хопа.

### 3.5. Порядок викладки

1. Задеплоїти **staging** з фінальними плейсхолдерами → content QA (§6).
2. Задеплоїти **prod** agency + com.ua (можна паралельно після DNS ready).
3. DNS cutover (якщо сайти вже на CDN — лише перемикання CNAME).
4. Smoke (§8) протягом 15–30 хв після cutover.
5. Search Console (§4).

---

## 4. Search Console / hreflang — кроки верифікації

### 4.1. Власність доменів

- [ ] Додати property **Domain** або URL-prefix для `fidesa.com.ua`.
- [ ] Додати окремо для `fidesa.agency`.
- [ ] Підтвердити DNS TXT (або HTML-файл / meta — що зручніше на статиці; DNS TXT надійніший для domain property).
- [ ] Не лишати verification-файли з чужих тестових акаунтів.

### 4.2. Sitemap

- [ ] Надіслати `https://fidesa.com.ua/sitemap.xml`.
- [ ] Надіслати `https://fidesa.agency/sitemap.xml` (URL всередині — з `/en/…` де треба).
- [ ] Переконатися, що в sitemap немає staging, `localhost`, дублів www/apex.

### 4.3. hreflang (майстер §5.1)

Очікувана матриця для пари сторінок:

| Сторінка | `hreflang="uk"` | `hreflang="en"` | `hreflang="x-default"` |
|---|---|---|---|
| Home | `https://fidesa.com.ua/` | `https://fidesa.agency/en/` | `https://fidesa.agency/en/` |
| Vacancies list | `https://fidesa.com.ua/vacancies/` | `https://fidesa.agency/en/vacancies/` | `https://fidesa.agency/en/` |
| Аналогічно blog / privacy / vacancy slug / post slug | дзеркало path | дзеркало `/en{path}` | x-default → EN home (міжнародний дефолт) |

- [ ] View-source на 3–5 ключових URL з кожного домену: є взаємні `link rel="alternate" hreflang=…`.
- [ ] Немає `hreflang` на неіснуючі URL.
- [ ] Після індексації: Search Console → International Targeting / Page indexing звіти (з’являться із затримкою; зафіксувати дату submit).
- [ ] URL Inspection на home UK і home EN: canonical = очікуваний; покриття без «Redirect error» на agency `/`.

### 4.4. robots / AI crawlers (коротко на релізі)

- [ ] `robots.txt` обох доменів дозволяє Googlebot + GPTBot, ClaudeBot, PerplexityBot, Google-Extended.
- [ ] `llms.txt` доступний за `https://fidesa.com.ua/llms.txt` і `https://fidesa.agency/llms.txt` з підставленим email (без `[EMAIL_PLACEHOLDER]`).

---

## 5. Final acceptance — about.md §9 і майстер-план DoD §10

### 5.1. about.md §9 «Результат розробки»

| # | Вимога ТЗ | Як перевірити | Статус |
|---|---|---|---|
| A1 | Адаптивний сайт (mobile + desktop) | Ручний прохід 375 / 768 / 1440 на проді; Task 7 пристрої | [ ] |
| A2 | UA/EN з ручним і геолокаційним перемиканням | com.ua без внутрішнього switcher; agency — UA-банер + UA\|EN лінки; localStorage dismiss | [ ] |
| A3 | Окрема сторінка вакансій з фільтрами | `/vacancies/` і `/en/vacancies/`; filters direction/location/format | [ ] |
| A4 | Блог з тегами та кількома авторами | list + post + tag; byline Валерія / Team | [ ] |
| A5 | Базове SEO/AI з about §6 | schema Organization/JobPosting/BreadcrumbList; hreflang; llms.txt; robots AI; контент у HTML | [ ] |
| A6 | Відповідність кольоровій/шрифтовій логіці логотипу | Візуально navy `#2E4259` + graphite `#424443`; logo.svg у UI | [ ] |

### 5.2. Майстер-план §10 Definition of Done

| # | DoD | Перевірка на проді | Статус |
|---|---|---|---|
| D1 | Два домени з мовною логікою | DNS+HTTPS+redirect `/`→`/en/`; path-preserving UA↔EN | [ ] |
| D2 | Усі секції головної; testimonials empty stub | Home UK/EN: Hero→…→Contact; empty testimonials copy | [ ] |
| D3 | Вакансії з фільтрами; блог з тегами й авторами | Як A3–A4 | [ ] |
| D4 | Немає DNA325; немає публічних цін/пакетів | Content QA §6 | [ ] |
| D5 | Чистий HTML; llms; schema; hreflang; robots AI | view-source + файли в корені | [ ] |
| D6 | Strict defence + §0A.7 | Скрін прод vs конкуренти; чекліст Task 7 re-confirm | [ ] |
| D7 | Vacancies §0A.5 + mobile стек | Немає client logos / salary filter / chat; стек-картки | [ ] |
| D8 | Mobile UX §2.3 без критичних дефектів | CTA видимий; touch ≥44px; no overflow | [ ] |
| D9 | Lighthouse mobile ≥ 95 | Прогін на **prod** URL (або staging=prod-identical); Calendly лише після кліку | [ ] |
| D10 | Тексти UA/EN узгоджені | Парний прочитання §6.2 | [ ] |

**Done when (Task 8):** усі A1–A6 і D1–D10 checked; плейсхолдери P1–P3 закриті; по P5 є задокументоване рішення замовника; Search Console properties + sitemaps надіслані.

---

## 6. Pre-release content QA

Виконувати на staging з **вже підставленими** P1–P3 (і після рішення P5), до DNS cutover.

### 6.1. UA / EN parity

- [ ] Кожна секція home UK має відповідник EN (заголовки, Q/A, 4 кроки процесу, 2 security підблоки, Team, testimonials stub, Contact).
- [ ] Однакові факти (спеціалізація, відсутність generalist IT, security disclaimer) — без суперечностей між мовами.
- [ ] Вакансії: той самий набір slugів UK/EN (або свідоме empty state з обох боків).
- [ ] Blog: 3 пости × 2 мови; теги узгоджені (`defence-tech`, …).
- [ ] Privacy: ті самі категорії даних / контакти запитів; email = прод.
- [ ] Nav labels локалізовані; domain switch: на com.ua лише EN→agency; на agency — UA→com.ua.

### 6.2. Заборонений контент

- [ ] Пошук по всьому білду (HTML + MD + JSON + llms + privacy): **немає** `DNA325`, `dna325`, варіантів материнського бренду.
- [ ] Немає публічних цін, «% комісії», «пакетів», PDF прайсу, Sourcing/Recruiting % як у конкурентів.
- [ ] Немає community/QR/events/salary survey / client logo wall / hero lead-form / resume-upload на home (антипатерни §0A).
- [ ] Testimonials: лише empty state, без фейкових імен клієнтів.

### 6.3. Плейсхолдери і биті лінки

- [ ] Grep: немає `EMAIL_PLACEHOLDER`, `CALENDLY_URL`, `TODO`, `lorem`, `example@`, `tbd`.
- [ ] Усі internal лінки 200 на staging.
- [ ] Calendly URL відкривається в новій вкладці / lazy iframe після взаємодії.
- [ ] Mailto apply (якщо є) веде на фінальний email.
- [ ] Зображення Валерії: коректні розміри, `width`/`height`, не ламає CLS.
- [ ] OG-image і favicon віддаються 200 на обох доменах.

### 6.4. Короткий візуальний / брендовий прохід

- [ ] Бренд Fidesa читається в першому екрані (logo + wordmark).
- [ ] Палітра не «з’їхала» на cream/amber/yellow.
- [ ] CTO блок без вигаданого ПІБ.

---

## 7. Checkbox steps + DoD задачі

### Фаза A — Збір даних від замовника

- [ ] **A.1** Запросити й зафіксувати в внутрішній нотатці (не обов’язково в git): email, Calendly URL, файл фото Валерії, правки біо, рішення по вакансіях (A/B/C з §1 P5), юр. назва/ЄДРПОУ або «немає».
- [ ] **A.2** Підтвердити політику `www` і хостинг-акаунт для обох доменів.
- [ ] **A.3** Переконатися, що Calendly event публічний і відповідає «Book a call» / «Забронювати дзвінок».

### Фаза B — Підстановка контенту

- [ ] **B.1** Підставити email у Contacts, Privacy, `llms.txt`, mailto (усі UK+EN джерела + білд).
- [ ] **B.2** Підставити Calendly URL у всі CTA / lazy loader / noscript fallback.
- [ ] **B.3** Оптимізувати фото Валерії (WebP 1x/2x ≤80 KB), оновити Team, перевірити `alt`.
- [ ] **B.4** Застосувати затверджене біо UA+EN (якщо є правки).
- [ ] **B.5** Вакансії: замінити на реальні **або** видалити демо й показати empty state **або** інше письмове рішення замовника; оновити sitemap / JobPosting.
- [ ] **B.6** Privacy: внести юр. дані або свідомо залишити короткий варіант без ЄДРПОУ.
- [ ] **B.7** Повний grep на залишки плейсхолдерів (§6.3).
- [ ] **B.8** Пересобрати `uk-site` + `en-site`.

### Фаза C — Pre-release QA

- [ ] **C.1** Пройти §6.1–§6.4 на staging.
- [ ] **C.2** Швидкий Lighthouse mobile на staging (регресія vs Task 7).
- [ ] **C.3** Ручний Calendly flow: клік CTA → календар бронюється.
- [ ] **C.4** Geo-банер на agency: показати / dismiss / localStorage.
- [ ] **C.5** Зафіксувати скрін home UK/EN для архіву приймання.

### Фаза D — Деплой і DNS

- [ ] **D.1** Задеплоїти prod-артефакти на обидва CDN-проєкти.
- [ ] **D.2** Налаштувати DNS (§3.2), HTTPS (§3.3), redirects (§3.4).
- [ ] **D.3** Перевірити `https://fidesa.com.ua/` і `https://fidesa.agency/` → `/en/`.
- [ ] **D.4** Виконати smoke §8.1.

### Фаза E — Search Console і приймання

- [ ] **E.1** Верифікація обох доменів у Search Console (§4.1).
- [ ] **E.2** Submit sitemaps (§4.2); spot-check hreflang (§4.3).
- [ ] **E.3** Закрити таблиці §5.1 і §5.2 (усі checkbox).
- [ ] **E.4** Короткий звіт замовнику: URL прод, що підставлено, що відкладено (CTO photo, testimonials, wordmark SVG).
- [ ] **E.5** Оновити статус плейсхолдерів у цій таблиці §1 на «Закритий» / «Відкладений».

### DoD Task 8 (локальний)

- [ ] P1 Email, P2 Calendly, P3 фото Валерії — на проді.
- [ ] P5 рішення виконано (реальні / empty / інше за згодою).
- [ ] Dual-domain HTTPS + корректні redirects.
- [ ] Content QA: UA/EN parity, no DNA325, no pricing.
- [ ] about.md §9 і майстер §10 — усі пункти прийняті.
- [ ] Search Console: properties + sitemaps.
- [ ] Smoke після деплою зелений; план rollback зрозумілий команді.

---

## 8. Rollback / smoke після деплою

### 8.1. Smoke (протягом 15–30 хв після cutover)

Виконати на **обох** доменах:

| # | Перевірка | Очікування |
|---|---|---|
| S1 | Home 200, HTTPS | Без certificate warning |
| S2 | `fidesa.agency/` | Redirect на `/en/` |
| S3 | Header CTA | Відкриває Calendly (не 404, не placeholder) |
| S4 | Contacts email | Видимий фінальний адрес; клік mailto коректний |
| S5 | Team photo | Валерія завантажується; alt коректний |
| S6 | Vacancies | List + ≥1 detail **або** узгоджений empty state; фільтри не падають |
| S7 | Blog | List + 1 post 200 |
| S8 | Privacy + llms.txt + robots + sitemap | 200; без PLACEHOLDER |
| S9 | UA↔EN switch | Path зберігається; домени правильні |
| S10 | Mobile 375 home | Немає horizontal overflow; CTA досяжний |
| S11 | View-source home | Organization JSON-LD; hreflang uk/en/x-default |
| S12 | Немає DNA325 / pricing | Швидкий пошук по HTML |

Якщо S1–S5 червоні — **негайний rollback** (§8.2). S6–S12 можна фіксити hotfix’ом, якщо регресія некритична; зафіксувати в звіті.

### 8.2. Rollback

Мета: повернути попередню стабільну версію сайту за < 15 хв без зміни DNS (бажано).

| Крок | Дія |
|---|---|
| R1 | У CDN/hosting — **Instant Rollback** / previous deployment для **обох** проєктів (uk + en). |
| R2 | Якщо проблема лише в DNS — повернути попередні CNAME/A; дочекатися TTL. |
| R3 | Якщо зламаний лише контент (email/Calendly) — hotfix forward-fix швидший за rollback; rollback якщо невпевнені в білді. |
| R4 | Після rollback повторити smoke S1–S5. |
| R5 | Заборонити індексацію зламаного деплою (якщо встиг потрапити в sitemap — не критично при швидкому відкаті). |
| R6 | Записати: час інциденту, симптом, який деплой відкотили, root cause для Task follow-up. |

**Не робити без потреби:** `docker system prune`, видалення DNS-зон, force-push секретов, вимкнення HTTPS.

### 8.3. Post-release моніторинг (24–72 год)

- [ ] Search Console: покриття / помилки редіректів.
- [ ] CDN analytics / uptime (якщо є).
- [ ] Calendly: чи з’являються тестові/реальні букінги.
- [ ] Форма відгуку на вакансії (mailto) — тестовий лист дійшов.

---

## 9. Файли, які зазвичай чіпає Task 8

> Точні шляхи залежать від реалізації Tasks 1–7; шукати за символами плейсхолдерів.

| Зона | Типові шляхи | Що змінюється |
|---|---|---|
| Контакти / CTA | `src/partials/*`, `content/uk/home.md`, `content/en/home.md`, `src/js/calendly-lazy.js` | email, Calendly |
| Team | `content/*/team.json`, `assets/images/valeriia*.webp` | фото, біо |
| Вакансії | `content/uk/vacancies/*`, `content/en/vacancies/*` | заміна/видалення демо |
| Privacy / llms | `content/*/privacy*`, `public/*/llms.txt` | email, юр. дані |
| Деплой | CI/CDN config, DNS у реєстраторі | не код фіч |

**Не змінювати в Task 8 без регресії:** `tokens.css`, дизайн-систему, логіку фільтрів/банера (лише якщо баг блокує реліз).

---

## 10. Комунікація з замовником (шаблон запиту даних)

Короткий список для одного листа/повідомлення:

1. Публічний email для сайту  
2. Публічне посилання Calendly (event «знайомчий дзвінок»)  
3. Фото Валерії (висока якість; ми зробимо WebP)  
4. Фінальне біо (UA та/або правки до чернетки)  
5. Реальні вакансії **або** дозвіл запуску з порожнім списком  
6. Юридична назва / ЄДРПОУ для Privacy — якщо вже є  
7. Підтвердження: на сайті **немає** згадок DNA325 і **немає** цін  

---

*План Task 8. Індекс усіх задач: [`README.md`](./README.md). Майстер-план: [`../2026-09-04-fidesa-site-plan.md`](../2026-09-04-fidesa-site-plan.md).*
