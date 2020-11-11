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

PINS = [4, 5]
# PIN = 1
# PIN2 = 0

print("Starting up")
myKit = ServoKit(channels=16, frequency=369) # 369   370 too high
# myKit.servo[PIN].angle = 180

lo = 0
hi = 180
for pin in PINS:
    myKit.servo[pin].actuation_range=195
    # myKit.servo[pin].set_pulse_width_range(500, 2750) # 1ms to 2ms   # SG90: 500, 2750
    myKit.servo[pin].set_pulse_width_range(500, 2850)  #Specs says 900 to 2100 microseconds
    # For the TGY-50090W, the actuation_range = 195, and the pulse_width_range is 5000, 2850



print("Starting")
pause_time = 0.01

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
