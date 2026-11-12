@echo off
chcp 65001 >nul
cd /d "%~dp0"
title physics-animator-lab 一键发布

set "PYCMD="
py -3 -V >nul 2>&1
if not errorlevel 1 set "PYCMD=py -3"
if not defined PYCMD (
    python -V >nul 2>&1
    if not errorlevel 1 set "PYCMD=python"
)
if not defined PYCMD (
    echo [错误] 未找到 Python 3，请先安装 Python 后再运行。
    pause
    exit /b 1
)

%PYCMD% "%~dp0deploy.py"
echo.
pause
