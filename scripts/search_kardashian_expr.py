# Search Kardashians corpus for transferable expressions (phrase-centered)
import json
import re

with open('data/kardashian-s01.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# Candidate expression patterns (transferable to IELTS speaking)
PATTERNS = [
    # 开场破题
    (r"i\s+feel\s+like", "I feel like...", "开场破题"),
    (r"i\s+was\s+like", "I was like...", "开场破题"),
    (r"to\s+be\s+honest", "to be honest", "开场破题"),
    (r"at\s+the\s+end\s+of\s+the\s+day", "at the end of the day", "总结收束"),
    (r"i\s+literally", "I literally...", "表达观点"),
    (r"my\s+biggest\s+focus", "my biggest focus is", "表达观点"),
    (r"i\s+can'?t\s+believe", "I can't believe", "表达观点"),
    (r"this\s+is\s+my\s+last\s+chance", "this is my last chance", "表达观点"),
    (r"clean\s+slate", "clean slate", "表达观点"),
    (r"just\s+between\s+", "just between us", "表达观点"),
    (r"keeping\s+it\s+to\s+ourselves", "keep it to ourselves", "表达观点"),
    (r"i\s+don'?t\s+think\s+i'?m\s+gonna", "I don't think I'm gonna", "表达观点"),
    (r"makes\s+me\s+", "it makes me...", "表达观点"),
    (r"i\s+guess\s+", "I guess", "表达观点"),
    (r"i\s+would\s+say", "I would say", "表达观点"),
    (r"one\s+of\s+my", "one of my...", "举例说明"),
    (r"for\s+example|for\s+instance", "for example", "举例说明"),
    (r"like\s+when\s+", "like when...", "举例说明"),
    (r"it's\s+like", "it's like", "举例说明"),
    (r"compared\s+to", "compared to", "比较对比"),
    (r"different\s+from", "different from", "比较对比"),
    (r"much\s+more", "much more...", "比较对比"),
    (r"i\s+used\s+to", "I used to...", "比较对比"),
    (r"in\s+the\s+past", "in the past", "比较对比"),
    (r"at\s+this\s+point", "at this point", "总结收束"),
    (r"that'?s\s+what", "that's what...", "总结收束"),
    (r"so\s+at\s+the\s+end", "at the end", "总结收束"),
]

results = []
for ep, data in corpus.items():
    for i, l in enumerate(data['lines']):
        en = l['en']
        cn = l['cn']
        for pat, label, func in PATTERNS:
            if re.search(pat, en, re.IGNORECASE):
                # Skip profanity-heavy lines
                if re.search(r'\bfuck\w*\b|\bshit\b|\b bitch\b|\bdick\b|\bass\b', en, re.I):
                    break
                # Extract the sentence containing the pattern
                sentences = re.split(r'(?<=[.!?])\s+', en)
                match_sent = next((s for s in sentences if re.search(pat, s, re.I)), en)
                # Clean
                match_sent = match_sent.strip()
                if len(match_sent) > 12 and len(match_sent) < 200:
                    results.append({
                        'ep': ep,
                        'pattern': label,
                        'func': func,
                        'sentence': match_sent,
                        'cn': cn,
                    })
                break

# Deduplicate by sentence
seen = set()
unique = []
for r in results:
    key = r['sentence'][:60].lower()
    if key not in seen:
        seen.add(key)
        unique.append(r)

print(f"Found {len(unique)} candidates\n")
# Group by pattern
by_pat = {}
for r in unique:
    by_pat.setdefault(r['pattern'], []).append(r)
for pat, items in sorted(by_pat.items(), key=lambda x: -len(x[1])):
    print(f"=== {pat} ({len(items)}) ===")
    for r in items[:3]:
        print(f"  [{r['ep']}] {r['sentence'][:130]}")
    print()
