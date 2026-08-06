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

// Show all hometown entries
console.log('=== HOMETOWN entries (' + obj.hometown.length + ') ===');
obj.hometown.forEach((e, i) => {
  console.log('[' + (i+1) + '] function=' + e.function + ' source=' + e.source);
  console.log('  en: ' + (e.en || '').substring(0, 150) + '...');
  console.log('  highlight: ' + (e.highlight || '').substring(0, 100));
  console.log('');
});

// Check relevance: does the text contain hometown-related words?
const townWords = ['hometown', 'home town', 'grew up', 'neighborhood', 'neighbourhood', 'where i was born', 'childhood', 'street', 'house', 'village', 'city', 'born and raised', 'move', 'left', 'live', 'local', 'community'];
console.log('=== RELEVANCE CHECK ===');
obj.hometown.forEach((e, i) => {
  const text = (e.en || '').toLowerCase();
  const matches = townWords.filter(w => text.includes(w));
  const score = matches.length;
  console.log('[' + (i+1) + '] score=' + score + ' matches=[' + matches.join(',') + ']');
});
