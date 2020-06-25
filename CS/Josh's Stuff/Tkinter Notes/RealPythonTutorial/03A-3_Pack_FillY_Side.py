# Pack with FillY and Side=Left
# J Delgado

# Creates a window with vertical lines that resize to fill vertically

# https://realpython.com/python-gui-tkinter/

import tkinter as tk 

window = tk.Tk() 

frame1 = tk.Frame(master=window, width=200, height=100, bg="red")
frame1.pack(fill=tk.Y, side=tk.LEFT) 

frame2 = tk.Frame(master=window, width=100, bg="yellow")
frame2.pack(fill=tk.Y, side=tk.LEFT) 

frame3 = tk.Frame(master=window, width=50, bg="blue")
frame3.pack(fill=tk.Y, side=tk.LEFT) 

window.mainloop()
