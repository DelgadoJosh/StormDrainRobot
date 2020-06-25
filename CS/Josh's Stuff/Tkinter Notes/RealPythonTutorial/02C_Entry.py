# Entry
# Single line text entry
# J Delgado

# https://realpython.com/python-gui-tkinter/

import tkinter as tk


# Open a window to throw some stuff into
window = tk.Tk() 


# ENTRY
entry = tk.Entry(
  fg="yellow",
  bg="blue",
  width=50
)
entry.pack()

# 3 main operations you can perform:
# .get()     retrieves text
# .delete()  deletes text
# .insert()  inserts text


# inputtedText = entry.get()


# entry.delete(0)  # Deletes the first character
# entry.delete(0, 100) # Deletes the first 100 characters.

# entry.delete(beginning, end)  # beg is INCLUSIVE,  end is NOT INCLUSIVE.


# entry.insert(0, "Python")   # Inserts 'Python' at the beginning. 
#   If you put (100, "Python") then it'll put it at the beginning
#     if there wasn't already text there


# Run the application
window.mainloop()

