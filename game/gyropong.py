#!/usr/bin/env python3

from math import cos, sin, pi
import pyglet
import sprites.paddle
import tools.animators
from tools import gamestate

pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

window = pyglet.window.Window(1024, 1024)
window.set_caption('GyroPong')
gamestate['window'] = window

imgBg = pyglet.resource.image("bg.jpg")
imgBg.anchor_x = imgBg.width // 2
imgBg.anchor_y = imgBg.height // 2
sBg = pyglet.sprite.Sprite(img=imgBg, x=window.width//2, y=window.height//2)

imgPaddle = pyglet.resource.image("paddle.png")
imgPaddle.anchor_x = imgPaddle.width //2
imgPaddle.anchor_y = imgPaddle.height //2
sPaddle1 = sprites.paddle.Paddle(img=imgPaddle)
sPaddle1.color = (0, 255, 255)
sPaddle2 = sprites.paddle.Paddle(img=imgPaddle)
sPaddle2.color = (255, 255, 0)

a = tools.animators.LinearAnimator(duration=10, looped=True, run=True)
def update(dt):
    a.update(dt)
    sPaddle1.set_angle(a.value() * 2 * pi)
    sPaddle2.set_angle(pi + a.value() * 2 * pi)
pyglet.clock.schedule_interval(update, 1/60.0)

@window.event
def on_draw():
    window.clear()
    sBg.draw()
    sPaddle1.draw()
    sPaddle2.draw()

if __name__ == '__main__':
    pyglet.app.run()
