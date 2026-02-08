"""Example: Simple Movement Script."""

from fortini_engine.scripting.script import Script
from fortini_engine.utils.math_utils import Vector3


class SimpleMovement(Script):
    """Simple example script for object movement."""

    def __init__(self, game_object):
        super().__init__(game_object)
        self.speed = 2.0
        self.direction = Vector3(1, 0, 0)

    def update(self, delta_time: float) -> None:
        """Called every frame."""
        # Move object
        movement = self.direction * (self.speed * delta_time)
        self.api.transform_translate(movement.x, movement.y, movement.z)

        # Simple bounce effect
        pos = self.api.get_position()
        if abs(pos[0]) > 10:
            self.direction.x *= -1


if __name__ == "__main__":
    print("This is an example script for Fortini Engine")
    print("Attach it to a GameObject in the editor to see it in action!")
