# import adc 
# import lights 
# import motors
import servos 
import teensy 
import time

def testTeensy():
    print("Testing Teensy\n")
    for i in range(10):
        value = teensy.readEncoder()
        print(f"Encoder Reading: {value}")
        time.sleep(.1)
    print("\nCompleted Teensy Testing\n")

print("Beginning test")
# adc.testADC()
# lights.testLights()
# motors.testMotors()
# servos.testServos()
servos.runTestLoop() 
# testTeensy()
