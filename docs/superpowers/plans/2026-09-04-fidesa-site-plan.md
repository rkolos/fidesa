# Fidesa — план розробки сайту (для ML/агентної реалізації)

> **Для агентних воркерів:** виконувати задачі послідовно за чекбоксами. Код у цей документ не входить — лише специфікація. Реалізація: чистий HTML + CSS + мінімальний vanilla JS. Не використовувати React/Vue/Next і важкі UI-бібліотеки.

**Goal:** Адаптивний дводоменний сайт рекрутингової агенції Fidesa (Defence Tech) з максимальною швидкістю (Google PageSpeed 95–100 mobile/desktop), UA + EN, контентом у чистому HTML.

**Architecture:** Статичний HTML (або SSG, що збирає в статику: Eleventy/Astro static). Два корені деплою: `fidesa.com.ua` (лише UK) і `fidesa.agency` (багатомовний, старт `/en/`). Спільні CSS/JS/assets через однаковий дизайн-токен і шаблони. Конверсія замовника — лише Calendly. Без згадок DNA325.

**Tech Stack:** HTML5, CSS3 (custom properties, container queries де доречно), vanilla JS (меню, фільтри, мова/гео, lazy Calendly), SVG-іконки inline, WebP/AVIF зображення, `llms.txt`, schema.org JSON-LD, sitemap/robots.

## Global Constraints

- Бренд: **Fidesa** — тільки Defence Tech recruitment; жодних згадок DNA325 / материнських структур.
- Мова: `fidesa.com.ua` = українська без внутрішнього перемикача; `fidesa.agency` = `/en/` на старті + архітектура під майбутні `/de/`, `/pl/` тощо.
- Конверсія B2B: **тільки бронювання дзвінка через Calendly** (немає цін, пакетів, форм «залишити email» як основного CTA).
- Стек: **кінцевий результат — чистий HTML** (SSR/SSG ок, SPA без pre-render — заборонено).
- Дизайн: **строгий defence** — navy + графіт + білий/світло-сірий; без неону, без purple-градієнтів, без cream/serif «AI-кліше», без карток у hero, без dark-mode за замовчуванням.
- Шрифт: гротеск **не** російського/білоруського походження (пріоритет: українські дизайнери або перевірені міжнародні з ліцензією). Кандидати для вибору на етапі дизайн-токенів: e-Ukraine / Mak / Kyiv Type (якщо ліцензія дозволяє) або Inter **не** брати як дефолт; краще **IBM Plex Sans**, **Source Sans 3**, **Manrope**, **Geist** — перевірити походження/ліцензію перед фіксацією.
- Конкурентна візуальна диференціація: див. **§0A** (аудит Everstar / BazaIT Defense / ITExpert / BazaIT Jobs від 2026-09-04).
- Testimonials: порожній модуль-заглушка, без логотипів клієнтів.
- PageSpeed: ціль **≥95 mobile**, **≥98 desktop**; LCP < 2.5s, INP < 200ms, CLS < 0.1.
- Античні мотиви: лише лінійна графіка (колос→PCB, dextrarum iunctio, меандр/лавр у футері) — без богів, золота, статуй.

---

## 0. Зафіксовані рішення (де ТЗ лишало вибір підряднику)

| Питання | Рішення в плані |
|---|---|
| CMS | На старті — **без CMS**: контент у Markdown/HTML-файлах; testimonials і вакансії — структуровані JSON/MD. Пізніше можна підключити headless CMS без зміни публічного HTML-контракту. |
| ATS для вакансій | Статичний каталог з JSON/MD + клієнтський фільтр; форма «відгукнутися» = `mailto:` або зовнішня форма (не фіксуємо ATS). |
| hreflang EN | `https://fidesa.agency/en/` (корінь `fidesa.agency/` → 302/canonical на `/en/` до появи інших мов). |
| Перехід між доменами | У шапці: посилання «UA | EN» (com.ua ↔ agency/en); на com.ua — тільки перехід на EN-домен; на agency — мовний select + лінк на UA-домен. |
| Геолокація на agency | При першому візиті: якщо Accept-Language / geo ≈ UA — м’який банер «Перейти на українську версію (fidesa.com.ua)?»; інакше лишатися на `/en/`. Зберегти вибір у `localStorage`. |
| Аналітика | Privacy-friendly: Plausible або GA4 з consent-banner (мінімальний JS). Не блокувати LCP. |
| Calendly | Lazy-load iframe після кліку / IntersectionObserver біля секції Contacts (не в hero-бандл). |
| Логотип | **Готовий:** корінь проєкту `logo.svg` (комбінований знак Φ + колос/PCB). Кольори з SVG — джерело правди для токенів. |

**Колірні токени (з `logo.svg`):**

| Token | HEX | Джерело / роль |
|---|---|---|
| `--navy` | `#2E4259` | fill основного контуру Φ у логотипі — бренд, заголовки, header, primary CTA |
| `--graphite` | `#424443` | fill колоса/PCB-деталі в логотипі — акцентний графіт, вторинні елементи, іконки |
| `--navy-mid` | `#3D566F` | Hover / mid (похідна від `--navy`, +світліше) |
| `--steel` | `#5A738C` | Стриманий акцент ліній (похідна `--navy`) |
| `--ink` | `#1A1C1B` | Текст body (темніше за graphite логотипу для читабельності) |
| `--ink-muted` | `#5C6570` | Secondary text |
| `--bg` | `#F7F8FA` | Фон сторінки |
| `--surface` | `#FFFFFF` | Секції / інтерактивні контейнери |
| `--line` | `#D8DEE6` | Роздільники 1px |
| `--focus` | `#2E4259` | Focus ring 2px (= `--navy`) |
| `--on-navy` | `#FFFFFF` | Текст/іконки на navy-кнопках і hero overlay |

---

## 0A. Конкурентний аудит (референси з about.md §2 і §3.2)

> Джерела: live-scrape 2026-09-04 — [everstar.in.ua](https://everstar.in.ua/), [bazait.com/defense](https://bazait.com/defense), [itexpert.work](https://itexpert.work/), [app.bazait.com/search/jobs](https://app.bazait.com/search/jobs). Скріни: `.firecrawl/*-shot.png`.  
> Мета аудиту: **не копіювати** візуал/композицію трьох сайтів; для jobs — **взяти функціональну логіку**, адаптувати під бренд Fidesa.

### 0A.1. Зведена матриця «вони vs Fidesa»

| Вимір | Everstar | BazaIT Defense | ITExpert | **Fidesa (ціль)** |
|---|---|---|---|---|
| Модель | Нішева miltech-агенція + сильний candidate-facing | Платформа + community + recruiting + івенти | Генералістська IT-агенція; MilTech = один із напрямів | **Тільки** Defence Tech recruiting для **замовників** |
| Головний меседж hero | «Перше агентство… наближати перемогу» + dual audience | «Reliable recruiting partner» + Post a Job / Join Community | «Find Your Top Tech Talent» + глобальний IT | «Рекрутинг для Defence Tech» — спеціалізація, не патріотичний слоган як вісь |
| CTA | Mailto / popup «Напишіть нам», форма резюме | Post a Job, Community, Calendly, Survey | Schedule a call + форма консультації в hero | **Лише Calendly** (B2B); apply на вакансіях — окремо |
| Публічні ціни | Ні на лендінгу | Так: Sourcing 9% / Recruiting 360 14% + PDF | Ні (класична агенція) | **Ні** (ТЗ) |
| Community / events / survey | Ні | Telegram/Signal QR, календар івентів, salary survey | Ні (є cases/blog/reviews) | **Немає** на сайті |
| Stats-смуга в hero | Ні | 13+ / 3+ / 100% Victory | 32 recruiters, 200 clients, 1900 roles… | **Немає** stats у першому екрані |
| Тема UI | Світла, тепла cream/beige | Темна + amber/yellow | Біла corporate + жовтий акцент | Світла **cool** navy/steel (`#2E4259`) + graphite — **не** cream, **не** dark+amber, **не** yellow CTA |
| Типовий стек сайту | WordPress + Elementor | Product SPA + Tailwind-like | WordPress, важкий | Статичний HTML, мінімум JS |

### 0A.2. Everstar — що зафіксовано і чого уникати

**Структура one-pager:** Hero → Місія (3 колонки) → Як ми працюємо → Ми шукаємо (чіпи спеціалізацій office/production) → Вакансії на головній → Форма «Залишити резюме» → Контакти/соцмережі. ATS: Breezy (`everstar.breezy.hr`).

**Візуал (скрін + CSS):**
- Фон / surfaces: теплий cream `#f5efe0`, subtle `#dcd7ca` — «паперовий», дружній.
- Primary: чорний `#000`; accent WP `#cd2653` (майже не домінує на hero).
- Великі стокові фото людей (рукостискання, фрилансер за ноутбуком), м’які радіуси, «людяний» Elementor-лейаут.
- Лого у шапці дрібне; H1 «МИ — EVERSTAR» домінує над брендом-знаком.

**Позиціонування (для копірайтингу Fidesa, не для дизайну):** dual audience (компанії + кандидати), місія «перемога», акцент на безкоштовність для кандидатів, реферальний/інженерний нішевий тон.

**Fidesa — антипатерни від Everstar:**
1. Не використовувати cream/beige/warm paper палітру.
2. Не ставити сітку стокових «HR-фото рукостискань» як головний візуал.
3. Не робити головну candidate-first (форма резюме, «ми шукаємо» чіпи як центр лендінгу).
4. Не дублювати вакансії великим блоком на home — лише лінк у nav/footer; вакансії на окремій сторінці.
5. Не CTA через mailto як primary для замовника.
6. Brand mark Fidesa має бути hero-level (на відміну від дрібного лого Everstar vs кричущого H1).

### 0A.3. BazaIT Defense — що зафіксовано і чого уникати

**Структура:** Hero (partner + dual CTA) → stats → Salary Survey → блоки recruiting-фіч → community (Telegram/Signal + QR) → CEO + Calendly + PDF presentation → Event calendar → FAQ з **публічними % комісій**.

**Візуал:**
- Dark UI `#2d2d2d` / чорний; акцент amber `#f19100` (hover `#c78015`); жовті кнопки CTA.
- Product/platform мова: «We are a product…», Sign up / Post a Job.
- Багато карток-фіч, QR-коди, івент-карусель — щільний маркетинг-хаб.
- Chatwoot live-chat на сторінках (важкий third-party).

**Позиціонування:** платформа + ком’юніті + рекрутинг; defense — вертикаль продукту BazaIT.

**Fidesa — антипатерни від BazaIT Defense:**
1. Не dark-mode лендінг і не amber/yellow (#f19100 / #fdd835-подібні) як primary CTA.
2. Не QR Telegram/Signal, не event calendar, не salary survey, не «Join the Community».
3. Не публікувати пакети/% комісій і PDF «presentation» з прайсом.
4. Не позиціонуватись як «product/platform».
5. Не вбудовувати live-chat віджети (PageSpeed + зайвий candidate/support UX).
6. Stats «N years / 100% Victory» у hero — не копіювати; якщо потрібні факти — лише в About як декларативні речення, не marketing counters.

**Що можна запозичити обережно (не візуал):**
- Наявність Calendly у блоці людини/контакту — у Fidesa це **єдиний** B2B CTA, але в секції Contacts, не dual «Post a Job + Community».
- FAQ-як-формат всередині секцій (у BazaIT окремий FAQ) — у Fidesa вже закладено Q→A в About/Why без окремого меню FAQ.

### 0A.4. ITExpert — що зафіксовано і чого уникати

**Структура:** корпоративний мегасайт — Services / Directions / Technologies / Cases / Reviews / Blog; hero з формою «Order a consultation»; велика статистика; MilTech — **одна плитка** серед IT recruiting, rare specialists, core team, outsourcing тощо.

**Візуал:**
- Білий фон, чорний текст, жовтий акцент кнопок (`#ffcc36` / `#fdd835`).
- Багато іконок-ілюстрацій у плитках послуг, клієнтські логотипи, «agency corporate» щільність.
- Мультимова включаючи `/ru/` — для Fidesa **не релевантно і небажано** як патерн.

**Позиціонування:** «10+ years, global IT talent»; Defence/MilTech = додатковий сервіс серед FinTech/Web3/SaaS.

**Fidesa — антипатерни від ITExpert:**
1. Не жовті CTA і не «жовтий + білий + чорний» corporate look.
2. Не сітка з 8+ сервісних карток на home; один фокус — Defence Tech recruiting.
3. Не hero з довгою lead-формою (ім’я/телефон/email/how can we help) — лише Calendly.
4. Не виносити логотипи клієнтів (у ТЗ testimonials без лого; ITExpert ними насичений).
5. Не розмивати меседж «ми IT-агенція, а ще й miltech» — у Fidesa навпаки: **лише** defence.
6. Не додавати російську локаль / не копіювати їхній language switcher UX.

### 0A.5. BazaIT Jobs (`app.bazait.com/search/jobs`) — функціональний референс для Fidesa Vacancies

ТЗ (§3.2): орієнтуватись на **функціональну логіку**, не на бренд-UI BazaIT.

**Що є на референсі (за scrape):**
- Вкладки: Jobs / Companies (для Fidesa Companies **не потрібні**).
- Фільтри: Category, Position, Type of Work, Salary + кнопка «Open All Filters»; лічильник «N jobs found».
- Картка вакансії: лого компанії, дата публікації, назва компанії, title, формат (Remote/Office/Hybrid), salary або «—», локація, CTA Apply.
- Пагінація (1, 2, 3…).
- Live-chat Chatwoot.

**Що взяти в Fidesa (адаптовано):**

| Елемент BazaIT Jobs | Рішення Fidesa |
|---|---|
| Список карток + окрема detail URL | Так |
| Фільтр напрямок (Category) | Так → `direction` |
| Фільтр локація | Так → `location` (у референсі локація в картці; винести в filter bar) |
| Type of Work (Remote/Office/Hybrid) | Так → `format` |
| Salary filter | **Ні** на старті (часто «—»; зайва складність; salary опційно в картці якщо є) |
| Companies tab / company logos | **Ні** лого клієнтів (ТЗ); у картці — лише title/meta, без brandmark замовника |
| «N jobs found» | Так, коротко |
| Open All Filters (drawer) | На mobile — один panel «Фільтри»; на desktop — inline chips/selects |
| Pagination | До 20 — без; далі «Показати ще» |
| Chatwoot | **Ні** |
| Sign up / Login platform | **Ні** — статичний сайт агенції |

**Картка Fidesa (поля):** `title` · `location` · `employment/format` · `direction` · `short` (≤160) · `datePosted` (можно дрібним meta) · link «Детальніше». Без salary-обов’язковості, без logo клієнта.

**Mobile jobs (уточнення від референсу):** референс — широкі горизонтальні картки з Apply справа; на вузьких екранах у BazaIT тісно. У Fidesa: **стек** — title → meta row → excerpt → full-width «Детальніше»; фільтри — horizontal snap chips або bottom sheet, не десктопний sidebar.

### 0A.6. Позиціонування однією фразою (для hero / llms.txt)

- Everstar ≈ «miltech recruiting + кандидати + місія перемоги».  
- BazaIT Defense ≈ «defense platform: jobs + community + events + priced packages».  
- ITExpert ≈ «generalist IT agency (MilTech among many)».  
- **Fidesa ≈ «specialized Defence Tech recruiting agency for hiring companies — book a call».**

### 0A.7. Чекліст диференціації перед релізом (обов’язковий)

- [ ] Скрін Fidesa home поруч зі скрінами трьох конкурентів: палітра/CTA/щільність **не** плутаються.
- [ ] Немає cream `#f5efe0`-подібних фонів, amber `#f19100`, yellow `#ffcc36` CTA.
- [ ] Немає community/QR/events/survey/pricing % / client logo wall / hero lead-form / resume-upload на home.
- [ ] Hero: бренд + одна спеціалізаційна обіцянка + Calendly — без stats strip.
- [ ] Vacancies UX відповідає §0A.5 (логіка так, UI BazaIT — ні).

---

## 1. Карта сайту та файлова структура

### 1.1. URL-карта

**fidesa.com.ua (UK only)**

| URL | Сторінка |
|---|---|
| `/` | Головна (one-pager) |
| `/vacancies/` | Список вакансій |
| `/vacancies/{slug}/` | Деталь вакансії |
| `/blog/` | Список постів |
| `/blog/{slug}/` | Пост |
| `/blog/tag/{tag}/` | Фільтр за тегом |
| `/privacy/` | Політика конфіденційності (коротка) |
| `/llms.txt` | AI-файл |
| `/robots.txt`, `/sitemap.xml` | Технічні |

**fidesa.agency**

| URL | Сторінка |
|---|---|
| `/` | Redirect → `/en/` |
| `/en/` | Home |
| `/en/vacancies/` … | як вище |
| `/en/blog/` … | як вище |
| `/en/privacy/` | Privacy |
| `/llms.txt`, `/robots.txt`, `/sitemap.xml` | Технічні |
| Майбутнє: `/de/`, `/pl/` — дзеркало структури `/en/` |

### 1.2. Дерево проєкту (цільове)

```
/
├── about.md                          # ТЗ (існуюче)
├── docs/superpowers/plans/…          # цей план
├── content/
│   ├── uk/
│   │   ├── home.md                   # секційні тексти головної
│   │   ├── team.json
│   │   ├── vacancies/*.md
│   │   └── blog/*.md
│   └── en/                           # дзеркало
├── public/                           # або dist після збірки
│   ├── uk-site/ … → деплой com.ua
│   └── en-site/ … → деплой agency
├── src/
│   ├── styles/
│   │   ├── tokens.css
│   │   ├── base.css
│   │   ├── layout.css
│   │   ├── components.css
│   │   └── pages.css
│   ├── js/
│   │   ├── nav.js                    # mobile menu
│   │   ├── filters.js                # vacancies + blog tags
│   │   ├── domain-lang.js            # banner / localStorage
│   │   └── calendly-lazy.js
│   ├── partials/                     # header, footer, schema
│   └── pages/                        # шаблони
├── logo.svg                          # ДЖЕРЕЛО: комбінований знак (уже в корені)
└── assets/
    ├── brand/
    │   ├── logo.svg                  # копія/оптимізований варіант з кореня
    │   ├── logo-mark.svg             # лише знак (без зайвого viewBox padding, якщо потрібно)
    │   ├── favicon.svg               # спрощений mark 32×32
    │   └── apple-touch-icon.png      # 180×180 з navy фоном за потреби
    ├── fonts/                        # self-host woff2 subset
    ├── images/                       # webp/avif + fallback
    └── icons/                        # svg sprites / inline
```

### 1.3. Логотип — специфікація використання

**Файл:** `/logo.svg` (viewBox `0 0 448 509`, вертикальний комбінований знак).

**Палітра з файлу (не вигадувати інші бренд-кольори):**
- `#2E4259` — основний navy (літера Φ / зовнішній контур)
- `#424443` — графіт (колос → мікросхема всередині)

**Правила розміщення:**
- Header: висота знака **28–32px** (mobile), **36–40px** (desktop); поруч або під ним wordmark «Fidesa» текстом у гротеску (у SVG зараз лише знак без напису — wordmark верстати CSS/текстом, не раструвати).
- Hero: знак як частина brand-блоку; не розмивати, не перефарбовувати в неонові кольори; на темному overlay — залишити оригінальні fill **або** одноколірний knockout `#FFFFFF` / `#F7F8FA` (окремий `logo-on-dark.svg` з `fill="currentColor"`).
- Favicon: обрізати/спростити до читабельного Φ на 16–32px; фон — `--navy` або прозорий.
- Не обводити логотип тінями, градієнтами, glow.
- `alt="Fidesa"` / для decorative в header поруч з видимим текстом бренду — `alt=""` + текст «Fidesa».
- Перед продом: SVGO-оптимізація (зберегти обидва fill); перевірити контраст знака на `--bg` і на hero.

---

## 2. Дизайн-система: строгий defence

> Перед версткою обов’язково прочитати **§0A**: палітра й композиція мають **явно відрізнятися** від Everstar (cream/фото), BazaIT Defense (dark+amber+product), ITExpert (white+yellow+service grid).

### 2.1. Візуальна мова (обов’язково для верстки)

- **Композиція:** одна чітка вісь, багато повітря, тонкі 1px лінії (`--line`), ніяких «карток з тінню» у hero і в маркетингових секціях. Картки дозволені лише там, де є інтеракція (вакансія, пост, фільтр).
- **Hero:** full-bleed фон (темний navy або фото виробництва/інженерії з navy overlay 60–70%). Бренд **Fidesa** — hero-level (крупніше або рівно з H1 за вагою). Один headline, один supporting, одна CTA-група. Без badges, stats, sticky promo chips поверх медіа.
- **Секції:** чергування `--surface` / `--bg`; роздільники — тонкий SVG-патерн «колос→PCB» (opacity ~0.08), не декоративні ілюстрації.
- **Іконки:** stroke 1.5px, `currentColor`, лінійні; для «Процес» / «Чому Fidesa» — опційно dextrarum iunctio (дві руки) як 24–32px SVG.
- **Motion (2–3 навмисні):** (1) fade+translateY 8px секційних заголовків при scroll (IntersectionObserver, `prefers-reduced-motion: reduce` → off); (2) underline/slide на nav links; (3) CTA `scale(0.96)` на press. Без parallax, glow, blur-heavy.
- **Не робити:** rounded-full pills, multi-layer shadows, emoji, неонові акценти, dark theme toggle на v1.
- **Заборонені «конкурентні» кліше (з аудиту §0A):** warm cream paper-фони; dark landing + amber/yellow CTA; жовті кнопки corporate; stats counters у hero; сітка 6–12 сервісних карток; QR community; логотипи клієнтів у стіні довіри.

### 2.2. Типографіка

| Роль | Розмір desktop | Mobile | Вага |
|---|---|---|---|
| Brand / Display | clamp(2.5rem, 5vw, 3.75rem) | ~2.25rem | 600–700 |
| H1 (якщо окремо від brand) | 2rem–2.5rem | 1.75rem | 600 |
| H2 секції | 1.75rem | 1.5rem | 600 |
| H3 | 1.25rem | 1.125rem | 600 |
| Body | 1.0625–1.125rem / 1.6 | 1rem / 1.55 | 400 |
| Small / meta | 0.875rem | 0.8125rem | 400 |

Self-host `woff2` subset (latin + cyrillic). `font-display: swap`. Не більше 2 накреслень (400, 600).

### 2.3. Брейкпоінти та мобільний пріоритет

| Token | px | Поведінка |
|---|---|---|
| `sm` | 480 | дрібні правки відступів |
| `md` | 768 | 2 колонки процес/безпека |
| `lg` | 1024 | повний header без hamburger |
| `xl` | 1280 | max content width ~1120–1200px |

**Mobile-first правила (критично):**

1. Header: логотип + CTA «Забронювати дзвінок» (короткий) + hamburger; мовне посилання в drawer.
2. Hero висота: `min-height: 100svh` але контент не обрізати — CTA завжди видимий без scroll на типових 375×667; якщо не вміщується — зменшити supporting, не ховати CTA.
3. Touch targets ≥ 44×44px; фільтри вакансій — повна ширина, chips у горизонтальний scroll з `scroll-snap`, не multi-select dropdown що вилазить за екран.
4. Calendly на mobile: не iframe на всю сторінку в hero — кнопка відкриває Calendly popup або секцію з lazy iframe нижче fold.
5. Команда: фото Валерії — квадрат/портрет full-bleed у колонці, біо під ним (стек), не side-by-side до `md`.
6. Sticky mobile CTA-bar (опційно, лише на головній): одна кнопка Calendly внизу екрана після scroll > 40% hero; `safe-area-inset-bottom`; не перекривати контент футера (ховати біля Contacts).
7. Жодного horizontal overflow; таблиці/довгі URL — wrap.
8. Тестувати: 320, 375, 390, 414, 768, 1024, 1440; iOS Safari + Chrome Android.

---

## 3. Повна копірайтинг-специфікація (згенеровано; можна правити)

> Усі ключові факти — декларативні речення для GEO/AEO. Де природно — формат Q→A всередині секції.

### 3.1. Головна — українська (`fidesa.com.ua`)

**Meta**

- Title: `Fidesa — рекрутинг для Defence Tech`
- Description: `Fidesa — спеціалізована рекрутингова агенція для виробників озброєння, БПЛА та оборонного ПЗ. Підбір інженерів і технічних команд під ключ.`

**Nav:** Про нас · Процес · Чому Fidesa · Команда · Вакансії · Блог · Контакти  
**CTA (primary):** Забронювати дзвінок  
**CTA (header short mobile):** Дзвінок  
**Domain switch:** EN

---

**Hero**

- Brand: `Fidesa`
- H1: `Рекрутинг для Defence Tech`
- Supporting: `Ми підбираємо інженерів, розробників і технічних лідерів для компаній, що створюють озброєння, безпілотні системи та оборонне програмне забезпечення.`
- CTA primary: `Забронювати дзвінок`
- CTA secondary (anchor): `Як ми працюємо`

---

**Про нас**

- H2: `Хто така Fidesa`
- Lead (факт): `Fidesa — рекрутингова агенція, що працює виключно зі сферою Defence Tech.`
- Body: `Ми допомагаємо виробникам і розробникам у сфері оборони закривати критичні ролі: від вбудованих систем і радіоінженерії до software, data та production. Фокус один — оборонний ринок. Ми не ведемо загальний IT-рекрутинг і не змішуємо Defence Tech з іншими індустріями.`
- Q/A block:
  - **Для кого Fidesa?** Для компаній-замовників: виробників озброєння та БПЛА, engineering- і software-команд в оборонній сфері.
  - **Що ми робимо?** Повний цикл підбору персоналу: бриф, пошук, скринінг, інтерв’ю-координація, офер і супровід до виходу кандидата.
  - **Чому вузька спеціалізація?** Глибина ринку, розуміння ролей і вимог безпеки дають швидший і якісніший найм, ніж у генералістських агенцій.

---

**Процес**

- H2: `Як проходить співпраця`
- Intro: `Прозорий процес від брифу до найму — з чіткими етапами і відповідальними з обох сторін.`
- Кроки (4):
  1. **Бриф** — Фіксуємо роль, стек, рівень, обмеження безпеки, терміни та критерії успіху.
  2. **Пошук і скринінг** — Досліджуємо ринок, перевіряємо відповідність і ризики, готуємо короткий список.
  3. **Інтерв’ю** — Координуємо зустрічі з вашою командою, збираємо зворотний зв’язок, калібруємо пошук.
  4. **Офер і онбординг** — Підтримуємо офер, прийняття рішення та вихід кандидата на роботу.
- Мікрокопія під кроками: `Угода між двома сторонами — основа нашої роботи.` (концепт dextrarum iunctio; іконка лінійна)

---

**Чому Fidesa**

- H2: `Чому обирають Fidesa`
- Intro: `Спеціалізація на Defence Tech — головна причина. Безпека — обов’язкова частина процесу, а не маркетинг-слоган.`

**Підблок A — Операційна безпека**

- H3: `Операційна безпека агенції`
- Факти:
  - Конфіденційна комунікація з замовником і кандидатами.
  - Обмежений доступ до даних вакансій і проєктів за принципом need-to-know.
  - Захист персональних і комерційних даних клієнта відповідно до застосовного законодавства.
- Q: **Як ви захищаєте інформацію клієнта?** A: Ми мінімізуємо коло осіб з доступом до брифу, не публікуємо ідентифікатори клієнта без дозволу та використовуємо захищені канали комунікації.

**Підблок B — Безпека підбору**

- H3: `Безпека підбору кандидатів`
- Факти:
  - Перевірка на зв’язки з рф та окупованими територіями в межах доступних і законних процедур.
  - Урахування військового статусу та обмежень, релевантних для ролі й юрисдикції.
  - Відповідність вимогам захисту персональних даних під час обробки резюме та комунікації.
- Q: **Чи гарантуєте ви абсолютну перевірку?** A: Ми застосовуємо протоколи скринінгу та ескалуємо сумнівні кейси замовнику. Остаточне рішення щодо допуску завжди залишається за клієнтом і його compliance-процесами.

---

**Команда**

- H2: `Команда`
- Intro: `Люди, з якими ви працюєте напряму.`

**Валерія — Founder**

- Role: `Засновниця`
- Bio: `Валерія керує Fidesa та відповідає за розвиток агенції й ключові клієнтські відносини. Публічна представниця бренду; фокус — побудова спеціалізованого рекрутингу для Defence Tech і якісний сервіс для команд, що масштабують оборонні продукти.`
- (Фото: окремий asset; alt: `Валерія, засновниця Fidesa`)

**CTO (без фото на старті)**

- Title: `CTO`
- Trust line: `Технічний директор з військовим досвідом — забезпечує інженерну експертизу в оцінці ролей і вимог до кандидатів у Defence Tech.`
- Не розкривати ПІБ, якщо не надано окремо.

---

**Testimonials (заглушка)**

- H2: `Відгуки клієнтів`
- Empty state: `Тут з’являться відгуки компаній, з якими ми працюємо. Модуль готовий до наповнення.`
- Розмітка: контейнер `data-testimonials` з 0 карток; шаблон картки задокументувати в HTML-коментарі: photo / quote / name / role.

---

**Contacts / Calendly**

- H2: `Забронюйте дзвінок`
- Supporting: `Короткий зінг із засновницею або командою — щоб зрозуміти роль, терміни й чи можемо бути корисними.`
- CTA fallback (якщо JS off): посилання на Calendly URL текстом.
- Contacts block:
  - Email: `[EMAIL_PLACEHOLDER]` (підставити перед деплоєм)
  - Location line: `Україна · робота з клієнтами в Україні та міжнародно`
  - Не публікувати фізичну адресу, якщо не потрібна юридично.

---

**Footer**

- Brand + короткий рядок: `Спеціалізований рекрутинг для Defence Tech`
- Links: Вакансії · Блог · Privacy · EN (agency)
- Декор: тонкий меандр / лавр SVG
- © `© {year} Fidesa`

---

### 3.2. Головна — англійська (`fidesa.agency/en/`)

**Meta**

- Title: `Fidesa — Defence Tech Recruitment`
- Description: `Fidesa is a specialized recruiting agency for defence manufacturers, UAV builders, and defence software teams. We hire engineers and technical talent with security-aware screening.`

**Nav:** About · Process · Why Fidesa · Team · Vacancies · Blog · Contact  
**CTA:** Book a call · mobile short: `Book`  
**Domain switch:** UA

**Hero**

- Brand: `Fidesa`
- H1: `Recruitment for Defence Tech`
- Supporting: `We hire engineers, developers, and technical leaders for companies building weapons systems, unmanned platforms, and defence software.`
- CTA: `Book a call` / secondary `How we work`

**About**

- H2: `What Fidesa is`
- Lead: `Fidesa is a recruiting agency focused exclusively on Defence Tech.`
- Body: `We help defence manufacturers and product teams fill critical roles — from embedded systems and RF engineering to software, data, and production. One focus: the defence market. We do not run generalist IT recruiting alongside Defence Tech.`
- Q/A: For whom / What we do / Why specialization — дзеркально UK.

**Process** — H2 `How engagement works`  
Steps: Brief → Search & screening → Interviews → Offer & onboarding  
Microcopy: `An agreement between two sides is the foundation of our work.`

**Why Fidesa** — H2 `Why companies choose Fidesa`  
Intro: `Defence Tech specialization is the primary reason. Security is a required part of delivery — not a slogan.`  
Subheads: `Operational security` / `Hiring security` — дзеркало фактів UK (screening for rf/occupied territories links, military status awareness, personal data compliance).  
Disclaimer Q: We apply screening protocols and escalate edge cases; final clearance decisions remain with the client’s compliance process.

**Team** — Valeriia, Founder + CTO with military background (trust signal, no photo required at launch)

**Testimonials empty:** `Client testimonials will appear here. This module is ready to be populated.`

**Contact:** `Book a call` + email placeholder + `Ukraine · serving clients in Ukraine and internationally`

---

### 3.3. Вакансії — шаблони текстів

> UX-логіка карток/фільтрів — **§0A.5** (референс BazaIT Jobs). Візуал карток — дизайн-система Fidesa (§2), не UI app.bazait.com.

**List page UK**

- H1: `Вакансії`
- Intro: `Відкриті ролі в компаніях Defence Tech. Fidesa супроводжує підбір; умови співпраці з роботодавцем обговорюються окремо.`
- Filters labels: `Напрямок` · `Локація` · `Формат` · `Скинути`
- Empty filter: `За цими фільтрами вакансій немає.`
- Card fields: title, location, employment type, short description (≤160 chars), link «Детальніше»

**List page EN:** `Vacancies` / `Open roles across Defence Tech companies…` / Direction · Location · Format · Reset

**Detail CTA UK:** `Відгукнутися`  
**Detail CTA EN:** `Apply`  
Supporting under CTA: `Надішліть резюме — ми зв’яжемося щодо наступних кроків.` / `Send your CV — we will follow up on next steps.`

**Стартові вакансії (приклад для запуску — 3 шт., вигадані плейсхолдери; замінити реальними):**

1. **Embedded Software Engineer (UAV)** — Київ / Remote UA — Full-time — Firmware для бортових систем БПЛА; C/C++, RTOS.  
2. **Full-Stack Engineer (Defence SaaS)** — Remote EU/UA — Full-time — Платформа для logistics/C2; TypeScript, Node.  
3. **RF / Electronics Engineer** — Україна — Hybrid — Радіолінії та антенні рішення для unmanned systems.

Slug examples: `embedded-software-engineer-uav`, `fullstack-defence-saas`, `rf-electronics-engineer`

На кожній детальній: JobPosting schema (title, datePosted, employmentType, hiringOrganization=Fidesa або client confidential, jobLocation, description).

---

### 3.4. Блог — 3 стартові пости (UK + EN)

**Спільні теги:** `defence-tech`, `recruiting`, `security`, `engineering-hiring`, `ukraine`

**Пост 1**  
- Slug: `why-defence-tech-needs-specialized-recruiters`  
- Author: Валерія / Valeriia  
- UK title: `Чому Defence Tech потрібен спеціалізований рекрутинг`  
- EN title: `Why Defence Tech needs specialized recruiters`  
- Summary UK: `Ролі в оборонці вимагають розуміння стеку, безпеки й ринку. Генералістський підхід уповільнює найм.`  
- Outline (800–1200 слів): відмінність ролей; вартість помилкового найму; як спеціалізація скорочує time-to-hire; без розкриття клієнтів.

**Пост 2**  
- Slug: `screening-without-theatre`  
- Author: Валерія / Valeriia  
- UK: `Скринінг кандидатів без театру безпеки`  
- EN: `Candidate screening without security theatre`  
- Про протоколи, межі агенції vs compliance клієнта, персональні дані.

**Пост 3**  
- Slug: `briefing-a-defence-role`  
- Author: Команда Fidesa / Fidesa Team  
- UK: `Як брифувати оборонну роль, щоб пошук був швидким`  
- EN: `How to brief a defence role so search moves fast`  
- Чекліст брифу: місія продукту, стек, clearance expectations, timeline, must-have vs nice-to-have.

Кожен пост: author name + optional photo, date, tags, related posts (same tags).

---

### 3.5. Privacy (коротко)

UK + EN сторінки: хто контролер даних, які дані (Calendly, заявки, аналітика), підстави, строк зберігання, контакти для запитів. Без юридичного «простырадла» на 20 сторінок — 1 екран + посилання на повну політику якщо з’явиться пізніше.

---

### 3.6. `llms.txt` (зміст для обох доменів)

Обов’язкові блоки:

```
# Fidesa
> Specialized Defence Tech recruiting agency.

## What we do
- Recruitment only for defence manufacturers, UAV, defence software teams.
- Primary audience: hiring companies. Candidates use /vacancies.

## Sites
- Ukrainian: https://fidesa.com.ua/
- International (English): https://fidesa.agency/en/

## Key pages
- / (home sections: about, process, why, team, contact)
- /vacancies/
- /blog/

## Contact
- Book a call via Calendly on the contact section.
- Email: [EMAIL_PLACEHOLDER]

## Notes
- No public pricing. No affiliation claims beyond Fidesa brand.
```

UK-домен — українською версією того ж змісту; EN-домен — англійською.

---

## 4. Специфікація сторінок (секції + поведінка)

### 4.1. Header (спільний)

- Sticky, фон `--surface` / blur легкий **лише якщо не б’є по perf** (інакше solid).
- Logo → home.
- Anchor links на one-pager; на внутрішніх — абсолютні на `/#section`.
- Primary CTA завжди видимий (desktop: кнопка; mobile: в барі або drawer + sticky bar).
- Skip link «Перейти до контенту».

### 4.2. Home sections order

1. Hero  
2. About  
3. Process  
4. Why Fidesa (2 колонки від `md`)  
5. Team  
6. Testimonials stub  
7. Contact + Calendly lazy  
8. Footer  

### 4.3. Vacancies

- Реалізувати за матрицею **§0A.5** (що взяти / що відкинути з BazaIT Jobs).
- Toolbar filters: `direction`, `location`, `format` (дані з frontmatter). **Без** salary-filter і **без** company logos.
- Client-side filter без перезавантаження; URL query sync (`?direction=&location=&format=`) для шарингу.
- Лічильник «N вакансій» / «N vacancies».
- Mobile: стек-картка + filter chips/sheet (§0A.5); desktop: inline filters над списком.
- Pagination не потрібна до >20 вакансій; далі — «Показати ще».
- Detail: breadcrumb Головна → Вакансії → Title; CTA apply; related vacancies optional.
- На **home не дублювати** лістинг вакансій (антипатерн Everstar) — лише nav-лінк.

### 4.4. Blog

- Grid/list: title, date, author, tags, excerpt.
- Tag filter pages.
- Article: readable measure `max-width: 68ch`; author byline; share links optional (без важких widgets).

### 4.5. 404

- Короткий текст + лінки Home / Vacancies / Blog. Окремо для кожного домену/мови.

---

## 5. SEO / AEO / технічна розмітка

### 5.1. На кожній сторінці

- Унікальні `title`, `meta description`, canonical.
- Open Graph + Twitter card (статичне OG-зображення бренду 1200×630).
- `lang="uk"` / `lang="en"`.
- hreflang:
  - `uk` → `https://fidesa.com.ua{path}`
  - `en` → `https://fidesa.agency/en{path}`
  - `x-default` → `https://fidesa.agency/en/` (міжнародний дефолт)

### 5.2. JSON-LD

- Home: `Organization` (+ `ProfessionalService`), `WebSite`.
- Vacancy detail: `JobPosting`.
- Blog post: `BlogPosting` + `Person` author.
- All inner: `BreadcrumbList`.

### 5.3. robots.txt

Дозволити GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Googlebot. Sitemap URL абсолютний для домену.

### 5.4. Контент у HTML

Жодного ключового тексту лише в JS. Фільтри можуть ховати картки CSS/JS, але всі вакансії присутні в DOM або окремі URL для деталей завжди в HTML.

---

## 6. Продуктивність (Google PageSpeed) — обов’язковий чекліст

### 6.1. Бюджет ресурсів (mobile)

| Ресурс | Бюджет |
|---|---|
| HTML document | < 50 KB gzip |
| CSS total | < 40 KB gzip (краще < 25) |
| JS total | < 30 KB gzip; краще < 15 |
| Hero image | < 120 KB (AVIF/WebP), width srcset |
| Fonts | ≤ 2 files woff2, subset, preload лише critical |
| Third-party | Calendly — після interaction/visible; analytics deferred |

### 6.2. Техніки

1. Critical CSS inline **або** один CSS файл без render-blocking ланцюжків; `media`/`preload` для non-critical.
2. Зображення: `width`/`height` або aspect-ratio → CLS=0; `loading="lazy"` нижче fold; hero — `fetchpriority="high"`.
3. Немає jQuery, Bootstrap, icon-font (Font Awesome) — тільки SVG.
4. Немає web fonts з Google CDN у runtime (self-host).
5. Мініфікація HTML/CSS/JS на білді; Brotli/Gzip на CDN.
6. Cache-Control довгий для hashed assets; HTML — short/revalidate.
7. Уникати layout thrashing у JS фільтрів; debounce input.
8. Calendly: placeholder з кнопкою «Відкрити календар» → inject script once.
9. Перевірка Lighthouse mobile + WebPageTest (Cable/4G) перед релізом.
10. Accessibility: контраст WCAG AA, focus visible, labels на фільтрах — впливає і на SEO, і на UX mobile.

### 6.3. Хостинг

CDN (Cloudflare / Netlify / Cloudflare Pages / S3+CloudFront). Окремі проєкти/роути для двох доменів. HTTPS, HTTP/2+, HSTS.

---

## 7. Доступність і UX-деталі

- Контраст тексту на navy overlay: білий текст, перевірити AA.
- Форми/фільтри з `<label>` і `fieldset` де потрібно.
- `prefers-reduced-motion`.
- Мовне перемикання не губить шлях: `/vacancies/foo` ↔ `/en/vacancies/foo` і UA-дзеркало.
- Банер гео: dismiss + «більше не показувати».

---

## 8. Контент-активи, які треба підготувати окремо

| Asset | Статус | Примітка |
|---|---|---|
| Логотип (Φ + колос/PCB) | **Є:** `logo.svg` | Скопіювати в `assets/brand/`, зробити favicon + on-dark варіант |
| HEX фінальні | **З логотипу:** `#2E4259`, `#424443` | Токени §0 уже вирівняні |
| Фото Валерії | Потрібне | WebP 1x/2x, ≤80KB |
| CTO фото | Опційно пізніше | Місце в розмітці reserved |
| Hero visual | Згенерувати/замовити | Defence/engineering атмосфера, не стокові «солдати» |
| Іконки античні | Намалювати SVG | колос-PCB, руки, меандр |
| Calendly URL | Підставити | |
| Email | Підставити | |
| Реальні вакансії | Замінити 3 плейсхолдери | |
| Blog drafts | Тексти §3.4 розширити до full HTML | |

---

## 9. Етапи реалізації (задачі для ML-моделі)

### Task 1: Каркас репозиторію та дизайн-токени

- [ ] Створити структуру каталогів §1.2
- [ ] Підключити `logo.svg` → `assets/brand/` за §1.3 (header mark + favicon + on-dark)
- [ ] `tokens.css` з колірною/типографською шкалою §0–§2 (`--navy: #2E4259`, `--graphite: #424443`)
- [ ] Перевірити токени проти заборон §0A.7 (немає cream / amber / yellow CTA)
- [ ] Базовий layout: header/footer partials з логотипом, max-width, spacing scale (4/8/16/24/40/64)
- [ ] Підключити self-host шрифт (обраний після ліцензійної перевірки)
- **Done when:** порожня сторінка з токенами і логотипом у header, Lighthouse CSS < бюджету

### Task 2: Головна UK — розмітка всіх секцій

- [ ] Секції 1–8 з текстами §3.1
- [ ] Mobile-first CSS; sticky CTA за §2.3
- [ ] SVG-роздільники та іконки
- [ ] Organization JSON-LD + meta
- **Done when:** one-pager валідний HTML, читається без JS, mobile 375px без overflow

### Task 3: Головна EN + доменна логіка

- [ ] Дзеркало `/en/` з текстами §3.2
- [ ] hreflang + canonical
- [ ] `domain-lang.js`: банер UA, localStorage, лінки UA↔EN зі збереженням path
- [ ] Redirect `/` → `/en/` на agency
- **Done when:** ручний і «гео»-сценарії перевірені; без JS сайт лишається на вибраній мовній URL

### Task 4: Вакансії

- [ ] Контент 3 вакансій UK/EN
- [ ] List + filters + detail за §0A.5 / §4.3 (без logos, salary-filter, chat)
- [ ] JobPosting schema
- [ ] Apply CTA
- [ ] Mobile: стек-картки + filter UX
- **Done when:** фільтри працюють; деталі індексуються як окремі URL; UI не схожий на app.bazait.com

### Task 5: Блог

- [ ] 3 пости UK/EN full text за outline §3.4
- [ ] List, tag pages, post template з автором
- [ ] BlogPosting schema
- **Done when:** теги фільтрують; автор видно під кожним постом

### Task 6: Calendly, privacy, llms, robots, sitemap

- [ ] Lazy Calendly
- [ ] Privacy UK/EN
- [ ] llms.txt обидва домени
- [ ] robots + sitemap
- **Done when:** ключовий контент у view-source; AI bots дозволені

### Task 7: Перформанс і полірування mobile

- [ ] Оптимізація зображень, preload hero/font
- [ ] Видалити зайвий JS; audit third-parties (**без** Chatwoot/аналогів)
- [ ] Lighthouse mobile/desktop ≥ цілей § Global
- [ ] Ручний прохід §2.3 пристрої
- [ ] Чекліст диференціації §0A.7 (side-by-side зі скрінами конкурентів)
- [ ] Axe/accessibility smoke
- **Done when:** PageSpeed цілі досягнуті на staging URL; §0A.7 усі пункти checked

### Task 8: Контент-заміна плейсхолдерів і реліз

- [ ] Email, Calendly, фото (логотип і HEX уже з `logo.svg`)
- [ ] Прибрати демо-вакансії або замінити
- [ ] Деплой двох доменів + DNS + перевірка hreflang у Search Console
- **Done when:** прод відповідає §9 ТЗ (about.md розділ 9)

---

## 10. Критерії приймання (Definition of Done)

1. Два домени з мовною логікою §5 about.md і §0 цього плану.  
2. Усі секції головної з контентом; testimonials — empty stub.  
3. Вакансії з фільтрами; блог з тегами й авторами.  
4. Немає згадок DNA325; немає публічних цін/пакетів.  
5. Чистий HTML для контенту; llms.txt; schema; hreflang; robots дозволяє AI crawlers.  
6. Строгий defence-візуал; пройдений чекліст диференціації **§0A.7** (не плутається з Everstar / BazaIT Defense / ITExpert).  
7. Vacancies відповідають **§0A.5** + mobile стек.  
8. Mobile UX за §2.3 без критичних дефектів.  
9. Lighthouse Performance mobile ≥ 95 (або обґрунтований виняток лише через Calendly після кліку).  
10. Тексти UA та EN узгоджені за змістом (не машинний «сирий» переклад з помилками термінології Defence Tech).

---

## 11. Порядок виконання для агента (коротко)

`Task 1 → 2 → 3 → 4 → 5 → 6 → 7 → 8`  
Не починати Task 7, доки контент і сторінки не стабільні. Не підключати CMS/ATS у v1. Не писати React. Будь-який новий JS — лише якщо без нього неможливі меню / фільтри / lazy Calendly / мовний банер.

---

## 12. Відкриті плейсхолдери (підставити перед прод)

- `[EMAIL_PLACEHOLDER]`
- `[CALENDLY_URL]`
- Юридична назва / ЄДРПОУ якщо потрібні у Privacy/footer
- Реальні вакансії та фінальне біо Валерії (зараз — робочий чернетковий текст)
- Wordmark «Fidesa» у SVG відсутній — лишається текстовим у UI (узгодити трекінг/регістр з гайдлайном, якщо з’явиться)

---

*План підготований на основі `about.md`. Копірайт згенерований для старту і підлягає редактурі замовником.*
