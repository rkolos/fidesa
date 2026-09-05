# Task 7: Перформанс и полировка mobile — план реализации

> **Status 2026-09-04:** Done + audit-fixes. Evidence: `.superpowers/task-07/REPORT.md`. Lighthouse mobile **98** / desktop **100** (docroot `public/uk-site`). §0A.7 screenshots refreshed in `.firecrawl/*-shot.png`. Open non-blocking: public PSI, WebPageTest 4G, physical iOS/Android → Task 8 / ops.


> **Для агентных воркеров:** REQUIRED SUB-SKILL: `superpowers:subagent-driven-development` (рекомендуется) или `superpowers:executing-plans`. Шаги — чекбоксы `- [ ]`. **Код в этот документ не входит** — только чеклисты, бюджеты, команды проверки и DoD.
>
> **Источники:** мастер-план `docs/superpowers/plans/2026-09-04-fidesa-site-plan.md` (§0 Global, §0A.7, §2.3, §6, §7, Task 7, §10 п.6–9); `about.md` (§2 конкуренты, §9 результат).

**Goal:** Довести staging-сайт до целей PageSpeed/Lighthouse (≥95 mobile, ≥98 desktop), пройти ручной mobile UX по §2.3 и обязательный чеклист дифференциации §0A.7 — без Chatwoot/аналогов live-chat.

**Architecture:** Финальный pass поверх уже стабильных Tasks 1–6: оптимизация ассетов и сети, аудит third-party, polish sticky CTA / filters / hero, a11y smoke, side-by-side с конкурентами. Новый JS — **запрещён**, кроме правок существующих `nav.js` / `filters.js` / `calendly-lazy.js` / `domain-lang.js`, если они ломают бюджеты или UX.

**Tech Stack:** статический HTML/CSS/vanilla JS, self-host fonts, WebP/AVIF, Lighthouse CLI / PageSpeed Insights / DevTools, axe (расширение или CLI).

## Global Constraints (наследуются; не ослаблять)

- PageSpeed: **≥95 mobile**, **≥98 desktop**; LCP < 2.5s, INP < 200ms, CLS < 0.1.
- Контент в чистом HTML; B2B CTA — только Calendly (lazy).
- Без DNA325; без публичных цен/пакетов; без React/тяжёлых UI-библиотек.
- Визуал: navy `#2E4259` + graphite `#424443` + cool light — **не** cream / dark+amber / yellow CTA.
- **Не начинать Task 7**, пока Tasks 1–6 не стабильны (контент и страницы не «плывут»).
- Скрины конкурентов: `.firecrawl/*-shot.png` (Everstar, BazaIT Defense, ITExpert).

---

## Предусловия (gate перед стартом)

- [x] Task 1–6 Done when выполнены; staging URL доступен (оба корня или локальный preview обоих сайтов).
- [x] Нет открытых блокеров по контенту, требующих массовой перевёрстки секций.
- [x] Известны пути: `assets/images/`, `assets/fonts/`, `src/js/calendly-lazy.js`, CSS бандл(и).
- [x] Зафиксированы staging base URL(ы), например: `https://staging…` **или** `http://127.0.0.1:PORT` для UK и EN.

**Команда проверки gate:**

```bash
# Пример: убедиться, что ключевые страницы отдают 200
curl -sI "$STAGING_UK/" | head -1
curl -sI "$STAGING_EN/en/" | head -1
curl -sI "$STAGING_UK/vacancies/" | head -1
curl -sI "$STAGING_EN/en/vacancies/" | head -1
```

Ожидание: `HTTP/… 200` (или корректный 301/302 только для `/` → `/en/` на agency).

---

## 1. Бюджеты ресурсов (из §6.1 — mobile)

| Ресурс | Бюджет (жёсткий) | Цель «лучше» | Как мерить |
|---|---|---|---|
| HTML document | < 50 KB gzip | — | Network → документ; или `curl` + gzip size |
| CSS total | < 40 KB gzip | < 25 KB gzip | все `.css` на первом экране / total transfer |
| JS total | < 30 KB gzip | < 15 KB gzip | все first-party `.js` **до** клика Calendly |
| Hero image | < 120 KB (AVIF/WebP) | — | Network; srcset width |
| Fonts | ≤ 2 файла woff2, subset | preload только critical face | Network; latin+cyrillic subset |
| Third-party | Calendly — после interaction/visible; analytics deferred | **0** live-chat scripts | Coverage / Network blocklist |

**Core Web Vitals (из Global Constraints):**

| Метрика | Цель |
|---|---|
| LCP | < 2.5 s |
| INP | < 200 ms |
| CLS | < 0.1 |
| Lighthouse Performance | mobile ≥ 95; desktop ≥ 98 |

**Исключение (единственное, из §10 п.9):** если после клика «Открыть календарь» Lighthouse падает из‑за Calendly — метрики **до** клика должны держать цели; в отчёте зафиксировать «Calendly post-interaction only».

### Команды измерения размеров

```bash
# Gzip size одного файла (пример)
gzip -c -9 path/to/file.css | wc -c

# Сумма CSS в dist (подставить реальный путь сборки)
find dist -name '*.css' -print0 | xargs -0 -I{} sh -c 'gzip -c -9 "{}" | wc -c' | awk '{s+=$1} END {print s " bytes gzip CSS"}'

# Сумма first-party JS (без vendor calendly)
find dist -name '*.js' -print0 | xargs -0 -I{} sh -c 'gzip -c -9 "{}" | wc -c' | awk '{s+=$1} END {print s " bytes gzip JS"}'

# Размер hero
ls -la assets/images/hero*.{webp,avif,jpg,png} 2>/dev/null
```

---

## 2. Пошаговый perf checklist

### 2.1. Images

- [x] Все растровые изображения — WebP и/или AVIF; JPEG/PNG только fallback при необходимости.
- [x] Hero: `<img>`/`<picture>` с `width`/`height` **или** CSS `aspect-ratio` (CLS → 0).
- [x] Hero: `fetchpriority="high"`; **не** `loading="lazy"`.
- [x] Ниже fold (команда, blog-карточки, декоративные): `loading="lazy"` + `decoding="async"`.
- [x] Hero file ≤ 120 KB; фото Валерии ≤ 80 KB (1x/2x отдельно, если есть).
- [x] `srcset`/`sizes` для hero и крупных фото; нет «раздувания» 2x на mobile.
- [x] SVG логотип/иконки — inline или отдельные `.svg`, без icon-font (Font Awesome запрещён).
- [x] Нет стоковых «HR-рукопожатий» как главного визуала (§0A.2).

**Проверка:**

```bash
# Файлы > 120KB в images — красные флаги
find assets/images -type f \( -name '*.webp' -o -name '*.avif' -o -name '*.jpg' -o -name '*.png' \) -size +120k -ls
```

DevTools → Network (Img) на mobile emulation: LCP-элемент = hero; transfer size в бюджете.

### 2.2. Fonts

- [x] Self-host в `assets/fonts/` — **нет** runtime Google Fonts / Adobe CDN.
- [x] ≤ 2 файла woff2; начертания только **400** и **600**.
- [x] Subset: latin + cyrillic.
- [x] `font-display: swap`.
- [x] Preload **только** critical face (обычно 400 или тот, что в hero/brand).
- [x] Нет FOUT-скачка, дающего CLS > 0.1 (проверить Performance trace).

**Проверка:** Network filter `font` — 1–2 запроса, origin = свой хост; в HTML/CSS нет `fonts.googleapis.com`.

```bash
rg -n "fonts\.googleapis|fonts\.gstatic|typekit|use\.typekit" public dist src 2>/dev/null || true
```

Ожидание: пустой вывод.

### 2.3. CSS / JS

- [x] Один CSS-путь без цепочки render-blocking (critical inline **или** один минифицированный файл).
- [x] CSS total gzip < 40 KB (цель < 25).
- [x] Нет jQuery, Bootstrap, Tailwind CDN, крупных UI-kit.
- [x] JS total gzip < 30 KB до Calendly (цель < 15): только `nav`, `filters`, `domain-lang`, `calendly-lazy` (+ analytics deferred).
- [x] Фильтры: без layout thrashing; debounce на input, если есть.
- [x] Минификация HTML/CSS/JS на билде; Brotli/Gzip на CDN/host.
- [x] Hashed assets — длинный `Cache-Control`; HTML — short/revalidate.
- [x] Motion: `prefers-reduced-motion: reduce` отключает fade/translate (§2.1, §7).

**Проверка:**

```bash
rg -n "jquery|bootstrap|font-awesome|chatwoot|crisp\.chat|intercom|tawk\.to|drift\." public dist src 2>/dev/null || true
```

Ожидание: пустой вывод (нет запрещённых third-party / тяжёлых библиотек).

Coverage (DevTools): unused CSS/JS на home — вынести или удалить мёртвый код.

### 2.4. Calendly lazy

- [x] В hero **нет** iframe / `calendly.com/assets/external/widget.js` на first load.
- [x] Contacts: placeholder + кнопка «Открыть календарь» / эквивалент → inject script **once**.
- [x] Альтернатива: IntersectionObserver у секции Contacts — script только когда секция видна; на mobile лучше click-to-load (§2.3 п.4).
- [x] Fallback без JS: текстовая ссылка на `[CALENDLY_URL]`.
- [x] После открытия: iframe не ломает layout (зарезервированная высота / CLS).

**Проверка:**

1. Открыть home → Network: фильтр `calendly` — **0** запросов до клика / до scroll в Contacts (зависит от выбранной стратегии; click-to-load — строже).
2. Клик CTA → появляется один inject; повторный клик не дублирует script.
3. View-source / Disable JS → ссылка на Calendly остаётся кликабельной.

```bash
# В собранном HTML главной не должно быть widget.js в первом документе
rg -n "calendly\.com/assets/external/widget" public dist 2>/dev/null || true
```

Если совпадение есть только внутри lazy-модуля как строка URL для inject — ок; если в статическом `<script src=…>` в `<head>` home — **фейл**.

### 2.5. No Chatwoot / live-chat / лишние third-parties

- [x] **Нет** Chatwoot, Crisp, Intercom, Tawk, Drift, Facebook Messenger plugin.
- [x] Analytics: только выбранный privacy-friendly вариант (Plausible **или** GA4 + consent); deferred; не блокирует LCP (§0).
- [x] Нет лишних pixel / heatmap / A-B без явного решения в Task 8.
- [x] Vacancies: нет Sign up / Login platform / Companies tab (§0A.5).

**Проверка:** Network на cold load home + vacancies — список third-party origins; разрешены: свой CDN/host, (опционально) analytics после consent, Calendly **после** trigger. Любой chat-host — блокер релиза Task 7.

```bash
rg -ni "chatwoot|crisp|intercom|tawk|driftt|messenger\.com/t/" public dist src content 2>/dev/null || true
```

---

## 3. Mobile device matrix (320–1440) + UX checks

### 3.1. Матрица ширин (§2.3)

| Ширина (px) | Класс устройства | Обязательные проверки |
|---|---|---|
| **320** | самый узкий | overflow-x = 0; CTA в hero видим; chips/filters не клипают |
| **375** | iPhone SE / типичный | hero CTA без scroll; sticky bar (если включён) |
| **390** | iPhone 12/13/14 | то же + safe-area |
| **414** | широкие телефоны | touch targets ≥ 44×44 |
| **768** | `md` tablet | 2 колонки процесс/безопасность; команда ещё может быть stack до md |
| **1024** | `lg` | полный header **без** hamburger |
| **1440** | desktop wide | max content ~1120–1200px; без растягивания строк |

Дополнительно ОС/браузеры (§2.3 п.8): **iOS Safari** + **Chrome Android** (реальный девайс или BrowserStack; минимум — DevTools + один реальный телефон).

### 3.2. UX checks — главная (sticky CTA, hero)

- [x] **Hero CTA visible:** на 375×667 (и 320) primary «Забронювати дзвінок» / «Book a call» видим **без** вертикального scroll; если не вмещается — уменьшить supporting, **не** прятать CTA (§2.3 п.2).
- [x] Header mobile: логотип + короткий CTA («Дзвінок» / `Book`) + hamburger; язык — в drawer (§2.3 п.1).
- [x] Primary CTA всегда достижим: desktop — кнопка в header; mobile — бар или drawer + опциональный sticky.
- [x] **Sticky mobile CTA-bar** (если реализован на home): появляется после scroll > 40% hero; одна кнопка Calendly; `safe-area-inset-bottom`; **скрывается** у Contacts / не перекрывает футер (§2.3 п.6).
- [x] Calendly **не** iframe на всю страницу в hero (§2.3 п.4).
- [x] Команда: фото → био стеком до `md` (§2.3 п.5).
- [x] Никакого horizontal overflow; длинные URL/строки — wrap (§2.3 п.7).
- [x] Touch targets ≥ 44×44 px (§2.3 п.3).

**Быстрая проверка overflow:**

```javascript
// DevTools Console на каждой ширине из матрицы
document.documentElement.scrollWidth > document.documentElement.clientWidth
// Ожидание: false
```

### 3.3. UX checks — Vacancies (filters + stack)

- [x] Mobile: карточка-**стек** — title → meta → excerpt → full-width «Детальніше» / «Details» (§0A.5).
- [x] Фильтры: horizontal snap chips **или** bottom sheet / одна panel «Фільтри» — **не** desktop sidebar (§2.3 п.3, §0A.5).
- [x] Нет multi-select dropdown, вылезающего за экран.
- [x] Счётчик «N jobs found» корректен после фильтра.
- [x] Нет лого клиентов, salary-filter, Chatwoot.
- [x] Desktop (`lg+`): inline chips/selects над списком.

### 3.4. UX checks — кросс-страничные

- [x] Blog list/post: читабельная колонка, без overflow на 320.
- [x] Domain/lang banner: dismiss работает; не перекрывает sticky CTA критично.
- [x] Focus order: Tab проходит header → main → footer логично на mobile с открытым/закрытым меню.

**Ручной проход (чеклист сессии):**

- [x] 320 UK home
- [x] 375 UK home + sticky CTA сценарий
- [x] 375 UK vacancies filters
- [x] 390 EN home
- [x] 414 EN vacancies
- [x] 768 UK home (2 col)
- [x] 1024 header без hamburger
- [x] 1440 max-width
- [ ] iOS Safari spot-check
- [ ] Chrome Android spot-check

---

## 4. Accessibility smoke checklist (§6.2 п.10, §7)

- [x] Контраст текста WCAG **AA** (особенно белый текст на navy overlay hero).
- [x] `:focus-visible` виден на ссылках, кнопках, чипах фильтров, CTA.
- [x] Фильтры вакансий/блога: есть `<label>` (и `fieldset` где группа).
- [x] Кнопка меню: `aria-expanded`, понятный accessible name.
- [x] Sticky CTA / drawer не теряют фокус «в никуда»; Escape закрывает меню (если принято в реализации).
- [x] `prefers-reduced-motion` отключает анимации секций.
- [x] Изображения: смысловые — с `alt`; декоративные / logo рядом с текстом «Fidesa» — `alt=""`.
- [x] Заголовки: один H1 на страницу; иерархия без прыжков.
- [x] Без JS: контент и Calendly-ссылка доступны; фильтры могут не скрывать карточки, но список в DOM/URL деталей живой.
- [x] Языковое переключение не теряет path (§7).

**Команды / инструменты:**

```bash
# Lighthouse accessibility (Chrome)
npx --yes lighthouse "$STAGING_UK/" --only-categories=accessibility --form-factor=mobile --output=json --output-path=./lh-a11y-uk.json --chrome-flags="--headless"

# Опционально axe CLI
npx --yes @axe-core/cli "$STAGING_UK/" --exit
```

Ожидание: Lighthouse Accessibility ≥ 90 (цель 100 на простых страницах); критические axe violations = 0 (serious/critical).

Вручную: keyboard-only проход home + vacancies (Tab / Shift+Tab / Enter / Space).

---

## 5. §0A.7 Differentiation checklist (side-by-side)

Подготовить три панели/окна: **Fidesa staging home** | скрины `.firecrawl/*-shot.png` (Everstar, BazaIT Defense, ITExpert).

- [x] Скрин Fidesa home рядом со скринами трёх конкурентов: палитра / CTA / плотность **не** путаются.
- [x] Нет cream `#f5efe0`-подобных фонов, amber `#f19100`, yellow `#ffcc36` CTA.
- [x] Нет community / QR / events / survey / pricing % / client logo wall / hero lead-form / resume-upload на home.
- [x] Hero: бренд + одно специализационное обещание + Calendly — **без** stats strip.
- [x] Vacancies UX соответствует §0A.5 (логика да, UI BazaIT — нет): стек-карточки, без platform chrome.

**Дополнительные антипаттерны (быстрый audit из §0A.2–0A.4):**

- [x] Не candidate-first форма резюме на home (Everstar).
- [x] Не dark landing + amber buttons (BazaIT Defense).
- [x] Не сетка 8+ сервисных карточек / жёлтый corporate CTA (ITExpert).
- [x] Нет live-chat виджета.

**Проверка токенов:**

```bash
rg -ni "#f5efe0|#f19100|#ffcc36|#fdd835|cream|beige" src/styles assets 2>/dev/null || true
```

Ожидание: нет этих HEX как brand/CTA (допустимы только упоминания в комментариях «не использовать» — лучше убрать и из комментариев в проде).

---

## 6. Lighthouse / PageSpeed — цели и как прогонять

### 6.1. Цели

| Профиль | Performance | LCP | INP | CLS | Прочее |
|---|---|---|---|---|---|
| Mobile | ≥ **95** | < 2.5s | < 200ms | < 0.1 | Best Practices / SEO — без критических фейлов |
| Desktop | ≥ **98** | < 2.5s | < 200ms | < 0.1 | то же |

Страницы минимум: UK `/`, EN `/en/`, UK `/vacancies/`, одна vacancy detail, blog index. Home — обязательный gate; остальные — если падение >5 баллов из‑за общего бандла, фиксить бандл.

### 6.2. Локальный Lighthouse CLI

```bash
export STAGING_UK="http://127.0.0.1:PORT"   # или https://staging…
export STAGING_EN="http://127.0.0.1:PORT"

# Mobile home UK
npx --yes lighthouse "$STAGING_UK/" \
  --only-categories=performance,accessibility,best-practices,seo \
  --form-factor=mobile \
  --screenEmulation.mobile=true \
  --throttling-method=simulate \
  --output=html --output-path=./lh-mobile-uk-home.html \
  --chrome-flags="--headless"

# Desktop home UK
npx --yes lighthouse "$STAGING_UK/" \
  --only-categories=performance \
  --preset=desktop \
  --output=html --output-path=./lh-desktop-uk-home.html \
  --chrome-flags="--headless"

# Mobile EN + vacancies (повторить с URL)
npx --yes lighthouse "$STAGING_EN/en/" --only-categories=performance --form-factor=mobile --output=html --output-path=./lh-mobile-en-home.html --chrome-flags="--headless"
npx --yes lighthouse "$STAGING_UK/vacancies/" --only-categories=performance --form-factor=mobile --output=html --output-path=./lh-mobile-uk-vacancies.html --chrome-flags="--headless"
```

Ожидание: в HTML-отчёте Performance ≥95 (mobile) / ≥98 (desktop); проверить LCP element и unused JS.

### 6.3. Google PageSpeed Insights (staging с публичным URL)

1. Открыть [PageSpeed Insights](https://pagespeed.web.dev/).
2. Вставить staging URL UK home → Run.
3. Зафиксировать Mobile + Desktop scores и CWV.
4. Повторить для EN home.
5. Сохранить скрины/PDF в заметки релиза (не обязательно в репо).

Ожидание: те же пороги, что в §6.1. Если PSI и локальный Lighthouse расходятся >3 балла — брать **худший** как gate, пока не выяснен throttling/CDN.

### 6.4. WebPageTest (по §6.2 п.9)

- Профиль: **Mobile, 4G** (или Cable + mobile Emulation).
- Смотреть filmstrip: hero LCP; нет долгой блокировки main thread до interaction.
- Waterfall: Calendly отсутствует на first view.

### 6.5. DevTools Performance / Network (быстрый ритуал)

1. Network → Disable cache → Mobile → Reload.
2. Проверить бюджеты из таблицы §1.
3. Performance: record load; LCP/CLS markers.
4. После клика Calendly — отдельная запись (не смешивать с cold-load score).

---

## 7. Checkbox steps (порядок выполнения)

### Шаг A — Baseline

- [x] Зафиксировать staging URL и commit/hash сборки.
- [x] Прогнать Lighthouse mobile home (UK) — сохранить baseline score.
- [x] Снять Network waterfall cold load (скрин или HAR).

### Шаг B — Images & fonts

- [x] Пройти §2.1 Images; сжать/перекодировать нарушителей бюджета.
- [x] Пройти §2.2 Fonts; убрать CDN; оставить ≤2 woff2.
- [x] Повторный Lighthouse mobile — сравнить LCP.

### Шаг C — CSS/JS trim

- [x] Пройти §2.3; удалить мёртвый CSS/JS; проверить суммы gzip.
- [x] `rg` на jquery/bootstrap/chatwoot — чисто.
- [x] Повторный Lighthouse; JS boot < бюджета.

### Шаг D — Calendly & third-parties

- [x] Подтвердить lazy §2.4; zero Calendly на cold load (или только IO после Contacts — задокументировать выбор).
- [x] Подтвердить §2.5 No Chatwoot.
- [x] Analytics deferred / за consent.

### Шаг E — Mobile matrix UX

- [x] Пройти §3.1–§3.4 на всех ширинах; список дефектов → фикс → ретест.
- [x] Sticky CTA: scroll 40% / hide near Contacts.
- [x] Vacancies filters + stack на 320–414.

### Шаг F — A11y smoke

- [x] Пройти §4; Lighthouse a11y + axe; клавиатурный проход.

### Шаг G — Differentiation §0A.7

- [x] Side-by-side со скринами конкурентов; все пункты §5 checked.

### Шаг H — Final scores

- [x] Lighthouse mobile ≥95 и desktop ≥98 на UK home (+ spot EN/vacancies).
- [ ] PSI на публичном staging (если есть).
- [ ] WebPageTest 4G spot-check.
- [x] Записать финальные цифры в короткий отчёт (комментарий к PR / заметка).

### Шаг I — DoD review

- [x] Пройти Definition of Done ниже; не открывать Task 8, пока Task 7 красный.

---

## 8. Definition of Done

Task 7 **закрыт**, когда выполнено **всё**:

1. **Бюджеты §1** соблюдены на cold load home (mobile), кроме осознанно post-interaction Calendly.
2. **Perf checklist §2** полностью checked; `rg` на Chatwoot/тяжёлые libs — пустой.
3. **Mobile matrix §3** пройдена без критических дефектов (overflow, спрятанный hero CTA, сломанные filters, sticky, съедающий футер).
4. **A11y smoke §4** без critical/serious; focus visible; AA контраст на hero.
5. **§0A.7** все пункты checked (side-by-side с Everstar / BazaIT Defense / ITExpert).
6. **Lighthouse / PageSpeed:** Performance **mobile ≥ 95**, **desktop ≥ 98** на staging URL; LCP/INP/CLS в пределах Global Constraints.
7. Единственное допустимое исключение по score — обосновано в отчёте **только** как влияние Calendly **после** клика; cold load остаётся в целях (§10 п.9 мастер-плана).
8. Не добавлен новый JS вне существующих модулей меню / фильтров / lazy Calendly / языкового баннера (§11).

**Не входит в Task 7:** замена плейсхолдеров email/фото/реальных вакансий и прод-DNS (это Task 8).

---

## 9. Артефакты на выходе

| Артефакт | Назначение |
|---|---|
| `lh-mobile-uk-home.html` (+ EN/vacancies по необходимости) | Доказательство Performance |
| Короткий markdown/PR-комментарий с цифрами PSI/Lighthouse | Handoff в Task 8 |
| Чеклист §0A.7 с датой прохождения | Приёмка §10 п.6 |
| Список «известных non-blocking» (если есть) | Только косметика, не CWV |

---

## 10. Ссылки на мастер-план

| Тема | Секция |
|---|---|
| Цели CWV / PageSpeed | Global Constraints; §10 п.9 |
| Бюджеты и техники | §6.1–§6.2 |
| Mobile breakpoints & UX | §2.3 |
| Дифференциация | §0A.7 (+ антипаттерны 0A.2–0A.4) |
| Vacancies mobile | §0A.5 |
| A11y | §7; §6.2 п.10 |
| Task 7 one-liner | §9 Task 7 |
| Порядок | §11 — после Task 6, перед Task 8 |

---

*План Task 7. Другие tasks не менять. Код в этот файл не добавлять — только выполнять чеклисты на стабильной сборке Tasks 1–6.*
