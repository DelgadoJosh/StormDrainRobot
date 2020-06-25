# Text Editor
# J Delgado

# https://realpython.com/python-gui-tkinter/

import tkinter as tk 
from tkinter.filedialog import askopenfilename, asksaveasfilename

def open_file():
  # Opens a file for editing

  # Pulls up the dialog box
  filepath = askopenfilename(
    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")]
  )

  # If the user closes dialog box/clicks cancel, it'll return None
  if not filepath:
    return 

  # Clears the current content of txt_edit to replace it
  txt_edit.delete("1.0", tk.END) 

  # Reads the content
  with open(filepath, "r") as input_file:
    text = input_file.read()
    # Inserts the content into the text box
    txt_edit.insert(tk.END, text)

  # Chantes the window titlebar
  window.title(f"Better than Notepad - {filepath}")


def save_file():
  # Save the current file as a new file

  # Pulls up dialog box
  filepath = asksaveasfilename(
    defaultextension="txt",
    filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")],
  )
  
  # If the user closes dialog box/clicks cancel, it'll return home
  if not filepath:
    return 
  
  with open(filepath, "w") as output_file:
    # Extracts the text from txt_edit with .get() and assigns to text
    text = txt_edit.get("1.0", tk.END) 
    # Writes text to output file
    output_file.write(text)

  # Updates title of the window
  window.title(f"Better than Notepad - {filepath}")


# Default
window = tk.Tk() 
window.title("Better than Notepad")

# rowconfigure configures how thick the row is, so it adjusts minHeight
# This allows the row to change height
window.rowconfigure(0, minsize=800, weight=1)

# This allows the width to resize, but only for the second (index=1) col
window.columnconfigure(1, minsize=800, weight=1) # MinWidth = 800

txt_edit = tk.Text(window)
frm_buttons = tk.Frame(window)
btn_open = tk.Button(frm_buttons, text="Open", command=open_file)
btn_save = tk.Button(frm_buttons, text="Save As...", command=save_file)

# Organizes where to put the buttons, and to stretch them out horizontally
# This adds padding outside the buttons.
# The top button has vertical button since it's away fro the top
btn_open.grid(row=0, column=0, sticky="ew", padx=5, pady=5)
btn_save.grid(row=1, column=0, sticky="ew", padx=5)

frm_buttons.grid(row=0, column=0, sticky="ns")
txt_edit.grid(row=0, column=1, stick="nsew")

window.mainloop()

