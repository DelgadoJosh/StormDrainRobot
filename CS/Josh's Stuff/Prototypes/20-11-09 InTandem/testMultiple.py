import board
import busio
import adafruit_si7021 # Temp/Humidity
from adafruit_pca9685 import PCA9685 # PWM Board 
import adafruit_ads1x15.ads1115 as ADS # ADC 
from adafruit_ads1x15.analog_in import AnalogIn # ADC AnalogIn
import time

print("Starting up")
i2c = busio.I2C(board.SCL, board.SDA)
print(f"i2c Scan: {i2c.scan()}")
# 72 = ADC
# 64 = Temp Sensor



print("Initializing Analog to Digital Converter")
ads = ADS.ADS1115(i2c)
ads.mode = ADS.Mode.CONTINUOUS
ads.gain = 1

R1 = 30000
R2 = 7500

print("Initializing Temp/Humidity Sensor")
sensor = adafruit_si7021.SI7021(i2c)




print("Initializing PWM Controller (PCA)")
pca = PCA9685(i2c) #(i2c_bus) 

print("Setting frequency")
pca.frequency = 100

MAX = 0xFFFF

TEST_PIN = 1

def setSpeed(percentSpeed):
    print(f"Setting speed to {percentSpeed} out of 1")
    speed = abs( int(MAX*percentSpeed) )
    pca.channels[TEST_PIN].duty_cycle = speed

setSpeed(0)
time.sleep(3)

setSpeed(0.5)
time.sleep(3)

setSpeed(1)
time.sleep(3)

setSpeed(0)



while(True):
    # Temperature to Humdiity
    print(f"Temperature: {sensor.temperature} | Humidity: {sensor.relative_humidity}")

    # Analog to Digital Converter
    chan = AnalogIn(ads, ADS.P1)

    Vout = chan.voltage 
    Vin = Vout * (R1 + R2)/R2 

    print(f"{chan.value} {chan.voltage} | Vin = {Vin}")
    time.sleep(1)




# from board import SCL, SDA
# import busio 
# import time
# import RPi.GPIO as GPIO  # Yes, that's RPi, as in Raspberry Pi. Jetson doesn't support PWM.

# print("Starting up")
# i2c_bus = busio.I2C(SCL, SDA) 
# print(i2c_bus.scan())


# # Disable warning from GPIO
# GPIO.setwarnings(False)





# setup()

print("Cleaning it up")

