import screens
from tools import gamestate

class GameManager:
    def __init__(self):
        self.screens = {
            'wait': screens.WaitPlayersScreen(),
        }
        self.screen = self.screens['wait']

    def animate(self, dt):
        self.screen.animate(dt)

    def draw(self):
        gamestate['window'].clear()
        self.screen.draw()
