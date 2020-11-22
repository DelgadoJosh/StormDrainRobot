from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685
import RPi.GPIO as GPIO  # Yes, that's RPi, as in Raspberry Pi. Jetson doesn't support PWM.
import time 

print("Starting up")
i2c_bus = busio.I2C(SCL, SDA) 
print(i2c_bus.scan())

print("Starting up pca")
pca = PCA9685(i2c_bus) 

print("Setting frequency for motors")
# pca.frequency = 369 #100
pca.frequency = 1526

# Disable warning from GPIO
GPIO.setwarnings(False)

MAX = 0xFFFF
motor_pwm_pins = [0, 1, 2, 3]
motor_dir_pins = ["GPIO_PZ0", "GPIO_PE6", "SPI1_MISO", "SPI1_SCK"] # 31=GPIO_PZ0,  33=GPIO_PE6, SPI1_MISO=21, SPI1_SCK=23
    # GPIO.TEGRA_SOC = the mode for defining the pins
motor_signs = [-1, -1, 1, 1] 
    # Due to the wiring, the front and back have reversed directions

# Front = 0, 1
# Rear = 2, 3
left_indices = [1, 2]
right_indices = [0, 3]

def setup():
    for i in range(len(motor_dir_pins)):
        GPIO.setup(motor_dir_pins[i], GPIO.OUT)

def setSpeed(index, percentSpeed):
    print(f"Setting speed for {index} to {percentSpeed}")
    percentSpeed *= motor_signs[index] 
    if percentSpeed > 0:
        sign = GPIO.HIGH 
    else: 
        sign = GPIO.LOW 
    speed = abs( int(MAX*percentSpeed) )

    pca.channels[motor_pwm_pins[index]].duty_cycle = speed 
    GPIO.output(motor_dir_pins[index], sign)

def setLeftSpeed(percentSpeed):
    print(f"Setting left speed to {percentSpeed}")
    for i in left_indices:
        setSpeed(i, percentSpeed)

def setRightSpeed(percentSpeed):
    print(f"Setting right speed to {percentSpeed}")
    for i in right_indices:
        setSpeed(i, percentSpeed)

setup()

def testMotors():
    print("Beginning motor test")
    print("Both at rest for 1 sec")
    setLeftSpeed(0)
    setRightSpeed(0)
    time.sleep(1)

    print()
    print("Both forwards at 0.1 for 3 secs")
    setLeftSpeed(0.1)
    setRightSpeed(0.1)
    time.sleep(3)

    # print()
    # print("Left in place at 0.1 for 3 secs")
    # setLeftSpeed(-0.1)
    # setRightSpeed(0.1)
    # time.sleep(3)

    # print()
    # print("Right in place at 0.1 for 3 secs")
    # setLeftSpeed(0.1)
    # setRightSpeed(-0.1)
    # time.sleep(3)

    print()
    print("Right motors only 0.1 for 3 secs")
    setLeftSpeed(0)
    setRightSpeed(0.1)
    time.sleep(3)

    print() 
    print("Right motors only -0.1 for 3 secs")
    setLeftSpeed(0)
    setRightSpeed(-0.1)
    time.sleep(3)

    print()
    print("Left motors only 0.1 for 3 secs")
    setLeftSpeed(0.1)
    setRightSpeed(0)
    time.sleep(3)

    print()
    print("Left motors only -0.1 for 3 secs")
    setLeftSpeed(-0.1)
    setRightSpeed(0)
    time.sleep(3)

    print()
    print("Ending testing.")
    setLeftSpeed(0)
    setRightSpeed(0)

# runTest()

