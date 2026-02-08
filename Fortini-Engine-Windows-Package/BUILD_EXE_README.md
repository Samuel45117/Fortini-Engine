# 🎮 Compilar Fortini Engine para Windows EXE

Guia completo para criar um executável .exe do Fortini Engine.

## 📋 Opções de Compilação

### Opção 1: Compilar NO WINDOWS (⭐ Recomendado)

**Requisitos:**
- Windows 10 ou superior
- Python 3.10+ instalado
- Git (opcional)

**Passos:**

```bash
# 1. Clone o repositório
git clone https://github.com/Samuel45117/Fortini-Engine.git
cd Fortini-Engine

# 2. Execute o script
build_exe_windows.bat

# 3. Espere (3-5 minutos)

# 4. Seu EXE estará em: dist\Fortini Editor\fortini_editor.exe
```

**Vantagens:**
- ✅ Mais rápido
- ✅ Sem dependências estranhas
- ✅ Resultado otimizado para Windows
- ✅ Pode incluir icone/versão/certificado

---

### Opção 2: Compilar NO LINUX para Windows

**Requisitos:**
- Linux (Ubuntu, Debian, Fedora, etc)
- Python 3.10+
- pip, zip

**Passos:**

```bash
# 1. Clone o repositório
git clone https://github.com/Samuel45117/Fortini-Engine.git
cd Fortini-Engine

# 2. Execute um dos scripts:

# Opção A: Script interativo com 3 métodos
bash build_exe_from_linux.sh

# Opção B: Script direto
bash build_exe_windows.sh
```

**Métodos Disponíveis:**

| Método | Ferramentas | Resultado | Velocidade |
|--------|-----------|-----------|-----------|
| **PyInstaller** | pip install | Pasta com EXE | ⭐⭐⭐ Rápido |
| **Nuitka** | pip install | EXE único | ⭐⭐ Médio |
| **Wine** | wine + Python Windows | EXE nativo | ⭐ Lento |

---

### Opção 3: Instalar Wine + Python (Avançado)

Se quer compilar EXE Windows DENTRO do Linux:

```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install wine wine32 wine64 wineboot

# Fedora
sudo dnf install wine

# Após instalar, rode:
bash build_exe_windows.sh
```

---

## 📦 Métodos de Compilação Explicados

### PyInstaller (Recomendado)

```bash
pyinstaller build_windows_exe.spec
```

**O que faz:**
- Analisa o código Python
- Copia todas as dependências
- Empacota em uma pasta
- Cria exe que roda a aplicação

**Resultado:**
```
dist/Fortini Editor/
├── fortini_editor.exe    (executável)
├── PyQt6/               (dependências)
├── OpenGL/
├── numpy/
└── ... (outras libs)
```

**Tamanho:** 200-400 MB (inclui tudo)

---

### Nuitka (Alternativo)

```bash
python -m nuitka --onefile fortini_engine/editor/run_editor.py
```

**O que faz:**
- Transpila Python para C
- Compila com gcc/MSVC
- Cria um EXE único (sem pasta)

**Resultado:**
```
dist/fortini_editor.exe  (tudo em 1 arquivo)
```

**Tamanho:** 250-500 MB (comprimido)

**Limitações:**
- Primeira compilação mais lenta
- EXE mais pesado

---

### Wine (Experimental)

```bash
wine python.exe build_windows_exe.spec
```

**O que faz:**
- Emula Windows no Linux
- Roda Python Windows nativo
- Compila como se estivesse no Windows

**Resultado:**
- EXE 100% compatível Windows

**Limitações:**
- Muito lento (30+ minutos)
- Requer Wine instalado
- Instável às vezes

---

## 🚀 Distribuição

Após compilar, você tem 3 opções:

### 1. Entregar a Pasta

```bash
# Copie simplesmente:
dist/Fortini Editor/

# Usuários baixam e executam:
./Fortini Editor/fortini_editor.exe
```

### 2. Comprimir em ZIP

```bash
cd dist
zip -r ../Fortini-Engine.zip "Fortini Editor"
```

Depois share o ZIP.

### 3. Criar Installer (NSIS/Inno Setup)

**No Windows:**

```bash
# Instale Inno Setup
# https://jrsoftware.org/isdl.php

# Crie arquivo: setup.iss
# Use: dist/Fortini Editor/ como fonte
# Compile

# Resultado: Fortini-Engine-Setup.exe (installer profissional)
```

---

## 🔧 Solução de Problemas

### ❌ "Python não encontrado"
```bash
# Windows: Instale Python
# https://www.python.org/

# Linux:
sudo apt-get install python3 python3-pip
```

### ❌ "PyOpenGL não encontrado"
```bash
pip install --upgrade PyOpenGL PyOpenGL-accelerate
```

### ❌ "Tamanhp muito grande"

**Reduza:**
```python
# Em build_windows_exe.spec, remova:
# excludedimports = ['matplotlib', 'scipy', 'pandas', ...]
```

### ❌ "EXE não executa"

1. Teste no código primeiro:
```bash
python -m fortini_engine.editor.run_editor
```

2. Verifique se todas as dependências foram instaladas:
```bash
pip install -r requirements.txt
```

3. Check console do EXE:
```bash
# No Windows, abra CMD e execute:
"dist\Fortini Editor\fortini_editor.exe"
# Verá mensagens de erro
```

---

## 📊 Comparação de Métodos

| Aspecto | PyInstaller | Nuitka | Wine |
|--------|-----------|--------|------|
| **Instalação** | 2 min | 5 min | 20+ min |
| **Primeira compilação** | 5 min | 15 min | 30+ min |
| **Recompilações** | 5 min | 1 min | 30+ min |
| **Tamanho final** | 300 MB | 300 MB | 300 MB |
| **Performance** | Normal | 2x mais rápido | Normal |
| **Compatibilidade** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **Dificuldade** | Fácil | Médio | Difícil |

---

## 💡 Dicas Finais

**Para Desenvolvimento:**
```bash
# Sempre teste primeiro
python -m fortini_engine.editor.run_editor

# Depois compile
pyinstaller build_windows_exe.spec
```

**Para Distribuição:**
```bash
# 1. Crie o EXE
pyinstaller build_windows_exe.spec

# 2. Teste no EXE compilado
./dist/Fortini\ Editor/fortini_editor.exe

# 3. Comprima
zip -r Fortini-Engine.zip dist/Fortini\ Editor/

# 4. Share!
```

**Para Equipe:**
```bash
# Versione o spec:
git add build_windows_exe.spec

# Crie release:
git tag -a v1.0.0-exe -m "First EXE build"
git push origin v1.0.0-exe

# Anexe o ZIP ao release
```

---

## Mais Ajuda

- 📖 [PyInstaller Docs](https://pyinstaller.org/)
- 🔧 [Nuitka Docs](https://nuitka.net/)
- 🍷 [Wine Docs](https://www.winehq.org/)

---

**Sucesso compilando!** 🎮🚀
