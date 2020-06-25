# Text
# Multi-line text entry
# J Delgado

# https://realpython.com/python-gui-tkinter/

import tkinter as tk 

# Open a window to stuff stuff into
window = tk.Tk() 



# === TEXT ===

# Text widgets
# .get()
# .delete()
# .insert()

# Create a text box
text_box = tk.Text() 
text_box.pack() 

# text_box.get(start_index, end_index)  # (]
#   However, it's not as simple as number, number.
#   A textBox index has 2 pieces of info
#     <line_number>.<character_umbre>
#     ex:
#       1.0 = first character on first line
#       2.3 = fourth character on second line
#       Line numbers are inclusive, inclusive
#       Char numbers are inlcusive, exclusive


# == GET ==
#   .get("1.0", tk.END)  # grabs all the text


# == DELETE ==
# .delete(single_char_index)
# .delete(start_index, end_index)
#   inclusive, exclusive

# Keep in mind that newline characters count as a character!


# == INSERT ==
# .insert(index, string)

# If you're trying to insert something on te second line
# Make sure to insert a "\n" at the beginning of your string
# Just like with the entry, you can't insert unless there was spacing there

# text_box.insert("2.0", "\nWorld")

# text_box.insert(tk.END, "Put me at the end!")
# text_box.insert(tk.END, "\nPut me on a new line!")



# Open the main loop
window.mainloop()

