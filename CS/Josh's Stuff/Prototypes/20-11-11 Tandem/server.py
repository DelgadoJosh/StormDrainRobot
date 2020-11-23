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
import struct
import json 
import base64
import threading
from multiprocessing import Process # Actually use multiple proccessors
import lights
import utils
import time
import motors
import servos
import adc
from queue import Queue
from datetime import datetime
# import teensy

port = 5000
ip_address = ""

class Video_Sender():
  port = 5000
  def __init__(self, Address=(ip_address, port), MaxClient=1):
    self.s = socket.socket()
    self.s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    self.s.bind(Address)
    self.s.listen(MaxClient)
  
  def WaitForConnection(self):
    self.Client, self.Adr = (self.s.accept())
    print(f"Got a connection from: {str(self.Client)}.")
  
s = Video_Sender()
print("Video Sender initialized. Waiting for connection before sending video.")
s.WaitForConnection()


# Based off of https://github.com/JetsonHacksNano/CSI-Camera/blob/master/simple_camera.py
# This returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values of 0 and 2)
# display_width and display_height determine the size of the window on the screen

# Adjsut display_width, display_height
def gstreamer_pipeline(
    # capture_width=1920,
    # capture_height=1080,
    # display_width=1920,
    # display_height=1080,
   capture_width=1280,
   capture_height=720,
    display_width=1280,
    display_height=720,
#    framerate=60,
#    flip_method=0,
    # capture_width=1280,
    # capture_height=720,
  #  display_width=320,
  #  display_height=180,
    # display_width=1000,
    # display_height=600,
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
camera = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
# camera = cv2.VideoCapture(0)  
# frameShared = None
frameQueue = Queue(maxsize=100)
stopFlag = False
frame = None 

folderName = './videos/'
date_split = str(datetime.now()).split(" ")
date = date_split[0]
timeStartedRunString = date_split[1]
timeStartedRunString = timeStartedRunString.replace('.', " ")
timeStartedRunString = timeStartedRunString.split(" ")[0]  # Throwing away the milliseconds
timeStartedRunString = timeStartedRunString.replace(":", "-")
name = date + "_" + timeStartedRunString
extension = '.mp4'
filename = folderName + name + extension 
fourcc = cv2.VideoWriter_fourcc(*'MP4V')
out = cv2.VideoWriter(filename, fourcc, 11.0, (1280, 720))

# A parallel thread
def constantlyReadVideoFeed():
    # global frameQueue
    # global stopFlag
    global frame
    print("Starting constantaly reading")
    while True:
        if stopFlag:
            return 
        print("Reading frame")
        grabbed, frame = camera.read()
        frameQueue.put(frame)
    print("Ending the video feed loop")

saveVideoFrameQueue = Queue(maxsize=10)
def loopToSaveVideo():
    startTimeSaved = time.time()
    numFramesSaved = 0
    while True:
        try: 
            time.sleep(0.01)
            if saveVideoFrameQueue.empty():
                continue
            numFramesSaved += 1
            durationSaved = time.time() - startTimeSaved 
            if numFramesSaved % 10 == 0:
                print(f"    FPS: {numFramesSaved/durationSaved:.3f}")
            frameToSave = saveVideoFrameQueue.get()
            out.write(frameToSave)
        except:
            print("[SaveVideo] Exception")
            out.release()

# Loop to send the video, frame by frame.
def broadcastVideo():
    global frame
    # global camera
    # global frameQueue
    # read_video = threading.Thread(target=constantlyReadVideoFeed, daemon=True)
    # read_video = Process(target=constantlyReadVideoFeed, daemon=True)
    # read_video.start()

    frameIndex = 0
    startTime = time.time()
    prevTime = time.time()
    while True: 
        try:
            # Grab the current frame
            # It should be updated by the looping constantlyReadVideoFeed()
            grabbed, frame = camera.read()

            if not grabbed:
                continue

            # Save the frame
            # out.write(frame)
            if not saveVideoFrameQueue.full():
                saveVideoFrameQueue.put(frame)

            # if frame == None:
            #     continue 
            # if frameQueue.qsize() == 0:
            #     time.sleep(0.01)
            #     continue 
            # frame = frameQueue.get()

            # Encode the frame as a jpg
            grabbed, buffer = cv2.imencode('.jpg', frame)

            # Convert the image as bytes encoded as a string
            data = base64.b64encode(buffer)  # What actually works

            # Send message length first
            message_size = struct.pack("L", len(data))

            # Then data
            s.Client.sendall(message_size + data)


            # Grab the voltage data
            voltage = adc.getVoltage()
            # data = voltage.to_bytes(10, 'big')
            voltage_int = int(voltage*100)
            data = voltage_int.to_bytes(10, 'big')
            message_size = struct.pack("L", len(data))
            s.Client.sendall(message_size + data)

            # Grab the rotation data
            # numRotationsRaw = teensy.readEncoder()
            # data = numRotationsRaw.to_bytes(10, 'big')
            # message_size = struct.pack("L", len(data))
            # s.Client.sendall(message_size + data)


            # Record the current time needed
            curTime = time.time()
            elapsedTime = curTime - startTime
            dTime = curTime - prevTime 
            prevTime = curTime
            if frameIndex % 10 == 0:
                print(f"Frame {frameIndex} | fps: {frameIndex/elapsedTime:.3f} | Voltage: {voltage:.3f}")
            frameIndex += 1

        
        except:
            print("[Broadcast] Exception")
            # s.s.close((ip_address, port))
            camera.release()
            out.release()
            cv2.destroyAllWindows()
            break
    
    out.release()
    print("Ending")

def awaitInput():
    # Wait for the data, print it, and send it back
    while True:
        try:
            data = s.Client.recv(1024) # Recieve the data from the client
            print(data)

            if not data:
                break

            # Use the data received
            splitData = utils.parse(utils.cleanup(str(data)))
            if splitData is not None:
                lights.setPWM(splitData[utils.LIGHTS_INDEX])
                motors.setLeftSpeed(splitData[utils.MOTOR_LEFT_INDEX])
                motors.setRightSpeed(splitData[utils.MOTOR_RIGHT_INDEX])
                servos.setHorizontalAngle(splitData[utils.SERVO_HORIZONTAL_INDEX])
                servos.setVerticalAngle(splitData[utils.SERVO_VERTICAL_INDEX])
        except: 
            print("[InputLoop] Exception")
            break

# Trying using threading
# read_video = Process(target=constantlyReadVideoFeed, daemon=True)
send_video = threading.Thread(target=broadcastVideo)
save_video = threading.Thread(target=loopToSaveVideo, daemon=True)
# get_input = threading.Thread(target=awaitInput)


# send_video = Process(target=broadcastVideo, daemon=True)
get_input = Process(target=awaitInput, daemon=True)

# read_video.start()
send_video.start()
save_video.start()
get_input.start()


# Trying using multiprocessing
# send_video = Process(target=broadcastVideo)
# get_input = Process(target=awaitInput)

# send_video.start()
# get_input.start()

