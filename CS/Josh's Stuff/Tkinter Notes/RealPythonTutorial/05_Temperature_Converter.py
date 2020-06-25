# Temperature Converter
# J Delgado

# https://realpython.com/python-gui-tkinter/

import tkinter as tk 

def fahrenheit_to_celsius():
  # Convert the value for Fahrenheit to Celsius 
  #   and insert the result into lbl_result
  fahrenheit = ent_temperature.get() # Grabs data from entry
  celsius = (5/9) * (float(fahrenheit) - 32)
  lbl_result["text"] = f"{round(celsius, 2)} \N{DEGREE CELSIUS}"

window = tk.Tk() 
window.title("Temperature Converter")

# The entry where you put the temperature
frm_entry = tk.Frame(master=window)
ent_temperature = tk.Entry(master=frm_entry, width=10)
lbl_temp = tk.Label(master=frm_entry, text="\N{DEGREE FAHRENHEIT}") 
  # Unicode for degree symbol with F

# Places the entry & label in the frame
ent_temperature.grid(row=0, column=0, sticky="e") # Right aligned
lbl_temp.grid(row=0, column=1, sticky="w") # Left aligned


# Button to convert, with a rightwards arrow on it
btn_convert = tk.Button( 
  master=window,
  text="\N{RIGHTWARDS BLACK ARROW}",
  command=fahrenheit_to_celsius
)

# Label that displays the result
lbl_result = tk.Label(master=window, text="\N{DEGREE CELSIUS}")

# Places the three components in a row
frm_entry.grid(row=0, column=0, padx=10)
btn_convert.grid(row=0, column=1, pady=10)
lbl_result.grid(row=0, column=2, padx=10)

window.mainloop()


