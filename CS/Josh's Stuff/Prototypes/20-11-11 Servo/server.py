import socket 
import time 
import os 
import random 

# Importing custom libraries
import lights
import utils

class Server():
    port = 4000
    def __init__(self , Address=('', port), MaxClient=1):
        self.s = socket.socket() 
        self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.s.bind(Address)
        self.s.listen(MaxClient) 
    
    def WaitForConnection(self):
        self.Client, self.Adr = (self.s.accept())
        print(f"Got a connection from {str(self.Client)}.")

s = Server() 
print("Server initiated. Waiting for connection.") 
s.WaitForConnection() 

# motors.setup()

# Wait for the data, print it, and send it back
while True:
    data = s.Client.recv(1024) # Recieve the data from the client
    print(data)

    if not data:
        break

    # Move the motors
    splitData = utils.parse(utils.cleanup(str(data)))
    if splitData is not None:
        # motors.setLeftSpeed(splitData[0])
        # motors.setRightSpeed(splitData[1])
        lights.setPWM(splitData[0])


    if (data == b"ping"):
        s.Client.sendall("Pong!".encode('utf-8'))
        print("Test")
    else:
        s.Client.sendall(data) # Ping back the received data


