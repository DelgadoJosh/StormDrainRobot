# Attempting to create a motorGUI
# J Delgado

# Note that padding is measured in pixels, *not* text units.

import tkinter as tk 
# import testLoop
from queue import Queue 

queue = Queue(maxsize=100)

ids = ["Foward", "Reverse", "Left turn in place", "Right turn in place"]
multipliers = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
vals = [10, 25, 50, 75, 100]


def setSpeed(leftSpeed, rightSpeed):
  print(f"Changing left to {leftSpeed} and changing right to {rightSpeed}")
  speedString = f"{leftSpeed} {rightSpeed}"
  queue.put(speedString)


def handle_click(row, col):
  # print(f"The button was clicked! by {row} {col}")
  leftSpeed = multipliers[row][0]*vals[col-1]
  rightSpeed = multipliers[row][1]*vals[col-1]
  setSpeed(leftSpeed, rightSpeed)
  # testLoop.changeSpeed(leftSpeed, rightSpeed)

window = tk.Tk() 


for row in range(len(ids)):
  nameFrame = tk.Frame(
    master=window,
    relief=tk.FLAT,
    borderwidth = 1
  )
  nameFrame.grid(row=row, column=0, padx=2, pady=2, sticky="w")
  label = tk.Label(master=nameFrame, text=f"{ids[row]}")
  label.pack(fill = tk.BOTH)

  for col in range(1, len(vals)+1):
    frame = tk.Frame(
      master=window,
      relief=tk.RAISED,
      borderwidth = 1
    )
    frame.grid(row=row, column=col, padx=2, pady=2) 
    # label = tk.Label(master=frame, text=f"Row {row}\nColumn {col}")
    # label = tk.Label(master=frame, text=f"{vals[col-1]}")
    # label.pack() 

    # https://stackoverflow.com/questions/7299955/tkinter-binding-a-function-with-arguments-to-a-widget
    button = tk.Button(
      master=frame,
      text = f"{vals[col-1]}",
      command = lambda row=row, col=col: handle_click(row, col)
      # width = 25,
      # height = 5,
      # bg = "blue",
      # fg = "yellow"
    )
    
    # button.bind("<Button-1>", handle_click)
    # <Button-1> = left click
    # <Button-2> = middle click
    # <Button-3> = right click
    button.pack()

stopButton = tk.Button(
  master=window,
  text = f"Set speed to 0",
  command = lambda leftSpeed=0, rightSpeed=0: setSpeed(leftSpeed, rightSpeed)
)
stopButton.grid(row=len(ids), column=1, columnspan=len(vals), sticky="WE")


def begin():
  window.mainloop()


# Then add the part for manual typing, and status


# Begins the loop
window.mainloop()



