import pyglet
from tools import gamestate

class Ball(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.vx = 0
        self.vy = 0

    def reset(self):
        sw, sh = gamestate['window'].width, gamestate['window'].height
        self.update(
            x = sw/2,
            y = sw/2
        )

    def set_speed(self, vx, vy):
        self.vx = vx
        self.vy = vy

    def animate(self, dt):
        self.update(
            self.position[0] + self.vx,
            self.position[1] + self.vy,
        )
