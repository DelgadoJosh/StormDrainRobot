# Making Applications Interactive
# J Delgado

# https://realpython.com/python-gui-tkinter/


# Tkinter has an "event loop"
# Event = any action that occurs
#   ex: key or mouse button is pressed
#   Tkinter automatically adds it to the queue of events

# Conceptually, this is what happens:

"""
# Run the event loop
while true: 
  # If events_list is empty, then no events have occurred and
  #   you can skip to the next iteration of the loop
  if events_list == []:
    continue 

  # If execution reaches this point, then there is at least 1
  #   event object in events_list
  event = events_list[0]
"""



# What if we add more functionality?

"""
# Create an event handler
def handle_keypress(event): 
  # Print the character associated to the key pressed
  print(event.char)

# Run the event loop
while true: 
  if events_list == []:
    continue 
  event = events_list[0]

  # if event is a keypress event object
  if event.type == "keypress":
    # Call the keypress event handler
    handle_keypress(event)
"""


# So now let tkinter handle the event loop

import tkinter as tk 

# Create a window object
window = tk.Tk() 

# Create an event handler
def handle_keypress(event):
  # Print the character associated to the key press
  print(event.char) 

# Run the event loop
window.mainloop()

