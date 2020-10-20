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







# import RPi.GPIO as io
# import GPIO as io

import Jetson.GPIO as GPIO
import time 

GPIO.setmode(GPIO.BCM)

# Constant values, 
PWM_MAX                 = 100

# Disable warning from GPIO
# GPIO.setwarnings(False)

# Here we configure the GPIO settings for the left and right motors spinning direction.
# as described in the user manual of MDD10A http://www.robotshop.com/media/files/pdf/user-manual-mdd10a.pdf
# there are four input PWM1-DIR1-PWM2-DIR2
# WITH MAX Frequency 20 Hz, and it works as follow,
#		Input	DIR		Output-A	Output-B
#	PWM	 off	X		  off		  off
#	PWM	 on		off		  on		  off
#	PWM	 on		on		  off		  on

# The pins configuration for Model B Revision 1.0 
leftMotor_DIR_pin = 22 # 33, 35, 37 maybe
leftMotor_PWM_pin = 17 
# rightMotor_DIR_pin = 23
# rightMotor_PWM_pin = 18

GPIO.setup(leftMotor_DIR_pin, GPIO.OUT)
# io.setup(rightMotor_DIR_pin, io.OUT)

GPIO.output(leftMotor_DIR_pin, False)


# Here we configure the GPIO settings for the left and right motors spinning speed. 

GPIO.setup(leftMotor_PWM_pin, GPIO.OUT)

# MAX Frequency 20 Hz
leftMotorPWM = GPIO.PWM(leftMotor_PWM_pin,20)

leftMotorPWM.start(0)
leftMotorPWM.ChangeDutyCycle(0)

leftMotorPower = 0

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
		# Stopp mode for the left motor
		GPIO.output(leftMotor_DIR_pin, False)
		pwm = 0
  #	print "SetMotorLeft", pwm
	leftMotorPower = pwm
	leftMotorPWM.ChangeDutyCycle(pwm)