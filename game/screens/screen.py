from tools import gamestate

class Screen:
    def draw(self, names):
        for n in names:
            gamestate['sprites'][n].draw()
