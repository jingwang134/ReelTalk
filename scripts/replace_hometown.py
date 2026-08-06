# Replace hometown entries in ielts-speak-lab.html
import re

with open('hometown_js.txt', 'r', encoding='utf-8') as f:
    new_block = f.read().rstrip()

with open('ielts-speak-lab.html', 'r', encoding='utf-8') as f:
    html = f.read()

# Find the hometown array: from '"hometown": [' to the next '"xxx": [' at same nesting
start_marker = '  "hometown": ['
start_idx = html.index(start_marker)

# Find the next topic key at 2-space indent (end of hometown array)
# Pattern: '\n  "other-topic": [' after the hometown block
end_pattern = re.compile(r'\n  "[a-z_-]+": \[\n')
end_match = end_pattern.search(html, start_idx + len(start_marker))
if not end_match:
    print("ERROR: could not find end of hometown array")
    exit(1)

end_idx = end_match.start()

print(f"Replacing hometown block: lines {html[:start_idx].count(chr(10))+1} to {html[:end_idx].count(chr(10))+1}")
print(f"Old block length: {end_idx - start_idx} chars")
print(f"New block length: {len(new_block)} chars")

# Replace: keep the leading 2-space indent for the key, replace content
new_html = html[:start_idx] + new_block + html[end_idx:]
# Fix: new_block starts with '"hometown": [' but the original had '  "hometown": ['
# We removed everything from start_idx which includes the 2-space indent. Add it back.
if not new_block.startswith('  '):
    new_block_indented = '  ' + new_block.replace('\n', '\n  ')
else:
    new_block_indented = new_block
new_html = html[:start_idx] + new_block_indented + html[end_idx:]

with open('ielts-speak-lab.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print("Done! Hometown entries replaced.")
