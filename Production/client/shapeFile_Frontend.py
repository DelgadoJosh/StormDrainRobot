# UCF
# Senior Design
# Stormwater Drain Robot
# Team Black

# ShapeFile_FrontEnd
# This will create a GUI, and take in infor for generating a shape file

# Python 3
import tkinter as tk 
import tkinter.ttk 
import tkinter.messagebox as messagebox
from tkcalendar import DateEntry
from tkinter.filedialog import askdirectory
import datetime
import math

import shapeFile_Backend

debug = True

def feetToLatitude(feet):
  # https://www.usgs.gov/faqs/how-much-distance-does-a-degree-minute-and-second-cover-your-maps?qt-news_science_products=0#qt-news_science_products
  # At 38 degrees North Latitude:
  # 1 degree of latitude = 364,000 feet
  # http://www.csgnetwork.com/degreelenllavcalc.html
  # Since we're at 28.605 degrees north latitude
  # 1 degree of latitude = 363612.32899
  # return feet/364000.0
  # return feet/363612.32899
  # return feet/365228.16
  return feet/363000

def feetToLongitude(feet):
  # One degree of longitude = 288,200 feet
  # One degree of longitude = 320,888.48099
  # https://gis.stackexchange.com/questions/142326/calculating-longitude-length-in-miles
  # Says it's = math.cos(latitude_radians)*69.172 miles * 5280
  # https://www.thoughtco.com/degree-of-latitude-and-longitude-distance-4070616
  # Suggests 68.703 miles at equator
  # return feet/288200.0
  # return feet/320888.48099
  # return feet/325000
  return feet/350000

def create_shape_file_dialog(root, start_latitude_text=None, start_longitude_text=None, end_latitude_text=None, end_longitude_text=None, dist_in_feet=0):
  def save_file():
    try:
      # Saves the current input as a new shapefile
      nameOfFile = ent_name.get()
      if nameOfFile == "":
        messagebox.showerror("Error", "Name of this location cannot be empty")
        top.destroy()
        return
      # xs = [float(ent_x.get())]
      # ys = [float(ent_y.get())]
      x1 = float(start_longitude_text.get())
      y1 = float(start_latitude_text.get())
      x2 = float(end_longitude_text.get())
      y2 = float(end_latitude_text.get())
      dist_in_feet = float(feet_traveled_text.get())
      # try: 
      #   dist_in_feet = float(dist_in_feet)
      # except Exception as e:
      #   print(f"[ShapeFile] Exception {e}")
      #   dist_in_feet = 0
      dx = x2-x1 
      dy = y2-y1 
      mag = math.sqrt(dx*dx + dy*dy)
      dx /= mag 
      dy /= mag 
      distInLongitude = feetToLongitude(dist_in_feet)
      distInLatitude = feetToLatitude(dist_in_feet)
      dx *= distInLongitude
      dy *= distInLatitude
      x = x1 + dx 
      y = y1 + dy
      xs = [x]
      ys = [y]
      date = datetime.datetime.strptime(cal_date.get(), "%m/%d/%y").date()
      dates = [date]

      if debug:
        print(f"x1 = {x1}, y1 = {y1}, x2 = {x2}, y2 = {y2}, dist_in_feet={dist_in_feet}")
        print(f"dx = {dx}, dy = {dy}, mag = {mag}")
        print(f"distInLongitude={distInLongitude}, distInLatitude={distInLatitude}")
        print(f"final x = {x}, final y = {y}")

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
    except Exception as e:
      print(f"[ShapeFile] Exception: {e}")
      messagebox.showerror("Error", "Invalid input. \nMake sure all the longitudes and latitudes are numbers.")
      top.destroy()
      return
    top.destroy() # Clean up the window once it's done
  
  top = tk.Toplevel(root)
  top.title("Creating a shape file")

  # Creates the frame for name of the file
  lbl_name = tk.Label(top, text="Name of point:")
  ent_name = tk.Entry(top) 

  # Customizes size of the columns
  textLength = 600
  top.columnconfigure(1, minsize=textLength)
  
  # Places into grid
  lbl_name.grid(row=0, column=0, padx=5, sticky="e")
  ent_name.grid(row=0, column=1, sticky="ew")


  # Creates the row for start Latitude
  lbl_start_latitude = tk.Label(top, text="Start Latitude:")
  if start_latitude_text == None:
    start_latitude_text = tk.StringVar()
  ent_start_latitude = tk.Entry(top, textvariable=start_latitude_text) 
  
  # Places into grid
  lbl_start_latitude.grid(row=1, column=0, padx=5, sticky="e")
  ent_start_latitude.grid(row=1, column=1, sticky="ew")


  # Creates the row for start longitude
  lbl_start_longitude = tk.Label(top, text="Start Longitude:")
  if start_longitude_text == None:
    start_longitude_text = tk.StringVar()
  ent_start_longitude = tk.Entry(top, textvariable=start_longitude_text) 
  
  # Places into grid
  lbl_start_longitude.grid(row=2, column=0, padx=5, sticky="e")
  ent_start_longitude.grid(row=2, column=1, sticky="ew")


  # Creates the row for end Latitude
  lbl_end_latitude = tk.Label(top, text="End Latitude:")
  if end_latitude_text == None:
    end_latitude_text = tk.StringVar()
  ent_end_latitude = tk.Entry(top, textvariable=end_latitude_text) 
  
  # Places into grid
  lbl_end_latitude.grid(row=3, column=0, padx=5, sticky="e")
  ent_end_latitude.grid(row=3, column=1, sticky="ew")


  # Creates the row for end longitude
  lbl_end_longitude = tk.Label(top, text="End Longitude:")
  if end_longitude_text == None:
    end_longitude_text = tk.StringVar()
  ent_end_longitude = tk.Entry(top, textvariable=end_longitude_text) 
  
  # Places into grid
  lbl_end_longitude.grid(row=4, column=0, padx=5, sticky="e")
  ent_end_longitude.grid(row=4, column=1, sticky="ew")


  # Creates the row for feet traveled
  lbl_feet_traveled = tk.Label(top, text="Feet Traveled:")
  feet_traveled_text = tk.StringVar()
  feet_traveled_text.set(dist_in_feet)
  ent_feet_traveled = tk.Entry(top, textvariable=feet_traveled_text)

  lbl_feet_traveled.grid(row=5, column=0, padx=5, sticky="e")
  ent_feet_traveled.grid(row=5, column=1, sticky="ew")


  # Creates the frame for date
  lbl_date = tk.Label(top, text="Date:")
  cal_date = DateEntry(top, width=12, background="darkblue",
                      foreground="white", borderwidth=2, firstweekday="sunday")
  
  # Places into the grid
  lbl_date.grid(row=6, column=0, padx=5, sticky="e")
  cal_date.grid(row=6, column=1, sticky="w")


  # Creates the final row of save as
  frm_buttons = tk.Frame(top) 
  btn_saveas = tk.Button(frm_buttons, text="Save As...", command=save_file)
  
  numButtons = 1
  btn_saveas.grid(row=0, column=numButtons-1, sticky="e", padx=5, pady=5)
  
  frm_buttons.grid(row=7, column=1, sticky="ew")


if __name__ == '__main__':
  # Dummy file for testing.
  # Opens up a window
  root = tk.Tk() 

  lbl_dud = tk.Label(text="UCF Team Black.\nPlaceholder GUI goes here", 
    width=50, height=20, fg="white", bg="black")
  lbl_dud.pack()

  btn_test = tk.Button(text="Create Shape File", command=create_shape_file_dialog)
  btn_test.pack() 

  root.mainloop()