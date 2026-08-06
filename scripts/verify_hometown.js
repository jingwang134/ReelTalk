// Verify hometown data in updated HTML
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

console.log('=== HOMETOWN entries (' + obj.hometown.length + ') ===');
obj.hometown.forEach((e, i) => {
  console.log('[' + (i+1) + '] ' + e.function + ' | ' + e.source);
  console.log('  EN: ' + e.en.substring(0, 110));
  console.log('  HL: ' + e.highlight.substring(0, 80));
  console.log('  TR: ' + (e.translation || '').substring(0, 60));
  console.log('  KW: ' + (e.keywords || []).map(k => k.en).join(' | '));
  console.log('');
});
