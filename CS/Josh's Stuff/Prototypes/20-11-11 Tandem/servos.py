# Custom Library to adjust the servos
# https://www.youtube.com/watch?v=8YKAtpPSEOk
from adafruit_servokit import ServoKit
import time 

HORIZONTAL_PIN = 0 # 4 
VERTICAL_PIN = 1 # 5
PINS = [HORIZONTAL_PIN, VERTICAL_PIN]

print("Starting up servo kit")
# myKit = ServoKit(channels=16, frequency=60) # 369   370 too high
myKit = ServoKit(channels=16, frequency=60, address=0x41)

# lo = 0
# hi = 180
# Initialize the servos
for pin in PINS:
    # For the TGY-50090W, the actuation_range = 195, and the pulse_width_range is 5000, 2850
    myKit.servo[pin].actuation_range=195
    myKit.servo[pin].set_pulse_width_range(500, 2650)  #2850

def setAngle(angle, pin):
    print(f"Setting Pin {pin} to angle {angle}")
    myKit.servo[pin].angle = angle

def setHorizontalAngle(angle):
    setAngle(angle, HORIZONTAL_PIN) 

def setVerticalAngle(angle):
    setAngle(angle, VERTICAL_PIN)