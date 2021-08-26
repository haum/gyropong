import pyglet
from .screen import Screen
import tools.animators
from tools import gamestate
from random import random
from math import pi

class Match(Screen):
    def __init__(self):
        self.timer_quit = tools.animators.LinearAnimator(duration=10)
        self.ballspeed = tools.animators.LinearAnimator(duration=30, run=True)

    def enter(self):
        self.timer_quit.start()
        self.playing = False
        gamestate['sprites']['score'].reset()

    def calcspeed(self):
        return 100 + 300 * self.ballspeed.value()

    def animate(self, dt):
        ball = gamestate['sprites']['ball']
        ball.animate(dt)
        self.timer_quit.update(dt)
        self.ballspeed.update(dt)
        threeplayers = gamestate['3players']

        # Drive paddles
        p1 = gamestate['sprites']['paddle1']
        p2 = gamestate['sprites']['paddle2']
        p3 = gamestate['sprites']['paddle3']
        p1.drive(gamestate['angles'][0], dt)
        p2.drive(gamestate['angles'][1], dt)
        p3.drive(gamestate['angles'][2], dt)

        # Display presence
        p1here = gamestate['angles'][0] != None
        p2here = gamestate['angles'][1] != None
        p3here = gamestate['angles'][2] != None
        p1.opacity = 255 if p1here else 64
        p2.opacity = 255 if p2here else 64
        p3.opacity = 255 if p3here else 64

        # Quit game
        if p1here or p2here or (p3here and threeplayers):
            self.timer_quit.stop()
            self.timer_quit.reset()
        if not p1here and not p2here and (not p3here or not threeplayers):
            self.timer_quit.resume()
        if self.timer_quit.value() == 1:
           gamestate['game'].change_screen('wait')

        # Start ball
        if not self.playing and p1here and p2here and (p3here or not threeplayers):
            if gamestate['sprites']['score'].is_full():
                ball.reset()
                ball.color = (255, 255, 255)
                ball.set_speed(0, 0)
            else:
                self.playing = True
                self.ballspeed.reset()
                self.ballspeed.start()
                ball.reset()
                ball.color = (255, 255, 255)
                a = random() * 2 * pi
                ball.set_speed(a, self.calcspeed())

        # Ball out
        sw, sh = gamestate['window'].width, gamestate['window'].height
        ss = min(sw, sh) * 0.48
        if (ball.position[0] - sw/2)**2 + (ball.position[1] - sh/2)**2 > ss * ss:
            self.playing = False
            if not(ball.color[0] == 255 and ball.color[1] == 255 and ball.color[2] == 255):
                if 'end' in gamestate['sounds']:
                    gamestate['sounds']['end'].play()
                gamestate['sprites']['score'].add_point(ball.color)

        # Check pad touch
        if self.playing:
            p1ball = p1.check_ball()
            p2ball = p2.check_ball()
            p3ball = p3.check_ball() if threeplayers else None
            p = None
            if p1ball != None and p2ball != None and (p3ball != None or not threeplayers):
                if threeplayers:
                    r = random()
                    if r < 0.33333: p = p1
                    elif r > 0.66666: p = p2
                    else: p = p3
                else:
                    if random() < 0.5:
                        p = p1
                    else:
                        p = p2
            elif p1ball != None:
                p = p1
            elif p2ball != None:
                p = p2
            elif p3ball != None:
                p = p3

            if p:
                if 'ping' in gamestate['sounds']:
                    gamestate['sounds']['ping'].play()
                ball.set_speed(p.check_ball(), self.calcspeed())
                ball.color = p.color

    def draw(self):
        super().draw(['bg', 'score', 'paddle1', 'paddle2', 'ball'])
        if gamestate['3players']: super().draw(['paddle3'])
