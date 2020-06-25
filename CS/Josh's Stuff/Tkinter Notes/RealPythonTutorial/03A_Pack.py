# Pack
# J Delgado

# https://realpython.com/python-gui-tkinter/


# Packing algorithm
# 1: Compute a rectangular area called a parcel
#   Exactly tall/wide enough to fit it,
#   and fills the remaining width/height with blank space
# 2: Center the widget in the parcel, 
#   unless a different location is specified

import tkinter as tk 

window = tk.Tk() 

# Creates 3 frames that have red, yellow, blue backgrounds
frame1 = tk.Frame(master=window, width=100, height=100, bg="red")
frame1.pack()

frame2 = tk.Frame(master=window, width=50, height=50, bg="yellow")
frame2.pack() 

frame3 = tk.Frame(master=window, width=25, height=25, bg="blue")
frame3.pack() 

window.mainloop()

