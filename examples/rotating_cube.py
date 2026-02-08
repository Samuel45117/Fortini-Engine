"""Example: Rotating Cube Script."""

from fortini_engine.scripting.script import Script
import math


class RotatingCube(Script):
    """Simple rotating cube script."""

    def __init__(self, game_object):
        super().__init__(game_object)
        self.rotation_speed = 2.0  # radians per second

    def update(self, delta_time: float) -> None:
        """Called every frame."""
        # Rotate around Y axis
        angle = self.rotation_speed * delta_time
        self.api.transform_translate(0, 0, 0)  # Keep position
        # Note: Full rotation implementation would require proper quaternion
        # This is a simplified example


if __name__ == "__main__":
    print("Example: Rotating Cube Script")
