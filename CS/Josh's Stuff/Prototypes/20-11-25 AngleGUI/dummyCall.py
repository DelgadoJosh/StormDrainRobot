import testgui 

print("Initializing Script")
while True: 
  inputVal = input() 
  if inputVal == 'quit':
    break
  
  try: 
    inputVal = float(inputVal) 
    testgui.app.changeAngle(inputVal)
  except: 
    continue 

print("Quit the script. Make sure GUI is closed")