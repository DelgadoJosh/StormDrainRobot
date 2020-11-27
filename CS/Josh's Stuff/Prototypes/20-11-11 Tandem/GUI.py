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
import math
import numpy
import shapeFile_Frontend
import os

try:
  from controller import Controller
  controllerConnected = True
except:
  controllerConnected = False 

DEBUG = False

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

  inputQueriesPerSecond = 100
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


      joystickLX = self.removeDeadZone(controller.getLeftJoystickX())
      joystickLY = self.removeDeadZone(controller.getLeftJoystickY())

      joystickRX = self.removeDeadZone(controller.getRightJoystickX())
      joystickRY = self.removeDeadZone(controller.getRightJoystickY())

      bPressed = controller.getBPressedAndReleased()

      leftBumperPressed = controller.getLeftBumperPressedAndReleased()
      rightBumperPressed = controller.getRightBumperPressedAndReleased()

      dPadX = controller.getDPadXState()
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
        self.setLeftMotor(0)
        self.setRightMotor(0)
      
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
      
      if bPressed:
        if DEBUG:
          print("B was pressed!")
        self.emergencyStop()
      
      if leftBumperPressed:
        newMax = maxPower - INCREMENT
        newMax = self.clamp(newMax, 0, 1.0)
        maxPower = newMax
        self.setJoystickMaxPower(maxPower)
        print(f"Left Bumper pressed, new maxpower = {maxPower}")
      
      
      if rightBumperPressed:
        # print(f"right bumper pressed: maxpower = {maxPower}")
        newMax = maxPower + INCREMENT
        # print(f"  Temp: {newMax}")
        newMax = self.clamp(newMax, 0, 1.0)
        maxPower = newMax 
        self.setJoystickMaxPower(maxPower)
        # print(f"  new max: {maxPower}")
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
    try:
      val = float(val)
      self.lights_entry_text.set(f"{val:.3}")
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
  
  encoder_label = None
  def setEncoder(self, numRotations):
    if self.encoder_label == None:
      return
    self.encoder_label["text"] = f"Rotations: {numRotations}"
  
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
      maxPower = int(maxPower*100)
      self.joystick_max_power_label["text"] = f"Max Power: {maxPower:3d}%"
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
    except Exception as e:
      print(f"[ClearLayout] Exception: {e}")

  def setLayoutDefault(self):
    try: 
      self.clearLayout()
      self.image_frame.grid(row=0, column=0)
      self.side_frame.grid(row=0, column=1, sticky='n')

      # Setup their grid in their data frame
      self.canvas.grid(row=0, column=0)
      self.data_frame.grid(row=1, column=0, pady=2)
      self.checkbox_frame.grid(row=2, column=0)
      self.button_frame.grid(row=3, column=0)
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
      self.lmain.imgtk = defaultWallpapertk 
      self.lmain.configure(image=defaultWallpapertk)
  
  def setVideoSizeDefault(self):
    self.smallerFrame = False
    self.defaultWallpaper = self.defaultWallpaper.resize((1280, 720), Image.ANTIALIAS)
    defaultWallpapertk = ImageTk.PhotoImage(self.defaultWallpaper)
    if self.imgTkQueue.empty():
      self.lmain.imgtk = defaultWallpapertk 
      self.lmain.configure(image=defaultWallpapertk) 

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
  frameRefreshDelay = int(1 / videoMaxFramerate)
  def loopToEncodeImg(self):
    while True:
      if not self.frameQueue.empty():
        frame = self.frameQueue.get() 
        img = Image.open(io.BytesIO(frame)) 

        if self.smallerFrame:
          img = img.resize((16*70, 9*70), Image.ANTIALIAS)

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
    # submit_data_button.grid(row=1, column=5)
    submit_data_button.grid(row=1, column=6)

    self.button_frame = tk.Frame(self.side_frame, relief=tk.FLAT, borderwidth=2)
    # self.button_frame.grid(row=0, column=6)
    self.button_frame.grid(row=0, column=1)
    create_shapefile_button = tk.Button(
      self.button_frame,
      text = "Create ShapeFile",
      command = lambda 
        root=self.root:
        shapeFile_Frontend.create_shape_file_dialog(root),
    )
    create_shapefile_button.grid(row=2, column=0)

    center_angle_button = tk.Button(
      self.button_frame, 
      text="Center Angle",
      command = self.centerAngle,
    )
    center_angle_button.grid(row=1, column=0)

    emergency_stop_button = tk.Button(
      # self.manual_input_frame,
      self.button_frame,
      text="STOP MOTORS",
      command = self.emergencyStop,
      background = 'red'
    )
    # emergency_stop_button.grid(row=0, column=6)
    emergency_stop_button.grid(row=0, column=0)

    # Todo: Add a checkbox for constantly send the data every x seconds
    self.checkbox_frame = tk.Frame(self.side_frame, relief=tk.RAISED, borderwidth=2)
    # self.checkbox_frame.grid(row=1, column=7)
    self.checkbox_frame.grid(row=0, column=2)
    constantly_submit_checkbox_val = tk.IntVar()
    constantly_submit_checkbox = tk.Checkbutton(self.checkbox_frame, text="Constantly Submit", variable=constantly_submit_checkbox_val)
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
    self.joystick_max_power_label = tk.Label(self.data_frame, text="Max Power:  50%")
    self.joystick_max_power_label.grid(row=3, column=0)

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
    
    # Capture video frames
    # Create a default image for the frame before streaming
    defaultWallpaperFileName = os.getcwd() + "\\UCF Wallpaper.png"
    self.defaultWallpaper = Image.open(defaultWallpaperFileName)
    self.defaultWallpaper = self.defaultWallpaper.resize((1280, 720), Image.ANTIALIAS)
    defaultWallpapertk = ImageTk.PhotoImage(self.defaultWallpaper)
    self.lmain = tk.Label(self.image_frame, image=defaultWallpapertk)
    self.lmain.grid(row=0, column=0)

    # To default layout
    self.setLayoutDefault()

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

