"""
from pymata4 import pymata4
from pymata4 import Ultrasonic
import time

class Ultrasonic(object):
    def init(self,board,trigPin=13,echoPin=12):
        self.board=board
        self.sr=board.sr
        self.trigPin=trigPin
        self.echoPin=echoPin

    def distanceMeasure(self):
        cmd_str = build_cmd_str("us", (self.trigPin, self.echoPin))
        self.sr.write(cmd_str)
        self.sr.flush()
        rd = self.sr.readline().replace("\r\n", "")

        if rd.isdigit():
            return int(rd)

us1 = Ultrasonic(ar,13,12) #13, trigPin; 12, echoPin

while True:
    dis=us1.distanceMeasure()
    if type(dis) is int:
        print('Distance= %d cm' % dis)
    time.sleep(0.5)
"""