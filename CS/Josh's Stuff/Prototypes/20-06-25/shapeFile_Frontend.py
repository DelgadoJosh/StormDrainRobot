# UCF
# Senior Design
# Stormwater Drain Robot
# Team Black

# ShapeFile_FrontEnd
# This will create a GUI, and take in infor for generating a shape file

# Python 3
import tkinter as tk 
import tkinter.ttk 
from tkcalendar import DateEntry
from tkinter.filedialog import askdirectory
import datetime

import shapeFile_Backend

debug = True

def create_shape_file_dialog():
  def save_file():
    # Saves the current input as a new shapefile
    nameOfFile = ent_name.get()
    xs = [float(ent_x.get())]
    ys = [float(ent_y.get())]
    date = datetime.datetime.strptime(cal_date.get(), "%m/%d/%y").date()
    dates = [date]



    # TODO: Add check to ensure data is good
    

    # Pulls up dialog box
    filepath = askdirectory()

    if not filepath:
      return 

    if debug: 
      print(f"Filepath: {filepath}")
      print(f"nameOfFile: {nameOfFile}")
      print(f"xs: {xs}")
      print(f"ys: {ys}")
      print(f"Date: {dates}")
    
    shapeFile_Backend.create_shapefile(filepath, nameOfFile, xs, ys, dates)
  
  
  top = tk.Toplevel(root)
  top.title("Creating a shape file")

  # Creates the frame for name of the file
  lbl_name = tk.Label(top, text="Name:")
  ent_name = tk.Entry(top) 

  # Customizes size of the columns
  textLength = 600
  top.columnconfigure(1, minsize=textLength)
  
  # Places into grid
  lbl_name.grid(row=0, column=0, padx=5, sticky="e")
  ent_name.grid(row=0, column=1, sticky="ew")


  # Creates the row for x
  lbl_x = tk.Label(top, text="X:")
  ent_x = tk.Entry(top) 
  
  # Places into grid
  lbl_x.grid(row=1, column=0, padx=5, sticky="e")
  ent_x.grid(row=1, column=1, sticky="ew")


  # Creates the row for y
  lbl_y = tk.Label(top, text="Y:")
  ent_y = tk.Entry(top) 
  
  # Places into grid
  lbl_y.grid(row=2, column=0, padx=5, sticky="e")
  ent_y.grid(row=2, column=1, sticky="ew")


  # Creates the frame for date
  lbl_date = tk.Label(top, text="Date:")
  cal_date = DateEntry(top, width=12, background="darkblue",
                      foreground="white", borderwidth=2, firstweekday="sunday")
  
  # Places into the grid
  lbl_date.grid(row=3, column=0, padx=5, sticky="e")
  cal_date.grid(row=3, column=1, sticky="w")


  # Creates the final row of save as
  frm_buttons = tk.Frame(top) 
  btn_saveas = tk.Button(frm_buttons, text="Save As...", command=save_file)
  
  numButtons = 1
  btn_saveas.grid(row=0, column=numButtons-1, sticky="e", padx=5, pady=5)
  
  frm_buttons.grid(row=4, column=1, sticky="ew")





  



# Dummy file for testing.
# Opens up a window
root = tk.Tk() 

lbl_dud = tk.Label(text="UCF Team Black.\nPlaceholder GUI goes here", 
  width=50, height=20, fg="white", bg="black")
lbl_dud.pack()

btn_test = tk.Button(text="Create Shape File", command=create_shape_file_dialog)
btn_test.pack() 

root.mainloop()

