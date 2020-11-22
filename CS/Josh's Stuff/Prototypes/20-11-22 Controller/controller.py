from inputs import get_gamepad 

if __name__ == '__main__':
  while True:
    for event in events:
      print(event.ev_type, event.code, event.state)
