"""
from pymata_aio.pymata3 import PyMata3
from pymata_aio.constants import Constants
import time
while 1:
    print("Enter COM Port Number:")
    port = input()
    if port != "":
        break

board = PyMata3(com_port='COM'+port)


def distance():
    board.digital_write(TRIG, True)
    time.sleep(0.00001)
    board.digital_write(TRIG, False)
    StartTime = time.time()
    StopTime = time.time()
    while board.digital_read(ECHO)==0:
        StartTime = time.time()
    while board.digital_read(ECHO)==1:
        StopTime = time.time()
    TimeElapsed = StopTime - StartTime
    #distance = (TimeElapsed * 34300) / 2
    distance = TimeElapsed * 17150
    distance = round(distance, 2)
    print(distance)
    return distance
while True:
    dist=distance()
    print(dist)
    time.sleep(1)

# https://github.com/MrYsLab/pymata-aio/issues/95
"""