"""Editor UI - Main Window."""

from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, 
    QToolBar, QPushButton, QLabel, QSplitter, QDockWidget
)
from PyQt6.QtCore import Qt, QTimer
from PyQt6.QtGui import QAction, QIcon

from fortini_engine.editor.panels.viewport import ViewportPanel
from fortini_engine.editor.panels.hierarchy import HierarchyPanel
from fortini_engine.editor.panels.inspector import InspectorPanel
from fortini_engine.editor.panels.assets import AssetBrowserPanel
from fortini_engine.editor.panels.console import ConsolePanel
from fortini_engine.utils.logger import Logger


class FortiniEditor(QMainWindow):
    """Main editor window."""

    def __init__(self):
        super().__init__()
        self.logger = Logger().get_logger(self.__class__.__name__)
        self.setWindowTitle("Fortini Engine Editor")
        self.setGeometry(100, 100, 1600, 900)

        self._create_ui()
        self._setup_engine()
        self._setup_signals()

        self.is_playing = False

    def _create_ui(self) -> None:
        """Create UI components."""
        # Central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        # Main layout
        main_layout = QHBoxLayout(central_widget)

        # Left panel (Hierarchy)
        self.hierarchy_panel = HierarchyPanel()
        left_dock = QDockWidget("Hierarchy")
        left_dock.setWidget(self.hierarchy_panel)
        self.addDockWidget(Qt.DockWidgetArea.LeftDockWidgetArea, left_dock)

        # Center (Viewport)
        self.viewport = ViewportPanel()
        main_layout.addWidget(self.viewport, 2)

        # Right panel (Inspector)
        self.inspector_panel = InspectorPanel()
        right_dock = QDockWidget("Inspector")
        right_dock.setWidget(self.inspector_panel)
        self.addDockWidget(Qt.DockWidgetArea.RightDockWidgetArea, right_dock)

        # Asset browser
        self.asset_browser = AssetBrowserPanel()
        asset_dock = QDockWidget("Assets")
        asset_dock.setWidget(self.asset_browser)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, asset_dock)

        # Console
        self.console_panel = ConsolePanel()
        console_dock = QDockWidget("Console")
        console_dock.setWidget(self.console_panel)
        self.addDockWidget(Qt.DockWidgetArea.BottomDockWidgetArea, console_dock)

        # Toolbar
        self._create_toolbar()

    def _create_toolbar(self) -> None:
        """Create top toolbar."""
        toolbar = self.addToolBar("Main Toolbar")
        toolbar.setMovable(False)

        # Play button
        self.play_action = QAction("▶ Play", self)
        self.play_action.triggered.connect(self._on_play)
        toolbar.addAction(self.play_action)

        # Stop button
        self.stop_action = QAction("⏹ Stop", self)
        self.stop_action.triggered.connect(self._on_stop)
        self.stop_action.setEnabled(False)
        toolbar.addAction(self.stop_action)

        toolbar.addSeparator()

        # FPS label
        self.fps_label = QLabel("FPS: 0")
        toolbar.addWidget(self.fps_label)

    def _setup_engine(self) -> None:
        """Setup game engine."""
        from fortini_engine.core.engine import GameEngine
        from fortini_engine.core.game_object import GameObject
        from fortini_engine.assets.manager import AssetManager

        self.engine = GameEngine()
        self.asset_manager = AssetManager()

        # Initialize engine for editor (don't create pygame display/renderer here)
        self.engine.initialize(self.viewport.width(), self.viewport.height(), "Fortini Editor", create_display=False, create_renderer=False)

        # Create default objects
        cube = GameObject("Cube")
        cube.mesh = self.asset_manager.get_mesh("cube")
        cube.material = self.asset_manager.get_material("default")
        self.engine.current_scene.add_object(cube)

        # Update hierarchy
        self.hierarchy_panel.set_scene(self.engine.current_scene)

    def _setup_signals(self) -> None:
        """Setup signal connections."""
        # Update timer
        self.update_timer = QTimer()
        self.update_timer.timeout.connect(self._on_timer_tick)
        self.update_timer.start(16)  # ~60 FPS

        # Hierarchy selection
        self.hierarchy_panel.object_selected.connect(self._on_object_selected)

    def _on_timer_tick(self) -> None:
        """Update engine and UI."""
        if not self.is_playing:
            # Editor mode - update time and render
            self.engine.update()
        
        # Render
        self.viewport.render_scene(self.engine.current_scene, self.engine.main_camera)

        # Update FPS
        self.fps_label.setText(f"FPS: {self.engine.get_fps():.1f}")

    def _on_play(self) -> None:
        """Start game."""
        self.is_playing = True
        self.play_action.setEnabled(False)
        self.stop_action.setEnabled(True)
        self.logger.info("Game started")

    def _on_stop(self) -> None:
        """Stop game."""
        self.is_playing = False
        self.play_action.setEnabled(True)
        self.stop_action.setEnabled(False)
        self.logger.info("Game stopped")

    def _on_object_selected(self, game_object) -> None:
        """Update inspector when object is selected."""
        self.inspector_panel.set_object(game_object)

    def closeEvent(self, event) -> None:
        """Handle window close."""
        self.engine.shutdown()
        event.accept()
