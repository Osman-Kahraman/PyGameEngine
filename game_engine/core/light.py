import pygame, repackage, math
from pygame import gfxdraw

from ui.images.init import *
repackage.up()
from event import *

pygame.init()

class Light:
    """
Light
=====

Creates a light source. 

Basic Usage of the Class:
-------------------------
>>> light_system = Light(...) #You must set the light size.
>>> light_system.render(...) #You must set the coordinates and images.

The Class Variable;
-------------------
>>> light_system.width #Width of the surface size. 
>>> light_system.height #Height of the surface size. 
>>> light_system.light_image #The default light image but you can change with monkey-patching. 

Function(s);/
`segments_from_image`
`screen_border_segments`
`intersect`
`visibility_polygon`
`render`
    """
    def __init__(self, size) -> None:
        self.width, self.height = size
        self.darkness = pygame.Surface(size, pygame.SRCALPHA)
        try:
            image = pygame.image.load("../game_engine/ui/images/light.png").convert_alpha()
        except:
            image = pygame.image.load("game_engine/images/light.png").convert_alpha()
        self.light_image = pygame.transform.scale(image, size)

    def segments_from_image(self, image: pygame.image, pos: tuple) -> list:
        """
        Turns segments from the given image for shadow effect. 

        Examples of the Parameters;
        ---------------------------
        >>> image = pygame.image.load("C:/Users/Osman/foo/bar.png").convert_alpha()
        >>> pos = (3, 4)
        """

        mask = pygame.mask.from_surface(image)
        outline = mask.outline()[::10]

        segs = []
        for i in range(len(outline)):
            x1, y1 = outline[i]
            x2, y2 = outline[(i + 1) % len(outline)]
            segs.append({
                "a": {"x": x1 + pos[0], "y": y1 + pos[1]},
                "b": {"x": x2 + pos[0], "y": y2 + pos[1]}
            })
        return segs

    def screen_border_segments(self) -> list:
        """
        Defines borders of the light. 
        """

        w, h = self.width, self.height
        return [
            {"a": {"x": 0, "y": 0}, "b": {"x": w, "y": 0}},
            {"a": {"x": w, "y": 0}, "b": {"x": w, "y": h}},
            {"a": {"x": w, "y": h}, "b": {"x": 0, "y": h}},
            {"a": {"x": 0, "y": h}, "b": {"x": 0, "y": 0}},
        ]

    def intersect(self, ray: dict, segment: dict) -> tuple:
        """
        Calculates the intersection point between a ray and a line segment.

        This function is used in the shadow / visibility system to determine
        where a light ray first hits an obstacle edge (segment). If there is
        a valid intersection in front of the ray origin and within the segment
        bounds, the closest hit point is returned.

        Parameters;
        -----------
        ray : dict
            Ray definition with two points:
            {
                "a": (x, y),   # ray origin (light position)
                "b": (x, y)    # ray end point (direction * distance)
            }

        segment : dict
            Line segment definition:
            {
                "a": {"x": x1, "y": y1},  # segment start
                "b": {"x": x2, "y": y2}   # segment end
            }

        Returns;
        --------
        tuple or None
            (hit_x, hit_y, t1)
            - hit_x, hit_y : intersection coordinates
            - t1           : distance factor along the ray
            Returns None if there is no valid intersection.

        Examples;
        ---------
        >>> ray = {"a": (100, 100), "b": (300, 100)}
        >>> segment = {
        ...     "a": {"x": 200, "y": 50},
        ...     "b": {"x": 200, "y": 150}
        ... }
        >>> intersect(ray, segment)
        (200.0, 100.0, 0.5)
        """

        r_px, r_py = ray["a"]
        r_dx = ray["b"][0] - r_px
        r_dy = ray["b"][1] - r_py

        s_px = segment["a"]["x"]
        s_py = segment["a"]["y"]
        s_dx = segment["b"]["x"] - s_px
        s_dy = segment["b"]["y"] - s_py

        cross = r_dx * s_dy - r_dy * s_dx
        if abs(cross) < 1e-8:
            return None

        try:
            T2 = (r_dx * (s_py - r_py) + r_dy * (r_px - s_px)) / (s_dx * r_dy - s_dy * r_dx)
            T1 = (s_px + s_dx * T2 - r_px) / r_dx
        except ZeroDivisionError:
            return None

        if T1 < 0 or not (0 <= T2 <= 1):
            return None

        return (r_px + r_dx * T1, r_py + r_dy * T1, T1)

    def visibility_polygon(self, light_pos: tuple, segments: list) -> list:
        """
        Calculates the visibility polygon from a light source position
        using the given line segments for shadow casting.

        The function casts rays towards segment endpoints with small
        angle offsets and finds the closest intersections to build
        the visible area.

        Examples of the Parameters;
        ---------------------------
        >>> light_pos = (400, 300)
        >>> segments = [
        ...     {"a": {"x": 100, "y": 100}, "b": {"x": 300, "y": 100}},
        ...     {"a": {"x": 300, "y": 100}, "b": {"x": 300, "y": 300}},
        ... ]
        """

        lx, ly = light_pos
        angles = []

        for seg in segments:
            for p in (seg["a"], seg["b"]):
                a = math.atan2(p["y"] - ly, p["x"] - lx)
                angles.extend([a - 0.00001, a + 0.00001])

        points = []

        for a in angles:
            dx = math.cos(a)
            dy = math.sin(a)

            ray = {
                "a": (lx, ly),
                "b": (lx + dx * 2000, ly + dy * 2000)
            }

            closest = None
            for seg in segments:
                hit = self.intersect(ray, seg)
                if hit and (closest is None or hit[2] < closest[2]):
                    closest = hit

            if closest:
                points.append((a, (closest[0], closest[1])))

        points.sort(key=lambda x: x[0])
        return [p for _, p in points]

    def render(self, light_pos: tuple, items: list) -> pygame.Surface:
        """
        Renders the light and shadow effect using the given image as
        an occluder and returns the final light surface.

        The function calculates shadow-casting segments from the image,
        builds a visibility polygon, and applies it as a mask over
        the light texture.

        Examples of the Parameters;
        ---------------------------
        >>> light_pos = (400, 300)
        >>> items = [[(3, 4), pygame_image_1], [(5, 6), pygame_image_2]]
        """

        segments = self.screen_border_segments()

        for image_pos, image in items:
            i_x, i_y = image_pos
            l_x, l_y = light_pos
            i_s_x, i_s_y = image.get_size()

            is_inside = i_x + i_s_x > l_x and i_y + i_s_y > l_y and i_x < l_x + self.width and i_y < l_y + self.height

            if is_inside: #optimizing: only works if image is inside the light
                clarify = (i_x - l_x, i_y - l_y)

                segments += self.segments_from_image(image, clarify)

        if len(segments) > 4: #if there is more segments except border
            poly = self.visibility_polygon((self.width // 2, self.height // 2), segments) #Inserting the source in the middle coords
            
            mask_surf = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            mask_surf.fill((0, 0, 0, 0))
            
            if len(poly) >= 3:
                gfxdraw.filled_polygon(
                    mask_surf,
                    poly,
                    (255, 255, 255, 255)
                )

                small = pygame.transform.smoothscale(
                    mask_surf,
                    (self.width // 2, self.height // 2)
                )
                mask_surf = pygame.transform.smoothscale(
                    small,
                    (self.width, self.height)
                )

            light_cut = self.light_image.copy()
            light_cut.blit(mask_surf, (0, 0), special_flags = pygame.BLEND_RGBA_MULT)

            self.darkness.fill((0, 0, 0, 0))
            self.darkness.blit(light_cut, (0, 0))

        return self.darkness