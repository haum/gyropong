import screens
from tools import gamestate

class GameManager:
    def __init__(self):
        self.screens = {
            'wait': screens.WaitPlayersScreen(),
            'match': screens.Match(),
        }
        self.screen = self.screens['wait']
        self.screen.enter()

    def animate(self, dt):
        gamestate['angles'] = gamestate['cam'].get_angles()
        self.screen.animate(dt)

    def draw(self):
        gamestate['window'].clear()
        self.screen.draw()

    def change_screen(self, name):
        if name in self.screens:
            self.screen.exit()
            self.screen = self.screens[name]
            self.screen.enter()
