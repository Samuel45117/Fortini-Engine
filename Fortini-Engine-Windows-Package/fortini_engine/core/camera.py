"""Camera system for 3D rendering."""

import numpy as np
from fortini_engine.core.game_object import GameObject
from fortini_engine.utils.math_utils import Vector3, Matrix4


class Camera(GameObject):
    """Base camera class."""

    def __init__(self, name: str = "Camera"):
        super().__init__(name)
        self.near_plane = 0.1
        self.far_plane = 1000.0
        self.projection_matrix = None
        self.view_matrix = None

    def get_view_matrix(self) -> Matrix4:
        """Get view matrix."""
        if self.view_matrix is None:
            eye = self.transform.position
            center = eye + Vector3(0, 0, -1)
            up = Vector3(0, 1, 0)
            self.view_matrix = Matrix4.look_at(eye, center, up)
        return self.view_matrix

    def get_projection_matrix(self) -> Matrix4:
        """Get projection matrix."""
        raise NotImplementedError("Subclasses must implement get_projection_matrix")

    def look_at(self, target: Vector3) -> None:
        """Point camera at a target."""
        eye = self.transform.position
        up = Vector3(0, 1, 0)
        self.view_matrix = Matrix4.look_at(eye, target, up)

    def update(self, delta_time: float) -> None:
        """Update camera."""
        # Reset view matrix to recalculate
        self.view_matrix = None
        super().update(delta_time)


class PerspectiveCamera(Camera):
    """Perspective camera."""

    def __init__(self, name: str = "Camera", fov: float = 45.0, aspect: float = 16 / 9):
        super().__init__(name)
        self.fov = fov  # in degrees
        self.aspect = aspect

    def get_projection_matrix(self) -> Matrix4:
        """Get perspective projection matrix."""
        fov_rad = np.radians(self.fov)
        return Matrix4.perspective(fov_rad, self.aspect, self.near_plane, self.far_plane)

    def set_viewport(self, width: int, height: int) -> None:
        """Update aspect ratio based on viewport size."""
        self.aspect = width / height

    def __repr__(self) -> str:
        return f"PerspectiveCamera(name='{self.name}', fov={self.fov}, aspect={self.aspect:.2f})"


class OrthographicCamera(Camera):
    """Orthographic camera for 2D."""

    def __init__(
        self, name: str = "Camera", left: float = -10, right: float = 10, bottom: float = -10, top: float = 10
    ):
        super().__init__(name)
        self.left = left
        self.right = right
        self.bottom = bottom
        self.top = top

    def get_projection_matrix(self) -> Matrix4:
        """Get orthographic projection matrix."""
        return Matrix4.orthographic(
            self.left, self.right, self.bottom, self.top, self.near_plane, self.far_plane
        )

    def set_size(self, width: float, height: float) -> None:
        """Set orthographic size."""
        self.left = -width / 2
        self.right = width / 2
        self.bottom = -height / 2
        self.top = height / 2

    def __repr__(self) -> str:
        return f"OrthographicCamera(name='{self.name}', size=({self.right - self.left}, {self.top - self.bottom}))"
