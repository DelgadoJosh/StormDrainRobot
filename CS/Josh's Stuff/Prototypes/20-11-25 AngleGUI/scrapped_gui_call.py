# Attempting to create a motorGUI
# J Delgado

# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Multithreading is great

import tkinter as tk 
import threading
import time
import math
import numpy
import testgui

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
  
  slider = None 
  # Create loop to use slider to update the test gui

  def run(self):
    window = tk.Tk() 
    window.title("Bearing Test")
    self.root = window
    self.root.protocol("WM_DELETE_WINDOW", self.callback)

    self.slider = tk.Scale(from_=0, to=180, orient=tk.HORIZONTAL)

    self.root.mainloop()

    # print("Changing angle in 3 seconds")
    # time.sleep(3)
    # print("Changing angle")
    # self.changeAngle(90)



# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Begins the loop on a separate thread
app = App()
