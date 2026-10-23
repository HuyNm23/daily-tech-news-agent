@echo off
chcp 65001 > nul
title Daily Tech News Agent
echo ================================================================
echo  DANG KHOI DONG AI AGENT SAN TIN CONG NGHE...
echo ================================================================
cd /d "%~dp0"
python main.py
echo.
echo ================================================================
echo  Hoan tat! Dang mo bao cao web tren trinh duyet cua ban...
echo ================================================================
for /f "delims=" %%a in ('dir /b /od reports\*.html') do set "LATEST=reports\%%a"
if defined LATEST (
    start "" "%LATEST%"
)
pause
