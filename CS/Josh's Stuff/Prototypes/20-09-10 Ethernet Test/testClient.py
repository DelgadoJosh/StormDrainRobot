import socket 

class Client():
  ip_address = "10.0.0.2" # The one you're connecting to
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
while True:
  command = input()

  if (command == "quit"):
    break

  c.send(command.encode('utf-8')) # Note how it must be a byte stream.

  data = c.s.recv(1024)
  print("Received:", repr(data))



