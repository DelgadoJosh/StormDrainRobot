import socket 
import GUI
import struct
import threading
import base64
import numpy as np
import cv2
import time
# from queue import Queue

# Read the queue from the GUI to grab instructions to send
queue = GUI.app.queue
stopFlag = GUI.app.programEnd
frameQueue = GUI.app.frameQueue

# Loop for receiving input, the input is added to a queue
def getInput():
    global stopFlag
    while not stopFlag:
      stopFlag = GUI.app.programEnd
      time.sleep(0.01)
      try: 
        if not queue.empty():
          command = queue.get()
          print(f"Sending {command}")

          # c.send(command.encode('utf-8'))
      except KeyboardInterrupt:
        stopFlag = True
    print("Ended input loop")

camera = cv2.VideoCapture(0)
def showVideo():

  # Loop for showing images images
  global stopFlag
  global frameQueue
  data = b''
  startTime = time.time()
  numFrames = 0
  while True:
    try:
      if stopFlag:
        return

      _, frame = camera.read()

      numFrames += 1
      duration = time.time() - startTime 
      fps = numFrames / duration 
      print(f"FPS: {fps}")

      # Display
      # cv2.imshow("Frame", frame)
      # cv2.waitKey(1)
      # GUI.app.showFrame(frame)

      # Simulate encoding and receiving
      # Encode the frame as a jpg
      grabbed, buffer = cv2.imencode('.jpg', frame)

      # Convert the image as bytes encoded as a string
      data = base64.b64encode(buffer)  # What actually works
      
      # Receiving data
      frame_data = data
      # img_as_np = np.frombuffer(frameBytes, dtype=np.uint8)
      # frame = cv2.imdecode(img_as_np, flags=1)

      # if not frameQueue.full():
        # frameQueue.put(frame)

      frameBytes = base64.b64decode(frame_data) 
      if not frameQueue.full():
        frameQueue.put(frameBytes)
    except KeyboardInterrupt:
      cv2.destroyAllWindows()
      break
  
  print("Video loop end")


input_thread = threading.Thread(target=getInput, daemon=True)
video_thread = threading.Thread(target=showVideo, daemon=True)

input_thread.start()
video_thread.start()

