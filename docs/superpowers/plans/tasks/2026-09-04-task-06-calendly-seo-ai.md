# Task 6: Calendly, privacy, llms, robots, sitemap — план реализации

> **Для агентных воркеров:** REQUIRED SUB-SKILL: Use `superpowers:subagent-driven-development` (рекомендуется) или `superpowers:executing-plans`. Шаги с чекбоксами `- [ ]`. **Код в этот документ не входит** — только спецификация, полные тексты и критерии приёмки. Реализация: чистый HTML + CSS + минимальный vanilla JS (`calendly-lazy.js`).

**Goal:** Подключить ленивый Calendly, короткие Privacy UK/EN, `llms.txt` на обоих доменах, `robots.txt` с явным Allow для AI-краулеров и Googlebot, полный `sitemap.xml` по URL-карте, с напоминаниями hreflang/canonical — так, чтобы ключевой контент был в view-source, а AI-боты не блокировались.

**Architecture:** Секция Contacts на home уже есть (Tasks 2–3). Task 6 добавляет: (1) UX-обёртку lazy Calendly без скрипта в initial bundle; (2) статические страницы `/privacy/` и `/en/privacy/`; (3) корневые текстовые артефакты `llms.txt`, `robots.txt`, `sitemap.xml` в каждом корне деплоя (`uk-site` → com.ua, `en-site` → agency). Плейсхолдеры `[CALENDLY_URL]` и `[EMAIL_PLACEHOLDER]` не подставлять реальными значениями в этой задаче (финал — Task 8).

**Tech Stack:** HTML5, vanilla JS (IntersectionObserver + click → однократная инъекция Calendly), статические `.txt` / `.xml` в `public/`, без SPA.

**Источник требований:** мастер-план `docs/superpowers/plans/2026-09-04-fidesa-site-plan.md` §3.5, §3.6, §5, §6.1–6.2 (Calendly budget), Task 6; `about.md` §6 (AI-оптимизация).

## Global Constraints (наследуются)

- Бренд: **Fidesa**; никаких упоминаний DNA325.
- com.ua = только UK; agency = `/en/` (+ архитектура под будущие локали).
- B2B CTA: **только** Calendly; нет цен/пакетов/lead-форм.
- Ключевой контент — в чистом HTML (не только JS).
- Third-party: Calendly **после** click или visible; не в hero-бандле.
- Плейсхолдеры: `[CALENDLY_URL]`, `[EMAIL_PLACEHOLDER]` до Task 8.

**Зависимости:** Tasks 1–5 (каркас, home UK/EN, vacancies, blog) должны быть на месте или хотя бы существовать URL-пути из §1.1, иначе sitemap ссылается на ещё не сверстанные страницы — это допустимо, если пути уже зафиксированы в проекте.

**Не трогать:** Tasks 1–5, 7–8; не менять дизайн-токены, копирайт секций home (кроме Contacts/Calendly UX), контент вакансий/блога.

---

## Карта файлов Task 6

| Путь | Роль |
|---|---|
| `src/js/calendly-lazy.js` | Lazy-load: click и/или IntersectionObserver; однократный inject |
| `src/partials/` (Contacts / footer) | Placeholder Calendly + fallback `<a>`, ссылка Privacy |
| Home UK / Home EN (секция Contacts) | Разметка кнопки/контейнера без iframe в initial HTML |
| `public/uk-site/privacy/index.html` (или шаблон → сборка) | Privacy UK |
| `public/en-site/en/privacy/index.html` | Privacy EN |
| `public/uk-site/llms.txt` | AI-файл com.ua (украинский) |
| `public/en-site/llms.txt` | AI-файл agency (английский) |
| `public/uk-site/robots.txt` | Allow AI + Googlebot; Sitemap com.ua |
| `public/en-site/robots.txt` | То же для agency |
| `public/uk-site/sitemap.xml` | URL только com.ua |
| `public/en-site/sitemap.xml` | URL только agency (`/en/…`) |

Если в репозитории уже другая раскладка `src/pages` + SSG — те же артефакты должны оказаться в **корне соответствующего домена** после сборки. Имена URL фиксированы §1.1.

---

## 1. Lazy Calendly UX

### 1.1. Поведение

1. **Initial HTML (Contacts):** нет `<iframe>` Calendly и нет `<script src="…calendly…">` в head/body до взаимодействия.
2. Видимый блок:
   - H2 / supporting из §3.1 / §3.2 (уже должны быть с Tasks 2–3).
   - Контейнер-placeholder (например `data-calendly-root`) с кнопкой открытия.
   - Рядом или под кнопкой — **fallback-ссылка** на `[CALENDLY_URL]` (работает при отключённом JS).
3. **Триггер A — click:** по клику на primary CTA в секции (и опционально на sticky/header CTA, если они ведут в эту же секцию и должны открыть виджет) — один раз инжектить официальный Calendly script + виджет/iframe в контейнер **или** открыть Calendly popup API. Повторные клики не грузят скрипт снова.
4. **Триггер B — visible:** когда секция Contacts входит в viewport (`IntersectionObserver`, `rootMargin` умеренный, напр. ~100–200px), можно **предзагрузить** скрипт **или** сразу смонтировать виджет — выбрать один режим на реализацию и задокументировать в комментарии к `calendly-lazy.js`. Рекомендация мастер-плана: placeholder + кнопка «Відкрити календар» / «Open calendar», inject once; на mobile — не iframe на весь viewport в hero (Contacts ниже fold).
5. **`prefers-reduced-motion`:** не добавлять лишней анимации появления; поведение загрузки то же.
6. **Perf:** скрипт Calendly не входит в critical path; LCP не должен зависеть от Calendly. Исключение PageSpeed из‑за Calendly допустим только *после* клика (см. DoD глобального плана).

### 1.2. Тексты UI (кнопка + fallback)

**UK (`fidesa.com.ua`, секция Contacts):**

| Элемент | Текст |
|---|---|
| H2 (уже в §3.1) | Забронюйте дзвінок |
| Supporting (уже в §3.1) | Короткий зінг із засновницею або командою — щоб зрозуміти роль, терміни й чи можемо бути корисними. |
| Кнопка открытия календаря (lazy) | Відкрити календар |
| Primary CTA (если отдельно от «открыть») | Забронювати дзвінок |
| Fallback-ссылка (JS off / до load) | Відкрити Calendly в новій вкладці |
| `aria-label` fallback (если текст короткий) | Забронювати дзвінок у Calendly |

**EN (`fidesa.agency/en/`, Contact):**

| Элемент | Текст |
|---|---|
| H2 | Book a call |
| Supporting | A short conversation with the founder or team — to clarify the role, timeline, and whether we can help. |
| Lazy open button | Open calendar |
| Primary CTA | Book a call |
| Fallback link | Open Calendly in a new tab |
| `aria-label` fallback | Book a call on Calendly |

### 1.3. Атрибуты ссылки / плейсхолдер

- `href="[CALENDLY_URL]"` на fallback и на любых прямых CTA до подстановки в Task 8.
- `target="_blank"` + `rel="noopener noreferrer"` на внешних ссылках Calendly.
- Не хардкодить чужой demo-URL Calendly в прод-контенте; только `[CALENDLY_URL]`.
- Header/mobile sticky CTA могут быть `href="#contact"` (якорь) **или** тем же `[CALENDLY_URL]` fallback — согласовать с уже сверстанным header: предпочтительно якорь на Contacts + lazy внутри секции, чтобы не грузить third-party с первого экрана.

### 1.4. Чекбоксы — Calendly

- [x] **Шаг 1.** Найти секцию Contacts на UK и EN home; убедиться, что нет раннего Calendly script/iframe в initial HTML.
- [x] **Шаг 2.** Добавить placeholder-контейнер + кнопку «Відкрити календар» / «Open calendar» + fallback-ссылку с текстами §1.2 и `href="[CALENDLY_URL]"`.
- [x] **Шаг 3.** Реализовать `src/js/calendly-lazy.js`: однократная загрузка по click и/или IntersectionObserver; без повторного inject.
- [x] **Шаг 4.** Подключить скрипт только на страницах с Contacts (home), defer; не на privacy/blog list без необходимости.
- [x] **Шаг 5.** Проверка вручную: view-source — нет calendly CDN; после клика/появления секции — виджет или переход по fallback; с отключённым JS — видна текстовая ссылка с понятным UK/EN текстом.
- [x] **Шаг 6.** Mobile 375px: календарь не ломает layout; touch target кнопки ≥ 44×44px.

---

## 2. Privacy — полные тексты (UK + EN)

### 2.1. Требования к страницам

- URL: `https://fidesa.com.ua/privacy/` и `https://fidesa.agency/en/privacy/`.
- Объём: **~1 экран** (коротко, юридически вменяемо, без «простыни» на 20 страниц).
- Meta title/description уникальные; `lang="uk"` / `lang="en"`.
- Canonical на себя; hreflang-пара UK↔EN (см. §6).
- Ссылка из footer: «Privacy» / «Політика конфіденційності» (коротко в UK footer — «Privacy» или «Конфіденційність» — единообразно с §3.1 Footer: **Privacy**).
- Контролёр: **Fidesa** (бренд); юр. название / ЄДРПОУ — плейсхолдер на будущее, в v1 можно указать «Fidesa (рекрутингова агенція)» / «Fidesa (recruiting agency)» без DNA325.
- Email для запросов: `[EMAIL_PLACEHOLDER]`.
- Не публиковать физический адрес, если не требуется отдельно.

### 2.2. Полный текст — українська (`/privacy/`)

**Title:** `Політика конфіденційності — Fidesa`  
**Description:** `Як Fidesa обробляє персональні дані на сайті fidesa.com.ua: Calendly, заявки, аналітика та ваші права.`

**H1:** Політика конфіденційності

**Вступ**

Ця коротка політика пояснює, як Fidesa («ми») обробляє персональні дані відвідувачів і користувачів сайту fidesa.com.ua. Користуючись сайтом або надсилаючи нам дані, ви ознайомлюєтеся з цією інформацією. Повна розширена політика може бути опублікована пізніше за потреби; актуальна версія завжди доступна за цією адресою.

**1. Хто є контролером даних**

Контролер персональних даних: Fidesa — рекрутингова агенція, що спеціалізується на Defence Tech.  
Контакт для запитів щодо персональних даних: `[EMAIL_PLACEHOLDER]`.

**2. Які дані ми можемо обробляти**

Залежно від ваших дій на сайті:

- **технічні дані відвідування** — IP-адреса (або її скорочений/анонімізований вигляд), тип пристрою та браузера, сторінки перегляду, приблизний регіон — якщо підключена аналітика;
- **дані бронювання дзвінка** — ім’я, email, телефон, час зустрічі та повідомлення, які ви вказуєте в Calendly (обробка також на стороні Calendly як окремого сервісу);
- **дані заявки на вакансію** — ім’я, email, телефон, резюме/лінк, текст звернення, якщо ви надсилаєте відгук через зазначений на сайті канал (наприклад, email);
- **комунікація** — зміст листування, якщо ви пишете нам на `[EMAIL_PLACEHOLDER]`.

Ми не просимо спеціальні категорії даних через форми сайту навмисно. Просимо не надсилати зайві чутливі відомості без необхідності.

**3. Мета і правові підстави**

Ми обробляємо дані для:

- відповіді на запити та організації дзвінків з потенційними клієнтами;
- розгляду відгуків кандидатів на опубліковані вакансії;
- забезпечення роботи та безпеки сайту;
- розуміння відвідуваності (аналітика) — у мінімально необхідному обсязі.

Підстави (залежно від випадку): ваша згода; виконання кроків до договору / запиту про послуги; законні інтереси Fidesa у веденні рекрутингової діяльності та підтримці сайту — за умови, що вони не переважають ваших прав; виконання обов’язків за законодавством України про захист персональних даних, де застосовно.

**4. Передача третім сторонам**

Ми можемо залучати перевірених постачальників, без яких сервіс неможливий, зокрема:

- **Calendly** — бронювання зустрічей (їхня політика конфіденційності застосовується до даних у віджеті);
- **хостинг / CDN** — розміщення сайту;
- **аналітика** (якщо увімкнено) — наприклад, privacy-oriented або GA4 із банером згоди.

Ми не продаємо персональні дані. Передача клієнтам-роботодавцям резюме кандидатів відбувається лише в межах рекрутингового процесу та з відповідною метою.

**5. Строк зберігання**

Зберігаємо дані лише стільки, скільки потрібно для мети обробки або вимог закону: звернення та листування — зазвичай до 12–24 місяців після останнього контакту (або довше, якщо є договір/спір); дані аналітики — згідно з налаштуваннями інструменту; дані Calendly — згідно з вашим обліковим записом і політикою Calendly. Далі — видалення або знеособлення.

**6. Ваші права**

Ви можете звернутися на `[EMAIL_PLACEHOLDER]` щоб: дізнатися, які дані ми про вас маємо; виправити неточність; видалити дані (якщо немає обов’язку зберігати); обмежити або заперечити проти обробки; відкликати згоду (якщо обробка на згоді); отримати копію даних у зручному форматі, де це застосовно. Також ви можете подати скаргу до уповноваженого органу з захисту персональних даних в Україні.

**7. Файли cookie та подібні технології**

Сайт може використовувати необхідні технічні cookie для роботи сторінок. Аналітичні / маркетингові cookie — лише після згоди, якщо такий банер підключено. Calendly може встановлювати власні cookie після відкриття віджета — див. політику Calendly.

**8. Діти**

Сайт не призначений для осіб молодше 16 років. Ми свідомо не збираємо їхні дані.

**9. Оновлення**

Ми можемо оновлювати цей текст. Дата останнього оновлення: **4 вересня 2026**. Істотні зміни будуть відображені на цій сторінці.

### 2.3. Полный текст — English (`/en/privacy/`)

**Title:** `Privacy Policy — Fidesa`  
**Description:** `How Fidesa processes personal data on fidesa.agency: Calendly, applications, analytics, and your rights.`

**H1:** Privacy Policy

**Introduction**

This short policy explains how Fidesa (“we”) processes personal data of visitors and users of fidesa.agency (including the `/en/` pages). By using the site or sending us information, you acknowledge this notice. A longer policy may be published later if needed; the current version is always available at this URL.

**1. Data controller**

Controller: Fidesa — a recruiting agency focused on Defence Tech.  
Privacy contact: `[EMAIL_PLACEHOLDER]`.

**2. Data we may process**

Depending on how you use the site:

- **technical visit data** — IP address (or truncated/anonymised form), device/browser type, pages viewed, approximate region — if analytics is enabled;
- **call-booking data** — name, email, phone, meeting time, and messages you enter in Calendly (also processed by Calendly as a separate provider);
- **vacancy application data** — name, email, phone, CV/link, and message if you apply via the channel shown on the site (e.g. email);
- **correspondence** — content of emails you send to `[EMAIL_PLACEHOLDER]`.

We do not intentionally request special-category data through site forms. Please do not send unnecessary sensitive information.

**3. Purposes and legal bases**

We process data to:

- respond to enquiries and arrange calls with prospective clients;
- review candidate applications for published roles;
- operate and secure the website;
- understand traffic (analytics) in a minimal necessary scope.

Legal bases (as applicable): your consent; steps prior to a contract / service request; Fidesa’s legitimate interests in running a recruiting business and maintaining the site, balanced against your rights; compliance with applicable data-protection law.

**4. Sharing with third parties**

We may use processors/providers needed to run the service, including:

- **Calendly** — meeting scheduling (their privacy policy applies to data in the widget);
- **hosting / CDN** — site delivery;
- **analytics** (if enabled) — e.g. a privacy-oriented tool or GA4 with a consent banner.

We do not sell personal data. Candidate CVs are shared with employer clients only as part of the recruiting process and for that purpose.

**5. Retention**

We keep data only as long as needed for the purpose or legal requirements: enquiries and correspondence — typically 12–24 months after last contact (or longer if a contract or dispute requires); analytics — per tool settings; Calendly data — per your Calendly account and Calendly’s policy. Then we delete or anonymise.

**6. Your rights**

You may email `[EMAIL_PLACEHOLDER]` to: access your data; correct inaccuracies; erase data (where we have no duty to retain it); restrict or object to processing; withdraw consent (where processing is consent-based); receive a copy in a portable format where applicable. You may also lodge a complaint with a competent data-protection authority (including, where relevant, in your country of residence or in Ukraine).

**7. Cookies and similar technologies**

We may use strictly necessary cookies for site operation. Analytics/marketing cookies — only after consent if a banner is enabled. Calendly may set its own cookies after the widget loads — see Calendly’s policy.

**8. Children**

The site is not directed at anyone under 16. We do not knowingly collect their data.

**9. Updates**

We may update this text. Last updated: **4 September 2026**. Material changes will appear on this page.

### 2.4. Чекбоксы — Privacy

- [x] **Шаг 7.** Создать страницу Privacy UK с полным текстом §2.2 (без сокращения блоков 1–9).
- [x] **Шаг 8.** Создать страницу Privacy EN с полным текстом §2.3.
- [x] **Шаг 9.** Meta, canonical, hreflang UK↔EN для пары privacy; `lang` корректный.
- [x] **Шаг 10.** Ссылка Privacy в footer обоих доменов.
- [x] **Шаг 11.** Проверка: view-source содержит полный текст политики (не подгрузка только через JS); email = `[EMAIL_PLACEHOLDER]`.

---

## 3. llms.txt — полные файлы

> Формат: plain text в корне домена. com.ua — **украинский** текст; agency — **английский**. Содержание зеркалит §3.6 мастер-плана и позиционирование §0A.6.

### 3.1. Полный файл — `https://fidesa.com.ua/llms.txt`

```
# Fidesa
> Спеціалізована рекрутингова агенція для Defence Tech.

## Хто ми
- Fidesa — рекрутингова агенція, що працює виключно зі сферою Defence Tech.
- Фокус: виробники озброєння та БПЛА, engineering- і software-команди в оборонній сфері.
- Ми не ведемо генералістський IT-рекрутинг і не змішуємо Defence Tech з іншими індустріями.
- Бренд незалежний: на сайті немає заяв про афіліації поза брендом Fidesa.

## Що ми робимо
- Повний цикл підбору для компаній-замовників: бриф, пошук, скринінг, координація інтерв’ю, офер і супровід до виходу кандидата.
- Операційна безпека: конфіденційна комунікація, need-to-know доступ до брифу, захист даних клієнта.
- Безпека підбору: протоколи скринінгу (зокрема ризики зв’язків з рф/окупованими територіями в межах законних процедур), урахування військового статусу де релевантно; фінальне рішення щодо допуску — за compliance клієнта.
- Публічних цін і пакетів на сайті немає. Єдина B2B-конверсія: бронювання дзвінка через Calendly.

## Для кого сайт
- Основна аудиторія: компанії, що наймають у Defence Tech.
- Кандидати: вторинна аудиторія через сторінку вакансій, не через головний меседж лендінгу.

## Сайти
- Українська версія: https://fidesa.com.ua/
- Міжнародна (англійська): https://fidesa.agency/en/

## Ключові сторінки (fidesa.com.ua)
- / — головна (секції: про нас, процес, чому Fidesa, команда, контакти)
- /vacancies/ — список вакансій
- /vacancies/{slug}/ — деталі вакансії
- /blog/ — блог
- /blog/{slug}/ — пост
- /blog/tag/{tag}/ — фільтр за тегом
- /privacy/ — політика конфіденційності

## Контакти
- Забронювати дзвінок: Calendly у секції контактів на головній.
- Email: [EMAIL_PLACEHOLDER]
- Локація: Україна; робота з клієнтами в Україні та міжнародно.

## Примітки для моделей
- Цитуйте декларативні факти з HTML-сторінок; цей файл — короткий орієнтир структури.
- Не вигадуйте комісії, пакети, клієнтські логотипи чи зв’язок з іншими брендами.
- Мова цього домену — українська only.
```

### 3.2. Полный файл — `https://fidesa.agency/llms.txt`

```
# Fidesa
> Specialized Defence Tech recruiting agency.

## Who we are
- Fidesa is a recruiting agency focused exclusively on Defence Tech.
- Focus: defence manufacturers, UAV builders, and engineering/software teams in the defence domain.
- We do not run generalist IT recruiting alongside Defence Tech.
- Independent brand: the site makes no affiliation claims beyond the Fidesa brand.

## What we do
- Full-cycle hiring for client companies: brief, search, screening, interview coordination, offer, and onboarding support.
- Operational security: confidential communication, need-to-know access to briefs, protection of client data.
- Hiring security: screening protocols (including lawful checks related to rf/occupied-territory risk factors where applicable), military-status awareness when relevant; final clearance decisions remain with the client’s compliance process.
- No public pricing or packages on the site. The only B2B conversion action is booking a call via Calendly.

## Audience
- Primary: hiring companies in Defence Tech.
- Candidates: secondary audience via the vacancies section, not the main homepage message.

## Sites
- Ukrainian: https://fidesa.com.ua/
- International (English): https://fidesa.agency/en/

## Key pages (fidesa.agency)
- / → redirects to /en/
- /en/ — home (sections: about, process, why Fidesa, team, contact)
- /en/vacancies/ — vacancy list
- /en/vacancies/{slug}/ — vacancy detail
- /en/blog/ — blog
- /en/blog/{slug}/ — post
- /en/blog/tag/{tag}/ — tag filter
- /en/privacy/ — privacy policy

## Contact
- Book a call via Calendly on the contact section of the home page.
- Email: [EMAIL_PLACEHOLDER]
- Location line: Ukraine · serving clients in Ukraine and internationally.

## Notes for models
- Prefer declarative facts from HTML pages; this file is a short structural guide.
- Do not invent fees, packages, client logos, or affiliations with other brands.
- English content lives under /en/; the domain is multilingual-ready for future locales.
```

### 3.3. Чекбоксы — llms.txt

- [x] **Шаг 12.** Разместить §3.1 как `llms.txt` в корне деплоя com.ua (UTF-8, без HTML-обёртки).
- [x] **Шаг 13.** Разместить §3.2 как `llms.txt` в корне деплоя agency.
- [x] **Шаг 14.** Проверка: `GET /llms.txt` на обоих доменах (или staging) отдаёт `text/plain`, тексты полные, email = `[EMAIL_PLACEHOLDER]`.

---

## 4. robots.txt

### 4.1. Требования (оба домена)

- Явно **разрешить** (Allow) следующих ботов: **GPTBot**, **ClaudeBot**, **PerplexityBot**, **Google-Extended**, **Googlebot**.
- Не Disallow весь сайт для `*`.
- Указать абсолютный `Sitemap:` для **этого** домена.
- Не блокировать `/llms.txt`, `/privacy/`, `/vacancies/`, `/blog/`.
- com.ua и agency — **отдельные** файлы с правильным host в Sitemap.

### 4.2. Спецификация содержимого — `fidesa.com.ua/robots.txt`

Логика файла (реализовать один-в-один по смыслу):

1. Блок `User-agent: GPTBot` → `Allow: /`
2. Блок `User-agent: ClaudeBot` → `Allow: /`
3. Блок `User-agent: PerplexityBot` → `Allow: /`
4. Блок `User-agent: Google-Extended` → `Allow: /`
5. Блок `User-agent: Googlebot` → `Allow: /`
6. Блок `User-agent: *` → `Allow: /`
7. Строка: `Sitemap: https://fidesa.com.ua/sitemap.xml`

Пустые строки между блоками — по желанию; комментарии `#` допустимы.

### 4.3. Спецификация содержимого — `fidesa.agency/robots.txt`

Те же User-agent / Allow блоки, что в §4.2.  
Sitemap: `Sitemap: https://fidesa.agency/sitemap.xml`

### 4.4. Чекбоксы — robots

- [x] **Шаг 15.** Добавить `robots.txt` для uk-site по §4.2.
- [x] **Шаг 16.** Добавить `robots.txt` для en-site по §4.3.
- [x] **Шаг 17.** Проверка: в файле нет `Disallow: /` для перечисленных AI-ботов; Sitemap URL абсолютный и совпадает с доменом.

---

## 5. sitemap.xml

### 5.1. Правила

- Отдельный sitemap на каждый домен; **не** смешивать host’ы в одном файле.
- Включать индексируемые HTML-страницы; `llms.txt` / `robots.txt` в sitemap обычно **не** включают.
- Корень agency `/` — редирект на `/en/`: в sitemap agency указывать **`/en/`**, не обязательно `/`.
- `lastmod` — дата деплоя или дата контента (ISO `YYYY-MM-DD`); `changefreq`/`priority` — опционально, можно опустить для простоты.
- Tag-страницы блога — включить для пяти стартовых тегов из §3.4.
- Три стартовые вакансии и три поста — из мастер-плана §3.3–3.4.

### 5.2. Полный список URL — `https://fidesa.com.ua/sitemap.xml`

| URL |
|---|
| `https://fidesa.com.ua/` |
| `https://fidesa.com.ua/privacy/` |
| `https://fidesa.com.ua/vacancies/` |
| `https://fidesa.com.ua/vacancies/embedded-software-engineer-uav/` |
| `https://fidesa.com.ua/vacancies/fullstack-defence-saas/` |
| `https://fidesa.com.ua/vacancies/rf-electronics-engineer/` |
| `https://fidesa.com.ua/blog/` |
| `https://fidesa.com.ua/blog/why-defence-tech-needs-specialized-recruiters/` |
| `https://fidesa.com.ua/blog/screening-without-theatre/` |
| `https://fidesa.com.ua/blog/briefing-a-defence-role/` |
| `https://fidesa.com.ua/blog/tag/defence-tech/` |
| `https://fidesa.com.ua/blog/tag/recruiting/` |
| `https://fidesa.com.ua/blog/tag/security/` |
| `https://fidesa.com.ua/blog/tag/engineering-hiring/` |
| `https://fidesa.com.ua/blog/tag/ukraine/` |

**Итого com.ua: 15 URL.**

### 5.3. Полный список URL — `https://fidesa.agency/sitemap.xml`

| URL |
|---|
| `https://fidesa.agency/en/` |
| `https://fidesa.agency/en/privacy/` |
| `https://fidesa.agency/en/vacancies/` |
| `https://fidesa.agency/en/vacancies/embedded-software-engineer-uav/` |
| `https://fidesa.agency/en/vacancies/fullstack-defence-saas/` |
| `https://fidesa.agency/en/vacancies/rf-electronics-engineer/` |
| `https://fidesa.agency/en/blog/` |
| `https://fidesa.agency/en/blog/why-defence-tech-needs-specialized-recruiters/` |
| `https://fidesa.agency/en/blog/screening-without-theatre/` |
| `https://fidesa.agency/en/blog/briefing-a-defence-role/` |
| `https://fidesa.agency/en/blog/tag/defence-tech/` |
| `https://fidesa.agency/en/blog/tag/recruiting/` |
| `https://fidesa.agency/en/blog/tag/security/` |
| `https://fidesa.agency/en/blog/tag/engineering-hiring/` |
| `https://fidesa.agency/en/blog/tag/ukraine/` |

**Итого agency: 15 URL** (все под `/en/`).

### 5.4. Чекбоксы — sitemap

- [x] **Шаг 18.** Собрать `sitemap.xml` com.ua со всеми URL из §5.2 (валидный XML urlset).
- [x] **Шаг 19.** Собрать `sitemap.xml` agency со всеми URL из §5.3.
- [x] **Шаг 20.** Сверить: ни один URL com.ua не попал в agency sitemap и наоборот; trailing slash согласован с реальными страницами проекта.
- [x] **Шаг 21.** Убедиться, что `robots.txt` ссылается на эти файлы.

---

## 6. Напоминания: hreflang и canonical

> Не отдельная «фича» Task 6, но **обязательный gate** при добавлении Privacy и при проверке SEO-артефактов. Логика уже в Task 3 / §5.1 мастер-плана — здесь не ломать и дополнить для новых URL.

### 6.1. Canonical

- Каждая страница: один `<link rel="canonical" href="…">` на **свой** абсолютный URL.
- Privacy UK → `https://fidesa.com.ua/privacy/`
- Privacy EN → `https://fidesa.agency/en/privacy/`
- На agency корень `/` (если отдаёт HTML) — canonical на `https://fidesa.agency/en/` **или** только HTTP redirect без индексируемой копии (предпочтительно redirect 302/301 как в §0).

### 6.2. hreflang (пары)

Для каждой логической страницы (home, privacy, vacancy slug, blog slug, blog tag):

| hreflang | href |
|---|---|
| `uk` | `https://fidesa.com.ua{path}` |
| `en` | `https://fidesa.agency/en{path}` |
| `x-default` | `https://fidesa.agency/en/` (международный дефолт; для внутренних EN-страниц допустимо `x-default` → соответствующий EN URL **или** стабильно на `/en/` — **выбрать одно правило проекта и не смешивать**; рекомендация мастер-плана: `x-default` → `https://fidesa.agency/en/`) |

Примеры path: `/`, `/privacy/`, `/vacancies/embedded-software-engineer-uav/`, `/blog/screening-without-theatre/`, `/blog/tag/security/`.

На com.ua path **без** `/en/`; на agency path **с** `/en`.

### 6.3. Чекбоксы — hreflang/canonical

- [x] **Шаг 22.** На Privacy UK/EN выставить canonical + hreflang uk/en/x-default по §6.1–6.2.
- [x] **Шаг 23.** Smoke: выборочно home + одна vacancy + один post — пары hreflang не битые (URL существуют в sitemap).
- [x] **Шаг 24.** Не добавлять hreflang на `llms.txt` / `robots.txt` / `sitemap.xml` (это не HTML-документы).

---

## 7. Definition of Done (Task 6)

### 7.1. Чеклист приёмки

- [x] **DoD-1. Calendly lazy:** в initial view-source home нет Calendly iframe/script CDN; есть кнопка + fallback-тексты UK и EN; `href` содержит `[CALENDLY_URL]`; после click и/или visible виджет или скрипт загружается один раз.
- [x] **DoD-2. Privacy:** обе страницы с **полными** текстами §2.2 и §2.3 в HTML; видны в view-source; `[EMAIL_PLACEHOLDER]` на месте; ссылка в footer.
- [x] **DoD-3. llms.txt:** оба файла §3.1 и §3.2 отдаются из корня доменов; язык соответствует домену.
- [x] **DoD-4. robots:** GPTBot, ClaudeBot, PerplexityBot, Google-Extended, Googlebot — явно Allow; Sitemap абсолютный; AI bots **не** заблокированы.
- [x] **DoD-5. sitemap:** 15+15 URL по §5.2–5.3; host’ы не смешаны.
- [x] **DoD-6. hreflang/canonical:** privacy-пара корректна; напоминания §6 соблюдены.
- [x] **DoD-7. Контент для AI/SEO:** ключевые тексты (home секции уже из Tasks 2–3, privacy, llms) доступны **без JS**; фильтры вакансий не удаляют detail URL из индекса.
- [x] **DoD-8. Бренд:** нет DNA325; нет публичных цен в новых текстах.
- [x] **DoD-9. Плейсхолдеры:** не «зашиты» фейковые email/Calendly вместо `[EMAIL_PLACEHOLDER]` / `[CALENDLY_URL]` (подстановка — Task 8).

### 7.2. Как проверять (команды / вручную)

1. Открыть home → View Source → поиск `calendly` — до взаимодействия пусто (кроме разве текстового слова в copy); есть fallback `<a href="[CALENDLY_URL]"`.
2. Клик «Відкрити календар» / «Open calendar» → сеть: запрос к Calendly; повторный клик без второго download script (или idempotent).
3. `curl -sI` / браузер: `/privacy/`, `/en/privacy/`, `/llms.txt`, `/robots.txt`, `/sitemap.xml` на обоих staging-доменах → 200.
4. Прочитать `robots.txt`: все пять ботов + Googlebot Allow; Sitemap совпадает.
5. Прочитать `sitemap.xml`: список = таблицы §5; валидный XML.
6. Disable JS → Contacts: видна понятная ссылка UK/EN; Privacy и llms читаются полностью.

### 7.3. Вне scope Task 6

- Подстановка реальных Calendly/email (Task 8).
- Lighthouse ≥95 / чистка third-parties сверх Calendly lazy (Task 7).
- Consent-banner аналитики (если ещё не сделан) — не блокировать Task 6; при появлении аналитики — упомянуть в Privacy уже заложено.
- Юр. название / ЄДРПОУ — опционально позже; не выдумывать.

---

## 8. Порядок шагов (сводка чекбоксов)

| # | Тема | Шаги |
|---|---|---|
| A | Lazy Calendly | 1–6 |
| B | Privacy UK/EN | 7–11 |
| C | llms.txt | 12–14 |
| D | robots.txt | 15–17 |
| E | sitemap.xml | 18–21 |
| F | hreflang/canonical | 22–24 |
| G | DoD | 7.1 все пункты |

Рекомендуемый порядок выполнения: **A → B → C → D → E → F → G**.

---

## 9. Self-review против мастер-плана

| Требование | Где в Task 6 |
|---|---|
| §3.5 Privacy коротко, 1 экран, контролер/данные/сроки/контакт | §2 полные тексты |
| §3.6 llms.txt блоки What we do / Sites / Key pages / Contact / Notes | §3.1–3.2 расширенные полные файлы |
| §5.3 robots Allow AI + Googlebot + Sitemap | §4 |
| §5.1 hreflang/canonical | §6 |
| §1.1 URL privacy, llms, robots, sitemap | карта файлов + §5 |
| Task 6 Done: контент в view-source; AI bots allowed | §7 DoD |
| Calendly lazy click/visible; fallback; perf | §1 |
| about.md §6 GPTBot, ClaudeBot, PerplexityBot, Google-Extended | §4 (плюс Googlebot из мастер-плана) |
| Плейсхолдеры §12 | везде `[CALENDLY_URL]`, `[EMAIL_PLACEHOLDER]` |

Пробелов по Task 6 относительно §3.5, §3.6, §5 и формулировки Task 6 в §9 — нет. Другие tasks не затронуты.

---

*План Task 6. Язык документа: русский. Копирайт Privacy/llms — для реализации as-is с последующей юр. вычиткой заказчиком.*
