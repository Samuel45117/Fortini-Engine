# 🎮 Compilar Fortini Engine para EXE no Windows

## Pré-requisitos

1. **Windows 10 ou Superior**
2. **Python 3.10+** - Baixe em: https://www.python.org/
   - ⚠️ **IMPORTANTE**: Marque "Add Python to PATH" durante instalação
3. **Git** (opcional) - https://git-scm.com/

## Verificar Instalação

Abra PowerShell ou CMD e teste:

```powershell
python --version
pip --version
```

Ambos devem mostrar versões.

## Compilar

### Opção 1: Usar Script Automático (Recomendado)

```powershell
# 1. Abra PowerShell como Administrador
# 2. Navegue até a pasta descompactada
cd C:\Users\SeuNome\Fortini-Engine-Windows-Package

# 3. Execute o script
.\build_exe_windows.bat

# 4. Espere 3-5 minutos

# 5. Seu EXE estará em: dist\Fortini Editor\fortini_editor.exe
```

### Opção 2: Compilação Manual

```powershell
# 1. Instalar dependências
pip install -r requirements.txt
pip install pyinstaller

# 2. Compilar
pyinstaller build_windows_simple.spec

# 3. Seu EXE estará em: dist\Fortini Editor\fortini_editor.exe
```

## ✅ Pronto!

Você agora tem:
- **dist/Fortini Editor/** - Pasta com o editor
- **dist/Fortini Editor/fortini_editor.exe** - Executável

## 📦 Distribuir

Para enviar para outras pessoas:

```powershell
# Compactar em ZIP
Add-Type -AssemblyName System.IO.Compression.FileSystem
[System.IO.Compression.ZipFile]::CreateFromDirectory("dist\Fortini Editor", "Fortini-Engine.zip")

# Ou use WinRAR/7-Zip para compactar a pasta
```

## ❓ Dúvidas?

- 📖 Ver: BUILD_EXE_README.md
- 🔗 Docs: README.md
- 🏗️ Arquitetura: ARCHITECTURE.md

**Sucesso!** 🎮
