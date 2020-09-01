# Place
# J Delgado

# https://realpython.com/python-gui-tkinter/


# Places things into the exact coordinates you choose
# Good for maps and stuff
# Not commonly used because:
#   Can be difficult to manage layout (especially with many widgets)
#   Not responsive to resized windows

import tkinter as tk

window = tk.Tk() 

frame = tk.Frame(master=window, width=150, height=150) 
frame.pack() 

label1 = tk.Label(master=frame, text="I'm at (0, 0)", bg="red")
label1.place(x=0, y=0)

label2 = tk.Label(master=frame, text="I'm at (75, 75)", bg="yellow")
label2.place(x=75, y=75)

window.mainloop()
