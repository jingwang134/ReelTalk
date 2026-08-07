# Generate Kardashians style DNA analysis (mirrors __MF_ANALYSIS__ format)
import json
import re
from collections import Counter

with open('data/kardashian-s01.json', 'r', encoding='utf-8') as f:
    corpus = json.load(f)

all_lines = []
for ep, data in corpus.items():
    for l in data['lines']:
        all_lines.append(l['en'])

all_text = ' '.join(all_lines)
total_words = len(all_text.split())

# Stopwords
SW = set('the a an is are was were be been being have has had do does did will would could should may might can shall i you he she it we they me him her us them my your his its our their this that these those am of in to for on with at from by about as into through during before after above below between out off over under again further then once here there when where why how all both each few more most other some some such no nor not only own same so than too very just because but and or if while up down what which who whom like get got one two three yeah okay'.split())

# Tokenize
words = all_text.lower().split()
content_words = [w.strip('.,;:!?()"\'') for w in words]
content_words = [w for w in content_words if w and w not in SW and len(w) > 2]
freq = Counter(content_words)
top_words = [{'word': w, 'count': c} for w, c in freq.most_common(15)]

# Bigrams/trigrams
clean_words = [w.strip('.,;:!?()"\'') for w in words]
clean_words = [w for w in clean_words if w]
bigrams = Counter()
trigrams = Counter()
for i in range(len(clean_words) - 1):
    bg = clean_words[i] + ' ' + clean_words[i+1]
    bigrams[bg] += 1
for i in range(len(clean_words) - 2):
    tg = clean_words[i] + ' ' + clean_words[i+1] + ' ' + clean_words[i+2]
    trigrams[tg] += 1
top_bigrams = [{'phrase': p, 'count': c} for p, c in bigrams.most_common(12) if c >= 2]
top_trigrams = [{'phrase': p, 'count': c} for p, c in trigrams.most_common(10) if c >= 2]

# Discourse markers
DM = ['you know', 'i mean', 'like', 'right', 'okay', 'well', 'look', 'honestly', 'basically', 'literally', 'actually', 'obviously', 'seriously', 'here is the thing', 'the thing is', 'let me tell you', 'not gonna lie', 'to be honest', 'at the end of the day', 'kind of', 'sort of', 'come on', 'listen', 'i guess', 'oh my god', 'oh my gosh']
lower_text = ' ' + all_text.lower() + ' '
found_markers = [m for m in DM if m in lower_text]

# Contractions / formality
contractions = len(re.findall(r"\b(it's|don't|can't|won't|isn't|aren't|didn't|doesn't|i'm|you're|they're|we're|that's|what's|let's|gonna|wanna|gotta|kinda|sorta|i've|you've|we've|there's|he's|she's)\b", all_text.lower()))
formality = round(max(1, min(10, 8 - (contractions / total_words * 40 if total_words else 0))))

# Sentences
sentences = [s for s in re.split(r'[.!?]+', all_text) if s.strip() and len(s.strip()) > 3]
avg_sent_len = round(len(clean_words) / len(sentences)) if sentences else 8

# Tone analysis - keyword based
tone_kw = {
    'dramatic': ['oh my god', 'are you kidding', 'i can\'t', 'this is crazy', 'literally', 'insane', 'fucking', 'crazy', 'seriously', 'unbelievable'],
    'bold': ['i win', 'i\'m the best', 'real', 'strong', 'power', 'boss', 'million', 'billion', 'deal', 'negotiate', 'brand', 'empire'],
    'warm': ['love', 'family', 'mom', 'baby', 'happy', 'proud', 'sweet', 'beautiful', 'grateful', 'thank'],
    'self_deprecating': ['i hate', 'i\'m so bad', 'i can\'t believe', 'i\'m insane', 'i know i\'m', 'stupid'],
    'anxious': ['nervous', 'worried', 'stress', 'pressure', 'scared', 'afraid', 'can\'t sleep'],
}
tone_counts = {}
for tone, kws in tone_kw.items():
    c = sum(len(re.findall(kw, all_text.lower())) for kw in kws)
    if c > 0:
        tone_counts[tone] = c
all_tones = dict(sorted(tone_counts.items(), key=lambda x: -x[1]))
primary_tone = {'tone': list(all_tones.keys())[0] if all_tones else 'neutral', 'intensity': min(10, max(5, list(all_tones.values())[0] if all_tones else 5))}

analysis = {
    'topWords': top_words,
    'topBigrams': top_bigrams,
    'topTrigrams': top_trigrams,
    'sigExpr': [t['phrase'] for t in top_trigrams[:6]],
    'primaryTone': primary_tone,
    'formality': formality,
    'avgSentLen': avg_sent_len,
    'totalWords': total_words,
    'totalSentences': len(sentences),
    'discourseMarkers': found_markers,
    'allTones': all_tones,
    'episodes': len(corpus),
    'lines': len(all_lines),
}

# Output as JS
js = 'window.__K_ANALYSIS__=' + json.dumps(analysis, ensure_ascii=False) + ';'
with open('data/k-analysis.js', 'w', encoding='utf-8') as f:
    f.write(js)

print('=== KARDASHIAN DNA ===')
print('Total words:', total_words, '| sentences:', len(sentences), '| avg sent len:', avg_sent_len)
print('Formality:', formality, '/10 | contractions:', contractions)
print('Primary tone:', primary_tone)
print('All tones:', all_tones)
print('Discourse markers:', found_markers)
print('Top words:', [w['word'] for w in top_words])
print('Top bigrams:', [b['phrase'] for b in top_bigrams[:8]])
print('Top trigrams:', [t['phrase'] for t in top_trigrams[:8]])
print('Written to data/k-analysis.js', len(js), 'chars')
