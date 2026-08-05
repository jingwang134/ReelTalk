# ReelTalk — 项目记忆

## 产品
- **名称**：ReelTalk（reel 电影胶片 + talk，押头韵，点题"从影视/综艺/访谈学口语"）
- **文件**：`ielts-speak-lab.html`（单页应用，LocalStorage 持久化）
- **定位**：雅思口语话题卡片工作台，从任意语料中学习说话风格 → 生成多风格答案 → 多邻国式游戏化练习

## 核心机制
- 语料分析引擎：词频 / N-gram / 句首模式 / 话语标记 / 句式 / 正式度 / 语气基调 / 签名表达
- 动态风格档案：用户自建自命名，聚合语料形成 style DNA
- 风格迁移：基于 DNA 对基础答案做 7 步变换（非模板套用）
- 游戏化：XP / 连续打卡 / 每日目标 / 星星评级 / 心心系统 / 闪卡复习
- 分步练习：READ → LISTEN → SPEAK（语音识别打分）→ COLLECT → COMPLETE

## 用户偏好
- 不满意硬编码模板，要求"从语料真正学习风格"
- 视觉参考多邻国（绿#58cc02 配色、3D 按键、弹跳动效）
- 起名要"好听"——最终在 SpeakEasy/CueCard/ReelTalk/BingeSpeak 中选 ReelTalk
