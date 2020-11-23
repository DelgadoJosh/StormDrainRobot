# Attempting to create a motorGUI
# J Delgado

# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Multithreading is great

# Note that padding is measured in pixels, *not* text units.

import tkinter as tk 
from queue import Queue 
import threading
import time
import cv2
from PIL import Image, ImageTk
import io
from multiprocessing import Process

try:
  from controller import Controller
  controllerConnected = True
except:
  controllerConnected = False 

class App(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.start()
  
  programEnd = False
  def callback(self):
    self.programEnd = True
    time.sleep(0.2) # To let the loop close
    # threading._shutdown()
    self.root.quit()

  # Create a concurrency-safe queue for the client to read
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

  # X, Y axes are on a 16 bit number (0-16k)
  DEAD_ZONE = 2000
  def isInDeadZone(self, lx, ly):
    return abs(lx) < self.DEAD_ZONE \
      and abs(ly) < self.DEAD_ZONE
  
  def removeDeadZone(self, val):
    if abs(val) < self.DEAD_ZONE:
      val = 0
    return val
  
  def clamp(self, val, min, max):
    try:
      val = float(val)
      if val > max:
        val = max 
      if val < min:
        val = min
      return val
    except:
      print("Invalid val")
      return val

  def clampAbsolute(self, val, max):
    # return self.clamp(val, -max, max)
    try:
      val = float(val)
      if abs(val) > max:
        if val > 0:
          val = max
        else:
          val = -max
      return val
    except:
      print("Invalid val")
      return val

  inputQueriesPerSecond = 100
  SENSITIVITY = 0.001 * 10
  SENSITIVITY_ANGLE = 0.001 * 750
  MAX_JOYSTICK = 32000
  def loopToQueryController(self):
    controller = Controller()
    inputQueryDelay = 1.0/100

    maxPower = 1.0
    INCREMENT = 0.1
    LIGHT_INCREMENT = 0.05

    horizontalAngle = 90
    verticalAngle = 45
    while True:
      # Every inpuQueryDelay, query to see 
      #  - if we increase/decrease the speed
      #  - change the servo angle
      #  - emergency stop
      time.sleep(inputQueryDelay)


      joystickLX = self.removeDeadZone(controller.getLeftJoystickX())
      joystickLY = self.removeDeadZone(controller.getLeftJoystickY())

      joystickRX = self.removeDeadZone(controller.getRightJoystickX())
      joystickRY = self.removeDeadZone(controller.getRightJoystickY())

      bPressed = controller.getBPressedAndReleased()

      leftBumperPressed = controller.getLeftBumperPressedAndReleased()
      rightBumperPressed = controller.getRightBumperPressedAndReleased()

      dPadY = controller.getDPadYState()

      if not self.getUseController():
        continue

      # If it's not in the deadzone, then we'll update
      if not self.isInDeadZone(joystickLX, joystickLY):
        # print(f"LX: {joystickLX} | LX: {joystickLY} | RX: {joystickRX} | RY: {joystickRY}")
        # changeInSpeed = 1.0*joystickLY/self.MAX_JOYSTICK * self.SENSITIVITY
        # motorLeftSpeed = float(self.getLeftMotorSpeed())
        # motorLeftSpeed += changeInSpeed
        # motorLeftSpeed = self.clampAbsolute(motorLeftSpeed, 1.0)
        # motorRightSpeed = float(self.getRightMotorSpeed())
        # motorRightSpeed += changeInSpeed
        # motorRightSpeed = self.clampAbsolute(motorRightSpeed, 1.0)

        # # print(f"Left: {motorLeftSpeed} | Right: {motorRightSpeed} | change{changeInSpeed}")

        # self.setLeftMotor(motorLeftSpeed)
        # self.setRightMotor(motorRightSpeed)

        newSpeed = 1.0*joystickLY/self.MAX_JOYSTICK
        newSpeed = self.clampAbsolute(newSpeed, maxPower)
        self.setLeftMotor(newSpeed)
        self.setRightMotor(newSpeed)
      else:
        # If in the deadzone for the joysticks, we come to a stop
        self.setLeftMotor(0)
        self.setRightMotor(0)
      
      if not self.isInDeadZone(joystickRX, joystickRY):
        changeInHorizontalAngle = 1.0*joystickRX/self.MAX_JOYSTICK * self.SENSITIVITY_ANGLE
        # servoHorizontalAngle = float(self.getServosHorizontal())
        # servoHorizontalAngle += changeInHorizontalAngle
        # servoHorizontalAngle = int(self.clamp(servoHorizontalAngle, 0, 180) + 0.5)
        horizontalAngle += changeInHorizontalAngle
        servoHorizontalAngle = int(self.clamp(horizontalAngle, 0, 180) + 0.5)

        changeInVerticalAngle = 1.0*joystickRY/self.MAX_JOYSTICK * self.SENSITIVITY_ANGLE
        # servoVerticalAngle = float(self.getServosVertical())
        # servoVerticalAngle += changeInVerticalAngle
        # servoVerticalAngle = int(self.clamp(servoVerticalAngle, 0, 90) + 0.5)
        verticalAngle += changeInVerticalAngle
        servoVerticalAngle = int(self.clamp(verticalAngle, 0, 90) + 0.5)

        # print(f"rx={joystickRX} | rx={joystickRY} | changeHoriz={changeInHorizontalAngle} | changeVert={changeInVerticalAngle}")

        self.setServosHorizontal(servoHorizontalAngle)
        self.setServosVertical(servoVerticalAngle)
      
      if bPressed:
        print("B was pressed!")
        self.emergencyStop()
      
      if leftBumperPressed:
        newMax = maxPower - INCREMENT
        newMax = self.clamp(newMax, 0, 1.0)
        maxPower = newMax
        print(f"Left Bumper pressed, new maxpower = {maxPower}")
      
      
      if rightBumperPressed:
        # print(f"right bumper pressed: maxpower = {maxPower}")
        newMax = maxPower + INCREMENT
        # print(f"  Temp: {newMax}")
        newMax = self.clamp(newMax, 0, 1.0)
        maxPower = newMax 
        # print(f"  new max: {maxPower}")
        print(f"Right bumper pressed, new maxpower = {maxPower}")

      if dPadY != 0:
        print(f"dPadY: {dPadY}")
      try: 
        lightsPower = float(self.getLights()) 
        lightsPower += dPadY * LIGHT_INCREMENT
        lightsPower = self.clamp(lightsPower, 0, 1.0)
        self.setLights(lightsPower)
      except:
        print("Lights invalid")

  motors_left_entry_text = None
  def getLeftMotorSpeed(self):
    if self.motors_left_entry_text == None:
      return "0"
    val = self.motors_left_entry_text.get()
    try: 
      val = float(val)
    except:
      val = 0
    return val
  
  def setLeftMotor(self, percentSpeed):
    if self.motors_left_entry_text == None:
      print(" Nope")
      return 
    self.motors_left_entry_text.set(str(percentSpeed))

  motors_right_entry_text = None 
  def getRightMotorSpeed(self):
    if self.motors_right_entry_text == None:
      return "0"
    val = self.motors_right_entry_text.get()
    try:
      val = float(val)
    except:
      val = 0
    return val

  def setRightMotor(self, percentSpeed):
    if self.motors_right_entry_text == None:
      return
    self.motors_right_entry_text.set(str(percentSpeed))
  

  lights_entry_text = None 
  def getLights(self):
    if self.lights_entry_text == None:
      return "0"
    return self.lights_entry_text.get()

  def setLights(self, val):
    if self.lights_entry_text == None:
      return 
    return self.lights_entry_text.set(val)

  servos_horizontal_slider = None
  def getServosHorizontal(self):
    if self.servos_horizontal_slider == None:
      return "0"
    return self.servos_horizontal_slider.get()
  
  def setServosHorizontal(self, val):
    if self.servos_horizontal_slider == None:
      return 
    try:
      val = int(val)
      self.servos_horizontal_slider.set(val)
    except:
      return

  servos_vertical_slider = None
  def getServosVertical(self):
    if self.servos_vertical_slider == None:
      return "0"
    return self.servos_vertical_slider.get()

  def setServosVertical(self, val):
    if self.servos_vertical_slider == None:
      return 
    try:
      val = int(val)
      self.servos_vertical_slider.set(val)
    except:
      return
  
  use_controller_checkbox_val = None 
  def getUseController(self):
    if self.use_controller_checkbox_val == None:
      return False 
    return self.use_controller_checkbox_val.get()

  def setUseController(self, val):
    if self.use_controller_checkbox_val == None:
      return
    self.use_controller_checkbox_val.set(val)

  def emergencyStop(self):
    self.setLeftMotor(0)
    self.setRightMotor(0)
    self.submitData()
    self.setUseController(False)


  # camera = cv2.VideoCapture(0)   # TEMP
  dTime = 0.01
  # def continuallySendData(self, checkbox, lights_entry, motors_left_entry, motors_right_entry, servos_horizontal_entry, servos_vertical_entry):
  def continuallySendData(self, checkbox):
    dTime = self.dTime
    nextTimeAvailable = time.time() + dTime
    # camera = self.camera # TEMP
    while True:
      # print(self.programEnd)
      # print("Should show new frame") #TEMP
      # _, frame = camera.read() #TEMP
      # self.showFrame(frame) #TEMP
      # time.sleep(dTime)
      if self.programEnd:
        break
      doConstantlySend = checkbox.get()
      if not doConstantlySend:
        continue
      if time.time() < nextTimeAvailable:
        continue 
      nextTimeAvailable = time.time() + dTime 

      self.submitData()
      # self.submitData(lights_entry, motors_left_entry, motors_right_entry, servos_horizontal_entry, servos_vertical_entry)
    print("Cleaned up loop")
    return

  # def submitData(self, lights_entry, motors_left_entry, motors_right_entry, servos_horizontal_entry, servos_vertical_entry):
  #   outputString = f"{lights_entry.get()} {motors_left_entry.get()} {motors_right_entry.get()} {servos_horizontal_entry.get()} {servos_vertical_entry.get()}"
  #   print(outputString)
  #   self.queue.put(outputString)

  # def submitData(self, lights_entry, servos_horizontal_entry, servos_vertical_entry):
  #   outputString = f"{lights_entry.get()} {self.getLeftMotorSpeed()} {self.getRightMotorSpeed()} {servos_horizontal_entry.get()} {servos_vertical_entry.get()}"
  #   print(outputString)
  #   self.queue.put(outputString)

  def submitData(self):
    outputString = f"{self.getLights()} {self.getLeftMotorSpeed()} {self.getRightMotorSpeed()} {self.getServosHorizontal()} {self.getServosVertical()}"
    print(outputString)
    if not self.queue.full():
      self.queue.put(outputString)

  def showFrame(self, frame):
    cv2Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    resizedImage = cv2.resize(cv2Image, (1280, 720))
    img = Image.fromarray(resizedImage)
    imgTk = ImageTk.PhotoImage(image=img)

    # Saves video to the directory
    # out.write(frame)

    # global lmain
    lmain.imgtk = imgTk
    lmain.configure(image=imgTk)
    lmain.image = imgTk
    # lmain.after(1, self.showFrame)

  voltage_label = None
  def setVoltage(self, voltage):
    if self.voltage_label == None: 
      return
    self.voltage_label["text"] = f"Voltage: {voltage:4.2f}"

  voltageQueue = Queue(maxsize=1)
  def loopToShowVoltage(self):
    while True:
      time.sleep(0.01)
      if self.voltageQueue.empty():
        continue 
      voltage = self.voltageQueue.get()
      self.setVoltage(voltage)

  fps_label = None
  def setFPS(self, fps):
    if self.fps_label == None:
      return
    self.fps_label["text"] = f"FPS: {fps:3.2f}"

  # Function to parse a frame into an image and imgtk
  def parseFrame(self, frame):
    cv2Image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
    resizedImage = cv2.resize(cv2Image, (1280, 720))
    img = Image.fromarray(resizedImage)
    imgTk = ImageTk.PhotoImage(image=img)
    return img, imgTk

  def parseFrameJpg(self, frame):
    img = Image.open(io.BytesIO(frame))

    # From bytes: mode, size, data, decodername
    # img = Image.frombytes('jpg', (1280, 720), frame, 'raw')
    imgTk = ImageTk.PhotoImage(img)
    return imgTk


  startTime = 0
  numFrames = 0
  curFrame = None
  frameQueue = Queue(maxsize=1)
  imgQueue = Queue(maxsize=2)
  imgTkQueue = Queue(maxsize=1)
  videoMaxFramerate = 60
  frameRefreshDelay = int(1 / videoMaxFramerate)
  def loopToEncodeImg(self):
    while True:
      if not self.frameQueue.empty():
        frame = self.frameQueue.get() 
        img = Image.open(io.BytesIO(frame)) 

        if not self.imgQueue.full():
          self.imgQueue.put(img)
          # print("                                                   AddingImg")
        # else:
        #   print("                                                          FullImg")
      else:
        time.sleep(0.01)

  def loopToTkImg(self):
    while True:
      if not self.imgQueue.empty():
        img = self.imgQueue.get()
        imgTk = ImageTk.PhotoImage(img)

        if not self.imgTkQueue.full():
          self.imgTkQueue.put(imgTk)
        #   print("                                                                         AddingImgTk")
        # else:
        #   print("                                                                                   FullImgTk")
      else:
        time.sleep(0.01)

  def loopToRefreshImage(self):
    while True:
      if not self.imgTkQueue.empty():
        imgTk = self.imgTkQueue.get()

        # Update the image
        self.lmain.imgtk = imgTk 
        self.lmain.configure(image=imgTk) 
        self.lmain.image = imgTk  
        # https://effbot.org/tkinterbook/photoimage.htm
        # Although the .image = imgTk seems redundant, it's necessary
        # To avoid it being cleared due to garbage collection

        # Update the framerate
        self.numFrames += 1
        duration = time.time() - self.startTime 
        self.setFPS(self.numFrames/duration)
      else:
        time.sleep(self.frameRefreshDelay)


  # Thread to grab the video frame
  def refreshFrame(self):
    while True:
      if not self.frameQueue.empty():
        # Then we update the cur frame
        self.curFrame = self.frameQueue.get()
        # duration = time.time() - self.startTime
        # print(f"Frame {self.numFrames} | fps: {self.numFrames/duration:.3f} | type: {type(self.curFrame)}")

      # if self.frameQueue.full():
      #   # Then we empty out a few frames to improve latency
      #   for i in range(10):
      #     _ = self.frameQueue.get()

      if self.curFrame is not None:
        # Parse the image
        # img, imgTk = self.parseFrame(self.curFrame)
        imgTk = self.parseFrameJpg(self.curFrame)

        # Update the image
        self.lmain.imgtk = imgTk 
        self.lmain.configure(image=imgTk) 
        self.lmain.image = imgTk 
        
        # Update the framerate
        self.numFrames += 1
        duration = time.time() - self.startTime 
        self.setFPS(self.numFrames/duration) 

        self.curFrame = None
      else: 
        # Prevent spam on the thread by waiting
        time.sleep(self.frameRefreshDelay)

      

  
  lmain = None
  def run(self):
    window = tk.Tk() 
    self.root = window
    self.root.protocol("WM_DELETE_WINDOW", self.callback)

    ids = self.ids 
    vals = self.vals 
    self.startTime = time.time()


    # Going to just manually define every part
    lights_label = tk.Label(text="Lights %")
    lights_label.grid(row=0, column=0)
    self.lights_entry_text = tk.StringVar(value="0")
    self.lights_entry = tk.Entry(width=20, textvariable=self.lights_entry_text)
    self.lights_entry.grid(row=1, column=0, padx=2)

    self.motors_left_entry_text = tk.StringVar(value="0")
    motors_left_label = tk.Label(text="Left Motor %")
    motors_left_label.grid(row=0, column=1)
    motors_left_entry = tk.Entry(width=20, textvariable=self.motors_left_entry_text)
    motors_left_entry.grid(row=1, column=1, padx=2)
    motors_right_label = tk.Label(text="Right Motor %")
    motors_right_label.grid(row=0, column=2)
    self.motors_right_entry_text = tk.StringVar(value="0")
    motors_right_entry = tk.Entry(width=20, textvariable=self.motors_right_entry_text)
    motors_right_entry.grid(row=1, column=2, padx=2)

    servos_horizontal_label = tk.Label(text="Horizontal\n Camera Angle")
    servos_horizontal_label.grid(row=0, column=3)
    servos_horizontal_entry = tk.Entry(width=20)
    # servos_horizontal_entry.grid(row=1, column=3, padx=2) 
    self.servos_horizontal_slider = tk.Scale(from_=0, to=180, orient=tk.HORIZONTAL) # Can optionally set tickInterval=10, length=something
    self.servos_horizontal_slider.set(90)
    self.servos_horizontal_slider.grid(row=1, column=3, padx=2)
    servos_vertical_label = tk.Label(text="Vertical\n Camera Angle")
    servos_vertical_label.grid(row=0, column=4)
    servos_vertical_entry = tk.Entry(width=20)
    # servos_vertical_entry.grid(row=1, column=4, padx=2)
    self.servos_vertical_slider = tk.Scale(from_=0, to=90, orient=tk.HORIZONTAL)
    self.servos_vertical_slider.set(45)
    self.servos_vertical_slider.grid(row=1, column=4, padx=2)

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
      command = self.submitData
      # command = lambda
      #   # lights_entry=lights_entry,
      #   # motors_left_entry=motors_left_entry,
      #   # motors_right_entry=motors_right_entry,
      #   # # servos_horizontal_entry=servos_horizontal_entry,
      #   # # servos_vertical_entry=servos_vertical_entry:
      #   # servos_horizontal_entry=servos_horizontal_slider,
      #   # servos_vertical_entry=servos_vertical_slider:
      #     self.submitData(
      #       # lights_entry,
      #       # motors_left_entry,
      #       # motors_right_entry,
      #       # servos_horizontal_entry,
      #       # servos_vertical_entry
      #     )
    )
    submit_data_button.grid(row=1, column=5)

    emergency_stop_button = tk.Button(
      text="STOP MOTORS",
      command = self.emergencyStop,
      background = 'red'
    )
    emergency_stop_button.grid(row=0, column=5)

    # Todo: Add a checkbox for constantly send the data every x seconds
    checkbox_frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=2)
    checkbox_frame.grid(row=1, column=6)
    constantly_submit_checkbox_val = tk.IntVar()
    constantly_submit_checkbox = tk.Checkbutton(checkbox_frame, text="Constantly Submit", variable=constantly_submit_checkbox_val)
    # constantly_submit_checkbox.grid(row=1, column=6)
    constantly_submit_checkbox.grid(row=0, column=0)
    self.use_controller_checkbox_val = tk.IntVar()
    use_controller_checkbox = tk.Checkbutton(checkbox_frame, text="Use Controller", variable=self.use_controller_checkbox_val)
    use_controller_checkbox.grid(row=1, column=0)

    # Add a box for data
    data_frame = tk.Frame(self.root, relief=tk.RAISED, borderwidth=2)
    data_frame.grid(row=0, column=7, rowspan=2, padx=2)
    # Populate the box with data
    self.fps_label = tk.Label(data_frame, text="FPS: 0")
    self.fps_label.grid(row=0, column=0)
    self.voltage_label = tk.Label(data_frame, text="Voltage: 0")
    self.voltage_label.grid(row=1, column=0)

    # Threads to refresh the data
    voltage_data_loop = threading.Thread(
      target=self.loopToShowVoltage,
      daemon=True
    )
    voltage_data_loop.start()

    # Start a thread so it'll keep on sending every dTime interval if the checkbox is checked
    send_data_loop = threading.Thread(
      target=self.continuallySendData, 
      args=(
        constantly_submit_checkbox_val, 
        # lights_entry,
        # motors_left_entry,
        # motors_right_entry,
        # # servos_horizontal_entry,
        # # servos_vertical_entry
        # servos_horizontal_slider,
        # servos_vertical_slider
      ),
      daemon=True,) 
    send_data_loop.start()

    # Todo: Add a image for the info
    imageFrame = tk.Frame(width=1280, height=720)
    imageFrame.grid(row=2, column=0, columnspan=8)
    
    # Capture video frames
    self.lmain = tk.Label(imageFrame)
    self.lmain.grid(row=0, column=0)
    # Start thread to refresh the video frame
    # refresh_frame_loop = threading.Thread(
    #   target=self.refreshFrame,
    #   daemon=True
    # )
    # refresh_frame_loop.start()

    encode_image_loop = threading.Thread(
      target=self.loopToEncodeImg,
      daemon=True
    )
    encode_image_loop.start()

    imageTk_loop = threading.Thread(
      target=self.loopToTkImg,
      daemon=True
    )
    # imageTk_loop = Process(
    #   target=self.loopToTkImg,
    #   daemon=True,
    #   args=(self,),
    # )
    imageTk_loop.start()

    display_loop = threading.Thread(
      target=self.loopToRefreshImage,
      daemon=True
    )
    display_loop.start()

    # # Output Video, file type can be changed in future
    # fourcc = cv2.VideoWriter_fourcc(*'XVID')
    # out = cv2.VideoWriter('./videos/output.avi', fourcc, 20.0, (1280, 720))

    # # Init img for screenshot function
    # img = None

    # Begin loop for querying the controller
    if controllerConnected:
      controller_loop = threading.Thread(
        target=self.loopToQueryController,
        daemon=True
      )
      controller_loop.start()

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

# def init():
#   app = App()
#   print("GUI has begun")

# def getApp():
#   app = App()
#   print("GUI has begun")
#   return app

