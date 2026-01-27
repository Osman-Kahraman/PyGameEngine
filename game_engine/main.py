import pygame, repackage, os

timer = pygame.time.Clock()
surface_size = (1366, 768)
screen = pygame.display.set_mode(surface_size) #pygame.FULLSCREEN
pygame.display.set_caption("PyGameEngine")
pygame.mouse.set_visible(False)

from ui.images.init import *
repackage.up()
from package import *

from ui import home, game, designer

home_ = home.Window(screen)
game_ = None
designer_ = None

command = "home_start"
while command:
    if command.startswith("home"):
        command = home_.update()
    elif command.startswith("game"): 
        if game_ is None:
            os.chdir("game_1")
            game_ = game.Window(screen)
        
        command = game_.update()
        
        if command.endswith("close"):
            home_.command = "home_start"
            game_.command = "game_start"
            command = "home_start"
    elif command.startswith("designer"):
        if designer_ is None:
            designer_ = designer.Window(screen) #It needs to be designer_.tile_dict_RAW and designer_.tile_dict parameters reloaded. 

        command = designer_.update()

        if command.endswith("close"):
            game_.command = "game_start"
            designer_.command = "designer_start"
            command = "game_start"

    if command == "quit":
        break

    pygame.display.update()

    timer.tick(60) #FPS Limit

pygame.quit()