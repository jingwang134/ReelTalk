"""Fix ALL embedded ASCII quotes in translation values. Handles multi-line dict format."""
import re, sys

FILE = r'C:\Users\15869\WorkBuddy\2026-08-05-10-43-07\scripts\v5_final_translations.py'

with open(FILE, 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
fixed = 0

for i, line in enumerate(lines):
    stripped = line.strip()
    # Translation value lines: start with ", end with ",
    if not (stripped.startswith('"') and stripped.endswith('",')):
        continue
    
    # The value is between the first " and the last ",
    # But the line is: spaces + " + value + ",
    # Find the value portion: from first " to last ",
    first_quote = line.index('"')
    last_quote_comma = line.rindex('",')
    value = line[first_quote+1:last_quote_comma]
    
    # Check if value contains any ASCII "
    if '"' not in value:
        continue
    
    # Find all " in value and replace pairs with corner brackets
    new_value_chars = list(value)
    quote_positions = [j for j, ch in enumerate(value) if ch == '"']
    bracket_on = False
    for pos in quote_positions:
        new_value_chars[pos] = '\u300d' if bracket_on else '\u300c'
        bracket_on = not bracket_on
    
    new_value = ''.join(new_value_chars)
    new_line = line[:first_quote+1] + new_value + line[last_quote_comma:]
    lines[i] = new_line
    fixed += 1
    print(f'Fixed line {i+1}: {new_value[:100]}...')

with open(FILE, 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'\nFixed {fixed} lines')

# Verify
with open(FILE, 'r', encoding='utf-8') as f:
    code = f.read()
try:
    compile(code, FILE, 'exec')
    print('Python syntax: OK')
except SyntaxError as e:
    print(f'Still has error at line {e.lineno}: {e.msg}')
    sys.exit(1)
