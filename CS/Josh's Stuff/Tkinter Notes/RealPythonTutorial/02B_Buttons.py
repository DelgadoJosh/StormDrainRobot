# Buttons
# J Delgado

# https://realpython.com/python-gui-tkinter/

import tkinter as tk 

# Open a window to put stuff into
window = tk.Tk() 

# === LABELS ===

helloWorldLabel = tk.Label(
  text="Hello world!",
  fg = "White",
  bg = "Black"
)
helloWorldLabel.pack()



# === BUTTONS ===

button = tk.Button(
  text = "Click me!",
  width = 25,
  height = 5,
  bg = "blue",
  fg = "yellow"
)
button.pack()


# Start application
window.mainloop()

