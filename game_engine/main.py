import pygame, repackage, os

timer = pygame.time.Clock()
surface_size = (1366, 768)
screen = pygame.display.set_mode(surface_size)
pygame.display.set_caption("PyGameEngine")
pygame.mouse.set_visible(False)

os.chdir("game_1")

from ui.images.init import *
repackage.up()
from package import *

from ui import home, game, designer

home_ = home.Window(screen)
game_ = game.Window(screen)
designer_ = designer.Window(screen)

command = "home_start"
while command:
    if command.startswith("home"):
        command = home_.update()
        game_.command = "game_start"
        if command.endswith("close"): 
            pass
    elif command.startswith("game"): 
        command = game_.update()
        home_.command = "home_start"
        designer_.command = "designer_start"
        if command.endswith("close"):
            command = "home_start"
        elif command == "designer_start":
            designer_ = designer.Window(screen) #It needs to be designer_.tile_dict_RAW and designer_.tile_dict parameters reloaded. 
    else:
        command = designer_.update()
        game_.command = "game_start"
        if command.endswith("close"):
            game_ = game.Window(screen)
            command = "game_start"

    if command == "quit":
        break

    pygame.display.update()

    timer.tick(60) #FPS Limit

pygame.quit()