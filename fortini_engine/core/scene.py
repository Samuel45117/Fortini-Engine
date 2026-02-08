"""Scene management system."""

from typing import Dict, List, Optional, Any
from fortini_engine.core.game_object import GameObject
from fortini_engine.utils.logger import Logger


class Scene:
    """A scene containing game objects and hierarchy."""

    _active_scene = None

    def __init__(self, name: str = "Scene"):
        self.name = name
        self.objects: List[GameObject] = []
        self.root_objects: List[GameObject] = []
        self._object_dict: Dict[int, GameObject] = {}
        self.main_camera: Optional[GameObject] = None

        self.logger = Logger().get_logger(self.__class__.__name__)

    @classmethod
    def set_active_scene(cls, scene: "Scene") -> None:
        """Set the active scene."""
        cls._active_scene = scene

    @classmethod
    def get_active_scene(cls) -> Optional["Scene"]:
        """Get the active scene."""
        return cls._active_scene

    def add_object(self, obj: GameObject, parent: Optional[GameObject] = None) -> None:
        """Add a game object to the scene."""
        if obj.id not in self._object_dict:
            self.objects.append(obj)
            self._object_dict[obj.id] = obj

            if parent is None:
                if obj not in self.root_objects:
                    self.root_objects.append(obj)
            else:
                parent.add_child(obj)

            self.logger.info(f"Added object '{obj.name}' (ID: {obj.id}) to scene '{self.name}'")

    def remove_object(self, obj: GameObject) -> None:
        """Remove a game object from the scene."""
        if obj.id in self._object_dict:
            self.objects.remove(obj)
            del self._object_dict[obj.id]

            if obj in self.root_objects:
                self.root_objects.remove(obj)
            elif obj.parent:
                obj.parent.remove_child(obj)

            self.logger.info(f"Removed object '{obj.name}' (ID: {obj.id}) from scene '{self.name}'")

    def find_object(self, name: str) -> Optional[GameObject]:
        """Find an object by name."""
        for obj in self.objects:
            if obj.name == name:
                return obj
        return None

    def find_object_by_id(self, obj_id: int) -> Optional[GameObject]:
        """Find an object by ID."""
        return self._object_dict.get(obj_id)

    def get_all_objects(self) -> List[GameObject]:
        """Get all objects in the scene."""
        return self.objects.copy()

    def update(self, delta_time: float) -> None:
        """Update all root objects in the scene."""
        for obj in self.root_objects:
            if obj.active:
                obj.update(delta_time)

    def get_hierarchy(self) -> List[Dict[str, Any]]:
        """Get scene hierarchy as a list of dictionaries."""
        hierarchy = []
        for root in self.root_objects:
            hierarchy.append(self._object_to_hierarchy(root))
        return hierarchy

    def _object_to_hierarchy(self, obj: GameObject) -> Dict[str, Any]:
        """Convert object to hierarchy dictionary."""
        return {
            "id": obj.id,
            "name": obj.name,
            "active": obj.active,
            "children": [self._object_to_hierarchy(child) for child in obj.children],
        }

    def to_dict(self) -> Dict[str, Any]:
        """Serialize scene to dictionary."""
        return {
            "name": self.name,
            "objects": [obj.to_dict() for obj in self.root_objects],
            "main_camera": self.main_camera.id if self.main_camera else None,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Scene":
        """Deserialize scene from dictionary."""
        scene = Scene(data.get("name", "Scene"))
        # Objects would be reconstructed here
        return scene

    def __repr__(self) -> str:
        return f"Scene(name='{self.name}', objects={len(self.objects)})"
