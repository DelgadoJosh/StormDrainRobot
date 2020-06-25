# Frame
# Basically containers for organizing layout of other widgets
# J Delgado

# https://realpython.com/python-gui-tkinter/

import tkinter as tk 

window = tk.Tk() 

frame = tk.Frame() 

# Creates a label to pack
label = tk.Label(
  master=frame, 
  text="Applesauce"
)
label.pack()

# Make sure to call this after you fill it of stuff
frame.pack() 


frame_a = tk.Frame() 
frame_b = tk.Frame() 

label_a = tk.Label(master=frame_a, text="I'm in Frame A")
label_a.pack()

label_b = tk.Label(master=frame_b, text="I'm in Frame B")
label_b.pack() 

# By changing the order of these, you change the order of
# the frames in the windows
frame_a.pack()
frame_b.pack() 



window.mainloop()

