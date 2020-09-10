import socket 

class Client():
  ip_address = "10.0.0.1" # The one you're connecting to
  port = 5000
  def __init__(self, Address=(ip_address,port)):
    self.s = socket.socket() 
    self.s.connect(Address)

print("Initiating Client")
c = Client()
print("Client Initiated")
