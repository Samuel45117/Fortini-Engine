"""Input management system for keyboard and mouse."""

import pygame
from typing import Dict, Callable, List


class Input:
    """Global input management system."""

    _instance = None
    _initialized = False

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(Input, cls).__new__(cls)
        return cls._instance

    def __init__(self):
        if Input._initialized:
            return

        Input._initialized = True
        self._keys_pressed = {}
        self._mouse_pos = (0, 0)
        self._mouse_buttons = {}
        self._key_callbacks: Dict[int, List[Callable]] = {}
        self._mouse_callbacks: Dict[str, List[Callable]] = {}

    def update(self) -> None:
        """Update input state. Call once per frame."""
        # Reset frame-based states
        self._reset_frame_states()

        # Handle pygame events
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                self._keys_pressed[event.key] = True
                self._trigger_key_callbacks(event.key, "down")
            elif event.type == pygame.KEYUP:
                self._keys_pressed[event.key] = False
                self._trigger_key_callbacks(event.key, "up")
            elif event.type == pygame.MOUSEBUTTONDOWN:
                self._mouse_buttons[event.button] = True
                self._trigger_mouse_callbacks("button_down", event.button)
            elif event.type == pygame.MOUSEBUTTONUP:
                self._mouse_buttons[event.button] = False
                self._trigger_mouse_callbacks("button_up", event.button)
            elif event.type == pygame.MOUSEMOTION:
                self._mouse_pos = event.pos
                self._trigger_mouse_callbacks("motion", event.pos)

    def _reset_frame_states(self) -> None:
        """Reset frame-specific input states."""
        pass

    def is_key_pressed(self, key: int) -> bool:
        """Check if a key is currently pressed."""
        return self._keys_pressed.get(key, False)

    def is_mouse_button_pressed(self, button: int) -> bool:
        """Check if a mouse button is currently pressed."""
        return self._mouse_buttons.get(button, False)

    def get_mouse_position(self) -> tuple:
        """Get current mouse position."""
        return self._mouse_pos

    def register_key_callback(self, key: int, callback: Callable) -> None:
        """Register a callback for key events."""
        if key not in self._key_callbacks:
            self._key_callbacks[key] = []
        self._key_callbacks[key].append(callback)

    def register_mouse_callback(self, event_type: str, callback: Callable) -> None:
        """Register a callback for mouse events."""
        if event_type not in self._mouse_callbacks:
            self._mouse_callbacks[event_type] = []
        self._mouse_callbacks[event_type].append(callback)

    def _trigger_key_callbacks(self, key: int, state: str) -> None:
        """Trigger registered key callbacks."""
        if key in self._key_callbacks:
            for callback in self._key_callbacks[key]:
                callback(state)

    def _trigger_mouse_callbacks(self, event_type: str, data) -> None:
        """Trigger registered mouse callbacks."""
        if event_type in self._mouse_callbacks:
            for callback in self._mouse_callbacks[event_type]:
                callback(data)

    # Convenience methods for common keys
    def is_key_w_pressed(self) -> bool:
        return self.is_key_pressed(pygame.K_w)

    def is_key_a_pressed(self) -> bool:
        return self.is_key_pressed(pygame.K_a)

    def is_key_s_pressed(self) -> bool:
        return self.is_key_pressed(pygame.K_s)

    def is_key_d_pressed(self) -> bool:
        return self.is_key_pressed(pygame.K_d)

    def is_key_space_pressed(self) -> bool:
        return self.is_key_pressed(pygame.K_SPACE)

    def is_key_escape_pressed(self) -> bool:
        return self.is_key_pressed(pygame.K_ESCAPE)
