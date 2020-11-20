import socket
import cv2 
import struct
import pickle
import base64
import time
# import PIL.Image as Image
import numpy as np
import threading

# Create the client to receive video

payload_size = struct.calcsize("Q")

class Client_Viewer():
  ip_address = "10.0.0.2"
  # ip_address = "localhost"
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

def grabVideoLoop():
  global data
  numFrames = 0
  startTime = time.time()
  while True:
    try:
      # Retrieve message size
      while len(data) < payload_size:
        data += c.s.recv(4096)
      
      packed_msg_size = data[:payload_size]
      data = data[payload_size:]
      msg_size = struct.unpack("Q", packed_msg_size)[0]

      # Retrieve all dat based on message size
      while len(data) < msg_size:
        data += c.s.recv(4096)
      
      frame_data = data[:msg_size]
      data = data[msg_size:]

      # Extract frame
      frameBytes = base64.b64decode(frame_data) # If doing the raw encoded data
      img_as_np = np.frombuffer(frameBytes, dtype=np.uint8)
      frame = cv2.imdecode(img_as_np, flags=1)
      

      # Display
      cv2.imshow("Frame", frame)
      cv2.waitKey(1)

      numFrames += 1
      duration = time.time() - startTime 
      print(f"FPS: {numFrames/duration:.3f}")

    except KeyboardInterrupt:
      cv2.destroyAllWindows()
      break


receive_video_loop = threading.Thread(target=grabVideoLoop)

receive_video_loop.start()

 
 