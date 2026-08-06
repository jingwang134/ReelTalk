"""
v3: 为每个话题设计 Native Speaker 内容思维框架。
生成 TOPIC_THINKING 数据，嵌入 HTML 的阅读跟练区。
"""

import json, sys, os, re

# ============================================================
# 22 个话题的思维框架
# 每个话题 3-5 个思维角度 + 一个整体表达框架
# ============================================================
TOPIC_THINKING = {
    "food": {
        "label": "Food & Cooking",
        "angles": [
            {
                "angle": "从个人记忆/家庭故事切入",
                "detail": "Native speakers almost never start with 'My favorite food is...' They lead with a specific memory — grandma's kitchen, a trip where they first tried it, a funny cooking disaster. This makes your answer instantly personal and relatable."
            },
            {
                "angle": "描述感官细节而非空洞评价",
                "detail": "Instead of 'it tastes good', describe texture (crispy, tender, melt-in-your-mouth), smell (aromatic, smoky), appearance (golden-brown, vibrant), and even sound (sizzling, crunchy). Sensory language = high-score vocabulary."
            },
            {
                "angle": "连接文化或情感意义",
                "detail": "Every dish has a story — comfort food from childhood, a dish that brings family together, something you only eat during a festival. This adds depth beyond 'I like it' and shows cultural awareness."
            },
            {
                "angle": "用对比让表达更立体",
                "detail": "Contrast homemade vs. restaurant, traditional vs. modern fusion, or your country's version vs. the original. Contrast is one of the easiest ways to sound analytical and thoughtful."
            }
        ],
        "framework": "个人记忆引入 → 感官细节描述 → 文化/情感连接 → 对比或个人推荐"
    },

    "travel": {
        "label": "Travel",
        "angles": [
            {
                "angle": "用具体瞬间开场，而非目的地列表",
                "detail": "Don't list where you went. Open with one vivid moment: 'I'll never forget standing at the edge of...' or 'The first thing that hit me was the smell of...' This is the native speaker instinct — story first, facts later."
            },
            {
                "angle": "Surprise 是最有力的叙事引擎",
                "detail": "Native speakers love the 'expectation vs. reality' structure. What surprised you? What was different from what you imagined? This shows reflection and keeps the answer interesting."
            },
            {
                "angle": "人比地点更值得讲",
                "detail": "A random encounter with a local, a funny miscommunication, someone who helped you — these human moments make travel answers memorable. Places are the backdrop; people are the story."
            },
            {
                "angle": "反思你带走了什么",
                "detail": "End with what changed in you: 'That trip taught me that...' or 'I came back with a different perspective on...' This elevates a travel answer from description to insight."
            }
        ],
        "framework": "一个具体瞬间 → 期待与现实的落差 → 遇到的人 → 你带回来的改变"
    },

    "family": {
        "label": "Family",
        "angles": [
            {
                "angle": "选一个人+一件事，不讲全家福",
                "detail": "The biggest mistake is describing your whole family like a list. Pick ONE person and ONE specific memory or habit. 'My dad has this thing where every Sunday morning he...' — this is how natives do it."
            },
            {
                "angle": "Show, don't tell 人物性格",
                "detail": "Don't say 'my mom is kind'. Describe a moment: 'Whenever I was sick, she'd stay up and make this terrible-tasting herbal soup...' Actions reveal character better than adjectives."
            },
            {
                "angle": "诚实比完美更有共鸣",
                "detail": "Families are complicated. A small conflict, an annoying habit, or how your relationship changed over time — these imperfect details make answers feel real, not rehearsed."
            },
            {
                "angle": "上升到普遍主题",
                "detail": "End by connecting your personal family story to something universal: growing up, sacrifice, tradition, forgiveness. This shows maturity and depth of thought."
            }
        ],
        "framework": "一个人物引入 → 一个具体故事 → 关系中的不完美 → 上升到普遍主题"
    },

    "book-movie": {
        "label": "Books & Movies",
        "angles": [
            {
                "angle": "不要复述情节",
                "detail": "Native speakers NEVER summarize the plot in exam answers. Instead, describe the experience of watching/reading: how it made you feel, what stuck with you after it ended."
            },
            {
                "angle": "选一个元素深入，不是覆盖全片",
                "detail": "Pick one thing — a character arc, a specific scene, a theme, the visual style — and go deep on that. One well-explained point beats five shallow ones."
            },
            {
                "angle": "连接到你的生活",
                "detail": "'This movie reminded me of...' or 'I saw myself in the character because...' Personal connection is what examiners reward. It shows you engaged with the work, not just consumed it."
            },
            {
                "angle": "为什么它重要，而非它讲了什么",
                "detail": "End with significance: why this story matters, what you learned, who else should watch/read it and why. This shifts from description to analysis."
            }
        ],
        "framework": "观看/阅读体验 → 聚焦一个元素 → 个人连接 → 为什么重要"
    },

    "childhood-memory": {
        "label": "Childhood Memories",
        "angles": [
            {
                "angle": "感官细节先行",
                "detail": "Childhood memories are sensory-rich. Start with a smell, a sound, the feel of something. 'I can still smell the rain on the pavement outside my kindergarten...' — instantly transports the listener."
            },
            {
                "angle": "儿童视角 vs. 成人回望",
                "detail": "The best childhood stories toggle between the child's limited understanding and the adult's retrospective wisdom: 'At the time I thought it was the end of the world, but looking back...'"
            },
            {
                "angle": "选一个瞬间，不是一段时期",
                "detail": "'When I was a kid' is too broad. Zoom into a specific afternoon, one event, a particular object. The more specific, the more universal the feeling becomes."
            },
            {
                "angle": "情感对比让记忆立体",
                "detail": "Mix emotions — a happy memory with a tinge of sadness (because it's gone), a scary moment that's now funny. Emotional complexity is a hallmark of mature English expression."
            }
        ],
        "framework": "感官细节开场 → 当时怎么想的 → 现在怎么看 → 情感层次"
    },

    "education": {
        "label": "Education",
        "angles": [
            {
                "angle": "个人经历 > 制度评价",
                "detail": "Don't lecture about 'the education system'. Tell a story about a specific teacher, a class that changed you, a moment of breakthrough or frustration. Personal makes it real."
            },
            {
                "angle": "用'人'驱动叙事",
                "detail": "The teacher who believed in you, the classmate you competed with, the moment someone said something that stuck. Education stories are always people stories in disguise."
            },
            {
                "angle": "你后悔没学到什么",
                "detail": "Talking about gaps — life skills school didn't teach, a subject you wish you'd taken — shows self-awareness and is a conversation-friendly angle."
            },
            {
                "angle": "分数之外的收获",
                "detail": "What did you learn beyond the syllabus? Teamwork from group projects, discipline from deadlines, curiosity from a great question. This elevates your answer beyond academic talk."
            }
        ],
        "framework": "一个人/一堂课引入 → 具体发生了什么 → 反思缺失 → 分数之外的收获"
    },

    "work-study": {
        "label": "Work & Study",
        "angles": [
            {
                "angle": "日常细节比宏大叙事更真实",
                "detail": "Don't talk about 'my career goals'. Describe your actual morning routine, the coffee you drink, the specific task that frustrates you. The mundane is the most relatable."
            },
            {
                "angle": "挑战的具体化",
                "detail": "Not 'it's challenging' — but HOW it's challenging. 'The hardest part is when you spend three days on something and then the requirements change overnight.' Specific pain points show authenticity."
            },
            {
                "angle": "转折点或顿悟时刻",
                "detail": "Every job or study journey has a moment when something clicked. Describe that shift — it's a natural story arc that examiners love."
            },
            {
                "angle": "影响你看世界的方式",
                "detail": "How has your work/study changed how you think? Maybe coding made you more systematic, teaching made you more patient. Connect the skill to personal growth."
            }
        ],
        "framework": "日常细节 → 具体挑战 → 顿悟或转折 → 对你思维方式的影响"
    },

    "hobbies": {
        "label": "Hobbies & Free Time",
        "angles": [
            {
                "angle": "偶然发现的故事最好",
                "detail": "How you discovered your hobby is often more interesting than the hobby itself — a friend dragged you along, you were bored during lockdown, you were terrible at first. Accidental beginnings are inherently charming."
            },
            {
                "angle": "进步的过程而非结果",
                "detail": "Native speakers often talk about the learning curve — being bad at first, the first small victory, the ongoing struggle. This is more engaging than 'I've been doing it for 5 years and I'm good.'"
            },
            {
                "angle": "它给了你工作/学习给不了的东西",
                "detail": "What does your hobby provide that your 'real life' doesn't? Creative outlet? Flow state? Social connection? Pure joy? This contrast shows self-awareness."
            },
            {
                "angle": "一个让你眼睛发亮的瞬间",
                "detail": "Describe one specific moment — finishing a hard climb, nailing a recipe, the first time you played a song all the way through. Joy is contagious in storytelling."
            }
        ],
        "framework": "怎么开始的 → 从笨拙到进步的历程 → 它填补了什么空缺 → 一个高光时刻"
    },

    "music": {
        "label": "Music",
        "angles": [
            {
                "angle": "一首歌 > 一个流派",
                "detail": "Don't say 'I like pop music'. Talk about one specific song and the exact moment you first heard it. Music memories are anchored in time and place — use that."
            },
            {
                "angle": "情绪连接先于技术描述",
                "detail": "Native speakers don't analyze chord progressions. They describe feelings: 'This song got me through a rough breakup' or 'It's the song we always played on road trips.' Emotion first."
            },
            {
                "angle": "品味的演变",
                "detail": "How your music taste changed over time is a natural conversation arc: 'I went through a phase where I only listened to... and now I can't believe I did.' Shows growth and humor."
            },
            {
                "angle": "音乐做了其他东西做不到的事",
                "detail": "What does music do to you that nothing else can? Instantly change your mood? Bring back memories? Make you feel understood? This is what native speakers reflect on."
            }
        ],
        "framework": "一首歌 + 一个场景 → 情绪连接 → 品味如何演变 → 音乐的独特力量"
    },

    "sports": {
        "label": "Sports & Exercise",
        "angles": [
            {
                "angle": "从个人参与切入，不完全旁观",
                "detail": "Even if you're not athletic, talk about trying something, failing at PE class, or walking. Direct experience — however modest — is always more engaging than 'I watch football sometimes.'"
            },
            {
                "angle": "一场具体比赛的情感过山车",
                "detail": "If you mention watching sports, narrate one game — the tension, the turning point, how you felt when it ended. Sports are emotional stories, not statistics."
            },
            {
                "angle": "运动教了你什么",
                "detail": "Discipline, resilience, teamwork, handling loss — sports are a metaphor for life skills. Native speakers naturally pivot from 'I play X' to 'and it taught me that...'"
            },
            {
                "angle": "社区感和社会连接",
                "detail": "The friends you made, the post-game chats, the shared ritual of watching with family. Sport as social glue is a rich and underexplored angle in IELTS answers."
            }
        ],
        "framework": "个人参与经历 → 一场比赛的叙事 → 运动教会你的 → 社交连接"
    },

    "tech": {
        "label": "Technology",
        "angles": [
            {
                "angle": "一个具体设备/应用改变了你的日常",
                "detail": "Don't talk about 'technology' in the abstract. Pick one device or app and describe your life before and after it. The before/after contrast is the simplest and most effective framework."
            },
            {
                "angle": "人味比功能更重要",
                "detail": "How does tech affect your actual relationships? Easier to stay in touch, or harder to have real conversations? The human impact angle shows critical thinking beyond 'it's convenient.'"
            },
            {
                "angle": "诚实的矛盾态度最可信",
                "detail": "Native speakers rarely give black-and-white tech opinions. Love the convenience, hate the addiction. The ambivalence is what makes the answer sound mature and thoughtful."
            },
            {
                "angle": "你给自己定的规矩",
                "detail": "Do you have tech rules? No phone at dinner? Screen time limits? Personal boundaries around tech show self-awareness and give concrete examples."
            }
        ],
        "framework": "一个具体设备 → Before/After 对比 → 对人的关系的影响 → 你的个人边界"
    },

    "social-media": {
        "label": "Social Media",
        "angles": [
            {
                "angle": "矛盾心态是最真实的态度",
                "detail": "Nobody genuinely loves or hates social media 100%. Native speakers naturally express ambivalence: 'I know I spend too much time on it, but it's also how I keep up with old friends...' Honest tension is compelling."
            },
            {
                "angle": "一个具体的连接或孤立时刻",
                "detail": "A message from an old friend that made your day, or scrolling through happy posts when you felt alone — one concrete example is worth ten general opinions."
            },
            {
                "angle": "改变了你的沟通方式",
                "detail": "How is your communication different now? Quicker but shallower? More visual? More performative? Reflect on the shift, not just whether it's good or bad."
            },
            {
                "angle": "真实生活 vs. 展示生活",
                "detail": "The gap between what people post and what their life actually looks like. This is a sophisticated angle that native speakers frequently use, mixing personal observation with social commentary."
            }
        ],
        "framework": "矛盾态度表态 → 一个具体时刻 → 沟通方式的改变 → 真实vs展示"
    },

    "environment": {
        "label": "Environment",
        "angles": [
            {
                "angle": "从身边开始，不讲大道理",
                "detail": "Don't lecture about climate change. Start with something you saw in your own community — a polluted river, plastic on the beach, clearer skies during lockdown. Local and personal always wins."
            },
            {
                "angle": "个人的代价感",
                "detail": "Talk about what environmental harm costs YOU personally — not abstract 'save the planet' rhetoric. 'The lake I grew up swimming in is now too dirty' hits harder than any statistic."
            },
            {
                "angle": "你做的具体改变（包括失败的）",
                "detail": "Even small changes count — carrying a reusable bag, eating less meat, trying and failing to go zero-waste. Honesty about the difficulty is more relatable than virtue signaling."
            },
            {
                "angle": "便利与良知之间的张力",
                "detail": "Plastic is convenient, flying is amazing, AC feels great — acknowledging this tension makes you sound thoughtful rather than preachy. This is how native speakers navigate this topic."
            }
        ],
        "framework": "身边的观察 → 个人的代价 → 你做的小改变 → 便利vs良知的矛盾"
    },

    "person-admire": {
        "label": "A Person You Admire",
        "angles": [
            {
                "angle": "一个具体的启发时刻，不是简历",
                "detail": "Don't list their achievements. Describe one moment when this person said or did something that changed how you think. Admiration is a story, not a CV."
            },
            {
                "angle": "突破模板人物",
                "detail": "Parents and teachers are fine — but a less obvious choice (a friend, a stranger you met once, a historical figure you discovered on your own) is inherently more interesting."
            },
            {
                "angle": "你试图模仿的具体品质",
                "detail": "Not 'they're hardworking' — but ONE specific quality you actively try to practice. 'She has this way of making everyone in the room feel heard, and I'm trying to learn that.' Actionable admiration."
            },
            {
                "angle": "崇拜是会变化的",
                "detail": "If relevant, talk about how your admiration evolved — maybe you once admired someone for success, now you admire different things. Growth in what you value is a mature reflection."
            }
        ],
        "framework": "一个启发时刻 → 具体品质（非履历） → 你如何尝试模仿 → 崇拜的演变"
    },

    "skill-learned": {
        "label": "A Skill You Learned",
        "angles": [
            {
                "angle": "决定的瞬间",
                "detail": "Why did you start? Boredom, necessity, a bet, a crush who was into it? The origin story is often more interesting than the skill itself — and native speakers always lead with it."
            },
            {
                "angle": "狼狈的失败时刻是最佳素材",
                "detail": "The time you burned the cake, crashed the bike, deleted the database. Embarrassing failures are inherently funny and relatable. They also set up a great triumph arc."
            },
            {
                "angle": "突破点/Aha moment",
                "detail": "Describe the exact moment when it clicked — suddenly the chord changes felt natural, the code started making sense. This is the emotional peak of any learning story."
            },
            {
                "angle": "改变了你看自己的方式",
                "detail": "Learning a skill changes your self-perception: 'I never thought I was a creative person until...' or 'It taught me that I can stick with something.' This is the deeper payoff."
            }
        ],
        "framework": "为什么开始 → 狼狈失败 → 突破时刻 → 自我认知的改变"
    },

    "hometown": {
        "label": "Hometown",
        "angles": [
            {
                "angle": "感官细节：一座城市的气味和声音",
                "detail": "Every place has a sensory signature — the smell of street food at night, the sound of a particular bird, the quality of light in the afternoon. Lead with senses, not facts."
            },
            {
                "angle": "一个对你意义特殊的角落",
                "detail": "Not the famous landmarks — a bench in a park, a specific street corner, your old school gate. Places with personal history make your hometown uniquely yours."
            },
            {
                "angle": "外来者会注意到但本地人习以为常的事",
                "detail": "What do visitors comment on? The friendliness, the chaos, the food, the pace? This outsider perspective shows you've thought about your hometown from a distance."
            },
            {
                "angle": "又爱又恨的关系",
                "detail": "Every local has a complicated relationship with their hometown. What annoys you about it? What do you miss when you're away? This tension is universally relatable."
            }
        ],
        "framework": "感官特征 → 你私人的角落 → 外人视角 → 又爱又恨"
    },

    "culture": {
        "label": "Culture & Tradition",
        "angles": [
            {
                "angle": "一个具体的习俗/行为，不是泛泛而谈",
                "detail": "Pick ONE specific tradition or practice — how your family celebrates a holiday, a superstition your grandmother follows, a food with a backstory. One deep example beats five shallow ones."
            },
            {
                "angle": "习俗背后的 WHY",
                "detail": "Don't just describe what people do — explain the meaning. Why do people give red envelopes? Why bow instead of shake hands? The 'why' is where cultural insight lives."
            },
            {
                "angle": "你向外人解释时的困境",
                "detail": "Ever tried to explain something from your culture to a foreigner and realized how strange it sounds? These cross-cultural confusion moments are gold. They show you see your own culture from the outside."
            },
            {
                "angle": "长大后才懂的东西",
                "detail": "A tradition you rolled your eyes at as a kid but now appreciate. Generational perspective shift is a sophisticated angle that shows personal growth and cultural depth."
            }
        ],
        "framework": "一个具体习俗 → 背后的意义 → 向外人解释的趣事 → 长大后才明白"
    },

    "weather": {
        "label": "Weather & Seasons",
        "angles": [
            {
                "angle": "一段具体的天气记忆",
                "detail": "Weather is a universal small-talk topic because everyone has weather memories — that snow day as a kid, a terrifying storm, the first day it felt like autumn. Pick one vivid moment."
            },
            {
                "angle": "天气如何真正影响你的情绪和日常",
                "detail": "Not just 'rain makes me sad' — but the actual chain of events: rain means canceled plans means staying in with a book means a different kind of nice day. Trace the real impact."
            },
            {
                "angle": "你所在地区天气的'性格'",
                "detail": "Every place has weather personality — unpredictable spring, brutal summer, endless grey winter. Personifying your local weather is a charming native-speaker move."
            },
            {
                "angle": "小确幸",
                "detail": "The first warm day after winter, the smell of rain on dry ground, the perfect autumn light. Small weather pleasures are cozy, poetic, and easy to describe vividly."
            }
        ],
        "framework": "一个天气记忆 → 天气的真实影响 → 本地天气性格 → 天气中的小确幸"
    },

    "urbanization": {
        "label": "Urbanization & City Life",
        "angles": [
            {
                "angle": "你亲眼目睹的一个变化",
                "detail": "A field that became a mall, a neighborhood that gentrified, a skyline that transformed. Personal witness is infinitely more powerful than statistics about urbanization rates."
            },
            {
                "angle": "失去了什么",
                "detail": "Every gain has a loss — a quiet street, a community that scattered, stars you can no longer see. Native speakers often lead with nostalgia because it's emotionally accessible."
            },
            {
                "angle": "得到了什么",
                "detail": "More jobs, better hospitals, exciting food scenes, diversity. Balance the loss with honest appreciation for what development brought. Neither blind optimism nor pure nostalgia."
            },
            {
                "angle": "节奏的改变",
                "detail": "The pace of life sped up — people walk faster, relationships feel more transactional, you have more options but less time. This sensory observation of 'pace' is a subtle but powerful angle."
            }
        ],
        "framework": "亲眼目睹的变化 → 失去了什么 → 得到了什么 → 生活节奏的改变"
    },

    "memorable-trip": {
        "label": "A Memorable Trip",
        "angles": [
            {
                "angle": "一个决定性时刻，不是行程流水账",
                "detail": "One moment that defines the trip — sunrise over somewhere unexpected, getting lost and finding something amazing, a conversation that stayed with you. One moment, richly told."
            },
            {
                "angle": "出了什么岔子（最好的故事都是事故）",
                "detail": "Lost luggage, missed trains, language barriers, food poisoning. Travel disasters are the most memorable and relatable stories. Native speakers lean into these, not away from them."
            },
            {
                "angle": "你带了多少没用上的东西",
                "detail": "Over-packing is a universal travel truth. What you packed vs. what you actually needed is a light, humorous angle that shows self-awareness."
            },
            {
                "angle": "回来后看世界不一样了",
                "detail": "How did the trip change your perspective? Maybe you became more patient, more grateful, more curious. The transformation is the 'so what' of any travel story."
            }
        ],
        "framework": "一个决定性的时刻 → 出岔子的故事 → 带了多少没用的东西 → 回来的改变"
    },

    "difficult-decision": {
        "label": "A Difficult Decision",
        "angles": [
            {
                "angle": "清晰地铺设 stakes",
                "detail": "Before describing the decision, make the listener feel what was at stake. What would you lose either way? Who else was affected? The weight of the choice must be clear before the resolution."
            },
            {
                "angle": "危机时刻：选择前的那个瞬间",
                "detail": "Describe the moment right before you decided — the sleepless night, the conversation that tipped the scale, the thing you realized in the shower. That liminal moment is the emotional core."
            },
            {
                "angle": "你是怎么选出来的",
                "detail": "Logic? Gut feeling? Advice from someone? A coin toss? The decision-making process itself is what examiners want to hear — it reveals how you think."
            },
            {
                "angle": "现在回头看",
                "detail": "Would you make the same choice? Maybe yes but for different reasons. Maybe no and here's what you learned. Hindsight perspective shows maturity and completes the story arc."
            }
        ],
        "framework": "铺设 stakes → 选择前的瞬间 → 怎么选的 → 回头看"
    },

    "work-life": {
        "label": "Work-Life Balance",
        "angles": [
            {
                "angle": "一个具体的日常张力",
                "detail": "Not 'balance is important' — but a real friction: checking emails during dinner, missing a family event for a deadline, the guilt of leaving early. Specific tensions make abstract concepts real."
            },
            {
                "angle": "你的'平衡'长什么样",
                "detail": "Balance means different things to different people. Describe YOUR version: maybe it's no work on Sundays, maybe it's leaving at 6 no matter what, maybe it's flexible hours. Personal definition beats generic advice."
            },
            {
                "angle": "文化差异的观察",
                "detail": "Different countries have different expectations about work. If you've experienced multiple work cultures, the contrast is rich material for comparative reflection."
            },
            {
                "angle": "你改变的一件事",
                "detail": "Talk about one specific change you made — a boundary you set, a habit you broke, a mindset shift. Action is more persuasive than philosophy."
            }
        ],
        "framework": "一个具体张力 → 你定义的平衡 → 文化差异观察 → 你做的改变"
    },
}

# ============================================================
# Output as JS
# ============================================================
output_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'topic-thinking.js')
with open(output_path, 'w', encoding='utf-8') as f:
    f.write('// Auto-generated by v3_topic_thinking.py\n')
    f.write('// Native speaker content thinking frameworks for each IELTS topic\n')
    f.write('const TOPIC_THINKING = ')
    json.dump(TOPIC_THINKING, f, ensure_ascii=False, indent=2)
    f.write(';\n')

print(f"Generated {output_path}")
print(f"Topics: {len(TOPIC_THINKING)}")

# Verify all angles exist
for tid, data in TOPIC_THINKING.items():
    n = len(data['angles'])
    print(f"  {tid}: {n} angles, framework={data['framework'][:40]}...")
