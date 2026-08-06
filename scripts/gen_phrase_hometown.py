# Generate hometown phrase-centered data (new format) and replace in HTML
import re

# New format: phrase-centered cards
HOMETOWN_PHRASES = [
    {
        "function": "开场破题",
        "phrase": "I come from a small village.",
        "meaning": "我来自一个小村庄",
        "example": "Jay's from the city. He has a big business. I come from a small village. Very poor but very, very beautiful.",
        "source": "Modern Family S01E01",
        "usage": "回答「你的家乡在哪」的标准开场。先说位置，再用 poor but beautiful 这类对比让描述立体、不空洞。",
        "ielts_example": "I come from a small village in Sichuan. It's not famous, but it's very, very peaceful."
    },
    {
        "function": "开场破题",
        "phrase": "a hick from the farm",
        "meaning": "来自农场的乡巴佬（自嘲式表达出身）",
        "example": "When we first met, he wouldn't even look at me... because I was a hick from the farm in Missouri, and he's a big city mouse.",
        "source": "Modern Family S01E03",
        "usage": "自嘲或幽默地描述自己来自乡村，适合 Part 1 聊家乡背景。注意 a hick 带自嘲意味，只能说自己，不能说别人。",
        "ielts_example": "People sometimes assume I'm a hick from the countryside, but my hometown is actually a fairly modern town."
    },
    {
        "function": "表达观点",
        "phrase": "I'm from + 地名. We don't have a lot of + 东西.",
        "meaning": "我是……人，我们那儿没什么……（解释家乡缺少某样东西）",
        "example": "I don't know. I'm from Denver. We don't have a lot of pho there.",
        "source": "Modern Family S01E06",
        "usage": "用「I'm from + 地名 + We don't have a lot of + 东西」解释家乡的饮食/文化特点，适合聊家乡食物或地域差异。",
        "ielts_example": "I'm from a coastal city. We don't have a lot of spicy food there, unlike the inland provinces."
    },
    {
        "function": "表达观点",
        "phrase": "It's still part of me.",
        "meaning": "它依然是我的一部分（对过往的珍视）",
        "example": "That was my old apartment. After I left Javier, that's all I could afford. It's still part of me.",
        "source": "Modern Family S01E18",
        "usage": "表达对家乡/旧居/过往经历的珍视——即使离开了，影响仍在。是 Part 1 家乡话题和 Part 2 记忆类话题的升华句。",
        "ielts_example": "I left my hometown ten years ago, but it's still part of me — the food, the people, the pace of life."
    },
    {
        "function": "举例说明",
        "phrase": "one of my favorite childhood memories",
        "meaning": "我童年最美好的记忆之一",
        "example": "One of my favorite childhood memories was attending the Moscow Marionette Theater. I grew up one mile away from Missouri's largest waterslide.",
        "source": "Modern Family S01E12",
        "usage": "回忆童年/家乡时的经典开场，后面接一个具体故事。适合 Part 2 童年记忆、难忘经历类话题。",
        "ielts_example": "One of my favorite childhood memories was running through the rice paddies near my grandmother's house."
    },
    {
        "function": "举例说明",
        "phrase": "couldn't hack it",
        "meaning": "搞不定；撑不下去（口语）",
        "example": "Ever since you moved to the city 'cause you couldn't hack it on the farm.",
        "source": "Modern Family S05E04",
        "usage": "口语化的「适应不了/撑不住」，解释某人离开某地或放弃某事的原因。适合描述从家乡搬到城市失败的经历。",
        "ielts_example": "I tried living in the city for a year, but honestly, I couldn't hack it — the noise and the pace were too much."
    },
    {
        "function": "比较对比",
        "phrase": "X was always hot and loud",
        "meaning": "家乡的……总是又热又吵（描述故乡特征）",
        "example": "Christmas in Colombia was always hot and loud, people arguing, betrayal, schemes. So I rented a mountain cabin for the whole family to celebrate my first Christmas as an American.",
        "source": "Modern Family S07E09",
        "usage": "用「家乡的 X 总是 + 形容词」描述故乡特征，再对比现在住的地方。是 Part 3 城乡对比、文化差异话题的绝佳句式。",
        "ielts_example": "Festivals in my hometown are always loud and crowded, which is very different from the quiet celebrations here."
    },
    {
        "function": "总结收束",
        "phrase": "losing touch with my roots",
        "meaning": "与自己的根源/故乡渐行渐远",
        "example": "My grandmother, who rests in peace, has been coming to me in my dreams, telling me that I'm losing touch with my roots.",
        "source": "Modern Family S02E02",
        "usage": "表达离开家乡久了、与本源疏远的感慨。适合 Part 3 讨论「年轻人离开家乡的影响」「传统是否被遗忘」。",
        "ielts_example": "Many young people move to big cities and slowly lose touch with their roots — their hometown customs and family traditions."
    },
]

def js_str(s):
    return s.replace('\\', '\\\\').replace('"', '\\"')

# Build JS array
lines_out = ['"hometown": [']
for e in HOMETOWN_PHRASES:
    lines_out.append('  {')
    lines_out.append(f'    "function": "{e["function"]}",')
    lines_out.append(f'    "phrase": "{js_str(e["phrase"])}",')
    lines_out.append(f'    "meaning": "{js_str(e["meaning"])}",')
    lines_out.append(f'    "example": "{js_str(e["example"])}",')
    lines_out.append(f'    "source": "{e["source"]}",')
    lines_out.append(f'    "usage": "{js_str(e["usage"])}",')
    lines_out.append(f'    "ielts_example": "{js_str(e["ielts_example"])}"')
    lines_out.append('  },')
lines_out.append('],')
new_block = '\n'.join(lines_out)

# Verify with Node
import subprocess
test_js = 'const T = { ' + new_block + ' }; console.log("entries:", T.hometown.length, "| has phrase:", T.hometown.every(e=>e.phrase));'
result = subprocess.run(
    ['C:/Users/15869/.workbuddy/binaries/node/versions/22.22.2/node.exe', '-e', test_js],
    capture_output=True, text=True, cwd='.'
)
print(result.stdout or result.stderr)

# Replace in HTML
with open('ielts-speak-lab.html', 'r', encoding='utf-8') as f:
    html = f.read()

start_marker = '  "hometown": ['
start_idx = html.index(start_marker)
end_pattern = re.compile(r'\n  "[a-z_-]+": \[\n')
end_match = end_pattern.search(html, start_idx + len(start_marker))
if not end_match:
    print("ERROR: cannot find end of hometown array")
    exit(1)
end_idx = end_match.start()

new_block_indented = '  ' + new_block.replace('\n', '\n  ')
new_html = html[:start_idx] + new_block_indented + html[end_idx:]

with open('ielts-speak-lab.html', 'w', encoding='utf-8') as f:
    f.write(new_html)

print(f"Replaced hometown block: {html[:end_idx].count(chr(10))-html[:start_idx].count(chr(10))} lines -> new format ({len(HOMETOWN_PHRASES)} phrases)")
