@echo off
REM Fortini Engine - Run All (Windows)
SETLOCAL ENABLEDELAYEDEXPANSION

echo =============================================
echo Fortini Engine - Run All (Windows)
echo =============================================





echo Fim.
pauseecho Iniciando playall.py...
python playall.pyecho Instalando dependencias...
python -m pip install -r requirements.txt || echo "Aviso: pip install falhou"
:SKIP_INSTALLecho Python encontrado:
python --version

set /p INSTALL=Instalar dependencias (pip install -r requirements.txt)? [S/n] 
if /I "%INSTALL%"=="N" goto SKIP_INSTALL:: Encontrar Python
where python >nul 2>&1
if %ERRORLEVEL% NEQ 0 (
    echo Python nao encontrado. Instale Python 3.10+ e marque 'Add Python to PATH'.
    pause
    exit /b 1
)