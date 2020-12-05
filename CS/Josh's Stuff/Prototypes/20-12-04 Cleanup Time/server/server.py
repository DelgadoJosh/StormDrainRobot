# UCF Stormwater Drain Robot 2020 - Team Black

# Server
# This server handles sending over the video frames and data
# And it also handles receiving instructions

import cv2 
import socket
import struct
import json 
import base64
import threading
import time
from queue import Queue
import os

# Custom Libraries
import adc
import attachment
import lights
import motors
import servos
import teensy
import utils

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

# At this point, all the custom libraries have been setup
flashLights = True
def loopToFlashLights():
    global flashLights
    while flashLights:
        lights.setPWM(0.005)
        time.sleep(0.5)
        lights.setPWM(0)
        time.sleep(0.5)
    print("[FlashLights] Ending")

# Flash Lights that setup is done
flash_lights_thread = threading.Thread(target=loopToFlashLights, daemon=True)
flash_lights_thread.start()

s = Video_Sender()
print("Video Sender initialized. Waiting for connection before sending video.")
s.WaitForConnection()
flashLights = False



# Based off of https://github.com/JetsonHacksNano/CSI-Camera/blob/master/simple_camera.py
# This returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values of 0 and 2)
# display_width and display_height determine the size of the window on the screen

# Adjust display_width, display_height
def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
    framerate=33,
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

# Loop to save the video frame by frame
# In our testing, the Jetson can save at roughly 10-12fps
frame = None 
stopFlag = False
saveVideo = True
saveVideoFrameQueue = Queue(maxsize=10)
def loopToSaveVideo():
    startTimeSaved = time.time()
    numFramesSaved = 0
    global saveVideo
    while saveVideo:
        try: 
            time.sleep(0.01)
            if saveVideoFrameQueue.empty():
                continue
            numFramesSaved += 1
            durationSaved = time.time() - startTimeSaved 
            if numFramesSaved % 10 == 0:
                print(f"    FPS: {numFramesSaved/durationSaved:.3f}")
            frameToSave = saveVideoFrameQueue.get()
            if out.isOpened():
                out.write(frameToSave)
            else:
                print("[SaveVideo] Out is not opened")
                break
        except:
            print("[SaveVideo] Exception")
    print("[SaveVideo] Ended")
    out.release()

# This is a safety loop to ensure that if the ethernet is disconnected/the laptop
# doesn't receive any data for 10 seconds, then we will safely shut down and save
# the video.
sentImage = True
def loopToCheckTimeout():
    global sentImage
    global saveVideo
    global stopFlag
    while True:
        time.sleep(10)
        if sentImage: 
            sentImage = False
        else:
            # We timed out as the other thread hasn't sent an image for 10 secs
            saveVideo = False 
            time.sleep(1)
            stopFlag = True
            break 

# Loop to send the data:
#   - Video Frames
#   - Voltage
#   - Encoder Data
# In the future, we can refactor to use a JSON wrapper, but there 
# were concerns that the overhead may slow it down significantly.
def loopToSendData():
    global frame
    global sendImage

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
            if not saveVideoFrameQueue.full():
                saveVideoFrameQueue.put(frame)

            # Encode the frame as a jpg
            grabbed, buffer = cv2.imencode('.jpg', frame)

            # Convert the image as bytes encoded as a string
            data = base64.b64encode(buffer)

            # Send message length first
            # Then data
            message_size = struct.pack("L", len(data))
            s.Client.sendall(message_size + data)

            
            # Let the timeout loop know we haven't timed out
            sendImage = True

            # Grab the voltage data
            voltage = adc.getVoltage()
            voltage_int = int(voltage*100)
            data = voltage_int.to_bytes(10, 'big')
            message_size = struct.pack("L", len(data))
            s.Client.sendall(message_size + data)

            # Grab the rotation data
            numRotationsRaw = teensy.readEncoder()
            data = numRotationsRaw.to_bytes(10, 'big')
            message_size = struct.pack("L", len(data))
            s.Client.sendall(message_size + data)


            # Record the current time needed
            curTime = time.time()
            elapsedTime = curTime - startTime
            prevTime = curTime
            if frameIndex % 10 == 0:
                print(f"Frame {frameIndex} | fps: {frameIndex/elapsedTime:.3f} | Voltage: {voltage:.3f}")
            frameIndex += 1

        
        except Exception as e:
            print(f"[Broadcast] Exception: {e}")
            break
    
    print("[Broadcast] Ending")
    camera.release()
    global saveVideo
    saveVideo = False
    time.sleep(1)
    print("[Broadcast] Ended Successfully")

# Loop to receive instructions from the Laptop
# It can either recieve instructions to:
#   - Start run, with the format NAME|date
#       - The date is necessary as the Jetson Nano does not have an accurate onboard clock
#   - Set light power %, motor speed %, servo angles, and attachment power % 
# This can be refactored to use JSON wrapper instead of the custom utils library
# but there were concerns that the JSON overhead may slow it down.
out = None
def loopToReceiveData():
    global out
    # Wait for the data, print it, and send it back
    while True:
        try:
            data = s.Client.recv(1024) # Recieve the data from the client
            # print(data)

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
                attachment.setPWM(splitData[utils.ATTACHMENT_INDEX])
            else:
                # Check if we have a command to start
                splitData = utils.parseTitle(utils.cleanup(str(data)))

                if splitData is not None:
                    # Then we start saving the stream
                    pipe_name = splitData[0]
                    name = splitData[1]

                    folderName = "/home/teamblack/Desktop/Videos"
                    folderName += "/" + pipe_name

                    # Create folder if it doesn't exist
                    if not os.path.exists(folderName):
                        os.makedirs(folderName)

                    extension = '.mp4'
                    filename = folderName + "/" + name + extension 
                    fourcc = cv2.VideoWriter_fourcc(*'MP4V')
                    out = cv2.VideoWriter(filename, fourcc, 11.0, (1280, 720))

                    global saveVideo 
                    saveVideo = True 

                    save_video = threading.Thread(target=loopToSaveVideo, daemon=True)
                    save_video.start()

        except Exception as e: 
            print(f"[InputLoop] Exception {e}")
            break
    print("[InputLoop] Ended")

# Trying using threading
send_data_loop = threading.Thread(target=loopToSendData)
get_input_loop = threading.Thread(target=loopToReceiveData)
timeout_loop = threading.Thread(target=loopToCheckTimeout, daemon=True)

send_data_loop.start()
get_input_loop.start()
timeout_loop.start()
