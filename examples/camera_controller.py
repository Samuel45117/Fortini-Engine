"""Example: Simple Camera Controller."""

from fortini_engine.scripting.script import Script
import math


class CameraController(Script):
    """Simple camera controller for free-fly movement."""

    def __init__(self, game_object):
        super().__init__(game_object)
        self.speed = 5.0
        self.sensitivity = 0.1

    def start(self) -> None:
        """Called at startup."""
        super().start()
        print(f"Camera controller started for '{self.api.get_name()}'")

    def update(self, delta_time: float) -> None:
        """Called every frame."""
        # This would be expanded with input handling
        # For now, just a placeholder
        pass


if __name__ == "__main__":
    print("Example: Camera Controller Script")
