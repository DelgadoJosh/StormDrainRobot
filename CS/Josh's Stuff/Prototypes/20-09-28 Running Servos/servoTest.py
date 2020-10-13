# from adafruit_servokit import ServoKit 

# myKit = ServoKit(channels=16)

# # Sets the angle to 90 degrees
# # myKit.servo[0].angle = 90 


# # Go from 0 to 180 degrees
# for i in range(0, 180, 1):
#   myKit.servo[0].angle=i 
#   time.sleep(.1)

# # Go from 180 to 0 degrees
# for i in range(180, 0, -1):
#   myKit.servo[0].angle = i
#   time.sleep(.1)


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