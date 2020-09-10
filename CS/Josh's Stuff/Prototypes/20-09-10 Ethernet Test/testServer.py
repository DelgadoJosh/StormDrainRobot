import socket
import time 
import os 
import random

class Server():
  port = 5000
  def __init__(self, Address=('', port), MaxClient=1):
    self.s = socket.socket()
    self.s.bind(Address)
    self.s.listen(MaxClient)
  
  def WaitForConnection(self):
    self.Client, self.Adr=(self.s.accept())
    print('Got a connection from: '+str(self.Client)+'.')

s = Server()
print("Server initiated. Waiting for connection.")
s.WaitForConnection()

# Wait for the data, and print it.
while True:
  data = s.Client.recv(1024) # Receive the data from the client
  print(data)
  
  if not data:
    break 

  s.Client.sendall(data) # Ping back the received data


