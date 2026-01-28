from os import listdir

import pygame
import pygame.locals


class image_:
    for image in listdir("game_engine/ui/images"):
        if image.endswith(".png"):
            script = pygame.image.load("game_engine/ui/images/" + image).convert_alpha()
            exec("{} = script".format(image[:-4]))
