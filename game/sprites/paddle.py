import pyglet
from tools import gamestate
from math import cos, sin, pi

class Paddle(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def set_angle(self, angle):
        sw, sh = gamestate['window'].width, gamestate['window'].height
        ss = min(sw, sh) * 0.45
        self.update(
            x = sw/2+ss*cos(angle),
            y = sh/2+ss*sin(angle),
            rotation = 180-angle*180/pi
        )

