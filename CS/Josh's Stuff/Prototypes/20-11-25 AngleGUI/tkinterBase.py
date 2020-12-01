# Attempting to create a motorGUI
# J Delgado

# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Multithreading is great

# Note that padding is measured in pixels, *not* text units.

import tkinter as tk 
import threading
import time

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

  def run(self):
    window = tk.Tk() 
    window.title("Test")
    self.root = window
    self.root.protocol("WM_DELETE_WINDOW", self.callback)



    self.root.mainloop()



# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Begins the loop on a separate thread
app = App()
