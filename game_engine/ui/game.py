import importlib, repackage, pygame, numpy as np, os

repackage.up()
from package import *
from event import pygame_

class Window:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.screen_size = screen.get_size()
        self.surface = pygame.Surface(np.array(self.screen_size) // 2).convert()
        self.surface_size = self.surface.get_size()

        self.func_dict = {}
        self.func_implementer("tiles.py", "datas")
        self.tile_dict_RAW, self.tile_dict = self.func_dict["tiles"].read(return_dict = "both")
        self.items = os.listdir("items")
        self.command = "game_start"

        if len(self.tile_dict.keys()) == 1:
            if not self.tile_dict[1]["layers"]:
                self.command = "designer_start"

    def func_implementer(self, funcName: str, directory: str):
        if not funcName.rstrip(".py") in self.func_dict.keys():
            spec = importlib.util.spec_from_file_location(funcName.rstrip(".py"), "{}/{}".format(directory, funcName))
            foo = importlib.util.module_from_spec(spec)
            spec.loader.exec_module(foo)

            self.func_dict.update({funcName.rstrip(".py"): foo})

    def update(self):
        pygame_.get()

        self.surface.fill((120, 107, 61)) #Green

        #-Controls----------------------------------------------------------------------------
        for event in pygame_.event:
            e_type = event.type

            if e_type == pygame.QUIT:
                self.command = "quit"
            elif e_type == pygame.KEYDOWN:
                key = event.key

                if key == pygame.K_ESCAPE:
                    self.command = "game_close"
                elif key == pygame.K_BACKQUOTE:
                    self.command = "designer_start"
        #-------------------------------------------------------------------------------------

        #-Tile Dictionary Loading------------------------------------------------------------------------------------------
        for key in sorted(self.tile_dict.keys()):
            for coords, image in self.tile_dict[key]["layers"].items():
                item = self.tile_dict_RAW[str(key)]["layers"][str(coords)].replace(".png", ".py")

                if item in self.items:
                    self.func_implementer(item, "items")
                    func = self.func_dict[item.rstrip(".py")]
                    obj = func.update(self.tile_dict)
                    image, coords = obj[0]
                    if len(obj) == 2: #if it's returning light
                        lght_img, lght_coords = obj[1]
                        lght_coords = (lght_coords[0] - Camera.coords[0], lght_coords[1] - Camera.coords[1])
                        self.surface.blit(lght_img, lght_coords)

                if self.tile_dict[key]["parallax"] != 0:
                    coords = coords - np.array(Camera.coords) // self.tile_dict[key]["parallax"]
                else:
                    coords = np.array(coords) - Camera.coords
                
                abe = (coords[0] + image.get_width(), coords[1] + image.get_height())
                foo = all((abe[0] >= 0, abe[1] >= 0))
                bar = all((coords[0] <= self.surface_size[0], coords[1] <= self.surface_size[1]))
                if foo and bar: #Game optimization: It does not render if the object is outside of the screen
                    self.surface.blit(image, coords)
        #------------------------------------------------------------------------------------------------------------------

        #-Setting Screen Size------------------------------------------
        self.screen.blit(pygame.transform.scale(self.surface, self.screen_size), (0, 0))
        #--------------------------------------------------------------

        return self.command