#!/usr/bin/env python3
"""
Extract stories from Penguin Parallel Texts - Short Stories in Italian
Each chapter: [Italian heading + text] → [English heading + text]
Output: content/racconti/penguin_parallel/
"""

import zipfile, re, json
from pathlib import Path
from datetime import datetime

STORYBOOK = Path(__file__).parent.parent / "storybook"
OUTPUT = Path(__file__).parent.parent / "storybook" / "penguin_parallel"
OUTPUT.mkdir(exist_ok=True, parents=True)

epub_path = STORYBOOK / "penguin_parallel" / "Short Stories in Italian_ New Penguin Parallel Texts.epub"

if not epub_path.exists():
    print(f"Epub not found: {epub_path}")
    exit(1)

def extract_story_text(html, start_anchor_id):
    """Extract story text from anchor element until next heading"""
    # Find the element with this ID
    idx = html.find(f'id="{start_anchor_id}"')
    if idx < 0:
        return ""
    
    # Find the end of this element block (next heading or end of content)
    # Look for the next <h1, <h2, <h3 tag after our position
    chunk = html[idx:]
    end_pattern = r'<h[1-6][^>]*id="'
    end_match = re.search(end_pattern, chunk[200:])  # skip first 200 to not match current
    if end_match:
        block = chunk[:200 + end_match.start()]
    else:
        block = chunk
    
    # Clean up: remove tags, get text
    text = re.sub(r'<style[^>]*>.*?</style>', ' ', block, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

with zipfile.ZipFile(epub_path, 'r') as z:
    toc_content = z.read('ShortStoriesinItalian/toc.ncx').decode('utf-8', errors='ignore')
    nav_points = re.findall(r'<navPoint\s[^>]*>.*?<text>([^<]+)</text>.*?<content\s+src="([^"]+)"', toc_content, re.DOTALL)
    
    chapters = {}
    for label, src in nav_points:
        label = label.strip()
        src = src.strip()
        if '#' not in src:
            continue
        base, anchor = src.split('#', 1)
        cn = re.search(r'chapter(\d+)', base)
        if not cn:
            continue
        cnum = cn.group(1)
        if cnum not in chapters:
            chapters[cnum] = {'base': base, 'items': []}
        chapters[cnum]['items'].append({'label': label, 'anchor': anchor})
    
    stories = []
    story_idx = 0
    
    for cn, ch in sorted(chapters.items()):
        items = ch['items']
        if len(items) < 2:
            continue
        
        # Find Italian and English anchor IDs
        italian_anchor = None
        english_anchor = None
        for item in items:
            label = item['label']
            if re.search(r'[àèéìòù&#8217;&#8216;]', label, re.IGNORECASE) or \
               re.match(r"^(L'|Il |La |Un |I )", label):
                italian_anchor = item['anchor']
                break
        
        for item in reversed(items):
            label = item['label']
            if not re.search(r'[àèéìòù&#8217;&#8216;]', label, re.IGNORECASE) and \
               not re.match(r"^(L'|Il |La |Un |I )", label):
                english_anchor = item['anchor']
                break
        
        if not italian_anchor:
            continue
        
        base_path = 'ShortStoriesinItalian/' + ch['base']
        try:
            html = z.read(base_path).decode('utf-8', errors='ignore')
        except:
            continue
        
        italian_text = extract_story_text(html, italian_anchor)
        english_text = extract_story_text(html, english_anchor) if english_anchor else ""
        
        if not italian_text or len(italian_text) < 100:
            continue
        
        # Get title
        italian_label = items[0]['label'].replace('&#8217;', "'").replace('&#8216;', "'")
        english_label = items[-1]['label'] if len(items) > 1 else italian_label
        
        # Parse author
        author = "Unknown"
        for item in items:
            label = item['label']
            if ':' in label and not re.search(r'[àèéìòù]', label):
                parts = label.split(':')
                if len(parts) >= 2:
                    potential = parts[0].strip()
                    if 3 < len(potential) < 50 and potential[0].isupper():
                        author = potential
                        break
        
        story_idx += 1
        idx_str = f"{story_idx:03d}"
        slug = re.sub(r'[^\w\s]', '', italian_label.lower())
        slug = re.sub(r'\s+', '_', slug.strip())[:60]
        if not slug:
            slug = f"story_{idx_str}"
        
        filename = f"{idx_str}_{slug}.md"
        
        frontmatter = f"""---
title: "{italian_label}"
lang: it
状态: 未读
难度: B1-B2
source: penguin_parallel
originalUrl: "epub: penguin_parallel/{epub_path.name}#chapter{cn}"
date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}
author: "{author}"
story_source: "Short Stories in Italian - New Penguin Parallel Texts"
---

# {italian_label}

**Author**: {author}
**English title**: {english_label}

---

## Italiano

{italian_text}

---

## English

{english_text if english_text.strip() else "(translation omitted)"}
"""
        
        (OUTPUT / filename).write_text(frontmatter, encoding='utf-8')
        
        stories.append({
            'idx': idx_str,
            'title': italian_label,
            'author': author,
            'filename': filename,
            'words': len(italian_text.split())
        })
    
    with open(OUTPUT / "index.json", 'w', encoding='utf-8') as f:
        json.dump({
            'source': 'penguin_parallel',
            'book': 'Short Stories in Italian - New Penguin Parallel Texts',
            'total_stories': len(stories),
            'stories': stories
        }, f, ensure_ascii=False, indent=2)
    
    print(f"Extracted {len(stories)} stories -> {OUTPUT}/")
    for s in stories:
        print(f"  {s['idx']} {s['title'][:50]} ({s['words']} words)")
