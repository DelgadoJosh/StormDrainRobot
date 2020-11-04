# Copied from Will's protoype
import numpy as np
import cv2
import tkinter as tk
from PIL import Image, ImageTk
from datetime import datetime
import shapeFile_Frontend

#Set up GUI
window = tk.Tk()  #Makes main window
# window.geometry("1800x1000")
window.geometry("1700x750")
window.wm_title("Senior Design")
window.configure(bg="gray17")
#window.config(background="#FFFFFF")

# Must be defined above Graphics window
def screenshot():
    now = datetime.now()
    now = str(now)
    now = now.replace(" ", "__")
    now = now.replace(":", "-")
    now = now.replace(".", "__")
    now = now + '.png'
    print("Screenshot taken: "+now)
    img.save(f"./screenshots/{now}")

def testFunction():
    distance = "1000.5"
    GPS = "\n1234 Latitude, \n4567 Longitude"
    battery = "79"
    orientation = "North"
    return f"Distance: {distance} \n GPS: {GPS} \n Battery: {battery} \n Orientation: {orientation}"

#Graphics window
imageFrame = tk.Frame(window, width=1280, height=720)
imageFrame.grid(row=1, column=0, columnspan = 5, rowspan = 5, padx=10, pady=10)

tk_object_height = '2' #'5'
tk_object_width = '30'

button_bg_color='gray30' # "darkgray"
b1 = tk.Button(window, text="Export .Shape File", bg=button_bg_color, height=tk_object_height, width=tk_object_width, font=("Helvetica", 16), command=shapeFile_Frontend.create_shape_file_dialog)
b2 = tk.Button(window, text="Quit", bg=button_bg_color, height=tk_object_height, width=tk_object_width, command=quit, font=("Helvetica", 16))
b3 = tk.Button(window, text="Screenshot", bg=button_bg_color, height=tk_object_height, width=tk_object_width, command=screenshot, font=("Helvetica", 16))
# b4 = tk.Button(window, text="", bg='gray', height=tk_object_height, width=tk_object_width, font=("Helvetica", 16))
data = tk.Label(window, bg='gray30', height=21, width=tk_object_width, text=testFunction(), font=("Helvetica", 16)) #anchor="w"
data.grid(row=1, column=6)
b1.grid(row=2, column=6)
# b4.grid(row=2, column=6)
b3.grid(row=3, column=6)
b2.grid(row=4, column=6)

# Based off of https://github.com/JetsonHacksNano/CSI-Camera/blob/master/simple_camera.py
# This returns a GStreamer pipeline for capturing from the CSI camera
# Defaults to 1280x720 @ 60fps
# Flip the image by setting the flip_method (most common values of 0 and 2)
# display_width and display_height determine the size of the window on the screen

def gstreamer_pipeline(
    capture_width=1280,
    capture_height=720,
    display_width=1280,
    display_height=720,
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



#   Capture video frames
lmain = tk.Label(imageFrame)
lmain.grid(row=0, column=0)
cap = cv2.VideoCapture(0)
#cap = cv2.VideoCapture(gstreamer_pipeline(flip_method=2), cv2.CAP_GSTREAMER)
# Set to 1280x720
cap.set(3, 1280)
cap.set(4, 720)

# Output Video, file type can be changed in future
fourcc = cv2.VideoWriter_fourcc(*'XVID')
out = cv2.VideoWriter('./videos/output.avi', fourcc, 20.0, (1280, 720))

# Init img for screenshot function
img = None

def show_frame():
    _, frame = cap.read()
    frame = cv2.flip(frame, 1)
    cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    # set img to global to capture in screenshot function
    global img
    #img = Image.fromarray(cv2image)
    height, width, layers = cv2image.shape
    resize = cv2.resize(cv2image, (1280, 720))
    img = Image.fromarray(resize)
    imgtk = ImageTk.PhotoImage(image=img)
    # Saves video to directory, unsure as why it is sped up
    # more likely an issue with lmain.after(1, show_frame) not sure how to fix
    # RECORD
    out.write(frame)
    lmain.imgtk = imgtk
    lmain.configure(image=imgtk)
    lmain.after(1, show_frame) 
    



#Slider window (slider controls stage position)
# sliderFrame = tk.Frame(window, width=600, height=100)
# sliderFrame.grid(row = 600, column=0, padx=10, pady=2)


show_frame()  #Display 2
window.mainloop()  #Starts GUI
