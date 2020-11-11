from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685 
import time
# import RPi.GPIO as GPIO  # Yes, that's RPi, as in Raspberry Pi. Jetson doesn't support PWM.

print("Starting up")
i2c_bus = busio.I2C(SCL, SDA) 
print(i2c_bus.scan())

print("Starting up pca")
pca = PCA9685(i2c_bus) 

print("Setting frequency")
pca.frequency = 369

# Disable warning from GPIO
# GPIO.setwarnings(False)

MAX = 0xFFFF

def setSpeed(angle, pin):
    pwm_angle = abs(int(MAX*angle)) 

    pca.channels[pin].duty_cycle = pwm_angle
    

PIN = 4
while True:
    percent = float(input())
    setSpeed(percent, PIN)

print("Cleaning it up")

