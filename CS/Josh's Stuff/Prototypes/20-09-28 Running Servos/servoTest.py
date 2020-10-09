# https://www.youtube.com/watch?v=8YKAtpPSEOk
from adafruit_servokit import ServoKit 
import time # For pausing

myKit = ServoKit(channels=16)
myKit.servo[0].angle = 180

pause_time = .01

for i in range(0, 180, 1):
    myKit.servo[0].angle = i
    time.sleep(pause_time)

for i in range(180, 0, -1):
    myKit.servo[0].angle = i
    time.sleep(pause_time)
