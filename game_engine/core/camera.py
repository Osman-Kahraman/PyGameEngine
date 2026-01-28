import random
import time

import numpy as np
import pygame

pygame.init()


class Camera:
    """
    Camera
    ======

    About the game camera system.

    Basic Usage of the Class:
    -------------------------
    >>> Camera.focus(...) #You must set the variables.
    >>> Camera.shake(...) #You must set the variables.

    You can take the parameter;/
    `Camera.surface_size`

    The Class Variable;
    -------------------
    >>> Camera.coords #It gives the camera's coords.

    Shortways of the Class:
    -----------------------
    >>> Camera.coords[0] += 1 #You can move the camera manually like that.
    >>> Camera.coords = np.array(Camera.coords) + (-1, 2) #It's another way the usage. Also you need to
    import numpy module as "np" variable.

    Function(s);/
    `focus`
    `shake`
    """

    surface_size = (683, 384)
    coords = [0, 0]

    @classmethod
    def focus(cls, item_coords: list or tuple) -> list:
        """
        Camera will focus to the item's coords and returns also the camera coords.

        Examples of the Parameters;
        ---------------------------
        >>> item_coords = (1, 2) #x and y coordinates
        """

        cls.coords = list(np.array(item_coords) - (np.array(cls.surface_size) // 2))

        return cls.coords

    @classmethod
    def shake(cls, velocity: int or float, timer: int or float = 0) -> None:
        """
        It will shake the camera by velocity amount. And also you can set time of the shake.

        Examples of the Parameters;
        ---------------------------
        >>> velocity = 30
        >>> timer = 32
        """

        if not hasattr(cls, "shaking_timer"):
            cls.shaking_timer = time.time()

        random_velocity = random.randrange(-velocity, velocity) if time.time() - cls.shaking_timer <= timer else 0

        cls.coords = np.array(cls.coords) + random_velocity
