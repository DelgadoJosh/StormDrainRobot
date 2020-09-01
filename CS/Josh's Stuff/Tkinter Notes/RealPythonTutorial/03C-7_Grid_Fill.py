# Grid fill
# This shows how you can make it stretch in the vertical or horizontal direction

# https://realpython.com/python-gui-tkinter/

import tkinter as tk 

window = tk.Tk() 

window.rowconfigure(0, minsize=50) 
window.columnconfigure([0, 1, 2, 3,], minsize=50) 

label1 = tk.Label(text="1", bg="black", fg="white") 
label2 = tk.Label(text="ew", bg="black", fg="white")
label3 = tk.Label(text="ns", bg="black", fg="white")
label4 = tk.Label(text="nsew", bg="black", fg="white")

label1.grid(row=0, column=0) 
label2.grid(row=0, column=1, sticky="ew") # Used to stretch horizontally
label3.grid(row=0, column=2, sticky="ns") # Used to stretch vertically
label4.grid(row=0, column=3, sticky="nsew") # Used to fill

window.mainloop()

