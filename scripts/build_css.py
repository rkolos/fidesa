#!/usr/bin/env python3
"""Concatenate src/styles/*.css → assets/css/site.css (one render-blocking file).

Source files stay modular for editing; run this after CSS changes, then refresh pages
that already point at assets/css/site.css (or run rewrite via --link-html).

Usage:
  python3 scripts/build_css.py
  python3 scripts/build_css.py --link-html   # also rewrite public/**/*.html + build_blog.py template
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
STYLES = ROOT / "src" / "styles"
OUT = ROOT / "assets" / "css" / "site.css"

ORDER = (
    "tokens.css",
    "base.css",
    "layout.css",
    "components.css",
    "pages.css",
)

# Paths in source CSS are relative to src/styles/; rewrite for assets/css/
FONT_URL_RE = re.compile(
    r"""url\(\s*(['"]?)(?:\.\./)+assets/fonts/([^)'"]+)\1\s*\)"""
)

STYLESHEET_BLOCK_RE = re.compile(
    r"""[ \t]*<link rel="stylesheet" href="([^"]*)src/styles/tokens\.css" />\s*\n"""
    r"""[ \t]*<link rel="stylesheet" href="[^"]*src/styles/base\.css" />\s*\n"""
    r"""[ \t]*<link rel="stylesheet" href="[^"]*src/styles/layout\.css" />\s*\n"""
    r"""[ \t]*<link rel="stylesheet" href="[^"]*src/styles/components\.css" />\s*\n"""
    r"""[ \t]*<link rel="stylesheet" href="[^"]*src/styles/pages\.css" />""",
    re.MULTILINE,
)

BLOG_TEMPLATE_BLOCK = '''    <link rel="stylesheet" href="{prefix}src/styles/tokens.css" />
    <link rel="stylesheet" href="{prefix}src/styles/base.css" />
    <link rel="stylesheet" href="{prefix}src/styles/layout.css" />
    <link rel="stylesheet" href="{prefix}src/styles/components.css" />
    <link rel="stylesheet" href="{prefix}src/styles/pages.css" />'''

BLOG_TEMPLATE_ONE = '''    <link rel="stylesheet" href="{prefix}assets/css/site.css" />'''


def minify_css(css: str) -> str:
    """Light minify: drop comments and excess whitespace.

    Do not strip spaces around ``+`` / ``-`` — CSS ``calc()`` requires them
    (e.g. ``calc(4rem + env(...))`` is valid; ``calc(4rem+env(...))`` is not).
    """
    css = re.sub(r"/\*.*?\*/", "", css, flags=re.DOTALL)
    css = re.sub(r"\s+", " ", css)
    css = re.sub(r"\s*([{}:;,~])\s*", r"\1", css)
    # Keep spaces around > (child) and + (sibling) combinators via prior collapse only.
    css = re.sub(r";}", "}", css)
    return css.strip() + "\n"


def write_stamp() -> Path:
    """Record source mtimes so stale bundles are easy to detect."""
    stamp = OUT.parent / ".stamp"
    lines = []
    for name in ORDER:
        path = STYLES / name
        lines.append(f"{name}\t{path.stat().st_mtime_ns}\t{path.stat().st_size}")
    stamp.write_text("\n".join(lines) + "\n", encoding="utf-8")
    return stamp


def build() -> Path:
    parts: list[str] = []
    for name in ORDER:
        path = STYLES / name
        if not path.is_file():
            raise SystemExit(f"Missing stylesheet: {path}")
        raw = path.read_text(encoding="utf-8")
        rewritten = FONT_URL_RE.sub(r"url(\1../fonts/\2\1)", raw)
        parts.append(f"/* --- {name} --- */\n{rewritten}")
    bundled = "\n".join(parts)
    minified = minify_css(bundled)
    OUT.parent.mkdir(parents=True, exist_ok=True)
    OUT.write_text(minified, encoding="utf-8")
    write_stamp()
    return OUT


def link_html() -> int:
    count = 0
    for html_path in (ROOT / "public").rglob("*.html"):
        text = html_path.read_text(encoding="utf-8")
        if "src/styles/tokens.css" not in text:
            continue

        def repl(m: re.Match[str]) -> str:
            prefix = m.group(1)
            return f'    <link rel="stylesheet" href="{prefix}assets/css/site.css" />'

        new_text, n = STYLESHEET_BLOCK_RE.subn(repl, text)
        if n == 0:
            print(f"WARN: pattern miss: {html_path}", file=sys.stderr)
            continue
        html_path.write_text(new_text, encoding="utf-8")
        count += n
    return count


def link_blog_builder() -> bool:
    blog = ROOT / "scripts" / "build_blog.py"
    text = blog.read_text(encoding="utf-8")
    if BLOG_TEMPLATE_BLOCK not in text:
        if "assets/css/site.css" in text:
            return False
        raise SystemExit("build_blog.py stylesheet block not found")
    blog.write_text(text.replace(BLOG_TEMPLATE_BLOCK, BLOG_TEMPLATE_ONE), encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--link-html",
        action="store_true",
        help="Rewrite public HTML + build_blog template to the bundled CSS",
    )
    args = parser.parse_args()

    out = build()
    raw = sum((STYLES / n).stat().st_size for n in ORDER)
    print(f"Wrote {out.relative_to(ROOT)} ({out.stat().st_size} bytes; sources {raw} bytes)")

    if args.link_html:
        n = link_html()
        blog = link_blog_builder()
        print(f"Linked {n} HTML files; build_blog.py updated={blog}")


if __name__ == "__main__":
    main()
