#!/usr/bin/env python3
"""Build CSS bundle and sync static assets into both site docroots.

Order:
  1. scripts/build_css.py  → assets/css/site.css
  2. scripts/sync_site_static.py → public/*/assets + public/*/js (+ HTML absolute paths)

Usage:
  python3 scripts/build_static.py
  python3 scripts/build_static.py --no-rewrite   # after paths already absolute
"""

from __future__ import annotations

import argparse
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def run(script: str, extra: list[str] | None = None) -> None:
    cmd = [sys.executable, str(ROOT / "scripts" / script)]
    if extra:
        cmd.extend(extra)
    print("+", " ".join(cmd))
    subprocess.check_call(cmd, cwd=ROOT)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--no-rewrite",
        action="store_true",
        help="Pass through to sync_site_static (skip HTML rewrite)",
    )
    args = parser.parse_args()
    run("build_css.py")
    sync_args = ["--no-rewrite"] if args.no_rewrite else None
    run("sync_site_static.py", sync_args)
    print("OK: CSS built and static assets synced")


if __name__ == "__main__":
    main()
