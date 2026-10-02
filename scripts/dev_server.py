#!/usr/bin/env python3
"""Local preview server that mimics production hosting behaviour.

Unlike `python3 -m http.server`, this handler:
  * serves 404.html with a real 404 status for unknown paths;
  * honours the legacy /en/* -> /* 301 redirects on the EN site
    (matching public/en-site/_redirects and .htaccess);
  * disables caching so edits show up on reload.

Usage:
  python3 scripts/dev_server.py --site uk --port 8080
  python3 scripts/dev_server.py --site en --port 8081
"""

from __future__ import annotations

import argparse
import functools
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DOCROOTS = {
    "uk": ROOT / "public" / "uk-site",
    "en": ROOT / "public" / "en-site",
}


class SiteHandler(SimpleHTTPRequestHandler):
    site = "uk"

    def end_headers(self) -> None:
        self.send_header("Cache-Control", "no-store, must-revalidate")
        super().end_headers()

    def do_GET(self) -> None:  # noqa: N802
        if self._maybe_redirect():
            return
        super().do_GET()

    def do_HEAD(self) -> None:  # noqa: N802
        if self._maybe_redirect():
            return
        super().do_HEAD()

    def _maybe_redirect(self) -> bool:
        """EN site: /en and /en/<rest> are legacy paths, 301 to the root."""
        if self.site != "en":
            return False
        path = self.path.split("?", 1)[0]
        if path == "/en" or path == "/en/":
            target = "/"
        elif path.startswith("/en/"):
            target = "/" + path[len("/en/"):]
        else:
            return False
        self.send_response(301)
        self.send_header("Location", target)
        self.end_headers()
        return True

    def send_error(self, code, message=None, explain=None):  # type: ignore[override]
        """Serve the site's own 404.html instead of the stdlib error page."""
        if code == 404:
            page = Path(self.directory) / "404.html"
            if page.is_file():
                body = page.read_bytes()
                self.send_response(404)
                self.send_header("Content-Type", "text/html; charset=utf-8")
                self.send_header("Content-Length", str(len(body)))
                self.end_headers()
                if self.command != "HEAD":
                    self.wfile.write(body)
                return
        super().send_error(code, message, explain)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--site", choices=sorted(DOCROOTS), required=True)
    parser.add_argument("--port", type=int, required=True)
    args = parser.parse_args()

    docroot = DOCROOTS[args.site]
    if not docroot.is_dir():
        raise SystemExit(f"Missing docroot: {docroot}")

    SiteHandler.site = args.site
    handler = functools.partial(SiteHandler, directory=str(docroot))

    print(f"{args.site}-site -> http://localhost:{args.port}/  ({docroot})")
    ThreadingHTTPServer(("127.0.0.1", args.port), handler).serve_forever()


if __name__ == "__main__":
    main()
