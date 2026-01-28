import pygame


class pygame_:
    event = []

    @classmethod
    def get(cls):
        cls.event = pygame.event.get()
