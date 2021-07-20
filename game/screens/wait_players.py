from .screen import Screen
from math import pi
import tools.animators
from tools import gamestate

class WaitPlayersScreen(Screen):
    def __init__(self):
        self.a = tools.animators.LinearAnimator(duration=10, looped=True, run=True)
        self.timer_presence = tools.animators.LinearAnimator(duration=3)

    def enter(self):
        self.a.reset()
        self.timer_presence.reset()

    def animate(self, dt):
        self.a.update(dt)
        self.timer_presence.update(dt)

        p1 = gamestate['sprites']['paddle1']
        p2 = gamestate['sprites']['paddle2']
        p1.set_angle(2 * pi * self.a.value())
        p2.set_angle(2 * pi * self.a.value() + pi)
        p1here = gamestate['angles'][0] != None
        p2here = gamestate['angles'][1] != None
        p1.opacity = 255 if p1here else 64
        p2.opacity = 255 if p2here else 64

        if not p1here or not p2here:
            self.timer_presence.stop()
            self.timer_presence.reset()
        if p1here and p2here:
            self.timer_presence.resume()
        if self.timer_presence.value() == 1:
           gamestate['game'].change_screen('match')

    def draw(self):
        super().draw(['bg', 'paddle1', 'paddle2'])

