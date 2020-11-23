from smbus import SMBus 
import time

addr = 0x29 
bus = SMBus(1)

doLoop = True 

len = 32
def convertToNum(arr):
  num = 0
  for i in range(len-1, 0-1, -1):
    num *= 255 
    num += arr[i] 
  return num

# print("Please input data to send, preferably a single integer")
while (doLoop):
  # data = bus.read_byte(addr)
  data = bus.read_i2c_block_data(addr, 0)
  num = convertToNum(data)
  # data = bus.read_block_data(addr, 0)
  # data = bus.read_byte_data()
  print(data)
  print(num)
  time.sleep(0.01)