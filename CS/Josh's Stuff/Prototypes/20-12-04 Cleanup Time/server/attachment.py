# https://www.youtube.com/watch?v=8YKAtpPSEOk
import time # For pausing
from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685 
import time

DEBUG = False
ATTACHMENT_PIN = 7
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

def testAttachment():
    print("Beginning Attachment Test")
    
    print("Setting to 0% power initially for 1 sec")
    setPWM(0)
    time.sleep(1)

    for i in range(100):
        setPWM(i / 100.0)
        time.sleep(0.1)

    print()
    print("Ending Test")
    print()
    setPWM(0)

if __name__ == '__main__':
    testAttachment()