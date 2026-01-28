from collections import namedtuple
from typing import overload

import pygame
import repackage
from core.animation import Animation

repackage.up()

pygame.init()


class Physic:
    """
    Physic
    ======

    This class performs calculations based on simple physics laws.

    Basic Usage of the Class:
    -------------------------
    >>> Physic.throwing(...) #You must set the variables.
    >>> Physic.pixel_perfect_collision(...) #You must set the variables.
    >>> Physic.rect_collision(...) #You must set the variables.

    The Class Variable;
    -------------------
    >>> physic_var.gen_obj #You can only use if the variable was set.

    Function(s);/
    `pixel_perfect_collision`
    `rect_collision`
    `throwing`
    """

    Result = namedtuple("Result", "item_collision_coords item_coords item_index item_size side overlap_rect")

    @classmethod
    def pixel_perfect_collision(
        cls, coords: tuple, image: pygame.image, collision_items: dict, col_ret_in_list: bool = False, *args, **kwds
    ) -> namedtuple:
        """
        It makes collision test between the image and the collision items, you can set return result visa versa.

        Examples of the Parameters;
        ---------------------------
        >>> coords = (1, 2) #x and y coordinates
        >>> image = pygame.image.load("C:/Users/Osman/foo/bar.png").convert_alpha()
        >>> collision_items = {(3, 4): pygame_image_1, (5, 6): pygame_image_2}
        """

        x_coor, y_coor = coords
        if image:
            img_mask = pygame.mask.from_surface(image)

        if not isinstance(collision_items, dict):
            raise TypeError(f"collision_items parameter type must be a dict, not {type(collision_items)}")

        for item_coords in collision_items.keys():
            item = collision_items[item_coords]["image"] if "key" in kwds.keys() else collision_items[item_coords]

            mask = (
                pygame.mask.from_surface(item.frame_image)
                if isinstance(item, Animation)
                else pygame.mask.from_surface(item)
            )

            if col_ret_in_list:
                offset = (int(x_coor - item_coords[0]), int(y_coor - item_coords[1]))
                result = mask.overlap(img_mask, offset)
            else:
                offset = (int(item_coords[0] - x_coor), int(item_coords[1] - y_coor))
                result = img_mask.overlap(mask, offset)

            if result:
                self_rect = pygame.Rect(x_coor, y_coor, image.get_width(), image.get_height())
                item_rect = pygame.Rect(item_coords, item.get_size())

                overlap = self_rect.clip(item_rect)

                side = None
                if overlap.width < overlap.height:
                    if self_rect.centerx < item_rect.centerx:
                        side = "left"
                    else:
                        side = "right"
                else:
                    if self_rect.centery < item_rect.centery:
                        side = "top"
                    else:
                        side = "bottom"

                return cls.Result(
                    result, item_coords, list(collision_items.keys()).index(item_coords), item.get_size(), side, overlap
                )

    @classmethod
    def rect_collision(cls, coords: tuple, size: tuple, collision_items: dict, *args, **kwds) -> namedtuple:
        """
        It makes collision test between the image and the collision items, you can set return result visa versa.

        Examples of the Parameters;
        ---------------------------
        >>> coords = (1, 2) #x and y coordinates
        >>> size = (1, 1) #height and width
        >>> collision_items = {(3, 4): pygame_image_1, (5, 6): pygame_image_2}
        """

        if type(collision_items) is not dict:
            raise TypeError(f"collision_items parameter type must be dict, not {type(collision_items)}")

        x_coor, y_coor = coords

        self_rect = pygame.Rect(x_coor, y_coor, size[0], size[1])

        for idx, item_coords in enumerate(collision_items.keys()):
            item = collision_items[item_coords]["image"] if "key" in kwds else collision_items[item_coords]

            try:
                item_size = item.get_size()
            except AttributeError:
                item_size = (int(item[0]), int(item[1]))

            item_rect = pygame.Rect(item_coords[0], item_coords[1], item_size[0], item_size[1])

            if self_rect.colliderect(item_rect):
                overlap = self_rect.clip(item_rect)

                # collision'un item içindeki lokal koordinatı
                local_coords = (overlap.x - item_rect.x, overlap.y - item_rect.y)

                return cls.Result(
                    local_coords,  # item_collision_coords
                    item_coords,  # item_coords
                    idx,  # item_index
                    item_size,  # item_size
                    "",  # side
                    overlap,  # overlap_rect
                )

        return None

    @overload
    def throwing(self, speed: int or float, velocity: int or float) -> tuple:
        """
        When this function had been set, it will calculate the condition and return the coords steps using generator.

        Examples of the Parameters;
        ---------------------------
        >>> speed = 30
        >>> velocity = 32
        """

    @overload
    def throwing(self, speed: int or float, velocity: int or float, coords: tuple or list = None) -> tuple: ...

    @classmethod
    def throwing(cls, speed: int or float, velocity: int or float, coords: tuple or list = None) -> tuple:
        def velocity_calculator(average):
            _average = average
            _average_countdown = _average
            move_value = 17

            foo = _average
            bar = ""
            while True:
                gravity_ratio = yield move_value

                if not _average_countdown:
                    _average //= gravity_ratio
                    foo //= gravity_ratio * 2
                    if not foo:
                        raise StopIteration("Velocity is over. ")

                    _average_countdown = _average
                    bar = _average // foo * "0"
                    bar = bar[:-1] + "1"
                    bar *= foo
                else:
                    _average_countdown -= 1

                    try:
                        bar[-1]
                    except IndexError:
                        pass
                    else:
                        move_value = 17 if int(bar[-1]) else 10

                        bar = bar[:-1]

        if not hasattr(cls, "gen_obj"):
            cls.gen_obj = velocity_calculator(velocity)
            next(cls.gen_obj)

        try:
            x_result, y_result = (speed, cls.gen_obj.send(2))
        except RuntimeError:
            del cls.gen_obj
            return None
        else:
            return (x_result, y_result) if not coords else (coords[0] + x_result, coords[1] - y_result)
