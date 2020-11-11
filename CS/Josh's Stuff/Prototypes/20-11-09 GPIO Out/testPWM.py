from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685 
import time
import RPi.GPIO as GPIO  # Yes, that's RPi, as in Raspberry Pi. Jetson doesn't support PWM.

print("Starting up")
i2c_bus = busio.I2C(SCL, SDA) 
print(i2c_bus.scan())

print("Starting up pca")
pca = PCA9685(i2c_bus) 

print("Setting frequency")
pca.frequency = 30#2000#100

# Disable warning from GPIO
GPIO.setwarnings(False)

MAX = 0xFFFF

PINS = [0]
# PERCENT_SPEEDS = [0, 0.1, 0.2]
TEST_PIN = 1

def setSpeed(percentSpeed, pin):
    print(f"Setting speed to {percentSpeed} out of 1")
    speed = abs( int(MAX*percentSpeed) )
    pca.channels[pin].duty_cycle = speed


print("Please input speed")
while True:
    percentSpeed = float(input())
    # print(percentSpeed)
    for pin in PINS:
        setSpeed(percentSpeed, pin)


# setSpeed(0)
# time.sleep(3)

# setSpeed(0.5)
# time.sleep(3)

# setSpeed(1)
# time.sleep(3)

# setSpeed(0)


# setup()

print("Cleaning it up")

