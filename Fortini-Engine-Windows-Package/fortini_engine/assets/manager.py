"""Asset management system."""

import numpy as np
from typing import Dict, List, Optional


class Mesh:
    """3D Mesh data."""

    def __init__(self, name: str = "Mesh"):
        self.name = name
        self.vertices: np.ndarray = np.array([], dtype=np.float32)  # Nx3
        self.normals: np.ndarray = np.array([], dtype=np.float32)   # Nx3
        self.uv_coords: np.ndarray = np.array([], dtype=np.float32) # Nx2
        self.indices: np.ndarray = np.array([], dtype=np.uint32)    # Nx3
        self.vao = None  # Vertex Array Object (OpenGL)
        self.vbo = None  # Vertex Buffer Object (OpenGL)
        self.ebo = None  # Element Buffer Object (OpenGL)

    def add_cube(self, size: float = 1.0) -> None:
        """Add a cube mesh."""
        s = size / 2
        self.vertices = np.array([
            # Front
            [-s, -s, s],
            [s, -s, s],
            [s, s, s],
            [-s, s, s],
            # Back
            [-s, -s, -s],
            [s, -s, -s],
            [s, s, -s],
            [-s, s, -s],
        ], dtype=np.float32)

        self.indices = np.array([
            0, 1, 2, 2, 3, 0,  # Front
            4, 6, 5, 4, 7, 6,  # Back
            0, 3, 7, 0, 7, 4,  # Left
            1, 5, 6, 1, 6, 2,  # Right
            3, 2, 6, 3, 6, 7,  # Top
            0, 4, 5, 0, 5, 1,  # Bottom
        ], dtype=np.uint32)

        self.normals = np.array([
            # Front face
            [0, 0, 1], [0, 0, 1], [0, 0, 1], [0, 0, 1],
            # Back face
            [0, 0, -1], [0, 0, -1], [0, 0, -1], [0, 0, -1],
        ], dtype=np.float32)

    def add_sphere(self, radius: float = 1.0, sectors: int = 32, stacks: int = 16) -> None:
        """Add a sphere mesh."""
        vertices = []
        indices = []

        for i in range(stacks + 1):
            stack_angle = np.pi / 2 - i * np.pi / stacks
            xy = radius * np.cos(stack_angle)
            z = radius * np.sin(stack_angle)

            for j in range(sectors + 1):
                sector_angle = 2 * np.pi * j / sectors
                x = xy * np.cos(sector_angle)
                y = xy * np.sin(sector_angle)
                vertices.append([x, y, z])

        for i in range(stacks):
            k1 = i * (sectors + 1)
            k2 = k1 + sectors + 1

            for j in range(sectors):
                if i != 0:
                    indices.extend([k1, k2, k1 + 1])
                if i != stacks - 1:
                    indices.extend([k1 + 1, k2, k2 + 1])
                k1 += 1
                k2 += 1

        self.vertices = np.array(vertices, dtype=np.float32)
        self.indices = np.array(indices, dtype=np.uint32)

    def add_pyramid(self, size: float = 1.0) -> None:
        """Add a pyramid mesh."""
        s = size / 2
        self.vertices = np.array([
            # Base
            [-s, -s, s],
            [s, -s, s],
            [s, -s, -s],
            [-s, -s, -s],
            # Apex
            [0, s, 0],
        ], dtype=np.float32)

        self.indices = np.array([
            0, 1, 2, 0, 2, 3,  # Base
            0, 4, 1,            # Front
            1, 4, 2,            # Right
            2, 4, 3,            # Back
            3, 4, 0,            # Left
        ], dtype=np.uint32)

    def calculate_normals(self) -> None:
        """Calculate vertex normals."""
        if len(self.normals) == 0:
            self.normals = np.zeros_like(self.vertices)

        for i in range(0, len(self.indices), 3):
            i0, i1, i2 = self.indices[i:i+3]
            v0 = self.vertices[i0]
            v1 = self.vertices[i1]
            v2 = self.vertices[i2]

            edge1 = v1 - v0
            edge2 = v2 - v0
            normal = np.cross(edge1, edge2)

            self.normals[i0] += normal
            self.normals[i1] += normal
            self.normals[i2] += normal

        # Normalize
        for i in range(len(self.normals)):
            norm = np.linalg.norm(self.normals[i])
            if norm > 0:
                self.normals[i] /= norm

    def __repr__(self) -> str:
        return f"Mesh(name='{self.name}', vertices={len(self.vertices)}, indices={len(self.indices)})"


class Material:
    """Material for rendering."""

    def __init__(self, name: str = "Material"):
        self.name = name
        self.color = [1.0, 1.0, 1.0, 1.0]  # RGBA
        self.ambient = [0.2, 0.2, 0.2]
        self.diffuse = [0.8, 0.8, 0.8]
        self.specular = [1.0, 1.0, 1.0]
        self.shininess = 32.0
        self.texture = None  # Texture path or ID
        self.shader = None   # Shader program

    def __repr__(self) -> str:
        return f"Material(name='{self.name}')"


class AssetManager:
    """Manage scene assets (meshes, textures, materials)."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(AssetManager, cls).__new__(cls)
            cls._instance._meshes: Dict[str, Mesh] = {}
            cls._instance._materials: Dict[str, Material] = {}
            cls._instance._textures: Dict[str, int] = {}  # name -> texture ID
        return cls._instance

    def register_mesh(self, name: str, mesh: Mesh) -> None:
        """Register a mesh."""
        self._meshes[name] = mesh

    def get_mesh(self, name: str) -> Optional[Mesh]:
        """Get a mesh by name."""
        return self._meshes.get(name)

    def register_material(self, name: str, material: Material) -> None:
        """Register a material."""
        self._materials[name] = material

    def get_material(self, name: str) -> Optional[Material]:
        """Get a material by name."""
        return self._materials.get(name)

    def register_texture(self, name: str, texture_id: int) -> None:
        """Register a texture."""
        self._textures[name] = texture_id

    def get_texture(self, name: str) -> Optional[int]:
        """Get a texture ID by name."""
        return self._textures.get(name)

    def create_default_assets(self) -> None:
        """Create default meshes and materials."""
        # Default cube mesh
        cube_mesh = Mesh("DefaultCube")
        cube_mesh.add_cube(1.0)
        self.register_mesh("cube", cube_mesh)

        # Default sphere mesh
        sphere_mesh = Mesh("DefaultSphere")
        sphere_mesh.add_sphere(1.0)
        self.register_mesh("sphere", sphere_mesh)

        # Default pyramid mesh
        pyramid_mesh = Mesh("DefaultPyramid")
        pyramid_mesh.add_pyramid(1.0)
        self.register_mesh("pyramid", pyramid_mesh)

        # Default material
        material = Material("DefaultMaterial")
        self.register_material("default", material)

    def list_meshes(self) -> List[str]:
        """List all mesh names."""
        return list(self._meshes.keys())

    def list_materials(self) -> List[str]:
        """List all material names."""
        return list(self._materials.keys())
