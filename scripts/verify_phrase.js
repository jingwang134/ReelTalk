// Verify hometown new-format data renders correctly
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

const ht = obj.hometown;
console.log('HOMETOWN entries:', ht.length);
console.log('All have phrase field:', ht.every(e => e.phrase));
console.log('All have meaning:', ht.every(e => e.meaning));
console.log('All have usage:', ht.every(e => e.usage));
console.log('All have ielts_example:', ht.every(e => e.ielts_example));
console.log('All have example:', ht.every(e => e.example));
console.log('All have function:', ht.every(e => e.function));
console.log('All have source:', ht.every(e => e.source));
console.log('');
ht.forEach((e, i) => {
  console.log('[' + (i+1) + '] ' + e.function + ' → ' + e.phrase);
});
console.log('');
// Check other topics still have old format
const otherTopic = Object.keys(obj).find(k => k !== 'hometown');
console.log('Other topics unchanged:', obj[otherTopic].every(e => e.en && !e.phrase));
console.log('Other topics count:', Object.keys(obj).filter(k => k !== 'hometown').length);
