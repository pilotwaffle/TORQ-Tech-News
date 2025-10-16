@echo off
echo ============================================================
echo MIT Sloan Review - Full Web Application
echo ============================================================
echo.
echo Starting Flask server...
echo.
echo Main site: http://localhost:5000
echo Admin dashboard: http://localhost:5000/admin
echo API: http://localhost:5000/api/analytics
echo.
echo Press Ctrl+C to stop the server
echo ============================================================
echo.

cd /d "%~dp0"
"E:\Python\Python311\python.exe" app.py

pause
