# Frames with Reliefs!
# J Delgado

# https://realpython.com/python-gui-tkinter/

import tkinter as tk 

# Create a dictionary:
#   keys = names of different relief effects
#   values = corresponding Tkinter objects
border_effects = {
  "flat": tk.FLAT,
  "sunken": tk.SUNKEN, 
  "raised": tk.RAISED,
  "groove": tk.GROOVE,
  "ridge": tk.RIDGE
}

window = tk.Tk() 

# Goes through each relief type in the dictionary
for relief_name, relief in border_effects.items():
  # Creates a new frame with that relief and a thick 5 borderwidth to see relief
  frame = tk.Frame(master=window, relief=relief, borderwidth=5) 
  frame.pack(side=tk.LEFT) # Left aligned
  label = tk.Label(master=frame, text=relief_name)
  label.pack() 

window.mainloop()

