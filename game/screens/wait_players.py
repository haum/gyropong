from .screen import Screen
from math import pi
import tools.animators
from tools import gamestate

class WaitPlayersScreen(Screen):
    def __init__(self):
        self.a = tools.animators.LinearAnimator(duration=10, looped=True, run=True)

    def animate(self, dt):
        self.a.update(dt)
        gamestate['sprites']['paddle1'].set_angle(2 * pi * self.a.value())
        gamestate['sprites']['paddle2'].set_angle(2 * pi * self.a.value() + pi)

    def draw(self):
        super().draw(['bg', 'paddle1', 'paddle2'])

