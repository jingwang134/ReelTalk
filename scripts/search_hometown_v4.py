# Search specific high-value content in later seasons
import json
import re

with open('data/modern-family.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# Targeted searches for specific high-quality content
TARGETS = [
    (r"grew\s+up\s+(on|in)\s+a\s+(farm|ranch)", "grew up on farm"),
    (r"i'm\s+from\s+", "I'm from"),
    (r"i\s+am\s+from\s+", "I am from"),
    (r"we're\s+from\s+", "we're from"),
    (r"we\s+are\s+from\s+", "we are from"),
    (r"from\s+colombia", "from Colombia"),
    (r"from\s+missouri", "from Missouri"),
    (r"from\s+florida", "from Florida"),
    (r"from\s+idaho", "from Idaho"),
    (r"from\s+the\s+(midwest|south|east\s+coast)", "from region"),
    (r"where\s+are\s+you\s+from", "where are you from"),
    (r"where\s+do\s+you\s+come\s+from", "where do you come from"),
    (r"my\s+home\s+is\s+in\s+", "my home is in"),
    (r"home\s+is\s+", "home is"),
    (r"this\s+is\s+my\s+home", "this is my home"),
    (r"feel(s|ing)?\s+at\s+home", "feel at home"),
    (r"make(s)?\s+you\s+feel\s+at\s+home", "make you feel at home"),
    (r"what\s+(was|is)\s+(your|my)\s+(hometown|home\s+town)\s+like", "what hometown like"),
    (r"remember\s+our\s+(old|first)\s+house", "remember old house"),
    (r"our\s+(old|first)\s+house", "our old house"),
    (r"the\s+(apartment|house)\s+we\s+(used\s+to|lived\s+in)", "apartment we lived"),
    (r"when\s+we\s+moved\s+", "when we moved"),
    (r"when\s+i\s+moved\s+", "when I moved"),
    (r"after\s+(we|i)\s+moved\s+", "after we moved"),
    (r"before\s+we\s+moved\s+", "before we moved"),
    (r"came\s+to\s+(america|the\s+states|california|los\s+angeles)", "came to America"),
    (r"first\s+came\s+to\s+", "first came to"),
    (r"came\s+here\s+", "came here"),
    (r"from\s+the\s+old\s+(country|neighborhood)", "from old country"),
    (r"back\s+in\s+the\s+(day|old\s+days)", "back in the day"),
    (r"this\s+(street|block|area)\s+", "this street"),
    (r"grew\s+up\s+around\s+", "grew up around"),
    (r"grew\s+up\s+there", "grew up there"),
    (r"raised\s+us", "raised us"),
    (r"raised\s+me", "raised me"),
    (r"raise(d)?\s+my\s+(kids|children|family)", "raise my kids"),
    (r"the\s+(kids|children)\s+(grew\s+up|were\s+born)", "kids grew up"),
]

results = []
for season, episodes in corpus.items():
    if not isinstance(episodes, dict):
        continue
    for ep_id, ep_data in episodes.items():
        if not isinstance(ep_data, dict):
            continue
        lines = ep_data.get('lines', [])
        for i in range(len(lines)):
            block_lines = lines[max(0, i-2):i+5]
            block_en = ' '.join(l.get('en', '') for l in block_lines)
            block_cn = ' '.join(l.get('cn', '') for l in block_lines)
            for pat, label in TARGETS:
                if re.search(pat, block_en, re.IGNORECASE):
                    noise = ['prison', 'court', 'police', 'trial', 'jury']
                    if any(n in block_en.lower() for n in noise):
                        break
                    results.append({
                        'ep': ep_id,
                        'pattern': label,
                        'en': block_en.strip(),
                        'cn': block_cn.strip(),
                    })
                    break

# Deduplicate
seen = set()
unique = []
for r in results:
    key = r['en'][:100].lower()
    if key not in seen:
        seen.add(key)
        unique.append(r)

unique.sort(key=lambda r: r['ep'])
print(f"Found {len(unique)} candidates\n")
for i, r in enumerate(unique):
    print(f"[{i+1}] {r['ep']} ({r['pattern']})")
    print(f"  EN: {r['en'][:200]}")
    print(f"  CN: {r['cn'][:120]}")
    print()
