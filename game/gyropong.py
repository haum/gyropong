#!/usr/bin/env python3

import pyglet
import sprites.paddle
import tools.game_manager
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
gamestate['sprites']['bg'] = sBg

imgPaddle = pyglet.resource.image("paddle.png")
imgPaddle.anchor_x = imgPaddle.width //2
imgPaddle.anchor_y = imgPaddle.height //2
sPaddle1 = sprites.paddle.Paddle(img=imgPaddle)
sPaddle1.color = (0, 255, 255)
gamestate['sprites']['paddle1'] = sPaddle1
sPaddle2 = sprites.paddle.Paddle(img=imgPaddle)
sPaddle2.color = (255, 255, 0)
gamestate['sprites']['paddle2'] = sPaddle2

gm = tools.game_manager.GameManager()
pyglet.clock.schedule_interval(lambda dt: gm.animate(dt), 1/60.0)

@window.event
def on_draw():
    gm.draw()

if __name__ == '__main__':
    pyglet.app.run()
