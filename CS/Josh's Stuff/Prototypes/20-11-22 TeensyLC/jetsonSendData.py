from smbus import SMBus 

addr = 0x29 
bus = SMBus(1)

doLoop = True 

print("Please input data to send, preferably a single integer")
while (doLoop):
  toSend = input(">>>>  ")
  
  if(toSend == "1" or toSend == "0"):
    bus.write_byte(addr, 0x1)
  else: 
    toSend = 0