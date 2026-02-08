"""Asset Browser Panel."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QLabel


class AssetBrowserPanel(QWidget):
    """Asset browser for managing game assets."""

    def __init__(self):
        super().__init__()
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup UI."""
        layout = QVBoxLayout(self)

        label = QLabel("Assets")
        layout.addWidget(label)

        # Asset list
        self.asset_list = QListWidget()
        layout.addWidget(self.asset_list)

        # Placeholder items
        items = ["Cube.mesh", "Sphere.mesh", "Material_Default.mat"]
        for item in items:
            self.asset_list.addItem(QListWidgetItem(item))
