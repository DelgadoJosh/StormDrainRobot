# UCF Stormwater Drain Robot 2020 - Team Black

# Teensy
# This controls reading the teensy for the motor encoder data

from smbus import SMBus 
import time

addr = 0x29 
bus = SMBus(1)
len = 32

def convertToInt(arr):
  num = 0
  for i in range(len-1, 0-1, -1):
    num *= 255 
    num += arr[i] 
  return num

readingsPerRotation = 960
def readEncoder():
    data_arr = bus.read_i2c_block_data(addr, 0)
    value = convertToInt(data_arr)
    value /= readingsPerRotation
    return value

