#!/usr/bin/env python

import rospy
from geometry_msgs.msg import Twist

import RPi.GPIO as GPIO
from board import SCL, SDA
import busio 
from adafruit_pca9685 import PCA9685 
import time

# Set the GPIO modes
GPIO.setwarnings(False)


print("Starting up")
i2c_bus = busio.I2C(SCL, SDA) 
print(i2c_bus.scan())

print("Starting up pca")
pca = PCA9685(i2c_bus) 
pca.frequency = 100
MAX = 0xFFFF



motor_pwm_pins = [1, 2, 3, 4]
motor_dir_pins = ["GPIO_PZ0", "GPIO_PE6", "SPI1_MISO", "SPI1_SCK"] # 31=GPIO_PZ0,  33=GPIO_PE6, SPI1_SCK=23, SPI1_MISO=21
    # GPIO.TEGRA_SOC = the mode for defining the pins

class Motor:
    def __init__(self, _pin):
        self._pin = _pin

        GPIO.setup(_pin, GPIO.OUT)

        self._forward_pwm = GPIO.PWM(forward_pin, _FREQUENCY)

    def move(self, percentSpeed):
        speed = abs( int(MAX*percentSpeed) )

        # Positive speeds move wheels forward, negative speeds
        # move wheels backward
        if percentSpeed > 0:
            GPIO.output(self._pin, GPIO.HIGH)
        else:
            GPIO.output(self._pin, GPIO.LOW)
        pca.channels[self._pin].duty_cycle = speed  

class Driver:
    def __init__(self):
        rospy.init_node('driver')

        self._last_received = rospy.get_time()
        self._timeout = rospy.get_param('~timeout', 2)
        self._rate = rospy.get_param('~rate', 10)
        self._max_speed = rospy.get_param('~max_speed', 0.5)
        self._wheel_base = rospy.get_param('~wheel_base', 0.091)

        # Assign pins to motors. These may be distributed
        # differently depending on how you've built your robot
        self._left_motor = Motor("GPIO_PZ0")
        self._right_motor = Motor("GPIO_PE6")
        self._left_speed_percent = 0
        self._right_speed_percent = 0

        # Setup subscriber for velocity twist message
        rospy.Subscriber(
            'cmd_vel', Twist, self.velocity_received_callback)

    def velocity_received_callback(self, message):
        """Handle new velocity command message."""

        self._last_received = rospy.get_time()

        # Extract linear and angular velocities from the message
        linear = message.linear.x
        angular = message.angular.z

        # Calculate wheel speeds in m/s
        left_speed = linear - angular*self._wheel_base/2
        right_speed = linear + angular*self._wheel_base/2

        # Ideally we'd now use the desired wheel speeds along
        # with data from wheel speed sensors to come up with the
        # power we need to apply to the wheels, but we don't have
        # wheel speed sensors. Instead, we'll simply convert m/s
        # into percent of maximum wheel speed, which gives us a
        # duty cycle that we can apply to each motor.
        self._left_speed_percent = (
            100 * left_speed/self._max_speed)
        self._right_speed_percent = (
            100 * right_speed/self._max_speed)

    def run(self):
        """The control loop of the driver."""

        rate = rospy.Rate(self._rate)

        while not rospy.is_shutdown():
            # If we haven't received new commands for a while, we
            # may have lost contact with the commander-- stop
            # moving
            delay = rospy.get_time() - self._last_received
            if delay < self._timeout:
                self._left_motor.move(self._left_speed_percent)
                self._right_motor.move(self._right_speed_percent)
            else:
                self._left_motor.move(0)
                self._right_motor.move(0)
            rate.sleep()


def main():
    driver = Driver()

    # Run driver. This will block
    driver.run()


if __name__ == '__main__':
    main()