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
      try: 
        if not queue.empty():
          command = queue.get()
          print(f"Sending {command}")

          c.send(command.encode('utf-8'))
      except KeyboardInterrupt:
        stopFlag = True
    print("Ended input loop")

camera = cv2.VideoCapture(0)
def showVideo():

  # Loop for showing images images
  global stopFlag
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

      # Display
      # cv2.imshow("Frame", frame)
      # cv2.waitKey(1)
      GUI.app.showFrame(frame)

    except KeyboardInterrupt:
      cv2.destroyAllWindows()
      break
  
  print("Video loop end")


# input_thread = threading.Thread(target=getInput, daemon=True)
video_thread = threading.Thread(target=showVideo, daemon=True)

# input_thread.start()
video_thread.start()

