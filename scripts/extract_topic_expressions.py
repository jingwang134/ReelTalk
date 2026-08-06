"""
从摩登家庭语料中按雅思话题提取观点表达
输出：TOPIC_EXPRESSIONS JS 数据结构
"""
import json
import re
from pathlib import Path
from collections import defaultdict, Counter

DATA_DIR = Path(r"C:\Users\15869\WorkBuddy\2026-08-05-10-43-07\data")
OUTPUT_DIR = Path(r"C:\Users\15869\WorkBuddy\2026-08-05-10-43-07\data")

with open(DATA_DIR / 'modern-family-compact.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

# 拼接所有英文文本
all_seasons = {}
for sk in sorted(corpus.keys()):
    season_text = ' '.join(corpus[sk][ek]['text'] for ek in sorted(corpus[sk].keys()))
    all_seasons[sk] = season_text

# 按剧集分句（保留上下文）
all_episodes = []
for sk in sorted(corpus.keys()):
    for ek in sorted(corpus[sk].keys()):
        ep = corpus[sk][ek]
        text = ep['text']
        sentences = re.split(r'(?<=[.!?])\s+', text)
        sentences = [s.strip() for s in sentences if len(s.strip()) > 15]
        # ek format: "s01e01"
        ep_num = int(ek.split('e')[1]) if 'e' in ek else int(ek[1:])
        all_episodes.append({
            'season': int(sk[1:]),
            'episode': ep_num,
            'title': ep['title'],
            'sentences': sentences,
            'full_text': text,
        })

print(f"Total episodes: {len(all_episodes)}")
print(f"Total seasons: {len(all_seasons)}")

# ============================================================
# 24 个雅思话题 × 搜索关键词组
# ============================================================
TOPIC_KEYWORDS = {
    'hometown': {
        'name': '家乡',
        'keywords': [
            'town', 'city', 'neighborhood', 'hometown', 'grew up', 'community',
            'where I live', 'small town', 'local', 'quiet', 'peaceful', 'suburb',
            'moved here', 'born', 'raised', 'everybody knows', 'home town',
            'live in', 'the area', 'street', 'safe', 'downtown'
        ],
        'negatives': ['in town', 'out of town'],  # 过滤出现在俚语中的误匹配
    },
    'work-study': {
        'name': '工作学习',
        'keywords': [
            'job', 'work', 'office', 'school', 'study', 'college', 'university',
            'career', 'boss', 'coworker', 'colleague', 'major', 'degree', 'class',
            'student', 'homework', 'project', 'deadline', 'stress', 'busy',
            'meeting', 'promotion', 'quit', 'fired'
        ],
    },
    'hobbies': {
        'name': '兴趣爱好',
        'keywords': [
            'hobby', 'free time', 'weekend', 'love doing', 'magic', 'golf',
            'photography', 'reading', 'cooking', 'gardening', 'music', 'play',
            'enjoy', 'passion', 'obsessed with', 'into', 'learning', 'practice'
        ],
    },
    'food': {
        'name': '美食',
        'keywords': [
            'food', 'eat', 'cook', 'dinner', 'lunch', 'breakfast', 'restaurant',
            'delicious', 'recipe', 'kitchen', 'meal', 'taste', 'coffee', 'wine',
            'hungry', 'order', 'chef', 'dish', 'chinese', 'pizza', 'bbq'
        ],
    },
    'weather': {
        'name': '天气',
        'keywords': [
            'weather', 'rain', 'sun', 'hot', 'cold', 'snow', 'sunny', 'storm',
            'freezing', 'summer', 'winter', 'season', 'climate', 'outside',
            'beautiful day', 'temperature', 'humid'
        ],
    },
    'music': {
        'name': '音乐',
        'keywords': [
            'music', 'song', 'sing', 'band', 'concert', 'guitar', 'piano',
            'listen to', 'album', 'playlist', 'dance', 'radio', 'musical',
            'beat', 'melody', 'sound', 'voice', 'singer'
        ],
    },
    'travel': {
        'name': '旅行',
        'keywords': [
            'travel', 'trip', 'vacation', 'visit', 'flight', 'airport', 'hotel',
            'beach', 'abroad', 'overseas', 'tourist', 'sightseeing', 'explore',
            'adventure', 'road trip', 'getaway', 'go back to', 'country'
        ],
    },
    'family': {
        'name': '家庭',
        'keywords': [
            'family', 'mom', 'dad', 'parent', 'kid', 'child', 'brother', 'sister',
            'husband', 'wife', 'marriage', 'married', 'grandparent', 'uncle',
            'aunt', 'cousin', 'son', 'daughter', 'raise', 'growing up', 'home'
        ],
    },
    'tech': {
        'name': '科技',
        'keywords': [
            'phone', 'computer', 'internet', 'technology', 'online', 'screen',
            'app', 'device', 'digital', 'social media', 'text', 'video', 'camera',
            'smart', 'gadget', 'website', 'google', 'facebook', 'youtube'
        ],
    },
    'sports': {
        'name': '运动',
        'keywords': [
            'sports', 'football', 'basketball', 'soccer', 'game', 'team', 'play',
            'exercise', 'gym', 'workout', 'run', 'coach', 'win', 'lose', 'match',
            'competition', 'player', 'champion', 'athlete'
        ],
    },
    'person-admire': {
        'name': '敬佩的人',
        'keywords': [
            'admire', 'look up to', 'respect', 'hero', 'inspiration', 'role model',
            'mentor', 'influence', 'I learned from', 'taught me', 'amazing person',
            'greatest', 'best person', 'changed my life', 'someone I know'
        ],
    },
    'memorable-trip': {
        'name': '难忘的旅行',
        'keywords': [
            'best trip', 'amazing trip', 'remember', 'unforgettable', 'first time',
            'never forget', 'that time we went', 'went to', 'visited', 'traveled',
            'on our way', 'the view', 'incredible', 'beautiful place'
        ],
    },
    'book-movie': {
        'name': '书影音',
        'keywords': [
            'movie', 'film', 'book', 'watch', 'read', 'show', 'series', 'theater',
            'cinema', 'actor', 'character', 'story', 'scene', 'episode', 'novel',
            'favorite movie', 'favorite book', 'touching', 'ending', 'plot'
        ],
    },
    'skill-learned': {
        'name': '学会的技能',
        'keywords': [
            'learned', 'taught myself', 'picked up', 'figured out how', 'skill',
            'started learning', 'practice', 'got better at', 'can now', 'finally',
            'lesson', 'master', 'improve', 'getting good at', 'I know how'
        ],
    },
    'childhood-memory': {
        'name': '童年记忆',
        'keywords': [
            'when I was a kid', 'childhood', 'growing up', 'back then', 'used to',
            'little kid', 'young', 'remember when', 'high school', 'elementary',
            'my dad used to', 'my mom would', 'we would always', 'those days'
        ],
    },
    'difficult-decision': {
        'name': '困难的决定',
        'keywords': [
            'decision', 'choice', 'hardest', 'difficult', 'torn between',
            'could not decide', 'went back and forth', 'had to choose',
            'right call', 'wrong', 'regret', 'risk', 'take a chance',
            'what if', 'made up my mind', 'finally decided'
        ],
    },
    'environment': {
        'name': '环境',
        'keywords': [
            'environment', 'nature', 'planet', 'green', 'recycle', 'pollution',
            'climate', 'waste', 'energy', 'clean', 'ocean', 'trees', 'animals',
            'save the', 'eco', 'environmental', 'sustainable', 'organic'
        ],
    },
    'education': {
        'name': '教育',
        'keywords': [
            'school', 'teacher', 'education', 'learn', 'class', 'college',
            'university', 'study', 'exam', 'test', 'grades', 'homework',
            'student', 'professor', 'degree', 'graduate', 'educate', 'teach'
        ],
    },
    'culture': {
        'name': '文化传统',
        'keywords': [
            'tradition', 'culture', 'heritage', 'festival', 'holiday', 'custom',
            'chinese', 'colombian', 'country', 'people', 'traditional', 'way of',
            'back home', 'celebrate', 'generation', 'passed down', 'roots'
        ],
    },
    'work-life': {
        'name': '工作生活平衡',
        'keywords': [
            'busy', 'stress', 'balance', 'work life', 'exhausted', 'tired',
            'too much work', 'no time', 'relax', 'rest', 'break', 'vacation',
            'overwhelmed', 'need a break', 'can not handle', 'pace', 'crazy'
        ],
    },
    'social-media': {
        'name': '社交媒体',
        'keywords': [
            'facebook', 'instagram', 'social media', 'post', 'online', 'follow',
            'like', 'comment', 'share', 'tweet', 'internet', 'viral', 'photo',
            'selfie', 'update', 'scroll', 'notification', 'followers'
        ],
    },
    'urbanization': {
        'name': '城市化',
        'keywords': [
            'city', 'suburb', 'neighborhood', 'move', 'urban', 'rural',
            'countryside', 'downtown', 'apartment', 'house', 'space',
            'noise', 'traffic', 'crowded', 'quiet', 'peaceful', 'live in'
        ],
    },
}

# ============================================================
# 5 种交际功能 × 句式特征
# ============================================================
FUNCTION_PATTERNS = {
    '开场破题': {
        'priority': 1,
        'patterns': [
            r'^(oh|well|okay|alright|so)[,\s]+',
            r'^(you know|you know what)[,\s]',
            r'^(actually|honestly)[,\s]',
            r'\bthat\'?s (a|an) (really |good )?question\b',
            r'^(let me|I.ll|I will) (tell|say|explain)',
            r'\byou ask(ed)?\b',
            r'\bhere\'?s the thing\b',
        ],
    },
    '表达观点': {
        'priority': 2,
        'patterns': [
            r'\bI (think|feel|believe|guess|mean)\b',
            r'\bthe (thing|way|truth) (is|about)\b',
            r'\bwhat I (love|like|find|enjoy) (is|about)\b',
            r'\b(to me|in my opinion|if you ask me)\b',
            r'\bhonestly[,\s]',
            r'\bI (would|.d) say\b',
            r'\bI.m (pretty|kind of|sort of|really)\b',
        ],
    },
    '举例说明': {
        'priority': 3,
        'patterns': [
            r'\b(like|take|remember) (this|that|when|the time)\b',
            r'\b(for (example|instance))\b',
            r'\bthere was this (one|time)\b',
            r'\bI (remember|recall) (this|when|one)\b',
            r'\bthis one (time|moment|day|night)\b',
            r'\byou should have seen\b',
        ],
    },
    '比较对比': {
        'priority': 4,
        'patterns': [
            r'\b(but|however) (honestly|really|actually)\b',
            r'\bnot (like|as|the same)\b',
            r'\b(I|we) used to\b',
            r'\b(on the other hand|at the same time)\b',
            r'\bcompared to\b',
            r'\bbefore this\b',
            r'\bdifferent from\b',
        ],
    },
    '总结收束': {
        'priority': 5,
        'patterns': [
            r'\b(so yeah|so anyway|anyway[,\s])',
            r'\bthat\'?s (the thing|how it is|what I mean)\b',
            r'\b(you know\?|right\?|don\'?t you think\?)\s*$',
            r'\b(bottom line|long story short|point is)\b',
            r'\b(and that|that.s|it.s) (why|how|what)\b',
        ],
    },
}


def classify_function(sentence):
    """按句式特征分类到交际功能"""
    for func_name, func_data in FUNCTION_PATTERNS.items():
        for pattern in func_data['patterns']:
            if re.search(pattern, sentence, re.IGNORECASE):
                return func_name
    return None


def find_topic_context(ep_data, topic_keywords, window=2):
    """在剧集的句子中搜索包含话题关键词的句子，返回前后各 window 句的上下文"""
    results = []
    kw_set = set(kw.lower() for kw in topic_keywords)

    for i, sent in enumerate(ep_data['sentences']):
        sent_lower = sent.lower()
        # 检查是否包含关键词
        matched = [kw for kw in kw_set if kw in sent_lower]
        if not matched:
            continue

        # 取上下文
        start = max(0, i - window)
        end = min(len(ep_data['sentences']), i + window + 1)
        context = ' '.join(ep_data['sentences'][start:end])

        # 质量过滤
        words = len(context.split())
        if words < 8 or words > 100:
            continue

        # 分类
        func = classify_function(sent)
        if not func:
            continue

        results.append({
            'sent': sent,
            'context': context,
            'function': func,
            'season': ep_data['season'],
            'episode': ep_data['episode'],
            'title': ep_data['title'],
            'matched_keywords': matched,
            'words': words,
        })

    return results


# ============================================================
# 主提取流程
# ============================================================
print("\n" + "="*60)
print("开始按话题提取表达...")
print("="*60)

all_topic_expressions = {}

for topic_id, topic_data in TOPIC_KEYWORDS.items():
    topic_name = topic_data['name']
    keywords = topic_data['keywords']
    negatives = topic_data.get('negatives', [])

    print(f"\n🔍 {topic_name} ({topic_id}) — 搜索关键词: {len(keywords)} 个")

    all_results = []
    for ep in all_episodes:
        results = find_topic_context(ep, keywords, window=2)
        all_results.extend(results)

    # 去重：相近的 context 只保留最好的
    deduped = []
    seen_sents = set()
    for r in sorted(all_results, key=lambda x: -len(x['context'].split())):
        # 用前20个字符哈希去重
        sig = r['sent'][:30].lower().strip()
        if sig in seen_sents:
            continue
        seen_sents.add(sig)

        # 过滤误匹配
        context_lower = r['context'].lower()
        skip = False
        for neg in negatives:
            if neg.lower() in context_lower and r['matched_keywords'][0] == neg.lower():
                skip = True
                break
        if skip:
            continue

        deduped.append(r)

    print(f"  原始匹配: {len(all_results)} → 去重后: {len(deduped)}")

    # 每组功能取前 3 条最优（按句子长度和质量排序）
    by_function = defaultdict(list)
    for r in deduped:
        by_function[r['function']].append(r)

    topic_expressions = []
    for func_name in ['开场破题', '表达观点', '举例说明', '比较对比', '总结收束']:
        func_results = by_function.get(func_name, [])
        # 按质量排序：句子长度适中最好（25-80词），太短太长的靠后
        scored = []
        for r in func_results:
            w = r['words']
            quality = 1.0 - abs(w - 45) / 45  # 45词左右最优
            scored.append((quality, r))
        scored.sort(key=lambda x: -x[0])

        # 取前 3 条
        selected = scored[:3]
        for _, r in selected:
            topic_expressions.append({
                'function': r['function'],
                'en': r['context'],
                'highlight': r['sent'],
                'season': r['season'],
                'episode': r['episode'],
                'source': f"Modern Family S{r['season']:02d}E{r['episode']:02d}",
            })
            print(f"    [{func_name}] S{r['season']:02d}E{r['episode']:02d} ({r['words']}词): {r['sent'][:70]}...")

    all_topic_expressions[topic_id] = topic_expressions

# ============================================================
# 统计
# ============================================================
total = sum(len(v) for v in all_topic_expressions.values())
print(f"\n" + "="*60)
print(f"✅ 提取完成！")
print(f"  话题数: {len(all_topic_expressions)}")
print(f"  总表达数: {total}")
print(f"  平均每话题: {total/len(all_topic_expressions):.1f} 条")
print("="*60)

# ============================================================
# 输出 JavaScript 文件
# ============================================================
output_js = "// Auto-generated from Modern Family corpus\n"
output_js += f"// {len(all_topic_expressions)} topics, {total} expressions\n"
output_js += "const TOPIC_EXPRESSIONS = {\n"

for topic_id in sorted(all_topic_expressions.keys()):
    exps = all_topic_expressions[topic_id]
    if not exps:
        continue
    output_js += f"  '{topic_id}': [\n"
    for exp in exps:
        # 转义 JS 字符串
        en_escaped = exp['en'].replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ').replace('\r', '')
        hl_escaped = exp['highlight'].replace('\\', '\\\\').replace("'", "\\'").replace('\n', ' ').replace('\r', '')
        src = exp['source']
        func = exp['function']
        output_js += f"    {{function:'{func}', en:'{en_escaped}', highlight:'{hl_escaped}', source:'{src}'}},\n"
    output_js += "  ],\n"
output_js += "};\n"

out_path = OUTPUT_DIR / 'topic-expressions.js'
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(output_js)

size_kb = out_path.stat().st_size / 1024
print(f"\n📁 输出: {out_path} ({size_kb:.1f} KB)")

# ============================================================
# 同时输出统计报告
# ============================================================
with open(OUTPUT_DIR / 'topic-expressions-report.txt', 'w', encoding='utf-8') as f:
    f.write("话题表达提取报告\n")
    f.write("="*60 + "\n\n")
    for topic_id in sorted(all_topic_expressions.keys()):
        exps = all_topic_expressions[topic_id]
        if not exps:
            continue
        topic_name = TOPIC_KEYWORDS[topic_id]['name']
        f.write(f"## {topic_name} ({topic_id}) — {len(exps)} 条\n\n")
        by_func = defaultdict(int)
        for exp in exps:
            by_func[exp['function']] += 1
        f.write(f"  功能分布: {dict(by_func)}\n")
        for exp in exps:
            f.write(f"  [{exp['function']}] {exp['source']}\n")
            f.write(f"    {exp['en'][:120]}...\n\n")
        f.write("\n")

print(f"📁 报告: {OUTPUT_DIR / 'topic-expressions-report.txt'}")
