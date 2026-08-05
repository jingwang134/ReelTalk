"""
提取摩登家庭全部PDF台词 → 清洗 → 结构化JSON
"""
import pdfplumber
import json
import re
import os
from pathlib import Path
from collections import Counter

BASE = Path(r"C:\Users\15869\Desktop\文件\WJ\en\PDF")
OUTPUT = Path(r"C:\Users\15869\WorkBuddy\2026-08-05-10-43-07\data")
OUTPUT.mkdir(exist_ok=True)

def clean_line(line):
    """清洗一行对话文本"""
    # 移除页眉（摩登家庭-S01E01-双语台词）
    if re.match(r'摩登家庭-S\d+E\d+-双语台词', line): return None
    # 移除页码
    if re.match(r'第\d+页/共\d+页', line): return None
    # 移除底部单词注释行（包含音标或词汇解释的行）
    if re.search(r'[a-z]+:[^ ]', line) and len(line) > 40: return None
    # 移除纯单词释义行（: 开头的）
    if re.match(r'^[a-z]+:', line): return None
    if not line.strip(): return None
    return line.strip()

def extract_episode(pdf_path):
    """提取单集对话"""
    dialogues = []
    try:
        with pdfplumber.open(str(pdf_path)) as pdf:
            for page in pdf.pages:
                text = page.extract_text()
                if not text: continue
                for line in text.split('\n'):
                    cleaned = clean_line(line)
                    if cleaned:
                        dialogues.append(cleaned)
    except Exception as e:
        print(f"  ERROR: {e}")
        return None
    return dialogues

def split_bilingual(line):
    """拆分双语行 → (英文, 中文)"""
    # 格式: English text 中文翻译 [timestamp]
    # 先提取时间戳
    ts_match = re.search(r'\[(\d{2}:\d{2})\]', line)
    ts = ts_match.group(1) if ts_match else None
    line_no_ts = re.sub(r'\[(\d{2}:\d{2})\]', '', line).strip()

    # 按中英文字符分界点拆分
    # 中文在句尾，英文在前 → 找第一个中文字符
    cn_match = re.search(r'[\u4e00-\u9fff]', line_no_ts)
    if not cn_match:
        return {'en': line_no_ts, 'cn': '', 'ts': ts}

    split_idx = cn_match.start()

    # 如果是连在一起的短句（如 "- Sorry."），特殊处理
    # 找英文部分最后一个合理的断点
    en_part = line_no_ts[:split_idx].strip()
    cn_part = line_no_ts[split_idx:].strip()

    return {'en': en_part, 'cn': cn_part, 'ts': ts}

# ===== 主流程 =====
all_data = {}
stats = Counter()

for season_dir in sorted(BASE.iterdir()):
    if not season_dir.is_dir() or not season_dir.name.startswith('PDF-S'):
        continue

    season_num = season_dir.name.replace('PDF-S', '')
    season_key = f"s{season_num}"
    all_data[season_key] = {}

    pdfs = sorted(season_dir.glob('*.pdf'))
    print(f"\n📺 Season {season_num} ({len(pdfs)} episodes)")

    for pdf_path in pdfs:
        ep_match = re.search(r'S(\d+)E(\d+)', pdf_path.name)
        if not ep_match: continue
        ep_key = f"s{season_num}e{int(ep_match.group(2)):02d}"

        dialogues = extract_episode(pdf_path)
        if not dialogues:
            print(f"  [{ep_key}] SKIP: extraction failed")
            continue

        # 清理双语行
        parsed = []
        for d in dialogues:
            result = split_bilingual(d)
            if result['en']:
                parsed.append(result)

        all_data[season_key][ep_key] = {
            'title': pdf_path.stem,
            'lines': parsed,
            'total_lines': len(parsed),
            'total_words_en': sum(len(p['en'].split()) for p in parsed)
        }

        stats['episodes'] += 1
        stats['total_lines'] += len(parsed)
        print(f"  [{ep_key}] {pdf_path.stem}: {len(parsed)} lines")

# ===== 输出 =====
out_path = OUTPUT / 'modern-family.json'
with open(out_path, 'w', encoding='utf-8') as f:
    json.dump(all_data, f, ensure_ascii=False)

print(f"\n✅ 完成！")
print(f"   剧集: {stats['episodes']} 集")
print(f"   总行数: {stats['total_lines']}")
print(f"   输出: {out_path}")
print(f"   大小: {out_path.stat().st_size / 1024 / 1024:.1f} MB")

# 同时生成一个精简版（只保留英文，适合语料分析）
compact = {}
for sk, seasons in all_data.items():
    compact[sk] = {}
    for ek, ep in seasons.items():
        compact[sk][ek] = {
            'title': ep['title'],
            'text': ' '.join(p['en'] for p in ep['lines'])
        }

compact_path = OUTPUT / 'modern-family-compact.json'
with open(compact_path, 'w', encoding='utf-8') as f:
    json.dump(compact, f, ensure_ascii=False)
print(f"   精简版: {compact_path} ({compact_path.stat().st_size / 1024 / 1024:.1f} MB)")
