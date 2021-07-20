import pyglet
from .screen import Screen
import tools.animators
from tools import gamestate

class Match(Screen):
    def __init__(self):
        self.timer = tools.animators.LinearAnimator(duration=5)
        self.label = pyglet.text.Label('Game will take place here',
                          #font_name='Times New Roman',
                          font_size=36,
                          x=gamestate['window'].width//2, y=gamestate['window'].height//2,
                          anchor_x='center', anchor_y='center')

    def enter(self):
        self.timer.start()

    def animate(self, dt):
        self.timer.update(dt)

        if self.timer.value() == 1:
           gamestate['game'].change_screen('wait')

    def draw(self):
        super().draw(['bg'])
        self.label.draw()
