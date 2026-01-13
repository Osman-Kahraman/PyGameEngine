import repackage

repackage.up()
from gameMotors import *

attributeMemory = {}
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
    def __init__(self, name):
        self.name = name

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

        self.surface = self.image

        self.direction = "Left"
        self.movementTimer = time.time()

        for animationPATH in self.animations:
            exec("self.{} = Animation('{}', 12)".format(animationPATH.split("/")[-1].replace(" ", "_"), animationPATH))

        self.anim = ""
        self.run = True

    def collision(self):
        if self.anim:
            if self.coords[1] <= 1000:
                result = Physic().collision(self.coords, self.anim.frame_image, self.tiles[5]["layers"], True, "basic")
                if result:
                    if result.item_collision_coords[1] < result.item_size[1] // 2:
                        self.coords[1] -= result.item_collision_coords[1]
                else:
                    self.coords[1] += 10
                result = Physic().collision((self.coords[0], self.coords[1] - 10), self.anim.frame_image, self.tiles[5]["layers"], True, "basic")
                if result:
                    if result.item_collision_coords[0] < result.item_size[0] // 2:
                        self.coords[0] -= result.item_collision_coords[0]
                    else:
                        self.coords[0] += result.item_size[0] - result.item_collision_coords[0]
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
                data[self.name]["image"] = self.anim.frame_PATH if self.anim else "images/built_in_images/{}.png".format(self.name)

                try:
                    with open("game_engine/items/info.json", "w") as fileWrite:
                        json.dump(data, fileWrite)
                except PermissionError:
                    pass

            if self.lights:
                bar = Light.source(np.array(self.coords) + self.lights["coords"] - self.lights["size"], self.lights["size"], self.lights["RGB"], data, alias = self.name)

                return ((self.surface, self.coords), (bar, np.array(self.coords) + self.lights["coords"] - self.lights["size"]))
            else:
                return ((self.surface, self.coords), )

        return wrapper