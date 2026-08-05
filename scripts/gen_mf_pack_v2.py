"""
生成两个文件：
1. mf-analysis.js — 预计算的风格分析（几KB，嵌入HTML）
2. mf-corpus.js — 完整语料（4.7MB，外部加载）
"""
import json
import re
from pathlib import Path
from collections import Counter

DATA_DIR = Path(r"C:\Users\15869\WorkBuddy\2026-08-05-10-43-07\data")

with open(DATA_DIR / 'modern-family-compact.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# ===== 聚合分析 =====
all_texts = []
for sk in sorted(corpus.keys()):
    for ek in sorted(corpus[sk].keys()):
        all_texts.append(corpus[sk][ek]['text'])

full_text = ' '.join(all_texts)

STOP_WORDS = set("the a an and or but in on at to for of with by from as is was are were am be been have has had do does did will would can could shall should may might I you he she it we they me him her us them my your his its our their this that these those so if when where how all about up out down just then now here there very too not no".split())

DISCOURSE_MARKERS = [
    'you know', 'i mean', 'like', 'honestly', 'literally', 'basically',
    'actually', 'obviously', 'seriously', 'technically', 'frankly',
    'look', 'listen', 'right', 'okay', 'well', 'so', 'anyway',
    'at the end of the day', 'the thing is', 'i guess', 'kind of', 'sort of',
    'i feel like', 'i think', 'bible', 'not gonna lie', 'to be honest',
]

TONE_PATTERNS = {
    'enthusiastic': ['amazing', 'incredible', 'love', 'awesome', 'fantastic', 'great', 'wonderful', 'best', 'perfect', 'obsessed'],
    'self_deprecating': ['stupid', 'idiot', 'mess', 'terrible', 'embarrassing', 'awkward', 'weird', 'fail', 'worst'],
    'sarcastic': ['really', 'wow', 'great', 'nice', 'sure', 'obviously', 'of course'],
    'warm': ['love', 'family', 'together', 'home', 'care', 'sweet', 'honey', 'kids', 'proud', 'happy', 'you know'],
    'dramatic': ['never', 'always', 'worst', 'best', 'everything', 'nothing', 'disaster', 'literally', 'absolutely'],
    'deadpan': ['okay', 'fine', 'whatever', 'sure', 'alright', 'cool', 'nice']
}

words = re.findall(r"[a-zA-Z']+", full_text.lower())
sentences = re.split(r'[.!?]+', full_text)
sentences = [s.strip() for s in sentences if s.strip()]

content_words = [w for w in words if w not in STOP_WORDS and len(w) > 1]
word_freq = Counter(content_words)

bigrams = [' '.join(content_words[i:i+2]) for i in range(len(content_words)-1)]
bi_freq = Counter(bigrams)

trigrams = [' '.join(content_words[i:i+3]) for i in range(len(content_words)-2)]
tri_freq = Counter(trigrams)

openers = [' '.join(s.strip().split()[:3]).lower() for s in sentences if s.strip().split()]
opener_freq = Counter(openers)

text_lower = full_text.lower()
markers = [m for m in DISCOURSE_MARKERS if m in text_lower]

sent_len = [len(s.split()) for s in sentences]
avg_sent_len = sum(sent_len) / len(sent_len) if sent_len else 0

contraction_count = len(re.findall(r"\b\w+'\w+\b", full_text))
contraction_rate = (contraction_count / len(words) * 100) if words else 0
complex_rate = (len([w for w in words if len(w) > 7 and w not in STOP_WORDS]) / len(words) * 100) if words else 0
formality = max(1, min(10, round(10 - contraction_rate * 3 + complex_rate * 2)))

tone_scores = {}
for tone, kw_list in TONE_PATTERNS.items():
    count = sum(full_text.lower().count(f' {kw} ') for kw in kw_list)
    tone_scores[tone] = count
best_tone = max(tone_scores, key=tone_scores.get)
intensity = min(100, tone_scores[best_tone] * 5)

excl_count = full_text.count('!')
q_count = full_text.count('?')
excl_rate = (excl_count / len(sentences) * 100) if sentences else 0
q_rate = (q_count / len(sentences) * 100) if sentences else 0

analysis = {
    'topWords': [{'word': w, 'count': c} for w, c in word_freq.most_common(30)],
    'topBigrams': [{'phrase': b, 'count': c} for b, c in bi_freq.most_common(30) if c >= 5],
    'topTrigrams': [{'phrase': t, 'count': c} for t, c in tri_freq.most_common(30) if c >= 3],
    'topOpeners': [{'phrase': o, 'count': c} for o, c in opener_freq.most_common(20)],
    'discourseMarkers': markers[:30],
    'avgSentLen': round(avg_sent_len, 1),
    'maxSentLen': max(sent_len),
    'minSentLen': min(sent_len),
    'totalWords': len(words),
    'totalSentences': len(sentences),
    'formality': formality,
    'primaryTone': {'tone': best_tone, 'intensity': intensity},
    'allTones': [{'tone': t, 'score': s} for t, s in sorted(tone_scores.items(), key=lambda x: -x[1])[:4]],
    'exclamationCount': excl_count,
    'questionCount': q_count,
    'exclamationRate': round(excl_rate, 1),
    'questionRate': round(q_rate, 1),
    'contractionRate': round(contraction_rate, 1),
    'complexWordRate': round(complex_rate, 1),
    'sigExpr': [t for t, c in tri_freq.most_common(10) if c >= 10],
}

# ===== 文件1: 分析数据（嵌入HTML） =====
analysis_js = f"window.__MF_ANALYSIS__ = {json.dumps(analysis, ensure_ascii=False)};"
with open(DATA_DIR / 'mf-analysis.js', 'w', encoding='utf-8') as f:
    f.write(analysis_js)
print(f"✅ mf-analysis.js: {len(analysis_js)} bytes (embed in HTML)")

# ===== 文件2: 完整语料（外部加载） =====
season_corpus = {}
for sk in sorted(corpus.keys()):
    season_text = ' '.join(corpus[sk][ek]['text'] for ek in sorted(corpus[sk].keys()))
    season_corpus[sk] = {
        'title': f'Modern Family S{int(sk[1:]):02d}',
        'text': season_text,
        'w': len(season_text.split()),
        'eps': len(corpus[sk])
    }

corpus_js = f"window.__MF_CORPUS__ = {json.dumps(season_corpus, ensure_ascii=False)};"
with open(DATA_DIR / 'mf-corpus.js', 'w', encoding='utf-8') as f:
    f.write(corpus_js)
size_mb = (DATA_DIR / 'mf-corpus.js').stat().st_size / 1024 / 1024
print(f"✅ mf-corpus.js: {size_mb:.1f} MB (external, load on demand)")

# ===== 统计 =====
print(f"\n📊 Analysis summary:")
print(f"  Tone: {best_tone} ({intensity}%)")
print(f"  Formality: {formality}/10 | Avg sent len: {avg_sent_len:.1f} words")
print(f"  Top words: {', '.join(w['word'] for w in analysis['topWords'][:12])}")
print(f"  Sig expr: {analysis['sigExpr'][:5]}")
print(f"  Discourse: {', '.join(analysis['discourseMarkers'][:10])}")
