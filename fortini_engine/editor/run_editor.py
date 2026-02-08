"""Fortini Engine Editor Application."""

import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent))

from PyQt6.QtWidgets import QApplication
from fortini_engine.editor.main import FortiniEditor
from fortini_engine.utils.logger import Logger


def main():
    """Start the Fortini Engine editor."""
    # Initialize logger
    logger = Logger()
    logger.info("Starting Fortini Engine Editor v1.0.0")

    # Create application
    app = QApplication(sys.argv)

    # Create and show editor
    editor = FortiniEditor()
    editor.show()

    # Run application
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
