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

port = 5000

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
  try:
    grabbed, frame = camera.read()  # Grab the current frame

    # Serialize frame
    data = pickle.dumps(frame) 

    # Send message length first
    message_size = struct.pack("L", len(data))

    # Then data
    s.Client.sendall(message_size + data)
  
  except KeyboardInterrupt:
    camera.release()
    cv2.destroyAllWindows()
    break

