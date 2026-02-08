@echo off
REM ============================================================
REM Script para compilar Fortini Engine para EXE no Windows
REM ============================================================

echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║                                                        ║
echo ║  🎮 Compilando Fortini Engine para Windows EXE        ║
echo ║                                                        ║
echo ╚════════════════════════════════════════════════════════╝
echo.

REM Verificar se Python está instalado
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ ERRO: Python não instalado ou não está no PATH
    echo.
    echo Instale Python de: https://www.python.org/
    echo ⚠️  Certifique-se de marcar "Add Python to PATH" durante instalação!
    pause
    exit /b 1
)

echo ✅ Python encontrado
python --version

REM Instalação de dependências
echo.
echo 📦 Instalando dependências...
pip install -q -r requirements.txt

echo 📦 Instalando PyInstaller...
pip install -q pyinstaller

REM Verificar se arquivo spec existe
if not exist "build_windows_exe.spec" (
    echo.
    echo ❌ ERRO: build_windows_exe.spec não encontrado!
    echo Certifique-se que está na pasta raiz do projeto.
    pause
    exit /b 1
)

REM Compilar com PyInstaller
echo.
echo 🔨 Compilando com PyInstaller...
echo (esto pode levar 2-5 minutos...)
echo.

pyinstaller build_windows_exe.spec --distpath=dist --buildpath=build --specpath=.

REM Verificar sucesso
if %errorlevel% equ 0 (
    echo.
    echo ╔════════════════════════════════════════════════════════╗
    echo ║                                                        ║
    echo ║          ✅ SUCESSO! EXE COMPILADO                    ║
    echo ║                                                        ║
    echo ╚════════════════════════════════════════════════════════╝
    echo.
    echo 📁 Arquivo: dist\Fortini Editor\fortini_editor.exe
    echo.
    echo Você pode:
    echo   1. Executar agora: dist\Fortini Editor\fortini_editor.exe
    echo   2. Copiar a pasta dist\Fortini Editor\ para qualquer lugar
    echo   3. Criar shortcut no desktop
    echo.
    pause
    start explorer.exe dist
) else (
    echo.
    echo ❌ ERRO ao compilar!
    echo.
    echo Verifique os erros acima.
    pause
    exit /b 1
)
