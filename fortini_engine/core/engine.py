"""Core game engine module."""

import pygame
from typing import Optional, List
from fortini_engine.core.time import Time
from fortini_engine.core.input import Input
from fortini_engine.core.scene import Scene
from fortini_engine.core.camera import PerspectiveCamera
from fortini_engine.assets.manager import AssetManager
from fortini_engine.utils.logger import Logger
from fortini_engine.rendering.opengl_renderer import OpenGLRenderer


class GameEngine:
    """Main game engine coordinator."""

    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(GameEngine, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        self._initialized = False

    def initialize(self, width: int = 1280, height: int = 720, title: str = "Fortini Engine"):
        """Initialize the game engine."""
        if self._initialized:
            return

        self._initialized = True
        self.width = width
        self.height = height
        self.title = title
        self.running = False

        # Initialize systems
        self.logger = Logger()
        self.logger.info(f"Initializing {title} ({width}x{height})")

        self.time = Time()
        self.input = Input()
        self.asset_manager = AssetManager()
        self.asset_manager.create_default_assets()

        # Initialize Pygame
        pygame.init()
        pygame.display.set_mode((width, height))
        pygame.display.set_caption(title)

        # Initialize renderer
        self.renderer = OpenGLRenderer(width, height)

        # Create default scene
        self.current_scene = Scene("DefaultScene")
        Scene.set_active_scene(self.current_scene)

        # Create default camera
        self.main_camera = PerspectiveCamera("MainCamera", fov=45.0, aspect=width / height)
        self.main_camera.transform.position = self.main_camera.transform.position + [0, 0, 5]
        self.current_scene.add_object(self.main_camera)
        self.current_scene.main_camera = self.main_camera

        self.logger.info("Engine initialized successfully")

    def update(self) -> None:
        """Update engine systems."""
        self.time.update()
        self.input.update()

        if self.current_scene:
            self.current_scene.update(self.time.delta_time)

    def render(self) -> None:
        """Render current scene."""
        if self.renderer and self.current_scene:
            self.renderer.render(self.current_scene, self.main_camera)

    def run(self) -> None:
        """Start the main game loop."""
        self.running = True
        self.logger.info("Starting game loop")

        clock = pygame.time.Clock()

        while self.running:
            # Handle quit event
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            self.update()
            self.render()

            clock.tick(60)  # 60 FPS

        self.shutdown()

    def shutdown(self) -> None:
        """Shutdown the engine."""
        self.logger.info("Shutting down engine")
        if self.renderer:
            self.renderer.cleanup()
        pygame.quit()
        self.running = False

    def set_scene(self, scene: Scene) -> None:
        """Set the active scene."""
        self.current_scene = scene
        Scene.set_active_scene(scene)
        self.logger.info(f"Switched to scene '{scene.name}'")

    def get_fps(self) -> float:
        """Get current FPS."""
        return self.time.fps

    def __repr__(self) -> str:
        return f"GameEngine(title='{self.title}', resolution={self.width}x{self.height})"
