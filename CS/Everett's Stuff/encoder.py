from gpiozero import DigitalInputDevice
from gpiozero.pins.native import NativeFactory
import time
    
if __name__ == "__main__":
    dist = 18.85 / 12 # Cicumference of the wheel in in/12 to convert to feet
    factory = NativeFactory() # Necessary for making into exe
    A = DigitalInputDevice(pin = 14, pin_factory=factory) # Setup the input line
    count = 0
    total = 0
    start = time.time()
    while(True):
        if(count > 1440/4): # This gearbox has 1440 ticks per rotation
            feetPerMinute = dist * 60 / (time.time() - start)
            print("Feet Per Minute: {:.2f}".format(feetPerMinute)) #Seconds per rotation
            start = time.time() # Reset time
            count = 0
        A.wait_for_active() # Only count everytime the values swaps
        A.wait_for_inactive()
        count += 1
