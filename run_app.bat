@echo off
title BrainQuest - Python Quiz Application
echo =======================================================
echo   BrainQuest Quiz Portal (B.Tech CSE AIML Project)
echo =======================================================
echo Launching Application...

REM Check if Python 3.11 is at the default local path
if exist "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" (
    "%LOCALAPPDATA%\Programs\Python\Python311\python.exe" main.py
    goto end
)

REM Fallback to system python
python main.py

:end
if errorlevel 1 (
    echo.
    echo An error occurred while running the application.
    pause
)
