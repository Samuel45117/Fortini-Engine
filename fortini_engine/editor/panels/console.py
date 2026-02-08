"""Console Panel."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTextEdit, QLabel


class ConsolePanel(QWidget):
    """Console for engine logs and output."""

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup UI."""
        layout = QVBoxLayout(self)

        label = QLabel("Console")
        layout.addWidget(label)

        # Log output
        self.log_output = QTextEdit()
        self.log_output.setReadOnly(True)
        layout.addWidget(self.log_output)

    def log(self, message: str) -> None:
        """Add a log message."""
        self.log_output.append(message)
