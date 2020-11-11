# https://www.youtube.com/watch?v=8YKAtpPSEOk
from adafruit_servokit import ServoKit 
import time # For pausing
from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685 
import time

print("Starting up")
i2c_bus = busio.I2C(SCL, SDA) 
print(i2c_bus.scan())

print("Starting up pca")
pca = PCA9685(i2c_bus) 

print("Setting frequency")
pca.frequency = 369

HORIZONTAL_PIN = 4
VERTICAL_PIN = 5
PWM_PIN = 0
PINS = [HORIZONTAL_PIN, VERTICAL_PIN]

print("Starting up")
myKit = ServoKit(channels=16, frequency=369) # 369   370 too high

lo = 0
hi = 180
for pin in PINS:
    # For the TGY-50090W, the actuation_range = 195, and the pulse_width_range is 5000, 2850
    myKit.servo[pin].actuation_range=195
    myKit.servo[pin].set_pulse_width_range(500, 2650)  #2850

MAX = 0xFFFF

def setAngle(angle, pin):
    print(f"Setting Pin {pin} to angle {angle}")
    myKit.servo[pin].angle = angle

def setPWM(percentPower, pin):
    power = abs(int(MAX*percentPower))
    pca.channels[pin].duty_cycle = power

print("Please input x and y range")
# while True:
#     x = float(input())
#     y = float(input())
#     pwm = float(input())

#     setAngle(x, HORIZONTAL_PIN)
#     setAngle(y, VERTICAL_PIN)
#     setPWM(pwm, PWM_PIN)
