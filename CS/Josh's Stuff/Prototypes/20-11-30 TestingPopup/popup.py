# Attempting to create a motorGUI
# J Delgado

# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Multithreading is great

# Creating a popup window
# https://stackoverflow.com/questions/41946222/how-do-i-create-a-popup-window-in-tkinter
# https://docs.python.org/3/library/tkinter.messagebox.html

import tkinter as tk 
import tkinter.messagebox
import threading
import time

DEBUG = False

class App(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.start()
  
  programEnd = False
  def callback(self):
    self.programEnd = True
    print("Closing program")
    time.sleep(0.2) # To let the loop close
    self.root.quit()
    print("Closed")

  def createPopup(self):
    title = "Popup Window"
    text = "Here's some text!"
    tk.messagebox.showinfo(title, text)

  def createError(self):
    tk.messagebox.showerror("Error", "There's an error in your boot!")

  def createWarning(self):
    tk.messagebox.showwarning("Warning Title", "Uh oh. you sure about that?")

  def run(self):
    window = tk.Tk() 
    window.title("Test")
    self.root = window
    self.root.protocol("WM_DELETE_WINDOW", self.callback)

    popupButton = tk.Button(self.root, text="Create Popup", command=self.createPopup)
    popupButton.grid(row=0, column=0)

    errorButton = tk.Button(self.root, text="Create Error", command=self.createError)
    errorButton.grid(row=1, column=0)

    warningButton = tk.Button(self.root, text="Create Warning", command=self.createWarning)
    warningButton.grid(row=2, column=0)

    self.root.mainloop()



# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Begins the loop on a separate thread
app = App()
