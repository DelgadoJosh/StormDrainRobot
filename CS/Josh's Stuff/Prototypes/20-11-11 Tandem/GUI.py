# Attempting to create a motorGUI
# J Delgado

# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Multithreading is great

# Note that padding is measured in pixels, *not* text units.

import tkinter as tk 
from queue import Queue 
import threading
import time

class App(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.start()
  
  def callback(self):
    self.root.quit()
  
  queue = Queue(maxsize=1000)

  ids = ["Foward", "Reverse", "Left turn in place", "Right turn in place"]
  multipliers = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
  vals = [10, 25, 50, 75, 100]

  # def setSpeed(self, leftSpeed, rightSpeed):
  #   print(f"Changing left to {leftSpeed} and changing right to {rightSpeed}")
  #   speedString = f"{leftSpeed} {rightSpeed}"
  #   self.queue.put(speedString)


  # def handle_click(self, row, col):
  #   # print(f"The button was clicked! by {row} {col}")
  #   multipliers = self.multipliers 
  #   vals = self.vals
  #   leftSpeed = multipliers[row][0]*vals[col-1]
  #   rightSpeed = multipliers[row][1]*vals[col-1]
  #   self.setSpeed(leftSpeed, rightSpeed)
  #   # testLoop.changeSpeed(leftSpeed, rightSpeed)

  # def submitData(self, lights_percent, motor_left_percent, motor_right_percent, servo_horizontal_angle, servo_vertical_angle):
  #   outputString = f"{lights_percent} {motor_left_percent} {motor_right_percent} {servo_horizontal_angle} {servo_vertical_angle}"
  #   print(outputString)
  #   self.queue.put(outputString)

  dTime = 1
  def continuallySendData(self, lights_entry, motors_left_entry, motors_right_entry, servos_horizontal_entry, servos_vertical_entry):
    nextTimeAvailable = time.time() + dTime
    while True:
      doConstantlySend = checkbox.get()
      if not doConstantlySend:
        continue
      if time.time() < nextTimeAvailable:
        continue 
      nextTimeAvailable = time.time() + dTime 

      submitData(lights_entry, motors_left_entry, motors_right_entry, servos_horizontal_entry, servos_vertical_entry)


  def submitData(self, lights_entry, motors_left_entry, motors_right_entry, servos_horizontal_entry, servos_vertical_entry):
    outputString = f"{lights_entry.get()} {motors_left_entry.get()} {motors_right_entry.get()} {servos_horizontal_entry.get()} {servos_vertical_entry.get()}"
    print(outputString)
    self.queue.put(outputString)

  def run(self):
    window = tk.Tk() 
    self.root = window
    self.root.protocol("WM_DELETE_WINDOW", self.callback)

    ids = self.ids 
    vals = self.vals 


    # Going to just manually define every part
    lights_label = tk.Label(text="Lights %")
    lights_label.grid(row=0, column=0)
    lights_entry = tk.Entry(width=20)
    lights_entry.grid(row=1, column=0, padx=2)

    motors_left_label = tk.Label(text="Left Motor %")
    motors_left_label.grid(row=0, column=1)
    motors_left_entry = tk.Entry(width=20)
    motors_left_entry.grid(row=1, column=1, padx=2)
    motors_right_label = tk.Label(text="Right Motor %")
    motors_right_label.grid(row=0, column=2)
    motors_right_entry = tk.Entry(width=20)
    motors_right_entry.grid(row=1, column=2, padx=2)

    servos_horizontal_label = tk.Label(text="Horizontal\n Camera Angle")
    servos_horizontal_label.grid(row=0, column=3)
    servos_horizontal_entry = tk.Entry(width=20)
    servos_horizontal_entry.grid(row=1, column=3, padx=2)
    servos_vertical_label = tk.Label(text="Vertical\n Camera Angle")
    servos_vertical_label.grid(row=0, column=4)
    servos_vertical_entry = tk.Entry(width=20)
    servos_vertical_entry.grid(row=1, column=4, padx=2)

    # Ahhhhh no multiline lambdas :(
    submit_data_button = tk.Button(
      text="Submit Data",
      # command = lambda 
      #   lights_percent=lights_entry.get(), 
      #   motor_left_percent=motors_left_entry.get(), 
      #   motor_right_percent=motors_right_entry.get(), 
      #   servo_horizontal_angle=servos_horizontal_entry.get(), 
      #   servo_vertical_angle=servos_vertical_entry.get(): 
      #     self.submitData(lights_percent, 
      #       motor_left_percent, 
      #       motor_right_percent, 
      #       servo_horizontal_angle, 
      #       servo_vertical_angle)
      command = lambda
        lights_entry=lights_entry,
        motors_left_entry=motors_left_entry,
        motors_right_entry=motors_right_entry,
        servos_horizontal_entry=servos_horizontal_entry,
        servos_vertical_entry=servos_vertical_entry:
          self.submitData(
            lights_entry,
            motors_left_entry,
            motors_right_entry,
            servos_horizontal_entry,
            servos_vertical_entry
          )
    )
    submit_data_button.grid(row=1, column=5)

    # Todo: Add a checkbox for constantly send the data every x seconds
    constantly_submit_checkbox = tk.Checkbutton(text="Constantly Submit")
    constantly_submit_checkbox.grid(row=1, column=6)
    # Start a thread so it'll keep on sending every dTime interval if the checkbox is checked

    # Todo: add a place where you put the current run info (pipe start id, pipe end id)

    self.root.mainloop()

    # lights_entry.pack()
    # lights_text = lights_entry.get()



    # entry = tk.Entry(
    #   fg="yellow",
    #   bg="blue",
    #   width=50
    # )
    # entry.pack()

    # for row in range(len(ids)):
    #   nameFrame = tk.Frame(
    #     master=window,
    #     relief=tk.FLAT,
    #     borderwidth = 1
    #   )
    #   nameFrame.grid(row=row, column=0, padx=2, pady=2, sticky="w")
    #   label = tk.Label(master=nameFrame, text=f"{ids[row]}")
    #   label.pack(fill = tk.BOTH)

    #   for col in range(1, len(vals)+1):
    #     frame = tk.Frame(
    #       master=window,
    #       relief=tk.RAISED,
    #       borderwidth = 1
    #     )
    #     frame.grid(row=row, column=col, padx=2, pady=2) 
    #     # label = tk.Label(master=frame, text=f"Row {row}\nColumn {col}")
    #     # label = tk.Label(master=frame, text=f"{vals[col-1]}")
    #     # label.pack() 

    #     # https://stackoverflow.com/questions/7299955/tkinter-binding-a-function-with-arguments-to-a-widget
    #     button = tk.Button(
    #       master=frame,
    #       text = f"{vals[col-1]}",
    #       command = lambda row=row, col=col: self.handle_click(row, col)
    #       # width = 25,
    #       # height = 5,
    #       # bg = "blue",
    #       # fg = "yellow"
    #     )
        
    #     # button.bind("<Button-1>", handle_click)
    #     # <Button-1> = left click
    #     # <Button-2> = middle click
    #     # <Button-3> = right click
    #     button.pack()

    # stopButton = tk.Button(
    #   master=window,
    #   text = f"Set speed to 0",
    #   command = lambda leftSpeed=0, rightSpeed=0: self.setSpeed(leftSpeed, rightSpeed)
    # )
    # stopButton.grid(row=len(ids), column=1, columnspan=len(vals), sticky="WE")

    # # Begin the main loop
    # self.root.mainloop()



# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Begins the loop on a separate thread
# thread = threading.Thread(target=begin)
# thread.start()

app = App()

print("GUI has begun")

