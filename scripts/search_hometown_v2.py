# Search Modern Family structured corpus for REAL hometown-related dialogue
import json
import re

with open('data/modern-family.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# Patterns that indicate REAL hometown-related content (content words, not just function words)
HOMETOWN_PATTERNS = [
    (r"grew\s+up", "grew up"),
    (r"growing\s+up", "growing up"),
    (r"where\s+i\s+was\s+born", "where I was born"),
    (r"born\s+and\s+raised", "born and raised"),
    (r"raised\s+in", "raised in"),
    (r"back\s+home", "back home"),
    (r"miss\s+(my\s+)?home", "miss home"),
    (r"my\s+hometown", "my hometown"),
    (r"home\s+town", "home town"),
    (r"the\s+(old\s+)?neighborhood", "neighborhood"),
    (r"when\s+i\s+was\s+a\s+kid", "when I was a kid"),
    (r"used\s+to\s+live", "used to live"),
    (r"moved?\s+from", "moved from"),
    (r"moved?\s+here", "moved here"),
    (r"where\s+i'?m\s+from", "where I'm from"),
    (r"in\s+colombia", "in Colombia"),
    (r"my\s+country", "my country"),
    (r"our\s+old\s+house", "our old house"),
    (r"remember\s+(growing|living|playing|being)", "remember growing up"),
    (r"little\s+town", "little town"),
    (r"small\s+town", "small town"),
    (r"from\s+the\s+(south|midwest|east|north)", "from the region"),
    (r"back\s+in\s+", "back in"),
    (r"when\s+we\s+first\s+moved", "when we first moved"),
    (r"first\s+(moved|moved\s+here)", "first moved here"),
    (r"this\s+used\s+to\s+be", "this used to be"),
    (r"that\s+used\s+to\s+be", "that used to be"),
    (r"home\s+for\s+", "home for"),
    (r"feel(s)?\s+like\s+home", "feels like home"),
    (r"homesick", "homesick"),
    (r"hometown", "hometown"),
]

def search_corpus():
    results = []
    for season, episodes in corpus.items():
        if not isinstance(episodes, dict):
            continue
        for ep_id, ep_data in episodes.items():
            if not isinstance(ep_data, dict):
                continue
            lines = ep_data.get('lines', [])
            # Join consecutive lines into blocks of 3-5
            for i in range(len(lines)):
                block_lines = lines[max(0, i-2):i+4]
                block_en = ' '.join(l.get('en', '') for l in block_lines)
                for pat, label in HOMETOWN_PATTERNS:
                    if re.search(pat, block_en, re.IGNORECASE):
                        results.append({
                            'ep': ep_id,
                            'pattern': label,
                            'block': block_en,
                            'lines': block_lines,
                            'index': i,
                        })
                        break  # one pattern per block
    
    # Deduplicate by first 100 chars
    seen = set()
    unique = []
    for r in results:
        key = r['block'][:100].lower()
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return unique

results = search_corpus()
print(f"Found {len(results)} hometown-related blocks\n")

# Group by pattern
by_pattern = {}
for r in results:
    by_pattern.setdefault(r['pattern'], []).append(r)

for pat, items in sorted(by_pattern.items(), key=lambda x: -len(x[1])):
    print(f"=== {pat} ({len(items)} blocks) ===")
    for r in items[:6]:
        print(f"  [{r['ep']}] {r['block'][:200]}")
        print()
