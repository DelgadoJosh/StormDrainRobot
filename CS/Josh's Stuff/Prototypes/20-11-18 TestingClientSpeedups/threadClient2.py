import socket
import cv2 
import struct
import pickle
import base64
import time
# import PIL.Image as Image
import numpy as np
import threading
from queue import Queue

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


def retrieveData(data):
  # Retrieve the message data from the stream, parsing in a single bit of data
  while len(data) < payload_size:
    data += c.s.recv(4096)
  
  packed_msg_size = data[:payload_size]
  data = data[payload_size:]
  msg_size = struct.unpack("Q", packed_msg_size)[0]

  # Retrieve all the data based on the message size, in buffers of 4096
  while len(data) < msg_size:
    data += c.s.recv(4096)
  
  output_data = data[:msg_size]
  remainder_data = data[msg_size:]

  return output_data, remainder_data


def parseData(frame_data):
  frameBytes = base64.b64decode(frame_data) # If doing the raw encoded data
  img_as_np = np.frombuffer(frameBytes, dtype=np.uint8)
  frame = cv2.imdecode(img_as_np, flags=1)
  return frame

frameDataQueue = Queue(maxsize=100)
def displayVideoLoop():
  global frameDataQueue
  numFrames = 0
  startTime = time.time()
  while True:
    time.sleep(0.01)
    if frameDataQueue.empty():
      continue 

    frame_data = frameDataQueue.get()
    frame = parseData(frame_data)

    # Display
    cv2.imshow("Frame", frame)
    cv2.waitKey(1)

    numFrames += 1
    duration = time.time() - startTime 
    print(f"FPS: {numFrames/duration:.3f}")

    

data = b''
def grabVideoLoop():
  global data
  while True:
    try:
      # Retrieve message size
      frame_data, data = retrieveData(data)

      # Dump it into the queue to be displayed
      if not frameDataQueue.full():
        frameDataQueue.put(frame_data)

    except KeyboardInterrupt:
      cv2.destroyAllWindows()
      break


receive_video_loop = threading.Thread(target=grabVideoLoop)
display_video_loop = threading.Thread(target=displayVideoLoop, daemon=True)

receive_video_loop.start()
display_video_loop.start()
 
 