import socket
import cv2 
import struct
import pickle
import base64
import numpy as np
import threading

# Create the client to receive video

payload_size = struct.calcsize("Q")

class Client_Viewer():
  ip_address = "10.0.0.2"
#   ip_address = "localhost"
  port = 5000
  def __init__(self, Address=(ip_address, port)):
    self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    self.s.connect(Address)

  def send(self, message):
    self.s.send(message)
  
print("Initiating Client Viewer")
c = Client_Viewer()
print("Client Connected to the Server")

data = b''
stopFlag = False

# Loop for receiving input, the input is added to a queue
def getInput():
    global stopFlag
    while True:
        try:
            command = input()

            if command == 'quit':
                stopFlag = True
                return

            c.send(command.encode('utf-8'))
        except KeyboardInterrupt:
            stopFlag = True
            return

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
            # print(frame_data)
            # print(int.from_bytes(frame_data, 'big'))

            # print(frame_data)

            # # Extract frame
            # # frame = pickle.loads(frame_data)
            # frameBytes = base64.b64decode(frame_data) # If doing the raw encoded data
            # # print(frameBytes)
            # # print(type(frameBytes))
            # # frame = Image.open(frameBytes)
            # img_as_np = np.frombuffer(frameBytes, dtype=np.uint8)
            # # frame = cv2.imdecode(img_as_np, cv2.IMREAD_COLOR)
            # frame = cv2.imdecode(img_as_np, flags=1)
            # # cv2.imwrite("./0.jpg", frame)

            # If going the direct encode/decode to get frameBytes
            frameBytes = base64.b64decode(frame_data) # If doing the raw encoded data

            # If going the json route to get frameBytes
            # jsonData = json.load(data.decode('utc-8'))
            # frameBytes = base64.b64decode(jsonData['img'].decode('utc-8'))

            img_as_np = np.frombuffer(frameBytes, dtype=np.uint8)
            frame = cv2.imdecode(img_as_np, flags=1)

            # Display
            cv2.imshow("Frame", frame)
            cv2.waitKey(1)

        except KeyboardInterrupt:
            cv2.destroyAllWindows()
            break



input_thread = threading.Thread(target=getInput)
video_thread = threading.Thread(target=showVideo)

input_thread.start()
video_thread.start()


 
 