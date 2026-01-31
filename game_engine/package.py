"""
UI Package
==========

Public interface for the game engine UI system.

This module exposes the main UI-related components
(Animation, Camera, Light, Physics, UI) while hiding
internal implementation details.
"""

# --- Core UI Components ---
from game_engine.core.animation import Animation
from game_engine.core.camera import Camera
from game_engine.core.light import Light
from game_engine.core.physic import Physic
from game_engine.core.ui import UI

__all__ = [
    "Animation",
    "Camera",
    "Light",
    "Physic",
    "UI",
]

__version__ = "0.1.0"
