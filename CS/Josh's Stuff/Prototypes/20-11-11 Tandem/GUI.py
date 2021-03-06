# Attempting to create a motorGUI
# J Delgado

# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Multithreading is great

# Note that padding is measured in pixels, *not* text units.

import tkinter as tk 
import tkinter.messagebox as messagebox
from queue import Queue 
import threading
import time
import cv2
from PIL import Image, ImageTk
import io
from multiprocessing import Process
import math
import numpy
import shapeFile_Frontend
import os
from datetime import datetime
import json

try:
  from controller import Controller
  controllerConnected = True
except:
  controllerConnected = False 

DEBUG = False

defaultConfig = {}
defaultConfig["Emergency Stop"] = "B" # "E"
defaultConfig["Center Angle"] = "X" # "W"
defaultConfig["Connect Controller"] = "Start"  # "SLCT" # SLCT = right menu button
defaultConfig["Show Help"] = "Select" # "STRT" # STRT = left menu button on the controller
defaultConfig["Increase Motor Max Power"] = "Right Bumper" # "TR"
defaultConfig["Decrease Motor Max Power"] = "Left Bumper" # "TL"

class App(threading.Thread):
  def __init__(self):
    threading.Thread.__init__(self)
    self.start()
  
  programEnd = False
  def callback(self):
    msgBox = messagebox.askquestion(
      "Exit Application", 
      "Are you sure you want to exit the application?", 
      icon='warning')

    if msgBox == 'yes':
      self.programEnd = True
      time.sleep(0.2) # To let the loop close
      # threading._shutdown()
      self.root.quit()
    else:
      # messagebox.showinfo('Return', 'You will now return to the application screen')
      return

  # Create a concurrency-safe queue for the client to read
  queue = Queue(maxsize=1000)

  ids = ["Foward", "Reverse", "Left turn in place", "Right turn in place"]
  multipliers = [[1, 1], [-1, -1], [-1, 1], [1, -1]]
  vals = [10, 25, 50, 75, 100]

  global defaultConfig
  filename = os.getcwd() + "/config.json"
  try:
    file_json = open(filename)
    json_text = file_json.read() 
    print(json_text)
    config = json.loads(json_text)
  except: 
    config = defaultConfig
    # Save the default config to disk

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

  def inputDataWindow(self):
    print("Input Data Run")
    self.setInputDataLayout()

  def startRun(self):
    print("Starting run")
    # TODO: Add check to ensure the data is good
    pipeName = self.getPipeName()
    if pipeName == "":
      # Empty name, send a warning
      messagebox.showerror("Blank Name Error", "Sorry, you can't have a blank pipe name. Please fill in a name.")
      return

    # Otherwise we have good data, submit it
    command = f"NAME|{pipeName}|{str(datetime.now())}"
    print(command)
    self.startTime = time.time()
    self.numFrames = 0
    self.queue.put(command)
    self.setLayoutDefault()

  def downloadVideo(self):
    print("Downloading data") 
    self.setLayoutDefault()

  help_window = None
  controllerImageTk = None
  def toggleHelpWindow(self):
    if self.help_window == None:
      self.openHelpWindow()
    else:
      self.closeHelpWindow()

  def closeHelpWindow(self):
    if self.help_window == None:
      return 
    self.help_window.destroy()
    self.help_window = None 
  
  def openHelpWindow(self):
    try:
      if self.help_window != None:
        return 
      self.help_window = tk.Toplevel()
      self.help_window.wm_title("Help")
      self.help_window.protocol("WM_DELETE_WINDOW", self.closeHelpWindow)
      controller_image_label = tk.Label(self.help_window, image=self.controllerImageTk)
      controller_image_label.grid(row=0, column=0)
    except Exception as e:
      print(f"[OpenHelpWindow] Exception: {e}")
      return

  about_window = None
  about_text = """UCF Stormwater Drain Robot

UCF Team Black 2020

Mechanical Engineers:
Andrew Davis 
Brian Hohl
Ryan Hoover 
Joshua Layland 
Everett Periman

Computer Science: 
Josh Delgado 
Ruman Rashid 
Wilfredo Vega

For view of the source code & CAD model:
https://github.com/DelgadoJosh/StormDrainRobot"""

  def openAboutWindow(self):
    try:
      if self.about_window != None:
        return 
      self.about_window = tk.Toplevel()
      self.about_window.wm_title("About")
      

      about_window_label = tk.Label(self.about_window, text=self.about_text)
      about_window_label.grid(row=0, column=0)
    except Exception as e:
      print(f"[OpenAboutWindow] Exception {e}")

  # X, Y axes are on a 16 bit number (0-16k)
  DEAD_ZONE = 3000
  def isInDeadZone(self, lx, ly):
    return abs(lx) < self.DEAD_ZONE \
      and abs(ly) < self.DEAD_ZONE
  
  def removeDeadZone(self, val):
    if abs(val) < self.DEAD_ZONE:
      val = 0
    return val
  
  def withinInterval(self, val, target, interval):
    try:
      isGood = target-interval <= val <= target+interval
      return isGood
    except: 
      return False

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

  def getConfig(self, abbv):
    try: 
      return self.config[abbv]
    except: 
      return defaultConfig[abbv]

  def getConfigController(self, abbv):
    val = self.getConfig(abbv)
    return Controller.GET_ABBV[val]



  controller_buttons = ["A", "B", "X", "Y", "Start", "Select", "Right Bumper", "Left Bumper"]
  controller_configurable = {
    "Emergency Stop", 
    "Center Angle", 
    "Connect Controller", 
    "Show Help",
    "Increase Motor Max Power",
    "Decrease Motor Max Power"}
  button_text = {}
  for name in controller_configurable:
    button_text[name] = None
  def saveConfig(self):
    for name in self.controller_configurable:
      if self.button_text[name] == None:
        continue 
      # Otherwise we save config
      self.config[name] = self.button_text[name].get()
  
    # Save to file
    json_text = json.dumps(self.config)
    # print(json_text)
    # print(json_text)
    filename = os.getcwd() + "\\" + "config.json"
    # Overwrite it
    # if os.path.exists(filename):
    #   os.remove(filename)
    json_file = open(filename, "w")
    # json.dump(self.config, json_file)
    json_file.write(json_text)
    
    # Change back to welcome screen
    self.setWelcomeLayout()

  def cancelConfig(self):
    for name in self.controller_configurable:
      print(f"{name} : {self.getConfig(name)}")
      self.button_text[name].set(self.getConfig(name))
    
    self.setWelcomeLayout()

  def restoreDefaultConfig(self):
    global defaultConfig
    for name in self.controller_configurable:
      self.button_text[name].set(defaultConfig[name])

    self.saveConfig()

  inputQueriesPerSecond = 100
  isSpeedControlEnabled = True
  isInCruiseControl = False
  SENSITIVITY = 0.001 * 10
  SENSITIVITY_HORIZONTAL_ANGLE = 0.001 * 750 * 1.5  # This is magic
  SENSITIVITY_VERTICAL_ANGLE = 0.001 * 750 * 1.5
  MAX_JOYSTICK = 32000
  horizontalAngle = 90
  verticalAngle = 45
  def loopToQueryController(self):
    controller = Controller()
    inputQueryDelay = 1.0/100

    maxPower = 0.5
    INCREMENT = 0.1
    LIGHT_INCREMENT = 0.05
    ATTACHMENT_INCREMENT = 0.05

    # This is the offset in a single direction, so the total is this doubled
    VERTICAL_ANGLE_OFFSET = math.radians(30)
    MAX_HEIGHT = 0.8 # Technically should use height
    HALFWAY_HEIGHT = MAX_HEIGHT/2

    # horizontalAngle = 90
    # verticalAngle = 45
    while True:
      # Every inputQueryDelay, query to see 
      #  - if we increase/decrease the speed
      #  - change the servo angle
      #  - emergency stop
      time.sleep(inputQueryDelay)

      # Please rename to "<action>buttonPressed" so we just change one line
      joystickLX = self.removeDeadZone(controller.getLeftJoystickX())
      joystickLY = self.removeDeadZone(controller.getLeftJoystickY())

      joystickRX = self.removeDeadZone(controller.getRightJoystickX())
      joystickRY = self.removeDeadZone(controller.getRightJoystickY())

      emergencyStopPressed = controller.getButtonPressed(self.getConfigController("Emergency Stop")) # controller.getBPressedAndReleased() # E

      centerAnglePressed = controller.getButtonPressed(self.getConfigController("Center Angle"))
      connectControllerPressed = controller.getButtonPressed(self.getConfigController("Connect Controller")) # Start = Select on the controller. idk why
      showHelpMenuPressed = controller.getButtonPressed(self.getConfigController("Show Help")) # STRT = Select button on controller

      maxSpeedDecreasePressed = controller.getButtonPressed(self.getConfigController("Decrease Motor Max Power")) # controller.getLeftBumperPressedAndReleased() # TL = left bumper
      maxSpeedIncreasePressed = controller.getButtonPressed(self.getConfigController("Increase Motor Max Power")) # controller.getRightBumperPressedAndReleased()

      # emergencyStopPressed = controller.getButtonPressed(self.getConfig("EmergencyStop")) # controller.getBPressedAndReleased() # E

      # centerAnglePressed = controller.getButtonPressed(self.getConfig("CenterAngle"))
      # connectControllerPressed = controller.getButtonPressed(self.getConfig("ConnectController")) # Start = Select on the controller. idk why
      # showHelpMenuPressed = controller.getButtonPressed(self.getConfig("ShowHelp")) # STRT = Select button on controller

      # maxSpeedDecreasePressed = controller.getButtonPressed(self.getConfig("DecreaseMotorMaxPower")) # controller.getLeftBumperPressedAndReleased() # TL = left bumper
      # maxSpeedIncreasePressed = controller.getButtonPressed(self.getConfig("IncreaseMotorMaxPower")) # controller.getRightBumperPressedAndReleased()
      
      
      # emergencyStopPressed = controller.getButtonPressed("E") # controller.getBPressedAndReleased() # E

      # centerAnglePressed = controller.getButtonPressed("W")
      # connectControllerPressed = controller.getButtonPressed("SLCT") # Start = Select on the controller. idk why
      # showHelpMenuPressed = controller.getButtonPressed("STRT") # STRT = Select button on controller

      # maxSpeedDecreasePressed = controller.getButtonPressed("TL") # controller.getLeftBumperPressedAndReleased() # TL = left bumper
      # maxSpeedIncreasePressed = controller.getButtonPressed("TR") # controller.getRightBumperPressedAndReleased()


      dPadX = controller.getDPadXState()
      dPadY = controller.getDPadYState()

      cruiseControlButtonPressed = False

      if emergencyStopPressed:
        self.emergencyStop()

      # All controls below this are disabled
      useController = self.getUseController()
      if connectControllerPressed:
        useController = not useController
        self.setUseController(useController)

      if not useController:
        continue

      # [ROBOT SPEED]
      # <LEFT STICK>
      # Only update speed if the controls are not disabled
      if self.isSpeedControlEnabled:
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
          # Relative LY and relative LX
          relX = 1.0*joystickLX/self.MAX_JOYSTICK
          relY = 1.0*joystickLY/self.MAX_JOYSTICK
          relX = self.clamp(relX, -1, 1)
          relY = self.clamp(relY, -1, 1)
          radius = math.sqrt(relX*relX + relY*relY)
          radius = self.clamp(radius, 0, 1)

          angle = numpy.arctan2(relY, relX)
          # self.setLights(angle)

          # If going directly up/directly down within VERTICAL_ANGLE_OFFSET in either direction
          if self.withinInterval(angle, math.pi/2, VERTICAL_ANGLE_OFFSET) or self.withinInterval(angle, -math.pi/2, VERTICAL_ANGLE_OFFSET):
            # Going straight forward/backwards
            newSpeed = relY
            newSpeed *= maxPower
            # newSpeed = self.clampAbsolute(newSpeed, maxPower)
            self.setLeftMotor(f"{newSpeed:.3f}")
            self.setRightMotor(f"{newSpeed:.3f}")
          else:
            # We are turning
            newSpeed = radius
            newSpeed *= maxPower
            x = math.cos(angle)
            y = math.sin(angle)
            if y > 0:
              fullSpeed = newSpeed
              signy = 1
            else:
              fullSpeed = -newSpeed 
              signy = -1

            otherSideSpeed = abs(y)-HALFWAY_HEIGHT # Want the halfway to be the new 0
            # otherSideSpeed *= signy # Add back signs
            otherSideSpeed /= HALFWAY_HEIGHT # Want it to be from -1 to 1
            otherSideSpeed = self.clamp(otherSideSpeed, -1, 1) 
            otherSideSpeed *= fullSpeed # Weigh it by how far from center you are
            # self.setLights(otherSideSpeed)

            if x > 0:
              # Turning right
              signx = 1
              if y > 0:
                leftSpeed = fullSpeed
                rightSpeed = otherSideSpeed
              else:
                leftSpeed = otherSideSpeed 
                rightSpeed = fullSpeed
            else: 
              # Turning left
              signx = -1
              if y > 0:
                leftSpeed = otherSideSpeed
                rightSpeed = fullSpeed
              else:
                leftSpeed = fullSpeed
                rightSpeed = otherSideSpeed

            self.setLeftMotor(f"{leftSpeed:.3f}")
            self.setRightMotor(f"{rightSpeed:.3f}")


        else:          
          # If in the deadzone for the joysticks, we come to a stop
          if not self.isInCruiseControl:
            self.setLeftMotor(0)
            self.setRightMotor(0)
          # If cruise control is enabled, and we're in the deadzone, we won't update speed

      
      # If cruise control is pressed, we'll disable the input
      # if cruiseControlButtonPressed:
      #   self.setCruiseControlCheckbox(True)


      # [SERVO ANGLES]
      # <RIGHT STICK>
      if not self.isInDeadZone(joystickRX, joystickRY):
        changeInHorizontalAngle = 1.0*joystickRX/self.MAX_JOYSTICK * self.SENSITIVITY_HORIZONTAL_ANGLE
        # servoHorizontalAngle = float(self.getServosHorizontal())
        # servoHorizontalAngle += changeInHorizontalAngle
        # servoHorizontalAngle = int(self.clamp(servoHorizontalAngle, 0, 180) + 0.5)
        # horizontalAngle += changeInHorizontalAngle
        # horizontalAngle = self.clamp(horizontalAngle, 0, 180)
        # servoHorizontalAngle = int(horizontalAngle + 0.5)
        self.horizontalAngle += changeInHorizontalAngle
        self.horizontalAngle = self.clamp(self.horizontalAngle, 0, 180) 
        servoHorizontalAngle = int(self.horizontalAngle + 0.5)

        changeInVerticalAngle = 1.0*joystickRY/self.MAX_JOYSTICK * self.SENSITIVITY_VERTICAL_ANGLE
        # servoVerticalAngle = float(self.getServosVertical())
        # servoVerticalAngle += changeInVerticalAngle
        # servoVerticalAngle = int(self.clamp(servoVerticalAngle, 0, 90) + 0.5)
        # verticalAngle += changeInVerticalAngle
        # verticalAngle = self.clamp(verticalAngle, 0, 90)
        # servoVerticalAngle = int(verticalAngle + 0.5)
        self.verticalAngle += changeInVerticalAngle
        self.verticalAngle = self.clamp(self.verticalAngle, 0, 90) 
        servoVerticalAngle = int(self.verticalAngle + 0.5)

        # print(f"rx={joystickRX} | rx={joystickRY} | changeHoriz={changeInHorizontalAngle} | changeVert={changeInVerticalAngle}")

        self.setServosHorizontal(servoHorizontalAngle)
        self.setServosVertical(servoVerticalAngle)
      
      if maxSpeedDecreasePressed:
        newMax = maxPower - INCREMENT
        newMax = self.clamp(newMax, 0, 1.0)
        maxPower = newMax
        self.setJoystickMaxPower(maxPower)
        if DEBUG:
          print(f"Left Bumper pressed, new maxpower = {maxPower}")
      
      
      if maxSpeedIncreasePressed:
        # print(f"right bumper pressed: maxpower = {maxPower}")
        newMax = maxPower + INCREMENT
        # print(f"  Temp: {newMax}")
        newMax = self.clamp(newMax, 0, 1.0)
        maxPower = newMax 
        self.setJoystickMaxPower(maxPower)
        # print(f"  new max: {maxPower}")
        if DEBUG:
          print(f"Right bumper pressed, new maxpower = {maxPower}")

      if dPadX != 0:
        try: 
          attachmentPower = float(self.getAttachmentPower())
          attachmentPower += dPadX * ATTACHMENT_INCREMENT 
          attachmentPower = self.clamp(attachmentPower, 0, 1.0) 
          self.setAttachmentPower(attachmentPower) 
        except:
          print("AttachmentPower invalid")

      if dPadY != 0:
        if DEBUG:
          print(f"dPadY: {dPadY}")
        try: 
          lightsPower = float(self.getLights()) 
          lightsPower += dPadY * LIGHT_INCREMENT
          lightsPower = self.clamp(lightsPower, 0, 1.0)
          self.setLights(lightsPower)
        except:
          print("Lights invalid")

      if centerAnglePressed:
        self.centerAngle()
      
      if showHelpMenuPressed:
        self.toggleHelpWindow()

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
    try:
      val = float(val)
      self.lights_entry_text.set(f"{val:.3}")
      if self.lights_power_label != None:
        try:
          power = int(val*100 + 0.5)
          self.lights_power_label["text"] = f"Lights Power: {power:3d}%"
        except Exception as e:
          print("[LightsPower] Exception {e}")
    except: 
      self.lights_entry_text.set(val)

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
  
  def centerAngle(self):
    self.setServosHorizontal(90)
    self.horizontalAngle = 90

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
  
  def getAttachmentPower(self):
    if self.attachment_entry_text == None:
      return "0"
    return self.attachment_entry_text.get()
  
  def setAttachmentPower(self, val):
    if self.attachment_entry_text == None:
      return 
    try:
      val = float(val)
      self.attachment_entry_text.set(f"{val:.3}")
      if self.attachment_power_label != None:
        try:
          power = int(val*100 + 0.5)
          self.attachment_power_label["text"] = f"Attachment Power: {power:3d}%"
        except Exception as e:
          print("[LightsPower] Exception {e}")
    except: 
      self.attachment_entry_text.set(val)
  
  use_controller_checkbox_val = None 
  def getUseController(self):
    if self.use_controller_checkbox_val == None:
      return False 
    return self.use_controller_checkbox_val.get()

  def setUseController(self, val):
    if self.use_controller_checkbox_val == None:
      return
    self.use_controller_checkbox_val.set(val)

  pipe_name_text = None
  def getPipeName(self):
    if self.pipe_name_text == None:
      return ""
    return self.pipe_name_text.get()

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
        time.sleep(dTime)
        continue
      time.sleep(dTime)
      # if time.time() < nextTimeAvailable:
      #   continue 
      # nextTimeAvailable = time.time() + dTime 

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
    servoHorizontal = self.getServosHorizontal()
    # try:
    #   servoHorizontal = 180 - float(servoHorizontal)
    # except: 
    #   # print("Bad horizontal")
    #   servoHorizontal = 90
    outputString = f"{self.getLights()} {self.getLeftMotorSpeed()} {self.getRightMotorSpeed()} {servoHorizontal} {self.getServosVertical()} {self.getAttachmentPower()}"
    if DEBUG:
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

    # global image_label
    image_label.imgtk = imgTk
    image_label.configure(image=imgTk)
    image_label.image = imgTk
    # image_label.after(1, self.showFrame)

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
  
  encoder_label = None
  def setEncoder(self, numRotations):
    if self.encoder_label == None:
      return
    self.encoder_label["text"] = f"Rotations: {numRotations}"

  # lights_power_label = None
  # def setLights(self, power):
  #   if self.lights_power_label == None:
  #     return 
  #   try:
  #     power = int(power*100 + 0.5)
  #     self.lights_power_label["text"] = f"Lights Power: {power:3d}%"
  #   except Exception as e:
  #     print("[LightsPower] Exception {e}")

  # attachment_power_label = None
  # def setAttachmentPower(self, power):
  #   if self.attachment_power_label == None:
  #     return 
  #   try:
  #     power = int(power*100 + 0.5)
  #     self.attachment_power_label["text"] = f"Attachment Power: {power:3d}%"
  #   except Exception as e:
  #     print("[LightsPower] Exception {e}")

  encoderQueue = Queue(maxsize=1)
  def loopToShowEncoder(self):
    while True:
      time.sleep(0.01)
      if self.encoderQueue.empty():
        continue 
      numRotations = self.encoderQueue.get()
      self.setEncoder(numRotations)
  
  joystick_max_power_label = None 
  def setJoystickMaxPower(self, maxPower):
    if self.joystick_max_power_label == None:
      return 
    try:
      maxPower = int(maxPower*100 + 0.5)
      self.joystick_max_power_label["text"] = f"Max Motor Power: {maxPower:3d}%"
    except:
      print("Bad max power for joystick label")
      return

  def clearLayout(self):
    try: 
      self.manual_input_frame.grid_remove()
      self.side_frame.grid_remove()
      self.button_frame.grid_remove()
      self.data_frame.grid_remove()
      self.checkbox_frame.grid_remove()
      self.image_frame.grid_remove()
      self.canvas.grid_remove()
      self.welcome_frame.grid_remove()
      self.input_data_frame.grid_remove()
      self.config_frame.grid_remove()
    except Exception as e:
      print(f"[ClearLayout] Exception: {e}")

  def setWelcomeLayout(self):
    try:
      self.clearLayout()
      self.image_frame.grid(row=0, column=0)
      self.welcome_frame.grid(row=1, column=0)
    except Exception as e:
      print(f"[WelcomeLayout] Exception: {e}")
  
  def setInputDataLayout(self):
    try:
      self.clearLayout()
      self.image_frame.grid(row=0, column=0)
      self.input_data_frame.grid(row=1, column=0)
    except Exception as e:
      print(f"[InputDataLayout] Exception: {e}")
  
  def setConfigLayout(self):
    try:
      self.clearLayout()
      self.image_frame.grid(row=0, column=0)
      self.config_frame.grid(row=1, column=0)
    except Exception as e:
      print(f"[ConfigLayout] Exception: {e}")

  def setLayoutDefault(self):
    try: 
      self.clearLayout()
      self.image_frame.grid(row=0, column=0)
      self.side_frame.grid(row=0, column=1, sticky='n')

      # Setup their grid in their data frame
      self.canvas.grid(row=0, column=0)
      # Not sure why we have to skip row 1, but it's necessary to maintain
      # the data_frame when switching to debug layout and back
      self.data_frame.grid(row=2, column=0)
      self.checkbox_frame.grid(row=3, column=0)
      self.button_frame.grid(row=4, column=0)
    except Exception as e: 
      print(f"[LayoutDefault] Exception: {e}")

  def setLayoutManualInput(self):
    try:
      self.clearLayout()
      self.side_frame.grid(row=0, column=0)
      self.image_frame.grid(row=1, column=0)

      # Within the side frame
      self.manual_input_frame.grid()
      self.button_frame.grid(row=0, column=1)
      self.checkbox_frame.grid(row=0, column=2)
      self.data_frame.grid(row=0, column=3)
      self.canvas.grid(row=0, column=4, rowspan=2) # TEMP
    except Exception as e: 
      print(f"[LayoutManualInput] Exception: {e}")

  def setVideoSizeSmall(self):
    self.smallerFrame = True
    self.defaultWallpaper = self.defaultWallpaper.resize((16*70, 9*70), Image.ANTIALIAS)
    defaultWallpapertk = ImageTk.PhotoImage(self.defaultWallpaper)
    if self.imgTkQueue.empty():
      self.image_label.imgtk = defaultWallpapertk 
      self.image_label.configure(image=defaultWallpapertk)
  
  def setVideoSizeDefault(self):
    self.smallerFrame = False
    self.defaultWallpaper = self.defaultWallpaper.resize((1280, 720), Image.ANTIALIAS)
    defaultWallpapertk = ImageTk.PhotoImage(self.defaultWallpaper)
    if self.imgTkQueue.empty():
      self.image_label.imgtk = defaultWallpapertk 
      self.image_label.configure(image=defaultWallpapertk) 

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
  
  canvas = None
  left_line = None
  right_line = None
  canvas_width = 150
  canvas_height = 200
  def updateGUIAngle(self, angle):
    if self.canvas == None: 
      return
    # Constants
    ORIGIN_X = self.canvas_width//2 
    ORIGIN_Y = self.canvas_height//4
    LEN = 50
    angle = 180 - angle # We want 0 degrees to be left
    angle = math.radians(angle) 
    

    ANGLE_WIDTH = math.radians(90)
    left_angle = angle + ANGLE_WIDTH/2 
    right_angle = angle - ANGLE_WIDTH/2 
    
    left_dx = math.cos(left_angle)
    left_dx = int(left_dx*LEN) 
    left_dy = math.sin(left_angle) 
    left_dy = -int(left_dy*LEN) # up is negative in canvas

    right_dx = math.cos(right_angle)
    right_dx = int(right_dx*LEN) 
    right_dy = math.sin(right_angle) 
    right_dy = -int(right_dy*LEN)

    if self.left_line != None:
      self.canvas.delete(self.left_line)

    self.left_line = self.canvas.create_line(ORIGIN_X, ORIGIN_Y, ORIGIN_X+left_dx, ORIGIN_Y+left_dy, width=5, fill="black")

    if self.right_line != None:
      self.canvas.delete(self.right_line)

    self.right_line = self.canvas.create_line(ORIGIN_X, ORIGIN_Y, ORIGIN_X+right_dx, ORIGIN_Y+right_dy, width=5, fill="black")


  def loopToUpdateGUIAngle(self):
    while True:
      time.sleep(0.04)
      if self.horizontalAngle == None: 
        continue 
      # self.updateGUIAngle(self.horizontalAngle)
      self.updateGUIAngle(self.getServosHorizontal())

  startTime = 0
  numFrames = 0
  curFrame = None
  frameQueue = Queue(maxsize=1)
  imgQueue = Queue(maxsize=2)
  imgTkQueue = Queue(maxsize=1)
  smallerFrame = False
  videoMaxFramerate = 60
  frameRefreshDelay = (1 / videoMaxFramerate)
  def loopToEncodeImg(self):
    while True:
      if not self.frameQueue.empty():
        frame = self.frameQueue.get() 
        img = Image.open(io.BytesIO(frame)) 

        if self.smallerFrame:
          # img = img.resize((16*70, 9*70), Image.ANTIALIAS)
          img = img.crop((0, 0, 16*70, 9*70))

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
        self.image_label.imgtk = imgTk 
        self.image_label.configure(image=imgTk) 
        self.image_label.image = imgTk  
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
        self.image_label.imgtk = imgTk 
        self.image_label.configure(image=imgTk) 
        self.image_label.image = imgTk 
        
        # Update the framerate
        self.numFrames += 1
        duration = time.time() - self.startTime 
        self.setFPS(self.numFrames/duration) 

        self.curFrame = None
      else: 
        # Prevent spam on the thread by waiting
        time.sleep(self.frameRefreshDelay)

      
  distance_traveled_feet = None
  image_label = None
  def run(self):
    root = tk.Tk() 
    root.title("Storm Drain Robot")
    self.root = root
    self.root.protocol("WM_DELETE_WINDOW", self.callback)
    self.root.geometry("+0+0") # Sets the location of the window

    ids = self.ids 
    vals = self.vals 
    self.startTime = time.time()

    # Menubar
    menubar = tk.Menu(self.root)

    # Create a layoutMenu
    layoutMenu = tk.Menu(menubar, tearoff=0) 
    layoutMenu.add_command(label="Default Layout", command=self.setLayoutDefault)
    layoutMenu.add_command(label="Debug Layout", command=self.setLayoutManualInput) 
    layoutMenu.add_separator()
    layoutMenu.add_command(label="Default Video Stream Size", command=self.setVideoSizeDefault)
    layoutMenu.add_command(label="Shrink Video Stream Size (For smaller screens)", command=self.setVideoSizeSmall)
    menubar.add_cascade(label="Layouts", menu=layoutMenu)

    # Rinse and repeat with other menus
    # HELP Tab
    helpMenu = tk.Menu(menubar, tearoff=0)
    helpMenu.add_command(label="Help", command=self.openHelpWindow)
    helpMenu.add_command(label="About...", command=self.openAboutWindow)
    menubar.add_cascade(label="Help", menu=helpMenu)

    # Add menubar to the root frame
    self.root.config(menu=menubar)



    # Going to just manually define every part
    self.side_frame = tk.Frame(self.root)
    self.side_frame.grid(row=0, column=0)

    self.manual_input_frame = tk.Frame(self.side_frame)
    self.manual_input_frame.grid(row=0, column=0)
    lights_label = tk.Label(self.manual_input_frame, text="Lights %")
    lights_label.grid(row=0, column=0)
    self.lights_entry_text = tk.StringVar(value="0")
    self.lights_entry = tk.Entry(self.manual_input_frame, width=20, textvariable=self.lights_entry_text)
    self.lights_entry.grid(row=1, column=0, padx=2)

    self.motors_left_entry_text = tk.StringVar(value="0")
    motors_left_label = tk.Label(self.manual_input_frame, text="Left Motor %")
    motors_left_label.grid(row=0, column=1)
    motors_left_entry = tk.Entry(self.manual_input_frame, width=20, textvariable=self.motors_left_entry_text)
    motors_left_entry.grid(row=1, column=1, padx=2)
    motors_right_label = tk.Label(self.manual_input_frame, text="Right Motor %")
    motors_right_label.grid(row=0, column=2)
    self.motors_right_entry_text = tk.StringVar(value="0")
    motors_right_entry = tk.Entry(self.manual_input_frame, width=20, textvariable=self.motors_right_entry_text)
    motors_right_entry.grid(row=1, column=2, padx=2)

    servos_horizontal_label = tk.Label(self.manual_input_frame, text="Horizontal\n Camera Angle")
    servos_horizontal_label.grid(row=0, column=3)
    servos_horizontal_entry = tk.Entry(self.manual_input_frame, width=20)
    # servos_horizontal_entry.grid(row=1, column=3, padx=2) 
    self.servos_horizontal_slider = tk.Scale(self.manual_input_frame, from_=0, to=180, orient=tk.HORIZONTAL) # Can optionally set tickInterval=10, length=something
    self.servos_horizontal_slider.set(90)
    self.servos_horizontal_slider.grid(row=1, column=3, padx=2)
    servos_vertical_label = tk.Label(self.manual_input_frame, text="Vertical\n Camera Angle")
    servos_vertical_label.grid(row=0, column=4)
    servos_vertical_entry = tk.Entry(self.manual_input_frame, width=20)
    # servos_vertical_entry.grid(row=1, column=4, padx=2)
    self.servos_vertical_slider = tk.Scale(self.manual_input_frame, from_=0, to=90, orient=tk.HORIZONTAL)
    self.servos_vertical_slider.set(45)
    self.servos_vertical_slider.grid(row=1, column=4, padx=2)

    attachment_label = tk.Label(self.manual_input_frame, text="Attachment\nPower")
    attachment_label.grid(row=0, column=5)
    self.attachment_entry_text = tk.StringVar(value="0") 
    attachment_entry = tk.Entry(self.manual_input_frame, width=20, textvariable=self.attachment_entry_text)
    attachment_entry.grid(row=1, column=5, padx=2)

    # Ahhhhh no multiline lambdas :(  Wait nvm.
    submit_data_button = tk.Button(
      self.manual_input_frame,
      text="Submit Data",
      command = self.submitData
    )
    submit_data_button.grid(row=1, column=6)

    self.start_latitude_text = tk.StringVar() 
    self.start_longitude_text = tk.StringVar() 
    self.end_latitude_text = tk.StringVar() 
    self.end_longitude_text = tk.StringVar() 
    self.button_frame = tk.Frame(self.side_frame, relief=tk.FLAT, borderwidth=2)
    self.button_frame.grid(row=0, column=1)
    create_shapefile_button = tk.Button(
      self.button_frame,
      text = "Create ShapeFile",
      command = lambda 
        root=self.root,
        start_latitude_text=self.start_latitude_text,
        start_longitude_text=self.start_longitude_text,
        end_latitude_text=self.end_latitude_text,
        end_longitude_text=self.end_longitude_text:
        shapeFile_Frontend.create_shape_file_dialog(
          root=root, 
          start_latitude_text=start_latitude_text,
          start_longitude_text=start_longitude_text,
          end_latitude_text=end_latitude_text,
          end_longitude_text=end_longitude_text          
        ),
    )
    create_shapefile_button.grid(row=2, column=0, pady=2)

    center_angle_button = tk.Button(
      self.button_frame, 
      text="Center Camera",
      command = self.centerAngle,
    )
    center_angle_button.grid(row=1, column=0, pady=2)

    emergency_stop_button = tk.Button(
      # self.manual_input_frame,
      self.button_frame,
      text="STOP MOTORS",
      command = self.emergencyStop,
      background = 'red'
    )
    # emergency_stop_button.grid(row=0, column=6)
    emergency_stop_button.grid(row=0, column=0, pady=2)

    help_button = tk.Button(
      self.button_frame,
      text = "Help",
      command = self.openHelpWindow
    )
    help_button.grid(row=3, column=0, pady=2)


    # Todo: Add a checkbox for constantly send the data every x seconds
    self.checkbox_frame = tk.Frame(self.side_frame, relief=tk.RAISED, borderwidth=2)
    # self.checkbox_frame.grid(row=1, column=7)
    self.checkbox_frame.grid(row=0, column=2)
    constantly_submit_checkbox_val = tk.IntVar()
    constantly_submit_checkbox = tk.Checkbutton(self.checkbox_frame, text="Send Instructions", variable=constantly_submit_checkbox_val)
    # constantly_submit_checkbox.grid(row=1, column=6)
    constantly_submit_checkbox.grid(row=0, column=0)
    self.use_controller_checkbox_val = tk.IntVar()
    use_controller_checkbox = tk.Checkbutton(self.checkbox_frame, text="Use Controller", variable=self.use_controller_checkbox_val)
    use_controller_checkbox.grid(row=1, column=0)


    # DATA BOX
    self.data_frame = tk.Frame(self.side_frame, relief=tk.RAISED, borderwidth=2)
    # self.data_frame.grid(row=0, column=8, rowspan=2, padx=2)
    self.data_frame.grid(row=0, column=3)
    # Populate the box with data
    self.fps_label = tk.Label(self.data_frame, text="FPS: 0")
    self.fps_label.grid(row=0, column=0)
    self.voltage_label = tk.Label(self.data_frame, text="Voltage: 0")
    self.voltage_label.grid(row=1, column=0)
    self.encoder_label = tk.Label(self.data_frame, text="Rotations: 0")
    self.encoder_label.grid(row=2, column=0)
    self.joystick_max_power_label = tk.Label(self.data_frame, text="Max Motor Power:  50%")
    self.joystick_max_power_label.grid(row=3, column=0)
    self.lights_power_label = tk.Label(self.data_frame, text="Lights Power:    0%")
    self.lights_power_label.grid(row=4, column=0)
    self.attachment_power_label = tk.Label(self.data_frame, text="Attachment Power:    0%")
    self.attachment_power_label.grid(row=5, column=0)
    

    # Threads to refresh the data
    voltage_data_loop = threading.Thread(
      target=self.loopToShowVoltage,
      daemon=True
    )
    voltage_data_loop.start()
    encoder_data_loop = threading.Thread(
      target=self.loopToShowEncoder,
      daemon=True
    )
    encoder_data_loop.start()

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


    # CAMERA BEARING CANVAS
    # Create Canvas to show the current bearing of the camera
    self.canvas = tk.Canvas(self.side_frame, bg="white", height=self.canvas_height, width=self.canvas_width)
    filename = os.getcwd() + "\\RobotTopDown.png" # 300 x 400
    robotImage = Image.open(filename)
    robotImage = robotImage.resize((self.canvas_width, self.canvas_height), Image.ANTIALIAS)
    robotImagetk = ImageTk.PhotoImage(robotImage)
    robotImage = self.canvas.create_image(0, 0, image=robotImagetk, anchor='nw', tags="IMG")
    canvas_update_loop = threading.Thread(
      target=self.loopToUpdateGUIAngle,
      daemon=True
    )
    canvas_update_loop.start()

    # Todo: Add a image for the info
    # imageFrame = tk.Frame(width=1280, height=720)
    # imageFrame.grid(row=2, column=0, columnspan=9)
    self.image_frame = tk.Frame(self.root)
    self.image_frame.grid(row=1, column=0)
    

    # IMAGE FRAME
    # Capture video frames
    # Create a default image for the frame before streaming
    defaultWallpaperFileName = os.getcwd() + "\\UCF Wallpaper.png"
    self.defaultWallpaper = Image.open(defaultWallpaperFileName)
    self.defaultWallpaper = self.defaultWallpaper.resize((1280, 720), Image.ANTIALIAS)
    defaultWallpapertk = ImageTk.PhotoImage(self.defaultWallpaper)
    self.image_label = tk.Label(self.image_frame, image=defaultWallpapertk)
    self.image_label.grid(row=0, column=0)


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


    # WELCOME GUI
    self.welcome_frame = tk.Frame(self.root)
    self.welcome_label = tk.Label(
      self.welcome_frame,
      text="Please select what you would like to do:")
    self.welcome_label.grid(row=0, column=0)
    self.welcome_button_frame = tk.Frame(self.welcome_frame)
    self.welcome_button_frame.grid(row=1, column=0, pady=3) 
    self.welcome_start_run_button = tk.Button(
      self.welcome_button_frame,
      text="Start Run",
      command=self.inputDataWindow
    )
    self.welcome_start_run_button.grid(row=0, column=0, padx=5)
    self._welcome_download_video_button = tk.Button(
      self.welcome_button_frame,
      text="Settings",
      command=self.setConfigLayout
    )
    self._welcome_download_video_button.grid(row=0, column=1, padx=5)


    # INPUT DATA GUI
    self.input_data_frame = tk.Frame(self.root) 
    pipe_name_label = tk.Label(self.input_data_frame, text="Pipe Name:")
    pipe_name_label.grid(row=3, column=0)
    self.pipe_name_text = tk.StringVar()
    pipe_name_entry = tk.Entry(self.input_data_frame, textvariable=self.pipe_name_text)
    pipe_name_entry.grid(row=3, column=1, columnspan=1, sticky="ew")
    start_latitude_label = tk.Label(self.input_data_frame, text="Start Latitude")
    start_latitude_label.grid(row=1, column=0)
    start_latitude_entry = tk.Entry(self.input_data_frame, textvariable=self.start_latitude_text)
    start_latitude_entry.grid(row=1, column=1)
    start_longitude_label = tk.Label(self.input_data_frame, text="Start Longitude", padx=2)
    start_longitude_label.grid(row=1, column=2)
    start_longitude_entry = tk.Entry(self.input_data_frame, textvariable=self.start_longitude_text)
    start_longitude_entry.grid(row=1, column=3)
    end_latitude_label = tk.Label(self.input_data_frame, text="End Latitude")
    end_latitude_label.grid(row=2, column=0)
    end_latitude_entry = tk.Entry(self.input_data_frame, textvariable=self.end_latitude_text)
    end_latitude_entry.grid(row=2, column=1)
    end_longitude_label = tk.Label(self.input_data_frame, text="End Longitude", padx=2)
    end_longitude_label.grid(row=2, column=2)
    end_longitude_entry = tk.Entry(self.input_data_frame, textvariable=self.end_longitude_text)
    end_longitude_entry.grid(row=2, column=3)
    input_data_start_run_button = tk.Button(self.input_data_frame, command=self.startRun, text="Start Run")
    input_data_start_run_button.grid(row=3, column=3)


    # HELP
    # Grab image
    filename = os.getcwd() + "\\controllerLayout.png" # 300 x 400
    controllerImage = Image.open(filename)
    controllerImage = controllerImage.resize((1280, 720), Image.ANTIALIAS)
    self.controllerImageTk = ImageTk.PhotoImage(controllerImage)
    

    # CONFIG
    self.config_frame = tk.Frame(self.root)
    # emergency_stop_button_label = tk.Label(self.config_frame, text="Emergency Stop:")
    # emergency_stop_button_label.grid(row=0, column=0)
    # self.emergency_stop_button_text = tk.StringVar()
    # self.emergency_stop_button_text.set("B")
    # emergency_stop_button_dropdown = tk.OptionMenu(self.config_frame, self.emergency_stop_button_text, *self.controller_buttons)
    # emergency_stop_button_dropdown.grid(row=0, column=1)    

    # center_angle_button_label = tk.Label(self.config_frame, text="Center Camera:")
    # center_angle_button_label.grid(row=1, column=0)
    # self.center_angle_button_text = tk.StringVar()
    # center_angle_button_dropdown = tk.OptionMenu(self.config_frame, self.emergency_stop_button_text, *self.controller_buttons)
    # center_angle_button_dropdown.grid(row=1, column=1)

    index = 0
    button_labels = {}
    button_dropdown = {}
    dropdown_width = 150
    self.config_frame.columnconfigure(1, minsize=dropdown_width)
    self.config_frame.columnconfigure(3, minsize=dropdown_width)
    for name in self.controller_configurable:
      button_labels[name] = tk.Label(self.config_frame, text=f"{name}:")
      button_labels[name].grid(row=index//2, column=2*(index%2), sticky="w")
      self.button_text[name] = tk.StringVar()
      self.button_text[name].set(self.getConfig(name))
      button_dropdown[name] = tk.OptionMenu(self.config_frame, self.button_text[name], *self.controller_buttons)
      button_dropdown[name].grid(row=index//2, column=2*(index%2)+1, padx=2, sticky="e")
      index += 1

    config_button_frame = tk.Frame(self.config_frame)
    # config_button_frame.grid(row=index, column=3, sticky="e", pady=2)
    config_button_frame.grid(row=0, column=5)
    save_config_button = tk.Button(config_button_frame, text="Save", command=self.saveConfig)
    save_config_button.grid(row=0, column=1, padx=4)
    cancel_config_button = tk.Button(config_button_frame, text="Cancel", command=self.cancelConfig)
    cancel_config_button.grid(row=0, column=2)
    default_config_button = tk.Button(config_button_frame, text="Defaults", command=self.restoreDefaultConfig)
    default_config_button.grid(row=0, column=0)

    self.cancelConfig() # Use this to restore the config to what it says in the file

    # To default layout
    # self.setLayoutDefault()

    self.setWelcomeLayout()

    self.root.mainloop()




# https://stackoverflow.com/questions/459083/how-do-you-run-your-own-code-alongside-tkinters-event-loop
# Begins the loop on a separate thread

app = App()

