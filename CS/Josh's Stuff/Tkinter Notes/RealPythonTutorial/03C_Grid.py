# Grid
# J Delgado

# https://realpython.com/python-gui-tkinter/

# Creates a 3x3 grid of frames with label widgets

import tkinter as tk

window = tk.Tk() 

for row in range(3):
  for col in range(3):
    # Creates a generic frame for each part in the grid
    frame = tk.Frame(
      master=window,
      relief=tk.RAISED,
      borderwidth=1
    )
    frame.grid(row=row, column=col) # Location in the grid
    label = tk.Label(master=frame, text=f"Row {row}\nColumn {col}")
    label.pack() 

window.mainloop()

