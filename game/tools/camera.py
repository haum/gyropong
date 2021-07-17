import cv2
import cv2.aruco as aruco
import numpy as np
import time
import threading
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
        self.running = True

    def run(self):
        cap = cv2.VideoCapture(self.cam)
        while True:
            if cv2.waitKey(1) & 0xFF in (ord('q'), -1, 27):
                self.debug = False
                cv2.destroyAllWindows()

            ret, frame = cap.read()
            if ret:
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                corners, ids, _ = aruco.detectMarkers(gray, self.aruco_dict)

            ap1 = 0 # TODO
            ap2 = 180 # TODO

            if self.debug:
                frame = aruco.drawDetectedMarkers(frame, corners)
                cv2.imshow('Camera debug', frame)

            if self.lock.acquire():
                if not self.running:
                    self.lock.release()
                    break
                self.angle_p1 = ap1
                self.angle_p2 = ap2
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
            angles = (self.angle_p1, self.angle_p2)
            self.lock.release()
        return pos
