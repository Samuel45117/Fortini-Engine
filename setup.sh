#!/bin/bash

# Fortini Engine - Quick Setup Script for Linux/macOS

echo "========================================"
echo "🎮 Fortini Engine Setup"
echo "========================================"
echo ""

# Check Python
echo "✓ Checking Python 3.10+..."
python3 --version

# Install dependencies
echo ""
echo "✓ Installing dependencies..."
pip install -r requirements.txt

# Install in dev mode
echo ""
echo "✓ Installing Fortini Engine..."
pip install -e .

# Create documents folder
echo ""
echo "✓ Setting up project directories..."
mkdir -p ~/Fortini\ Documents/Projects
mkdir -p ~/Fortini\ Documents/Logs

echo ""
echo "========================================"
echo "✅ Setup complete!"
echo ""
echo "To launch the editor, run:"
echo "  python fortini_editor.py"
echo ""
echo "Or:"
echo "  python -m fortini_engine.editor.run_editor"
echo ""
echo "Happy gaming! 🎮"
echo "========================================"
