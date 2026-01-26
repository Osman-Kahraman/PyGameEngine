"""
UI Package
==========

Public interface for the game engine UI system.

This module exposes the main UI-related components
(Animation, Camera, Light, Physics, UI) while hiding
internal implementation details.
"""

import repackage
repackage.up()

# --- Core UI Components ---
from core.animation import Animation
from core.camera import Camera
from core.light import Light
from core.physic import Physic
from core.ui import UI

__all__ = [
    "Animation",
    "Camera",
    "Light",
    "Physic",
    "UI",
]

__version__ = "0.1.0"