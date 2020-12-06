# UCF Stormwater Drain Robot 2020 - Team Black

# Lights
# This controls the PWM sent to modify the frequency of the lights

# https://www.youtube.com/watch?v=8YKAtpPSEOk
from adafruit_servokit import ServoKit 
from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685 

DEBUG = False
LIGHTS_PIN = 14
MAX = 0xFFFF

print("Starting up")
i2c_bus = busio.I2C(SCL, SDA) 
print(i2c_bus.scan())

print("Starting up pca")
pca = PCA9685(i2c_bus) 

print("Setting frequency")
pca.frequency = 1526

def setPWM(percentPower):
    power = abs(int(MAX*percentPower))
    if DEBUG:
        print(f"Setting power to {power}")
    pca.channels[LIGHTS_PIN].duty_cycle = power