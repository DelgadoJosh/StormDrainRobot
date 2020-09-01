# Grid offset
# Grid, but you can attach to n, w, s, e, or any combo of them
# J Delgado

# https://realpython.com/python-gui-tkinter/

import tkinter as tk 

window = tk.Tk() 
window.columnconfigure(0, minsize=250)
window.rowconfigure([0, 1], minsize=100)

# Note that this will make the size of the widget just big enough
# to contain any text or other contents inside of it.
# It won't fill the entire grid cell.
label1 = tk.Label(text="A")
label1.grid(row=0, column=0, sticky="n") # Note caps doesn't matter.

label1B = tk.Label(text="NE") 
label1B.grid(row=0, column=0, sticky="NE") # Can have multiple in one cell

label2 = tk.Label(text="B") 
label2.grid(row=1, column=0, sticky="sw") # Combos work too!

window.mainloop()
