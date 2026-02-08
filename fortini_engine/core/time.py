"""Time management system."""

import time


class Time:
    """Global time management for the engine."""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Time, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if Time._initialized:
            return

        Time._initialized = True
        self._start_time = time.time()
        self._last_frame_time = self._start_time
        self._delta_time = 0.0
        self._frame_count = 0
        self._fps = 0.0
        self._fps_update_interval = 1.0
        self._fps_timer = 0.0

    def update(self) -> None:
        """Update time tracking. Call once per frame."""
        current_time = time.time()
        self._delta_time = current_time - self._last_frame_time
        self._last_frame_time = current_time
        self._frame_count += 1

        # Update FPS calculation
        self._fps_timer += self._delta_time
        if self._fps_timer >= self._fps_update_interval:
            self._fps = self._frame_count / self._fps_timer
            self._frame_count = 0
            self._fps_timer = 0.0

    @property
    def delta_time(self) -> float:
        """Time elapsed since last frame in seconds."""
        return self._delta_time

    @property
    def elapsed_time(self) -> float:
        """Total time elapsed since engine start."""
        return time.time() - self._start_time

    @property
    def fps(self) -> float:
        """Frames per second."""
        return self._fps

    @property
    def frame_count(self) -> int:
        """Total frame count."""
        return self._frame_count

    def get_current_time(self) -> float:
        """Get current time in seconds."""
        return time.time()
