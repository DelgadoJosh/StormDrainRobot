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
pca.frequency = 100

# Disable warning from GPIO
GPIO.setwarnings(False)

MAX = 0xFFFF
motor_pwm_pins = [1, 2]
# GPIO.TEGRA_SOC = the mode for defining the pins
motor_dir_pins = ["GPIO_PZ0", "GPIO_PE6"]

def setup():
    for i in range(len(motor_dir_pins)):
        GPIO.setup(motor_dir_pins[i], GPIO.OUT)

def setSpeed(percentSpeed):
    print(f"Setting speed to {percentSpeed}")
    if percentSpeed > 0: 
        sign = GPIO.HIGH 
    else: 
        sign = GPIO.LOW
    speed = abs(int(MAX*percentSpeed))

    # Set the speed for all motors
    for i in range(len(motor_pwm_pins)):
        pca.channels[motor_pwm_pins[i]].duty_cycle = speed 
        GPIO.output(motor_dir_pins[i], sign)

setup()

setSpeed(0.5)
time.sleep(3)

setSpeed(1)
time.sleep(3)

setSpeed(-1)
time.sleep(3)

setSpeed(0)
time.sleep(3)

setSpeed(-1)
time.sleep(3)

setSpeed(0)

print("Cleaning it up")

