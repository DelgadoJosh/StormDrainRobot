import board
import busio
import adafruit_ads1x15.ads1115 as ADS 
from adafruit_ads1x15.analog_in import AnalogIn
import time

i2c = busio.I2C(board.SCL, board.SDA)

ads = ADS.ADS1115(i2c)
ads.mode = ADS.Mode.CONTINUOUS
ads.gain = 1

R1 = 30000
R2 = 7500


while(True):
    chan = AnalogIn(ads, ADS.P1)

    Vout = chan.voltage 
    Vin = Vout * (R1 + R2)/R2
    # print(chan.value, chan.voltage) 

    print(f"{chan.value} {chan.voltage} | Vin = {Vin}")
    time.sleep(1)

