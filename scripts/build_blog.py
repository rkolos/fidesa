#!/usr/bin/env python3
"""Generate static blog pages (UK + EN) from content/*/blog/*.md."""

from __future__ import annotations

import html
import json
import re
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

TAGS = {
    "defence-tech": {"uk": "Defence Tech", "en": "Defence Tech"},
    "recruiting": {"uk": "Рекрутинг", "en": "Recruiting"},
    "security": {"uk": "Безпека", "en": "Security"},
    "engineering-hiring": {"uk": "Інженерний найм", "en": "Engineering hiring"},
    "ukraine": {"uk": "Україна", "en": "Ukraine"},
}

AUTHORS = {
    "valeriia": {
        "uk": {"name": "Валерія", "role": "Засновниця Fidesa", "alt": "Валерія, засновниця Fidesa"},
        "en": {"name": "Valeriia", "role": "Founder, Fidesa", "alt": "Valeriia, Founder of Fidesa"},
        "schema": "Person",
        "photo": None,  # assets/images/team/valeriia.webp when ready
    },
    "fidesa-team": {
        "uk": {"name": "Команда Fidesa", "role": "Редакція агенції", "alt": None},
        "en": {"name": "Fidesa Team", "role": "Agency editorial", "alt": None},
        "schema": "Organization",
        "photo": None,
    },
}

UI = {
    "uk": {
        "nav_blog": "Блог",
        "subtitle": "Нотатки про найм у Defence Tech",
        "read_more": "Читати далі",
        "published": "Опубліковано",
        "by_author": "Автор",
        "tags": "Теги",
        "all_posts": "Усі матеріали",
        "filter_by_tag": "За тегом",
        "tag_heading": "Тег: {label}",
        "empty_tag": "Поки немає матеріалів з цим тегом.",
        "related": "Схожі матеріали",
        "back_to_list": "До списку блогу",
        "breadcrumb_home": "Головна",
        "breadcrumb_blog": "Блог",
        "meta_list_title": "Блог — Fidesa",
        "meta_list_desc": "Статті Fidesa про рекрутинг у Defence Tech: спеціалізація, скринінг і бриф ролей.",
        "skip": "Перейти до контенту",
        "nav_aria": "Основна навігація",
        "footer_nav_aria": "Навігація в підвалі",
        "open_menu": "Відкрити меню",
        "cta_short": "Дзвінок",
        "cta_full": "Забронювати дзвінок",
        "tagline": "Спеціалізований рекрутинг для Defence Tech",
        "nav_about": "Про нас",
        "nav_process": "Процес",
        "nav_why": "Чому Fidesa",
        "nav_team": "Команда",
        "nav_vacancies": "Вакансії",
        "nav_contact": "Контакти",
        "home": "/",
        "blog": "/blog/",
        "vacancies": "/vacancies/",
        "privacy": "/privacy/",
        "contact": "/#contact",
        "team_anchor": "/#team",
        "origin": "https://fidesa.com.ua",
        "og_locale": "uk_UA",
        "lang": "uk",
        "site": "uk",
        "hreflang_path_prefix": "",
        "other_lang": "en",
        "other_label": "EN",
        "months": [
            "",
            "січня",
            "лютого",
            "березня",
            "квітня",
            "травня",
            "червня",
            "липня",
            "серпня",
            "вересня",
            "жовтня",
            "листопада",
            "грудня",
        ],
    },
    "en": {
        "nav_blog": "Blog",
        "subtitle": "Notes on hiring in Defence Tech",
        "read_more": "Read more",
        "published": "Published",
        "by_author": "By",
        "tags": "Tags",
        "all_posts": "All posts",
        "filter_by_tag": "Filtered by tag",
        "tag_heading": "Tag: {label}",
        "empty_tag": "No posts with this tag yet.",
        "related": "Related posts",
        "back_to_list": "Back to blog",
        "breadcrumb_home": "Home",
        "breadcrumb_blog": "Blog",
        "meta_list_title": "Blog — Fidesa",
        "meta_list_desc": "Fidesa articles on Defence Tech recruiting: specialization, screening, and role briefs.",
        "skip": "Skip to content",
        "nav_aria": "Primary",
        "footer_nav_aria": "Footer",
        "open_menu": "Open menu",
        "cta_short": "Call",
        "cta_full": "Book a call",
        "tagline": "Specialized recruiting for Defence Tech",
        "nav_about": "About",
        "nav_process": "Process",
        "nav_why": "Why Fidesa",
        "nav_team": "Team",
        "nav_vacancies": "Vacancies",
        "nav_contact": "Contact",
        "home": "/en/",
        "blog": "/en/blog/",
        "vacancies": "/en/vacancies/",
        "privacy": "/en/privacy/",
        "contact": "/en/#contact",
        "team_anchor": "/en/#team",
        "origin": "https://fidesa.agency",
        "og_locale": "en_US",
        "lang": "en",
        "site": "agency",
        "hreflang_path_prefix": "/en",
        "other_lang": "uk",
        "other_label": "UA",
        "months": [
            "",
            "January",
            "February",
            "March",
            "April",
            "May",
            "June",
            "July",
            "August",
            "September",
            "October",
            "November",
            "December",
        ],
    },
}

FOOTER_MEANDER = """
        <div class="site-footer__decor container" aria-hidden="true">
          <svg
            class="site-footer__meander"
            width="120"
            height="12"
            viewBox="0 0 120 12"
            fill="none"
            xmlns="http://www.w3.org/2000/svg"
          >
            <path
              d="M1 6h8l4-4 4 4h8l4 4 4-4h8l4-4 4 4h8l4 4 4-4h8l4-4 4 4h8l4 4 4-4h14"
              stroke="currentColor"
              stroke-width="1"
              stroke-linejoin="miter"
            />
          </svg>
        </div>"""


def parse_frontmatter(text: str) -> tuple[dict, str]:
    if not text.startswith("---\n"):
        raise ValueError("missing frontmatter")
    _, rest = text.split("---\n", 1)
    fm_raw, body = rest.split("\n---\n", 1)
    meta: dict = {}
    for line in fm_raw.strip().splitlines():
        if ":" not in line:
            continue
        key, val = line.split(":", 1)
        key = key.strip()
        val = val.strip()
        if key == "tags":
            inner = val.strip("[]")
            meta[key] = [t.strip() for t in inner.split(",") if t.strip()]
        elif val.startswith('"') and val.endswith('"'):
            meta[key] = val[1:-1]
        else:
            meta[key] = val
    return meta, body.lstrip("\n")


def inline_md(text: str) -> str:
    text = html.escape(text)

    def code_repl(m: re.Match) -> str:
        return f"<code>{m.group(1)}</code>"

    text = re.sub(r"`([^`]+)`", code_repl, text)

    def link_repl(m: re.Match) -> str:
        label = m.group(1)
        href = m.group(2)
        return f'<a href="{html.escape(href, quote=True)}">{label}</a>'

    text = re.sub(r"\[([^\]]+)\]\(([^)]+)\)", link_repl, text)
    text = re.sub(r"\*\*([^*]+)\*\*", r"<strong>\1</strong>", text)
    text = re.sub(r"(?<!\*)\*([^*]+)\*(?!\*)", r"<em>\1</em>", text)
    return text


def markdown_to_html(body: str, skip_h1: bool = True) -> str:
    lines = body.splitlines()
    out: list[str] = []
    i = 0
    skipped_h1 = False

    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1
            continue

        if line.startswith("# ") and skip_h1 and not skipped_h1:
            skipped_h1 = True
            i += 1
            continue

        if line.startswith("### "):
            out.append(f"<h3>{inline_md(line[4:].strip())}</h3>")
            i += 1
            continue
        if line.startswith("## "):
            out.append(f"<h2>{inline_md(line[3:].strip())}</h2>")
            i += 1
            continue
        if line.startswith("# "):
            out.append(f"<h2>{inline_md(line[2:].strip())}</h2>")
            i += 1
            continue

        if line.strip().startswith("|") and i + 1 < len(lines) and set(lines[i + 1].strip()) <= set("|-: "):
            rows = []
            while i < len(lines) and lines[i].strip().startswith("|"):
                row = lines[i].strip()
                if not any(c not in "|-: " for c in row):
                    i += 1
                    continue
                cells = [c.strip() for c in row.strip("|").split("|")]
                rows.append(cells)
                i += 1
            if rows:
                out.append('<div class="blog-table-wrap"><table class="blog-table">')
                out.append("<thead><tr>" + "".join(f"<th>{inline_md(c)}</th>" for c in rows[0]) + "</tr></thead>")
                if len(rows) > 1:
                    out.append("<tbody>")
                    for row in rows[1:]:
                        out.append("<tr>" + "".join(f"<td>{inline_md(c)}</td>" for c in row) + "</tr>")
                    out.append("</tbody>")
                out.append("</table></div>")
            continue

        # Checklist before plain bullets so "- [ ] item" is never swallowed as a bullet.
        if re.match(r"^[-*] \[[ xX]\]", line.strip()):
            out.append('<ul class="blog-checklist">')
            while i < len(lines) and re.match(r"^[-*] \[[ xX]\]", lines[i].strip()):
                raw = lines[i].strip()
                checked = bool(re.match(r"^[-*] \[[xX]\]", raw))
                item = re.sub(r"^[-*] \[[ xX]\]\s*", "", raw)
                cls = ' class="is-checked"' if checked else ""
                aria = ' aria-checked="true"' if checked else ' aria-checked="false"'
                out.append(f'<li role="checkbox"{cls}{aria}>{inline_md(item)}</li>')
                i += 1
            out.append("</ul>")
            continue

        if re.match(r"^[-*] ", line.strip()):
            out.append("<ul>")
            while i < len(lines) and re.match(r"^[-*] ", lines[i].strip()):
                # Stop if next item is a checklist row (mixed list edge case).
                if re.match(r"^[-*] \[[ xX]\]", lines[i].strip()):
                    break
                item = re.sub(r"^[-*] ", "", lines[i].strip())
                out.append(f"<li>{inline_md(item)}</li>")
                i += 1
            out.append("</ul>")
            continue

        if re.match(r"^\d+\. ", line.strip()):
            out.append("<ol>")
            while i < len(lines) and re.match(r"^\d+\. ", lines[i].strip()):
                item = re.sub(r"^\d+\. ", "", lines[i].strip())
                out.append(f"<li>{inline_md(item)}</li>")
                i += 1
            out.append("</ol>")
            continue

        para = []
        while i < len(lines) and lines[i].strip() and not lines[i].startswith("#") and not re.match(
            r"^([-*] |\d+\. |\|)", lines[i].strip()
        ):
            para.append(lines[i])
            i += 1
        if para:
            text = " ".join(s.strip() for s in para)
            out.append(f"<p>{inline_md(text)}</p>")

    return "\n".join(out)


def format_date(iso: str, lang: str) -> str:
    y, m, d = map(int, iso.split("-"))
    months = UI[lang]["months"]
    if lang == "uk":
        return f"{d} {months[m]} {y}"
    return f"{d} {months[m]} {y}"


def posts_count_label(n: int, lang: str) -> str:
    if lang == "en":
        return f"{n} post" if n == 1 else f"{n} posts"
    if n % 10 == 1 and n % 100 != 11:
        return f"{n} матеріал"
    if n % 10 in (2, 3, 4) and n % 100 not in (12, 13, 14):
        return f"{n} матеріали"
    return f"{n} матеріалів"


def asset_prefix(depth: int) -> str:
    return "../" * depth


def other_url(lang: str, logical_path: str) -> str:
    """logical_path like /blog/ or /blog/slug/ (no /en)."""
    if lang == "uk":
        return "https://fidesa.agency/en" + logical_path
    return "https://fidesa.com.ua" + logical_path


def absolute_url(lang: str, logical_path: str) -> str:
    ui = UI[lang]
    if lang == "uk":
        return ui["origin"] + logical_path
    return ui["origin"] + "/en" + logical_path


def home_absolute(lang: str) -> str:
    """Canonical home URL for schema breadcrumbs."""
    if lang == "uk":
        return "https://fidesa.com.ua/"
    return "https://fidesa.agency/en/"


def load_posts(lang: str) -> list[dict]:
    folder = ROOT / "content" / lang / "blog"
    posts = []
    for path in sorted(folder.glob("*.md")):
        meta, body = parse_frontmatter(path.read_text(encoding="utf-8"))
        slug = meta.get("slug") or path.stem
        author = meta.get("author")
        if author not in AUTHORS:
            raise ValueError(f"{path}: unknown author {author!r}; expected one of {sorted(AUTHORS)}")
        tags = meta.get("tags") or []
        for tid in tags:
            if tid not in TAGS:
                raise ValueError(f"{path}: unknown tag {tid!r}; expected one of {sorted(TAGS)}")
        if "date" not in meta:
            raise ValueError(f"{path}: missing date")
        updated = meta.get("updated") or meta["date"]

        html_body = markdown_to_html(body)

        posts.append(
            {
                "slug": slug,
                "author": author,
                "date": meta["date"],
                "updated": updated,
                "tags": tags,
                "title": meta["title"],
                "summary": meta["summary"],
                "body_html": html_body,
                "path": f"/blog/{slug}/",
            }
        )
    posts.sort(key=lambda p: p["date"], reverse=True)
    return posts


def related_posts(post: dict, all_posts: list[dict], limit: int = 3) -> list[dict]:
    scored = []
    my_tags = set(post["tags"])
    for other in all_posts:
        if other["slug"] == post["slug"]:
            continue
        overlap = len(my_tags & set(other["tags"]))
        if overlap == 0:
            continue
        scored.append((overlap, other["date"], other))
    # highest overlap first; on tie newer date first
    scored.sort(key=lambda t: (-t[0], -int(t[1].replace("-", ""))))
    return [t[2] for t in scored[:limit]]


def header_footer(lang: str, depth: int, logical_path: str, current: str | None = None) -> tuple[str, str]:
    ui = UI[lang]
    prefix = asset_prefix(depth)
    mirror = other_url(lang, logical_path)
    other = ui["other_label"]
    other_lang = ui["other_lang"]

    def nav_item(href: str, label: str, key: str) -> str:
        cur = ' aria-current="page"' if current == key else ""
        return f'<li><a href="{href}"{cur}>{label}</a></li>'

    header = f"""      <header class="site-header">
        <div class="container site-header__inner">
          <a class="site-header__brand" href="{ui['home']}">
            <img
              class="site-header__logo"
              src="/assets/brand/logo.svg"
              width="33"
              height="38"
              alt=""
              decoding="async"
            />
            <span class="site-header__wordmark">Fidesa</span>
          </a>
          <nav class="site-nav" aria-label="{ui['nav_aria']}">
            <ul class="site-nav__list">
              {nav_item(ui['home'] + '#about', ui['nav_about'], 'about')}
              {nav_item(ui['home'] + '#process', ui['nav_process'], 'process')}
              {nav_item(ui['home'] + '#why', ui['nav_why'], 'why')}
              {nav_item(ui['home'] + '#team', ui['nav_team'], 'team')}
              {nav_item(ui['vacancies'], ui['nav_vacancies'], 'vacancies')}
              {nav_item(ui['blog'], ui['nav_blog'], 'blog')}
              {nav_item(ui['home'] + '#contact', ui['nav_contact'], 'contact')}
            </ul>
          </nav>
          <div class="site-header__actions">
            <a
              class="site-header__lang"
              href="{mirror}"
              hreflang="{other_lang}"
              lang="{other_lang}"
              data-domain-switch="{other_lang}"
              >{other}</a
            >
            <a class="btn-primary" href="{ui['contact']}">
              <span class="btn-primary__short">{ui['cta_short']}</span>
              <span class="btn-primary__full">{ui['cta_full']}</span>
            </a>
            <button
              class="nav-toggle"
              type="button"
              aria-controls="nav-drawer"
              aria-expanded="false"
              aria-label="{ui['open_menu']}"
            >
              <span class="nav-toggle__icon" aria-hidden="true">
                <span></span><span></span><span></span>
              </span>
            </button>
          </div>
        </div>
        <div class="nav-drawer" id="nav-drawer" hidden>
          <div class="container">
            <ul class="nav-drawer__list">
              {nav_item(ui['home'] + '#about', ui['nav_about'], 'about')}
              {nav_item(ui['home'] + '#process', ui['nav_process'], 'process')}
              {nav_item(ui['home'] + '#why', ui['nav_why'], 'why')}
              {nav_item(ui['home'] + '#team', ui['nav_team'], 'team')}
              {nav_item(ui['vacancies'], ui['nav_vacancies'], 'vacancies')}
              {nav_item(ui['blog'], ui['nav_blog'], 'blog')}
              {nav_item(ui['home'] + '#contact', ui['nav_contact'], 'contact')}
            </ul>
            <p class="nav-drawer__lang">
              <a
                href="{mirror}"
                hreflang="{other_lang}"
                lang="{other_lang}"
                data-domain-switch="{other_lang}"
                >{other}</a
              >
            </p>
          </div>
        </div>
      </header>"""

    footer = f"""      <footer class="site-footer">
        <div class="container site-footer__inner">
          <div>
            <p class="site-footer__brand">Fidesa</p>
            <p class="site-footer__tagline">{ui['tagline']}</p>
          </div>
          <nav class="site-footer__nav-wrap" aria-label="{ui['footer_nav_aria']}">
            <ul class="site-footer__nav site-footer__nav--sections">
              <li><a href="{ui['home']}#about">{ui['nav_about']}</a></li>
              <li><a href="{ui['home']}#process">{ui['nav_process']}</a></li>
              <li><a href="{ui['home']}#why">{ui['nav_why']}</a></li>
              <li><a href="{ui['home']}#team">{ui['nav_team']}</a></li>
              <li><a href="{ui['contact']}">{ui['nav_contact']}</a></li>
            </ul>
            <ul class="site-footer__nav">
              <li><a href="{ui['vacancies']}">{ui['nav_vacancies']}</a></li>
              <li><a href="{ui['blog']}"{" aria-current=\"page\"" if current == "blog" else ""}>{ui['nav_blog']}</a></li>
              <li><a href="{ui['privacy']}">Privacy</a></li>
              <li>
                <a
                  href="{mirror}"
                  hreflang="{other_lang}"
                  lang="{other_lang}"
                  data-domain-switch="{other_lang}"
                  >{other}</a
                >
              </li>
            </ul>
          </nav>
          <p class="site-footer__copy">© 2026 Fidesa</p>
        </div>
{FOOTER_MEANDER}
      </footer>"""
    return header, footer


def page_shell(
    lang: str,
    depth: int,
    title: str,
    description: str,
    logical_path: str,
    body_main: str,
    schema: dict | list | None = None,
    og_type: str = "website",
    current: str | None = "blog",
) -> str:
    ui = UI[lang]
    prefix = asset_prefix(depth)
    canon = absolute_url(lang, logical_path)
    uk_url = "https://fidesa.com.ua" + logical_path
    en_url = "https://fidesa.agency/en" + logical_path
    og_image = f"{ui['origin']}/assets/brand/og-default.svg"
    header, footer = header_footer(lang, depth, logical_path, current=current)

    schema_block = ""
    if schema is not None:
        schema_block = (
            '    <script type="application/ld+json">\n'
            + json.dumps(schema, ensure_ascii=False, indent=2)
            + "\n    </script>\n"
        )

    return f"""<!DOCTYPE html>
<html lang="{ui['lang']}" data-site="{ui['site']}">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{html.escape(title)}</title>
    <meta name="description" content="{html.escape(description)}" />
    <link rel="canonical" href="{canon}" />
    <link rel="alternate" hreflang="uk" href="{uk_url}" />
    <link rel="alternate" hreflang="en" href="{en_url}" />
    <link rel="alternate" hreflang="x-default" href="https://fidesa.agency/en/" />
    <meta property="og:type" content="{og_type}" />
    <meta property="og:locale" content="{ui['og_locale']}" />
    <meta property="og:url" content="{canon}" />
    <meta property="og:title" content="{html.escape(title)}" />
    <meta property="og:description" content="{html.escape(description)}" />
    <meta property="og:image" content="{og_image}" />
    <meta name="twitter:card" content="summary_large_image" />
    <meta name="twitter:title" content="{html.escape(title)}" />
    <meta name="twitter:description" content="{html.escape(description)}" />
    <meta name="twitter:image" content="{og_image}" />
    <link rel="icon" href="/assets/brand/favicon.svg" type="image/svg+xml" />
    <link
      rel="preload"
      href="/assets/fonts/IBMPlexSans-Regular.woff2"
      as="font"
      type="font/woff2"
      crossorigin
    />
    <link rel="stylesheet" href="/assets/css/site.css" />
{schema_block}  </head>
  <body>
    <div class="site">
      <a class="skip-link" href="#main">{ui['skip']}</a>
{header}
{body_main}
{footer}
    </div>
    <script src="/js/nav.js" defer></script>
    <script src="/js/domain-lang.js" defer></script>
  </body>
</html>
"""


def tag_chips(lang: str, tags: list[str]) -> str:
    ui = UI[lang]
    parts = []
    for tid in tags:
        label = TAGS[tid][lang]
        href = f"{ui['blog']}tag/{tid}/"
        parts.append(f'<a class="blog-tag" href="{href}">{html.escape(label)}</a>')
    return f'<ul class="blog-tags" aria-label="{ui["tags"]}">' + "".join(f"<li>{p}</li>" for p in parts) + "</ul>"


def byline_html(lang: str, author_id: str, iso_date: str, prefix: str = "") -> str:
    ui = UI[lang]
    author = AUTHORS[author_id]
    info = author[lang]
    date_str = format_date(iso_date, lang)
    photo = ""
    if author.get("photo"):
        src = author["photo"] if str(author.get("photo", "")).startswith(("http://", "https://", "/")) else "/" + str(author["photo"]).lstrip("/")
        photo = (
            f'<img class="blog-byline__photo" src="{html.escape(src, quote=True)}" width="48" height="48" '
            f'alt="{html.escape(info["alt"] or info["name"])}" decoding="async" />'
        )
    name_html = (
        f'<a class="blog-byline__name" href="{ui["team_anchor"]}">{html.escape(info["name"])}</a>'
        if author_id == "valeriia"
        else f'<span class="blog-byline__name">{html.escape(info["name"])}</span>'
    )
    return f"""          <div class="blog-byline">
            {photo}
            <div class="blog-byline__text">
              <p class="blog-byline__line">
                <span class="blog-byline__label">{ui['by_author']}</span>
                {name_html}
                <span class="blog-byline__role">{html.escape(info['role'])}</span>
              </p>
              <p class="blog-byline__date">
                <span class="blog-byline__label">{ui['published']}</span>
                <time datetime="{iso_date}">{date_str}</time>
              </p>
            </div>
          </div>"""


def card_html(lang: str, post: dict) -> str:
    ui = UI[lang]
    author = AUTHORS[post["author"]][lang]["name"]
    href = ui["blog"] + post["slug"] + "/"
    return f"""          <li>
            <article class="blog-card">
              <h2 class="blog-card__title">
                <a href="{href}">{html.escape(post['title'])}</a>
              </h2>
              <p class="blog-card__date"><time datetime="{post['date']}">{format_date(post['date'], lang)}</time></p>
              <p class="blog-card__author">{html.escape(author)}</p>
              {tag_chips(lang, post['tags'])}
              <p class="blog-card__summary">{html.escape(post['summary'])}</p>
              <a class="blog-card__more" href="{href}">{ui['read_more']}</a>
            </article>
          </li>"""


def write(path: Path, content: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(content, encoding="utf-8")
    print("wrote", path.relative_to(ROOT))


def build_list(lang: str, posts: list[dict]) -> None:
    ui = UI[lang]
    depth = 3 if lang == "uk" else 4
    out_dir = ROOT / ("public/uk-site/blog" if lang == "uk" else "public/en-site/en/blog")
    cards = "\n".join(card_html(lang, p) for p in posts)
    count = posts_count_label(len(posts), lang)
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "Blog",
                "name": ui["nav_blog"],
                "url": absolute_url(lang, "/blog/"),
                "description": ui["meta_list_desc"],
                "inLanguage": ui["lang"],
                "publisher": {"@type": "Organization", "name": "Fidesa", "url": ui["origin"] + "/"},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": ui["breadcrumb_home"], "item": home_absolute(lang)},
                    {"@type": "ListItem", "position": 2, "name": ui["breadcrumb_blog"], "item": absolute_url(lang, "/blog/")},
                ],
            },
        ],
    }

    main = f"""      <main id="main" class="page-blog">
        <div class="container section__inner">
          <nav aria-label="Breadcrumb">
            <ol class="breadcrumb">
              <li><a href="{ui['home']}">{ui['breadcrumb_home']}</a></li>
              <li aria-current="page">{ui['breadcrumb_blog']}</li>
            </ol>
          </nav>
          <h1>{ui['nav_blog']}</h1>
          <p class="page-blog__intro">{ui['subtitle']}</p>
          <p class="blog-count" aria-live="polite">{count}</p>
          <ul class="blog-list">
{cards}
          </ul>
        </div>
      </main>"""
    write(
        out_dir / "index.html",
        page_shell(lang, depth, ui["meta_list_title"], ui["meta_list_desc"], "/blog/", main, schema),
    )


def build_tag(lang: str, tag_id: str, posts: list[dict]) -> None:
    ui = UI[lang]
    label = TAGS[tag_id][lang]
    filtered = [p for p in posts if tag_id in p["tags"]]
    filtered.sort(key=lambda p: p["date"], reverse=True)
    depth = 5 if lang == "uk" else 6
    out_dir = ROOT / (
        f"public/uk-site/blog/tag/{tag_id}" if lang == "uk" else f"public/en-site/en/blog/tag/{tag_id}"
    )
    logical = f"/blog/tag/{tag_id}/"
    heading = ui["tag_heading"].format(label=label)
    title = f"{heading} — {ui['nav_blog']} — Fidesa"
    desc = f"{heading}. {ui['meta_list_desc']}"
    count = posts_count_label(len(filtered), lang)
    if filtered:
        cards = "\n".join(card_html(lang, p) for p in filtered)
        list_block = f'<ul class="blog-list">\n{cards}\n          </ul>'
    else:
        list_block = f'<p class="blog-empty">{ui["empty_tag"]}</p>'

    home_item = home_absolute(lang)
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "CollectionPage",
                "name": heading,
                "url": absolute_url(lang, logical),
                "inLanguage": ui["lang"],
                "isPartOf": {"@type": "Blog", "name": ui["nav_blog"], "url": absolute_url(lang, "/blog/")},
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": ui["breadcrumb_home"], "item": home_item},
                    {"@type": "ListItem", "position": 2, "name": ui["breadcrumb_blog"], "item": absolute_url(lang, "/blog/")},
                    {"@type": "ListItem", "position": 3, "name": heading, "item": absolute_url(lang, logical)},
                ],
            },
        ],
    }
    main = f"""      <main id="main" class="page-blog page-blog--tag">
        <div class="container section__inner">
          <nav aria-label="Breadcrumb">
            <ol class="breadcrumb">
              <li><a href="{ui['home']}">{ui['breadcrumb_home']}</a></li>
              <li><a href="{ui['blog']}">{ui['breadcrumb_blog']}</a></li>
              <li aria-current="page">{html.escape(heading)}</li>
            </ol>
          </nav>
          <p class="blog-tag-kicker">{ui['filter_by_tag']}</p>
          <h1>{html.escape(heading)}</h1>
          <p class="blog-count" aria-live="polite">{count}</p>
          <p class="blog-tag-nav"><a href="{ui['blog']}">{ui['all_posts']}</a></p>
          {list_block}
        </div>
      </main>"""
    write(out_dir / "index.html", page_shell(lang, depth, title, desc, logical, main, schema))


def author_schema(lang: str, author_id: str) -> dict:
    ui = UI[lang]
    info = AUTHORS[author_id][lang]
    if AUTHORS[author_id]["schema"] == "Organization":
        return {"@type": "Organization", "name": "Fidesa", "url": ui["origin"] + "/"}
    return {
        "@type": "Person",
        "name": info["name"],
        "url": home_absolute(lang) + "#team",
    }


def build_post(lang: str, post: dict, all_posts: list[dict]) -> None:
    ui = UI[lang]
    depth = 4 if lang == "uk" else 5
    prefix = asset_prefix(depth)
    out_dir = ROOT / (
        f"public/uk-site/blog/{post['slug']}" if lang == "uk" else f"public/en-site/en/blog/{post['slug']}"
    )
    logical = post["path"]
    related = related_posts(post, all_posts)
    related_html = ""
    if related:
        items = "".join(
            f'<li><a href="{ui["blog"]}{r["slug"]}/">{html.escape(r["title"])}</a></li>' for r in related
        )
        related_html = f"""          <section class="blog-related" aria-labelledby="related-heading">
            <h2 id="related-heading">{ui['related']}</h2>
            <ul class="blog-related__list">
              {items}
            </ul>
          </section>"""

    keywords = ", ".join(TAGS[t][lang] for t in post["tags"])
    canon = absolute_url(lang, logical)
    home_item = home_absolute(lang)
    author = author_schema(lang, post["author"])
    schema = {
        "@context": "https://schema.org",
        "@graph": [
            {
                "@type": "BlogPosting",
                "headline": post["title"],
                "description": post["summary"],
                "datePublished": post["date"],
                "dateModified": post["updated"],
                "inLanguage": ui["lang"],
                "mainEntityOfPage": {"@type": "WebPage", "@id": canon},
                "url": canon,
                "author": author,
                "publisher": {
                    "@type": "Organization",
                    "name": "Fidesa",
                    "logo": {
                        "@type": "ImageObject",
                        "url": f"{ui['origin']}/assets/brand/logo.svg",
                    },
                },
                "image": f"{ui['origin']}/assets/brand/og-default.svg",
                "keywords": keywords,
                "isPartOf": {"@type": "Blog", "name": ui["nav_blog"], "url": absolute_url(lang, "/blog/")},
                "articleSection": TAGS[post["tags"][0]][lang] if post["tags"] else "Defence Tech",
            },
            {
                "@type": "BreadcrumbList",
                "itemListElement": [
                    {"@type": "ListItem", "position": 1, "name": ui["breadcrumb_home"], "item": home_item},
                    {"@type": "ListItem", "position": 2, "name": ui["breadcrumb_blog"], "item": absolute_url(lang, "/blog/")},
                    {"@type": "ListItem", "position": 3, "name": post["title"], "item": canon},
                ],
            },
        ],
    }
    title = f"{post['title']} — {ui['nav_blog']} — Fidesa"
    main = f"""      <main id="main" class="page-blog-post">
        <div class="container section__inner section__inner--narrow">
          <nav aria-label="Breadcrumb">
            <ol class="breadcrumb">
              <li><a href="{ui['home']}">{ui['breadcrumb_home']}</a></li>
              <li><a href="{ui['blog']}">{ui['breadcrumb_blog']}</a></li>
              <li aria-current="page">{html.escape(post['title'])}</li>
            </ol>
          </nav>
          <article class="blog-article">
            <h1 class="blog-article__title">{html.escape(post['title'])}</h1>
{byline_html(lang, post['author'], post['date'], prefix=prefix)}
            {tag_chips(lang, post['tags'])}
            <div class="blog-article__body">
{post['body_html']}
            </div>
{related_html}
            <p class="blog-back"><a href="{ui['blog']}">{ui['back_to_list']}</a></p>
          </article>
        </div>
      </main>"""
    write(
        out_dir / "index.html",
        page_shell(
            lang,
            depth,
            title,
            post["summary"],
            logical,
            main,
            schema,
            og_type="article",
        ),
    )


def main() -> None:
    for lang in ("uk", "en"):
        posts = load_posts(lang)
        assert len(posts) == 3, f"{lang}: expected 3 posts, got {len(posts)}"
        build_list(lang, posts)
        for tag_id in TAGS:
            build_tag(lang, tag_id, posts)
        for post in posts:
            build_post(lang, post, posts)
    print("blog build complete")


if __name__ == "__main__":
    main()
