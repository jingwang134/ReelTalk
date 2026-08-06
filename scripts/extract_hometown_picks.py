# Extract the best hometown-related dialogue blocks and generate replacement data
import json
import re

with open('data/modern-family.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

def find_block(ep_id, start_line_idx, end_line_idx):
    """Extract a block of consecutive lines from an episode."""
    for season, episodes in corpus.items():
        if not isinstance(episodes, dict):
            continue
        for eid, ep_data in episodes.items():
            if eid == ep_id:
                lines = ep_data.get('lines', [])
                block = lines[start_line_idx:end_line_idx]
                en = ' '.join(l.get('en', '') for l in block)
                cn = ' '.join(l.get('cn', '') for l in block)
                return en, cn
    return None, None

def search_pattern(ep_id, pattern, context_before=2, context_after=4):
    """Find a pattern in an episode and return the block around it."""
    for season, episodes in corpus.items():
        if not isinstance(episodes, dict):
            continue
        for eid, ep_data in episodes.items():
            if eid == ep_id:
                lines = ep_data.get('lines', [])
                for i, l in enumerate(lines):
                    if re.search(pattern, l.get('en', ''), re.IGNORECASE):
                        start = max(0, i - context_before)
                        end = min(len(lines), i + context_after + 1)
                        block = lines[start:end]
                        en = ' '.join(l.get('en', '') for l in block)
                        cn = ' '.join(l.get('cn', '') for l in block)
                        return en, cn
    return None, None

# The 8 selected hometown segments
# (episode, search pattern, function label)
SELECTED = [
    # 1. Gloria describing her hometown (village vs city)
    ("s01e01", r"I\s+come\s+from\s+a\s+small\s+village", "开场破题"),
    # 2. Cam describing farm hometown vs Mitchell's city
    ("s01e03", r"from\s+the\s+farm\s+in\s+Missouri", "开场破题"),
    # 3. Mitchell on Denver hometown food
    ("s01e06", r"I'm\s+from\s+Denver", "表达观点"),
    # 4. Gloria on her old apartment / past neighborhood
    ("s01e18", r"used\s+to\s+live\s+down\s+here", "表达观点"),
    # 5. Cam on childhood memories and growing up near the waterslide
    ("s01e12", r"grew\s+up\s+one\s+mile\s+away", "举例说明"),
    # 6. Gloria remembering her village in Colombia (beauty pageant context)
    ("s04e06", r"When\s+I\s+was\s+young", "举例说明"),
    # 7. Comparing city mouse vs country mouse / different worlds
    ("s01e03", r"big\s+city\s+mouse", "比较对比"),
    # 8. Gloria: it's still part of me - remembering your roots
    ("s01e18", r"It's\s+still\s+part\s+of\s+me", "总结收束"),
]

for ep, pattern, func in SELECTED:
    en, cn = search_pattern(ep, pattern, context_before=2, context_after=5)
    if en:
        print(f"=== {ep} [{func}] ===")
        print(f"EN: {en}")
        print(f"CN: {cn}")
        print()
    else:
        print(f"=== {ep} [{func}] === NOT FOUND")
        print()
