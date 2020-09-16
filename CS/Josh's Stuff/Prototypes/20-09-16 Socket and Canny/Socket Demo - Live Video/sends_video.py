# ZMQ
# https://www.pyimagesearch.com/2019/04/15/live-video-streaming-over-network-with-opencv-and-imagezmq/


# Stack overflow
# https://stackoverflow.com/questions/30988033/sending-live-video-frame-over-network-in-python-opencv


# Lovely socket tutorial
# https://realpython.com/python-sockets/


import cv2 
import socket
import pickle
import struct
# import base64

port = 5000


# class Video_Sender():
#   ip_address = "localhost"
#   port = 5000
#   def __init__(self, Address=(ip_address, port)):
#     self.s = socket.socket()
#     self.s.connect(Address) 
  
#   def send(self, message):
#     self.s.send(message)

# print("Initiating Video Sender")
# vs = Video_Sender()
# print("Video Sender connected")


class Video_Sender():
  ip_address = ""
  port = 5000
  def __init__(self, Address=(ip_address, port), MaxClient=1):
    self.s = socket.socket()
    self.s.bind(Address)
    self.s.listen(MaxClient)
  
  def WaitForConnection(self):
    self.Client, self.Adr = (self.s.accept())
    print(f"Got a connection from: {str(self.Client)}.")
  
s = Video_Sender()
print("Video Sender initialized. Waiting for connection to send video.")
s.WaitForConnection()

# Initialize camera
camera = cv2.VideoCapture(0)  

# Loop to send the video, frame by frame.
while True: 
  grabbed, frame = camera.read()  # Grab the current frame
  # frame = cv2.resize(frame, (640, 480)) # Resize the frame
  # encoded, buffer = cv2.imencode('.jpg', frame) 

  # jpg_as_text = base64.b64encode(buffer) # This may not be necessary

  # # Send the data. Use sendAll to guarantee it's sent at the same time
  # s.Client.sendall(jpg_as_text)

  # Serialize frame
  data = pickle.dumps(frame) 

  # Send message length first
  message_size = struct.pack("L", len(data))

  # Then data
  s.Client.sendall(message_size + data)

