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

PWM_PIN = 0

MAX = 0xFFFF

def setPWM(percentPower):
    power = abs(int(MAX*percentPower))
    pca.channels[PWM_PIN].duty_cycle = power