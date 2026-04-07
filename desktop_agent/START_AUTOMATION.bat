@echo off
echo ========================================
echo   BUDDY AI - ChatGPT Codex Automation
echo ========================================
echo.

REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python first.
    echo Download from: https://www.python.org/downloads/
    pause
    exit /b 1
)

REM Install dependencies
echo Installing dependencies...
pip install selenium pyautogui pyperclip pygetwindow webdriver-manager Pillow --quiet

echo.
echo Starting automation...
echo.
python chatgpt_codex_automation.py

pause
