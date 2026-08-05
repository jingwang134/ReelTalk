# ReelTalk 同步脚本 (Windows)
# 双击运行，自动拉取+提交+推送所有修改

@echo off
cd /d "%~dp0"
echo.

REM 检查是否初次使用
if not exist ".git" (
    echo 第一次使用，正在克隆仓库...
    git clone git@github.com:jingwang134/ReelTalk.git .
    echo 克隆完成！
    pause
    exit /b
)

echo ===== ReelTalk 同步 =====
echo.

echo [1/3] 拉取远程最新代码...
git pull origin main

echo.
echo [2/3] 提交本地修改...
git add -A
git commit -m "auto sync" 2>nul
if %errorlevel% equ 1 (
    echo 没有需要提交的修改
) else (
    echo 已提交
)

echo.
echo [3/3] 推送到 GitHub...
git push origin main

echo.
echo ===== 同步完成 =====
echo.
pause
