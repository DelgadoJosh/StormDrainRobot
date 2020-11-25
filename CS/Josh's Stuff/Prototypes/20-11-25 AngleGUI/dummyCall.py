import testgui 

print("Initializing Script")
while True: 
  inputVal = input() 
  
  try: 
    inputVal = float(inputVal) 
    testgui.app.changeAngle(inputVal)
  except: 
    continue 