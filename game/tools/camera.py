import cv2
import cv2.aruco as aruco
import numpy as np
import time
import threading
from math import atan2, pi
from tools import gamestate

class ARUcoCam(threading.Thread):
    def __init__(self):
        super().__init__()
        self.lock = threading.Lock()
        self.cam = gamestate['args'].camera
        try:
            self.cam = int(self.cam)
        except:
            pass
        self.debug = gamestate['args'].debug
        self.aruco_dict = aruco.Dictionary_get(aruco.DICT_4X4_50)
        self.forced = [False, False]
        self.angles = [None, None]
        self.running = True

    def run(self):
        retryCap = True
        while retryCap and self.running:
            cap = cv2.VideoCapture(self.cam)
            if cap.isOpened():
                retryCap = False
            else:
                print('Camera not opened')
                time.sleep(2)
        anchors = [None, None, None, None]
        anchor0 = None
        players = [None, None]
        if self.debug:
            def evt(event, x, y, flags, userdata):
                if event == cv2.EVENT_LBUTTONDOWN:
                    if flags & cv2.EVENT_FLAG_SHIFTKEY:
                        userdata[0] = None if flags & cv2.EVENT_FLAG_CTRLKEY else (x, y)
                        self.forced[0] = True
                    else:
                        userdata[1] = None if flags & cv2.EVENT_FLAG_CTRLKEY else (x, y)
                        self.forced[1] = True
            cv2.namedWindow('Camera debug')
            cv2.setMouseCallback('Camera debug', evt, players)

        while True:
            if cv2.waitKey(1) & 0xFF in (ord('q'), -1, 27):
                self.debug = False
                cv2.destroyAllWindows()

            ret, frame = cap.read()
            corners = None
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                corners, ids, _ = aruco.detectMarkers(gray, self.aruco_dict)

                found = [False, False]
                if type(ids) != type(None):
                    for i, c in zip(ids, corners):
                        i = i[0]
                        center = (
                            (c[0][0][0] + c[0][1][0] + c[0][2][0] + c[0][3][0]) / 4,
                            (c[0][0][1] + c[0][1][1] + c[0][2][1] + c[0][3][1]) / 4
                        )
                        if i < 4:
                            anchors[i] = center
                        if i == 10:
                            players[0] = center
                            found[0] = True
                            self.forced[0] = False
                        if i == 34:
                            players[1] = center
                            found[1] = True
                            self.forced[1] = False
                    cx, cy, n = 0, 0, 0
                    for p in anchors:
                        if p:
                            cx += p[0]
                            cy += p[1]
                            n += 1
                    if n:
                        anchor0 = (cx/n, cy/n)
                if not found[0] and not self.forced[0]:
                    players[0] = None
                if not found[1] and not self.forced[1]:
                    players[1] = None

            angles = [
                -atan2(players[0][1] - anchor0[1], players[0][0] - anchor0[0]) if anchor0 and players[0] else None,
                -atan2(players[1][1] - anchor0[1], players[1][0] - anchor0[0]) if anchor0 and players[1] else None
            ]

            if self.debug:
                if corners != None:
                    frame = aruco.drawDetectedMarkers(frame, corners)
                else:
                    frame = np.zeros((480, 640, 3))
                for a in anchors:
                    if a:
                        frame = cv2.circle(frame, tuple(map(int, a)), 5, (255,0,0), -1)
                if anchor0:
                    frame = cv2.circle(frame, tuple(map(int, anchor0)), 4, (0,0,255), -1)
                if players[0]:
                    frame = cv2.circle(frame, tuple(map(int, players[0])), 4, (255,255,0), -1)
                if players[1]:
                    frame = cv2.circle(frame, tuple(map(int, players[1])), 4, (0,255,255), -1)
                frame = cv2.putText(
                    frame,
                    str(angles[0] * 180 / pi) if angles[0] else 'None',
                    (20,40), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255)
                )
                frame = cv2.putText(
                    frame,
                    str(angles[1] * 180 / pi) if angles[1] else 'None',
                    (20,80), cv2.FONT_HERSHEY_SIMPLEX, 1, (255,255,255)
                )
                cv2.imshow('Camera debug', frame)

            if self.lock.acquire():
                if not self.running:
                    self.lock.release()
                    break
                self.angles = angles.copy()
                self.lock.release()

        cap.release()
        cv2.destroyAllWindows()

    def stop(self):
        if self.lock.acquire():
            self.running = False
            self.lock.release()

    def get_angles(self):
        angles = None
        if self.lock.acquire():
            angles = self.angles.copy()
            self.lock.release()
        return angles
