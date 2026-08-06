# Focused search: find the BEST hometown-related dialogue for IELTS speaking
import json
import re

with open('data/modern-family.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# STRONG patterns - these almost always indicate real hometown content
STRONG = [
    (r"i\s+come\s+from\s+a\s+(small|little)\s+(village|town)", "come from village/town"),
    (r"grew\s+up\s+(in|on|near)\s+", "grew up in"),
    (r"from\s+the\s+farm\s+in", "from farm"),
    (r"from\s+a\s+small\s+(village|town|farm)", "from small village"),
    (r"my\s+(old\s+)?(hometown|home\s+town|neighborhood)", "my hometown"),
    (r"used\s+to\s+live\s+(down|in|near|on)", "used to live"),
    (r"old\s+apartment", "old apartment"),
    (r"old\s+neighborhood", "old neighborhood"),
    (r"in\s+colombia.*(family|grew|live|home|village|town|country)", "Colombia home"),
    (r"miss(ing)?\s+(home|it\s+there|colombia|missouri)", "missing home"),
    (r"homesick|home\s*sick", "homesick"),
    (r"when\s+i\s+was\s+a\s+kid.*(used\s+to|grew|live|play|remember)", "when I was a kid"),
    (r"childhood\s+(home|memories|neighborhood)", "childhood home"),
    (r"moved\s+(here|to|away|back)\s+", "moved"),
    (r"moving?\s+to\s+", "moving to"),
    (r"left\s+my\s+(hometown|home|village|town|country)", "left hometown"),
    (r"back\s+in\s+(colombia|missouri)", "back in homeland"),
    (r"my\s+family\s+is\s+from|my\s+family\s+(still)?\s+lives", "family from"),
    (r"the\s+house\s+i\s+grew\s+up", "childhood house"),
    (r"grew\s+up\s+there", "grew up there"),
    (r"small\s+town\s+", "small town"),
    (r"little\s+town\s+", "little town"),
    (r"i\s+remember\s+(growing|living|playing)\s+", "remember growing"),
    (r"that's\s+where\s+(i|we|you)\s+(grew|lived)", "that's where grew up"),
    (r"where\s+(i|we)\s+(was|were)\s+born", "where born"),
    (r"born\s+in\s+", "born in"),
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
            block_lines = lines[max(0, i-2):i+4]
            block_en = ' '.join(l.get('en', '') for l in block_lines)
            block_cn = ' '.join(l.get('cn', '') for l in block_lines)
            for pat, label in STRONG:
                if re.search(pat, block_en, re.IGNORECASE):
                    # Filter out noise
                    noise_words = ['prison', 'police', 'court', 'wallet', 'sex', 'prostitute']
                    if any(n in block_en.lower() for n in noise_words):
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

# Sort by source for review
unique.sort(key=lambda r: r['ep'])

print(f"Found {len(unique)} strong candidates\n")
for i, r in enumerate(unique):
    print(f"[{i+1}] {r['ep']} ({r['pattern']})")
    print(f"  EN: {r['en'][:200]}")
    print(f"  CN: {r['cn'][:150]}")
    print()
