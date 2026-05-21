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


def test_template_uses_configured_light_rgb(monkeypatch, tmp_path):
    pygame.display.init()
    pygame.display.set_mode((1, 1))
    from game_engine.items import template

    items_dir = tmp_path / "items"
    items_dir.mkdir()
    (items_dir / "info.json").write_text(
        """
        {
          "streetLight": {
            "sizes": [8, 8],
            "coords": [10, 20],
            "health": 100,
            "scale": 1,
            "animations": [],
            "image": "street-light.png",
            "lights": {"coords": [4, 4], "size": 16, "RGB": [150, 30, 10]}
          }
        }
        """,
        encoding="utf-8",
    )

    created_lights = []

    class FakeLight:
        def __init__(self, size, light_color=(255, 255, 255)):
            self.light_color = tuple(light_color)
            created_lights.append((size, self.light_color))

        def render(self, light_pos, items):
            return make_surface((16, 16), (*self.light_color, 255))

    monkeypatch.chdir(tmp_path)
    monkeypatch.setattr(template.pygame.image, "load", lambda path: make_surface())
    monkeypatch.setattr(template, "Light", FakeLight)
    monkeypatch.setattr(template, "ITEMS", {})

    item = template.Temp("streetLight")
    item.decorate(lambda tiles: None)({})

    assert created_lights == [((16, 16), (150, 30, 10))]
