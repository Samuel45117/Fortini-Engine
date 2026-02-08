"""Transform component for 3D objects."""

import numpy as np
from fortini_engine.utils.math_utils import Vector3, Matrix4, Quaternion


class Transform:
    """Transform component for position, rotation, and scale."""

    def __init__(self, parent=None):
        self.position = Vector3(0, 0, 0)
        self.rotation = Quaternion(0, 0, 0, 1)  # w, x, y, z order
        self.scale = Vector3(1, 1, 1)

        self.parent = parent
        self.children = []

        self._matrix_cache = None
        self._matrix_dirty = True
        self._inverse_matrix_cache = None

    def translate(self, x: float, y: float, z: float) -> None:
        """Translate the object."""
        self.position = Vector3(
            self.position.x + x,
            self.position.y + y,
            self.position.z + z,
        )
        self._mark_dirty()

    def rotate(self, pitch: float, yaw: float, roll: float) -> None:
        """Rotate the object (in radians)."""
        self.rotation = Quaternion.from_euler_angles(pitch, yaw, roll)
        self._mark_dirty()

    def set_position(self, x: float, y: float, z: float) -> None:
        """Set absolute position."""
        self.position = Vector3(x, y, z)
        self._mark_dirty()

    def set_rotation(self, pitch: float, yaw: float, roll: float) -> None:
        """Set absolute rotation (in radians)."""
        self.rotation = Quaternion.from_euler_angles(pitch, yaw, roll)
        self._mark_dirty()

    def set_scale(self, x: float, y: float, z: float) -> None:
        """Set absolute scale."""
        self.scale = Vector3(x, y, z)
        self._mark_dirty()

    def get_matrix(self) -> Matrix4:
        """Get the transformation matrix."""
        if self._matrix_dirty:
            self._recalculate_matrix()
        return self._matrix_cache

    def _recalculate_matrix(self) -> None:
        """Recalculate the transformation matrix."""
        # T * R * S (translation * rotation * scale)
        translation_mat = Matrix4.translation(
            self.position.x, self.position.y, self.position.z
        )

        # Simple rotation using quaternion (simplified for now)
        # In production, use proper quaternion to matrix conversion
        rotation_mat = Matrix4.identity()

        scale_mat = Matrix4.scale(self.scale.x, self.scale.y, self.scale.z)

        self._matrix_cache = translation_mat * rotation_mat * scale_mat

        if self.parent:
            parent_matrix = self.parent.transform.get_matrix()
            self._matrix_cache = parent_matrix * self._matrix_cache

        self._matrix_dirty = False

    def _mark_dirty(self) -> None:
        """Mark matrix as needing recalculation."""
        self._matrix_dirty = True
        # Propagate to children
        for child in self.children:
            child._mark_dirty()

    def add_child(self, child_transform: "Transform") -> None:
        """Add a child transform."""
        if child_transform not in self.children:
            self.children.append(child_transform)
            child_transform.parent = self
            child_transform._mark_dirty()

    def remove_child(self, child_transform: "Transform") -> None:
        """Remove a child transform."""
        if child_transform in self.children:
            self.children.remove(child_transform)
            child_transform.parent = None
            child_transform._mark_dirty()

    def __repr__(self) -> str:
        return f"Transform(pos={self.position}, rot={self.rotation}, scale={self.scale})"
