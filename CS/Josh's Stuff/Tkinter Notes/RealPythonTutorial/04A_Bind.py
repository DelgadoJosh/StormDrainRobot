# Bind
# Use .bind() to call an event handler whenever an event occurs on a widget
# J Delgado

# https://realpython.com/python-gui-tkinter/


# .bind()
#   Calls an event handler whenever an event occurs on a widget

import tkinter as tk 

window = tk.Tk() 

def handle_keypress(event):
  # Print the char associated with the key pressed
  # Note that this prints to stdout
  print(event.char) 

# Bind keypress event to handle_keypress()
window.bind("<Key>", handle_keypress) 

window.mainloop()

# Here are some common event types
# https://web.archive.org/web/20190512164300/http://infohost.nmt.edu/tcc/help/pubs/tkinter/web/event-types.html


