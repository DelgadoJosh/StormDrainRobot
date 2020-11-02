# # https://www.youtube.com/watch?v=8YKAtpPSEOk
# # https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython
# from adafruit_servokit import ServoKit 
# import time # For pausing

# myKit = ServoKit(channels=16)
# # myKit.servo[0].angle = 180
# myKit.continuous_servo[1].throttle = 0

# pause_time = .01

# # Full ahead
# myKit.continuous_servo[1].throttle = 1
# time.sleep(1) 

# # Full reverse
# myKit.continuous_servo[1].throttle = -1
# time.sleep(1)

# for i in range(0, 100, 1):
#     # myKit.servo[0].angle = i
#     myKit.continuous_servo[1].throttle = i
#     time.sleep(pause_time)

# for i in range(100, 0, -1):
#     myKit.continuous_servo[1].throttle = i
#     time.sleep(pause_time)



# Maybe use servo driver to support pwm
# https://learn.adafruit.com/16-channel-pwm-servo-driver/python-circuitpython
# led_channel = pca.channels[0]
# led_channel.duty_cycle = 0xffff

# Control IC
# https://circuitpython.readthedocs.io/projects/pca9685/en/latest/api.html

# sudo pip install adafruit-circuitpython-pca9685 
# python3 motorsViaController.py

from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685 
import time
i2c_bus = busio.I2C(SCL, SDA) 
pca = PCA9685(i2c_bus) 
pca.frequency = 60


import RPi.GPIO as GPIO  # Yes, that's RPi, as in Raspberry Pi. Jetson doesn't support PWM.

print(f"GPIO Mode {GPIO.getmode()}")
print(f"GPIO.Board = {GPIO.BOARD}")
print(f"GPIO.BCM = {GPIO.BCM}")
# Board Numbering Scheme
# GPIO.setmode(GPIO.BOARD)


# Disable warning from GPIO
GPIO.setwarnings(False)

leftMotor_DIR_pin = 31
GPIO.setup(leftMotor_DIR_pin, GPIO.OUT)
GPIO.output(leftMotor_DIR_pin, False)


print("Increasing to 50% speed")
pca.channels[1].duty_cycle = 0x7FFF
time.sleep(1)
print("Setting speed to 0")
pca.channels[1].duty_cycle = 0x0