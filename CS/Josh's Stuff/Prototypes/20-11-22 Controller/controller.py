from inputs import get_gamepad 

if __name__ == '__main__':
  while True:
    events = get_gamepad()
    for event in events:
      print(event.ev_type, event.code, event.state)
