@echo off
REM Shamll Tech PDF Extractor - Run Script
title PDF Extractor - Shamll Tech

REM تحقق من وجود Python
where python >nul 2>nul
if %errorlevel% neq 0 (
    echo.
    echo ❌ Python is not installed or not added to PATH.
    echo 🔗 Download Python: https://www.python.org/downloads/
    pause
    exit /b
)

REM تشغيل السكربت
echo.
echo 🚀 Starting PDF Extractor GUI...
python pdf_extractor_gui.py

pause
