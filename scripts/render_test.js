// Simulate renderSnippetCards for the new phrase format
const fs = require('fs');
const html = fs.readFileSync('ielts-speak-lab.html', 'utf8');

// Extract TOPIC_EXPRESSIONS
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

const S = { savedSnippetIds: [] };
const exp = obj.hometown[0];

// Replicate the new-format rendering branch
const phSafe = (exp.phrase||'').replace(/'/g,"\\'").replace(/"/g,'&quot;');
const exSafe = (exp.example||'').replace(/'/g,"\\'").replace(/"/g,'&quot;');
const usSafe = (exp.usage||'').replace(/'/g,"\\'").replace(/"/g,'&quot;');
const ieSafe = (exp.ielts_example||'').replace(/'/g,"\\'").replace(/"/g,'&quot;');
const saved = (S.savedSnippetIds||[]).includes('p:'+phSafe.slice(0,40));

const card = `<div class="snippet-card phrase-card">
  <div class="phrase-main">${phSafe}</div>
  <div class="phrase-meaning">${(exp.meaning||'').replace(/'/g,"\\'").replace(/"/g,'&quot;')}</div>
  ${exSafe ? `<div class="phrase-example"><span class="ph-label">剧中</span><span class="ph-ex-text">"${exSafe}"</span><span class="ph-source">— ${exp.source||''}</span></div>` : ''}
  ${usSafe ? `<div class="phrase-usage"><span class="ph-label ph-usage-label">怎么用</span><span class="ph-usage-text">${usSafe}</span></div>` : ''}
  ${ieSafe ? `<div class="phrase-ielts"><span class="ph-label ph-ielts-label">雅思例句</span><span class="ph-ielts-text">"${ieSafe}"</span></div>` : ''}
  <div class="card-footer">
    <span class="card-source">${exp.source||''}</span>
  </div>
</div>`;

// Check key elements
const checks = [
  ['phrase-main', card.includes('phrase-main')],
  ['meaning', card.includes(exp.meaning)],
  ['剧中 label', card.includes('剧中')],
  ['example text', card.includes('Jay')],
  ['怎么用 label', card.includes('怎么用')],
  ['usage text', card.includes('标准开场')],
  ['雅思例句 label', card.includes('雅思例句')],
  ['ielts example', card.includes('Sichuan')],
  ['source', card.includes('S01E01')],
];
let allOK = true;
checks.forEach(([name, ok]) => {
  console.log((ok ? '✅' : '❌') + ' ' + name);
  if (!ok) allOK = false;
});
console.log(allOK ? '\nRENDER OK' : '\nRENDER FAIL');
