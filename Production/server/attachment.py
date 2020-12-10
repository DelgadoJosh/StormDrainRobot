# UCF Stormwater Drain Robot 2020 - Team Black

# Attachment
# This controls the PWM sent to control the amount of power for the attachment
# https://www.youtube.com/watch?v=8YKAtpPSEOk
from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685 

DEBUG = False
ATTACHMENT_PIN = 15
MAX = 0xFFFF

print("Starting up")
i2c_bus = busio.I2C(SCL, SDA) 
print(i2c_bus.scan())

print("Starting up pca")
pca = PCA9685(i2c_bus) 

print("Setting frequency for attachment")
pca.frequency = 1526

def setPWM(percentPower):
    power = abs(int(MAX*percentPower))
    if DEBUG:
        print(f"Setting attachment power to {percentPower}")
    pca.channels[ATTACHMENT_PIN].duty_cycle = power