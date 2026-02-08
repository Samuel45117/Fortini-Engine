#!/bin/bash
# ============================================================
# Script para preparar Fortini Engine para compilação no Windows
# Cria um pacote pronto para ser compilado com PyInstaller no Windows
# ============================================================

set -e

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║  📦 Preparando Fortini Engine para Windows             ║"
echo "║     (Este pacote será compilado no Windows)           ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""

PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR"

# Criar diretório de saída
OUTPUT_DIR="Fortini-Engine-Windows-Package"
mkdir -p "$OUTPUT_DIR"

echo "📁 Copiando arquivos do projeto..."

# Copiar estrutura principal
cp -r fortini_engine "$OUTPUT_DIR/"
cp -r examples "$OUTPUT_DIR/" 2>/dev/null || true
cp launcher.py "$OUTPUT_DIR/"
cp requirements.txt "$OUTPUT_DIR/"
cp build_windows_simple.spec "$OUTPUT_DIR/"
cp build_windows_exe.spec "$OUTPUT_DIR/"
cp build_exe_windows.bat "$OUTPUT_DIR/"
cp BUILD_EXE_README.md "$OUTPUT_DIR/"
cp README.md "$OUTPUT_DIR/"
cp ARCHITECTURE.md "$OUTPUT_DIR/" 2>/dev/null || true
cp QUICKSTART.md "$OUTPUT_DIR/" 2>/dev/null || true
cp .gitignore "$OUTPUT_DIR/" 2>/dev/null || true
cp LICENSE "$OUTPUT_DIR/" 2>/dev/null || true

# Criar arquivo de instruções
cat > "$OUTPUT_DIR/LEIA_PRIMEIRO.txt" << 'INSTRUCOES'
╔════════════════════════════════════════════════════════╗
║                                                        ║
║    🎮 FORTINI ENGINE - WINDOWS BUILD PACKAGE         ║
║                                                        ║
╚════════════════════════════════════════════════════════╝

🚀 COMEÇAR AGORA:

1. Requisitos:
   ✓ Windows 10 ou Superior
   ✓ Python 3.10+ (https://www.python.org/)
   ✓ Marque "Add Python to PATH" na instalação do Python

2. Compilar para EXE:
   • Abra PowerShell/CMD nesta pasta
   • Execute: build_exe_windows.bat
   • Espere 3-5 minutos
   • EXE estará em: dist\Fortini Editor\fortini_editor.exe

3. Documentação:
   • BUILD_EXE_README.md - Guia completo
   • README.md - Sobre o projeto
   • ARCHITECTURE.md - Arquitetura interna
   • QUICKSTART.md - Quick start

📁 Estrutura:
   • fortini_engine/ - Código da engine
   • launcher.py - Ponto de entrada
   • build_windows_simple.spec - Config PyInstaller
   • requirements.txt - Dependências

✅ SUCESSO! Seu EXE será criado em minutos.

INSTRUCOES

# Contar arquivos
FILE_COUNT=$(find "$OUTPUT_DIR" -type f | wc -l)
SIZE=$(du -sh "$OUTPUT_DIR" | cut -f1)

echo "✅ Arquivos copiados: $FILE_COUNT"
echo "📦 Tamanho: $SIZE"
echo ""

# Criar ZIP
echo "📦 Criando ZIP para download..."
ZIP_NAME="Fortini-Engine-Windows-$(date +%Y%m%d).zip"
zip -r -q "$ZIP_NAME" "$OUTPUT_DIR"

echo "✅ Criado: $ZIP_NAME"
ls -lh "$ZIP_NAME"

echo ""
echo "╔════════════════════════════════════════════════════════╗"
echo "║                                                        ║"
echo "║           ✅ PACOTE PRONTO PARA WINDOWS              ║"
echo "║                                                        ║"
echo "╚════════════════════════════════════════════════════════╝"
echo ""
echo "📦 Arquivo gerado: $ZIP_NAME"
echo ""
echo "No Windows:"
echo "  1. Descompacte o ZIP"
echo "  2. Abra PowerShell/CMD na pasta"
echo "  3. Execute: build_exe_windows.bat"
echo "  4. EXE: dist\\Fortini Editor\\fortini_editor.exe"
echo ""
echo "═══════════════════════════════════════════════════════════"
