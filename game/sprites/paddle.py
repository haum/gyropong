import pyglet
from tools import gamestate
from math import cos, sin, atan2, pi

class Paddle(pyglet.sprite.Sprite):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.angle = 0

    def set_angle(self, angle):
        sw, sh = gamestate['window'].width, gamestate['window'].height
        ss = min(sw, sh) * 0.45
        self.update(
            x = sw/2+ss*cos(angle),
            y = sh/2+ss*sin(angle),
            rotation = 180-angle*180/pi
        )
        self.angle = angle

    def drive(self, angle, dt):
        if not angle: return
        da = angle - self.angle
        da = (da + pi) % (2 * pi) - pi
        al = 0.1
        if da > al: angle = self.angle + al
        elif da < -al: angle = self.angle - al
        self.set_angle(angle % (2 * pi))

    def check_ball(self):
        ball = gamestate['sprites']['ball']
        sw, sh = gamestate['window'].width, gamestate['window'].height
        bx, by = ball.position
        ss = min(sw, sh) * 0.45
        xcp, ycp = sw/2+(ss+412*self.scale)*cos(self.angle), sh/2+(ss+412*self.scale)*sin(self.angle)
        if (bx-xcp)**2 + (by-ycp)**2 < (450*self.scale)**2:
            n = atan2(by-ycp, bx-xcp)
            na = (n - self.angle) % (2 * pi)
            if na < pi + 0.254 and na > pi - 0.254:
                na = n + pi - ball.angle
                if na < pi/2 and na > -pi/2:
                    return (n + na) % (2 * pi)
                else:
                    return n
        return None
