import socket 
import struct
import threading
import cv2
import time

camera = cv2.VideoCapture(0)

stopFlag = False
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
      cv2.imshow("Frame", frame)
      cv2.waitKey(1)

    except KeyboardInterrupt:
      cv2.destroyAllWindows()
      break
  
  print("Video loop end")


# input_thread = threading.Thread(target=getInput, daemon=True)
video_thread = threading.Thread(target=showVideo, daemon=True)

print("Beginning loops")
# input_thread.start()
video_thread.start()

