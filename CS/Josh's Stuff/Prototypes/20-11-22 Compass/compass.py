import board 
import busio
import adafruit_mpu6050
import time

i2c = busio.I2C(board.SCL, board.SDA) 

print("Initializing Compass")
mpu = adafruit_mpu6050.MPU6050(i2c)

while True:
    print(f"Gyro: {mpu.gyro}")
    print(f"Temp: {mpu.temperature}C")
    print(f"Acce: {mpu.acceleration}")
    time.sleep(1)