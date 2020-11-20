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

def testServos():
    print("Beginning Servo Test")

    print("Initializing to Horizontal=90 degrees, Vertical=45 degrees, then wait 1 sec")
    setHorizontalAngle(90)
    setVerticalAngle(45)
    time.sleep(1)

    print("Changing Horizontal Angle to 45, then waiting 3 seconds")
    setHorizontalAngle(45)
    time.sleep(3)

    print("Changing Vertical Angle to 60, then waiting 3 seconds")
    setVerticalAngle(60)
    time.sleep(3)

    print("Resetting to Horizontal = 90, Vertical = 45")
    setHorizontalAngle(90)
    setVerticalAngle(45)

    print("Ending Servo Test")
    print()

testServos()