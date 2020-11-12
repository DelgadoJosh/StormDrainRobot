# https://www.youtube.com/watch?v=8YKAtpPSEOk
from adafruit_servokit import ServoKit 
import time # For pausing
from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685 
import time

LIGHTS_PIN = 6
MAX = 0xFFFF

print("Starting up")
i2c_bus = busio.I2C(SCL, SDA) 
print(i2c_bus.scan())

print("Starting up pca")
pca = PCA9685(i2c_bus) 

print("Setting frequency")
pca.frequency = 369

def setPWM(percentPower):
    power = abs(int(MAX*percentPower))
    print(f"Setting power to {power}")
    pca.channels[LIGHTS_PIN].duty_cycle = power