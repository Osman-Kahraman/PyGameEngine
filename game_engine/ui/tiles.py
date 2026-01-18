import json, pygame

def read(return_dict = "worked"):
        tile_dict_RAW = {}
        tile_dict = {}
        
        with open("game_engine/ui/tiles.json", "r") as file:
            datas = json.loads(file.read())

            for key in datas.keys():
                tile_dict_RAW.update({key: {"layers": {}, "visibility": datas[key]["visibility"], "parallax": datas[key]["parallax"], "hitbox": datas[key]["hitbox"]}})
                tile_dict.update({int(key): {"layers": {}, "visibility": datas[key]["visibility"], "parallax": datas[key]["parallax"], "hitbox": datas[key]["hitbox"]}})

                for data in datas[key]["layers"].keys():
                    coords = data[1:-1].split(", ")
                    directory = datas[key]["layers"][data].split("/")

                    if len(directory) >= 2:
                        data_image = directory[-1]
                    else:
                        data_image = "image"
                    with open("game_engine/items/info.json", "r") as file:
                        try:
                            coords = json.loads(file.read())[directory[0].rstrip(".png")]["coords"]
                        except KeyError:
                            pass

                    tile_dict_RAW[key]["layers"].update({"({}, {})".format(coords[0], coords[1]): datas[key]["layers"][data]})
                    tile_dict[int(key)]["layers"].update({(int(coords[0]), int(coords[1])): pygame.image.load("images/built_in_images/" + datas[key]["layers"][data]).convert_alpha()})

        abe = tile_dict_RAW if return_dict.lower() == "raw" else tile_dict
        if return_dict.lower() == "both":
            abe = (tile_dict_RAW, tile_dict)
        
        return abe