import time
import serial
import random       
ser = serial.Serial(            
port='/dev/ttyS0',
baudrate = 9600,
parity=serial.PARITY_NONE,
stopbits=serial.STOPBITS_ONE,
bytesize=serial.EIGHTBITS,
timeout=1
)
while True:
    time.sleep(1)
    feedback = ser.read()
    print(feedback)