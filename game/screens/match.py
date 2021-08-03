import pyglet
from .screen import Screen
import tools.animators
from tools import gamestate

class Match(Screen):
    def __init__(self):
        self.timer_quit = tools.animators.LinearAnimator(duration=10)

    def enter(self):
        self.timer_quit.start()

    def animate(self, dt):
        self.timer_quit.update(dt)

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

    def draw(self):
        super().draw(['bg', 'paddle1', 'paddle2'])
