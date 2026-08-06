# Search Modern Family corpus for hometown-related dialogue
import os
import re
import json

PDF_BASE = r"C:\Users\15869\Desktop\文件\WJ\en\PDF"

# Patterns that indicate REAL hometown-related content
HOMETOWN_PATTERNS = [
    (r"grew\s+up", "grew up"),
    (r"where\s+i\s+was\s+born", "where I was born"),
    (r"back\s+home", "back home"),
    (r"miss\s+(my\s+)?home", "miss home"),
    (r"my\s+hometown", "my hometown"),
    (r"neighborhood\s+", "neighborhood"),
    (r"when\s+i\s+was\s+a\s+kid", "when I was a kid"),
    (r"used\s+to\s+live", "used to live"),
    (r"moved?\s+(here\s+from|from)", "moved from"),
    (r"where\s+i'?m\s+from", "where I'm from"),
    (r"in\s+colombia", "in Colombia"),
    (r"my\s+country", "my country"),
    (r"our\s+old\s+house", "our old house"),
    (r"growing\s+up", "growing up"),
    (r"the\s+old\s+(neighborhood|house)", "the old neighborhood"),
    (r"remember\s+(growing|living|playing)", "remember growing up"),
    (r"raised\s+in", "raised in"),
    (r"born\s+and\s+raised", "born and raised"),
    (r"little\s+town", "little town"),
    (r"from\s+the\s+(south|midwest|east)", "from the south"),
    (r"home\s+town", "home town"),
]

def extract_lines_from_pdf(pdf_path):
    """Extract dialogue lines from MF PDF file."""
    lines = []
    try:
        with open(pdf_path, 'rb') as f:
            content = f.read()
        # Try to decode as text (PDFs of transcripts may have readable text)
        text = content.decode('utf-8', errors='ignore')
        # Also try latin-1
        if len(text) < 100:
            text = content.decode('latin-1', errors='ignore')
    except Exception as e:
        print(f"  Error reading {pdf_path}: {e}")
        return lines
    return text

def main():
    results = []
    for season_dir in sorted(os.listdir(PDF_BASE)):
        sdir = os.path.join(PDF_BASE, season_dir)
        if not os.path.isdir(sdir):
            continue
        for fname in sorted(os.listdir(sdir)):
            if not fname.lower().endswith('.pdf'):
                continue
            fpath = os.path.join(sdir, fname)
            text = extract_lines_from_pdf(fpath)
            # Search for patterns
            for pat, label in HOMETOWN_PATTERNS:
                for m in re.finditer(pat, text, re.IGNORECASE):
                    # Get surrounding context (300 chars before/after)
                    start = max(0, m.start() - 250)
                    end = min(len(text), m.end() + 350)
                    context = text[start:end].replace('\r', ' ').replace('\n', ' ')
                    # Clean whitespace
                    context = re.sub(r'\s+', ' ', context)
                    results.append({
                        'source': fname.replace('.pdf', ''),
                        'pattern': label,
                        'context': context,
                    })
                    break  # one match per pattern per file

    # Deduplicate
    seen = set()
    unique = []
    for r in results:
        key = r['context'][:80].lower()
        if key not in seen:
            seen.add(key)
            unique.append(r)

    print(f"Found {len(unique)} hometown-related segments\n")
    for i, r in enumerate(unique[:60]):
        print(f"[{i+1}] {r['source']} (pattern: {r['pattern']})")
        print(f"  {r['context'][:280]}")
        print()

if __name__ == '__main__':
    main()
