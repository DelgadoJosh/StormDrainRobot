# UCF Stormdrain Robot 2020 - Team Black

# Client
# This should receive 

# Standard libraries
import socket 
import struct
import threading
import base64
import numpy as np
import cv2
import time
from multiprocessing import Process
from queue import Queue

# Custom Libraries
import GUI


DEBUG = False

# Note that how windows vs ubuntu calculates size can be different
# This payload size is the size of the integer used to determine the size of 
#   the data to parse
# The current network setup is you send data in the format:
#   <datasize> <data>
payload_size = struct.calcsize("Q")

class Client():
  ip_address = "10.0.0.2" # The one you're connecting to
  # ip_address = "localhost"
  port = 5000
  def __init__(self, Address=(ip_address,port)):
    self.s = socket.socket() 
    self.s.connect(Address)

  def send(self, message):
    self.s.send(message)

print("Initiating Client")
c = Client()
print("Client Connected")

# Read the queue from the GUI to grab instructions to send
queue = GUI.app.queue
stopFlag = GUI.app.programEnd
frameQueue = GUI.app.frameQueue
voltageQueue = GUI.app.voltageQueue
encoderQueue = GUI.app.encoderQueue

def retrieveData(data):
  # Retrieve the message data from the stream, parsing in a single chunk of data
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

# Loop for receiving instructions, the instructions is added to a queue from the GUI
def loopForReceivingInstructions():
    global stopFlag
    while not stopFlag:
      stopFlag = GUI.app.programEnd
      time.sleep(0.01)
      try: 
        if not queue.empty():
          command = queue.get()
          # if DEBUG:
          #   print(f"Sending {command}")
          c.send(command.encode('utf-8'))
      except:
        stopFlag = True
    print("[InstructionLoop] Ended")

# def parseFrameFromBytes(frame_data):
#   # If going the direct encode/decode to get frameBytes
#   frameBytes = base64.b64decode(frame_data) 

#   img_as_np = np.frombuffer(frameBytes, dtype=np.uint8)
#   frame = cv2.imdecode(img_as_np, flags=1)

#   return frame

def parseFrameFromBytesJpg(frame_data):
  frame = base64.b64decode(frame_data)
  return frame

# def getNumpyArray(frame_data):
#   frameBytes = base64.b64decode(frame_data)
#   img_as_np = np.frombuffer(frameBytes, dtype=np.uint8)
#   return img_as_np

frameDataQueue = Queue(maxsize=1)
npArrayQueue = Queue(maxsize=1)
def loopToParseVideoData():
  while True:
    time.sleep(0.01)
    if frameDataQueue.empty():
      continue
    
    frame_data = frameDataQueue.get()
    frame = parseFrameFromBytesJpg(frame_data)

    if not frameQueue.full():
      frameQueue.put(frame)

# def loopToDecodeData():
#   while True:
#     time.sleep(0.01)
#     if npArrayQueue.empty():
#       continue 

#     img_as_np = npArrayQueue.get()
#     frame = cv2.imdecode(img_as_np, flags=1)

#     if not frameQueue.full():
#       frameQueue.put(frame)
  
#   print("[DecodeDataLoop] Ended Successfully")


def loopToReceiveData():
  global stopFlag
  data = b''
  startTime = time.time()
  numFramesReceived = 0
  while True:
    try:
      if stopFlag:
        break

      # Currently we have a

      # Receive Frame
      frame_data, data = retrieveData(data)
      numFramesReceived += 1
      duration = time.time() - startTime
      if numFramesReceived%10 == 0:
        print(f"Frame {numFramesReceived} | FPS: {numFramesReceived/duration:.3f}")
      if not frameDataQueue.full():
        frameDataQueue.put(frame_data)

      # Receive Voltage
      voltage_data, data = retrieveData(data)
      # Due to not being able to find how to encode/decode a float as bytes,
      # this is a hacky workaround of sending the float multiplied by 100
      voltage = int.from_bytes(voltage_data, 'big') / 100.0
      if not voltageQueue.full():
        voltageQueue.put(voltage)

      # Receive Encoder data
      encoder_data, data = retrieveData(data)
      encoder = int.from_bytes(encoder_data, 'big')
      if not encoderQueue.full():
        encoderQueue.put(encoder)

      time.sleep(0.005)
    except:
      break
  
  print("[RecieveDataLoop] Ended Safely")

if __name__ == '__main__':
  input_thread = threading.Thread(target=getInput, daemon=True)
  data_thread = threading.Thread(target=loopToReceiveData, daemon=True)
  parse_video_data_thread = threading.Thread(target=loopToParseVideoData, daemon=True)

  input_thread.start()
  data_thread.start()
  parse_video_data_thread.start()
