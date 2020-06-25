# Bind - Command & Label Update
# J Delgado

# https://realpython.com/python-gui-tkinter/

import tkinter as tk 

def increase():
  # use label_name["PropertyName"] to grab value
  value = int(lbl_value["text"])
  # Similarly, you can assign to label_name["PropertyName"]
  lbl_value["text"] = f"{value + 1}"

def decrease():
  value = int(lbl_value["text"])
  lbl_value["text"] = f"{value - 1}"

window = tk.Tk() 

window.rowconfigure(0, minsize=50, weight=1) 
window.columnconfigure([0, 1, 2], minsize=50, weight=1)

# Use command to increment 
btn_decrease = tk.Button(master=window, text="-", command=decrease)
btn_decrease.grid(row=0, column=0, sticky="nsew")

lbl_value = tk.Label(master=window, text="0")
lbl_value.grid(row=0, column=1) 

btn_increase = tk.Button(master=window, text="+", command=increase) 
btn_increase.grid(row=0, column=2, sticky="nsew")



'''
# How you get a label's text?

label = tk.Label(text="Hello")

# Retrieve a Label's text
text = label["text"]

# Set new text for the label
label["text"] = "Good bye"
'''

window.mainloop()
