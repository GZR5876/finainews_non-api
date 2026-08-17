#!/usr/bin/env python3
"""
Fetch Google News RSS results for a search query.

Usage:
    python scripts/fetch_google_news_rss.py --query "finance AI" --after 2026-08-01
    python scripts/fetch_google_news_rss.py --query "CFO AI agents adoption" --limit 15

Prints a JSON array of {title, link, source, published} to stdout, newest
first as returned by Google News. `published` is an ISO date (YYYY-MM-DD)
derived from the feed's pubDate, or null if it could not be parsed.
"""
import argparse
import json
import urllib.parse
import urllib.request
import xml.etree.ElementTree as ET
from datetime import datetime, timezone

FEED_URL = "https://news.google.com/rss/search"


def fetch_feed(query: str, hl: str = "en-US", gl: str = "US", ceid: str = "US:en") -> bytes:
    params = {"q": query, "hl": hl, "gl": gl, "ceid": ceid}
    url = f"{FEED_URL}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=20) as resp:
        return resp.read()


def parse_pubdate(raw: str):
    try:
        dt = datetime.strptime(raw, "%a, %d %b %Y %H:%M:%S %Z")
        return dt.replace(tzinfo=timezone.utc)
    except ValueError:
        return None


def parse_items(xml_bytes: bytes) -> list[dict]:
    root = ET.fromstring(xml_bytes)
    items = []
    for item in root.findall("./channel/item"):
        title = (item.findtext("title") or "").strip()
        link = (item.findtext("link") or "").strip()
        pub_raw = (item.findtext("pubDate") or "").strip()
        source_el = item.find("source")
        source_name = source_el.text.strip() if source_el is not None and source_el.text else None
        pub_dt = parse_pubdate(pub_raw)

        # Google News titles are formatted "Headline - Source Name"; strip
        # the trailing source suffix so `title` is the plain headline.
        headline = title
        if source_name and headline.endswith(f" - {source_name}"):
            headline = headline[: -(len(source_name) + 3)].strip()

        items.append({
            "title": headline,
            "link": link,
            "source": source_name,
            "published": pub_dt.strftime("%Y-%m-%d") if pub_dt else None,
        })
    return items


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--query", default="finance AI",
                         help="Search query; Google News search operators allowed (e.g. after:2026-08-01)")
    parser.add_argument("--after", default=None,
                         help="YYYY-MM-DD; drop items published before this date")
    parser.add_argument("--limit", type=int, default=20, help="Max items to return")
    args = parser.parse_args()

    xml_bytes = fetch_feed(args.query)
    items = parse_items(xml_bytes)

    if args.after:
        items = [i for i in items if i["published"] is None or i["published"] >= args.after]

    items = items[: args.limit]
    print(json.dumps(items, indent=2))


if __name__ == "__main__":
    main()
