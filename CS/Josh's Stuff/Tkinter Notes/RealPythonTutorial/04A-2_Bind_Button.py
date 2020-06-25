# Bind - Button
# Binding to a button
# J Delgado

# https://realpython.com/python-gui-tkinter/

# More event types
# https://web.archive.org/web/20190512164300/http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/event-types.html

import tkinter as tk 

window = tk.Tk()

def handle_click(event):
  print("The button was clicked!") 

button = tk.Button(text="Click me!")

button.bind("<Button-1>", handle_click)
button.pack()
# <Button-1> = left click
# <Button-2> = middle click
# <Button-3> = right click

window.mainloop()
