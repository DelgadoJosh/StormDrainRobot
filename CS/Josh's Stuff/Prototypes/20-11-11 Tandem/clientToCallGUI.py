import socket 
import GUI
import struct
import threading
# from queue import Queue

payload_size = struct.calcsize("Q")

class Client():
  ip_address = "10.0.0.2" # The one you're connecting to
  # ip_address = "localhost"
  port = 5000
  def __init__(self, Address=(ip_address,port)):
    self.s = socket.socket() 
    self.s.connect(Address)

  def send(self, message):
    self.s.send(message)

print("Initiating Client")
c = Client()
print("Client Connected")

# Continually attempt to send messages to the server
# If "quit" is sent, then it will send an empty string
#   which turns off the server.
queue = GUI.app.queue
stopFlag = GUI.app.programEnd

# Loop for receiving input, the input is added to a queue
def getInput():
    global stopFlag
    while not stopFlag:
      stopFlag = GUI.app.programEnd
      print("lol")
      print(stopFlag)
      try: 
        if not queue.empty():
          command = queue.get()
          print(f"Sending {command}")

          c.send(command.encode('utf-8'))
          
          # data = c.s.recv(1024) 
          # print(f"Received: {repr(data)}")
      except KeyboardInterrupt:
        stopFlag = True
    print("Ended input loop")
    # while True:
    #     try:
    #         command = input()

    #         if command == 'quit':
    #             stopFlag = True
    #             return

    #         c.send(command.encode('utf-8'))
    #     except KeyboardInterrupt:
    #         stopFlag = True
    #         return

def showVideo():
  # Loop for receiving images
  global stopFlag
  data = b''
  while True:
    try:
      if stopFlag:
        return
      # Retrieve message size
      while len(data) < payload_size:
        data += c.s.recv(4096)
      
      packed_msg_size = data[:payload_size]
      data = data[payload_size:]
      msg_size = struct.unpack("Q", packed_msg_size)[0]

      # Retrieve all dat based on message size
      while len(data) < msg_size:
        data += c.s.recv(4096)
      
      frame_data = data[:msg_size]
      data = data[msg_size:]

      # If going the direct encode/decode to get frameBytes
      frameBytes = base64.b64decode(frame_data) 

      img_as_np = np.frombuffer(frameBytes, dtype=np.uint8)
      frame = cv2.imdecode(img_as_np, flags=1)

      # Display
      cv2.imshow("Frame", frame)
      cv2.waitKey(1)

    except KeyboardInterrupt:
      cv2.destroyAllWindows()
      break
  
  print("Video loop end")


input_thread = threading.Thread(target=getInput)
video_thread = threading.Thread(target=showVideo)

input_thread.start()
video_thread.start()

