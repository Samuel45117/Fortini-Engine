#!/usr/bin/env python3
"""
Launcher para Fortini Editor sem dependência de shared library
Funciona com PyInstaller em ambientes com Python compilado sem --enable-shared
"""

import sys
import os
import subprocess

# Encontrar Python
python_exe = sys.executable

# Diretório da aplicação
app_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, app_dir)

# Iniciar editor
if __name__ == '__main__':
    from fortini_engine.editor.main import FortiniEditor
    from PyQt6.QtWidgets import QApplication
    
    app = QApplication(sys.argv)
    editor = FortiniEditor()
    editor.show()
    sys.exit(app.exec())
