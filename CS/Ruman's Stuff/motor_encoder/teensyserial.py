# /dev/ttyTHS1 = jetson port

# sudo python3 teensyserial.py
# ls -l /dev/ttyTHS1
# groups
# sudo usermod -aG dialout teamblack

# This makes it so everyone has read/write permissions
# sudo chmod 666 /dev/ttyTHS1
import time
import serial
import random       
ser = serial.Serial(            
    port='/dev/ttyTHS1', #'/dev/ttyS0',
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