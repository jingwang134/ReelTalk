# Generate final hometown replacement data and build JS snippet
import json

HOMETOWN = [
    {
        "function": "开场破题",
        "en": "We're very different. Jay's from the city. He has a big business. I come from a small village. Very poor but very, very beautiful.",
        "highlight": "I come from a small village. Very poor but very, very beautiful.",
        "source": "Modern Family S01E01",
        "translation": "我们很不一样。杰来自大城市，生意做得很大。而我来自一个小村庄，虽然很穷，但非常非常美。",
        "keywords": [
            {"en": "come from a small village", "zh": "来自一个小村庄（描述出生地的经典句式）", "category": "B2 高频表达", "context": "I come from a small village."},
            {"en": "very poor but very, very beautiful", "zh": "虽然很穷但非常美（先抑后扬的对比描述）", "category": "B2 描述句型", "context": "Very poor but very, very beautiful."}
        ]
    },
    {
        "function": "开场破题",
        "en": "When we first met, he wouldn't even look at me... because I was a hick from the farm in Missouri, and he's a big city mouse.",
        "highlight": "I was a hick from the farm in Missouri, and he's a big city mouse.",
        "source": "Modern Family S01E03",
        "translation": "我们第一次见面时，他连看都不看我一眼……因为我是个密苏里州农场来的乡巴佬，而他是个大城市人。",
        "keywords": [
            {"en": "a hick from the farm", "zh": "来自农场的乡巴佬（自嘲式表达出身）", "category": "C1 口语习语", "context": "I was a hick from the farm in Missouri"},
            {"en": "a big city mouse", "zh": "大城市人（与 country mouse 乡巴佬相对）", "category": "C1 口语习语", "context": "he's a big city mouse"}
        ]
    },
    {
        "function": "表达观点",
        "en": "I don't know. I'm from Denver. We don't have a lot of pho there. Uh, just to be sure, could you show me how hard Lily got hit?",
        "highlight": "I'm from Denver. We don't have a lot of pho there.",
        "source": "Modern Family S01E06",
        "translation": "我不知道。我是丹佛人，我们那儿没什么越南米粉。呃，保险起见，你能让我看看莉莉被撞得有多厉害吗？",
        "keywords": [
            {"en": "just to be sure", "zh": "保险起见；为了万无一失", "category": "B2 过渡表达", "context": "just to be sure, could you show me"}
        ]
    },
    {
        "function": "表达观点",
        "en": "I used to live down here, you know. Yeah, that's why I come down here. Look there. That was my old apartment. After I left Javier, that's all I could afford. It's still part of me.",
        "highlight": "That was my old apartment. After I left Javier, that's all I could afford. It's still part of me.",
        "source": "Modern Family S01E18",
        "translation": "你知道吗，我以前就住在这片。对，这就是我常来这边的原因。看那边，那是我以前的公寓��离开哈维尔之后，那是我唯一住得起的地方。它依然是我人生的一部分。",
        "keywords": [
            {"en": "that's all I could afford", "zh": "那是我唯一负担得起的", "category": "B2 表达", "context": "After I left Javier, that's all I could afford."},
            {"en": "It's still part of me", "zh": "它依然是我生命的一部分（对过往的珍视）", "category": "C1 情感表达", "context": "It's still part of me."}
        ]
    },
    {
        "function": "举例说明",
        "en": "Oh, one of my favorite childhood memories was attending the Moscow Marionette Theater. I grew up one mile away from Missouri's largest waterslide. And third largest in the country.",
        "highlight": "One of my favorite childhood memories was attending the Moscow Marionette Theater.",
        "source": "Modern Family S01E12",
        "translation": "哦，我童年最美好的记忆之一就是去看莫斯科木偶剧院的演出。我长大的地方离密苏里州最大的水滑梯只有一英里远。那可是全美第三大的水滑梯。",
        "keywords": [
            {"en": "one of my favorite childhood memories", "zh": "我童年最美好的记忆之一", "category": "B2 表达", "context": "One of my favorite childhood memories was"},
            {"en": "attending the theater", "zh": "去剧院观看演出", "category": "B2 词汇", "context": "attending the Moscow Marionette Theater"}
        ]
    },
    {
        "function": "举例说明",
        "en": "The whole family said you wouldn't take it well. Ever since you moved to the city 'cause you couldn't hack it on the farm. 'Couldn't hack it'? Yeah, that's right.",
        "highlight": "Ever since you moved to the city 'cause you couldn't hack it on the farm.",
        "source": "Modern Family S05E04",
        "translation": "全家人都说你会受不了的。自从你搬到城里，就因为你在农场待不下去。\"待不下去\"？对，没错。",
        "keywords": [
            {"en": "couldn't hack it", "zh": "搞不定；撑不下去", "category": "C1 口语习语", "context": "you couldn't hack it on the farm"},
            {"en": "take it well", "zh": "坦然接受（这件事）", "category": "B2 表达", "context": "you wouldn't take it well"}
        ]
    },
    {
        "function": "比较对比",
        "en": "Christmas in Colombia was always hot and loud, people arguing, betrayal, schemes. So I rented a mountain cabin for the whole family to celebrate my first Christmas as an American.",
        "highlight": "Christmas in Colombia was always hot and loud, people arguing, betrayal, schemes.",
        "source": "Modern Family S07E09",
        "translation": "哥伦比亚的圣诞节总是又热又吵，人们吵来吵去，还有背叛和阴谋。所以我在山上租了间小屋，让全家一起庆祝我作为美国人的第一个圣诞节。",
        "keywords": [
            {"en": "betrayal and schemes", "zh": "背叛与阴谋", "category": "C1 词汇", "context": "people arguing, betrayal, schemes"},
            {"en": "rented a mountain cabin", "zh": "租了一间山间小屋", "category": "B2 词汇", "context": "I rented a mountain cabin for the whole family"}
        ]
    },
    {
        "function": "总结收束",
        "en": "My grandmother, who rests in peace, has been coming to me in my dreams, telling me that I'm losing touch with my roots. In our culture, we believe that the dead are all around us.",
        "highlight": "I'm losing touch with my roots.",
        "source": "Modern Family S02E02",
        "translation": "我的祖母，愿她安息，一直在梦里告诉我，说我渐渐与自己的根源疏远了。在我们的文化里，我们相信逝者就在我们身边。",
        "keywords": [
            {"en": "losing touch with my roots", "zh": "与自己的根源/故乡渐行渐远", "category": "C1 习语", "context": "I'm losing touch with my roots"},
            {"en": "who rests in peace", "zh": "愿她安息（对逝者的敬语）", "category": "B2 表达", "context": "My grandmother, who rests in peace"}
        ]
    },
]

def js_str(s):
    """Escape a string for JS double-quoted literal."""
    return s.replace('\\', '\\\\').replace('"', '\\"')

# Build JS array literal
lines_out = []
lines_out.append('"hometown": [')
for e in HOMETOWN:
    lines_out.append('  {')
    lines_out.append(f'    "function": "{e["function"]}",')
    lines_out.append(f'    "en": "{js_str(e["en"])}",')
    lines_out.append(f'    "highlight": "{js_str(e["highlight"])}",')
    lines_out.append(f'    "source": "{e["source"]}",')
    lines_out.append(f'    "translation": "{js_str(e["translation"])}",')
    lines_out.append('    "keywords": [')
    for k in e["keywords"]:
        lines_out.append('      {')
        lines_out.append(f'        "en": "{js_str(k["en"])}",')
        lines_out.append(f'        "zh": "{js_str(k["zh"])}",')
        lines_out.append(f'        "category": "{k["category"]}",')
        lines_out.append(f'        "context": "{js_str(k["context"])}"')
        lines_out.append('      },')
    lines_out.append('    ]')
    lines_out.append('  },')
lines_out.append('],')

js_block = '\n'.join(lines_out)

# Verify with Node
import subprocess
test_js = 'const TEST = ' + js_block.replace('"hometown": [', '{ "hometown": [', 1) + '; console.log("entries:", TEST.hometown.length);'
test_js = 'const TEST = {' + js_block.replace('"hometown": [', '"hometown": [', 1).rstrip(',').rstrip() + '}; console.log("entries:", TEST.hometown.length);'
# simpler: just wrap
simple = 'const TEST = { ' + js_block + ' }; console.log("entries:", TEST.hometown.length);'
result = subprocess.run(
    ['C:/Users/15869/.workbuddy/binaries/node/versions/22.22.2/node.exe', '-e', simple],
    capture_output=True, text=True, cwd='.'
)
print(result.stdout or result.stderr)

with open('hometown_js.txt', 'w', encoding='utf-8') as f:
    f.write(js_block)
print('JS block written to hometown_js.txt (' + str(len(js_block)) + ' chars)')
print('\n--- PREVIEW ---')
print(js_block[:800])
