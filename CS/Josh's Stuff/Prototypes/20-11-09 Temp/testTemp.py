import board
import busio
import adafruit_si7021
import time
i2c = busio.I2C(board.SCL, board.SDA)
sensor = adafruit_si7021.SI7021(i2c)

while(True):
    print(f"Temperature: {sensor.temperature} | Humidity: {sensor.relative_humidity}")
    time.sleep(1)
