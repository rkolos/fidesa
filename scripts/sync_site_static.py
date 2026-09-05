#!/usr/bin/env python3
"""Copy shared static assets into each deployable site docroot.

Copies:
  assets/          → public/{uk-site,en-site}/assets/
  src/js/*.js      → public/{uk-site,en-site}/js/

Also rewrites HTML under public/ and scripts/build_blog.py to root-absolute paths:
  …/assets/… → /assets/…
  …/src/js/… → /js/…

Usage:
  python3 scripts/sync_site_static.py
  python3 scripts/sync_site_static.py --no-rewrite
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ASSETS = ROOT / "assets"
JS_SRC = ROOT / "src" / "js"
SITES = (ROOT / "public" / "uk-site", ROOT / "public" / "en-site")

REL_ASSETS_RE = re.compile(r"""(?:(?:\.\./)+|\{prefix\})assets/""")
REL_JS_RE = re.compile(r"""(?:(?:\.\./)+|\{prefix\})src/js/""")


def sync_tree(src: Path, dest: Path) -> None:
    if dest.exists():
        shutil.rmtree(dest)
    shutil.copytree(src, dest)


def sync_js(dest_js: Path) -> int:
    dest_js.mkdir(parents=True, exist_ok=True)
    count = 0
    for path in sorted(JS_SRC.glob("*.js")):
        shutil.copy2(path, dest_js / path.name)
        count += 1
    return count


def rewrite_text(text: str) -> str:
    text = REL_ASSETS_RE.sub("/assets/", text)
    text = REL_JS_RE.sub("/js/", text)
    return text


def rewrite_html() -> int:
    n = 0
    for html_path in (ROOT / "public").rglob("*.html"):
        original = html_path.read_text(encoding="utf-8")
        updated = rewrite_text(original)
        if updated != original:
            html_path.write_text(updated, encoding="utf-8")
            n += 1
    return n


def rewrite_build_blog() -> bool:
    blog = ROOT / "scripts" / "build_blog.py"
    original = blog.read_text(encoding="utf-8")
    updated = rewrite_text(original)
    old_photo = 'src = f"{prefix}{author[\'photo\']}"'
    new_photo = (
        'src = author["photo"] if str(author.get("photo", "")).startswith('
        '("http://", "https://", "/")) else "/" + str(author["photo"]).lstrip("/")'
    )
    if old_photo in updated:
        updated = updated.replace(old_photo, new_photo)
    if updated == original:
        return False
    blog.write_text(updated, encoding="utf-8")
    return True


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-rewrite",
        action="store_true",
        help="Only copy files; do not rewrite HTML / build_blog paths",
    )
    args = parser.parse_args()

    if not ASSETS.is_dir():
        raise SystemExit(f"Missing assets dir: {ASSETS}")
    if not JS_SRC.is_dir():
        raise SystemExit(f"Missing js dir: {JS_SRC}")

    for site in SITES:
        if not site.is_dir():
            print(f"WARN: skip missing site {site}", file=sys.stderr)
            continue
        sync_tree(ASSETS, site / "assets")
        js_count = sync_js(site / "js")
        print(f"Synced {site.name}: assets/ + {js_count} js files")

    # Repo-root /js for monorepo-root previews (alongside existing /assets).
    root_js = sync_js(ROOT / "js")
    print(f"Synced repo-root js/ ({root_js} files)")

    if not args.no_rewrite:
        html_n = rewrite_html()
        blog = rewrite_build_blog()
        print(f"Rewrote {html_n} HTML files; build_blog.py updated={blog}")


if __name__ == "__main__":
    main()
