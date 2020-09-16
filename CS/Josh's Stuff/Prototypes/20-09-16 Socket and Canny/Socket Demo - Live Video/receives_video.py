import socket
import cv2 
# import base64
import struct
import pickle
# import numpy as np


# Create the client to receive video

# class Viewer():
#   port = 5000
#   def __init__(self, Address=('', port), MaxClient=1):
#     self.s = socket.socket()
#     self.s.bind(Address)
#     self.s.listen(MaxClient)
  
#   def WaitForConnection(self):
#     self.Client, self.Adr = (self.s.accept())
#     print(f"Got a connection from: {str(self.Client)}.")

# v = Viewer()
# print ("Viewer Initiated. Waiting for connection.")
# v.WaitForConnection()

# size_of_data = 4096
payload_size = struct.calcsize("L")

class Client_Viewer():
  ip_address = "localhost"
  port = 5000
  def __init__(self, Address=(ip_address, port)):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect(Address)

  def send(self, message):
    self.s.send(message)
  
print("Initiating Client Viewer")
c = Client_Viewer()
print("Client Connected to the Server")

data = b''

while True:
  # Retrieve message size
  while len(data) < payload_size:
    data += c.s.recv(4096)
  
  packed_msg_size = data[:payload_size]
  data = data[payload_size:]
  msg_size = struct.unpack("L", packed_msg_size)[0]

  # Retrieve all dat based on message size
  while len(data) < msg_size:
    data += c.s.recv(4096)
  
  frame_data = data[:msg_size]
  data = data[msg_size:]

  # Extract frame
  frame = pickle.loads(frame_data)

  # Display
  cv2.imshow("Frame", frame)
  cv2.waitKey(1)

  # data = c.s.recv(size_of_data)

  # img = base64.b64decode(data) 

  # # npimg = np.fromstring(img, dtype=np.uint8) 
  # npimg = np.frombuffer(img, dtype=np.uint8)
  # source = cv2.imdecode(npimg, 1)
  # cv2.imshow("Stream", source) 
  # cv2.waitKey(1)



