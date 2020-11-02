# import Jetson.GPIO as GPIO
# import time

# # for 1st Motor on ENA
# ENA = 33
# IN1 = 35
# IN2 = 37

# # set pin numbers to the board's
# GPIO.setmode(GPIO.BOARD)

# # initialize EnA, In1 and In2
# GPIO.setup(ENA, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(IN1, GPIO.OUT, initial=GPIO.LOW)
# GPIO.setup(IN2, GPIO.OUT, initial=GPIO.LOW)

# # Stop
# GPIO.output(ENA, GPIO.HIGH)
# GPIO.output(IN1, GPIO.LOW)
# GPIO.output(IN2, GPIO.LOW)
# time.sleep(1)

# # Forward
# GPIO.output(IN1, GPIO.HIGH)
# GPIO.output(IN2, GPIO.LOW)
# time.sleep(1)

# # Stop
# GPIO.output(IN1, GPIO.LOW)
# GPIO.output(IN2, GPIO.LOW)
# time.sleep(1)

# # Backward
# GPIO.output(IN1, GPIO.LOW)
# GPIO.output(IN2, GPIO.HIGH)
# time.sleep(1)

# # Stop
# GPIO.output(ENA, GPIO.LOW)
# GPIO.output(IN1, GPIO.LOW)
# GPIO.output(IN2, GPIO.LOW)
# time.sleep(1)

# GPIO.cleanup()




# https://learn.adafruit.com/circuitpython-libraries-on-linux-and-the-nvidia-jetson-nano/initial-setup
# sudo pip install adafruit-blinka

# sudo pip install adafruit-circuitpython-pca9685 


# from board import SCL, SDA
# import busio 
# from adafruit_pca9685 import PCA9685 
# i2c_bus = busio.I2C(SCL, SDA) 
# pca = PCA9685(i2c_bus) 
# pca.frequency = 60
# pca.channels[1].duty_cycle = 0x7FFF









# import RPi.GPIO as io
# import GPIO as io

import RPi.GPIO as GPIO  # Yes, that's RPi, as in Raspberry Pi. Jetson doesn't support PWM.
# import Jetson.GPIO as GPIO
import time 

# Board Numbering Scheme
# GPIO.setmode(GPIO.BCM)
GPIO.setmode(GPIO.BOARD)

# Constant values, 
# PWM_MAX                 = 100
PWM_MAX = 100

# Disable warning from GPIO
GPIO.setwarnings(False)

# Here we configure the GPIO settings for the left and right motors spinning direction.
# as described in the user manual of MDD10A http://www.robotshop.com/media/files/pdf/user-manual-mdd10a.pdf
# there are four input PWM1-DIR1-PWM2-DIR2
# WITH MAX Frequency 20 Hz, and it works as follow,
#		Input	DIR		Output-A	Output-B
#	PWM	 off	X		  off		  off
#	PWM	 on		off		  on		  off
#	PWM	 on		on		  off		  on

# The pins configuration for Model B Revision 1.0 
# leftMotor_DIR_pin = 22 # 33, 35, 37 maybe
# leftMotor_PWM_pin = 17 
leftMotor_DIR_pin = 31 #37
leftMotor_PWM_pin = 33 #35  # I believe 33, 35 are pwm pins
# rightMotor_DIR_pin = 23
# rightMotor_PWM_pin = 18

GPIO.setup(leftMotor_DIR_pin, GPIO.OUT)
# io.setup(rightMotor_DIR_pin	, io.OUT)

# GPIO.output(leftMotor_DIR_pin, False)
GPIO.output(leftMotor_DIR_pin, GPIO.LOW)
# GPIO.output(leftMotor_DIR_pin, GPIO.HIGH)


# Here we configure the GPIO settings for the left and right motors spinning speed. 

# GPIO.setup(leftMotor_PWM_pin, GPIO.OUT)

# MAX Frequency 50 Hz
leftMotorPWM = GPIO.PWM(leftMotor_PWM_pin, 50)

print("Setting speed to 0%")
leftMotorPWM.start(0)
leftMotorPWM.ChangeDutyCycle(0)
# pca.channels[1].duty_cycle = 0x7FFF
time.sleep(1)
print("Setting speed to 50%")
leftMotorPWM.ChangeDutyCycle(50)
# pca.channels[1].duty_cycle = 0x0000
time.sleep(1)
print("Setting speed to 0%")
# pca.channels[1].duty_cycle = 0x7FFF
leftMotorPWM.ChangeDutyCycle(0)

leftMotorPower = 0



def setMotorLeft(power):

  # SetMotorLeft(power)

  # Sets the drive level for the left motor, from +1 (max) to -1 (min).

  # This is a short explanation for a better understanding:
  # SetMotorLeft(0)     -> left motor is stopped
  # SetMotorLeft(0.75)  -> left motor moving forward at 75% power
  # SetMotorLeft(-0.5)  -> left motor moving reverse at 50% power
  # SetMotorLeft(1)     -> left motor moving forward at 100% power

	if power < 0:
		# Reverse mode for the left motor
		GPIO.output(leftMotor_DIR_pin, False)
		pwm = -int(PWM_MAX * power)
		if pwm > PWM_MAX:
			pwm = PWM_MAX
	elif power > 0:
		# Forward mode for the left motor
		GPIO.output(leftMotor_DIR_pin, True)
		pwm = int(PWM_MAX * power)
		if pwm > PWM_MAX:
			pwm = PWM_MAX
	else:
		# Stop mode for the left motor
		GPIO.output(leftMotor_DIR_pin, False)
		pwm = 0
	print (f"SetMotorLeft {pwm}")
	leftMotorPower = pwm
	leftMotorPWM.ChangeDutyCycle(pwm)



# Move forwards at 100% speed
setMotorLeft(1) 
time.sleep(2) 

# Move backwards at 100% speed
setMotorLeft(-1) 
time.sleep(2)

# Stop the motor
setMotorLeft(0)
time.sleep(1)


GPIO.cleanup() 

