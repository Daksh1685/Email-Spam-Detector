@echo off
REM Email Spam Detection System - Startup Script
REM This script launches the Flask web application

echo.
echo ========================================================================
echo   Email Spam Detection with Machine Learning
echo   Powered by Machine Learning
echo ========================================================================
echo.

REM Change to project directory
cd /d "%~dp0"

REM Display menu
echo Choose what to run:
echo.
echo 1. Run Web Application (Interactive UI) - RECOMMENDED
echo 2. Run Python Script (Analysis Only)
echo 3. Exit
echo.

set /p choice="Enter your choice (1-3): "

if "%choice%"=="1" goto run_web
if "%choice%"=="2" goto run_script
if "%choice%"=="3" goto exit_script
goto invalid_choice

:run_web
echo.
echo Starting Flask Web Application...
echo.
echo Warming up model (this may take a minute on first run)...
echo.
.\.venv\Scripts\python.exe app.py
goto end

:run_script
echo.
echo Running Email Spam Detection Analysis...
echo.
.\.venv\Scripts\python.exe Email_Spam_Detection_with_Machine_Learning.py
goto end

:invalid_choice
echo.
echo Invalid choice! Please enter 1, 2, or 3.
echo.
goto run_web

:exit_script
exit /b 0

:end
pause
