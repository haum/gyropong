GyroPong
========

Game created for the 2021 teriaki festival based on a webcam and a video
projector.

Opponents control paddles that follow a circular path and should keep a ball
inside a circle. If the ball leaves, the last player who touched the ball wins.

Dependancies
------------

The game is powered by python and its dependancies are listed in
`game/requirements.txt`.

Options
-------

The game has some options that can be listed with `game/gyropong.py --help`.

Paddles tags
------------

The game detects the position of the board and of the paddles with tags in the
real world. The tags for the board are projected, but the tags for the paddles
need to be printed or drawn on a support.

The models of these tags are available in `src_resources/paddle[12].svg`

Launch the game
---------------

Preparation
```````````

Use the debug window (see options) to ensure that the board and paddles are
detected, and that the center of the circle is at the right place in the image.

Start a match
`````````````

In the waiting screen, show the paddles of all the players. After a short time
with detected tags, the game will start.

Play
````

If the ball is not of your color, try to touch it by moving your paddle. If the
ball leaves the arena with your color, you score a point.

If multiple paddles touch the ball, a random color is chosen.

The paddles are curved, you can use this curvature to orient the direction of
the ball.
