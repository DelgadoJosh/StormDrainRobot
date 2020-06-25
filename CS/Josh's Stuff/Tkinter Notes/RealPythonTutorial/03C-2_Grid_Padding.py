# Grid with padding
# J Delgado

# https://realpython.com/python-gui-tkinter/

# Note that padding is measured in pixels, *not* text units.

import tkinter as tk 

window = tk.Tk() 

for row in range(3):
  for col in range(3):
    frame = tk.Frame(
      master=window,
      relief=tk.RAISED,
      borderwidth = 1
    )
    frame.grid(row=row, column=col, padx=5, pady=5) 
    label = tk.Label(master=frame, text=f"Row {row}\nColumn {col}")
    label.pack() 

window.mainloop()
