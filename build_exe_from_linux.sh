#!/bin/bash
# ============================================================
# Script para compilar EXE Windows usando PyInstaller no Linux
# Com suporte a cross-compilation
# ============================================================

set -e

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║  🎮 Fortini Engine - Compilador Windows EXE            ║"
echo "║      (Linux → Windows)                                 ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

PROJECT_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_ROOT"

# ============================================================
# OPÇÃO 1: Usar PyInstaller direto (recomendado)
# ============================================================

compile_with_pyinstaller() {
    echo "🔨 Compilando EXE usando PyInstaller..."
    echo ""
    
    # Instalar PyInstaller
    echo "📦 Instalando PyInstaller..."
    pip install -q pyinstaller
    
    # Compilar
    echo "⏳ Compilando... (pode levar 3-5 minutos)"
    pyinstaller build_windows_exe.spec \
        --distpath=dist \
        --buildpath=build_pyinstaller \
        -y
    
    if [ -d "dist/Fortini Editor" ]; then
        return 0
    else
        return 1
    fi
}

# ============================================================
# OPÇÃO 2: Usar CrossCompile com MinGW (avançado)
# ============================================================

compile_with_wine() {
    echo "⚠️  Método experimental: Wine + Python Windows"
    echo ""
    
    if ! command -v wine &> /dev/null; then
        echo "❌ Wine não instalado"
        echo ""
        echo "Instale com:"
        echo "  Ubuntu/Debian: sudo apt-get install wine wine32 wine64 wineboot"
        echo "  Fedora: sudo dnf install wine"
        return 1
    fi
    
    echo "⏳ Preparando Wine environment..."
    
    # Baixar Python embarcado para Windows (se não existir)
    if [ ! -f "python-3.11.6-embed-amd64.zip" ]; then
        echo "📥 Baixando Python embarcado para Windows..."
        wget -q https://www.python.org/ftp/python/3.11.6/python-3.11.6-embed-amd64.zip
    fi
    
    echo "💾 Este método está em desenvolvimento"
    return 1
}

# ============================================================
# OPÇÃO 3: Usar Nuitka (transpiler alternativo)
# ============================================================

compile_with_nuitka() {
    echo "🔨 Compilando EXE usando Nuitka..."
    echo ""
    
    pip install -q nuitka ordered-set zstandard
    
    python -m nuitka \
        --onefile \
        --output-dir=dist_nuitka \
        --windows-icon-from-ico=assets/icon.ico \
        --include-package=fortini_engine \
        --include-package=PyQt6 \
        fortini_engine/editor/run_editor.py
    
    return $?
}

# ============================================================
# MENU PRINCIPAL
# ============================================================

echo "Qual método usar para compilar?"
echo ""
echo "1) PyInstaller (recomendado - rápido e confiável)"
echo "2) Nuitka (alternativo - arquivo único)"
echo "3) Wine (experimental - requer Wine)"
echo ""

read -p "Escolha (1-3): " choice

case $choice in
    1)
        if compile_with_pyinstaller; then
            echo "✅ Sucesso com PyInstaller!"
        else
            echo "❌ Erro com PyInstaller"
            exit 1
        fi
        ;;
    2)
        if compile_with_nuitka; then
            echo "✅ Sucesso com Nuitka!"
        else
            echo "❌ Erro com Nuitka"
            exit 1
        fi
        ;;
    3)
        if compile_with_wine; then
            echo "✅ Sucesso com Wine!"
        else
            echo "❌ Erro com Wine"
            exit 1
        fi
        ;;
    *)
        echo "Opção inválida"
        exit 1
        ;;
esac

# ============================================================
# RESULTADO FINAL
# ============================================================

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║          ✅ WINDOWS EXE COMPILADO COM SUCESSO         ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

if [ -d "dist/Fortini Editor" ]; then
    echo "📁 Localização: dist/Fortini Editor/"
    echo ""
    echo "Conteúdo:"
    ls -lh "dist/Fortini Editor/" | head -10
    echo ""
    
    SIZE=$(du -sh "dist/Fortini Editor/" | cut -f1)
    echo "💾 Tamanho: $SIZE"
    echo ""
    
    echo "📦 Próximos passos:"
    echo ""
    echo "1️⃣  NO WINDOWS:"
    echo "   - Copie a pasta 'dist/Fortini Editor/' para qualquer lugar"
    echo "   - Execute: fortini_editor.exe"
    echo ""
    
    echo "2️⃣  DISTRIBUIR:"
    echo "   - Compacte em ZIP: dist/Fortini Editor/ → Fortini-Engine.zip"
    echo "   - Envie por email ou upload em itch.io"
    echo ""
    
    echo "3️⃣  CRIAR INSTALLER:"
    echo "   - Use NSIS ou Inno Setup no Windows"
    echo "   - Transforme em .msi ou setup.exe"
    echo ""
fi

# ============================================================
# CRIAR ZIP PARA DISTRIBUIÇÃO
# ============================================================

echo ""
read -p "Deseja criar arquivo ZIP para distribuição? (s/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo ""
    echo "📦 Criando ZIP..."
    
    if [ -d "dist/Fortini Editor" ]; then
        cd dist
        zip -r -q ../Fortini-Engine-Windows-$(date +%Y%m%d).zip "Fortini Editor"
        cd ..
        
        echo "✅ Criado: Fortini-Engine-Windows-$(date +%Y%m%d).zip"
        ls -lh "Fortini-Engine-Windows-"*.zip | tail -1
    fi
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Pronto! 🎮"
echo "═══════════════════════════════════════════════════════════"
