from tools import gamestate

class Screen:
    def draw(self, names):
        for n in names:
            gamestate['sprites'][n].draw()

    def enter(self):
        pass

    def exit(self):
        pass
