# ZMQ
# https://www.pyimagesearch.com/2019/04/15/live-video-streaming-over-network-with-opencv-and-imagezmq/


# Stack overflow
# https://stackoverflow.com/questions/30988033/sending-live-video-frame-over-network-in-python-opencv


# Lovely socket tutorial
# https://realpython.com/python-sockets/


import cv2 
import socket
import pickle
import struct
import json 
import base64


# Based off of https://github.com/JetsonHacksNano/CSI-Camera/blob/master/simple_camera.py
# This returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values of 0 and 2)
# display_width and display_height determine the size of the window on the screen

def gstreamer_pipeline(
#    capture_width=1280,
#    capture_height=720,
    display_width=1280,
    display_height=720,
#    framerate=60,
#    flip_method=0,
    capture_width=1280,
    capture_height=720,
#    display_width=320,
#    display_height=180,
    framerate=60,
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

grabbed, frame = camera.read()  # Grab the current frame
print(f"Type {type(frame)}")

grabbed, buffer = cv2.imencode('.jpg', frame)

# Serialize frame
# data = pickle.dumps(frame) 
# jsonData = {}
# Encodes the image as a byte, then as a string to store in a json object
# jsonData['img'] = base64.b64encode(buffer).decode("utf-8")
# Encodes the json as a string, which is then encoded into bytes
# data = json.dumps(jsonData).encode('utf-8')
data = base64.b64encode(buffer)



# PATH = "penguin.jpg"
# PATH = "/home/teamblack/Desktop/TeamBlack/Github Repo/StormDrainRobot/CS/Josh's Stuff/Prototypes/20-11-09 JSON Attempt/penguin.jpg"
# with open(PATH, mode='rb') as file:
#     img = file.read() 
# # data['img'] = base64.encodebytes(img).decode('utf-8')

# # print(json.dumps(data))
# print(type(img))

# # Convert to base64 encoding and show start of data
# jpg_as_text = base64.b64encode(img)
# print(jpg_as_text[:80])

# # Convert back to binary
# jpg_original = base64.b64decode(jpg_as_text)

img_original = base64.b64decode(data)

# Write to a file to show conversion worked

FILE_NAME = "testOutLocal.jpg"
OUT_PATH = "/home/teamblack/Desktop/TeamBlack/Github Repo/StormDrainRobot/CS/Josh's Stuff/Prototypes/20-11-09 JSON Attempt/" + FILE_NAME
with open(OUT_PATH, 'wb') as f_output:
    f_output.write(img_original)





