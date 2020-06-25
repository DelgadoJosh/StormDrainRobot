# Hello world!
# J Delgado

# To run this:
# 1: Open Terminal
# 2: CD to the correct directory in terminal
# 3: Run the script: "python 01_HelloWorld.py"

# Uses this tutorial:
# https://realpython.com/python-gui-tkinter/


import tkinter as tk 

# Create an application window
window = tk.Tk() 

# Create a Label that reads "Hello, Tkinter"
greetingLabel = tk.Label(text="Hello, Tkinter")
greetingLabel.pack() # Add it to the window

# Start the program
window.mainloop()

# To close the program
# window.destroy()
