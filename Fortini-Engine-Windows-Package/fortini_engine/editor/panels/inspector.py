"""Inspector Panel - Object Properties."""

from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QFormLayout, QLineEdit, QSpinBox,
    QDoubleSpinBox, QLabel, QGroupBox, QScrollArea
)


class InspectorPanel(QWidget):
    """Inspector for editing object properties."""

    def __init__(self):
        super().__init__()
        self.current_object = None
        self._setup_ui()

    def _setup_ui(self) -> None:
        """Setup UI."""
        main_layout = QVBoxLayout(self)

        # Scroll area for properties
        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll_content = QWidget()
        self.content_layout = QVBoxLayout(scroll_content)

        scroll.setWidget(scroll_content)
        main_layout.addWidget(scroll)

    def set_object(self, obj) -> None:
        """Set the object to inspect."""
        self.current_object = obj
        self._refresh_properties()

    def _refresh_properties(self) -> None:
        """Refresh property fields."""
        # Clear previous layout
        while self.content_layout.count():
            child = self.content_layout.takeAt(0)
            if child.widget():
                child.widget().deleteLater()

        if not self.current_object:
            return

        # Object name
        name_group = QGroupBox("General")
        name_layout = QFormLayout()

        name_input = QLineEdit(self.current_object.name)
        name_input.editingFinished.connect(
            lambda: setattr(self.current_object, "name", name_input.text())
        )
        name_layout.addRow("Name:", name_input)

        active_check = QLineEdit(str(self.current_object.active))
        name_layout.addRow("Active:", active_check)
        name_group.setLayout(name_layout)
        self.content_layout.addWidget(name_group)

        # Transform group
        transform_group = QGroupBox("Transform")
        transform_layout = QFormLayout()

        # Position
        pos = self.current_object.transform.position
        pos_x = QDoubleSpinBox()
        pos_x.setValue(pos.x)
        pos_x.setSingleStep(0.1)
        pos_x.valueChanged.connect(
            lambda v: self._update_position(0, v)
        )
        transform_layout.addRow("Position X:", pos_x)

        pos_y = QDoubleSpinBox()
        pos_y.setValue(pos.y)
        pos_y.setSingleStep(0.1)
        pos_y.valueChanged.connect(
            lambda v: self._update_position(1, v)
        )
        transform_layout.addRow("Position Y:", pos_y)

        pos_z = QDoubleSpinBox()
        pos_z.setValue(pos.z)
        pos_z.setSingleStep(0.1)
        pos_z.valueChanged.connect(
            lambda v: self._update_position(2, v)
        )
        transform_layout.addRow("Position Z:", pos_z)

        # Scale
        scale = self.current_object.transform.scale
        scale_x = QDoubleSpinBox()
        scale_x.setValue(scale.x)
        scale_x.setSingleStep(0.1)
        scale_x.setMinimum(0.01)
        scale_x.valueChanged.connect(
            lambda v: self._update_scale(0, v)
        )
        transform_layout.addRow("Scale X:", scale_x)

        scale_y = QDoubleSpinBox()
        scale_y.setValue(scale.y)
        scale_y.setSingleStep(0.1)
        scale_y.setMinimum(0.01)
        scale_y.valueChanged.connect(
            lambda v: self._update_scale(1, v)
        )
        transform_layout.addRow("Scale Y:", scale_y)

        scale_z = QDoubleSpinBox()
        scale_z.setValue(scale.z)
        scale_z.setSingleStep(0.1)
        scale_z.setMinimum(0.01)
        scale_z.valueChanged.connect(
            lambda v: self._update_scale(2, v)
        )
        transform_layout.addRow("Scale Z:", scale_z)

        transform_group.setLayout(transform_layout)
        self.content_layout.addWidget(transform_group)

        self.content_layout.addStretch()

    def _update_position(self, axis: int, value: float) -> None:
        """Update object position."""
        pos = self.current_object.transform.position
        if axis == 0:
            pos.x = value
        elif axis == 1:
            pos.y = value
        elif axis == 2:
            pos.z = value

    def _update_scale(self, axis: int, value: float) -> None:
        """Update object scale."""
        scale = self.current_object.transform.scale
        if axis == 0:
            scale.x = value
        elif axis == 1:
            scale.y = value
        elif axis == 2:
            scale.z = value
