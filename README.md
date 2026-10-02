# Fidesa site

Статичний сайт рекрутингової агенції **Fidesa** (Defence Tech). Джерело плану: [`docs/superpowers/plans/2026-09-04-fidesa-site-plan.md`](docs/superpowers/plans/2026-09-04-fidesa-site-plan.md). Задачі: [`docs/superpowers/plans/tasks/`](docs/superpowers/plans/tasks/).

## Структура

```
assets/brand/     # logo.svg, logo-mark, logo-on-dark, favicon
assets/fonts/     # self-host woff2
assets/css/       # site.css — зібраний бандл
js/               # копія src/js для root-absolute /js/ (sync)
content/uk|en/    # майбутній контент (vacancies, blog)
public/uk-site/   # деплой com.ua (містить assets/ + js/ після sync)
public/en-site/   # деплой agency: EN у корені, легасі `/en/*` → 301 на `/`
src/styles/       # джерела: tokens, base, layout, components, pages
src/partials/     # header/footer (uk|en), lang-banner
src/js/           # джерела JS (nav, sticky-cta, domain-lang, filters, calendly-lazy)
```

Кореневий `logo.svg` — джерело правди для бренду (не змінювати деструктивно).

### Локальна розробка

```bash
./scripts/dev.sh start     # збірка + UK на :8080, EN на :8081
./scripts/dev.sh build     # лише перезбірка (CSS + блог)
./scripts/dev.sh restart   # перезапуск після змін у scripts/
./scripts/dev.sh stop
./scripts/dev.sh status
./scripts/dev.sh logs
```

UK: [http://localhost:8080/](http://localhost:8080/) · EN: [http://localhost:8081/](http://localhost:8081/)

`scripts/dev_server.py` повторює поведінку продакшену: віддає `404.html` зі статусом 404
і робить 301 з легасі `/en/*` на корінь (як `_redirects` + `.htaccess` на agency).

### Збірка статики

```bash
python3 scripts/build_static.py
```

Це збирає `assets/css/site.css` і копіює `assets/` + `js/` у `public/uk-site/` та `public/en-site/` (і `js/` у корінь репо). Сторінки підключають root-absolute `/assets/...` і `/js/...`.


## Головна UK (Task 2)

Контент-джерело: `content/uk/home.md`. Partials у `src/partials/` синхронізуються вручну в `public/uk-site/index.html` до появи SSG/білдера.

## Головна EN + domain (Task 3)

EN-сайт живе в корені `fidesa.agency` (не під `/en/`). Preview — `./scripts/dev.sh start`, порт 8081.

- Контент: `content/en/home.md` → `public/en-site/index.html`
- Легасі `/en/*` → 301 на корінь: `public/en-site/_redirects` (Netlify/CF), `.htaccess` (Apache/LiteSpeed), `public/en-site/en/index.html` (meta-refresh fallback)
- `src/js/domain-lang.js` — path-aware UA↔EN (`data-domain-switch`), geo-банер на agency (Accept-Language `uk`, localStorage `fidesa.*`)
- Для prod document root = `public/en-site/` (ассети під `/assets/` — окремий deploy wiring у Task 8)

`assets/brand/og-default.svg` — тимчасовий OG; перед продом потрібен raster 1200×630 (Task 7/8).

## Вакансії (Task 4)

Контент: `content/uk|en/vacancies/*.md` → HTML у `public/uk-site/vacancies/` і `public/en-site/en/vacancies/` (list + 3 detail, спільні slug).

```bash
python3 -m http.server 8080
```

- UK list: [http://localhost:8080/public/uk-site/vacancies/](http://localhost:8080/public/uk-site/vacancies/)
- EN list: [http://localhost:8080/public/en-site/en/vacancies/](http://localhost:8080/public/en-site/en/vacancies/)
- Фільтри: `src/js/filters.js` (`?direction=&location=&format=`), Apply — `mailto:[EMAIL_PLACEHOLDER]` (заміна в Task 8)

## Блог (Task 5)

Контент: `content/uk|en/blog/*.md` → HTML у `public/uk-site/blog/` і `public/en-site/en/blog/` (list + 5 tag + 3 post × UK/EN).

Перезбірка після правок контенту:

```bash
python3 scripts/build_blog.py
python3 -m http.server 8080
```

- UK list: [http://localhost:8080/public/uk-site/blog/](http://localhost:8080/public/uk-site/blog/)
- EN list: [http://localhost:8080/public/en-site/en/blog/](http://localhost:8080/public/en-site/en/blog/)
- Tag URL: `/blog/tag/{id}/` (і `/en/...`); related posts за перетином тегів; JSON-LD `BlogPosting`

## Calendly / Privacy / SEO-AI (Task 6)

- Lazy Calendly: `src/js/calendly-lazy.js` лише на home (`public/uk-site/index.html`, `public/en-site/en/index.html`). URL для JS — `data-calendly-url` на `[data-calendly-root]`; плейсхолдер `[CALENDLY_URL]` до Task 8 (кнопка не ламає fallback).
- Privacy: `/privacy/` · `/en/privacy/`
- Корені деплою: `llms.txt`, `robots.txt`, `sitemap.xml` у `public/uk-site/` і `public/en-site/`
- `x-default` hreflang проєкту: завжди `https://fidesa.agency/en/` (home, blog, privacy, vacancies)
- Contacts markup синхронізується вручну між UK/EN home (partial ще немає)

### CSS-класи (контракт для Task 2+)

| Клас | Роль |
|---|---|
| `.site-header` | Sticky header |
| `.site-footer` | Footer |
| `.btn-primary` | Primary CTA (navy) |
| `.nav-toggle` | Hamburger (&lt; lg) |
| `.nav-drawer` | Mobile menu |
| `.container` | max-width `--content-max` |

Breakpoint `lg = 1024px`: hamburger → повний nav.

## Шрифт

**IBM Plex Sans** (400 + 600), subset latin + cyrillic + latin-ext, self-host `woff2`, `font-display: swap`. Ліцензія: [OFL / SIL Open Font License](https://github.com/IBM/plex/blob/master/LICENSE.txt) (IBM Plex). Не Google Fonts CDN; не Inter.

## Brand assets

- `assets/brand/logo.svg` — оптимізований знак (fills `#2E4259`, `#424443`)
- `assets/brand/logo-on-dark.svg` — knockout `currentColor` (default white)
- `assets/brand/favicon.svg` — спрощений Φ на navy
- `apple-touch-icon.png` (180×180) — **TODO Task 7/8** (потрібен PNG-пайплайн)

## Палітра (заборонені cream / amber / yellow CTA)

`--navy #2E4259` · `--graphite #424443` · `--bg #F7F8FA` · primary CTA = navy + `--on-navy`.
