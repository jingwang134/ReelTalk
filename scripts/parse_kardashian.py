# Parse Kardashians S01 bilingual subtitles into structured JSON
import os
import re
import json

SRC_DIR = r"C:\Users\15869\Desktop\文件\WJ\en\k-s01-bilingual"
OUT = r"data\kardashian-s01.json"

def parse_file(path):
    """Parse one subtitle file into a list of {en, cn, time} dicts."""
    entries = []
    with open(path, 'r', encoding='utf-8-sig') as f:
        content = f.read()
    
    # Split by blocks: 【N】time \n EN: ... \n 中：... 
    blocks = re.split(r'【\d+】', content)
    for block in blocks:
        block = block.strip()
        if not block:
            continue
        lines = block.split('\n')
        time = ''
        en = ''
        cn = ''
        for line in lines:
            line = line.strip()
            if '-->' in line:
                time = line
            elif line.startswith('EN:') or line.startswith('EN：'):
                en = line[3:].strip()
            elif line.startswith('中：') or line.startswith('中:'):
                cn = line[2:].strip()
        if en:
            entries.append({'en': en, 'cn': cn, 'time': time})
    return entries

def get_episode_num(fname):
    """Extract episode number from filename."""
    m = re.search(r'S01E(\d+)', fname, re.IGNORECASE)
    if m:
        return int(m.group(1))
    # Try bare number files like "5.中英台本.txt"
    m2 = re.match(r'^(\d+)\.', fname)
    if m2:
        return int(m2.group(1))
    return None

def main():
    corpus = {}
    total_lines = 0
    for fname in sorted(os.listdir(SRC_DIR)):
        if not fname.endswith('.txt'):
            continue
        ep_num = get_episode_num(fname)
        fpath = os.path.join(SRC_DIR, fname)
        entries = parse_file(fpath)
        ep_id = f's01e{ep_num:02d}' if ep_num else fname.replace('.txt', '')
        corpus[ep_id] = {
            'title': fname.replace('.txt', ''),
            'lines': entries,
        }
        total_lines += len(entries)
        print(f"{ep_id}: {len(entries)} lines ({fname})")
    
    with open(OUT, 'w', encoding='utf-8') as f:
        json.dump(corpus, f, ensure_ascii=False, indent=1)
    print(f"\nTotal: {len(corpus)} episodes, {total_lines} lines -> {OUT}")

    # Quick content sample
    first_ep = list(corpus.values())[0]
    print("\n=== Sample lines ===")
    for l in first_ep['lines'][:5]:
        print(f"EN: {l['en'][:70]}")
        print(f"CN: {l['cn'][:50]}")
        print()

if __name__ == '__main__':
    main()
