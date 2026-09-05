# Task 1: Каркас репозиторію та дизайн-токени

> **Для агентних воркерів:** виконувати лише цю задачу. Код у план не входить (або мінімальна псевдоструктура без повних лістингів). Джерело правди: `docs/superpowers/plans/2026-09-04-fidesa-site-plan.md` (§0, §0A.7, §1.2–1.3, §2, §6.1, §9 Task 1). ТЗ: `about.md`. Логотип: `logo.svg`.

**Goal:** Підняти файловий каркас статичного сайту Fidesa, зафіксувати дизайн-токени з кольорів логотипу, підготувати brand-ассети за §1.3 і мінімальний header/footer shell — без контентних секцій головної (це Task 2).

**Architecture:** Чистий HTML + CSS custom properties. Один спільний `src/styles/` і `assets/brand/` для обох майбутніх деплоїв (`uk-site` / `en-site`). На цьому етапі — одна порожня smoke-сторінка (UK-скелет), що підключає токени й partials.

**Tech Stack:** HTML5, CSS3 (custom properties), SVG (inline / файли), self-host `woff2` (після ліцензійної перевірки). Без React/Vue/Next, без UI-бібліотек, без Google Fonts CDN.

---

## Global Constraints (коротко)

| Обмеження | Значення |
|---|---|
| Вихід | **Статичний HTML** (або SSG → static). SPA без pre-render — заборонено |
| Домени | `fidesa.com.ua` = лише UK; `fidesa.agency` = багатомовний, старт `/en/` |
| Бренд | Лише **Fidesa** / Defence Tech; **жодних** згадок DNA325 |
| CTA B2B | Лише Calendly (на Task 1 — кнопка-заглушка без iframe) |
| Дизайн | Світлий cool navy/steel + graphite; **не** cream, **не** dark+amber, **не** yellow CTA |
| PageSpeed | Ціль проєкту ≥95 mobile / ≥98 desktop; у Task 1 — CSS у бюджеті §6.1 |
| Шрифт | Гротеск **не** російського/білоруського походження; Inter як дефолт — **не** брати |

---

## 1. Мета і залежності

### Мета Task 1

1. Створити дерево каталогів §1.2 (порожні/мінімальні файли там, де ще немає контенту).
2. Зафіксувати колірні, типографічні, spacing і breakpoint-токени в `tokens.css`.
3. Підготувати логотип у `assets/brand/` за правилами §1.3 (mark, favicon, on-dark, wordmark текстом).
4. Зібрати мінімальний layout: skip-link, sticky header (logo + wordmark + CTA + hamburger-заглушка), footer, content max-width.
5. Підключити обраний self-host шрифт (400 + 600).
6. Перевірити заборонені палітри §0A.7 і CSS-бюджет Lighthouse.

### Що має бути ДО Task 1

| Артефакт | Статус |
|---|---|
| `about.md` | Є |
| Майстер-план `2026-09-04-fidesa-site-plan.md` | Є |
| `logo.svg` у корені (viewBox `0 0 448 509`) | Є |
| CMS / ATS / контент секцій | **Не потрібні** |

### Що йде ПІСЛЯ Task 1

| Наступна задача | Що споживає з Task 1 |
|---|---|
| **Task 2** — Головна UK, усі секції | `tokens.css`, layout, header/footer, brand assets, шрифт |
| Task 3+ | Ті самі токени/partials; дублювати палітру/структуру не можна |

### Поза scope Task 1 (не робити)

- Секції Hero / About / Process / Why / Team / Testimonials / Contacts з текстами §3.1
- EN-дзеркало, hreflang, `domain-lang.js`, redirect agency
- Вакансії, блог, Calendly iframe, privacy, llms.txt, sitemap
- Фото Валерії, hero-фото, античні іконки (меандр у футері — лише тонкий placeholder SVG ок)
- Аналітика, CMS, мініфікація продакшн-білду (ок мінімальний README / package later)

---

## 2. Точні шляхи файлів

### Створити (каталоги + файли)

```
/
├── assets/
│   ├── brand/
│   │   ├── logo.svg              # копія/оптимізація з кореня logo.svg
│   │   ├── logo-mark.svg         # знак без зайвого padding (за потреби)
│   │   ├── logo-on-dark.svg      # knockout / currentColor для темного overlay
│   │   ├── favicon.svg           # спрощений Φ, 16–32 читабельність
│   │   └── apple-touch-icon.png  # 180×180, navy фон за потреби (можна пізніше Task 7 — якщо немає пайплайну PNG, задокументувати TODO у README каркасу)
│   ├── fonts/                    # woff2 subset (latin + cyrillic), ≤2 файли
│   ├── images/                   # порожньо (placeholder .gitkeep)
│   └── icons/                    # порожньо або мінімальний hamburger SVG
├── content/
│   ├── uk/                       # .gitkeep + порожні підпапки
│   │   ├── vacancies/
│   │   └── blog/
│   └── en/
│       ├── vacancies/
│       └── blog/
├── public/
│   ├── uk-site/                  # smoke HTML для com.ua-каркасу
│   └── en-site/                  # .gitkeep (контент — Task 3)
├── src/
│   ├── styles/
│   │   ├── tokens.css            # обовʼязково
│   │   ├── base.css              # reset/мінімум typography apply
│   │   ├── layout.css            # header, footer, shell, max-width
│   │   ├── components.css        # CTA кнопка, skip-link (мінімум)
│   │   └── pages.css             # порожній або коментар «Task 2+»
│   ├── js/
│   │   └── nav.js                # мінімум: відкрити/закрити mobile drawer (або заглушка aria)
│   ├── partials/
│   │   ├── header.html
│   │   └── footer.html
│   └── pages/
│       └── smoke-uk.html         # або public/uk-site/index.html — одна порожня сторінка
├── logo.svg                      # НЕ чіпати як джерело правди (лише читати/копіювати)
└── README.md                     # коротко: структура, як відкрити smoke, який шрифт обрано
```

**Примітка для агента:** якщо SSG ще не обрано — тримати «живу» smoke-сторінку в `public/uk-site/index.html` з інлайн-включенням CSS через `<link>` на зібрані/відносні шляхи до `src/styles/*` **або** скопійовані CSS у `public/uk-site/css/` для локального відкриття. Головне: одна сторінка відкривається в браузері без білдера. Не розгалужувати два розбіжні набори токенів.

### Не створювати в Task 1

- `content/uk/home.md`, `team.json`, vacancy/blog MD з контентом
- `calendly-lazy.js`, `filters.js`, `domain-lang.js` (порожні stub-файли **не** обовʼязкові)
- Повні сторінки vacancies/blog/privacy

---

## 3. Дизайн-токени (з майстер-плану §0 / §2)

### 3.1. Кольори (джерело: `logo.svg`)

| Token | HEX | Роль |
|---|---|---|
| `--navy` | `#2E4259` | Бренд, заголовки, header accents, primary CTA |
| `--graphite` | `#424443` | Акцентний графіт, вторинні елементи, іконки |
| `--navy-mid` | `#3D566F` | Hover / mid (похідна navy) |
| `--steel` | `#5A738C` | Стриманий акцент ліній |
| `--ink` | `#1A1C1B` | Body text |
| `--ink-muted` | `#5C6570` | Secondary text |
| `--bg` | `#F7F8FA` | Фон сторінки |
| `--surface` | `#FFFFFF` | Header/footer/surface |
| `--line` | `#D8DEE6` | Роздільники 1px |
| `--focus` | `#2E4259` | Focus ring 2px (= navy) |
| `--on-navy` | `#FFFFFF` | Текст/іконки на navy CTA |

**Заборонено додавати** як бренд-токени: cream/beige (`#f5efe0` тощо), amber (`#f19100`), yellow CTA (`#ffcc36` / `#fdd835`), purple/neon accents.

### 3.2. Типографіка (§2.2)

| Роль | Desktop | Mobile | Вага |
|---|---|---|---|
| Brand / Display | `clamp(2.5rem, 5vw, 3.75rem)` | ~2.25rem | 600–700 |
| H1 | 2rem–2.5rem | 1.75rem | 600 |
| H2 | 1.75rem | 1.5rem | 600 |
| H3 | 1.25rem | 1.125rem | 600 |
| Body | 1.0625–1.125rem / line-height 1.6 | 1rem / 1.55 | 400 |
| Small / meta | 0.875rem | 0.8125rem | 400 |

Токени-змінні (імена на розсуд, семантика обовʼязкова): наприклад `--font-sans`, `--fs-brand`, `--fs-h1` … `--fs-small`, `--lh-body`, `--fw-regular` (400), `--fw-semibold` (600).

**Шрифт — вибір у Task 1 (один раз, зафіксувати в README):**

Кандидати з майстер-плану (перевірити ліцензію + відсутність РФ/БЛР походження): **IBM Plex Sans**, **Source Sans 3**, **Manrope**, **Geist**; або українські e-Ukraine / Mak / Kyiv Type якщо ліцензія дозволяє.

Правила:
- Self-host `woff2`, subset **latin + cyrillic**
- `font-display: swap`
- Не більше **2** накреслень: 400 і 600
- Preload лише critical woff2 (один файл body або combined)
- **Не** підключати Google Fonts CDN у runtime
- **Не** брати Inter як дефолт «бо звично»

### 3.3. Spacing scale

Фіксована шкала (px → rem у CSS): **4 / 8 / 16 / 24 / 40 / 64**.

Приклад імен: `--space-1` … або `--space-xs/sm/md/lg/xl/2xl` — головне: використовувати лише цю шкалу в header/footer/shell.

### 3.4. Breakpoints (§2.3)

| Token | px | Поведінка для каркасу |
|---|---|---|
| `sm` | 480 | дрібні правки відступів |
| `md` | 768 | (для Task 1 майже не змінює header) |
| `lg` | 1024 | повний header **без** hamburger; nav inline |
| `xl` | 1280 | max content width ~**1120–1200px** |

Mobile-first: базові стилі = mobile; `@media (min-width: 1024px)` — desktop header.

### 3.5. Інші layout-токени (мінімум)

- `--content-max`: 1120px або 1200px
- `--header-h-mobile` / `--header-h-desktop` (узгодити з висотою лого 28–40px + padding)
- `--radius`: малий або 0 для defence-строгості (не rounded-full pills)
- `--shadow`: **немає** multi-layer; для sticky header — solid background, blur лише якщо не бʼє perf (за замовчуванням solid `--surface`)

---

## 4. Правила логотипа (§1.3) — обовʼязково

**Файл-джерело:** `/logo.svg` (viewBox `0 0 448 509`, вертикальний комбінований знак Φ + колос/PCB).

**Палітра з файлу (не вигадувати інші бренд-кольори):**
- `#2E4259` — navy (літера Φ / зовнішній контур)
- `#424443` — graphite (колос → мікросхема)

**Розміщення в header:**
- Висота знака: **28–32px** (mobile), **36–40px** (desktop)
- Поруч (або під на дуже вузьких) wordmark **«Fidesa»** — **текстом** у гротеску (у SVG лише знак без напису; не раструвати wordmark)
- Посилання логоблоку → home (`/` для UK smoke)

**Hero / on-dark (підготовка ассета зараз, використання — Task 2):**
- Не розмивати, не перефарбовувати в неон
- На темному overlay: оригінальні fill **або** knockout `#FFFFFF` / `#F7F8FA`
- Окремий `logo-on-dark.svg` з `fill="currentColor"` (або фіксованим білим) — створити в Task 1

**Favicon:**
- Спростити до читабельного Φ на 16–32px
- Фон: `--navy` або прозорий
- Підключити в smoke `<link rel="icon" href="…favicon.svg">`

**Заборони для лого:**
- Не обводити тінями, градієнтами, glow
- `alt="Fidesa"` якщо знак один без видимого тексту; якщо поруч видимий wordmark — у `<img>` `alt=""` + текст «Fidesa» у DOM

**Перед «готово» по ассетах:**
- SVGO-оптимізація зі **збереженням обох fill** `#2E4259` і `#424443`
- Візуальна перевірка контрасту знака на `--bg` і (окремо) preview on-dark на navy прямокутнику

---

## 5. Заборони з §0A.7 (диференціація)

Перед Done — обовʼязковий самочек токенів і smoke-сторінки:

- [ ] Немає cream / beige / warm paper фонів (`#f5efe0`-подібні)
- [ ] Немає amber `#f19100` і yellow `#ffcc36` / `#fdd835` у CTA або accents
- [ ] Немає dark-mode лендінгу за замовчуванням і amber CTA
- [ ] Primary CTA = `--navy` фон + `--on-navy` текст (не жовтий, не «corporate yellow+white+black»)
- [ ] Немає purple-градієнтів, неону, glow
- [ ] У каркасі немає community/QR/stats/pricing/client logos (і не закладати під них токени)

Конкурентні антипатерни (памʼятка): Everstar = cream+фото; BazaIT Defense = dark+amber; ITExpert = white+yellow. Fidesa = cool navy `#2E4259` + graphite `#424443` + світлий `--bg`.

---

## 6. Mobile-first вимоги каркаса header / footer

### Header (спільний контракт для Task 2+)

- Sticky; фон `--surface` (solid за замовчуванням)
- Skip link першим у DOM: UK текст `Перейти до контенту` (EN пізніше: `Skip to content`)
- **Mobile (&lt; lg):** логотип (знак + wordmark) + короткий CTA + hamburger
  - CTA short UK: **`Дзвінок`** (повний текст кнопки desktop: **`Забронювати дзвінок`**)
  - CTA short EN (закласти data/коментар): `Book` / full `Book a call`
  - Мовне посилання **в drawer**, не обовʼязково в барі: на UK smoke — лінк `EN` → `#` або `https://fidesa.agency/en/` (поки без path-sync)
- **Desktop (≥ lg):** logo + nav anchors-заглушки + повний CTA; без hamburger
- Nav labels UK (плейсхолдери для майбутніх якорів, можна `href="#"`):  
  `Про нас` · `Процес` · `Чому Fidesa` · `Команда` · `Вакансії` · `Блог` · `Контакти`
- Touch targets ≥ **44×44px** (hamburger, CTA, domain link)
- Primary CTA завжди видимий на mobile (у барі, не лише в drawer)
- Жодного horizontal overflow на 320–414px

### Footer (мінімум)

- Brand «Fidesa» + короткий рядок: `Спеціалізований рекрутинг для Defence Tech`
- Links: `Вакансії` · `Блог` · `Privacy` · `EN` (agency)
- © `© 2026 Fidesa` (рік можна `{year}` коментарем / статично 2026 на старті)
- Декор: опційно тонка лінія/`--line` або мінімальний SVG-меандр без кольору-акценту (не обовʼязково повний малюнок)
- Без client logo wall, без QR, без pricing

### Smoke-сторінка

- Одна колонка: header → `<main id="content">` з коротким плейсхолдером (напр. «Fidesa — каркас») → footer
- `lang="uk"`
- Без hero full-bleed і без секційного контенту Task 2

---

## 7. Покрокові checkbox-кроки для агента

### Крок A — Каталоги

- [ ] **A1.** Створити дерево `assets/`, `content/uk|en` (+ vacancies/blog), `public/uk-site`, `public/en-site`, `src/styles`, `src/js`, `src/partials`, `src/pages` за §2 цього плану.
- [ ] **A2.** Додати `.gitkeep` у порожні `images/`, `icons/`, `content/**`, `public/en-site/`.
- [ ] **A3.** Короткий `README.md`: структура, як відкрити smoke, обраний шрифт (після кроку D), посилання на майстер-план.

### Крок B — Brand assets (§1.3)

- [ ] **B1.** Скопіювати кореневий `logo.svg` → `assets/brand/logo.svg`.
- [ ] **B2.** Прогнати SVGO (зберегти fill `#2E4259` і `#424443`); за потреби винести `logo-mark.svg` з тугішим crop.
- [ ] **B3.** Створити `favicon.svg` (спрощений Φ, читабельний на 16–32px).
- [ ] **B4.** Створити `logo-on-dark.svg` (knockout / `currentColor`).
- [ ] **B5.** Візуально перевірити logo на `#F7F8FA` і on-dark на `#2E4259`; без glow/shadow у файлах.
- [ ] **B6.** (Опційно) `apple-touch-icon.png` 180×180; якщо PNG не генерується — записати в README як follow-up Task 7/8, не блокувати Done.

### Крок C — Токени і базові стилі

- [ ] **C1.** Написати `src/styles/tokens.css`: усі кольори §3.1, typography §3.2, spacing §3.3, breakpoints як custom media або задокументовані значення, `--content-max`.
- [ ] **C2.** Самочек §0A.7: у файлі **немає** cream/amber/yellow токенів.
- [ ] **C3.** `base.css`: мінімальний reset, `body` → `--ink` на `--bg`, застосування `--font-sans`.
- [ ] **C4.** `layout.css`: shell, sticky header, footer, max-width container, mobile/desktop nav breakpoints.
- [ ] **C5.** `components.css`: skip-link, primary button (navy), icon-button hamburger.
- [ ] **C6.** `pages.css`: залишити порожнім або з коментарем `/* Task 2+ */`.

### Крок D — Шрифт

- [ ] **D1.** Обрати один гарнітур з кандидатів; перевірити ліцензію і походження (не РФ/БЛР).
- [ ] **D2.** Покласти ≤2 файли `woff2` (400, 600) з subset latin+cyrillic у `assets/fonts/`.
- [ ] **D3.** Підключити через `@font-face` у CSS (`font-display: swap`); preload critical у smoke HTML.
- [ ] **D4.** Зафіксувати назву шрифта і ліцензію одним рядком у `README.md`.

### Крок E — Partials + smoke HTML

- [ ] **E1.** `header.html`: skip-link, logo img/SVG + текстовий wordmark «Fidesa», nav UK labels, CTA (`Дзвінок` / `Забронювати дзвінок`), hamburger, drawer з `EN`.
- [ ] **E2.** `footer.html`: brand line, links, ©.
- [ ] **E3.** Зібрати `public/uk-site/index.html` (або еквівалент): `lang="uk"`, favicon, CSS links, вставка header/footer (копіпаста з partials ок на цьому етапі), `<main id="content">`.
- [ ] **E4.** Розміри лого в CSS: 28–32px mobile / 36–40px desktop; `alt` за §1.3.
- [ ] **E5.** Мінімальний `nav.js`: toggle `aria-expanded` на hamburger + відкриття drawer; без залежностей. Якщо JS вимкнено — CTA і skip-link лишаються клікабельними; nav можна показати fallback-посиланнями в footer.

### Крок F — Перевірка

- [ ] **F1.** Відкрити smoke на viewport **320, 375, 390, 414, 768, 1024, 1440** — немає horizontal overflow; CTA видимий на mobile.
- [ ] **F2.** Перевірити focus visible на skip-link, CTA, hamburger (кільце = `--focus`).
- [ ] **F3.** Lighthouse (mobile) або еквівалент: **CSS total &lt; 40 KB gzip** (ціль &lt; 25 KB); немає зайвих шрифтів/CDN.
- [ ] **F4.** Повторити чекліст §5 (§0A.7) на скріні header.
- [ ] **F5.** Переконатися, що кореневий `logo.svg` не змінений деструктивно (джерело правди збережене).

---

## 8. Definition of Done + як перевірити

### Done when

1. Дерево §1.2 (мінімум для Task 1) існує; smoke UK-сторінка відкривається локально.
2. `tokens.css` містить повну палітру з `--navy: #2E4259` і `--graphite: #424443` плюс похідні з майстер-плану.
3. Brand: `assets/brand/logo.svg`, `favicon.svg`, `logo-on-dark.svg`; wordmark «Fidesa» текстом у header.
4. Header/footer відповідають mobile-first правилам §6; touch ≥44px; breakpoint `lg` 1024.
5. Self-host шрифт підключений (400+600), зафіксований у README; не Inter-by-default; не Google CDN.
6. Немає cream/amber/yellow у токенах і CTA (§0A.7).
7. Lighthouse / розмір: **CSS сумарно &lt; 40 KB gzip** (краще &lt; 25); JS лише мінімальний `nav.js` або відсутній при прийнятному a11y-fallback.
8. Немає контентних секцій Task 2 і немає згадок DNA325.

### Команди / перевірки (орієнтири)

| Перевірка | Як |
|---|---|
| Відкрити smoke | Відкрити `public/uk-site/index.html` через локальний static server (не `file://` якщо preload/шлях ламається) |
| Розмір CSS | Gzip розміру всіх CSS, підключених до smoke: `gzip -c … \| wc -c` або Lighthouse «Network» |
| Lighthouse | Chrome DevTools → Lighthouse → Mobile → Performance; зафіксувати, що CSS не роздуває budget |
| Контраст | Wordmark + body на `--bg`; CTA `--on-navy` на `--navy` — WCAG AA |
| Overflow | DevTools responsive: 320px width, немає горизонтального скролу |
| Лого | Інспекція висоти img/svg у header на 375 і 1280 |

### Не вимагається для Done Task 1

- PageSpeed 95 на порожній сторінці як абсолютний гейт (ціль проєкту — на Task 7); **гейтяться** CSS budget і відсутність важких залежностей
- Повний axe-аудит усіх майбутніх сторінок
- EN-сайт і dual-domain деплой

---

## 9. Тексти UI для каркаса (зафіксувати як є)

**UK (smoke):**

| Елемент | Текст |
|---|---|
| Skip | `Перейти до контенту` |
| Wordmark | `Fidesa` |
| CTA full | `Забронювати дзвінок` |
| CTA short | `Дзвінок` |
| Domain | `EN` |
| Nav | `Про нас` · `Процес` · `Чому Fidesa` · `Команда` · `Вакансії` · `Блог` · `Контакти` |
| Footer tagline | `Спеціалізований рекрутинг для Defence Tech` |
| Footer links | `Вакансії` · `Блог` · `Privacy` · `EN` |
| © | `© 2026 Fidesa` |
| Main placeholder | `Fidesa — каркас` (або еквівалент без маркетингового героя) |

**EN (лише закладка в коментарі/data для Task 3, не обовʼязково верстати):**  
Skip `Skip to content` · CTA `Book a call` / `Book` · Domain `UA` · Nav About · Process · Why Fidesa · Team · Vacancies · Blog · Contact · tagline `Specialized recruiting for Defence Tech`.

CTA `href` на цьому етапі: `#contacts` або `#` (Calendly URL — плейсхолдер `[CALENDLY_URL]`, не вбудовувати iframe).

---

## 10. Інтерфейси для наступних задач

**Produces (контракт):**

- CSS variables з іменами кольорів як у §3.1 (обовʼязкові `--navy`, `--graphite`, …)
- Partials header/footer з тими самими class-іменами, що на smoke (задокументувати в README: напр. `.site-header`, `.site-footer`, `.btn-primary`, `.nav-toggle`)
- Шляхи brand: `assets/brand/logo.svg`, `favicon.svg`, `logo-on-dark.svg`
- Breakpoint `lg = 1024px` для перемикання hamburger ↔ full nav

**Consumes:** лише кореневий `logo.svg` + майстер-план / about.md.

---

## 11. Ризики і рішення «на місці»

| Ризик | Рішення |
|---|---|
| Ліцензія улюбленого шрифта неясна | Взяти наступний кандидат з списку (IBM Plex Sans / Source Sans 3 зазвичай безпечні) |
| SVGO зрізає fill | Повторити з прапорцями preserve; звірити HEX |
| Partial include без SSG | Дублювати HTML partial → smoke один раз; у README написати «синхронізувати partials вручну до появи білдера» |
| CSS &gt; 40 KB gzip | Прибрати зайві utility, не тягнути reset-фреймворки |

---

*Кінець плану Task 1. Наступний документ: Task 2 (головна UK — секції). Не починати Task 2, доки DoD цього файлу не виконано.*
