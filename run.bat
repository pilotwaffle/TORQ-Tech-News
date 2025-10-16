@echo off
REM MIT Sloan Review - One-Click Launcher
REM Starts the complete system with one command

cls
echo ============================================================
echo MIT Sloan Management Review
echo Complete Web Application Launcher
echo ============================================================
echo.

REM Kill any existing Flask processes on port 5000
echo [1/3] Cleaning up old processes...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do taskkill //F //PID %%a 2>nul
timeout /t 2 /nobreak >nul

REM Start Flask server
echo [2/3] Starting web server...
start "MIT Sloan Server" cmd /k "cd /d "%~dp0" && "E:\Python\Python311\python.exe" app.py"
timeout /t 3 /nobreak >nul

REM Open browser
echo [3/3] Opening browser...
start http://localhost:5000

echo.
echo ============================================================
echo [SUCCESS] MIT Sloan Review is now running!
echo.
echo Main Site:    http://localhost:5000
echo Admin Panel:  http://localhost:5000/admin
echo.
echo Press any key to stop the server...
echo ============================================================
pause >nul

REM Kill Flask when user presses a key
echo.
echo Stopping server...
for /f "tokens=5" %%a in ('netstat -ano ^| findstr :5000 ^| findstr LISTENING') do taskkill //F //PID %%a
echo Server stopped.
pause
