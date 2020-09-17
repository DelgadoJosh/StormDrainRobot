import socket
import cv2 
import struct
import pickle


# Create the client to receive video

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




