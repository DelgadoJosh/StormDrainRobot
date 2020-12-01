import tkinter as tk 
import tkinter.ttk 
from tkcalendar import DateEntry
from tkinter.filedialog import askdirectory
import datetime

import shapeFile_Frontend

# Opens up a window
root = tk.Tk() 

lbl_dud = tk.Label(text="UCF Team Black.\nPlaceholder GUI goes here", 
  width=50, height=20, fg="white", bg="black")
lbl_dud.pack()

# Runs the command in front_end
btn_test = tk.Button(text="Create Shape File", command=shapeFile_Frontend.create_shape_file_dialog)
btn_test.pack() 

root.mainloop()
