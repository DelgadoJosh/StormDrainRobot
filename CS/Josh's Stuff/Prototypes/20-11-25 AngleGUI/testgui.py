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
    time.sleep(0.2) # To let the loop close
    self.root.quit()
  
  lmain = None
  def run(self):
    window = tk.Tk() 
    window.title("Bearing Test")
    self.root = window
    self.root.protocol("WM_DELETE_WINDOW", self.callback)

    # https://pythonbasics.org/tkinter-canvas/#:~:text=A%20tkinter%20canvas%20can%20be,ovals%2C%20polygons%2C%20and%20rectangles.
    canvas = tk.Canvas(self.root, bg="white", height=400, width=300)
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
    image = canvas.create_image(0, 0, image=imagetk, anchor='nw', tags="IMG")
    # label = tk.Label(image=imagetk) 
    # label.grid(row=1, column=0)

    canvas.grid(row=0, column=0) 

    self.root.mainloop()



# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Begins the loop on a separate thread
app = App()
