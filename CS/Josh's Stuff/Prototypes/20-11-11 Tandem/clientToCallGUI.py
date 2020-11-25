import socket 
import GUI
import struct
import threading
import base64
import numpy as np
import cv2
import time
from multiprocessing import Process
from queue import Queue

DEBUG = False
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

# Loop for receiving input, the input is added to a queue
def getInput():
    global stopFlag
    while not stopFlag:
      stopFlag = GUI.app.programEnd
      time.sleep(0.01)
      try: 
        if not queue.empty():
          command = queue.get()
          if DEBUG:
            print(f"Sending {command}")

          c.send(command.encode('utf-8'))
      except KeyboardInterrupt:
        stopFlag = True
    print("Ended input loop")

def parseFrameFromBytes(frame_data):
  # If going the direct encode/decode to get frameBytes
  frameBytes = base64.b64decode(frame_data) 

  img_as_np = np.frombuffer(frameBytes, dtype=np.uint8)
  frame = cv2.imdecode(img_as_np, flags=1)

  return frame

def parseFrameFromBytesJpg(frame_data):
  frame = base64.b64decode(frame_data)
  return frame

def getNumpyArray(frame_data):
  frameBytes = base64.b64decode(frame_data)
  img_as_np = np.frombuffer(frameBytes, dtype=np.uint8)
  return img_as_np

frameDataQueue = Queue(maxsize=1)
npArrayQueue = Queue(maxsize=1)
def loopToParseData():
  while True:
    time.sleep(0.01)
    if frameDataQueue.empty():
      # print("                           Dirk")
      continue
    
    frame_data = frameDataQueue.get()
    # frame = parseFrameFromBytes(frame_data)
    frame = parseFrameFromBytesJpg(frame_data)

    if not frameQueue.full():
      frameQueue.put(frame)
    #   print("                                      Adding")
    # else:
    #   print("                                                  Full")

    # img_as_np = getNumpyArray(frame_data)

    # if not npArrayQueue.full():
    #   npArrayQueue.put(img_as_np)
    #   print("                                 Adding") 
    # else:
    #   print("                                          Full")

def loopToDecodeData():
  while True:
    time.sleep(0.01)
    if npArrayQueue.empty():
      print("                                                 Dirk")
      continue 

    img_as_np = npArrayQueue.get()
    frame = cv2.imdecode(img_as_np, flags=1)

    if not frameQueue.full():
      frameQueue.put(frame)
      print("                                                       Adding")
    else:
      print("                                                             Full")


def showVideo():
  # Loop for receiving images
  global stopFlag
  data = b''
  startTime = time.time()
  numFramesReceived = 0
  while True:
    try:
      if stopFlag:
        return
      # # Retrieve message size
      # while len(data) < payload_size:
      #   data += c.s.recv(4096)
      
      # packed_msg_size = data[:payload_size]
      # data = data[payload_size:]
      # msg_size = struct.unpack("Q", packed_msg_size)[0]

      # # Retrieve all dat based on message size
      # while len(data) < msg_size:
      #   data += c.s.recv(4096)
      
      # frame_data = data[:msg_size]
      # data = data[msg_size:]

      frame_data, data = retrieveData(data)
      numFramesReceived += 1
      duration = time.time() - startTime
      if numFramesReceived%10 == 0:
        print(f"Frame {numFramesReceived} | FPS: {numFramesReceived/duration:.3f}")
      if not frameDataQueue.full():
        frameDataQueue.put(frame_data)
        # print("  Adding to frame data queue")
      # else:
      #   print("     Frame Data Queue is Full!")


      # time_data, data = retrieveData(data)  # Uncomment to grab time data
      # print(int.from_bytes(time_data, 'big')) # Uncomment to grab time_data

      voltage_data, data = retrieveData(data)
      voltage = int.from_bytes(voltage_data, 'big') / 100.0
      # print(f"ADC: Voltage={int.from_bytes(voltage_data, 'big') / 100.0}")
      if not voltageQueue.full():
        voltageQueue.put(voltage)

      encoder_data, data = retrieveData(data)
      encoder = int.from_bytes(encoder_data, 'big')
      if not encoderQueue.full():
        encoderQueue.put(encoder)

      # Parsing data
      # frame = parseFrameFromBytes(frame_data)



      # # If going the direct encode/decode to get frameBytes
      # frameBytes = base64.b64decode(frame_data) 

      # img_as_np = np.frombuffer(frameBytes, dtype=np.uint8)
      # frame = cv2.imdecode(img_as_np, flags=1)

      # Display
      # cv2.imshow("Frame", frame)
      # cv2.waitKey(1)
      # GUI.app.showFrame(frame)
      # if not frameQueue.full():
      #   frameQueue.put(frame)

    except KeyboardInterrupt:
      cv2.destroyAllWindows()
      break
  
  print("Video loop end")

if __name__ == '__main__':
  input_thread = threading.Thread(target=getInput, daemon=True)
  video_thread = threading.Thread(target=showVideo, daemon=True)
  parse_data_thread = threading.Thread(target=loopToParseData, daemon=True)
  decode_data_loop = threading.Thread(target=loopToDecodeData, daemon=True)


  # input_thread = Process(target=getInput)
  # video_thread = Process(target=showVideo)
  # parse_data_thread = Process(target=loopToParseData, daemon=True)

  input_thread.start()
  video_thread.start()
  parse_data_thread.start()
  # decode_data_loop.start()
