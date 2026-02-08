#!/bin/bash
# ============================================================
# Script para criar EXE do Fortini Engine usando Wine
# Linux → Windows EXE (com Wine + Python para Windows)
# ============================================================

set -e  # Exit on error

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║  🎮 Compilando Fortini Engine para Windows EXE        ║"
echo "║     (Usando Wine para gerar EXE no Linux)             ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

# ============================================================
# PARTE 1: Verificar dependências
# ============================================================

echo "📋 Verificando dependências..."
echo ""

# Verificar Python local
if ! command -v python3 &> /dev/null; then
    echo "❌ Python não encontrado"
    exit 1
fi
echo "✅ Python: $(python3 --version)"

# Verificar Wine (opcional mas recomendado)
if ! command -v wine &> /dev/null; then
    echo "⚠️  Wine não instalado"
    echo "   Para compilar EXE no Linux, você precisa de Wine:"
    echo ""
    echo "   Ubuntu/Debian:"
    echo "     sudo apt-get install wine wine32 wine64 wineboot"
    echo ""
    echo "   Ou instale Python para Windows e use esse script no Windows"
    echo ""
    read -p "Continuar mesmo assim? (s/n): " -n 1 -r
    echo
    if [[ ! $REPLY =~ ^[Ss]$ ]]; then
        exit 1
    fi
fi

# ============================================================
# PARTE 2: Instalar dependências Python
# ============================================================

echo ""
echo "📦 Instalando dependências Python..."

pip install -q -r requirements.txt
pip install -q pyinstaller

# PyInstaller para Windows
pip install -q --upgrade pyinstaller

echo "✅ Dependências instaladas"

# ============================================================
# PARTE 3: Preparar código para Windows
# ============================================================

echo ""
echo "🔧 Preparando repositório..."

# Criar diretório de build
mkdir -p build_windows
mkdir -p dist

echo "✅ Diretórios preparados"

# ============================================================
# PARTE 4: Compilar com PyInstaller
# ============================================================

echo ""
echo "🔨 Compilando exe com PyInstaller..."
echo "   (isso pode levar 3-5 minutos...)"
echo ""

if [ -f "build_windows_exe.spec" ]; then
    pyinstaller build_windows_exe.spec \
        --distpath=dist \
        --buildpath=build_windows \
        --specpath=. \
        -y
else
    echo "❌ Arquivo build_windows_exe.spec não encontrado!"
    exit 1
fi

# ============================================================
# PARTE 5: Verificar resultado
# ============================================================

echo ""
if [ -d "dist/Fortini Editor" ]; then
    echo "╔════════════════════════════════════════════════════════╗"
    echo "║                                                        ║"
    echo "║          ✅ SUCESSO! EXE COMPILADO                    ║"
    echo "║                                                        ║"
    echo "╚════════════════════════════════════════════════════════╝"
    echo ""
    echo "📁 Arquivo: dist/Fortini Editor/fortini_editor.exe"
    echo ""
    echo "Próximos passos:"
    echo "  1. Copie a pasta 'dist/Fortini Editor/' para Windows"
    echo "  2. Execute fortini_editor.exe no Windows"
    echo "  3. Distribuir: compacte a pasta em ZIP"
    echo ""
    echo "Tamanho aproximado:"
    du -sh "dist/Fortini Editor/"
    echo ""
    
    # Se tiver Wine, pode tentar executar
    if command -v wine &> /dev/null; then
        echo "💡 Wine detectado - você pode tentar:"
        echo "   wine dist/Fortini\ Editor/fortini_editor.exe"
        echo ""
    fi
else
    echo "❌ Erro ao compilar EXE"
    echo ""
    echo "Verifique os erros acima"
    exit 1
fi

# ============================================================
# PARTE 6: Criar distributável
# ============================================================

echo ""
read -p "Deseja criar arquivo ZIP para distribuição? (s/n): " -n 1 -r
echo

if [[ $REPLY =~ ^[Ss]$ ]]; then
    echo ""
    echo "📦 Criando arquivo ZIP..."
    
    cd dist
    zip -r -q ../Fortini-Engine-Windows.zip "Fortini Editor"
    cd ..
    
    echo "✅ Criado: Fortini-Engine-Windows.zip"
    ls -lh Fortini-Engine-Windows.zip
    echo ""
    echo "Você pode agora:"
    echo "  1. Enviar o ZIP a alguém pelo email/cloud"
    echo "  2. Subir no GitHub Releases"
    echo "  3. Distribuir no itch.io"
fi

echo ""
echo "═══════════════════════════════════════════════════════════"
echo "Pronto! 🎉"
echo "═══════════════════════════════════════════════════════════"
