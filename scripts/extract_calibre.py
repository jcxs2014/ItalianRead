#!/usr/bin/env python3
"""
Extract stories from epub using Calibre's ebook-convert.
Calibre converts epub to clean TXT preserving structure.
Then we parse the TXT to extract individual stories.
Usage: python3 extract_calibre.py <source_dir> [source_name]
"""

import sys, subprocess, re, json
from pathlib import Path
from datetime import datetime

CALIBRE = "/Applications/calibre.app/Contents/MacOS/ebook-convert"

def convert_epub(epub_path, txt_path):
    """Convert epub to txt using Calibre"""
    cmd = [
        CALIBRE, str(epub_path), str(txt_path),
        "--input-encoding", "utf-8"
    ]
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)
    return result.returncode == 0

def parse_stories_from_txt(txt_path, source_name):
    """Parse stories from Calibre-generated TXT"""
    content = txt_path.read_text(encoding='utf-8')
    lines = content.split('\n')
    
    stories = []
    story_idx = 0
    current_story = None
    italian_text = []
    english_text = []
    in_italian = False
    in_english = False
    
    i = 0
    while i < len(lines):
        line = lines[i].strip()
        
        # Detect author line (all caps, Italian names)
        if re.match(r'^[A-ZÀÈÉÌÒÙ][A-ZÀÈÉÌÒÙ\s\,\-\']+$', line) and len(line) > 3 and len(line) < 60:
            # Save previous story if exists
            if current_story:
                it_text = '\n'.join(italian_text).strip()
                en_text = '\n'.join(english_text).strip()
                
                if it_text:
                    slug = re.sub(r'[^\w\s]', '', current_story['title'].lower())
                    slug = re.sub(r'\s+', '_', slug.strip())[:50]
                    idx_str = f"{story_idx:03d}"
                    filename = f"{idx_str}_{slug}.md"
                    
                    frontmatter = f"""---
title: "{current_story['title']}"
lang: it
状态: 未读
难度: B2-C1
source: "{source_name}"
originalUrl: "epub: {current_story['epub']}"
date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}
author: "{current_story['author']}"
story_source: "{current_story['epub']}"
---

# {current_story['title']}

**Author**: {current_story['author']}

---

## Italiano

{it_text}

---

## English

{en_text if en_text else "(translation omitted)"}
"""
                    
                    (txt_path.parent / filename).write_text(frontmatter, encoding='utf-8')
                    stories.append({
                        'idx': idx_str,
                        'title': current_story['title'],
                        'author': current_story['author'],
                        'filename': filename,
                        'words': len(it_text.split())
                    })
            
            # Start new story
            author = line
            story_idx += 1
            current_story = {'author': author, 'title': '', 'epub': txt_path.stem + '.epub'}
            italian_text = []
            english_text = []
            in_italian = False
            in_english = False
            i += 1
            continue
        
        # Detect Italian title (usually first non-empty line after author, or line with specific patterns)
        if current_story and not current_story['title'] and line and len(line) > 2:
            # Skip special markers
            if line in ['* * *', 'Contents', 'A Note on the Citation']:
                i += 1
                continue
            
            # This might be the Italian title
            current_story['title'] = line
            in_italian = True
            in_english = False
            i += 1
            continue
        
        # Detect English translation section
        if current_story and current_story['title']:
            # Check for English title marker (often followed by "Translated by")
            if 'Translated by' in line or 'translated by' in line.lower():
                in_english = True
                in_italian = False
                i += 1
                continue
            
            # Skip page markers
            if re.match(r'^\* \* \*$', line) or line.startswith('Page '):
                i += 1
                continue
            
            # Collect text
            if in_italian and line and len(line) > 10:
                italian_text.append(line)
            elif in_english and line and len(line) > 10:
                english_text.append(line)
        
        i += 1
    
    # Save last story
    if current_story and italian_text:
        it_text = '\n'.join(italian_text).strip()
        en_text = '\n'.join(english_text).strip()
        
        slug = re.sub(r'[^\w\s]', '', current_story['title'].lower())
        slug = re.sub(r'\s+', '_', slug.strip())[:50]
        idx_str = f"{story_idx:03d}"
        filename = f"{idx_str}_{slug}.md"
        
        frontmatter = f"""---
title: "{current_story['title']}"
lang: it
状态: 未读
难度: B2-C1
source: "{source_name}"
originalUrl: "epub: {current_story['epub']}"
date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}
author: "{current_story['author']}"
story_source: "{current_story['epub']}"
---

# {current_story['title']}

**Author**: {current_story['author']}

---

## Italiano

{it_text}

---

## English

{en_text if en_text else "(translation omitted)"}
"""
        
        (txt_path.parent / filename).write_text(frontmatter, encoding='utf-8')
        stories.append({
            'idx': idx_str,
            'title': current_story['title'],
            'author': current_story['author'],
            'filename': filename,
            'words': len(it_text.split())
        })
    
    return stories

def extract_epub(epub_path, source_name=None):
    """Extract stories from a single epub using Calibre"""
    epub_path = Path(epub_path)
    if source_name is None:
        source_name = epub_path.stem[:50]
    
    txt_path = epub_path.parent / f"{epub_path.stem}.txt"
    
    print(f"Converting {epub_path.name}...")
    if not convert_epub(epub_path, txt_path):
        print(f"  Conversion failed")
        return []
    
    print(f"  Converted, parsing stories...")
    stories = parse_stories_from_txt(txt_path, source_name)
    
    # Write index
    if stories:
        index = {
            'source': source_name,
            'book': epub_path.name,
            'total_stories': len(stories),
            'stories': stories
        }
        with open(txt_path.parent / "index.json", 'w', encoding='utf-8') as f:
            json.dump(index, f, ensure_ascii=False, indent=2)
    
    return stories

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 extract_calibre.py <source_dir> [source_name]")
        sys.exit(1)
    
    source_dir = Path(sys.argv[1])
    source_name = sys.argv[2] if len(sys.argv) > 2 else source_dir.name
    
    epub_files = list(source_dir.glob('*.epub'))
    if not epub_files:
        print(f"No epub files in {source_dir}")
        sys.exit(1)
    
    total = 0
    for epub in epub_files:
        count = len(extract_epub(epub, source_name))
        print(f"  -> {count} stories")
        total += count
    
    print(f"Total: {total} stories extracted to {source_dir}/")
