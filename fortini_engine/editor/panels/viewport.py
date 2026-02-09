"""Viewport Panel - 3D Scene View."""

try:
    # PyQt6 moved QOpenGLWidget to QtOpenGLWidgets
    from PyQt6.QtOpenGLWidgets import QOpenGLWidget
except Exception:
    from PyQt6.QtWidgets import QOpenGLWidget

from PyQt6.QtWidgets import QVBoxLayout, QWidget
from PyQt6.QtCore import Qt, QTimer
from OpenGL.GL import *
from OpenGL.GLU import *
import numpy as np


class ViewportPanel(QOpenGLWidget):
    """OpenGL viewport for scene rendering."""

    def __init__(self):
        super().__init__()
        self.scene = None
        self.camera = None
        self.last_pos = None

    def initializeGL(self) -> None:
        """Initialize OpenGL and create renderer if engine didn't create one."""
        # Ensure we have a renderer attached to the engine now that a GL context exists
        try:
            from fortini_engine.core.engine import GameEngine
            from fortini_engine.rendering.opengl_renderer import OpenGLRenderer
        except Exception:
            GameEngine = None
            OpenGLRenderer = None

        # Standard GL init for the widget
        glClearColor(0.1, 0.1, 0.1, 1.0)
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_MULTISAMPLE)

        # Create renderer now that context is current
        if GameEngine is not None:
            engine = GameEngine()
            if getattr(engine, 'renderer', None) is None and OpenGLRenderer is not None:
                try:
                    engine.renderer = OpenGLRenderer(self.width(), self.height())
                    engine.logger.info('Renderer created in Viewport.initializeGL')
                except Exception as e:
                    # Log but allow editor to continue — rendering will be disabled
                    try:
                        engine.logger.error(f'Failed to create OpenGLRenderer in viewport: {e}')
                    except Exception:
                        pass

    def resizeGL(self, w: int, h: int) -> None:
        """Handle resize."""
        glViewport(0, 0, w, h)
        if self.camera:
            self.camera.set_viewport(w, h)

    def paintGL(self) -> None:
        """Render the scene."""
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)

    def render_scene(self, scene, camera) -> None:
        """Render a scene."""
        self.scene = scene
        self.camera = camera
        self.update()

    def mousePressEvent(self, event) -> None:
        """Handle mouse press."""
        self.last_pos = event.pos()

    def mouseMoveEvent(self, event) -> None:
        """Handle mouse move (orbit camera)."""
        if self.last_pos is None:
            return

        delta_x = event.pos().x() - self.last_pos.x()
        delta_y = event.pos().y() - self.last_pos.y()

        # Simple camera rotation
        if event.buttons() & Qt.MouseButton.MiddleButton:
            if self.camera:
                sensitivity = 0.01
                self.camera.transform.translate(delta_x * sensitivity, delta_y * sensitivity, 0)

        self.last_pos = event.pos()

    def wheelEvent(self, event) -> None:
        """Handle mouse wheel (zoom)."""
        if self.camera:
            zoom_speed = 0.1
            delta = event.angleDelta().y() / 120
            self.camera.transform.translate(0, 0, delta * zoom_speed)
