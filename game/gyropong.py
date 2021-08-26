#!/usr/bin/env python3

import argparse
import pyglet
import sprites.paddle
import sprites.ball
import sprites.score
import tools.game_manager
import tools.camera
from tools import gamestate

parser = argparse.ArgumentParser(description='GyroPong')
parser.add_argument('-c --camera', dest='camera', default=0,
        help='OpenCV camera id')
parser.add_argument('-d --debug', dest='debug',
        default=False, action='store_true',
        help='Display camera debug window')
parser.add_argument('-f --fullscreen', dest='fullscreen',
        default=False, action='store_true',
        help='Display at fullscreen')
parser.add_argument('-s --screen', dest='screen',
        default=0, type=int,
        help='Screen id')
parser.add_argument('-a --anchors', dest='anchors',
        default=None, type=str,
        help='Anchor coordinates in camera image')
gamestate['args'] = parser.parse_args()

pyglet.resource.path = ['./resources']
pyglet.resource.reindex()

screen = None
if gamestate['args'].screen:
    screens = pyglet.canvas.get_display().get_screens()
    if gamestate['args'].screen < len(screens):
        screen = screens[gamestate['args'].screen]

window = pyglet.window.Window(1024, 1024, screen=screen, resizable=True)
window.set_caption('GyroPong')
if gamestate['args'].fullscreen:
    window.set_fullscreen(True)
gamestate['window'] = window

imgBg = pyglet.resource.image("bg.jpg")
imgBg.anchor_x = imgBg.width // 2
imgBg.anchor_y = imgBg.height // 2
sBg = pyglet.sprite.Sprite(img=imgBg, x=window.width//2, y=window.height//2)
gamestate['sprites']['bg'] = sBg

imgBoardTags = pyglet.resource.image("board_tags.png")
imgBoardTags.anchor_x = imgBoardTags.width // 2
imgBoardTags.anchor_y = imgBoardTags.height // 2
sBoardTags = pyglet.sprite.Sprite(img=imgBoardTags, x=window.width//2, y=window.height//2)
gamestate['sprites']['board_tags'] = sBoardTags

imgHaum = pyglet.resource.image("haum.png")
imgHaum.anchor_x = imgHaum.width // 2
imgHaum.anchor_y = imgHaum.height // 2
sHaum = pyglet.sprite.Sprite(img=imgHaum, x=window.width//2, y=window.height//2, subpixel=True)
gamestate['sprites']['haum'] = sHaum

imgPaddle = pyglet.resource.image("paddle.png")
imgPaddle.anchor_x = 0
imgPaddle.anchor_y = imgPaddle.height //2
sPaddle1 = sprites.paddle.Paddle(img=imgPaddle, subpixel=True)
sPaddle1.color = (0, 255, 255)
gamestate['sprites']['paddle1'] = sPaddle1
sPaddle2 = sprites.paddle.Paddle(img=imgPaddle, subpixel=True)
sPaddle2.color = (255, 255, 0)
gamestate['sprites']['paddle2'] = sPaddle2

imgBall = pyglet.resource.image("ball.png")
imgBall.anchor_x = imgBall.width //2
imgBall.anchor_y = imgBall.height //2
sBall = sprites.ball.Ball(img=imgBall, subpixel=True)
gamestate['sprites']['ball'] = sBall

sScore = sprites.score.Score(imgBall, window.width//2, window.height//2)
gamestate['sprites']['score'] = sScore

if not gamestate['args'].debug: # Sound strangely interfere with the debug window, so do not load it when enabled
    gamestate['sounds']['ping'] = pyglet.resource.media('ping.ogg', streaming=False)
    gamestate['sounds']['end'] = pyglet.resource.media('end.ogg', streaming=False)

gm = tools.game_manager.GameManager()
gamestate['game'] = gm
pyglet.clock.schedule_interval(lambda dt: gm.animate(dt), 1/60.0)

cam = tools.camera.ARUcoCam()
cam.start()
gamestate['cam'] = cam

@window.event
def on_draw():
    gm.draw()

@window.event
def on_resize(width, height):
    scale = min(width, height)/min(imgBg.width, imgBg.height)
    sBg.update(x=width//2, y=height//2, scale=scale)
    sBoardTags.update(x=width//2, y=height//2, scale=scale)
    sHaum.update(x=width//2, y=height//2, scale=scale)
    sScore.reset_position(width//2, height//2, scale)
    sPaddle1.scale = scale
    sPaddle2.scale = scale
    sBall.scale = scale

@window.event
def on_key_press(symbol, modifiers):
    if symbol == ord('f'):
        window.set_fullscreen(not window.fullscreen)

if __name__ == '__main__':
    pyglet.app.run()
    cam.stop()
    cam.join()
