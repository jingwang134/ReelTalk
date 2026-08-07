const fs = require('fs');
const html = fs.readFileSync('ielts-speak-lab.html', 'utf8');

const startIdx = html.indexOf('const KARDASHIAN_EXPRESSIONS = [');
let depth = 0, endIdx = startIdx, inString = false, sc = null;
for (let i = startIdx; i < html.length; i++) {
  const c = html[i];
  if (inString) {
    if (c === '\\') { i++; continue; }
    if (c === sc) inString = false;
    continue;
  }
  if (c === '"' || c === "'" || c === '`') { inString = true; sc = c; continue; }
  if (c === '[') depth++;
  if (c === ']') { depth--; if (depth === 0) { endIdx = i; break; } }
}
const code = html.substring(startIdx, endIdx + 1);
const exprs = eval('(' + code.replace('const KARDASHIAN_EXPRESSIONS = ', '') + ')');
console.log('KARDASHIAN_EXPRESSIONS:', exprs.length, 'entries');
console.log('All phrase format:', exprs.every(e => e.phrase && e.meaning && e.example && e.source && e.usage && e.ielts_example && e.function));
console.log('');
const funcs = {};
exprs.forEach(e => { funcs[e.function] = (funcs[e.function]||0)+1; });
Object.entries(funcs).forEach(([f, c]) => console.log('  ' + f + ': ' + c + '条'));
console.log('');
const bad = exprs.filter(e => /fuck|shit|bitch|dick/i.test(e.example + e.phrase));
console.log('Profanity found:', bad.length);
console.log('');
console.log('Sample entry:');
console.log(JSON.stringify(exprs[0], null, 1));
