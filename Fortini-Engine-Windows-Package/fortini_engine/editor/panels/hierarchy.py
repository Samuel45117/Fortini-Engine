"""Hierarchy Panel - Scene Tree View."""

from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTreeWidget, QTreeWidgetItem
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QIcon


class HierarchyPanel(QWidget):
    """Scene hierarchy tree view."""

    object_selected = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.scene = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup UI."""
        layout = QVBoxLayout(self)

        self.tree = QTreeWidget()
        self.tree.setHeaderLabel("Scene Hierarchy")
        self.tree.itemClicked.connect(self._on_item_clicked)

        layout.addWidget(self.tree)

    def set_scene(self, scene) -> None:
        """Set the scene to display."""
        self.scene = scene
        self._refresh_tree()

    def _refresh_tree(self) -> None:
        """Refresh the tree view."""
        self.tree.clear()

        if not self.scene:
            return

        for obj in self.scene.root_objects:
            self._add_object_to_tree(obj, self.tree)

    def _add_object_to_tree(self, obj, parent) -> None:
        """Add an object and its children to the tree."""
        if isinstance(parent, QTreeWidget):
            item = QTreeWidgetItem(parent)
        else:
            item = QTreeWidgetItem(parent)

        item.setText(0, obj.name)
        item.setData(0, Qt.ItemDataRole.UserRole, obj)

        for child in obj.children:
            self._add_object_to_tree(child, item)

    def _on_item_clicked(self, item: QTreeWidgetItem, column: int) -> None:
        """Handle item selection."""
        obj = item.data(0, Qt.ItemDataRole.UserRole)
        if obj:
            self.object_selected.emit(obj)
