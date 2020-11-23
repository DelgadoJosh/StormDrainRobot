# Analog to Digital Converter
# Used to measure the voltage in the board

import board
import busio
import adafruit_ads1x15.ads1115 as ADS 
from adafruit_ads1x15.analog_in import AnalogIn
import time

i2c = busio.I2C(board.SCL, board.SDA)

print("Beginning ADC")
ads = ADS.ADS1115(i2c)
ads.mode = ADS.Mode.CONTINUOUS
ads.gain = 1

R1 = 29573 # 30000
R2 = 7300 # 7500

# Used to tune the ADC
# Vin*R2/Vout - R2 = R1 
# print((13.23 * R2)/Vout -R2)


# Vin = Vout * (R1 + R2)/R2
coefficient = 1.0*(R1 + R2)/R2

def getVoltage():
    chan = AnalogIn(ads, ADS.P0)

    Vout = chan.voltage
    Vin = Vout * coefficient 
    return Vin

