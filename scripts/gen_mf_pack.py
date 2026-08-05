"""
生成 ReelTalk 数据包 JS 文件：预计算摩登家庭风格 DNA + 采样语料
"""
import json
import re
from pathlib import Path
from collections import Counter

DATA_DIR = Path(r"C:\Users\15869\WorkBuddy\2026-08-05-10-43-07\data")
OUT_DIR = DATA_DIR

with open(DATA_DIR / 'modern-family-compact.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)  # {s01: {s01e01: {title, text}, ...}, ...}

# ===== 1. 聚合所有对话文本 =====
all_texts = []
sample_episodes = {}  # 每季取1集作为样本
for sk in sorted(corpus.keys()):
    season_eps = sorted(corpus[sk].keys())
    season_text = ''
    for ek in season_eps:
        t = corpus[sk][ek]['text']
        all_texts.append(t)
        season_text += ' ' + t

    # 取中间一集作为样本
    mid_idx = len(season_eps) // 2
    sample_ek = season_eps[mid_idx]
    sample_episodes[f"{sk}/mid"] = {
        'title': corpus[sk][sample_ek]['title'],
        'text': corpus[sk][sample_ek]['text'][:3000]  # 截取前3000字符
    }

full_text = ' '.join(all_texts)
total_words = len(full_text.split())
total_chars = len(full_text)

print(f"Total: {total_words} words, {total_chars} chars across {len(all_texts)} texts")

# ===== 2. NLP 分析函数（复刻 ReelTalk 逻辑） =====
STOP_WORDS = set("the a an and or but in on at to for of with by from as is was are were am be been have has had do does did will would can could shall should may might I you he she it we they me him her us them my your his its our their this that these those so if when where how all about up out down just then now here there very too not no".split())

DISCOURSE_MARKERS = [
    'you know', 'i mean', 'like', 'honestly', 'literally', 'basically',
    'actually', 'obviously', 'seriously', 'technically', 'frankly',
    'look', 'listen', 'right', 'okay', 'well', 'so', 'anyway',
    'at the end of the day', 'the thing is', 'i guess', 'kind of', 'sort of',
    'i feel like', 'i think', 'i believe', 'bible', 'period', 'vibes',
    'not gonna lie', 'to be honest', 'i\'m not gonna lie'
]

TONE_PATTERNS = {
    'enthusiastic': ['amazing', 'incredible', 'love', 'awesome', 'fantastic', 'great', 'wonderful', 'best', 'perfect', 'obsessed', 'everything'],
    'self_deprecating': ['stupid', 'idiot', 'mess', 'terrible', 'embarrassing', 'awkward', 'weird', 'fail', 'wrong', 'mistake', 'sorry'],
    'sarcastic': ['really', 'wow', 'great', 'nice', 'sure', 'perfect', 'obviously', 'of course', 'congratulations'],
    'warm': ['love', 'family', 'together', 'home', 'care', 'sweet', 'honey', 'kids', 'always', 'never', 'proud', 'happy'],
    'dramatic': ['never', 'always', 'worst', 'best', 'everything', 'nothing', 'disaster', 'crisis', 'literally', 'absolutely'],
    'deadpan': ['okay', 'fine', 'whatever', 'sure', 'alright', 'cool', 'nice', 'interesting']
}

def analyze_corpus(text):
    """复刻 ReelTalk 的 analyzeCorpus 函数，返回预计算 analysis"""
    words = re.findall(r"[a-zA-Z']+", text.lower())
    sentences = re.split(r'[.!?]+', text)
    sentences = [s.strip() for s in sentences if s.strip()]

    if not words or not sentences:
        return None

    # 词频
    content_words = [w for w in words if w not in STOP_WORDS and len(w) > 1]
    word_freq = Counter(content_words)
    top_words = [{'word': w, 'count': c} for w, c in word_freq.most_common(30)]

    # Bigrams
    bigrams = [' '.join(content_words[i:i+2]) for i in range(len(content_words)-1)]
    bi_freq = Counter(bigrams)
    top_bigrams = [{'phrase': b, 'count': c} for b, c in bi_freq.most_common(30) if c >= 3]

    # Trigrams
    trigrams = [' '.join(content_words[i:i+3]) for i in range(len(content_words)-2)]
    tri_freq = Counter(trigrams)
    top_trigrams = [{'phrase': t, 'count': c} for t, c in tri_freq.most_common(20) if c >= 2]

    # 句首
    openers = [' '.join(s.strip().split()[:3]).lower() for s in sentences if s.strip().split()]
    opener_freq = Counter(openers)
    top_openers = [{'phrase': o, 'count': c} for o, c in opener_freq.most_common(20)]

    # 话语标记
    text_lower = text.lower()
    markers = [m for m in DISCOURSE_MARKERS if m in text_lower]

    # 句长
    sent_len = [len(s.split()) for s in sentences]
    avg_sent_len = sum(sent_len) / len(sent_len) if sent_len else 0

    # 正式度
    contraction_count = len(re.findall(r"\b\w+'\w+\b", text))
    contraction_rate = (contraction_count / len(words) * 100) if words else 0
    complex_words = [w for w in words if len(w) > 7 and w not in STOP_WORDS]
    complex_rate = (len(complex_words) / len(words) * 100) if words else 0
    formality = max(1, min(10, round(10 - contraction_rate * 3 + complex_rate * 2)))

    # 语气
    tone_scores = {}
    all_tone_words = []
    for tone, kw_list in TONE_PATTERNS.items():
        count = sum(text_lower.count(f' {kw} ') + text_lower.count(f' {kw}.') + text_lower.count(f' {kw},') + text_lower.count(f' {kw}!') for kw in kw_list)
        tone_scores[tone] = count
        all_tone_words.extend(kw for kw in kw_list if kw in text_lower.split())

    best_tone = max(tone_scores, key=tone_scores.get) if any(tone_scores.values()) else 'warm'
    intensity = min(100, tone_scores[best_tone] * 5) if tone_scores[best_tone] > 0 else 30

    # 标点
    excl_count = text.count('!')
    q_count = text.count('?')
    excl_rate = (excl_count / len(sentences) * 100) if sentences else 0
    q_rate = (q_count / len(sentences) * 100) if sentences else 0

    # 签名表达
    sig = [{'phrase': t, 'count': c} for t, c in tri_freq.most_common(5) if c >= 3]

    return {
        'topWords': top_words[:20],
        'topBigrams': top_bigrams[:20],
        'topTrigrams': top_trigrams[:15],
        'topOpeners': top_openers[:10],
        'discourseMarkers': markers[:20],
        'avgSentLen': round(avg_sent_len, 1),
        'maxSentLen': max(sent_len) if sent_len else 0,
        'minSentLen': min(sent_len) if sent_len else 0,
        'totalWords': len(words),
        'totalSentences': len(sentences),
        'formality': formality,
        'primaryTone': {'tone': best_tone, 'intensity': intensity},
        'allTones': [{'tone': t, 'score': s} for t, s in sorted(tone_scores.items(), key=lambda x: -x[1])[:3]],
        'exclamationCount': excl_count,
        'questionCount': q_count,
        'exclamationRate': round(excl_rate, 1),
        'questionRate': round(q_rate, 1),
        'contractionRate': round(contraction_rate, 1),
        'complexWordRate': round(complex_rate, 1),
        'sigExpr': [s['phrase'] for s in sig],
    }

# ===== 3. 分析 =====
analysis = analyze_corpus(full_text)
print(f"Analysis complete")
print(f"  Tone: {analysis['primaryTone']['tone']} ({analysis['primaryTone']['intensity']}%)")
print(f"  Formality: {analysis['formality']}/10")
print(f"  Avg Sent Len: {analysis['avgSentLen']}")
print(f"  Top words: {', '.join(w['word'] for w in analysis['topWords'][:10])}")
print(f"  Sig expressions: {analysis['sigExpr']}")

# ===== 4. 生成 JS 文件 =====
# 分季语料（每季的聚合文本用于分析）
season_corpus = {}
for sk in sorted(corpus.keys()):
    season_text = ' '.join(corpus[sk][ek]['text'] for ek in sorted(corpus[sk].keys()))
    season_corpus[sk] = {
        'title': f'Modern Family Season {int(sk[1:]):02d}',
        'text': season_text,
        'wordCount': len(season_text.split())
    }

js_content = f"""// ReelTalk Data Pack: Modern Family 全11季台词
// Auto-generated {__import__('datetime').datetime.now().isoformat()}
// 247 episodes, 173,963 lines

window.__MF_CORPUS__ = {json.dumps(season_corpus, ensure_ascii=False)};

window.__MF_ANALYSIS__ = {json.dumps(analysis, ensure_ascii=False)};

window.__MF_STATS__ = {{
  totalEpisodes: 247,
  totalLines: 173963,
  totalWords: {total_words},
  seasons: 11
}};

// 样例对话（用于搜索/浏览）
window.__MF_SAMPLES__ = {json.dumps(sample_episodes, ensure_ascii=False)};
"""

out_path = OUT_DIR / 'mf-corpus.js'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(js_content)

print(f"\n✅ Data pack generated: {out_path} ({out_path.stat().st_size / 1024 / 1024:.1f} MB)")
print(f"   Include in ReelTalk with: <script src=\"data/mf-corpus.js\"></script>")
