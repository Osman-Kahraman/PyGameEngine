from typing import overload
import pygame, numpy as np,  json, repackage
from unicodedata import name

from ui.images.init import *
from core.animation import Animation
from core.physic import Physic
repackage.up()
from event import *

pygame.init()

class UI:
    """
UI
==

Creates UI tools. Which they are window and text.

Basic Usage of the Class:
-------------------------
>>> UI.delete_images(...) #You must set the parameters.
>>> UI.add_images(...) #You must set the parameters.
>>> UI.fill(...) #You must set the parameters.
>>> UI.listen(...) #You must set the parameters.
>>> UI.window(...) #You must set the parameters.
>>> UI.text(...) #You must set the parameters.

The Class Variable;
-------------------
>>> physic_var.gen_obj #You can only use if you create the class variable.  

Function(s);/
`delete_images`
`add_images`
`listen`
`window`
`text`
    """

    memory = {}
    cursor_pos = (0, 0)
    selam = 1
    pointer = Animation("game_engine/ui/images/pointer", 4)

    @classmethod
    def delete_images(cls, coords: list or tuple, win_name: str) -> list:
        """
        It deletes the images from the window. You must give the name with parameter.

        Examples of the Parameters;
        ---------------------------
        >>> coords = [(1, 2)] #x and y coordinates
        >>> win_name = "clippy"
        """

        images = cls.memory[win_name]["text"]["images"]
        clickables = images["clickables"]
        not_clickables = images["not_clickables"]

        dels = [clickables.pop(coord) if coord in clickables else not_clickables.pop(coord) for coord in coords]
        return dels

    @classmethod
    def add_images(cls, images: dict, win_name: str, clickable: bool = False) -> None:
        """
        You can add an image or images to the window with this function. Also the images can be set clickable or not-clickable. 

        Examples of the Parameters;
        ---------------------------
        >>> images = {{(3, 4): pygame_image_1, (5, 6): pygame_image_2}}
        >>> win_name = "bob"
        """

        if type(images) != dict:
            raise TypeError("images parameter type must be a dict, not {}".format(type(images)))

        try: 
            cls.memory[win_name]
        except KeyError:
            raise KeyError("{name} not found. You must set {name} first.".format(name = win_name))
        else:
            clickable_distinction = "clickables" if clickable else "not_clickables"
            cls.memory[win_name]["text"]["images"][clickable_distinction].update(images)

    @classmethod
    def listen(cls, win_name: str) -> str:
        """
        You can track the window name. 

        Examples of the Parameters;
        ---------------------------
        >>> win_name = "rover"
        """

        try:
            return cls.memory[win_name]["condition"]
        except KeyError:
            return f'win_name "{win_name}" not found'

    @overload
    def window(self, name: str, coords: tuple or list, size: tuple or list, color: tuple or list) -> pygame.Surface:
        """
        With this function, you can create a window surface and it makes calculation much easier and faster than normal effort. 

        Examples of the Parameters;
        ---------------------------
        >>> name = "hank"
        >>> coords = (1, 2) #x and y coordinates
        >>> size = (404, 500) #x and y coordinates
        >>> color = (255, 255, 255) #Red, Green, Blue values

        Types;/
        `basic`
        `button`
        `scrollbar`
        `1`
        `2`
        `3`
        """

    @overload
    def window(cls, name: str, coords: tuple or list, size: tuple or list, color: tuple or list, type_: str = None, text_bool: bool = False, win_name: str = None, min_sizes: tuple or list = None, max_sizes: tuple or list = None) -> pygame.Surface: ...

    @classmethod
    def window(cls, name: str, coords: tuple or list, size: tuple or list, color: tuple or list, type_: str = "basic", text_bool: bool = False, win_name: str = None, min_sizes: tuple or list = None, max_sizes: tuple or list = None) -> pygame.Surface:
        if min_sizes and max_sizes: 
            s = size if not win_name else cls.memory[win_name]["surface"].get_size()
            if min_sizes > s or max_sizes < s:
                raise ArithmeticError("min_sizes not bigger than {size} or max_sizes not lower than {size}".format(size = s))

        def color_fix_p(n): return 255 if n >= 225 else n + 30
        def color_fix_m(n): return 0 if n <= 30 else n - 30 

        def character_blit(name: str, surface: pygame.Surface):
            try:
                mem_imgs = cls.memory[name]["text"]["images"]
                scroll = cls.memory[name]["scroll"]
            except KeyError:
                pass
            else:
                for images in mem_imgs.values():
                    for coords, image in images.items():
                        image = next(image) if isinstance(image, Animation) else image
                        coords = (coords[0] + scroll[0], coords[1] + scroll[1])

                        abe = (coords[0] + image.get_size()[0], coords[1] + image.get_size()[1])
                        foo = all((abe[1] >= 0, coords[1] <= surface.get_size()[1]))
                        if foo:
                            bar = all((abe[0] >= 0, coords[0] <= surface.get_size()[0]))
                            if bar:
                                surface.blit(image, coords)

                if text_bool:
                    pointer_coords = list(mem_imgs["not_clickables"].keys())[-cls.selam] if list(mem_imgs["not_clickables"].keys()) else (0, 0)
                    pointer_coords += np.array(scroll) + (10, -5)

                    surface.blit(next(cls.pointer), pointer_coords)

        #-Important Variables Adding to the cls.memory--------------------------------------------------------------------------------
        try:
            cls.memory[name]
        except KeyError:
            cls.memory.update({name: {}})
        try:
            cls.memory[name]["surface"]
        except KeyError:
            surface = pygame.Surface(size)
            surface_in = pygame.Surface(np.array(size) - 6)
            surface_in_in = pygame.Surface(np.array(size) - 16)

            win_coords = list(coords)
            attached_win = win_name
            while attached_win:
                win_coords[0] += cls.memory[attached_win]["coords"][0]
                win_coords[1] += cls.memory[attached_win]["coords"][1]
                attached_win = cls.memory[attached_win]["win_name"] if cls.memory[attached_win]["win_name"] else None

            cls.memory[name].update({
                "surface": surface,
                "surface_in": surface_in,
                "surface_in_in": surface_in_in, 
                "coords": coords, 
                "win_coords": win_coords, 
                "win_name": win_name, 
                "scroll": [0, 0], 
                "condition": "idle", 
                "collision": None, 
                "text": {"images": {"clickables": {}, "not_clickables": {}}, "name": ""}
                })

            if text_bool:
                try:
                    if cls.memory["info_name"]["text"]["name"] + "_c_e" != name:
                        raise FileNotFoundError
                    with open("items/{}.py".format(cls.memory["info_name"]["text"]["name"]), "r", encoding = "utf-8") as file:
                        data = file.readlines()

                        start = data.index("    exec('''\n") + 1
                        end = data.index("    ''')")
                        user_codes = data[start:end]
                        user_codes = "".join(user_codes)

                        cls.text(user_codes, 1, (5, 30), (255, 255, 255), name, font = "normal_anim")
                except FileNotFoundError:
                    pass
        #------------------------------------------------------------------------------------------------------------------------------

        _memory = cls.memory[name]
        x_size, y_size = _memory["surface"].get_size()
        lightCursor_size = image_.lightCursor.get_size()

        def is_cursor_in_surface(x_result, y_result):
            foo = x_result >= 0 and y_result >= 0
            bar = x_result <= x_size and y_result <= y_size

            return foo and bar

        if win_name:
            aaw = cls.memory[win_name]["scroll"]
        else:
            aaw = 0
        x_result, y_result = np.array(cls.cursor_pos) - _memory["win_coords"] - aaw

        #-The event Parameter Setting-------------------------------------
        for event in pygame_.event:
            if event.type == pygame.KEYDOWN:
                if text_bool:
                    #-Keyboard Event Input Setting-----------------------------------------------------------------------
                    key = event.key

                    if key == pygame.K_s and pygame.key.get_mods() & pygame.KMOD_SHIFT:
                        name = cls.memory["info_name"]["text"]["name"]
                        with open(f"items/{name}.py", "w", encoding = "utf-8") as file:
                            file.write("""
import repackage

repackage.up()
repackage.up()
from game_engine.items.template import *

self = Temp("{}")

@self.decorate
def update(tiles):
    exec('''
{}
    ''')""".format(name, _memory["text"]["name"]))

                            with open("items/info.json", "r") as json_file:
                                data = json.loads(json_file.read())

                                if not name in data.keys():
                                    infos = cls.memory["info"]["text"]["name"].split("\n")
                                    sizesInfo = infos[0].lstrip("Size: ").lstrip("(").rstrip(")").split(", ")
                                    coordsInfo = infos[1].lstrip("Coords: ").lstrip("(").rstrip(")").split(", ")
                                    healthInfo = int(infos[2].lstrip("Health: "))
                                    scaleInfo = int(infos[3].lstrip("Scale: "))

                                    data.update({
                                        name: {
                                            "sizes": list(map(int, sizesInfo)),
                                            "coords": list(map(int, coordsInfo)), 
                                            "health": healthInfo, 
                                            "scale": scaleInfo, 
                                            "animations": [], 
                                            "image": "images/built_in_images/{}.png".format(name), 
                                            "lights": {}}
                                        })
                                    with open("items/info.json", "w") as json_file_w:
                                        json.dump(data, json_file_w)
                    elif key == pygame.K_BACKSPACE:
                        if _memory["text"]["name"][-1] != " " and _memory["text"]["images"]["not_clickables"]:
                            _memory["text"]["images"]["not_clickables"].popitem()
                        
                        _memory["text"]["name"] = _memory["text"]["name"][:-1]
                    elif key == pygame.K_UP:
                        cls.selam += 37
                    elif key == pygame.K_DOWN:
                        cls.selam -= 37
                    elif key == pygame.K_RIGHT:
                        cls.selam -= 1
                    elif key == pygame.K_LEFT:
                        cls.selam += 1
                    else:
                        cls.text(_memory["text"]["name"] + event.unicode, 1, (5, 30), (255, 255, 255), name, font = "normal_anim")
                    #----------------------------------------------------------------------------------------------------
            elif event.type == pygame.MOUSEMOTION:
                cls.cursor_pos = event.pos

                if event.buttons[0]:
                    if type(_memory["condition"]) == int:
                        if is_cursor_in_surface(x_result, y_result):
                            _memory["scroll"][0] = x_result
                    elif _memory["condition"].startswith("resizing"):
                        if win_name:
                            cls.delete_images([_memory["coords"]], win_name)

                        if _memory["condition"] == "resizing_l": 
                            x_size -= event.rel[0]
                            _memory["win_coords"][0] += event.rel[0]
                            _memory["coords"] = tuple(_memory["win_coords"])
                        elif _memory["condition"] == "resizing_r": 
                            x_size = x_result
                        elif _memory["condition"] == "resizing_t": 
                            y_size -= event.rel[1]
                            _memory["win_coords"][1] += event.rel[1]
                            _memory["coords"] = tuple(_memory["win_coords"])
                        else:
                            y_size = y_result
                    
                        if min_sizes[0] > x_size:
                            x_size = min_sizes[0]
                        elif min_sizes[1] > y_size:
                            y_size = min_sizes[1]
                        elif max_sizes[0] < x_size:
                            x_size = max_sizes[0]
                        elif max_sizes[1] < y_size:
                            y_size = max_sizes[1]

                        size = (x_size, y_size)
                        _memory["surface"] = pygame.Surface(size)
                        _memory["surface_in"] = pygame.Surface(np.array(size) - 6)
                        _memory["surface_in_in"] = pygame.Surface(np.array(size) - 16)
                else:
                    if type_ == "button" or type_ == 2:
                        if is_cursor_in_surface(x_result, y_result):
                            _memory["condition"] = "waked_up"
                        else:
                            _memory["condition"] = "idle"
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if is_cursor_in_surface(x_result, y_result):
                    if event.button == 1: 
                        collision_area = _memory["text"]["images"]["clickables"]
                        collision = Physic.rect_collision((x_result - _memory["scroll"][0], y_result - _memory["scroll"][1]), (1, 1), collision_area, True)

                        if collision:
                            if win_name:
                                cls.memory[win_name]["collision"] = collision
                            else:
                                return (collision, _memory["coords"])

                        if min_sizes and max_sizes:
                            if x_result > 0 and x_result < 10:
                                _memory["condition"] = "resizing_l"
                            elif x_result > x_size - 10 and x_result < x_size:
                                _memory["condition"] = "resizing_r"
                            elif y_result > 0 and y_result < 10:
                                _memory["condition"] = "resizing_t"
                            elif y_result > y_size - 10 and y_result < y_size: 
                                _memory["condition"] = "resizing_b"
                    elif len(_memory["text"]["images"]["clickables"].keys()) or len(_memory["text"]["images"]["not_clickables"].keys()):
                        sum = list(_memory["text"]["images"]["clickables"].keys()) + list(_memory["text"]["images"]["not_clickables"].keys())
                        if event.button == 4:
                            if _memory["scroll"][1] + 15 <= sum[0][1]:
                                _memory["scroll"][1] += 15
                        elif event.button == 5:
                            if sum[-1][1] + _memory["scroll"][1] + 15 >= size[1]:
                                _memory["scroll"][1] -= 15
            elif event.type == pygame.MOUSEBUTTONUP:
                _memory["condition"] = "idle"

            if _memory["collision"]:
                if win_name:
                    cls.memory[win_name]["collision"] = _memory["collision"]
                    _memory["collision"] = None
                else:
                    a = _memory["collision"]
                    _memory["collision"] = None
                    return (a, _memory["coords"])
        #-----------------------------------------------------------------

        #-The "type_" Parameter Setting-------------------------------------------------------------------------------------------------------------------------------------------------------
        if type_ == "basic":
            _memory["surface"].fill(color)

            character_blit(name, _memory["surface"])
        elif type_ == "button":
            if _memory["condition"] == "waked_up":
                _memory["surface"].fill(tuple(map(color_fix_p, color)))
            elif _memory["condition"] == "idle":
                _memory["surface"].fill(tuple(map(color_fix_m, color)))

            character_blit(name, _memory["surface"])
        elif type_ == "scrollbar":
            _memory["surface"].fill((0, 0, 0, 0))

            pygame.draw.rect(_memory["surface"], color, (_memory["scroll"][0], _memory["scroll"][1], 10, size[1]))

            _memory["condition"] = int(_memory["scroll"][0])
            character_blit(name, _memory["surface"])
        else:
            _memory["surface_in"].fill(tuple(map(color_fix_p, color)))

            if type_ == 1:
                _memory["surface_in"].blit(image_.lightCursor_4x, (x_result, y_result) - np.array(lightCursor_size) * 2)
                cene, bene = _memory["surface_in"].get_size()
                pygame.draw.rect(_memory["surface_in"], tuple(map(color_fix_m, color)), (2, 2, cene - 4, bene - 4))

                character_blit(name, _memory["surface_in"])
            elif type_ == 2:
                _memory["surface_in_in"].fill(color)
                cene, bene = _memory["surface_in_in"].get_size()

                if _memory["condition"] == "waked_up":
                    _memory["surface_in_in"].blit(image_.lightCursor_4x, (x_result, y_result) - np.array(lightCursor_size) * 2)
                elif _memory["condition"] == "idle":
                    _memory["surface_in"].blit(image_.lightCursor_2x, np.array((x_result, y_result)) - lightCursor_size)
                
                pygame.draw.rect(_memory["surface_in_in"], color, (2, 2, cene - 4, bene - 4))
                
                character_blit(name, _memory["surface_in_in"])
                
                x, y = ((x_result, y_result) - np.array(size) // 2) // 64 + 5
                if x < 2 or x > 8:
                    if x < 2:
                        x = 2
                    else:
                        x = 8
                if y < 2 or y > 8:
                    if y < 2:
                        y = 2
                    else:
                        y = 8
                _memory["surface_in"].blit(_memory["surface_in_in"], (x, y))
            elif type_ == 3:
                cene, bene = _memory["surface_in"].get_size()
                pygame.draw.rect(_memory["surface_in"], tuple(map(color_fix_m, color)), (0, 0, cene, bene))

                character_blit(name, _memory["surface_in"])

            _memory["surface"].fill(color)
            _memory["surface"].blit(image_.lightCursor, (x_result, y_result) - np.array(lightCursor_size) // 2)
            _memory["surface"].blit(_memory["surface_in"], (3, 3))
        #------------------------------------------------------------------------------------------------------------------------------------------------------------------------------------

        if win_name:
            clickable = True if type_ == "button" else False
            cls.add_images({_memory["coords"]: _memory["surface"]}, win_name, clickable = clickable)
        else:
            return _memory["surface"], _memory["coords"]

    @classmethod
    def text(cls, text: str, scale: int, coords: tuple or list, color: tuple or list, win_name: str, font: str = "arial") -> None:
        """
        This function allows to write text in the window. 

        Examples of the Parameters;
        ---------------------------
        >>> text = "Hello World"
        >>> scale = 13
        >>> coords = (1, 2) #x and y coordinates
        >>> color = (255, 255, 255) #Red, Green, Blue values
        >>> win_name = "scuzz"
        >>> font = "times new roman"
        """

        try: 
            cls.memory[win_name]
        except KeyError:
            raise KeyError("{name} not found. You must set {name} first.".format(name = win_name))

        if cls.memory[win_name]["text"]["name"] != text:
            compeleted_text = {}
            x_coor, y_coor = coords

            if font.endswith("anim"):
                anim = Animation("../game_engine/ui/images/pixelFont_{}/latin_capital_letter_a".format(font.lower()), 3, scale, stop_iteration = True)
                raw_text = [*text]
                for index in range(len(raw_text)):
                    letter = raw_text[index]

                    try:
                        boolean = raw_text[index] != cls.memory[win_name]["text"]["name"][index]
                    except IndexError:
                        boolean = True
                    if letter in [" ", "\n", "\t", "\r"]:
                        boolean = False

                    if boolean:
                        path = "../game_engine/ui/images/pixelFont_{}/{}".format(font.lower(), name(letter).lower().replace(" ", "_"))
                        anim = Animation(path, 3, scale, stop_iteration = True)

                        compeleted_text.update({(x_coor, y_coor): anim})
                        x_coor += anim.image_size[0]
                    else:
                        if letter == "\n" or letter == "\r":
                            x_coor = coords[0]
                            y_coor += (anim.image_size[1] // 2) * scale
                        elif letter == "\t":
                            x_coor += anim.image_size[0] * scale * 2
                        else:
                            x_coor += anim.image_size[0]
            else:
                lines = text.split("\n")
                for line in lines:
                    font_ = pygame.font.SysFont(font, scale)
                    surface = font_.render(line, 1, color)
                    compeleted_text.update({(x_coor, y_coor): surface})
                    y_coor += surface.get_height()

            cls.memory[win_name]["text"]["name"] = text
            cls.memory[win_name]["text"]["images"]["not_clickables"].update(compeleted_text)