#!/usr/bin/env python3

from math import cos, sin, pi
import pyglet

pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

window = pyglet.window.Window(1024, 1024)
window.set_caption('GyroPong')

imgBg = pyglet.resource.image("bg.jpg")
imgBg.anchor_x = imgBg.width // 2
imgBg.anchor_y = imgBg.height // 2
sBg = pyglet.sprite.Sprite(img=imgBg, x=window.width//2, y=window.height//2)

imgPaddle = pyglet.resource.image("paddle.png")
imgPaddle.anchor_x = imgPaddle.width //2
imgPaddle.anchor_y = imgPaddle.height //2
sPaddle1 = pyglet.sprite.Sprite(img=imgPaddle)
sPaddle1.color = (0, 255, 255)
sPaddle2 = pyglet.sprite.Sprite(img=imgPaddle)
sPaddle2.color = (255, 255, 0)

def setPaddle(sPaddle, angle):
    sw, sh = window.width, window.height
    ss = min(sw, sh) * 0.45
    sPaddle.update(x=sw/2+ss*cos(angle), y=sh/2+ss*sin(angle), rotation=180-angle*180/pi)

t = 0
def update(dt):
    global t
    t += dt
    setPaddle(sPaddle1, 0.4*t)
    setPaddle(sPaddle2, pi+0.4*t)
pyglet.clock.schedule_interval(update, 1/60.0)

@window.event
def on_draw():
    window.clear()
    sBg.draw()
    sPaddle1.draw()
    sPaddle2.draw()

if __name__ == '__main__':
    pyglet.app.run()
