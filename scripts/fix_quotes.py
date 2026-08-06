"""Fix embedded ASCII double quotes in translation strings."""
import re

with open(r'C:\Users\15869\WorkBuddy\2026-08-05-10-43-07\scripts\v5_final_translations.py', 'r', encoding='utf-8') as f:
    content = f.read()

lines = content.split('\n')
fixed_count = 0

for i, line in enumerate(lines):
    stripped = line.strip()
    # Match translation value lines: starts with ", ends with ",
    if stripped.startswith('"') and stripped.endswith('",'):
        dq_count = stripped.count('"')
        if dq_count > 4:
            # Has embedded ASCII double quotes in the Chinese translation
            # Find the value portion (between ": " and the final ",)
            sep_match = re.search(r'":\s+"', line)
            if sep_match:
                value_start = sep_match.end()  # after the opening quote of value
                last_comma = line.rfind('",')
                value_content = line[value_start:last_comma]

                # Replace embedded ASCII " with corner bracket pairs
                result = []
                quote_on = False
                for ch in value_content:
                    if ch == '"':
                        result.append('\u300d' if quote_on else '\u300c')
                        quote_on = not quote_on
                    else:
                        result.append(ch)
                new_value = ''.join(result)

                new_line = line[:value_start] + new_value + line[last_comma:]
                lines[i] = new_line
                fixed_count += 1
                print(f'  Fixed: {new_line[:100]}...')

# Write back
with open(r'C:\Users\15869\WorkBuddy\2026-08-05-10-43-07\scripts\v5_final_translations.py', 'w', encoding='utf-8') as f:
    f.write('\n'.join(lines))

print(f'\nFixed {fixed_count} lines total')
