# https://www.youtube.com/watch?v=8YKAtpPSEOk
# https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython
from adafruit_servokit import ServoKit 
import time # For pausing

myKit = ServoKit(channels=16)
# myKit.servo[0].angle = 180
myKit.continuous_servo[1].throttle = 0

pause_time = .01

# Full ahead
myKit.continuous_servo[1].throttle = 1
time.sleep(1) 

# Full reverse
myKit.continuous_servo[1].throttle = -1
time.sleep(1)

# for i in range(0, 100, 1):
#     # myKit.servo[0].angle = i
#     myKit.continuous_servo[1].throttle = i
#     time.sleep(pause_time)

# for i in range(100, 0, -1):
#     myKit.continuous_servo[1].throttle = i
#     time.sleep(pause_time)
