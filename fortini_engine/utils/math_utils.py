"""Math utilities for 3D graphics."""

import numpy as np
from typing import Union, Tuple


class Vector3:
    """3D Vector representation."""

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __add__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        return NotImplemented

    def __sub__(self, other):
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        return NotImplemented

    def __mul__(self, scalar: float):
        if isinstance(scalar, (int, float)):
            return Vector3(self.x * scalar, self.y * scalar, self.z * scalar)
        return NotImplemented

    def __rmul__(self, scalar: float):
        return self.__mul__(scalar)

    def magnitude(self) -> float:
        """Calculate vector magnitude."""
        return np.sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        """Normalize the vector (returns new Vector3)."""
        mag = self.magnitude()
        if mag == 0:
            return Vector3(0, 0, 0)
        return Vector3(self.x / mag, self.y / mag, self.z / mag)

    def dot(self, other):
        """Calculate dot product."""
        if isinstance(other, Vector3):
            return self.x * other.x + self.y * other.y + self.z * other.z
        return NotImplemented

    def cross(self, other):
        """Calculate cross product."""
        if isinstance(other, Vector3):
            return Vector3(
                self.y * other.z - self.z * other.y,
                self.z * other.x - self.x * other.z,
                self.x * other.y - self.y * other.x,
            )
        return NotImplemented

    def to_numpy(self) -> np.ndarray:
        """Convert to numpy array."""
        return np.array([self.x, self.y, self.z], dtype=np.float32)

    def __repr__(self) -> str:
        return f"Vector3({self.x:.2f}, {self.y:.2f}, {self.z:.2f})"

    def to_tuple(self) -> Tuple[float, float, float]:
        """Convert to tuple."""
        return (self.x, self.y, self.z)


class Quaternion:
    """Quaternion for 3D rotations."""

    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0, w: float = 1.0):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def to_numpy(self) -> np.ndarray:
        """Convert to numpy array."""
        return np.array([self.x, self.y, self.z, self.w], dtype=np.float32)

    @staticmethod
    def from_euler_angles(pitch: float, yaw: float, roll: float):
        """Create quaternion from Euler angles (in radians)."""
        cy = np.cos(yaw * 0.5)
        sy = np.sin(yaw * 0.5)
        cp = np.cos(pitch * 0.5)
        sp = np.sin(pitch * 0.5)
        cr = np.cos(roll * 0.5)
        sr = np.sin(roll * 0.5)

        w = cr * cp * cy + sr * sp * sy
        x = sr * cp * cy - cr * sp * sy
        y = cr * sp * cy + sr * cp * sy
        z = cr * cp * sy - sr * sp * cy

        return Quaternion(x, y, z, w)

    def __repr__(self) -> str:
        return f"Quaternion({self.x:.2f}, {self.y:.2f}, {self.z:.2f}, {self.w:.2f})"


class Matrix4:
    """4x4 Matrix for 3D transformations."""

    def __init__(self, data: np.ndarray = None):
        if data is None:
            self.data = np.identity(4, dtype=np.float32)
        else:
            self.data = data.astype(np.float32)

    @staticmethod
    def identity() -> "Matrix4":
        """Create identity matrix."""
        return Matrix4()

    @staticmethod
    def translation(x: float, y: float, z: float) -> "Matrix4":
        """Create translation matrix."""
        mat = np.identity(4, dtype=np.float32)
        mat[0, 3] = x
        mat[1, 3] = y
        mat[2, 3] = z
        return Matrix4(mat)

    @staticmethod
    def scale(x: float, y: float, z: float) -> "Matrix4":
        """Create scale matrix."""
        mat = np.identity(4, dtype=np.float32)
        mat[0, 0] = x
        mat[1, 1] = y
        mat[2, 2] = z
        return Matrix4(mat)

    @staticmethod
    def rotation_x(angle: float) -> "Matrix4":
        """Create rotation matrix around X axis."""
        c, s = np.cos(angle), np.sin(angle)
        mat = np.identity(4, dtype=np.float32)
        mat[1, 1] = c
        mat[1, 2] = -s
        mat[2, 1] = s
        mat[2, 2] = c
        return Matrix4(mat)

    @staticmethod
    def rotation_y(angle: float) -> "Matrix4":
        """Create rotation matrix around Y axis."""
        c, s = np.cos(angle), np.sin(angle)
        mat = np.identity(4, dtype=np.float32)
        mat[0, 0] = c
        mat[0, 2] = s
        mat[2, 0] = -s
        mat[2, 2] = c
        return Matrix4(mat)

    @staticmethod
    def rotation_z(angle: float) -> "Matrix4":
        """Create rotation matrix around Z axis."""
        c, s = np.cos(angle), np.sin(angle)
        mat = np.identity(4, dtype=np.float32)
        mat[0, 0] = c
        mat[0, 1] = -s
        mat[1, 0] = s
        mat[1, 1] = c
        return Matrix4(mat)

    @staticmethod
    def perspective(fov: float, aspect: float, near: float, far: float) -> "Matrix4":
        """Create perspective projection matrix."""
        f = 1.0 / np.tan(fov / 2.0)
        mat = np.zeros((4, 4), dtype=np.float32)
        mat[0, 0] = f / aspect
        mat[1, 1] = f
        mat[2, 2] = (far + near) / (near - far)
        mat[2, 3] = (2 * far * near) / (near - far)
        mat[3, 2] = -1.0
        return Matrix4(mat)

    @staticmethod
    def orthographic(left: float, right: float, bottom: float, top: float, near: float, far: float) -> "Matrix4":
        """Create orthographic projection matrix."""
        mat = np.identity(4, dtype=np.float32)
        mat[0, 0] = 2.0 / (right - left)
        mat[1, 1] = 2.0 / (top - bottom)
        mat[2, 2] = -2.0 / (far - near)
        mat[0, 3] = -(right + left) / (right - left)
        mat[1, 3] = -(top + bottom) / (top - bottom)
        mat[2, 3] = -(far + near) / (far - near)
        return Matrix4(mat)

    @staticmethod
    def look_at(eye: Vector3, center: Vector3, up: Vector3) -> "Matrix4":
        """Create look at matrix."""
        f = (center - eye).normalize()
        s = f.cross(up).normalize()
        u = s.cross(f)

        mat = np.identity(4, dtype=np.float32)
        mat[0, 0] = s.x
        mat[1, 0] = s.y
        mat[2, 0] = s.z
        mat[0, 1] = u.x
        mat[1, 1] = u.y
        mat[2, 1] = u.z
        mat[0, 2] = -f.x
        mat[1, 2] = -f.y
        mat[2, 2] = -f.z
        mat[0, 3] = -s.dot(eye)
        mat[1, 3] = -u.dot(eye)
        mat[2, 3] = f.dot(eye)

        return Matrix4(mat)

    def __mul__(self, other):
        if isinstance(other, Matrix4):
            return Matrix4(np.dot(self.data, other.data))
        return NotImplemented

    def to_numpy(self) -> np.ndarray:
        """Get numpy array representation."""
        return self.data

    def __repr__(self) -> str:
        return f"Matrix4:\n{self.data}"
