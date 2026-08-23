#!/usr/bin/env python3
"""
Fetch articles from Il Post using the official API wrapper.
Requires: pip install ilpost-api-wrapper
"""

import json
import sys
from datetime import datetime, timezone
from pathlib import Path
import argparse

try:
    from ilpost import IlPostClient, SortOrder, ContentType, DateRange
except ImportError:
    print("Error: ilpost-api-wrapper not installed. Run: pip install ilpost-api-wrapper")
    sys.exit(1)


def fetch_articles(
    query: str = "",
    category: str = None,
    date_range: DateRange = DateRange.PAST_30_DAYS,
    max_results: int = 20,
    fetch_content: bool = True,
) -> list:
    """Fetch articles from Il Post."""
    client = IlPostClient(timeout=30)

    if category:
        results = client.search_articles(
            query or "",
            category=category,
            date_range=date_range,
            hits=max_results,
            fetch_content=fetch_content,
        )
    else:
        results = client.search(
            query or "",
            date_range=date_range,
            content_type=ContentType.ARTICLES,
            hits=max_results,
            fetch_content=fetch_content,
        )

    articles = []
    for doc in results.docs:
        article = {
            'title': doc.title,
            'url': doc.link,
            'timestamp': doc.timestamp,
            'category': doc.category,
            'summary': doc.summary,
            'is_paywalled': doc.is_paywalled,
            'source': 'Il Post',
            'fetched_at': datetime.now(timezone.utc).isoformat(),
        }
        if doc.content:
            article['content'] = doc.content

        articles.append(article)

    return articles


def main():
    parser = argparse.ArgumentParser(description="Fetch Il Post articles")
    parser.add_argument('--query', default='', help='Search query')
    parser.add_argument('--category', help='Category (politica, mondo, tecnologia, etc.)')
    parser.add_argument('--days', type=int, default=30, help='Days to look back')
    parser.add_argument('--max', type=int, default=20, help='Max results')
    parser.add_argument('--no-content', action='store_true', help='Skip full content')
    parser.add_argument('--output', help='Output JSON file')
    args = parser.parse_args()

    date_map = {
        7: DateRange.PAST_30_DAYS,  # Use PAST_30 for any small number
        30: DateRange.PAST_30_DAYS,
        365: DateRange.PAST_YEAR,
    }
    date_range = date_map.get(args.days, DateRange.PAST_30_DAYS)

    print(f"Fetching Il Post articles...")
    articles = fetch_articles(
        query=args.query,
        category=args.category,
        date_range=date_range,
        max_results=args.max,
        fetch_content=not args.no_content,
    )

    print(f"Fetched {len(articles)} articles")
    for a in articles[:3]:
        print(f"  - {a['title'][:60]}...")
        if a.get('content'):
            print(f"    Content: {len(a['content'])} chars")

    if args.output and articles:
        output_path = Path(args.output)
        output_path.parent.mkdir(parents=True, exist_ok=True)
        with open(output_path, 'w', encoding='utf-8') as f:
            json.dump(articles, f, ensure_ascii=False, indent=2)
        print(f"Saved to {args.output}")

    return articles


if __name__ == '__main__':
    main()
