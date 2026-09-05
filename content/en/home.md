# Fidesa — home (EN)

Джерело істин для копірайту: `docs/superpowers/plans/tasks/2026-09-04-task-03-home-en-i18n.md` §2–4.
Рендер: `public/en-site/en/index.html`.

## Meta

- **Title:** Fidesa — Defence Tech Recruitment
- **Description:** Fidesa is a specialized recruiting agency for defence manufacturers, UAV builders, and defence software teams. We hire engineers and technical talent with security-aware screening.
- **lang:** en
- **Canonical:** https://fidesa.agency/en/
- **hreflang:** uk → https://fidesa.com.ua/ · en → https://fidesa.agency/en/ · x-default → https://fidesa.agency/en/
- **OG locale:** en_US (alternate uk_UA)

## Nav

1. About → #about
2. Process → #process
3. Why Fidesa → #why
4. Team → #team
5. Vacancies → /en/vacancies/
6. Blog → /en/blog/
7. Contact → #contact
8. UA → https://fidesa.com.ua/

## CTA

- Header desktop: Book a call
- Header mobile: Book
- Hero primary: Book a call → #contact / [CALENDLY_URL]
- Hero secondary: How we work → #process
- Contact: Open calendar · fallback «Open Calendly in a new tab» → [CALENDLY_URL]
- Skip: Skip to content → #main
- Hamburger: Open menu / Close menu

## Hero

- **Brand:** Fidesa
- **H1:** Recruitment for Defence Tech
- **Supporting:** We hire engineers, developers, and technical leaders for companies building weapons systems, unmanned platforms, and defence software.

## About (#about)

- **H2:** What Fidesa is
- **Lead:** Fidesa is a recruiting agency focused exclusively on Defence Tech.
- **Body:** We help defence manufacturers and product teams fill critical roles — from embedded systems and RF engineering to software, data, and production. One focus: the defence market. We do not run generalist IT recruiting alongside Defence Tech.

### Q→A

**Who is Fidesa for?**  
For hiring companies: weapons and UAV manufacturers, and engineering and software teams in the defence sector. Candidates use a separate vacancies page — the home page is built for hiring teams.

**What do we do?**  
Full-cycle recruiting: briefing, search, screening, interview coordination, offer support, and follow-through until the candidate starts. Commercial terms are discussed on a call — this site does not publish packages or commission rates.

**Why narrow specialization?**  
Market depth, role fluency, and security expectations produce faster, higher-quality hires than generalist agencies where Defence Tech is only one vertical among many.

## Process (#process)

- **H2:** How engagement works
- **Intro:** A transparent path from brief to hire — with clear stages and ownership on both sides.

1. **Brief** — We lock the role, stack, seniority, security constraints, timeline, and success criteria. We agree what can be published about the vacancy and what stays confidential.
2. **Search & screening** — We research the market, check profile fit and risks within the agency’s protocols, and prepare a shortlist for your team.
3. **Interviews** — We coordinate meetings with your team, collect feedback after each round, and recalibrate the search.
4. **Offer & onboarding** — We support the offer stage, decision-making, and the candidate’s start — until the hire is complete by your criteria.

- **Microcopy:** An agreement between two sides is the foundation of our work.

## Why (#why)

- **H2:** Why companies choose Fidesa
- **Intro:** Defence Tech specialization is the primary reason. Security is a required part of delivery — not a slogan.

### Operational security

- Confidential communication with clients and candidates.
- Need-to-know access to vacancy and project data.
- Protection of the client’s personal and commercial data under applicable law.

**How do you protect client information?**  
We minimize who can access the brief, do not publish client identifiers without permission, and use secured communication channels.

### Hiring security

- Screening for links to the russian federation and occupied territories within available and lawful procedures.
- Consideration of military status and constraints relevant to the role and jurisdiction.
- Compliance with personal-data protection requirements when processing CVs and communications.

**Do you guarantee absolute vetting?**  
We apply screening protocols and escalate edge cases to the client. Final clearance decisions always remain with the client and their compliance processes.

## Team (#team)

- **H2:** Team
- **Intro:** The people you work with directly.

### Valeriia — Founder

Valeriia leads Fidesa and owns agency growth and key client relationships. She is the public face of the brand, focused on building specialized Defence Tech recruiting and reliable service for teams scaling defence products.

- Photo alt: Valeriia, Founder of Fidesa

### CTO

A CTO with military background — bringing engineering judgment to role design and candidate requirements in Defence Tech.

## Testimonials (#testimonials)

- **H2:** Client testimonials
- **Empty:** Client testimonials will appear here. This module is ready to be populated.

## Contact (#contact)

- **H2:** Book a call
- **Supporting:** A short conversation with the founder or team — to clarify the role, timeline, and whether we can help.
- **CTA:** Open calendar
- **Fallback:** Open Calendly in a new tab → [CALENDLY_URL] (target=_blank, rel=noopener noreferrer; accessible name = visible text)
- **Lazy:** `data-calendly-root` + `calendly-lazy.js` (click mount; IntersectionObserver preload). Sync Contacts markup manually with UK home until SSG.
- **Email:** Email · [EMAIL_PLACEHOLDER]
- **Location:** Ukraine · serving clients in Ukraine and internationally

## Footer

- Tagline: Specialized recruiting for Defence Tech
- Links: Vacancies · Blog · Privacy · UA
- Privacy: /en/privacy/
- Copyright: © 2026 Fidesa

## Geo banner (agency; Variant A default)

- Message: Схоже, вам зручніша українська версія сайту.
- Primary: Перейти на fidesa.com.ua
- Secondary: Залишитись англійською
- Dismiss: Закрити
- Persist: Більше не показувати

### Variant B (EN mirror)

- Message: Looking for the Ukrainian version of this site?
- Primary: Go to fidesa.com.ua
- Secondary: Stay in English
- Dismiss: Dismiss
- Persist: Don’t show again
