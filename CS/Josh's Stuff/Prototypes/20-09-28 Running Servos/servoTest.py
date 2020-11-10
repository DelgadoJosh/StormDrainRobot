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

PINS = [0, 1]
# PIN = 1
# PIN2 = 0

print("Starting up")
myKit = ServoKit(channels=16)
# myKit.servo[PIN].angle = 180

lo = 0
hi = 180
for pin in PINS:
    myKit.servo[pin].actuation_range=hi
    myKit.servo[pin].set_pulse_width_range(500, 2750) # 1ms to 2ms


print("Starting")
pause_time = .01

for i in range(lo, hi, 1):
    print(i)
    for pin in PINS:
        myKit.servo[pin].angle = i
    # myKit.servo[PIN].angle = i
    # myKit.servo[PIN2].angle = i
    time.sleep(pause_time)

time.sleep(1)
for i in range(hi, lo, -1):
    print(i)
    for pin in PINS:
        myKit.servo[pin].angle = i
    # myKit.servo[PIN].angle = i
    # myKit.servo[PIN2].angle = i
    time.sleep(pause_time)
