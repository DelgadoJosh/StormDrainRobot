from inputs import get_key

if __name__ == '__main__':
  while True:
    events = get_key()
    for event in events:
      print(event.ev_type, event.code, event.state)

