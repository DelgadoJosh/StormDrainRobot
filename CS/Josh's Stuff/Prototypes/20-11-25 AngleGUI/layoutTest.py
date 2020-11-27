# Attempting to create a motorGUI
# J Delgado

# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Multithreading is great

# Note that padding is measured in pixels, *not* text units.

import tkinter as tk 
import threading
import time
from PIL import Image, ImageTk
import os

DEBUG = False

class App(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.start()
  
  programEnd = False
  def onExit(self):
    self.programEnd = True
    print("Closing program")
    time.sleep(0.2) # To let the loop close
    self.root.quit()
    print("Closed")

  def doNothing(self):
    print("Doing nothing")

  def clearLayout(self):
    try:
      self.horizontal_frame.grid_remove()
      self.vertical_frame.grid_remove()
      self.image_frame.grid_remove()
    except Exception as e:
      print(f"[Clear Layout] {e}")
  
  def setLayout1(self):
    self.clearLayout()
    self.vertical_frame.grid()
    self.image_frame.grid()

  def setLayout2(self):
    self.clearLayout()
    self.horizontal_frame.grid()
    self.image_frame.grid()

  def run(self):
    self.root = tk.Tk()
    self.root.title("Test")
    self.root.protocol("WM_DELETE_WINDOW", self.onExit)
    self.root.geometry("+0+0") # Sets the location of the window

    # Menubar
    menubar = tk.Menu(self.root)

    # Create a layoutMenu
    layoutMenu = tk.Menu(menubar, tearoff=0) 
    layoutMenu.add_command(label="Default Layout", command=self.setLayout1)
    layoutMenu.add_command(label="Layout 2", command=self.setLayout2) 
    layoutMenu.add_separator()
    layoutMenu.add_command(label="Layout 3", command=self.doNothing)
    menubar.add_cascade(label="Layouts", menu=layoutMenu)

    # Rinse and repeat with other menus

    # Add menubar to the root frame
    self.root.config(menu=menubar)

    # IMAGE FRAME
    # self.image_frame = tk.Frame(self.root, width=1280, height=720)
    self.image_frame = tk.Frame(self.root, width=1000, height=720)
    self.image_frame.grid(row=1, column=0)
    defaultWallpaperFileName = os.getcwd() + "\\UCF Wallpaper.png"
    defaultWallpaper = Image.open(defaultWallpaperFileName)
    # defaultWallpaper = defaultWallpaper.resize((1280, 720), Image.ANTIALIAS)
    defaultWallpaper = defaultWallpaper.resize((16*70, 9*70), Image.ANTIALIAS)
    # defaultWallpaper = defaultWallpaper.crop((10, 0, 1100, 720))
    defaultWallpapertk = ImageTk.PhotoImage(defaultWallpaper)
    self.image_label = tk.Label(self.image_frame, image=defaultWallpapertk)
    self.image_label.grid(row=0, column=0)

    # Define one layout
    self.horizontal_frame = tk.Frame(self.root) 
    self.horizontal_frame.grid(row=0, column=0)
    lights_label = tk.Label(self.horizontal_frame, text="Lights %")
    lights_label.grid(row=0, column=0)
    self.lights_entry_text = tk.StringVar(value="0")
    self.lights_entry = tk.Entry(self.horizontal_frame, width=20, textvariable=self.lights_entry_text)
    self.lights_entry.grid(row=1, column=0, padx=2)

    self.motors_left_entry_text = tk.StringVar(value="0")
    motors_left_label = tk.Label(self.horizontal_frame, text="Left Motor %")
    motors_left_label.grid(row=0, column=1)
    motors_left_entry = tk.Entry(self.horizontal_frame, width=20, textvariable=self.motors_left_entry_text)
    motors_left_entry.grid(row=1, column=1, padx=2)
    motors_right_label = tk.Label(self.horizontal_frame, text="Right Motor %")
    motors_right_label.grid(row=0, column=2)
    self.motors_right_entry_text = tk.StringVar(value="0")
    motors_right_entry = tk.Entry(self.horizontal_frame, width=20, textvariable=self.motors_right_entry_text)
    motors_right_entry.grid(row=1, column=2, padx=2)

    # Define another layout
    self.vertical_frame = tk.Frame(self.root)
    self.vertical_frame.grid(row=1, column=1)
    lights_label_v = tk.Label(self.vertical_frame, text="Lights %")
    lights_label_v.grid(row=0, column=0)
    self.lights_entry_v = tk.Entry(self.vertical_frame, width=20, textvariable=self.lights_entry_text)
    self.lights_entry_v.grid(row=0, column=1, padx=2)

    motors_left_label_v = tk.Label(self.vertical_frame, text="Left Motor %")
    motors_left_label_v.grid(row=1, column=0)
    motors_left_entry_v = tk.Entry(self.vertical_frame, width=20, textvariable=self.motors_left_entry_text)
    motors_left_entry_v.grid(row=1, column=1, padx=2)
    motors_right_label_v = tk.Label(self.vertical_frame, text="Right Motor %")
    motors_right_label_v.grid(row=2, column=0)
    motors_right_entry_v = tk.Entry(self.vertical_frame, width=20, textvariable=self.motors_right_entry_text)
    motors_right_entry_v.grid(row=2, column=1, padx=2)
  
    # Set the default layout
    self.setLayout1()

    self.root.mainloop()



# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Begins the loop on a separate thread
app = App()
