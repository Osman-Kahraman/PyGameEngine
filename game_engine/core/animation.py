import pygame, os, numpy as np, repackage

from ui.images.init import *
repackage.up()
from event import *

pygame.init()

class Animation:
    """
Animation
=========

Provides an iterable animation tuple object with the parameters by simple usage. 


Basic Usage of the Class:
-------------------------

>>> PATH = "C:/Users/Osman/Desktop/AnimationFolder"
>>> framerate = 3
>>> foo = Animation(PATH, framerate)
>>> next(foo) #Returns an pygame.Image object.

You can take the parameters;/
`foo.PATH`
`foo.framerate`
`foo.scale`
`foo.stop_iteration`

The Class Variables:
--------------------
>>> foo.frames #It gives all animation frames.
>>> foo.frame_image #It gives the current image. 
>>> foo.frame_PATH #It gives the current image PATH. 
>>> foo.image_size #It gives the current image's size. 

Shortways of the Class:
-----------------------
>>> len(foo)
2
>>> foo[0] 
(<Surface(726x30x32 SW)>, "C:/Users/Osman/Desktop/AnimationFolder/AnimationFolder1.png")
>>> (<Surface(726x30x32 SW)>, "C:/Users/Osman/Desktop/AnimationFolder/AnimationFolder1.png") in foo
True
    """

    __slots__ = ["PATH", "framerate", "scale", "stop_iteration", "frames", "iter", "frame_image", "frame_PATH"]

    def __init__(self, PATH: str, framerate: int, scale: int = 1, stop_iteration: bool = False) -> iter:
        self.PATH = str(PATH)
        self.framerate = int(framerate)
        self.scale = int(scale)
        self.stop_iteration = bool(stop_iteration)

        self.frames = ()
        frames = list(os.listdir(PATH))
        frames.sort(key = str)
        for frame in frames:
            try:
                img = pygame.image.load(PATH + "/" + frame).convert_alpha()
                scaled_img = pygame.transform.scale(img, tuple(np.array(img.get_rect().size) * scale))

                self.frames += ((scaled_img, PATH + "/" + frame), ) * framerate
            except:
                break

        self.iter = iter(self.frames)
        self.frame_image = self.frames[0][0]
        self.frame_PATH = self.frames[0][1]

    @property
    def image_size(self):
        return self.frame_image.get_size()

    def __len__(self) -> len:
        return len(self.frames)

    def __getitem__(self, position):
        return self.frames[position]

    def __contains__(self, item):
        return True if item in self.frames else False

    def __next__(self):
        try:
            frame = next(self.iter)
        except StopIteration: 
            if self.stop_iteration:
                frame = self.frames[-1]
            else:
                self.iter = iter(self.frames)
                frame = next(self.iter)

        self.frame_image, self.frame_PATH = frame

        return self.frame_image