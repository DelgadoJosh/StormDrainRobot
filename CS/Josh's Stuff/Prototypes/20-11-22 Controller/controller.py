from inputs import get_gamepad 
import time

if __name__ == '__main__':
  while True:
    events = get_gamepad()
    # print(len(events))
    for event in events:
      print(event.ev_type, event.code, event.state)
    time.sleep(1)