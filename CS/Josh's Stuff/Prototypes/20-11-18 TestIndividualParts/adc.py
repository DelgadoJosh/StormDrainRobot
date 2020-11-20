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

R1 = 30000
R2 = 7500

# Vin = Vout * (R1 + R2)/R2
coefficient = 1.0*(R1 + R2)/R2

def getVoltage():
    chan = AnalogIn(ads, ADS.P0)

    Vout = chan.voltage
    Vin = Vout * coefficient 
    return Vin

def testADC():
    print("Beginning ADC Test (Measuring voltage)")

    print("Reading input every 0.1 sec for 1 sec")
    for i in range(10):
        voltage = getVoltage()
        print(f"Voltage: {voltage:.4f}")
        time.sleep(0.1)
    
    print()
    print("Ending ADC Test")
    print()

# testADC()