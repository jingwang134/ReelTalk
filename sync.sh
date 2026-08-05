#!/bin/bash
# ReelTalk 同步脚本 (Mac/Linux)
# 双击运行，自动拉取+提交+推送所有修改

cd "$(dirname "$0")"

if [ ! -d ".git" ]; then
    echo "第一次使用，正在克隆仓库..."
    git clone git@github.com:jingwang134/ReelTalk.git .
    echo "克隆完成！按任意键退出"
    read
    exit 0
fi

echo "===== ReelTalk 同步 ====="
echo ""

echo "[1/3] 拉取远程最新代码..."
git pull origin main

echo ""
echo "[2/3] 提交本地修改..."
git add -A
if git commit -m "auto sync" 2>/dev/null; then
    echo "已提交"
else
    echo "没有需要提交的修改"
fi

echo ""
echo "[3/3] 推送到 GitHub..."
git push origin main

echo ""
echo "===== 同步完成 ====="
echo ""
read -p "按 Enter 退出"
