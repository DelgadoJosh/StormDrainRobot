# https://maker.pro/nvidia-jetson/tutorial/streaming-real-time-video-from-rpi-camera-to-browser-on-jetson-nano-with-flask

import cv2 
import time 
import threading 
from flask import Response, Flask 

# IMage frame sent to the Flask object
global video_frame 
video_frame = None 

# Use locks for thread-safe viewing of frames in multiple browsers
global thread_lock
thread_lock = threading.Lock() 

# GStreamer Pipeline to access the Raspberry Pi camera
GSTREAMER_PIPELINE = 'nvarguscamerasrc ! video/x-raw(memory:NVMM), width=3280, height=2464, format=(string)NV12, framerate=21/1 ! nvvidconv flip-method=0 ! video/x-raw, width=960, height=616, format=(string)BGRx ! videoconvert ! video/x-raw, format=(string)BGR ! appsink wait-on-eos=false max-buffers=1 drop=True'

# Create the Flask object for the application
app = Flask(__name__)

def captureFrames():
  global video_frame, thread_lock 

  # Video capturing from OpenCV
  # video_capture = cv2.VideoCapture(GSTREAMER_PIPELINE, cv2.CAP_GSTREAMER)
  video_capture = cv2.VideoCapture(0) # 4 = usb camera, I think

  while True and video_capture.isOpened():
    return_key, frame = video_capture.read()
    if not return_key:
      break

    # Create a copy of the frame and store it in the global variable
    with thread_lock:
      video_frame = frame.copy()
    
    key = cv2.waitKey(30) & 0xff
    if key == 27:
      break

  video_capture.release() # Once done with the loop
  
def encodeFrame():
  global thread_lock 
  while True:
    # Acquire thread_lock to access the global video_frame object
    with thread_lock:
      global video_frame 
      if video_frame is None:
        continue 
        
      return_key, encoded_image = cv2.imencode(".jpg", video_frame)
      if not return_key:
        continue 
    
    # Output image as a byte array
    yield(b'--frame\r\n' b'Content-type: image/jpeg\r\n\r\n' +
      bytearray(encoded_image) + b'\r\n')

@app.route("/")
def streamFrames():
  return Response(encodeFrame(), mimetype = "multipart/x-mixed-replace; boundary=frame")

# Check to see if this is the main thread of execution
if __name__ == '__main__':
  # Create a thread and attach the method that captures the image frames to it
  process_thread = threading.Thread(target=captureFrames)
  process_thread.daemon = True 

  # Start the thread
  process_thread.start() 

  # Start the Flask Web Application
  # While it can run on any feasible IP, 
  # IP=0.0.0.0 renders the web app on
  # the host machine's localhose 
  # and is discoverable by other machines on the same network
  app.run("0.0.0.0", port="8000")





