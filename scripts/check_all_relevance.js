const fs = require('fs');
const html = fs.readFileSync('ielts-speak-lab.html', 'utf8');
const startIdx = html.indexOf('const TOPIC_EXPRESSIONS = {');
let depth = 0, endIdx = startIdx, inString = false, sc = null;
for (let i = startIdx; i < html.length; i++) {
  const c = html[i];
  if (inString) {
    if (c === '\\') { i++; continue; }
    if (c === sc) inString = false;
    continue;
  }
  if (c === '"' || c === "'" || c === '`') { inString = true; sc = c; continue; }
  if (c === '{') depth++;
  if (c === '}') { depth--; if (depth === 0) { endIdx = i; break; } }
}
const code = html.substring(startIdx, endIdx + 1);
const obj = eval('(' + code.replace('const TOPIC_EXPRESSIONS = ', '') + ')');

// Topic relevance keywords
const topicKeywords = {
  hometown: ['hometown', 'grew up', 'neighborhood', 'where i was born', 'born', 'childhood', 'street', 'house', 'village', 'town', 'city', 'move away', 'left home', 'local', 'community', 'my parents', 'growing up', 'back home', 'my old'],
  'work-study': ['job', 'work', 'study', 'student', 'college', 'university', 'office', 'boss', 'colleague', 'career', 'promotion', 'interview', 'major', 'degree', 'class', 'homework', 'teacher', 'school'],
  hobbies: ['hobby', 'free time', 'weekend', 'play', 'game', 'fun', 'enjoy', 'love doing', 'relax', 'cook', 'paint', 'draw', 'guitar', 'piano', 'read', 'movie', 'sport', 'collect'],
  food: ['food', 'eat', 'meal', 'dinner', 'lunch', 'breakfast', 'cook', 'recipe', 'restaurant', 'dish', 'taste', 'delicious', 'hungry', 'kitchen', 'bake', 'snack', 'wine', 'coffee'],
  weather: ['weather', 'rain', 'sunny', 'cloudy', 'snow', 'cold', 'hot', 'warm', 'temperature', 'season', 'summer', 'winter', 'spring', 'autumn', 'storm', 'wind'],
  music: ['music', 'song', 'sing', 'guitar', 'piano', 'concert', 'band', 'album', 'listen to', 'melody', 'rhythm', 'dance', 'karaoke'],
  travel: ['travel', 'trip', 'vacation', 'holiday', 'airport', 'flight', 'hotel', 'tourist', 'visit', 'beach', 'mountain', 'abroad', 'foreign', 'destination', 'luggage', 'suitcase'],
  family: ['family', 'mom', 'dad', 'mother', 'father', 'brother', 'sister', 'son', 'daughter', 'wife', 'husband', 'parent', 'grandma', 'grandpa', 'uncle', 'aunt', 'cousin', 'sibling'],
  tech: ['phone', 'computer', 'laptop', 'internet', 'app', 'social media', 'technology', 'gadget', 'screen', 'device', 'online', 'digital', 'video game', 'text', 'email', 'software'],
  sports: ['sport', 'game', 'team', 'player', 'football', 'basketball', 'soccer', 'tennis', 'swim', 'run', 'gym', 'workout', 'exercise', 'coach', 'match', 'score', 'ball'],
  'person-admire': ['admire', 'inspire', 'look up to', 'role model', 'respect', 'hero', 'mentor', 'achievement', 'influence', 'talent', 'success', 'proud', 'motivate', 'dream'],
  'memorable-trip': ['trip', 'travel', 'vacation', 'visit', 'beach', 'mountain', 'hotel', 'tourist', 'flight', 'journey', 'adventure', 'unforgettable', 'memorable'],
  'important-event': ['important', 'event', 'graduation', 'wedding', 'birthday', 'celebration', 'festival', 'ceremony', 'anniversary', 'special day', 'once in a lifetime', 'remember'],
  'favorite-place': ['favorite', 'favourite', 'place', 'park', 'beach', 'corner', 'spot', 'coffee shop', 'library', 'museum', 'garden', 'rooftop', 'quiet', 'relax'],
  'book-movie': ['book', 'movie', 'film', 'read', 'watch', 'novel', 'chapter', 'character', 'plot', 'story', 'cinema', 'theater', 'screen', 'scene', 'author', 'director', 'actor'],
  'skill-learned': ['skill', 'learn', 'teach', 'practice', 'master', 'improve', 'technique', 'train', 'course', 'lesson', 'practically', 'useful'],
  'childhood-memory': ['childhood', 'kid', 'grew up', 'remember', 'young', 'elementary', 'playground', 'toy', 'game', 'fairy tale', 'memory', 'little', 'six years old'],
  'difficult-decision': ['decision', 'choose', 'choice', 'hard', 'difficult', 'decide', 'weigh', 'option', 'risk', 'regret', 'trade-off'],
  environment: ['environment', 'pollution', 'climate', 'global warming', 'plastic', 'recycle', 'green', 'sustainable', 'nature', 'energy', 'carbon', 'waste', 'tree', 'ocean'],
  education: ['education', 'school', 'learn', 'teach', 'teacher', 'student', 'university', 'college', 'degree', 'exam', 'study', 'knowledge', 'classroom', 'curriculum'],
  culture: ['culture', 'tradition', 'festival', 'custom', 'heritage', 'history', 'ancestor', 'celebrate', 'ceremony', 'language', 'art', 'generation'],
  'work-life': ['work', 'life', 'balance', 'stress', 'overtime', 'burnout', 'family time', 'schedule', 'career', 'relax', 'weekend', 'vacation', 'pressure'],
  'social-media': ['social media', 'instagram', 'facebook', 'twitter', 'online', 'post', 'like', 'follow', 'internet', 'influencer', 'privacy', 'addiction', 'screen time', 'troll'],
  urbanization: ['city', 'urban', 'rural', 'countryside', 'village', 'move to the city', 'population', 'traffic', 'apartment', 'suburb', 'concrete', 'skyline', 'develop'],
};

// Check each topic
let totalScore = 0, totalEntries = 0, badTopics = [];
for (const [topic, words] of Object.entries(topicKeywords)) {
  const entries = obj[topic] || [];
  let topicScore = 0;
  entries.forEach(e => {
    const text = (e.en || '').toLowerCase();
    const matches = words.filter(w => text.includes(w));
    topicScore += matches.length;
  });
  const avg = entries.length ? (topicScore / entries.length).toFixed(1) : 0;
  totalScore += topicScore;
  totalEntries += entries.length;
  const relevance = topicScore >= entries.length * 1.2 ? '✅' : (topicScore >= entries.length * 0.5 ? '⚠️' : '❌');
  console.log(`${relevance} ${topic}: avg=${avg} total=${topicScore}/${entries.length} entries`);
  if (topicScore < entries.length * 1.2) badTopics.push(topic);
}
console.log('\n=== PROBLEM TOPICS ===');
console.log(badTopics.join(', '));
