# Grid with resizing when window resize
# J Delgado

# https://realpython.com/python-gui-tkinter/

# columnConfigure() and rowConfigure() take 3 arguments:
#   index of grid col/row you want to configure (or a list)
#   weight: How the column should respond to window resizing
#   minsize: Sets min size of the row height/col width.

import tkinter as tk 

window = tk.Tk() 

for row in range(3):
  window.columnconfigure(row, weight=1, minsize=75)
  window.rowconfigure(row, weight=1, minsize=50) 

  for col in range(0, 3):
    frame = tk.Frame(
      master=window,
      relief=tk.RAISED,
      borderwidth = 1
    )
    frame.grid(row=row, column=col, padx=5, pady=5) 

    label = tk.Label(master=frame, text=f"Row {row}\nColumn {col}")
    label.pack(padx=5, pady=5)

window.mainloop()

