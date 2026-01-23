import repackage

repackage.up()
from package import *
from items.info import ITEMS

attributeMemory = {}
temp_image = pygame.image.load("images/built_in_images/character.png").convert_alpha()
class Pin:
    global attributeMemory

    def __init__(self, **attributes) -> None:
        for attribute in attributes.keys():
            if not attribute in attributeMemory.keys(): #if not hasattr(self, name):
                attributeMemory.update({attribute: attributes[attribute]})

    def __setattr__(self, name: str, value) -> None:
        attributeMemory[name] = value #super().__setattr__(name, value)

    def __getattribute__(self, name: str):
        return attributeMemory[name]

class Temp:
    def __init__(self, name, data = []):
        self.name = name
        ITEMS[name] = self

        with open("game_engine/items/info.json", "r") as file:
            data = json.loads(file.read())

            self.image_sizes = data[self.name]["sizes"]
            self.coords = data[self.name]["coords"]
            self.health = data[self.name]["health"]
            self.scale = data[self.name]["scale"]
            self.animations = data[self.name]["animations"]
            self.lights = data[self.name]["lights"]
            self.tiles = {}
            self.image = pygame.image.load("images/built_in_images/{}.png".format(self.name)).convert_alpha()
            self.velocity_x = 0
            self.velocity_y = 0

            self.on_ground = False

            self.GRAVITY = 1.2
            self.MAX_FALL_SPEED = 18

        self.surface = self.image

        self.direction = "Left"
        self.movementTimer = time.time()

        self.light_system = None

        for animationPATH in self.animations:
            exec("self.{} = Animation('{}', 12)".format(animationPATH.split("/")[-1].replace(" ", "_"), animationPATH))

        self.anim = ""
        self.run = True

    def collision(self):
        if self.anim:
            if self.coords[1] <= 1000:
                for i in self.tiles.keys():
                    if self.tiles[i]["hitbox"]:
                        result = Physic().pixel_perfect_collision([self.coords[0], self.coords[1]], self.image, self.tiles[i]["hitbox"], True)
                        if result:
                            overlap = result.overlap_rect
                            item_x, item_y = result.item_coords
                            item_w, item_h = result.item_size

                            if overlap.height < overlap.width: #y collision
                                if self.velocity_y > 0: # landing
                                    self.coords[1] = item_y - self.image_sizes[1]
                                    self.on_ground = True
                                elif self.velocity_y < 0: # head hit
                                    self.coords[1] = item_y + item_h
                                
                                self.velocity_y = 0
                            else: #x collision
                                if self.velocity_x > 0: # left hit
                                    self.coords[0] -= 1
                                elif self.velocity_x < 0: # right hit
                                    self.coords[0] += 1
                                
                                self.velocity_x = 0
                    else:
                        self.on_ground = False
            else:
                self.run = False
                self.anim = ""

    def info(self, infoName):
        with open("game_engine/items/info.json", "r") as file:
            data = json.loads(file.read())[infoName]

            return {"sizes": data["sizes"], 
                    "coords": data["coords"], 
                    "health": int(data["health"]), 
                    "scale": int(data["scale"]), 
                    "animations": data["animations"]}

    def decorate(self, func):
        def wrapper(tiles):
            if not self.tiles:
                self.tiles = tiles

            #-Animation Iterable System---------------------------------------------------------------------------
            if self.anim:
                if self.direction == "Right":
                    self.surface = pygame.transform.flip(next(self.anim), True, False)
                else:
                    self.surface = next(self.anim)
            else:
                self.surface = self.image
            #-----------------------------------------------------------------------------------------------------

            if self.run:
                """#-Gravity----------------------------------------
                if not self.on_ground:
                    self.velocity_y += self.GRAVITY
                    if self.velocity_y > self.MAX_FALL_SPEED:
                        self.velocity_y = self.MAX_FALL_SPEED
                #------------------------------------------------"""

                #-User Codes--------------------------------------------------------------------------------------
                func(tiles)
                #-------------------------------------------------------------------------------------------------

            #-Collision-------------------------------------------------------------------------------------------
            self.collision()
            #-----------------------------------------------------------------------------------------------------

            with open("game_engine/items/info.json", "r") as fileRead:
                data = json.loads(fileRead.read())

                data[self.name]["sizes"] = self.image_sizes
                data[self.name]["coords"] = self.coords
                data[self.name]["health"] = self.health
                data[self.name]["scale"] = self.scale
                data[self.name]["image"] = self.anim.frame_PATH if self.anim else f"images/built_in_images/{self.name}.png"

                try:
                    with open("game_engine/items/info.json", "w") as fileWrite:
                        json.dump(data, fileWrite)
                except PermissionError:
                    pass

            if self.lights:
                if self.light_system is None:
                    self.light_system = Light((self.lights["size"], self.lights["size"]))
                
                l_c_x, l_c_y = self.lights["coords"]
                size_mid = self.lights["size"] // 2
                c_x, c_y = self.coords
                light_pos = (c_x + l_c_x - size_mid, c_y + l_c_y - size_mid) #Inserting the source in the middle coords
                
                light_items = [[ITEMS[i].coords, ITEMS[i].surface] for i in ITEMS.keys() if i != self.name]
                light_surface = self.light_system.render(
                    light_pos,
                    light_items
                )

                return ((self.surface, self.coords), (light_surface, light_pos))
            else:
                return ((self.surface, self.coords), )

        return wrapper