import pygame, pygame.locals

class pygame_:
    event = []

    @classmethod
    def get(cls):
        cls.event = pygame.event.get()