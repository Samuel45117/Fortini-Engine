"""3D Game Object."""

import json
from typing import Dict, Any, Optional, List
from fortini_engine.core.transform import Transform


class GameObject:
    """Base 3D game object with transform and components."""

    _id_counter = 0

    def __init__(self, name: str = "GameObject", position=(0, 0, 0), parent=None):
        GameObject._id_counter += 1
        self.id = GameObject._id_counter
        self.name = name
        self.active = True

        self.transform = Transform(parent)
        self.transform.set_position(*position)

        self.components = {}
        self.children: List[GameObject] = []
        self.parent: Optional[GameObject] = parent

        # Mesh and material reference
        self.mesh = None
        self.material = None

        # Script component
        self.script = None

    def add_component(self, name: str, component: Any) -> None:
        """Add a component to the object."""
        self.components[name] = component

    def get_component(self, name: str) -> Optional[Any]:
        """Get a component by name."""
        return self.components.get(name)

    def add_child(self, child: "GameObject") -> None:
        """Add a child game object."""
        if child not in self.children:
            self.children.append(child)
            child.parent = self
            self.transform.add_child(child.transform)

    def remove_child(self, child: "GameObject") -> None:
        """Remove a child game object."""
        if child in self.children:
            self.children.remove(child)
            child.parent = None
            self.transform.remove_child(child.transform)

    def set_active(self, active: bool) -> None:
        """Set object active state."""
        self.active = active

    def find_child(self, name: str) -> Optional["GameObject"]:
        """Recursively find a child by name."""
        for child in self.children:
            if child.name == name:
                return child
            found = child.find_child(name)
            if found:
                return found
        return None

    def get_all_children(self, recursive: bool = True) -> List["GameObject"]:
        """Get all children."""
        if not recursive:
            return self.children.copy()

        all_children = []
        for child in self.children:
            all_children.append(child)
            all_children.extend(child.get_all_children(recursive=True))
        return all_children

    def to_dict(self) -> Dict[str, Any]:
        """Serialize to dictionary."""
        return {
            "id": self.id,
            "name": self.name,
            "active": self.active,
            "position": self.transform.position.to_tuple(),
            "rotation": (
                self.transform.rotation.x,
                self.transform.rotation.y,
                self.transform.rotation.z,
                self.transform.rotation.w,
            ),
            "scale": self.transform.scale.to_tuple(),
            "mesh": self.mesh,
            "material": self.material,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "GameObject":
        """Deserialize from dictionary."""
        obj = GameObject(name=data.get("name", "GameObject"))
        obj.id = data.get("id", obj.id)
        obj.active = data.get("active", True)

        pos = data.get("position", (0, 0, 0))
        obj.transform.set_position(*pos)

        obj.mesh = data.get("mesh")
        obj.material = data.get("material")

        return obj

    def update(self, delta_time: float) -> None:
        """Update the object and its children."""
        if not self.active:
            return

        # Call script update if present
        if self.script and hasattr(self.script, "update"):
            self.script.update(delta_time)

        # Update children
        for child in self.children:
            child.update(delta_time)

    def __repr__(self) -> str:
        return f"GameObject(id={self.id}, name='{self.name}', pos={self.transform.position})"
