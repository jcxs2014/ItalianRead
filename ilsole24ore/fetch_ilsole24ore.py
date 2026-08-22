#!/usr/bin/env python3
"""
Fetch articles from Il Sole 24 Ore RSS feed.
Il Sole 24 Ore - 经济/商业新闻，难度 B2
RSS: https://www.ilsole24ore.com/rss/italia.xml
"""

import json
import re
import sys
from datetime import datetime
from pathlib import Path

import feedparser

FEED_URL = "https://www.ilsole24ore.com/rss/italia.xml"
SOURCE = "ilsole24ore"
MAX_ARTICLES = 10


def to_filename(title: str) -> str:
    title = re.sub(r"[^\w\s]", "", title)
    title = re.sub(r"\s+", "_", title.strip())
    return title.lower()


def fetch_articles():
    print(f"Fetching from {FEED_URL}...")
    feed = feedparser.parse(FEED_URL)

    if not feed.entries:
        print("No entries found!")
        sys.exit(1)

    today = datetime.utcnow()
    date_str = today.strftime("%Y%m%d")
    weekday = today.strftime("%A").lower()
    output_dir = Path(__file__).parent / f"{date_str}_{weekday}"
    output_dir.mkdir(exist_ok=True)

    articles = []
    for i, entry in enumerate(feed.entries[:MAX_ARTICLES], 1):
        title = entry.get("title", "No title")
        link = entry.get("link", "")
        description = entry.get("description", "")

        description = re.sub(r"<[^>]+>", "", description)
        description = description.strip()

        slug = to_filename(title)
        filename = f"{i:02d}_{slug}.src.md"

        content = f"""---
lang: it
source: {SOURCE}
url: {link}
date: {entry.get("published", today.isoformat())}
---

# {title}

{description}
"""

        filepath = output_dir / filename
        filepath.write_text(content, encoding="utf-8")
        print(f"  [{i}] {title[:60]}...")

        articles.append({
            "idx": i,
            "title": title,
            "link": link,
            "slug": slug,
            "description": description[:200],
        })

    index_path = output_dir / "index.json"
    with open(index_path, "w", encoding="utf-8") as f:
        json.dump({
            "source": SOURCE,
            "date": today.isoformat(),
            "articles": articles,
        }, f, ensure_ascii=False, indent=2)

    print(f"\nSaved {len(articles)} articles to {output_dir}/")
    print(f"Index: {index_path}")


if __name__ == "__main__":
    fetch_articles()
