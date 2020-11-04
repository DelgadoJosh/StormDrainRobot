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

# import RPi.GPIO as GPIO 
# GPIO.setmode(GPIO.BOARD)

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
pca.frequency = 60



# # from __future__ import division 
# import time 
# # import Adafruit_PCA9685 
# import adafruit_pca9685

# pca = adafruit_pca9685.PCA9685()




import RPi.GPIO as GPIO  # Yes, that's RPi, as in Raspberry Pi. Jetson doesn't support PWM.

print(f"GPIO Mode {GPIO.getmode()}")
print(f"GPIO.Board = {GPIO.BOARD}")
print(f"GPIO.BCM = {GPIO.BCM}")
# Board Numbering Scheme
# GPIO.setmode(GPIO.BOARD)


# Disable warning from GPIO
GPIO.setwarnings(False)

# 
# GPIO.TEGRA_SOC = the mode
leftMotor_DIR_pin = "GPIO_PZ0"  #6 #200 #31
GPIO.setup(leftMotor_DIR_pin, GPIO.OUT)
# GPIO.output(leftMotor_DIR_pin, False)
GPIO.output(leftMotor_DIR_pin, GPIO.HIGH) 

# # # Completely on
# # pca.channels[2].duty_cycle = 0xFFFF 

MAX = 0xFFFF
pwm_pin = 1
print("Increasing to 50% speed")
pca.channels[pwm_pin].duty_cycle = int(MAX*0.5)
time.sleep(3)
print("Increasing to 100% speed")
pca.channels[pwm_pin].duty_cycle = MAX
time.sleep(3)
print("Reversing direction") 
GPIO.output(leftMotor_DIR_pin, GPIO.LOW)
time.sleep(3)
print("Setting speed to 0")
pca.channels[pwm_pin].duty_cycle = 0x0
time.sleep(3)
print("Reversing direction") 
GPIO.output(leftMotor_DIR_pin, GPIO.LOW)
pca.channels[pwm_pin].duty_cycle = MAX
time.sleep(3)
print("Setting speed to 0")
pca.channels[pwm_pin].duty_cycle = 0x0



# # # Locked antiphase
# leftMotor_PWM_pin = "GPIO_PZ0"  #6 #200 #31
# GPIO.setup(leftMotor_PWM_pin, GPIO.OUT)
# # GPIO.output(leftMotor_DIR_pin, False)
# GPIO.output(leftMotor_PWM_pin, GPIO.OUT) 

# MAX = 0xFFFF
# dir_pin = 1
# print("Increasing to 50% speed")
# pca.channels[dir_pin].duty_cycle = int(MAX*0.75)
# time.sleep(3)
# print("Increasing to 100% speed")
# pca.channels[dir_pin].duty_cycle = int(MAX)
# time.sleep(3)
# print("Reversing direction") 
# pca.channels[dir_pin].duty_cycle = 0x0
# time.sleep(3)
# print("Setting speed to 0")
# pca.channels[dir_pin].duty_cycle = 0x0





# https://circuitpython.readthedocs.io/projects/pca9685/en/latest/api.html

# # Locked anti-phase!
# MAX = 0xFFFF
# dir_pin = 2
# pwm_pin = 1
# pca.channels[dir_pin].duty_cycle = 0xFFFF # Set the PWM pin to HIGH to activate locked antiphase

# print("increasing to 100% speed in one dir")
# pca.channels[pwm_pin].duty_cycle = 0x0
# time.sleep(3)

# print("decreasing to 0% speed (neutral)")
# pca.channels[pwm_pin].duty_cycle = 0x7FFF
# time.sleep(1)


# print("Resetting to 0")
# pca.channels[pwm_pin].duty_cycle = 0x0
# pca.channels[dir_pin].duty_cycle = 0x0


# Sign-magnitude!
# dir_pin = 2
# pwm_pin = 1
# pca.channels[dir_pin].duty_cycle = MAX

# print("increasing speed to 50%")
# pca.channels[pwm_pin].duty_cycle = int(MAX*0.5)
# time.sleep(3)

# print("setting speed to 0")
# pca.channels[pwm_pin].duty_cycle = 0x0
# time.sleep(2) 



# Another useful tutorial that may fix this
# https://github.com/adafruit/Adafruit_Python_PCA9685/blob/master/examples/simpletest.py
# Alt version
# https://github.com/adafruit/Adafruit_Python_PCA9685/blob/master/examples/simpletest.py

# Busio
# https://circuitpython.readthedocs.io/en/3.x/shared-bindings/busio/__init__.html

# This may be what I'm looking for
# https://stackoverflow.com/questions/61039191/how-to-setup-gpio-pins-in-gpio-tegra-soc-mode-vs-gpio-bcm-mode-using-jetson-nano


