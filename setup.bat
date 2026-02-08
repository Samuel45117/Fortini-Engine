@echo off
REM Fortini Engine - Quick Setup Script for Windows

echo ========================================
echo  Fortini Engine Setup
echo ========================================
echo.

REM Check Python
echo Checking Python 3.10+...
python --version

REM Install dependencies
echo.
echo Installing dependencies...
pip install -r requirements.txt

REM Install in dev mode
echo.
echo Installing Fortini Engine...
pip install -e .

REM Create documents folder
echo.
echo Setting up project directories...
if not exist "%USERPROFILE%\Fortini Documents\Projects" mkdir "%USERPROFILE%\Fortini Documents\Projects"
if not exist "%USERPROFILE%\Fortini Documents\Logs" mkdir "%USERPROFILE%\Fortini Documents\Logs"

echo.
echo ========================================
echo Setup complete!
echo.
echo To launch the editor, run:
echo   python fortini_editor.py
echo.
echo Or:
echo   python -m fortini_engine.editor.run_editor
echo.
echo Happy gaming!
echo ========================================
pause
