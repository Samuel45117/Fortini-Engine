#!/usr/bin/env python3
"""
Fortini Engine - Launcher Script

This script launches the Fortini Engine Editor.
Run this to start game development!
"""

import sys
import os
from pathlib import Path

# Add the project root to Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

def main():
    """Main entry point."""
    print("=" * 60)
    print(" " * 10 + "🎮 Fortini Engine Editor 🎮")
    print(" " * 15 + "v1.0.0")
    print("=" * 60)
    print()

    try:
        from fortini_engine.utils.logger import Logger
        from PyQt6.QtWidgets import QApplication
        from fortini_engine.editor.main import FortiniEditor

        logger = Logger()
        logger.info("Starting Fortini Engine Editor")
        print("✓ Fortini Engine initialized")
        print("✓ Logger system ready")
        print("✓ Creating editor interface...")
        print()

        # Create Qt application
        app = QApplication(sys.argv)

        # Create and show editor
        editor = FortiniEditor()
        editor.show()

        print("=" * 60)
        print(" Editor launched successfully!")
        print()
        print(" Quick Tips:")
        print("  • Right-click Hierarchy to create objects")
        print("  • Select objects to edit properties in Inspector")
        print("  • Write Python scripts in Scripts/ folder")
        print("  • Click Play ▶ to test your game")
        print("  • Check QUICKSTART.md for tutorials")
        print()
        print(" Documentation:")
        print("  • README.md - Full feature documentation")
        print("  • QUICKSTART.md - 10-minute tutorial")
        print("  • ARCHITECTURE.md - Technical details")
        print()
        print("=" * 60)

        # Run application
        sys.exit(app.exec())

    except ImportError as e:
        print(f"❌ Import Error: {e}")
        print()
        print("Make sure you have installed dependencies:")
        print("  pip install -r requirements.txt")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        print()
        print("Check the logs at: ~/Fortini Documents/Logs/")
        sys.exit(1)


if __name__ == "__main__":
    main()
