# ReelTalk

> 从影视学说话 — 雅思口语话题卡片工作台

喂美剧/综艺/访谈语料 → 自动学习说话风格 → 多邻国式游戏化跟练

## 打开即用

双击 `ielts-speak-lab.html` 在浏览器中打开，所有数据存储在浏览器本地。

## 多台电脑同步

### 初次使用（每台电脑只需一次）

**1. 配置 SSH key**

```bash
ssh-keygen -t ed25519 -C "你的标识@email.com"
cat ~/.ssh/id_ed25519.pub
# 复制输出，粘贴到 https://github.com/settings/ssh/new
```

**2. 克隆仓库**

```bash
git clone git@github.com:jingwang134/ReelTalk.git
cd ReelTalk
```

### 日常同步（改完代码后）

| 系统 | 操作 |
|---|---|
| **Windows** | 双击 `sync.bat` |
| **Mac** | 终端里跑 `./sync.sh` |

脚本会自动：拉取最新代码 → 提交你的修改 → 推送到 GitHub。每次开电脑先跑一次拉最新，改完跑一次推上去。
