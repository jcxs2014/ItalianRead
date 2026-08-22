#!/usr/bin/env python3
"""
Extract stories from First Italian Reader (Appelbaum)
Dual-language: Italian text + English translation.
Output: content/racconti/first_italian_reader/
"""

import zipfile, re, json
from pathlib import Path
from datetime import datetime

STORYBOOK = Path(__file__).parent.parent / "storybook"
OUTPUT = Path(__file__).parent.parent / "storybook" / "first_italian_reader"
OUTPUT.mkdir(exist_ok=True, parents=True)

epub_path = STORYBOOK / "first_italian_reader" / "First Italian reader a dual-language book (Appelbaum, Stanley) (Z-Library).epub"

if not epub_path.exists():
    print(f"Epub not found: {epub_path}")
    exit(1)

def get_text_by_id(html, elem_id):
    idx = html.find(f'id="{elem_id}"')
    if idx < 0:
        return ""
    chunk = html[idx:]
    # Get until next id= element
    next_id = re.search(r'id="([^"]+)"', chunk[10:])
    if next_id:
        block = chunk[:10 + next_id.start()]
    else:
        block = chunk
    text = re.sub(r'<[^>]+>', ' ', block)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

with zipfile.ZipFile(epub_path, 'r') as z:
    toc_content = z.read('OEBPS/toc.ncx').decode('utf-8', errors='ignore')
    nav_points = re.findall(r'<navPoint\s[^>]*>.*?<text>([^<]+)</text>.*?<content\s+src="([^"]+)"', toc_content, re.DOTALL)
    
    # Get spine order
    opf_content = z.read('OEBPS/9780486465357.opf').decode('utf-8', errors='ignore')
    items = re.findall(r'<item\s([^>]+)/>', opf_content)
    item_map = {}
    for item in items:
        href = re.search(r'href="([^"]+)"', item)
        id_ = re.search(r'id="([^"]+)"', item)
        if href and id_:
            item_map[id_.group(1)] = href.group(1)
    spine = re.findall(r'<itemref[^>]+idref="([^"]+)"', opf_content)
    spine_files = [item_map.get(s) for s in spine if s in item_map]
    
    stories = []
    story_idx = 0
    
    for label, src in nav_points:
        label = label.strip()
        src = src.strip()
        
        # Skip non-story entries
        skip = ['Cover', 'Title Page', 'Copyright', 'Preface', 'Contents', 'Introduction']
        if any(s.lower() in label.lower() for s in skip):
            continue
        
        # Parse: "1. Novellino / Storybook (ca. 1300): 3 novelle / 3 stories"
        # Extract author/origin and Italian title
        if ':' in label:
            parts = label.split(':')
            header = parts[0].strip()  # e.g., "1. Novellino / Storybook (ca. 1300)"
            it_en = parts[1].strip() if len(parts) > 1 else ""
        else:
            header = label
            it_en = ""
        
        # Parse author from header (e.g., "1. Novellino" or "Dante")
        author = header.split('.')[1].strip().split('/')[0].strip() if '.' in header else header
        
        # Parse anchor from src
        anchor = None
        base_file = src
        if '#' in src:
            base_file, anchor = src.split('#', 1)
        else:
            base_file = src
        
        # Find the actual HTML file in spine
        src_basename = base_file.split('/')[-1]
        html_file = None
        for sf in spine_files:
            if sf and src_basename in sf:
                html_file = 'OEBPS/' + sf
                break
        if not html_file:
            html_file = 'OEBPS/' + src
        
        try:
            html_content = z.read(html_file).decode('utf-8', errors='ignore')
        except:
            continue
        
        if anchor:
            text = get_text_by_id(html_content, anchor)
        else:
            # Get all text from file
            text = re.sub(r'<[^>]+>', ' ', html_content)
            text = re.sub(r'\s+', ' ', text).strip()
        
        if len(text) < 100:
            continue
        
        story_idx += 1
        idx_str = f"{story_idx:03d}"
        
        # Clean up label for slug
        clean_label = re.sub(r'[^\w\s]', '', label)
        clean_label = re.sub(r'\s+', '_', clean_label.strip())[:60]
        if not clean_label:
            clean_label = f"story_{idx_str}"
        
        filename = f"{idx_str}_{clean_label}.md"
        
        frontmatter = f"""---
title: "{label}"
lang: it
状态: 未读
难度: A2-B1
source: first_italian_reader
originalUrl: "epub: first_italian_reader/{epub_path.name}#{anchor or 'noid'}"
date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}
author: "{author}"
story_source: "First Italian Reader - A Dual-Language Book (Appelbaum)"
---

# {label}

**Author/Origin**: {author}

---

{text}
"""
        
        (OUTPUT / filename).write_text(frontmatter, encoding='utf-8')
        
        stories.append({
            'idx': idx_str,
            'title': label[:60],
            'author': author,
            'filename': filename,
            'words': len(text.split())
        })
    
    with open(OUTPUT / "index.json", 'w', encoding='utf-8') as f:
        json.dump({
            'source': 'first_italian_reader',
            'book': 'First Italian Reader - A Dual-Language Book (Appelbaum)',
            'total_stories': len(stories),
            'stories': stories
        }, f, ensure_ascii=False, indent=2)
    
    print(f"Extracted {len(stories)} stories -> {OUTPUT}/")
    for s in stories:
        print(f"  {s['idx']} {s['title'][:50]} ({s['words']} words)")
