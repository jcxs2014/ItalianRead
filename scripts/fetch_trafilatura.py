#!/usr/bin/env python3
"""
Fetch articles from Italian news websites using trafilatura.
Supports full article text extraction from URLs.
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import argparse

try:
    import trafilatura
except ImportError:
    print("Error: trafilatura not installed. Run: pip install trafilatura")
    sys.exit(1)


def fetch_article(url: str) -> dict:
    """Fetch a single article and extract text using trafilatura."""
    downloaded = trafilatura.fetch_url(url)
    if not downloaded:
        return None

    result = trafilatura.bare_extraction(
        downloaded,
        url=url,
        include_comments=False,
        include_images=False,
    )
    return result


def fetch_from_rss(feed_url: str, source: str, max_articles: int = 10) -> list:
    """Fetch articles from an RSS feed using trafilatura."""
    feed = trafilatura.fetch_feed(feed_url, max_articles)
    if not feed:
        return []

    articles = []
    for entry in feed:
        url = entry.get('url') or entry.get('link')
        if not url:
            continue

        article = fetch_article(url)
        if article:
            article['source'] = source
            article['fetched_at'] = datetime.now(timezone.utc).isoformat()
            articles.append(article)

    return articles


def main():
    parser = argparse.ArgumentParser(description="Fetch Italian articles using trafilatura")
    parser.add_argument('--url', help='Single article URL to fetch')
    parser.add_argument('--feed', help='RSS feed URL to fetch from')
    parser.add_argument('--source', default='unknown', help='Source name')
    parser.add_argument('--max', type=int, default=10, help='Max articles from feed')
    parser.add_argument('--output', help='Output JSON file')
    args = parser.parse_args()

    articles = []

    if args.url:
        article = fetch_article(args.url)
        if article:
            article['source'] = args.source
            articles.append(article)
            print(f"Fetched: {article.get('title', 'No title')}")

    elif args.feed:
        articles = fetch_from_rss(args.feed, args.source, args.max)
        print(f"Fetched {len(articles)} articles from feed")

    else:
        print("Error: specify --url or --feed")
        sys.exit(1)

    if args.output and articles:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"Saved to {args.output}")

    return articles


if __name__ == '__main__':
    main()
