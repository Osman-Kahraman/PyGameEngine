import os

import pygame

# TODO: add caching


class Images:
    def __init__(self):
        base_path = os.path.join(os.path.dirname(__file__))
        self._images = {}

        for file in os.listdir(base_path):
            if file.endswith(".png"):
                name, _ = os.path.splitext(file)  # remove file extension
                path = os.path.join(base_path, file)
                self._images[name] = pygame.image.load(path).convert_alpha()

        print("Loaded images:", list(self._images.keys()))

    def __getattr__(self, item):
        return self._images.get(item)


IMAGES = Images()
