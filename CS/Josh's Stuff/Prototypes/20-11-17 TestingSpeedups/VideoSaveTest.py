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

# Output Video, file type can be changed in future
# To change type: https://stackoverflow.com/questions/30509573/writing-an-mp4-video-using-python-opencv
# https://docs.opencv.org/3.4/dd/d9e/classcv_1_1VideoWriter.html
# https://www.fourcc.org/codecs.php
# https://stackoverflow.com/questions/52932157/opencv-ffmpeg-tag-0x34363268-h264-is-not-supported-with-codec/56723380
# fourcc = cv2.VideoWriter_fourcc(*'XVID')
# out = cv2.VideoWriter('./videos/output.avi', cv2.VideoWriter_fourcc(*'XVID'), 20.0, (1280, 720))
# fourcc = cv2.VideoWriter_fourcc(*'MJPG')
# out = cv2.VideoWriter('./videos/output.avi', fourcc, 20.0, (1280, 720))
fourcc = cv2.VideoWriter_fourcc(*'MP4V') # Four character code for video format
# fourcc = cv2.VideoWriter_fourcc(*'H264')
# print("before")
out = cv2.VideoWriter('./videos/output.mp4', fourcc, 20.0, (1280, 720))
# print("after")



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
camera.set(3, 1280)  # This must be set to save correctly
camera.set(4, 720)
def showVideo():

  # Loop for showing images images
  global stopFlag
  global frameQueue
  data = b''
  startTime = time.time()
  numFrames = 0
  for i in range(100):
    try:
      if stopFlag:
        return

      _, frame = camera.read()
      hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
      # out.write(hsv)
      out.write(frame)

      numFrames += 1
      duration = time.time() - startTime 
      fps = numFrames / duration 
      print(f"FPS: {fps}")

      # Simulate encoding and receiving
      # Encode the frame as a jpg
      grabbed, buffer = cv2.imencode('.jpg', frame)

      # Convert the image as bytes encoded as a string
      data = base64.b64encode(buffer)  # What actually works
      
      # Receiving data
      frame_data = data
      frameBytes = base64.b64decode(frame_data) 
      img_as_np = np.frombuffer(frameBytes, dtype=np.uint8)
      frame = cv2.imdecode(img_as_np, flags=1)

      if not frameQueue.full():
        frameQueue.put(frame)


    except KeyboardInterrupt:
      cv2.destroyAllWindows()
  
  camera.release()
  out.release()
  print("Video loop end")


# input_thread = threading.Thread(target=getInput, daemon=True)
# video_thread = threading.Thread(target=showVideo, daemon=True)

# input_thread.start()
# video_thread.start()

showVideo()

