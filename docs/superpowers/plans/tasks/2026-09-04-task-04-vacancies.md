# Task 4: Вакансії — план реалізації

> **Для агентних воркерів:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) або superpowers:executing-plans. Кроки з чекбоксами (`- [ ]`). **Код у цей документ не входить** — лише специфікація контенту, UX і DoD. Реалізація за стеком мастер-плану: статичний HTML + CSS + vanilla JS (`filters.js`).

**Goal:** Окремий каталог вакансій Fidesa (list + detail) з фільтрами за §0A.5 / §4.3, трьома стартовими ролями UK+EN, JobPosting schema і apply-CTA — без salary-filter, логотипів клієнтів і чату.

**Architecture:** Контент вакансій у `content/uk/vacancies/*.md` і дзеркалі `content/en/vacancies/*.md` (frontmatter + body). List-сторінка рендерить усі картки в HTML; клієнтський `filters.js` ховає/показує за `data-*` і синхронізує query `?direction=&location=&format=`. Detail — окремі URL з BreadcrumbList + JobPosting JSON-LD. На home лістинг **не** дублюється (лише nav/footer).

**Tech Stack:** Markdown/frontmatter → статичний HTML; `src/js/filters.js`; partials header/footer/schema; без ATS, без Chatwoot, без React.

**Джерела:** мастер-план `docs/superpowers/plans/2026-09-04-fidesa-site-plan.md` (§0A.5, §1.1, §3.3, §4.3, §5.2); ТЗ `about.md` (§3.2, §6).

## Global Constraints (успадковані)

- Бренд **Fidesa** — лише Defence Tech; без DNA325.
- Apply на вакансіях — окремий шлях (не Calendly B2B).
- Усі ключові тексти в чистому HTML; фільтр може ховати картки, але DOM/URL деталей індексуються.
- UI **не** копіювати app.bazait.com — лише функціональна логіка §0A.5.
- Картки дозволені лише як інтерактивний контейнер (вакансія = клікабельний блок).
- Touch targets ≥ 44×44px; labels на фільтрах обов’язкові.

---

## 1. URL map (UK / EN)

### 1.1. fidesa.com.ua (українська)

| URL | Призначення |
|---|---|
| `/vacancies/` | Список вакансій + фільтри |
| `/vacancies/embedded-software-engineer-uav/` | Деталь: Embedded Software Engineer (UAV) |
| `/vacancies/fullstack-defence-saas/` | Деталь: Full-Stack Engineer (Defence SaaS) |
| `/vacancies/rf-electronics-engineer/` | Деталь: RF / Electronics Engineer |

### 1.2. fidesa.agency (англійська, підпапка `/en/`)

| URL | Призначення |
|---|---|
| `/en/vacancies/` | Vacancies list + filters |
| `/en/vacancies/embedded-software-engineer-uav/` | Detail: Embedded Software Engineer (UAV) |
| `/en/vacancies/fullstack-defence-saas/` | Detail: Full-Stack Engineer (Defence SaaS) |
| `/en/vacancies/rf-electronics-engineer/` | Detail: RF / Electronics Engineer |

### 1.3. Парність і SEO URL

- **Один slug на обидві мови** (латиниця) — щоб path mapping UA↔EN не ламався: `/vacancies/{slug}/` ↔ `/en/vacancies/{slug}/`.
- hreflang на list і кожній detail: `uk` → com.ua, `en` → agency/en, `x-default` → agency/en/.
- Canonical — на канонічний URL своєї мови/домену.
- Query фільтрів (`?direction=…`) **не** створює окремі індексовані URL: canonical list без query; `robots`/sitemap містять лише чисті list + 3 detail.

### 1.4. Файли контенту (цільові)

| Мова | Шлях |
|---|---|
| UK | `content/uk/vacancies/embedded-software-engineer-uav.md` |
| UK | `content/uk/vacancies/fullstack-defence-saas.md` |
| UK | `content/uk/vacancies/rf-electronics-engineer.md` |
| EN | `content/en/vacancies/embedded-software-engineer-uav.md` |
| EN | `content/en/vacancies/fullstack-defence-saas.md` |
| EN | `content/en/vacancies/rf-electronics-engineer.md` |

Шаблони сторінок (орієнтир дерева мастер-плану): list + detail у `src/pages/`; стилі карток/фільтрів у `src/styles/`; логіка — `src/js/filters.js`.

---

## 2. List page — тексти UI (UK + EN)

### 2.1. Мета сторінки

| Поле | UK | EN |
|---|---|---|
| `<title>` | Вакансії — Fidesa | Vacancies — Fidesa |
| `meta description` | Відкриті ролі в компаніях Defence Tech. Fidesa супроводжує підбір персоналу для виробників і engineering-команд оборонної сфери. | Open roles across Defence Tech companies. Fidesa supports hiring for defence manufacturers and engineering teams. |

### 2.2. Заголовок і intro

| Елемент | UK | EN |
|---|---|---|
| H1 | Вакансії | Vacancies |
| Intro (1–2 речення під H1) | Відкриті ролі в компаніях Defence Tech. Fidesa супроводжує підбір; умови співпраці з роботодавцем обговорюються окремо. | Open roles across Defence Tech companies. Fidesa supports the hiring process; employment terms with the employer are agreed separately. |

### 2.3. Фільтри — labels і службові рядки

| Елемент | UK | EN |
|---|---|---|
| Група / легенда 1 | Напрямок | Direction |
| Група / легенда 2 | Локація | Location |
| Група / легенда 3 | Формат | Format |
| Кнопка скидання | Скинути | Reset |
| Mobile: відкрити панель | Фільтри | Filters |
| Mobile: застосувати / закрити панель | Показати результати | Show results |
| Лічильник (шаблон) | `{N} вакансій` / `1 вакансія` / `2–4 вакансії` (узгодити plural rules UK) | `{N} vacancies` / `1 vacancy` |
| Empty state (після фільтра) | За цими фільтрами вакансій немає. | No vacancies match these filters. |
| Empty state CTA під текстом | Скинути фільтри | Reset filters |
| Картка: лінк | Детальніше | View details |
| Aria live для лічильника | регіон з `aria-live="polite"` | same |

### 2.4. Опції фільтрів (values — стабільні латинські ключі; labels — локалізовані)

**Direction (`direction`)**

| value | Label UK | Label EN |
|---|---|---|
| `embedded` | Embedded / Firmware | Embedded / Firmware |
| `software` | Software | Software |
| `electronics` | Electronics / RF | Electronics / RF |
| *(порожньо / all)* | Усі напрямки | All directions |

**Location (`location`)**

| value | Label UK | Label EN |
|---|---|---|
| `kyiv` | Київ | Kyiv |
| `ukraine` | Україна | Ukraine |
| `remote-ua` | Remote UA | Remote UA |
| `remote-eu-ua` | Remote EU/UA | Remote EU/UA |
| *(порожньо / all)* | Усі локації | All locations |

**Format (`format`)** — відповідає Type of Work у референсі

| value | Label UK | Label EN |
|---|---|---|
| `full-time-remote` | Full-time · Remote | Full-time · Remote |
| `full-time-hybrid` | Full-time · Hybrid | Full-time · Hybrid |
| `full-time-office` | Full-time · Office | Full-time · Office |
| *(порожньо / all)* | Усі формати | All formats |

Примітка реалізації: у картці відображати **людиночитний** рядок формату (напр. `Full-time · Remote UA`), а для фільтра — нормалізований `format` + окремі `location` / `direction` з frontmatter. Одна вакансія може мати кілька location-tagів у data-атрибутах, якщо роль покриває кілька зон (напр. Remote EU/UA + Remote UA) — для стартових трьох достатньо **одного** primary location value на роль (див. §5).

---

## 3. Спека фільтрів (§0A.5 / §4.3)

### 3.1. Що реалізуємо

| Елемент | Статус | Поведінка |
|---|---|---|
| Список карток + окремі detail URL | Так | Кожна вакансія — окремий HTML |
| Фільтр `direction` | Так | Exact match по frontmatter / `data-direction` |
| Фільтр `location` | Так | Exact match по `data-location` |
| Фільтр `format` | Так | Exact match по `data-format` |
| Лічильник «N вакансій» | Так | Оновлюється без reload |
| URL query sync | Так | `?direction=&location=&format=` для шарингу; порожні параметри прибирати |
| Desktop toolbar | Так | Inline chips або native `<select>` / radio-chip groups над списком |
| Mobile filters | Так | Один panel/sheet «Фільтри» **або** horizontal snap-chips на всю ширину; не desktop sidebar |
| Client-side filter | Так | Без перезавантаження сторінки |
| Pagination | Ні (до 20) | При >20 пізніше — «Показати ще»; на старті 3 картки |
| Усі картки в DOM | Так | Filter лише hide/show; для AI/SEO текст list+detail у HTML |

### 3.2. Що свідомо НЕ робимо (анти-скоуп)

| Елемент BazaIT / зайве | Рішення Fidesa |
|---|---|
| Salary filter | **Ні** |
| Salary як обов’язкове поле картки | **Ні** (опційно пізніше в detail, не в MVP) |
| Companies tab | **Ні** |
| Логотипи / назви клієнтів-замовників | **Ні** (конфіденційність; hiring org у schema — Fidesa або «confidential client» через агенцію) |
| Live-chat / Chatwoot | **Ні** |
| Sign up / Login | **Ні** |
| Position filter (окремий від direction) | **Ні** на старті |
| «Open All Filters» як окремий складний drawer з salary | **Ні**; mobile — один простий panel трьох груп |

### 3.3. Логіка комбінування

- Фільтри **AND** між групами: direction ∩ location ∩ format.
- Усередині групи — single-select (одне значення або «усі»).
- «Скинути» очищає всі три + query + показує всі картки + оновлює лічильник.
- Якщо після фільтра 0 карток — показати empty state (§2.3), список приховати або залишити порожній контейнер з повідомленням.

### 3.4. Дані для фільтра (frontmatter кожної вакансії)

Обов’язкові ключі:

- `slug`
- `title`
- `direction` — один з values §2.4
- `location` — один з values §2.4
- `format` — один з values §2.4
- `locationLabel` / відображувана локація (вільна фраза UK або EN відповідно до файлу)
- `formatLabel` — відображуваний формат зайнятості
- `directionLabel` — відображуваний напрямок
- `short` — ≤160 символів
- `datePosted` — ISO `YYYY-MM-DD`
- `employmentType` — для JobPosting (напр. `FULL_TIME`)

---

## 4. Картка вакансії та mobile stack

### 4.1. Поля картки (desktop і mobile — ті самі дані)

Порядок контенту:

1. **title** (посилання на detail або вся картка клікабельна + окремий видимий лінк)
2. **meta row:** `locationLabel` · `formatLabel` · `directionLabel`
3. **datePosted** — дрібний meta (опційно, не конкурує з title)
4. **short** — ≤160 символів
5. **CTA лінк:** «Детальніше» / «View details»

**Заборонено в картці:** лого клієнта, назва компанії-замовника, salary, Apply-кнопка (Apply лише на detail), chat widget.

### 4.2. Desktop layout

- Список вертикальний, повітря між рядками; тонка 1px лінія (`--line`) або легкий surface — без багатошарових тіней «як BazaIT».
- Meta в один рядок з розділювачами; short під ним; лінк справа або під excerpt — головне: не горизонтальна «широка картка з Apply справа» як у референсі.

### 4.3. Mobile stack (обов’язково)

На вузьких екранах картка **стеком**, не горизонтальним split:

```
[ title                    ]
[ location · format · dir  ]
[ datePosted (optional)    ]
[ short excerpt            ]
[ Детальніше  (full width) ]
```

- CTA full-width, min-height 44px.
- Фільтри: horizontal scroll-snap chips **або** bottom/full sheet «Фільтри» з трьома групами + «Показати результати» + «Скинути».
- Не використовувати multi-select dropdown, що виходить за екран.

### 4.4. a11y картки

- Якщо клікабельна вся картка — один фокусний контрол; уникати вкладених інтерактивних елементів без потреби.
- Контраст meta (`--ink-muted` на `--surface`/`--bg`) — WCAG AA.
- `prefers-reduced-motion`: без зайвих анімацій filter toggle.

---

## 5. Три стартові вакансії — повні тексти UK + EN

> Плейсхолдери для запуску (вигадані ролі в екосистемі Defence Tech). Пізніше замінити реальними. Salary не вказувати. Ім’я клієнта не розкривати.

---

### 5.1. Vacancy A — Embedded Software Engineer (UAV)

| Поле | Значення |
|---|---|
| `slug` | `embedded-software-engineer-uav` |
| `direction` | `embedded` |
| `location` | `kyiv` |
| `format` | `full-time-remote` |
| `employmentType` | `FULL_TIME` |
| `datePosted` | `2026-09-01` |

#### UK

**title:** Embedded Software Engineer (UAV)

**locationLabel:** Київ / Remote UA  
**formatLabel:** Full-time · Remote UA  
**directionLabel:** Embedded / Firmware  

**short:** Розробка firmware для бортових систем БПЛА: C/C++, RTOS, надійність у полі. Супровід підбору — Fidesa.

**full description (~UK):**

Ми шукаємо Embedded Software Engineer для продуктової команди в сегменті unmanned aerial systems. Роль зосереджена на бортовому ПЗ: від низькорівневої ініціалізації периферії до стабільного польотного контуру та телеметрії. Ви працюватимете з інженерами електроніки, системними інтеграторами та QA, які перевіряють поведінку firmware на стенді й у польових сценаріях.

Обов’язки включають проєктування та реалізацію модулів на C/C++ під RTOS (або еквівалентне real-time середовище), роботу з шинами та протоколами обміну з датчиками й актуаторами, оптимізацію затримок і споживання, а також підготовку збірок для різних ревізій плати. Очікується участь у code review, веденні технічної документації модулів і розборі інцидентів після стендових/польових тестів — без театральності, з фокусом на відтворюваність і безпеку змін.

Вимоги: впевнений C/C++ у embedded-контексті; досвід RTOS або жорсткого real-time на MCU/SoC; розуміння memory map, interrupt handling, DMA; навички дебагу на залізі (JTAG/SWD, логічний аналізатор — плюс). Буде перевагою досвід з автопілотами/польотними стеками, CAN/UAVCAN або подібними шинами, CI для firmware та навички читання схем. Англійська — достатня для технічної документації та синхронів з міжнародними підрядниками.

Формат: full-time, базування Київ з можливістю Remote UA за домовленістю команди. Клієнт — компанія Defence Tech; назва на етапі відгуку не публікується. Fidesa супроводжує комунікацію, скринінг відповідності ролі та організацію наступних етапів з роботодавцем. Умови працевлаштування, компенсація та допуск до матеріалів проєкту обговорюються безпосередньо зі стороною найму після успішного первинного скринінгу.

Якщо вам близька інженерна дисципліна бортових систем і ви готові працювати в контурі, де якість коду впливає на безпеку місії, надішліть резюме через кнопку відгуку на цій сторінці.

**Apply CTA UK:** Відгукнутися  
**Supporting under CTA UK:** Надішліть резюме — ми зв’яжемося щодо наступних кроків.

#### EN

**title:** Embedded Software Engineer (UAV)

**locationLabel:** Kyiv / Remote UA  
**formatLabel:** Full-time · Remote UA  
**directionLabel:** Embedded / Firmware  

**short:** Onboard UAV firmware: C/C++, RTOS, field-grade reliability. Hiring process supported by Fidesa.

**full description (~EN):**

We are hiring an Embedded Software Engineer for a product team building unmanned aerial systems. The role focuses on onboard software — from low-level bring-up of peripherals to a stable flight-related control path and telemetry. You will collaborate with electronics engineers, system integrators, and QA who validate firmware behaviour on the bench and in field scenarios.

Responsibilities include designing and implementing C/C++ modules on an RTOS (or equivalent real-time environment), working with buses and protocols that connect sensors and actuators, optimising latency and power, and preparing builds across board revisions. You will take part in code reviews, keep module documentation current, and help triage issues found in bench or field tests — with an emphasis on reproducibility and safe change management rather than ceremony.

Requirements: strong C/C++ in an embedded context; RTOS or hard real-time experience on MCU/SoC platforms; solid grasp of memory maps, interrupts, and DMA; hands-on hardware debugging (JTAG/SWD; logic analyser is a plus). Experience with autopilot or flight stacks, CAN/UAVCAN-like buses, firmware CI, and the ability to read schematics are advantageous. English should be sufficient for technical documentation and syncs with international partners.

Format: full-time, Kyiv-based with Remote UA possible by team agreement. The employer is a Defence Tech company; the client name is not published at the application stage. Fidesa runs outreach, role-fit screening, and coordinates next steps with the hiring side. Employment terms, compensation, and access to project materials are discussed directly with the employer after a successful initial screen.

If you care about disciplined onboard engineering — where software quality affects mission safety — apply via the button on this page and send your CV.

**Apply CTA EN:** Apply  
**Supporting under CTA EN:** Send your CV — we will follow up on next steps.

---

### 5.2. Vacancy B — Full-Stack Engineer (Defence SaaS)

| Поле | Значення |
|---|---|
| `slug` | `fullstack-defence-saas` |
| `direction` | `software` |
| `location` | `remote-eu-ua` |
| `format` | `full-time-remote` |
| `employmentType` | `FULL_TIME` |
| `datePosted` | `2026-09-01` |

#### UK

**title:** Full-Stack Engineer (Defence SaaS)

**locationLabel:** Remote EU/UA  
**formatLabel:** Full-time · Remote  
**directionLabel:** Software  

**short:** Платформа logistics/C2 для Defence Tech: TypeScript, Node, відповідальний full-stack. Супровід — Fidesa.

**full description (~UK):**

Шукаємо Full-Stack Engineer для команди, що розвиває SaaS-платформу в контурі defence logistics та command-and-control (C2) підтримки. Продукт допомагає операційним і інженерним користувачам планувати ресурси, відстежувати статуси та працювати з даними в умовах жорстких вимог до надійності, аудиту дій і розмежування доступу. Ви працюватимете з продуктовым менеджером, дизайном і бекенд/фронтенд колегами в remote-first режимі EU/UA.

Обов’язки: розробка клієнтських інтерфейсів і серверних API на TypeScript; проєктування доменних модулів; інтеграції з внутрішніми сервісами; покриття критичних сценаріїв тестами; участь у проєктуванні схеми даних і подій. Важливо вміти розрізняти «швидкий прототип» і production-контур з логірованием, обробкою помилок і зрозумілими контрактами API. Очікується уважність до UX складних таблиць/станів і до того, як права доступу відображаються в UI.

Вимоги: впевнений TypeScript; досвід Node (або еквівалент) і сучасного фронтенд-стеку (React/Vue/Svelte — конкретний стек уточнюється на скринінгу); розуміння REST/JSON API, автентифікації/сесій або token-based доступу; досвід роботи з PostgreSQL або аналогом; навички code review і акуратного git-процесу. Переваги: досвід B2B SaaS, черги/фонові воркери, OpenAPI, спостережуваність (metrics/logs), розуміння вимог до audit trail у регульованих середовищах. Англійська — робоча для async-комунікації в EU-розподіленій команді.

Формат: full-time, Remote EU/UA. Роботодавець — Defence Tech продуктова компанія; бренд клієнта на публічній сторінці не розкривається. Fidesa веде первинний контакт, перевіряє відповідність стеку й досвіду та передає сильні профілі замовнику. Деталі контракту, рівень компенсації та security onboarding — на стороні роботодавця після успішних інтерв’ю.

Якщо вам цікаві складні operational UI і бекенд, де помилка коштує дорого, відгукніться та надішліть резюме з посиланнями на релевантний досвід (без секретних деталей проєктів).

**Apply CTA UK:** Відгукнутися  
**Supporting under CTA UK:** Надішліть резюме — ми зв’яжемося щодо наступних кроків.

#### EN

**title:** Full-Stack Engineer (Defence SaaS)

**locationLabel:** Remote EU/UA  
**formatLabel:** Full-time · Remote  
**directionLabel:** Software  

**short:** Defence logistics/C2 SaaS: TypeScript, Node, accountable full-stack delivery. Hiring supported by Fidesa.

**full description (~EN):**

We are looking for a Full-Stack Engineer to join a team building a SaaS platform in the defence logistics and command-and-control (C2) support space. The product helps operational and engineering users plan resources, track statuses, and work with data under strict expectations for reliability, action auditability, and access control. You will collaborate with a product manager, design, and fellow engineers in a remote-first EU/UA setup.

Responsibilities include shipping TypeScript client interfaces and server APIs; shaping domain modules; integrating internal services; covering critical paths with tests; and contributing to data and event design. You should be comfortable distinguishing a throwaway prototype from a production path with logging, error handling, and clear API contracts. Attention to complex table/state UX — and how permissions surface in the UI — matters.

Requirements: strong TypeScript; Node (or equivalent) plus a modern front-end stack (React/Vue/Svelte — exact stack confirmed at screening); REST/JSON APIs; auth/session or token-based access patterns; PostgreSQL or similar; disciplined code review and git hygiene. Nice to have: B2B SaaS background, queues/background workers, OpenAPI, observability (metrics/logs), and familiarity with audit-trail expectations in controlled environments. English must be workable for async collaboration across an EU-distributed team.

Format: full-time, Remote EU/UA. The employer is a Defence Tech product company; the client brand is not disclosed on this public page. Fidesa handles first contact, screens for stack and experience fit, and passes strong profiles to the hiring team. Contract details, compensation, and security onboarding are owned by the employer after successful interviews.

If you want to build operational software where mistakes are expensive, apply and send a CV with links to relevant experience (omit any classified or non-disclosable project detail).

**Apply CTA EN:** Apply  
**Supporting under CTA EN:** Send your CV — we will follow up on next steps.

---

### 5.3. Vacancy C — RF / Electronics Engineer

| Поле | Значення |
|---|---|
| `slug` | `rf-electronics-engineer` |
| `direction` | `electronics` |
| `location` | `ukraine` |
| `format` | `full-time-hybrid` |
| `employmentType` | `FULL_TIME` |
| `datePosted` | `2026-09-01` |

#### UK

**title:** RF / Electronics Engineer

**locationLabel:** Україна  
**formatLabel:** Full-time · Hybrid  
**directionLabel:** Electronics / RF  

**short:** Радіолінії та антенні рішення для unmanned systems: RF, схемотехніка, вимірювання. Супровід — Fidesa.

**full description (~UK):**

Відкрита роль RF / Electronics Engineer для команди, що проєктує радіолінії та антенні вузли для unmanned systems. Фокус — зв’язок і радіочастотний тракт: від вибору елементної бази й розрахунку лінійки до стендових вимірювань, узгодження з механікою/корпусом і супроводу дослідних партій. Ви взаємодіятимете з embedded-інженерами (протоколи, модеми, діагностика) та production-інженерами, які готують повторюваний складальний процес.

Обов’язки: участь у проєктуванні RF-трактів і суміжної електроніки; моделювання/оцінка лінк-бюджету на рівні, достатньому для інженерних рішень; підготовка й проведення вимірювань (спектр, КСХН/S-параметри — залежно від оснащення лабораторії); оформлення BOM і змін після тестів; документування обмежень інтеграції (розміщення антени, екранування, EMC-ризики). Потрібна дисципліна в змінах ревізій і чітка комунікація ризиків до product/systems owner.

Вимоги: профільна освіта або еквівалентний досвід у RF/електроніці; практика з вимірювальним обладнанням; розуміння антен, фідерних ліній, шумів і завад; вміння читати й коригувати схеми/PCB у зв’язці з layout-інженером. Переваги: досвід саме unmanned/defence або industrial wireless; знайомство з регуляторними обмеженнями; Python/MATLAB для обробки вимірів; досвід DFM для малих серій. Українська — основна робоча; англійська для datasheet і вендорів.

Формат: full-time, hybrid по Україні (офіс/лабораторія + віддалені дні за домовленістю; конкретне місто базування уточнюється на скринінгу). Замовник — виробник/інтегратор у Defence Tech; публічно ім’я не вказується. Fidesa організовує відгук, первинну оцінку релевантності та передачу кандидатів роботодавцю. Компенсація, форма зайнятості й доступ до лабораторії — предмет розмови з наймаючою стороною.

Якщо вам близька інженерія радіоліній «від плати до польового лінку» і ви готові працювати в гібридному режимі з вимірюваннями на стенді — натисніть «Відгукнутися» та надішліть резюме.

**Apply CTA UK:** Відгукнутися  
**Supporting under CTA UK:** Надішліть резюме — ми зв’яжемося щодо наступних кроків.

#### EN

**title:** RF / Electronics Engineer

**locationLabel:** Ukraine  
**formatLabel:** Full-time · Hybrid  
**directionLabel:** Electronics / RF  

**short:** Radio links and antenna solutions for unmanned systems: RF design, electronics, measurement. Supported by Fidesa.

**full description (~EN):**

We are hiring an RF / Electronics Engineer for a team designing radio links and antenna assemblies for unmanned systems. The focus is the communications and RF path: component selection and link reasoning, bench measurement, mechanical/enclosure integration, and support through prototype batches. You will work with embedded engineers (protocols, modems, diagnostics) and production engineers preparing a repeatable build process.

Responsibilities include contributing to RF path and related electronics design; link-budget reasoning at a level that drives engineering decisions; preparing and running measurements (spectrum, VSWR/S-parameters depending on lab tooling); maintaining BOM and post-test change notes; and documenting integration constraints (antenna placement, shielding, EMC risks). Revision discipline and clear risk communication to the product/systems owner are essential.

Requirements: formal background or equivalent experience in RF/electronics; hands-on measurement practice; working knowledge of antennas, feed lines, noise and interference; ability to read and revise schematics/PCB in partnership with a layout engineer. Nice to have: unmanned/defence or industrial wireless experience; awareness of regulatory constraints; Python/MATLAB for measurement post-processing; DFM for small-series builds. Ukrainian is the primary working language; English is needed for datasheets and vendors.

Format: full-time, hybrid across Ukraine (lab/office days plus remote days by agreement; exact base city confirmed at screening). The client is a Defence Tech manufacturer/integrator; the name is not published here. Fidesa manages applications, initial relevance screening, and handoff to the employer. Compensation, employment form, and lab access are discussed with the hiring side.

If you want radio-link engineering from board to field link — and are ready for hybrid work with bench measurement — click Apply and send your CV.

**Apply CTA EN:** Apply  
**Supporting under CTA EN:** Send your CV — we will follow up on next steps.

---

### 5.4. Зведена матриця для фільтрів (перевірка покриття)

| Slug | direction | location | format |
|---|---|---|---|
| `embedded-software-engineer-uav` | `embedded` | `kyiv` | `full-time-remote` |
| `fullstack-defence-saas` | `software` | `remote-eu-ua` | `full-time-remote` |
| `rf-electronics-engineer` | `electronics` | `ukraine` | `full-time-hybrid` |

Кожна комбінація фільтра на старті має давати передбачуваний результат (1 або 0–2 картки). Після «Скинути» — завжди 3.

---

## 6. Detail page — breadcrumb і Apply UX

### 6.1. Структура сторінки

1. Breadcrumb  
2. H1 = title вакансії  
3. Meta row: location · format · direction · datePosted  
4. Full description (HTML з Markdown)  
5. Блок Apply (CTA + supporting)  
6. Опційно (не блокер MVP): «Інші вакансії» — 1–2 лінки без окремого дизайну-каруселі  

### 6.2. Breadcrumb labels

| Позиція | UK | EN | URL |
|---|---|---|---|
| 1 | Головна | Home | `/` або `/en/` |
| 2 | Вакансії | Vacancies | `/vacancies/` або `/en/vacancies/` |
| 3 | {title} | {title} | поточна (не лінк або `aria-current="page"`) |

Schema: `BreadcrumbList` з трьома ListItem (Home → Vacancies → Title).

### 6.3. Apply UX

| Аспект | Рішення |
|---|---|
| Кнопка | Primary CTA: «Відгукнутися» / «Apply» |
| Supporting | Рядок під кнопкою (§5 тексти) |
| Механіка MVP | `mailto:` на контакт агенції з subject, що містить title + slug (напр. `Application: Embedded Software Engineer (UAV)`) **або** зовнішня form URL з query `role={slug}` — обрати один варіант на етапі реалізації Task 6/контактів і **зафіксувати один** для всіх трьох |
| Що не робити | Не вбудовувати ATS iframe; не Calendly як apply; не upload-віджет, що тягне важкий third-party у first load; не chat |
| Після кліку | Відкриття поштового клієнта / зовнішньої форми; на сторінці можна коротко лишити той самий supporting текст (без фейкового «дякуємо» без підтвердження відправки) |
| Privacy | Не збирати CV на своєму сервері в MVP без окремого рішення; mailto/зовнішня форма знімає hosting резюме |

Рекомендований дефолт плану: **mailto** на адресу з Contact/footer (коли з’явиться в Task home/contact), з тілом-заготовкою «Ім’я / Лінк на CV / Коротко про досвід». Якщо email ще не зафіксований у контенті — використати плейсхолдер-ключ `careers@…` лише після появи реального ящика в контент-активах; доти тримати CTA як кнопку з `mailto` на узгоджений адрес з footer.

### 6.4. Мета detail

| Поле | Шаблон UK | Шаблон EN |
|---|---|---|
| title | `{Vacancy title} — Вакансії — Fidesa` | `{Vacancy title} — Vacancies — Fidesa` |
| description | Перші ~150–160 символів від `short` або стислий paraphrase short | same from EN `short` |

---

## 7. JobPosting schema — список полів (без коду)

На **кожній** detail-сторінці — JSON-LD `@type: JobPosting`. Поля:

| Поле schema.org | Джерело / правило Fidesa |
|---|---|
| `@context` | `https://schema.org` |
| `@type` | `JobPosting` |
| `title` | frontmatter `title` |
| `description` | повний текст опису (plain/HTML-consistent з visible body) |
| `datePosted` | ISO дата frontmatter |
| `employmentType` | `FULL_TIME` (для стартових трьох) |
| `hiringOrganization` | Організація **Fidesa** (`Organization`: name, url відповідного домену) **або** формулювання конфіденційного клієнта через агенцію — **не** публікувати бренд замовника |
| `jobLocation` | `Place` + `PostalAddress`: країна UA; для Kyiv — addressLocality Kyiv/Київ; для Remote — `jobLocationType: TELECOMMUTE` + `applicantLocationRequirements` (UA та/або EU за роллю) |
| `jobLocationType` | `TELECOMMUTE` якщо remote/hybrid-remote акцент; для hybrid — уточнити Place (Ukraine) + примітка в description |
| `identifier` | slug або внутрішній id агенції |
| `url` | абсолютний canonical URL detail |
| `directApply` | `true` якщо є прямий apply (mailto/form) на сторінці |
| `industry` | напр. Defence Technology / Defense & Space (узгодити EN spelling у EN-schema) |
| `occupationalCategory` | опційно: коротка категорія (Software Engineering / Electronics Engineering) |
| `validThrough` | опційно; якщо немає дати закриття — не вимикати JobPosting, можна опустити або ставити +90 днів від `datePosted` за політикою оновлення |

**Не включати в MVP schema:** `baseSalary` (немає salary на сайті), логотип клієнта, `employmentUnit` клієнта.

Паралельно на detail: `BreadcrumbList` (§6.2).  
На list: достатньо звичайних meta + опційно `CollectionPage` / `ItemList` — **не обов’язково** для DoD Task 4; обов’язковий мінімум schema для задачі — **JobPosting на detail**.

---

## 8. Кроки реалізації (checkbox) + DoD + mobile

### 8.1. Підготовка контенту

- [ ] **Step 1.** Створити 3 UK Markdown-файли в `content/uk/vacancies/` зі frontmatter (§3.4) і повними текстами §5.1–5.3 (UK).
- [ ] **Step 2.** Створити 3 EN Markdown-файли в `content/en/vacancies/` (ті самі slug, тексти EN з §5).
- [ ] **Step 3.** Перевірити `short` ≤160 символів у кожній мові; direction/location/format values з матриці §5.4.

### 8.2. List page

- [ ] **Step 4.** Зібрати `/vacancies/` (UK) і `/en/vacancies/` (EN): H1, intro, meta з §2.
- [ ] **Step 5.** Відрендерити всі картки в HTML з `data-direction`, `data-location`, `data-format` і полями §4.1.
- [ ] **Step 6.** Додати toolbar фільтрів: Direction / Location / Format + Reset (§2.3–2.4); labels через `<label>` / `fieldset`.
- [ ] **Step 7.** Підключити клієнтський фільтр (логіка в `filters.js`): AND між групами, лічильник, empty state, sync query string без reload.
- [ ] **Step 8.** Переконатися: **немає** salary-filter, **немає** client logos, **немає** chat, **немає** Companies tab.

### 8.3. Detail pages

- [ ] **Step 9.** Зібрати 6 HTML detail (3 slug × 2 мови) за URL map §1.
- [ ] **Step 10.** Breadcrumb UK/EN (§6.2) + видимий meta row + full description.
- [ ] **Step 11.** Apply CTA + supporting; єдиний механізм mailto або зовнішньої форми (§6.3).
- [ ] **Step 12.** JSON-LD JobPosting з полями §7 + BreadcrumbList; title/description meta (§6.4).
- [ ] **Step 13.** hreflang + canonical на list і кожній detail (§1.3).

### 8.4. Mobile і диференціація

- [ ] **Step 14.** Mobile stack карток (§4.3): title → meta → excerpt → full-width «Детальніше»/«View details».
- [ ] **Step 15.** Mobile filter UX: snap-chips або один sheet «Фільтри»; touch ≥44px; перевірка на ширині ~360–390px.
- [ ] **Step 16.** Візуально звірити з антипатерном BazaIT Jobs: логіка так, UI Fidesa (navy/graphite, без чужого chrome).
- [ ] **Step 17.** Перевірити: на home **немає** блоку-лістингу вакансій — лише пункт Nav/Footer «Вакансії»/«Vacancies».
- [ ] **Step 18.** View-source: тексти вакансій і detail description присутні в HTML без обов’язкового JS.
- [ ] **Step 19.** Ручний прогін фільтрів за матрицею §5.4 + Reset → 3 картки; share URL з query відкриває той самий відфільтрований стан.
- [ ] **Step 20.** Мовне дзеркало path: `/vacancies/{slug}/` ↔ `/en/vacancies/{slug}/` не 404.

### 8.5. Definition of Done

Task 4 вважається завершеним, коли одночасно виконано:

1. **Контент:** 3 вакансії повністю UK+EN (title, location, format, direction, short, full ~200–400 words, apply CTA) опубліковані за slug з §5.  
2. **List + filters:** працюють `direction`, `location`, `format` + лічильник + empty + Reset + query sync; **без** salary-filter, logos, chat.  
3. **Detail:** окремі індексовані URL; breadcrumb; Apply UX; JobPosting schema з полями §7.  
4. **Mobile:** стек-картки + адекватний filter UX (§0A.5).  
5. **SEO/AEO:** key copy в HTML; hreflang між UA/EN парами.  
6. **Диференціація:** UI не плутається з app.bazait.com; home без дубль-лістингу вакансій.  
7. **Анти-скоуп дотримано:** немає Companies tab, login, Chatwoot, обов’язкового salary.

### 8.6. Поза скоупом Task 4 (не блокують DoD)

- Реальні вакансії замість плейсхолдерів.  
- ATS-інтеграція.  
- Related vacancies карусель.  
- Pagination / «Показати ще».  
- Salary в картці чи schema.  
- Окремі CMS admin screens.

---

## 9. Самоперевірка плану vs мастер-план

| Вимога | Де в цьому документі |
|---|---|
| §0A.5 матриця take/skip | §3 |
| §3.3 list/detail copy + 3 ролі | §2, §5 |
| §4.3 filters, query, mobile, no home list | §3, §4, §8 |
| JobPosting | §7 |
| about.md §3.2 job listing pattern | §1–4 |
| about.md §6 JobPosting | §7 |
| Без коду в плані | виконано |
| Тексти вакансій повністю UK+EN | §5 |

---

**План збережено.** Реалізацію Task 4 виконувати окремо за цим документом, не змішуючи з Task 5 (Блог) та іншими задачами мастер-плану.
