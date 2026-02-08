"""Python Scripting System."""

import importlib.util
import sys
from pathlib import Path
from typing import Optional, Any, Dict
from fortini_engine.utils.logger import Logger


class ScriptingAPI:
    """API available to game scripts."""

    def __init__(self, game_object):
        self.game_object = game_object

    def transform_translate(self, x: float, y: float, z: float) -> None:
        """Translate the object."""
        self.game_object.transform.translate(x, y, z)

    def transform_set_position(self, x: float, y: float, z: float) -> None:
        """Set position."""
        self.game_object.transform.set_position(x, y, z)

    def transform_set_rotation(self, pitch: float, yaw: float, roll: float) -> None:
        """Set rotation."""
        self.game_object.transform.set_rotation(pitch, yaw, roll)

    def transform_set_scale(self, x: float, y: float, z: float) -> None:
        """Set scale."""
        self.game_object.transform.set_scale(x, y, z)

    def get_position(self) -> tuple:
        """Get position."""
        return self.game_object.transform.position.to_tuple()

    def get_scale(self) -> tuple:
        """Get scale."""
        return self.game_object.transform.scale.to_tuple()

    def set_active(self, active: bool) -> None:
        """Set object active state."""
        self.game_object.set_active(active)

    def get_name(self) -> str:
        """Get object name."""
        return self.game_object.name


class Script:
    """Base class for game scripts."""

    def __init__(self, game_object):
        self.game_object = game_object
        self.api = ScriptingAPI(game_object)

    def start(self) -> None:
        """Called when the game starts."""
        pass

    def update(self, delta_time: float) -> None:
        """Called every frame."""
        pass

    def on_destroy(self) -> None:
        """Called when the object is destroyed."""
        pass


class ScriptManager:
    """Manage loading and executing game scripts."""

    def __init__(self):
        self.logger = Logger().get_logger(self.__class__.__name__)
        self.loaded_scripts: Dict[str, Any] = {}

    def load_script(self, script_path: Path) -> Optional[type]:
        """Load a Python script from a file."""
        if not script_path.exists():
            self.logger.error(f"Script not found: {script_path}")
            return None

        try:
            spec = importlib.util.spec_from_file_location(script_path.stem, script_path)
            module = importlib.util.module_from_spec(spec)
            sys.modules[script_path.stem] = module
            spec.loader.exec_module(module)

            # Look for a Script class
            if hasattr(module, "Script"):
                self.loaded_scripts[script_path.stem] = module.Script
                self.logger.info(f"Loaded script: {script_path.stem}")
                return module.Script
            else:
                self.logger.warning(f"No Script class found in {script_path}")
                return None

        except Exception as e:
            self.logger.error(f"Failed to load script {script_path}: {e}")
            return None

    def create_script_instance(self, script_class: type, game_object):
        """Create an instance of a script."""
        try:
            instance = script_class(game_object)
            instance.start()
            return instance
        except Exception as e:
            self.logger.error(f"Failed to instantiate script: {e}")
            return None

    def load_and_attach_script(self, script_path: Path, game_object):
        """Load a script and attach it to a game object."""
        script_class = self.load_script(script_path)
        if script_class:
            script = self.create_script_instance(script_class, game_object)
            game_object.script = script
            return script
        return None
