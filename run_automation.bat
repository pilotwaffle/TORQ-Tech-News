@echo off
REM MIT Sloan Review - Automation Agent Runner
REM This script runs the automation agent to update the landing page

echo ============================================================
echo MIT Sloan Review - Running Automation Agent
echo ============================================================
echo.

"E:\Python\Python311\python.exe" "%~dp0automation_agent.py"

echo.
echo ============================================================
echo Done! Press any key to exit...
pause >nul
