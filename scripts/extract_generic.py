#!/usr/bin/env python3
"""
Generic epub extractor - extracts stories from any epub.
Reads TOC and spine, extracts text by section.
Usage: python3 extract_generic.py <source_dir> [source_name]
"""

import sys, zipfile, re, json
from pathlib import Path
from datetime import datetime

def extract_text_from_html(content):
    text = re.sub(r'<style[^>]*>.*?</style>', ' ', content, flags=re.DOTALL)
    text = re.sub(r'<script[^>]*>.*?</script>', ' ', text, flags=re.DOTALL)
    text = re.sub(r'<[^>]+>', ' ', text)
    text = re.sub(r'\s+', ' ', text).strip()
    return text

def get_text_by_anchor(html, anchor_id):
    idx = html.find(f'id="{anchor_id}"')
    if idx < 0:
        return ""
    chunk = html[idx:]
    end_match = re.search(r'<[a-z]+\s+[^>]*id="', chunk[10:])
    if end_match:
        block = chunk[:10 + end_match.start()]
    else:
        block = chunk
    return extract_text_from_html(block)

def get_text_block(html, start_id):
    idx = html.find(f'id="{start_id}"')
    if idx < 0:
        return ""
    chunk = html[idx:]
    end_match = re.search(r'<h[1-6][^>]*>', chunk[5:])
    if end_match:
        block = chunk[:end_match.start()]
    else:
        block = chunk
    return extract_text_from_html(block)

def parse_toc_ncx(z, toc_path):
    """Parse NCX TOC file"""
    try:
        content = z.read(toc_path).decode('utf-8', errors='ignore')
    except:
        return []
    
    entries = []
    nav_points = re.findall(r'<navPoint\s[^>]*>(.*?)</navPoint>', content, re.DOTALL)
    for np in nav_points:
        label_match = re.search(r'<text[^>]*>([^<]+)</text>', np)
        src_match = re.search(r'<content\s+src="([^"]+)"', np)
        if label_match and src_match:
            label = label_match.group(1).strip()
            src = src_match.group(1).strip()
            if len(label) > 2 and len(label) < 150:
                entries.append({'label': label, 'src': src})
    return entries

def parse_nav_xhtml(z, nav_path):
    """Parse HTML-based NAV file (EPUB 3)"""
    try:
        content = z.read(nav_path).decode('utf-8', errors='ignore')
    except:
        return []
    
    entries = []
    links = re.findall(r'<a[^>]+href="([^"]+)"[^>]*>([^<]+)</a>', content)
    for href, label in links:
        label = label.strip()
        if len(label) > 2 and len(label) < 150:
            entries.append({'label': label, 'src': href})
    return entries

def get_manifest_and_spine(z, opf_path):
    """Get manifest item_map and spine order from OPF"""
    try:
        content = z.read(opf_path).decode('utf-8', errors='ignore')
    except:
        return {}, []
    
    # Parse manifest items
    items = re.findall(r'<item\s([^>]+)/>', content)
    item_map = {}
    for item in items:
        href_m = re.search(r'href="([^"]+)"', item)
        id_m = re.search(r'id="([^"]+)"', item)
        if href_m and id_m:
            item_map[id_m.group(1)] = href_m.group(1)
    
    # Parse spine
    spine = re.findall(r'<itemref[^>]+idref="([^"]+)"', content)
    spine_files = []
    for sid in spine:
        if sid in item_map:
            # Resolve relative path from OPF location
            opf_dir = '/'.join(opf_path.split('/')[:-1])
            href = item_map[sid]
            if '/' not in href and opf_dir:
                full_path = opf_dir + '/' + href
            elif '/' not in href:
                full_path = href
            else:
                full_path = href
            spine_files.append(full_path)
    
    return item_map, spine_files

def resolve_href(opf_path, href):
    """Resolve href relative to OPF location"""
    opf_dir = '/'.join(opf_path.split('/')[:-1])
    if '/' not in href and opf_dir:
        return opf_dir + '/' + href
    elif '/' not in href:
        return href
    return href

def extract_epub(epub_path, source_name=None):
    """Extract stories from an epub file"""
    epub_path = Path(epub_path)
    if source_name is None:
        source_name = epub_path.stem[:50]
    
    output_dir = epub_path.parent
    epub_name = epub_path.name
    
    with zipfile.ZipFile(epub_path, 'r') as z:
        all_files = z.namelist()
        
        # Find OPF
        opf_files = [f for f in all_files if f.endswith('.opf')]
        if not opf_files:
            print(f"No OPF found in {epub_path.name}")
            return 0
        opf_path = opf_files[0]
        
        # Find TOC
        toc_files = [f for f in all_files if f.endswith(('toc.ncx', 'toc.xhtml', 'nav.xhtml', 'nav.html'))]
        
        # Parse manifest and spine
        item_map, spine_files = get_manifest_and_spine(z, opf_path)
        
        # Parse TOC
        toc_entries = []
        for tf in toc_files:
            if tf.endswith('.ncx'):
                toc_entries = parse_toc_ncx(z, tf)
                break
            else:
                toc_entries = parse_nav_xhtml(z, tf)
                if toc_entries:
                    break
        
        if not toc_entries:
            print(f"No TOC found in {epub_path.name}")
            # Fall back to spine order
            toc_entries = [{'label': f'Chapter {i+1}', 'src': f} for i, f in enumerate(spine_files[:20])]
        
        # Extract each section
        stories = []
        story_idx = 0
        
        for entry in toc_entries:
            label = entry['label']
            src = entry['src']
            
            # Skip obvious non-content
            skip = ['cover', 'copyright', 'title page', 'contents', 'introduction', 
                    'about', 'preface', 'acknowledgements', 'notes', 'index', 'bibliography']
            if any(s in label.lower() for s in skip):
                continue
            
            # Resolve src to file path
            if '#' in src:
                base_src, anchor = src.split('#', 1)
            else:
                base_src, anchor = src, None
            
            resolved = resolve_href(opf_path, base_src)
            
            try:
                html = z.read(resolved).decode('utf-8', errors='ignore')
            except:
                # Try finding in spine
                try:
                    html = z.read(base_src).decode('utf-8', errors='ignore')
                except:
                    continue
            
            if anchor:
                text = get_text_by_anchor(html, anchor) if anchor else extract_text_from_html(html)
                if not text:
                    text = get_text_block(html, anchor)
            else:
                text = extract_text_from_html(html)
            
            if len(text) < 50:
                continue
            
            story_idx += 1
            idx_str = f"{story_idx:03d}"
            
            # Create slug
            slug = re.sub(r'[^\w\s]', '', label.lower())
            slug = re.sub(r'\s+', '_', slug.strip())[:50]
            if not slug:
                slug = f"story_{idx_str}"
            
            filename = f"{idx_str}_{slug}.md"
            
            frontmatter = f"""---
title: "{label}"
lang: it
状态: 未读
难度: A2-B1
source: "{source_name}"
originalUrl: "epub: {epub_name}#{src}"
date: {datetime.now().strftime('%a, %d %b %Y %H:%M:%S +0000')}
story_source: "{epub_name}"
---

# {label}

---

{text}
"""
            
            (output_dir / filename).write_text(frontmatter, encoding='utf-8')
            stories.append({
                'idx': idx_str,
                'title': label[:60],
                'filename': filename,
                'words': len(text.split())
            })
        
        # Write index
        if stories:
            index = {
                'source': source_name,
                'book': epub_name,
                'total_stories': len(stories),
                'stories': stories
            }
            with open(output_dir / "index.json", 'w', encoding='utf-8') as f:
                json.dump(index, f, ensure_ascii=False, indent=2)
        
        return len(stories)

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("Usage: python3 extract_generic.py <source_dir> [source_name]")
        sys.exit(1)
    
    source_dir = Path(sys.argv[1])
    source_name = sys.argv[2] if len(sys.argv) > 2 else source_dir.name
    
    epub_files = list(source_dir.glob('*.epub'))
    if not epub_files:
        print(f"No epub files in {source_dir}")
        sys.exit(1)
    
    total = 0
    for epub in epub_files:
        print(f"Extracting {epub.name}...")
        count = extract_epub(epub, source_name)
        print(f"  -> {count} stories")
        total += count
    
    print(f"Total: {total} stories extracted to {source_dir}/")
