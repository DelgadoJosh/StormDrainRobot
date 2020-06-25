# Working with Widgets
# J Delgado

# https://realpython.com/python-gui-tkinter/

# Multiple types of widgets:
# Label: Display text
# Button: Can contain text & do action when clicked
# Entry: Text entry with only a single line of text
# Text: Text entry with multiple lines (Text box)
# Frame: Rectangular region to group related widgets/provide padding btw widgets

import tkinter as tk 

# Create a window to throw widgets into

window = tk.Tk()


# === LABELS ===

label = tk.Label(
  text="Hello, Tkinter",
  foreground="white", # Set the text color to white
  background="black"  # Set the background color to black
)
label.pack() # Adds it to the window.

# Other colors: red, orange, yellow, green, blue, purple, etc.
# Many HTML color names work as well
# http://www.science.smith.edu/dftwiki/index.php/Color_Charts_for_TKinter

labelWithShortIds = tk.Label(
  text="Hello, I'm lazy and like short tags",
  fg="white",  # Short for foreground
  bg="black"   # Short for background
)
labelWithShortIds.pack()

# Mess with  the size too!
labelWithCustomSize = tk.Label(
  text="Look at my size!",
  fg="white",
  bg="black",
  width=50,  # Measured in "text units". Horizontal = width of "0"
  height=10  # Measured in "text units". Vertical = height of "0"
)
labelWithCustomSize.pack()

# Note that width != height unit size. 
labelThatsNotSquareEvenThoughItHasSameDimensions = tk.Label(
  text="I'm not a square! :(",
  fg="white",
  bg="black",
  width=20,
  height=20 
)
labelThatsNotSquareEvenThoughItHasSameDimensions.pack()



# Run the program
window.mainloop()

