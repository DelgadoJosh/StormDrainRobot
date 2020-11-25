# Attempting to create a motorGUI
# J Delgado

# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Multithreading is great

# Note that padding is measured in pixels, *not* text units.

import tkinter as tk 
import threading
import time
import math
import numpy
from PIL import Image, ImageTk

DEBUG = False

class App(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.start()
  
  programEnd = False
  def callback(self):
    self.programEnd = True
    print("Closing program")
    time.sleep(0.2) # To let the loop close
    self.root.quit()
    print("Closed")
  
  canvas = None
  left_line = None
  right_line = None
  def changeAngle(self, angle):
    if self.canvas == None: 
      return
    # Constants
    ORIGIN_X = 150 
    ORIGIN_Y = 100
    LEN = 100
    angle = math.radians(angle)
    

    ANGLE_WIDTH = math.radians(90)
    left_angle = angle + ANGLE_WIDTH/2 
    right_angle = angle - ANGLE_WIDTH/2 
    
    left_dx = math.cos(left_angle)
    left_dx = int(left_dx*LEN) 
    left_dy = math.sin(left_angle) 
    left_dy = -int(left_dy*LEN) # up is negative in canvas

    right_dx = math.cos(right_angle)
    right_dx = int(right_dx*LEN) 
    right_dy = math.sin(right_angle) 
    right_dy = -int(right_dy*LEN)

    if self.left_line != None:
      self.canvas.delete(self.left_line)

    self.left_line = self.canvas.create_line(ORIGIN_X, ORIGIN_Y, ORIGIN_X+left_dx, ORIGIN_Y+left_dy, width=5, fill="black")

    if self.right_line != None:
      self.canvas.delete(self.right_line)

    self.right_line = self.canvas.create_line(ORIGIN_X, ORIGIN_Y, ORIGIN_X+right_dx, ORIGIN_Y+right_dy, width=5, fill="black")


  def run(self):
    window = tk.Tk() 
    window.title("Bearing Test")
    self.root = window
    self.root.protocol("WM_DELETE_WINDOW", self.callback)

    # https://pythonbasics.org/tkinter-canvas/#:~:text=A%20tkinter%20canvas%20can%20be,ovals%2C%20polygons%2C%20and%20rectangles.
    self.canvas = tk.Canvas(self.root, bg="white", height=400, width=300)
    coord = 10, 10, 300, 300 
    # arc = canvas.create_arc(coord, start=0, extent=150, fill="red")
    # arc2 = canvas.create_arc(coord, start=150, extent=215, fill="green")

    filename = r"D:\Jay\Desktop\Joshs Folder\Code\Github Repos\UCF\StormDrainRobot\CS\Josh's Stuff\Prototypes\20-11-25 AngleGUI\20-11-25 Robot Top-down wire cropped.png" # 300 x 350
    filename = r"D:\Jay\Desktop\Joshs Folder\Code\Github Repos\UCF\StormDrainRobot\CS\Josh's Stuff\Prototypes\20-11-25 AngleGUI\20-11-25 Robot Top-down wire cropped 2.png" # 300 x 400
    # image = PhotoImage(file=filename)
    image = Image.open(filename)
    # image = image.resize((300, 350), Image.ANTIALIAS) # Image is originally 600x700
    image = image.resize((300, 400), Image.ANTIALIAS)
    imagetk = ImageTk.PhotoImage(image)
    # image = canvas.create_image(0, 50, image=imagetk, anchor='nw', tags="IMG")
    image = self.canvas.create_image(0, 0, image=imagetk, anchor='nw', tags="IMG")
    # label = tk.Label(image=imagetk) 
    # label.grid(row=1, column=0)

    self.canvas.grid(row=0, column=0) 

    self.root.mainloop()

    # print("Changing angle in 3 seconds")
    # time.sleep(3)
    # print("Changing angle")
    # self.changeAngle(90)



# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Begins the loop on a separate thread
app = App()
