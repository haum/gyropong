import pyglet
from tools import gamestate
from math import cos, sin

class Ball(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.xr = 0
        self.yr = 0
        self.angle = 0
        self.speed = 0

    def reset(self):
        self.xr = self.yr = 0

    def set_speed(self, angle, speed):
        self.angle = angle
        self.speed = speed

    def animate(self, dt):
        self.xr += dt * self.speed * cos(self.angle)
        self.yr += dt * self.speed * sin(self.angle)
        sw, sh = gamestate['window'].width, gamestate['window'].height
        self.update(sw/2 + self.xr, sh/2 + self.yr)
