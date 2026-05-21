# ruff: noqa: E402,I001
import os


os.environ.setdefault("SDL_VIDEODRIVER", "dummy")

import pygame

from game_engine.core.light import Light


def make_surface(size=(8, 8), color=(255, 255, 255, 255)):
    surface = pygame.Surface(size, pygame.SRCALPHA)
    surface.fill(color)
    return surface


def test_render_tints_light_with_light_color(monkeypatch):
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    monkeypatch.setattr(pygame.image, "load", lambda path: make_surface())

    light = Light((8, 8), light_color=(255, 0, 0))
    light.visibility_polygon = lambda light_pos, segments: [(0, 0), (7, 0), (7, 7), (0, 7)]

    result = light.render((0, 0), [((0, 0), make_surface((1, 1)))])

    assert result.get_at((4, 4)) == (255, 0, 0, 255)
