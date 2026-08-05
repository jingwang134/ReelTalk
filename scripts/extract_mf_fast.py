"""
快速版：用 pypdf 批量提取摩登家庭台词 → 结构化 JSON
"""
import json
import re
from pathlib import Path
from pypdf import PdfReader

BASE = Path(r"C:\Users\15869\Desktop\文件\WJ\en\PDF")
OUTPUT = Path(r"C:\Users\15869\WorkBuddy\2026-08-05-10-43-07\data")
OUTPUT.mkdir(exist_ok=True)

def clean_line(line):
    """清洗一行对话文本，返回 None 表示跳过"""
    line = line.strip()
    if not line: return None
    # 页眉
    if line.startswith('摩登家庭-S'): return None
    # 页码
    if re.match(r'^第\d+页/共\d+页$', line): return None
    # 底部单词注释行
    if re.match(r'^[a-z]+:', line): return None
    if re.search(r'[a-z]+:[a-z]', line) and not any(c > '\u4e00' for c in line[:20]): return None
    return line

def split_line(line):
    """拆分双语行 → (en, cn, ts)"""
    ts_match = re.search(r'\[(\d{2}:\d{2})\]', line)
    ts = ts_match.group(1) if ts_match else None
    text = re.sub(r'\[\d{2}:\d{2}\]', '', line).strip()

    # 找第一个中文字符位置
    cn_idx = None
    for i, c in enumerate(text):
        if '\u4e00' <= c <= '\u9fff':
            cn_idx = i
            break

    if cn_idx is None:
        return {'en': text.strip(), 'cn': '', 'ts': ts}

    en = text[:cn_idx].strip().rstrip('-').strip()
    cn = text[cn_idx:].strip()
    return {'en': en, 'cn': cn, 'ts': ts}

def extract_episode(pdf_path):
    """快速提取单集"""
    reader = PdfReader(str(pdf_path))
    lines = []
    for page in reader.pages:
        text = page.extract_text()
        if text:
            for line in text.split('\n'):
                cl = clean_line(line)
                if cl:
                    parsed = split_line(cl)
                    if parsed['en']:
                        lines.append(parsed)
    return lines

# ===== 主流程 =====
all_data = {}
total_eps = 0
total_lines = 0
season_dirs = sorted(d for d in BASE.iterdir() if d.is_dir() and d.name.startswith('PDF-S'))

for season_dir in season_dirs:
    season_num = season_dir.name.replace('PDF-S', '')
    sk = f"s{season_num}"
    all_data[sk] = {}
    pdfs = sorted(season_dir.glob('*.pdf'))

    for pdf_path in pdfs:
        ep_match = re.search(r'S(\d+)E(\d+)', pdf_path.name)
        if not ep_match: continue
        ek = f"s{season_num}e{int(ep_match.group(2)):02d}"

        lines = extract_episode(pdf_path)
        if not lines: continue

        all_data[sk][ek] = {
            'title': pdf_path.stem,
            'lines': lines,
            'total': len(lines)
        }
        total_eps += 1
        total_lines += len(lines)

    print(f"  Season {season_num}: {len(all_data[sk])} episodes")

# 精简版：纯英文拼接
compact = {}
for sk, seasons in all_data.items():
    compact[sk] = {}
    for ek, ep in seasons.items():
        text = ' '.join(l['en'] for l in ep['lines'])
        compact[sk][ek] = {'title': ep['title'], 'text': text}

# 输出
full_path = OUTPUT / 'modern-family.json'
with open(full_path, 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False)

compact_path = OUTPUT / 'modern-family-compact.json'
with open(compact_path, 'w', encoding='utf-8') as f:
    json.dump(compact, f, ensure_ascii=False)

print(f"\n✅ {total_eps} episodes, {total_lines} lines")
print(f"   Full:    {full_path} ({full_path.stat().st_size/1024/1024:.1f} MB)")
print(f"   Compact: {compact_path} ({compact_path.stat().st_size/1024/1024:.1f} MB)")
