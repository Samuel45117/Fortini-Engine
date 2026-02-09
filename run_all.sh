#!/usr/bin/env bash
set -e

echo "=== Fortini Engine - Run All (Linux/macOS) ==="
ROOT="$(cd "$(dirname "$0")" && pwd)"
cd "$ROOT"

# Instalar dependências (se desejar)
if command -v python3 >/dev/null 2>&1; then
  PY=python3
elif command -v python >/dev/null 2>&1; then
  PY=python
else
  echo "Python não encontrado. Instale Python 3.10+ e rode novamente." >&2
  exit 1
fi

echo "Usando: $PY"

read -p "Instalar dependências (pip install -r requirements.txt)? [S/n] " -r
if [[ $REPLY =~ ^[Nn]$ ]]; then
  echo "Pulando instalação de dependências"
else
  echo "Instalando dependências..."
  $PY -m pip install -r requirements.txt || true
fi

# Rodar playall em modo editor
echo "Iniciando Fortini Editor via playall.py..."
$PY playall.py

echo "Fim."