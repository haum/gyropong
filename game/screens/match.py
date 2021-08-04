import pyglet
from .screen import Screen
import tools.animators
from tools import gamestate
from random import random
from math import pi

class Match(Screen):
    def __init__(self):
        self.timer_quit = tools.animators.LinearAnimator(duration=10)
        self.ballspeed = tools.animators.LinearAnimator(duration=120, run=True)

    def enter(self):
        self.timer_quit.start()
        self.playing = False

    def animate(self, dt):
        ball = gamestate['sprites']['ball']
        ball.animate(dt)
        self.timer_quit.update(dt)
        self.ballspeed.update(dt)

        # Drive paddles
        p1 = gamestate['sprites']['paddle1']
        p2 = gamestate['sprites']['paddle2']
        p1.drive(gamestate['angles'][0], dt)
        p2.drive(gamestate['angles'][1], dt)

        # Display presence
        p1here = gamestate['angles'][0] != None
        p2here = gamestate['angles'][1] != None
        p1.opacity = 255 if p1here else 64
        p2.opacity = 255 if p2here else 64

        # Quit game
        if p1here or p2here:
            self.timer_quit.stop()
            self.timer_quit.reset()
        if not p1here and not p2here:
            self.timer_quit.resume()
        if self.timer_quit.value() == 1:
           gamestate['game'].change_screen('wait')

        # Start ball
        if not self.playing and p1here and p2here:
            self.playing = True
            ball.reset()
            ball.color = (255, 255, 255)
            a = random() * 2 * pi
            ball.set_speed(a, 50+300*self.ballspeed.value())

        # Ball out
        sw, sh = gamestate['window'].width, gamestate['window'].height
        ss = min(sw, sh) * 0.48
        if (ball.position[0] - sw/2)**2 + (ball.position[1] - sh/2)**2 > ss * ss:
            self.playing = False

    def draw(self):
        super().draw(['bg', 'paddle1', 'paddle2', 'ball'])
