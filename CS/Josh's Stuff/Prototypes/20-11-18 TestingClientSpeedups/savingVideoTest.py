# ZMQ
# https://www.pyimagesearch.com/2019/04/15/live-video-streaming-over-network-with-opencv-and-imagezmq/


# Stack overflow
# https://stackoverflow.com/questions/30988033/sending-live-video-frame-over-network-in-python-opencv


# Lovely socket tutorial
# https://realpython.com/python-sockets/

# This server handles sending over the video frames and data
# And it also handles receiving instructions

import cv2 
import socket
import pickle
import threading
import time
from queue import Queue
from datetime import datetime

# Based off of https://github.com/JetsonHacksNano/CSI-Camera/blob/master/simple_camera.py
# This returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values of 0 and 2)
# display_width and display_height determine the size of the window on the screen

# Adjsut display_width, display_height
def gstreamer_pipeline(
   capture_width=1280,
   capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=30,
    flip_method=0,
):
    return (
        "nvarguscamerasrc ! "
        "video/x-raw(memory:NVMM), "
        "width=(int)%d, height=(int)%d, "
        "format=(string)NV12, framerate=(fraction)%d/1 ! "
        "nvvidconv flip-method=%d ! "
        "video/x-raw, width=(int)%d, height=(int)%d, format=(string)BGRx ! "
        "videoconvert ! "
        "video/x-raw, format=(string)BGR ! appsink"
        % (
            capture_width,
            capture_height,
            framerate,
            flip_method,
            display_width,
            display_height,
        )
    )


# Initialize camera
# camera = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)

# Note that if you use camera = cv2.VideoCapture(0)
# Then you *must* call two functions to adjust the width & height
width = 600
height = 400
camera = cv2.VideoCapture(0)
camera.set(3, width)
camera.set(4, height)

filename = './output.mp4'
fourcc = cv2.VideoWriter_fourcc(*'MP4V') # four Character Code for how to encode video
fps = 20.0 
    # FPS of the saved video. Note that regardless of the
    #   FPS it was saved at, it will play at this fps
    #   So if you're saving 10 frames per second, then 
    #     the 20fps playback will make it play at 2x speed
size = (width, height)
out = cv2.VideoWriter(filename, fourcc, fps, size)

# Function for a thread to always save the video
saveVideoFrameQueue = Queue(maxsize=5) # If maxsize is too large, latency is an issue as it processes the queue
def loopToSaveVideo():
    while True:
        time.sleep(0.01) # This is essential to prevent the CPU from spinning on the same thread
        if saveVideoFrameQueue.empty():
            continue
        print("Writing frame")
        frameToSave = saveVideoFrameQueue.get()
        out.write(frameToSave)

# Loop to send the video, frame by frame.
def loopToBroadcastVideo():
    # while True: 
    for i in range(100): # For the purposes of testing, going to close this after 100 frames
        try:
            # Grab the current frame
            # It should be updated by the looping constantlyReadVideoFeed()
            grabbed, frame = camera.read()

            if not grabbed:
                continue

            # # Save the frame
            # if not saveVideoFrameQueue.full():
            #     saveVideoFrameQueue.put(frame)

            # Then send the frame
            # "client.send(frame)"  or similar
            cv2.imshow("Frame", frame)
        
        except KeyboardInterrupt:
            camera.release()
            break
    
    print("Releasing Video Writer")
    out.release()


# Create Threads
send_video = threading.Thread(target=loopToBroadcastVideo)
save_video = threading.Thread(target=loopToSaveVideo, daemon=True) 
    # Set all but 1 to be a daemon, all daemons will close upon exit automatically

# Start threads
send_video.start()
save_video.start()
