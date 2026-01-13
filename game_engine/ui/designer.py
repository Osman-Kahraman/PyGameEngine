import repackage, sys
from PIL import Image
from PyQt5 import QtWidgets

from images.init import *
import tiles
repackage.up()
from gameMotors import *

class Window:
    def __init__(self, screen: pygame.Surface):
        self.screen = screen
        self.surface = pygame.Surface(np.array(screen.get_size()) // 2).convert()
        self.tileset_choosing = ""
        self.drag_and_dropping = ""

        self.tile_dict_RAW, self.tile_dict = tiles.read(return_dict = "both")
        self.layer_amount = len(self.tile_dict)
        self.layer = 1
        self.tools_dict = {}
        self.tools_coords_dict = {}

        self.tile_x_size = None
        self.tile_y_size = None

        self.command = "designer_start"

        self.polygon_rects = []
        self.tileDictLocal = {}

        self.win_scale = self.screen.get_size()[0] // self.surface.get_size()[0]

        self.animation_folder = None

        self.tile_info_bool = False
        self.code_editor_bool = False
        self.animator_bool = False
        self.light_editor_bool = False
        self.cursor_bool = False
        self.drag_and_dropping_bool = False

        self.animation_command = "pause"

        self.cursor = image_.normalCursor
        self.cursor_pos = np.array(self.screen.get_size()) // 2

        self.animation_ = Animation("images/Animasyonlar/animationTimer", 1, 6)

        self.imageLoad()

    def imageLoad(self):
        image = Image.open("images/tileSet.png")
        rects = image.size

        try:
            os.mkdir("images/built_in_images/0set")
        except FileExistsError:
            image = None

        self.tile_x_size, self.tile_y_size = rects[0] // 6, rects[1] // 4

        var_1 = 0
        var_2 = 0
        while image:
            if var_1 < rects[0]:
                cropped_image = image.crop((var_1, var_2, var_1 + self.tile_x_size, var_2 + self.tile_y_size))
                while True:
                    try:
                        cropped_image.save("images/built_in_images/0set/{}.png".format((var_1, var_2)))
                        break
                    except PermissionError:
                        continue

                var_1 += self.tile_x_size
            else:
                var_1 = 0
                var_2 += self.tile_y_size
                if var_2 >= rects[1]:
                    break

        x = 10
        y = 10
        def x_collision(image, x, y):
            if x + image.get_size()[0] < 300:
                if os.listdir("images/built_in_images").index(image_name) != 0:
                    x += list(self.tools_dict.values())[-1]["image"].get_size()[0]
                else:
                    x += 5
            if x + image.get_size()[0] >= 300:
                x = 10
                y += image_.closeFolder.get_size()[1]

            return (x, y)

        for image_name in os.listdir("images/built_in_images"):
            if  image_name != ".DS_Store":
                if not image_name.endswith(".png"):
                    x, y = x_collision(image_.closeFolder, x, y)
                    collision = Physic.collision((x, y), image_.closeFolder, self.tools_dict, key = True)
                    if collision:
                        y = collision.item_coords[1] + self.tools_dict[collision.item_coords]["image"].get_size()[1]

                    self.tools_dict.update({(x, y): {"image": image_.closeFolder, "dir_name": image_name}})
                    
                    for tileImageName in os.listdir("images/built_in_images/{}".format(image_name)):
                        img = pygame.image.load("images/built_in_images/{}/{}".format(image_name, tileImageName)).convert_alpha()
                        self.tools_dict[(x, y)].update({tileImageName: img})
                else:
                    img = pygame.image.load("images/built_in_images/{}".format(image_name)).convert_alpha()

                    x, y = x_collision(img, x, y)
                    collision = Physic.collision((x, y), img, self.tools_dict, key = True)
                    if collision:
                        y = collision.item_coords[1] + self.tools_dict[collision.item_coords]["image"].get_size()[1]

                    self.tools_dict.update({(x, y): {"image": img, "dir_name": image_name}})

                self.tools_coords_dict.update({image_name: (x, y)})

    def auto_fill(self):
        tileDrawingIMG = pygame.Surface(self.screen.get_size()).convert()
        tileDrawingIMG.fill((25, 25, 25))
        pygame.draw.polygon(tileDrawingIMG, (255, 255, 255), self.polygon_rects)
        tileDrawingIMG.set_colorkey((25, 25, 25))

        x = [rect[0] for rect in self.polygon_rects]
        y = [rect[1] for rect in self.polygon_rects]

        xCoordsMin, yCoordsMin, xCoordsMax, yCoordsMax = min(x), min(y), max(x), max(y)

        filteredPolygonRect = []
        var = xCoordsMin
        while True:
            if var >= xCoordsMax:
                yCoordsMin += self.tile_y_size * self.win_scale
                var = xCoordsMin

            if yCoordsMin >= yCoordsMax:
                break

            image = self.tools_dict[self.tileset_choosing.item_coords]["({}, {}).png".format(self.tile_x_size * self.win_scale, self.tile_y_size * self.win_scale)]
            scaled_image = pygame.transform.scale(image, np.array([self.tile_x_size, self.tile_y_size]) * self.win_scale)
            if Physic.collision((var, yCoordsMin), scaled_image, {(0, 0): tileDrawingIMG}):
                filteredPolygonRect.append((var, yCoordsMin))
            var += self.tile_x_size * self.win_scale

        self.redesign(filteredPolygonRect)

    def redesign(self, filteredPolygonRect):
        for rect in filteredPolygonRect:
            signs = {
                "right": (rect[0] + (self.tile_x_size * self.win_scale), rect[1]) in filteredPolygonRect, 
                "left": (rect[0] - (self.tile_x_size * self.win_scale), rect[1]) in filteredPolygonRect, 
                "up": (rect[0], rect[1] - (self.tile_y_size * self.win_scale)) in filteredPolygonRect, 
                "down": (rect[0], rect[1] + (self.tile_y_size  * self.win_scale)) in filteredPolygonRect, 
                "right_up": (rect[0] + (self.tile_x_size * self.win_scale), rect[1] - (self.tile_y_size * self.win_scale)) in filteredPolygonRect, 
                "left_up": (rect[0] - (self.tile_x_size * self.win_scale), rect[1] - (self.tile_y_size * self.win_scale)) in filteredPolygonRect, 
                "right_down": (rect[0] + (self.tile_x_size * self.win_scale), rect[1] + (self.tile_y_size * self.win_scale)) in filteredPolygonRect, 
                "left_down": (rect[0] - (self.tile_x_size * self.win_scale), rect[1] + (self.tile_y_size * self.win_scale)) in filteredPolygonRect
            }
            
            tuned_rect = tuple(np.array(np.array(rect) // self.win_scale) + Camera.coords)
            tileset = self.tools_dict[self.tileset_choosing.item_coords]

            if signs["right"] and signs["left"] and not signs["up"] and signs["down"]:
                coords = "({}, 0).png".format(self.tile_x_size)
            elif signs["right"] and not signs["left"] and not signs["up"] and signs["down"]:
                coords = "(0, 0).png"
            elif not signs["right"] and signs["left"] and not signs["up"] and signs["down"]:
                coords = "({}, 0).png".format(self.tile_x_size * 2)
            elif signs["right"] and not signs["left"] and signs["up"] and signs["down"]:
                coords = "(0, {}).png".format(self.tile_y_size)
            elif not signs["right"] and signs["left"] and signs["up"] and signs["down"]:
                coords = "({}, {}).png".format(self.tile_x_size * 2, self.tile_y_size)
            elif signs["right"] and signs["left"] and signs["up"] and signs["down"] and not signs["left_up"]:
                coords = "({}, {}).png".format(self.tile_x_size * 5, self.tile_y_size)
            elif signs["right"] and signs["left"] and signs["up"] and signs["down"] and not signs["right_up"]:
                coords = "({}, {}).png".format(self.tile_x_size * 4, self.tile_y_size)
            elif not signs["right"] and signs["left"] and signs["up"] and not signs["down"] and not signs["right_down"]:
                coords = "({}, {}).png".format(self.tile_x_size * 2, self.tile_y_size * 2)
            elif signs["right"] and not signs["left"] and signs["up"] and not signs["down"] and not signs["left_down"]:
                coords = "(0, {}).png".format(self.tile_y_size * 2)
            elif signs["right"] and signs["left"] and signs["up"] and not signs["down"]:
                coords = "({}, {}).png".format(self.tile_x_size, self.tile_y_size * 2)
            elif signs["right"] and signs["left"] and signs["up"] and signs["down"] and not signs["left_down"]:
                coords = "({}, 0).png".format(self.tile_x_size * 5)
            elif signs["right"] and signs["left"] and signs["up"] and signs["down"] and not signs["right_down"]:
                coords = "({}, 0).png".format(self.tile_x_size * 4)
            elif not signs["right"] and not signs["left"] and not signs["up"] and not signs["down"]:
                coords = "({}, {}).png".format(self.tile_x_size * 3, self.tile_y_size *3)
            elif not signs["right"] and not signs["left"] and not signs["up"] and signs["down"]:
                coords = "({}, 0).png".format(self.tile_x_size * 3)
            elif not signs["right"] and not signs["left"] and signs["up"] and signs["down"]:
                coords = "({}, {}).png".format(self.tile_x_size * 3, self.tile_y_size)
            elif not signs["right"] and not signs["left"] and signs["up"] and not signs["down"]:
                coords = "({}, {}).png".format(self.tile_x_size * 3, self.tile_y_size * 2)
            elif signs["right"] and signs["left"] and not signs["up"] and not signs["down"]:
                coords = "({}, {}).png".format(self.tile_x_size, self.tile_y_size * 3)
            elif not signs["right"] and signs["left"] and not signs["up"] and not signs["down"]:
                coords = "({}, {}).png".format(self.tile_x_size * 2, self.tile_y_size * 3)
            elif signs["right"] and not signs["left"] and not signs["up"] and not signs["down"]:
                coords = "(0, {}).png".format(self.tile_y_size * 3)
            else:
                coords = "({}, {}).png".format(self.tile_x_size, self.tile_y_size)

            self.tile_dict_RAW[str(self.layer)]["layers"].update({str(tuned_rect): "{}/{}".format(tileset["dir_name"], coords)})
            self.tile_dict[self.layer]["layers"].update({tuned_rect: tileset[coords]})
    #----------------------------------------------------------------------------------------------------------------------------------------------------

    def converter(self, coords):
        if not self.tile_dict[self.layer]["parallax"]:
            converted = tuple((coords + np.array(Camera.coords) * self.win_scale) // self.win_scale)
        else:
            converted = tuple((coords + np.array(Camera.coords) * self.win_scale // self.tile_dict[self.layer]["parallax"]) // self.win_scale)
        
        converted = (int(converted[0]), int(converted[1]))

        return converted

    #-Display----------------------------------------------------------------------------------------------
    def update(self):
        pygame_.get()

        self.screen.fill((120, 107, 61)) #Green BAKILACAK

        #-Controls----------------------------------------------------------------------------
        for event in pygame_.event:
            e_type = event.type

            self.cursor_bool = False if e_type == 1 or e_type == 17 else True

            if e_type == pygame.QUIT:
                self.cursor_bool = False
                self.command = "quit"
            elif e_type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.command = "designer_close"
            elif e_type == pygame.MOUSEMOTION:
                self.cursor_pos = event.pos

                if self.drag_and_dropping and not self.tileset_choosing: 
                    self.drag_and_dropping_bool = True

                if any([
                    UI.listen("code_editor_open_button") == "waked_up", 
                    UI.listen("animator_open_button") == "waked_up", 
                    UI.listen("code_editor_close_button") == "waked_up", 
                    UI.listen("animator_close_button") == "waked_up", 
                    UI.listen("animator_play_button") == "waked_up", 
                    UI.listen("animator_pause_button") == "waked_up", 
                    UI.listen("new_layer_button") == "waked_up", 
                    UI.listen("animator_add_button") == "waked_up", 
                    UI.listen("light_editor_open_button") == "waked_up"
                    ]):
                    self.cursor = image_.choosingCursor
                elif any([
                    UI.listen("frame_{}".format(i)) == "resizing_r" or UI.listen("frame_{}".format(i)) == "resizing_l" for i in range(5)
                ]):
                    self.cursor = image_.extentCursorh
                elif UI.listen("code_editor") == "waked_up":
                    self.cursor = image_.textCursor
                elif self.polygon_rects: 
                    self.cursor = image_.drawingCursor
                    self.polygon_rects.append(self.cursor_pos)
                else:
                    self.cursor = image_.normalCursor
            elif e_type == pygame.MOUSEBUTTONDOWN:
                e_button = event.button
                cursor_interaction = Physic.collision(self.cursor_pos, self.cursor, self.tileDictLocal)

                if e_button == 1:
                    self.cursor = image_.normalCursorL

                    if self.tileset_choosing:
                        self.polygon_rects.append(self.cursor_pos)
                    else:
                        if cursor_interaction:
                            self.unconverted_objectCoords = cursor_interaction.item_coords
                            self.objectCoords = self.converter(self.unconverted_objectCoords)
                            self.objectName = self.tile_dict_RAW[str(self.layer)]["layers"][str(self.objectCoords)][:-4]
                            image = self.tile_dict[self.layer]["layers"][self.objectCoords]
                            self.objectSize = image.image_size if isinstance(image, Animation) else image.get_size()

                            try:
                                with open("game_engine/items/info.json", "r") as json_file:
                                    data = json.loads(json_file.read())

                                    self.objectHealth = data[self.objectName]["health"]
                                    self.objectScale = data[self.objectName]["scale"]
                                    self.objectAnims = data[self.objectName]["animations"].copy()
                            except KeyError:
                                self.objectHealth = 100 #Ayarlanacak
                                self.objectScale = 1 #Ayarlanacak
                                self.objectAnims = []
                            self.tile_info_bool = True
                        else:
                            if event.pos[0] < self.screen.get_size()[0] - 200 or event.pos[1] > 350:
                                self.tile_info_bool = False
                elif e_button == 3:
                    self.cursor = image_.normalCursorR
                    if cursor_interaction:
                        pop = self.converter(cursor_interaction.item_coords)

                        self.tile_dict_RAW[str(self.layer)]["layers"].pop(str(pop))                 
                        self.tile_dict[self.layer]["layers"].pop(pop)
                        self.tileDictLocal.clear()
            elif e_type == pygame.MOUSEBUTTONUP:
                self.cursor = image_.normalCursor

                if self.drag_and_dropping_bool:
                    foo = self.converter(self.cursor_pos)
                    bar = self.tools_dict[self.drag_and_dropping.item_coords]

                    self.tile_dict_RAW[str(self.layer)]["layers"].update({str(foo): bar["dir_name"]})
                    self.tile_dict[self.layer]["layers"].update({foo: bar["image"]})
                elif len(self.polygon_rects) > 2 and self.tileset_choosing:
                    self.auto_fill()

                self.polygon_rects = []
                self.drag_and_dropping = ""
                self.drag_and_dropping_bool = False
        #-------------------------------------------------------------------------------------

        #-Tile Dictionary Loading-------------------------------------------------------------------------------------------------------------------
        for key in sorted(self.tile_dict.keys()):
            layer_ = self.tile_dict[key]

            if layer_["visibility"]:
                for tile in layer_["layers"].keys():
                    try:
                        image_blit = pygame.transform.scale(layer_["layers"][tile], np.array(layer_["layers"][tile].get_size()) * self.win_scale)
                    except AttributeError:
                        image = next(layer_["layers"][tile]) if self.animation_command == "play" else layer_["layers"][tile].frame_image
                        image_blit = pygame.transform.scale(image, np.array(image.get_size()) * self.win_scale)

                    if not layer_["parallax"]:
                        coords_blit = np.array(tile) * self.win_scale - np.array(Camera.coords) * self.win_scale
                    else:
                        coords_blit = np.array(tile) * self.win_scale - np.array(Camera.coords) * self.win_scale // layer_["parallax"]
                    coords_blit = (int(coords_blit[0]), int(coords_blit[1]))

                    abe = (coords_blit[0] + image_blit.get_size()[0], coords_blit[1] + image_blit.get_size()[1])
                    foo = all((abe[0] >= 0, abe[1] >= 0))
                    bar = all((coords_blit[0] <= self.screen.get_size()[0], coords_blit[1] <= self.screen.get_size()[1]))
                    if foo and bar:
                        self.screen.blit(image_blit, coords_blit)
                        if self.layer == key:
                            if not coords_blit in self.tileDictLocal.keys():
                                self.tileDictLocal.update({coords_blit: image_blit})
        #-------------------------------------------------------------------------------------------------------------------------------------------

        #-Blitting of the Windows-------------------------------------------------------------------------------------------------------------------------
        #-Tile Info Window------------------------------------------------------------------------------------------------------
        if self.tile_info_bool:
            info_surf, info_coor = UI.window("info", (self.screen.get_size()[0] - 200, 50), (200, 300), (30, 30, 30), 2)
            UI.text(
                """Size: {}
Coords: {}
Health: {}
Scale: {}
Animation Amount: {}""".format(self.objectSize, self.objectCoords, self.objectHealth, self.objectScale, len(self.objectAnims)), 15, (5, 50), (170, 170, 170), "info")
            UI.window("info_name", (10, 10), (165, 30), (90, 90, 90), win_name = "info")
            UI.text(self.objectName, 21, (5, 0), (170, 170, 170), "info_name", font = "impact")
            UI.window("code_editor_open_button", (5, 260), (80, 20), (110, 110, 110), "button", win_name = "info")
            UI.add_images({
                (0, 0): image_.codeEditorOpenButton
                }, "code_editor_open_button")
            UI.window("animator_open_button", (100, 260), (80, 20), (110, 110, 110), "button", win_name = "info")
            UI.window("light_editor_open_button", (5, 230), (80, 20), (110, 110, 110), "button", win_name = "info")

            try:
                self.screen.blit(info_surf, info_coor)
            except TypeError: #It will trigger when one of the buttons clicked.
                if info_surf.item_coords == (5, 260):
                    self.code_editor_bool = True
                elif info_surf.item_coords == (100, 260):
                    self.animator_bool = True
                elif info_surf.item_coords == (5, 230):
                    self.light_editor_bool = True
        #----------------------------------------------------------------------------------------------------------------

        #-Tools Window-----------------------------------------------------------------------------------------------------
        tools_surf, tools_coor = UI.window("tools", (0, 50), (300, self.screen.get_size()[1] - 100), (30, 30, 30), 2)
        UI.add_images({
            key: self.tools_dict[key]["image"] for key in self.tools_dict.keys()
            }, "tools", clickable = True)
        try: 
            self.screen.blit(tools_surf, tools_coor)
        except TypeError: #It will trigger when one of the buttons clicked.
            if self.tools_dict[tools_surf.item_coords]["image"] == image_.closeFolder or self.tools_dict[tools_surf.item_coords]["image"] == image_.openFolder:
                UI.delete_images((
                        tools_surf.item_coords,
                ), "tools")

                self.tools_dict[tools_surf.item_coords]["image"] = image_.openFolder if tools_surf.item_collision_coords[1] < 16 else image_.closeFolder

                self.tileset_choosing = tools_surf
            else:
                self.tileset_choosing = None
                self.drag_and_dropping = tools_surf
        #------------------------------------------------------------------------------------------------------------------

        #-Layers Window--------------------------------------------------------------------------------------------------------------------------------
        layers_surf, layers_coor = UI.window("layers", tuple(np.array(self.screen.get_size()) - 200), (200, 150), (30, 30, 30), 2)
        UI.window("new_layer_button", (160, 5), (20, 20), (110, 110, 110), "button", win_name = "layers")
        UI.add_images({
                (0, 0): image_.newLayerButton
            }, "new_layer_button")
        layerTuneCrop = 25
        for i in range(1, self.layer_amount + 1):
            UI.window("layer{}_visibility".format(i), (5, layerTuneCrop), (20, 20), (100, 100, 100), "button", win_name = "layers")
            UI.add_images({
                (0, 0): image_.layerButtonVisibility
                }, "layer{}_visibility".format(i))
            UI.window("layer{}_parallax".format(i), (25, layerTuneCrop), (20, 20), (110, 110, 110), "button", win_name = "layers")
            UI.add_images({
                (0, 0): image_.layerButtonParallax
                }, "layer{}_parallax".format(i))
            UI.window("layer{}_button".format(i), (45, layerTuneCrop), (135, 20), (30, 30, 30), "button", win_name = "layers")
            UI.text("Katman {}".format(i), 13, (5, 0), (170, 170, 170), win_name = "layer{}_button".format(i))

            layerTuneCrop += 21

        try:
            self.screen.blit(layers_surf, layers_coor)
        except TypeError: #It will trigger when one of the buttons clicked.
            layer = layers_surf.item_coords[1] // 21
            if layers_surf.item_coords == (160, 5):
                self.layer_amount += 1

                self.tile_dict_RAW.update({str(self.layer_amount): {"layers": {}, "visibility": True, "parallax": 5 - 0.3 * self.layer_amount}})
                self.tile_dict.update({self.layer_amount: {"layers": {}, "visibility": True, "parallax": 5 - 0.3 * self.layer_amount}})
            elif layers_surf.item_coords[0] == 5: 
                self.tile_dict_RAW[str(layer)]["visibility"] = not self.tile_dict_RAW[str(layer)]["visibility"]
                self.tile_dict[layer]["visibility"] = not self.tile_dict[layer]["visibility"]
            elif layers_surf.item_coords[0] == 25: 
                if not self.tile_dict[layer]["parallax"]:
                    value = 5 - 0.3 * layer
                else:
                    value = 0

                self.tile_dict_RAW[str(layer)]["parallax"] = value
                self.tile_dict[layer]["parallax"] = value
                self.tileDictLocal.clear()
            elif layers_surf.item_coords[0] == 45:
                self.layer = layer

                self.tileDictLocal.clear()
        #----------------------------------------------------------------------------------------------------------------------------------------------

        #-Code Editor Window--------------------------------------------------------------------------------------------------------------
        if self.code_editor_bool:
            code_editor_name = "{}_c_e".format(self.objectName)
            code_editor_surf, code_editor_coor = UI.window("code_editor", (350, 100), (800, 500), (30, 30, 30), 2)
            UI.window("code_editor_close_button", (5, 5), (20, 20), (30, 30, 30), "button", win_name = "code_editor")
            UI.window(code_editor_name, (5, 30), (770, 430), (30, 30, 30), win_name = "code_editor", text_bool = True)
            UI.add_images({
                (0, 0): image_.closeButton
                }, "code_editor_close_button")
            try:
                self.screen.blit(code_editor_surf, code_editor_coor)
            except TypeError: #It will trigger when one of the buttons clicked.
                if code_editor_surf.item_coords == (5, 5): 
                    self.code_editor_bool = False
        #---------------------------------------------------------------------------------------------------------------------------------

        #-Animator Window-----------------------------------------------------------------------------------------------------
        elif self.animator_bool:
            anim_folders = "{}_anim_folders".format(self.objectName)
            anim_frames = "{}_anim_frames".format(self.objectName)

            animator_surf, animator_coor = UI.window("animator", (340, 0), (800, 200), (30, 30, 30), 2)
            UI.window("anim_close_b", (5, 5), (20, 20), (0, 30, 5), "button", win_name = "animator")
            UI.add_images({
                (0, 0): image_.closeButton
                }, "anim_close_b")
            UI.window("anim_add_b", (760, 5), (20, 20), (0, 30, 5), "button", win_name = "animator")
            UI.text("+", 21, (5, -5), (170, 170, 170), "anim_add_b", font = "impact")

            if self.objectAnims:
                UI.window(anim_folders, (5, 25), (775, 160), (30, 30, 30), win_name = "animator")
                for anim, coords in zip(self.objectAnims, range(len(self.objectAnims))):
                    anim = anim.split("/")[-1]
                    UI.window(anim, (coords * 64, 40), (84, 84), (130, 130, 130), "button", win_name = anim_folders)
                    UI.add_images({
                        (0, 0): image_.animFolder
                    }, anim)
                    UI.text(anim, 18, (0, 64), (255, 255, 255), anim)
            elif self.animation_folder:
                UI.delete_images(((5, 25), ), "animator")
                UI.window("anim_editor", (5, 25), (775, 160), (30, 30, 30), win_name = "animator")

                UI.window("edit_play_b", (350, 0), (30, 30), (0, 30, 5), "button", win_name = "anim_editor")
                UI.window("edit_pause_b", (390, 0), (30, 30), (0, 30, 5), "button", win_name = "anim_editor")
                UI.window(anim_frames, (30, 100), self.animation_.image_size, (66, 73, 73), win_name = "anim_editor")
                for i in range(len(os.listdir(self.animation_folder))): 
                    UI.window("frame_{}".format(i), (45 * i, 0), (50, self.animation_.image_size[1]), (255, 87, 51), 3, min_sizes = (5, self.animation_.image_size[1]), max_sizes = (1000, self.animation_.image_size[1]), win_name = anim_frames)
                if self.animation_command == "play":
                    UI.delete_images(((30, 80), ), "animator")
                    UI.add_images({
                                    (30, 80): self.animation_
                                }, "animator")
                else:
                    UI.add_images({
                        (30, 80): self.animation_.frame_image
                    }, "animator")

            try:
                self.screen.blit(animator_surf, animator_coor)
            except TypeError: #It will trigger when one of the buttons clicked.
                if animator_surf.item_coords == (5, 5): 
                    self.animator_bool = False
                elif animator_surf.item_coords == (350, 0):
                    for key in self.tile_dict.keys():
                        if self.objectName + ".png" in self.tile_dict_RAW[str(key)]["layers"].values():
                            self.tile_dict[key]["layers"][self.objectCoords] = Animation(self.animation_folder, 12)

                            self.animation_command = "play"

                elif animator_surf.item_coords == (390, 0):
                    self.animation_command = "pause"

                elif animator_surf.item_coords == (760, 5):
                    class Window_(QtWidgets.QWidget):
                        def __init__(self):
                            super().__init__()

                            msg = "Choose an Animation File for '{}' Sprite".format(self.objectName)
                            self.filePATH = QtWidgets.QFileDialog.getExistingDirectory(self, msg, os.getenv("HOME"))

                    app = QtWidgets.QApplication(sys.argv)

                    anim_PATH = Window_().filePATH
                    with open("game_engine/items/info.json", "r") as json_file:
                        data = json.loads(json_file.read())

                        data[self.objectName]["animations"].append(anim_PATH)
                        self.objectAnims = data[self.objectName]["animations"].copy()

                        with open("game_engine/items/info.json", "w") as json_file_w:
                            json.dump(data, json_file_w)
                elif animator_surf.item_coords[1] == 40:
                    self.animation_folder = self.objectAnims[animator_surf.item_index]
                    self.objectAnims = []
        #---------------------------------------------------------------------------------------------------------------------

        #-Light Editor Window--------------------------------------------------------------------------------------------------------------
        elif self.light_editor_bool:
            coords = list(self.unconverted_objectCoords)
            coords[0] += self.objectSize[0] * self.win_scale

            scrollbar_area = "{}_scrollbar_area".format(self.objectName)
            light_editor_surf, light_editor_coor = UI.window("light_editor", coords, (230, 170), (30, 30, 30), 2)
            UI.window("light_editor_close_button", (5, 5), (20, 20), (0, 30, 5), "button", win_name = "light_editor")
            UI.add_images({
                (0, 0): image_.closeButton
                }, "light_editor_close_button")
            UI.window(scrollbar_area, (5, 25), (200, 120), (30, 30, 30), text_bool = True, win_name = "light_editor")
            UI.text("R\nG\nB", 25, (70, 12), (200, 200, 200), scrollbar_area, font = "impact")
            UI.window("R", (100, 20), (100, 20), (200, 200, 200), "scrollbar", win_name = scrollbar_area)
            UI.window("G", (100, 50), (100, 20), (200, 200, 200), "scrollbar", win_name = scrollbar_area)
            UI.window("B", (100, 80), (100, 20), (200, 200, 200), "scrollbar", win_name = scrollbar_area)
            R = UI.listen("R")
            G = UI.listen("G")
            B = UI.listen("B")

            color_view = pygame.Surface((50, 100))
            color_view.fill((R, G, B))
            UI.add_images({
                (10, 10): color_view
                }, scrollbar_area)

            try:
                self.screen.blit(light_editor_surf, light_editor_coor)
            except TypeError: #It will trigger when one of the buttons clicked.
                with open("game_engine/items/info.json", "r") as json_file:
                    data = json.loads(json_file.read())

                    data[self.objectName]["lights"].update({
                        "coords": [0, 0], 
                        "size": 100, 
                        "RGB": (int(R), int(G), int(B))
                    })

                    with open("game_engine/items/info.json", "w") as json_file_w:
                        json.dump(data, json_file_w)

                self.light_editor_bool = False
        #----------------------------------------------------------------------------------------------------------------------------------
        #--------------------------------------------------------------------------------------------------------------------------------------------------

        #-Tileset Prelooking in the Tools Window-------------------------------------------------------------------------------------------
        if self.tileset_choosing:
            if self.tileset_choosing.item_collision_coords[1] < 16:
                coords = (self.tileset_choosing.item_coords[0] + image_.openFolder.get_size()[0], self.tileset_choosing.item_coords[1])
                window, coords = UI.window("folder_inside", coords, (200, 150), (230, 230, 230), 1)
                img = pygame.image.load("images/tileSet.png").convert_alpha()
                UI.add_images({
                    (0, 0): img
                }, "folder_inside")

                self.screen.blit(window, coords)
        #----------------------------------------------------------------------------------------------------------------------------------

        #-Tool Drag and Dropping Mechanism---------------------------------------------------------------------------
        if self.drag_and_dropping_bool:
            img = self.tools_dict[self.drag_and_dropping.item_coords]["image"]
            scale_ratio = tuple(np.array(self.tools_dict[self.drag_and_dropping.item_coords]["image"].get_size()) * self.win_scale)
            scaled_img = pygame.transform.scale(img, scale_ratio)
            coords = tuple(np.array(self.cursor_pos) - (np.array(self.drag_and_dropping.item_collision_coords) * self.win_scale))
            self.screen.blit(scaled_img, coords)
        #------------------------------------------------------------------------------------------------------------

        #-Auto Tile Mechanism's Choose Area---------------------------------
        if len(self.polygon_rects) > 2 and self.tileset_choosing:
            pygame.draw.polygon(self.screen, (255, 255, 255), self.polygon_rects)
        #-------------------------------------------------------------------

        #-Cursor----------------------------
        if self.cursor_bool:
            self.screen.blit(self.cursor, self.cursor_pos)
        #-----------------------------------

        if self.command == "designer_close":
            with open("game_engine/ui/tiles.json", "w") as file:
                json.dump(self.tile_dict_RAW, file)

        return self.command