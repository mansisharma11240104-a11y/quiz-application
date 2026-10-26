@echo off
title BrainQuest - Localhost Web Portal
echo =======================================================
echo   BrainQuest Quiz Portal (B.Tech CSE AIML Project)
echo   Localhost Web Server Launcher
echo =======================================================
echo.
echo Starting Flask web server on http://localhost:5000 ...
echo Press Ctrl+C in this window to stop the server.
echo.

REM Check if Python 3.11 is at the default local path
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" app.py
    goto end
)

REM Fallback to system python
python app.py

:end
if errorlevel 1 (
    echo.
    echo An error occurred while launching the web server.
    pause
)
