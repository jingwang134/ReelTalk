# Deep search: find REAL hometown discussions in Modern Family corpus
import json
import re

with open('data/modern-family.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# Precise content patterns - actual discussion of hometown/childhood home
PRECISE_PATTERNS = [
    (r"(grew|grow)\s+up\s+(in|on|near)", "grew up in"),
    (r"growing\s+up,\s+", "growing up,"),
    (r"where\s+((i|we|she|he)\s+)?(was|were)\s+born", "where born"),
    (r"born\s+in\s+", "born in"),
    (r"born\s+and\s+raised", "born and raised"),
    (r"raised\s+(in|on)", "raised in"),
    (r"my\s+hometown", "my hometown"),
    (r"our\s+hometown", "our hometown"),
    (r"back\s+in\s+(colombia|missouri|california|florida|idaho|new\s+york|the\s+midwest|the\s+south)", "back in [region]"),
    (r"in\s+colombia", "in Colombia"),
    (r"when\s+i\s+was\s+a\s+kid,\s+(i|we)\s+(used\s+to|lived|grew)", "when I was a kid"),
    (r"used\s+to\s+live\s+(in|on|near|down)", "used to live in"),
    (r"used\s+to\s+play\s+", "used to play"),
    (r"old\s+apartment", "old apartment"),
    (r"old\s+house", "old house"),
    (r"old\s+neighborhood", "old neighborhood"),
    (r"the\s+neighborhood\s+(i|we)\s+grew", "neighborhood grew up"),
    (r"miss\s+it\s+(there|back)", "miss it there"),
    (r"miss\s+my\s+", "miss my"),
    (r"moving?\s+(to|from|back|here)", "moving"),
    (r"moved\s+(to|from|here|back|away)", "moved"),
    (r"left\s+(my|our|home|the)", "left home"),
    (r"small\s+town", "small town"),
    (r"little\s+town", "little town"),
    (r"farm\s+", "farm"),
    (r"rural\s+", "rural"),
    (r"countryside", "countryside"),
    (r"suburb", "suburb"),
    (r"i\s+come\s+from\s+", "I come from"),
    (r"we\s+come\s+from\s+", "we come from"),
    (r"my\s+family\s+is\s+from\s+", "my family is from"),
    (r"from\s+(missouri|colombia|florida|idaho|california|new\s+york|chicago|texas)", "from [state]"),
    (r"homesick", "homesick"),
    (r"home\s+sick", "home sick"),
    (r"childhood\s+home", "childhood home"),
    (r"family\s+home", "family home"),
    (r"my\s+parents'?\s+(house|home)", "parents' house"),
    (r"my\s+grandparents'?\s+", "grandparents'"),
    (r"the\s+house\s+(i|we)\s+grew", "house grew up"),
    (r"memories\s+of\s+", "memories of"),
    (r"remember\s+(growing|playing|living)", "remember"),
    (r"that's\s+where\s+", "that's where"),
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
            block_lines = lines[max(0, i-1):i+4]
            block_en = ' '.join(l.get('en', '') for l in block_lines)
            block_cn = ' '.join(l.get('cn', '') for l in block_lines)
            for pat, label in PRECISE_PATTERNS:
                if re.search(pat, block_en, re.IGNORECASE):
                    # Skip noise patterns
                    noise = ['back in prison', 'back in the day', 'back in a sec', 'back in the hospital']
                    if any(n in block_en.lower() for n in noise):
                        break
                    results.append({
                        'ep': ep_id,
                        'pattern': label,
                        'en': block_en,
                        'cn': block_cn,
                    })
                    break

# Deduplicate
seen = set()
unique = []
for r in results:
    key = r['en'][:120].lower()
    if key not in seen:
        seen.add(key)
        unique.append(r)

print(f"Found {len(unique)} relevant blocks\n")
for i, r in enumerate(unique):
    print(f"[{i+1}] {r['ep']} (pattern: {r['pattern']})")
    print(f"  EN: {r['en'][:220]}")
    print(f"  CN: {r['cn'][:180]}")
    print()
