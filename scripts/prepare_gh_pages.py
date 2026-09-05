#!/usr/bin/env python3
"""Prepare public/uk-site for GitHub Pages project URL (/<repo>/).

Root-absolute paths (/assets/, /js/, /vacancies/, …) break on
https://<user>.github.io/<repo>/ — rewrite them to include the base path.
"""

from __future__ import annotations

import argparse
import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT / "public" / "uk-site"
OUT = ROOT / "dist" / "gh-pages"

# href="/…", src="/…", etc. Skip protocol-relative //.
ATTR_ABS_RE = re.compile(r"""=(["'])(/(?!/)[^"']*)\1""")
# JS / HTML string literals for static assets
ASSET_STR_RE = re.compile(r"""(["'])(/(?:assets|js)/[^"']*)\1""")


def rewrite(text: str, base: str) -> str:
    base = "/" + base.strip("/")

    def attr_sub(m: re.Match[str]) -> str:
        q, path = m.group(1), m.group(2)
        if path == base or path.startswith(base + "/"):
            return m.group(0)
        return f"={q}{base}{path}{q}"

    def asset_sub(m: re.Match[str]) -> str:
        q, path = m.group(1), m.group(2)
        if path.startswith(base + "/"):
            return m.group(0)
        return f"{q}{base}{path}{q}"

    text = ATTR_ABS_RE.sub(attr_sub, text)
    text = ASSET_STR_RE.sub(asset_sub, text)
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--base",
        default="fidesa",
        help="GitHub Pages project base path (repo name), default: fidesa",
    )
    parser.add_argument(
        "--src",
        type=Path,
        default=SRC,
        help="Source document root (default: public/uk-site)",
    )
    parser.add_argument(
        "--out",
        type=Path,
        default=OUT,
        help="Output directory (default: dist/gh-pages)",
    )
    args = parser.parse_args()

    if not args.src.is_dir():
        print(f"error: source not found: {args.src}", file=sys.stderr)
        return 1

    if args.out.exists():
        shutil.rmtree(args.out)
    shutil.copytree(args.src, args.out)

    n = 0
    for path in args.out.rglob("*"):
        if not path.is_file():
            continue
        if path.suffix.lower() not in {".html", ".js", ".css", ".svg", ".json", ".txt", ".xml"}:
            continue
        try:
            original = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = rewrite(original, args.base)
        if updated != original:
            path.write_text(updated, encoding="utf-8")
            n += 1

    print(f"Prepared {args.out} (base=/{args.base.strip('/')}/; rewrote {n} files)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
