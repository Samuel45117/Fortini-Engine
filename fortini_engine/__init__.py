"""
Fortini Engine - A lightweight Python game engine with integrated editor.

A desktop game engine designed for indie and hobby developers.
Features: OpenGL rendering, Python scripting, scene management, and a modern editor.
"""

__version__ = "1.0.0"
__author__ = "Fortini Contributors"

from fortini_engine.core.engine import GameEngine
from fortini_engine.core.time import Time
from fortini_engine.core.input import Input

__all__ = [
    "GameEngine",
    "Time",
    "Input",
]
