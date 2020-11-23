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

def readEncoder():
    data_arr = bus.read_i2c_block_data(addr, 0)
    value = convertToInt(data_arr)
    return value

