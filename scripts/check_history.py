#!/usr/bin/env python3
"""
Check whether a URL has already appeared in a previously circulated newsletter.

Scans two locations for source URLs:
  1. data/archive/*.html  -- past newsletters uploaded by the user
  2. data/issues/*/newsletter.html  -- newsletters rendered in the current repo

Usage:
    python scripts/check_history.py --url "https://example.com/article"

Prints "SEEN (filename)" if the URL was found, "NEW" otherwise.
"""
import argparse
import re
from pathlib import Path

ROOT = Path(__file__).parent.parent
ARCHIVE_DIR = ROOT / "data" / "archive"
ISSUES_DIR = ROOT / "data" / "issues"

# Match any href value in an <a> tag
_HREF_RE = re.compile(r'href=["\']([^"\']+)["\']', re.IGNORECASE)


def extract_urls(html_text: str) -> set[str]:
    """Return all href URLs found in an HTML file, normalised (trailing slash stripped)."""
    urls = set()
    for m in _HREF_RE.finditer(html_text):
        url = m.group(1).strip().rstrip("/")
        if url.startswith("http"):
            urls.add(url)
    return urls


def build_seen_index() -> dict[str, str]:
    """
    Return a dict mapping normalised URL -> source filename for every URL
    found in any archived or previously rendered newsletter.
    """
    seen: dict[str, str] = {}

    # 1. Uploaded past newsletters in data/archive/
    if ARCHIVE_DIR.exists():
        for html_file in sorted(ARCHIVE_DIR.glob("*.html")):
            for url in extract_urls(html_file.read_text(errors="replace")):
                if url not in seen:
                    seen[url] = html_file.name

    # 2. Rendered newsletters from previous issues in this repo
    if ISSUES_DIR.exists():
        for newsletter in sorted(ISSUES_DIR.glob("*/newsletter.html")):
            week_label = newsletter.parent.name
            for url in extract_urls(newsletter.read_text(errors="replace")):
                if url not in seen:
                    seen[url] = f"newsletter ({week_label})"

    return seen


def normalise(url: str) -> str:
    return url.strip().rstrip("/")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--url", required=True)
    args = parser.parse_args()

    candidate = normalise(args.url)
    seen = build_seen_index()

    if candidate in seen:
        print(f"SEEN ({seen[candidate]})")
    else:
        print("NEW")


if __name__ == "__main__":
    main()
