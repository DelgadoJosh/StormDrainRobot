import socket 
import GUI
import struct
import threading
import base64
import numpy as np
import cv2
from multiprocessing import Process, Pipe
# from queue import Queue

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


# def retrieveData(data):
#   # Retrieve the message data from the stream, parsing in a single bit of data
#   while len(data) < payload_size:
#     data += c.s.recv(4096)
  
#   packed_msg_size = data[:payload_size]
#   data = data[payload_size:]
#   msg_size = struct.unpack("Q", packed_msg_size)[0]

#   # Retrieve all the data based on the message size, in buffers of 4096
#   while len(data) < msg_size:
#     data += c.s.recv(4096)
  
#   output_data = data[:msg_size]
#   remainder_data = data[msg_size:]

#   return output_data, remainder_data

# def parseFrameFromBytes(frame_data):
#   # If going the direct encode/decode to get frameBytes
#   frameBytes = base64.b64decode(frame_data) 

#   img_as_np = np.frombuffer(frameBytes, dtype=np.uint8)
#   frame = cv2.imdecode(img_as_np, flags=1)

#   return frame

# Loop for receiving input, the input is added to a queue
def getInput(stopFlag, queue):
    # stopFlag
    while not stopFlag:
      # stopFlag = GUI.app.programEnd
      try: 
        if not queue.empty():
          command = queue.get()
          print(f"Sending {command}")

          c.send(command.encode('utf-8'))
      except KeyboardInterrupt:
        break
        # stopFlag = True
    print("Ended input loop")

# stopFlag = False
def showVideo(stopFlag):
  # Loop for receiving images
  stopFlag
  data = b''
  while True:
    try:
      if stopFlag:
        return
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

      # frame_data, data = retrieveData(data)

      # time_data, data = retrieveData(data)  # Uncomment to grab time data
      # print(int.from_bytes(time_data, 'big')) # Uncomment to grab time_data

      # voltage_data, data = retrieveData(data)
      # print(f"ADC: Voltage={int.from_bytes(voltage_data, 'big') / 100.0}")

      # frame = parseFrameFromBytes(frame_data)



      # If going the direct encode/decode to get frameBytes
      frameBytes = base64.b64decode(frame_data) 

      img_as_np = np.frombuffer(frameBytes, dtype=np.uint8)
      frame = cv2.imdecode(img_as_np, flags=1)

      # Display
      # cv2.imshow("Frame", frame)
      # cv2.waitKey(1)
      GUI.app.showFrame(frame)

    except KeyboardInterrupt:
      cv2.destroyAllWindows()
      break
  
  print("Video loop end")


if __name__ == '__main__':

  print("Initiating Client")
  c = Client()
  print("Client Connected")

  # Read the queue from the GUI to grab instructions to send
  global stopFlag
  global queue
  app = GUI.getApp()
  queue = app.queue
  stopFlagSender, stopFlagReceiver = Pipe()
  stopFlagSender.send(app.programEnd)

  # input_thread = threading.Thread(target=getInput)
  # video_thread = threading.Thread(target=showVideo)

  # input_thread = Process(target=getInput, args=(stopFlagSender, gui))
  # video_thread = Process(target=showVideo, args=(stopFlagReceiver))
  input_thread = Process(target=getInput, daemon=True, args=(queue,))
  video_thread = Process(target=showVideo, daemon=True)

  input_thread.start()
  video_thread.start()
