@echo off
chcp 65001 >nul
cd /d "%~dp0"
set "PYCMD="
py -3 -V >nul 2>&1
if not errorlevel 1 set "PYCMD=py -3"
if not defined PYCMD (
    python -V >nul 2>&1
    if not errorlevel 1 set "PYCMD=python"
)
if not defined PYCMD (
    echo [ERROR] Python 3 not found. Please install Python 3 first.
    pause
    exit /b 1
)
%PYCMD% "%~dp0deploy.py"
echo.
pause
