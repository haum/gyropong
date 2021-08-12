import pyglet
from random import choice
from math import cos, sin, pi

class Score(pyglet.graphics.Batch):
    def __init__(self, imgBall, x0, y0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        nb = 7
        self.dots = list(pyglet.sprite.Sprite(img=imgBall, subpixel=True, batch=self) for i in range(nb))
        self.reset()
        self.reset_position(x0, y0, 1)

    def reset(self):
        self.free = list(range(len(self.dots)))
        for d in self.dots:
            d.color = (0, 0, 0)

    def reset_position(self, x0, y0, scale):
        nb = len(self.dots)
        for i, d in enumerate(self.dots):
            d.update(
                x = x0 + 20 * scale * cos(i*pi*2/nb),
                y = y0 + 20 * scale * sin(i*pi*2/nb),
                scale = 0.25 * scale
            )

    def add_point(self, color):
        if not self.is_full():
            p = choice(self.free)
            self.dots[p].color = color
            self.free.remove(p)

    def is_full(self):
        return len(self.free) == 0
