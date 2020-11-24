"""Simple gamepad/joystick test example."""

from __future__ import print_function


import inputs

print("Initializing Controller")

EVENT_ABB = (
    # D-PAD, aka HAT
    ('Absolute-ABS_HAT0X', 'HX'),
    ('Absolute-ABS_HAT0Y', 'HY'),

    # Joystick (custom USB)
    ('Absolute-ABS_X', 'LX'),
    ('Absolute-ABS_Y', 'LY'),
    ('Absolute-ABS_RX', 'RX'),
    ('Absolute-ABS_RY', 'RY'),

    # Trigger buttons (custom USB)
    ('Absolute-ABS_Z', 'LT'),
    ('Absolute-ABS_RZ', 'RT'),

    # Face Buttons
    ('Key-BTN_NORTH', 'N'),
    ('Key-BTN_EAST', 'E'),
    ('Key-BTN_SOUTH', 'S'),
    ('Key-BTN_WEST', 'W'),

    # Other buttons
    ('Key-BTN_THUMBL', 'THL'),
    ('Key-BTN_THUMBR', 'THR'),
    ('Key-BTN_TL', 'TL'), # Left Bumper
    ('Key-BTN_TR', 'TR'), # Right Bumper
    ('Key-BTN_TL2', 'TL2'),
    ('Key-BTN_TR2', 'TR3'),
    ('Key-BTN_MODE', 'M'),
    ('Key-BTN_START', 'ST'),

    # PiHUT SNES style controller buttons
    ('Key-BTN_TRIGGER', 'N'),
    ('Key-BTN_THUMB', 'E'),
    ('Key-BTN_THUMB2', 'S'),
    ('Key-BTN_TOP', 'W'),
    ('Key-BTN_BASE3', 'SL'),
    ('Key-BTN_BASE4', 'ST'),
    ('Key-BTN_TOP2', 'TL'),
    ('Key-BTN_PINKIE', 'TR')
)


# This is to reduce noise from the PlayStation controllers
# For the Xbox controller, you can set this to 0
MIN_ABS_DIFFERENCE = 5


class Controller(object):
    """Simple joystick test class."""
    def __init__(self, gamepad=None, abbrevs=EVENT_ABB):
        self.btn_state = {}
        self.old_btn_state = {}
        self.abs_state = {}
        self.old_abs_state = {}
        self.abbrevs = dict(abbrevs)
        self.btn_pressed = {}
        self.btn_pressed_and_released = {}
        for key, value in self.abbrevs.items():
            if key.startswith('Absolute'):
                self.abs_state[value] = 0
                self.old_abs_state[value] = 0
            if key.startswith('Key'):
                self.btn_state[value] = 0
                self.old_btn_state[value] = 0
                self.btn_pressed[value] = False
                self.btn_pressed_and_released[value] = False
        self._other = 0
        self.gamepad = gamepad
        if not gamepad:
            self._get_gamepad()
    
    debugOutput = False

    def _get_gamepad(self):
        """Get a gamepad object."""
        try:
            self.gamepad = inputs.devices.gamepads[0]
        except IndexError:
            return
            raise inputs.UnpluggedError("No gamepad found.")

    def handle_unknown_event(self, event, key):
        """Deal with unknown events."""
        if event.ev_type == 'Key':
            new_abbv = 'B' + str(self._other)
            self.btn_state[new_abbv] = 0
            self.old_btn_state[new_abbv] = 0
            self.btn_pressed[new_abbv] = False 
            self.btn_pressed_and_released[new_abbv] = False
        elif event.ev_type == 'Absolute':
            new_abbv = 'A' + str(self._other)
            self.abs_state[new_abbv] = 0
            self.old_abs_state[new_abbv] = 0
        else:
            return None

        self.abbrevs[key] = new_abbv
        self._other += 1

        return self.abbrevs[key]

    def process_event(self, event):
        """Process the event into a state."""
        if event.ev_type == 'Sync':
            return
        if event.ev_type == 'Misc':
            return
        key = event.ev_type + '-' + event.code
        try:
            abbv = self.abbrevs[key]
        except KeyError:
            abbv = self.handle_unknown_event(event, key)
            if not abbv:
                return
        if event.ev_type == 'Key':
            self.old_btn_state[abbv] = self.btn_state[abbv]
            self.btn_state[abbv] = event.state

            if event.state == 1:
              self.btn_pressed[abbv] = True
            else:
              if self.btn_pressed[abbv]:
                self.btn_pressed_and_released[abbv] = True
                self.btn_pressed[abbv] = False

            # # Update the state of the B Button
            # if abbv == 'E':
            #     if event.state == 1:
            #         self.bPressed = True 
            #     else: 
            #         if self.bPressed:
            #             self.bPressedAndReleased = True 
            #             self.bPressed = False

            # # Update the state of the Left Bumper
            # if abbv == 'TL':
            #     if event.state == 1:
            #         self.leftBumperPressed = True 
            #     else:
            #         if self.leftBumperPressed:
            #             self.leftBumperPressedAndReleased = True 
            #             self.leftBumperPressed = False
            # # Update the state of the Right bumper
            # if abbv == 'TR':
            #     if event.state == 1:
            #         self.rightBumperPressed = True 
            #     else:
            #         if self.rightBumperPressed:
            #             self.rightBumperPressedAndReleased = True 
            #             self.rightBumperPressed = False
        if event.ev_type == 'Absolute':
            self.old_abs_state[abbv] = self.abs_state[abbv]
            self.abs_state[abbv] = event.state
            if abbv == 'HY':
                if event.state != 0:
                    self.dPadYLastNonZeroResult = event.state
            if abbv == 'HX':
                if event.state != 0:
                    self.dPadXLastNonZeroResult = event.state
        if self.debugOutput:
            self.output_state(event.ev_type, abbv)

    def format_state(self):
        """Format the state."""
        output_string = ""
        for key, value in self.abs_state.items():
            output_string += key + ':' + '{:>4}'.format(str(value) + ' ')

        for key, value in self.btn_state.items():
            output_string += key + ':' + str(value) + ' '

        return output_string

    def output_state(self, ev_type, abbv):
        """Print out the output state."""
        if ev_type == 'Key':
            if self.btn_state[abbv] != self.old_btn_state[abbv]:
                print(self.format_state())
                return

        if abbv[0] == 'H':
            print(self.format_state())
            return

        difference = self.abs_state[abbv] - self.old_abs_state[abbv]
        if (abs(difference)) > MIN_ABS_DIFFERENCE:
            print(self.format_state())

    def process_events(self):
        """Process available events."""
        try:
            events = self.gamepad.read()
        except EOFError:
            events = []
        except:
            return
        for event in events:
            self.process_event(event)

    def getLeftJoystickX(self):
        self.process_events()
        return self.abs_state['LX']

    def getLeftJoystickY(self):
        self.process_events()
        return self.abs_state['LY']

    def getRightJoystickX(self):
        self.process_events()
        return self.abs_state['RX']

    def getRightJoystickY(self):
        self.process_events()
        return self.abs_state['RY']
    
    dPadYLastNonZeroResult = 0
    def getDPadYState(self):
        if self.dPadYLastNonZeroResult != 0:
            val = self.dPadYLastNonZeroResult * -1  # Because - is up, changing it up
            self.dPadYLastNonZeroResult = 0
            return val 
        return 0
    
    dPadXLastNonZeroResult = 0
    def getDPadXState(self):
        if self.dPadXLastNonZeroResult != 0:
            val = self.dPadXLastNonZeroResult
            self.dPadXLastNonZeroResult = 0
            return val 
        return 0
    # bPressed = False
    # bPressedAndReleased = False 
    def getBPressedAndReleased(self):
        if self.btn_pressed_and_released['E']:
            self.btn_pressed_and_released['E'] = False 
            return True 
        return False
        # if self.bPressedAndReleased:
        #     self.bPressedAndReleased = False 
        #     return True
        # return False

    # leftBumperPressed = False
    # leftBumperPressedAndReleased = False 
    def getLeftBumperPressedAndReleased(self):
        if self.btn_pressed_and_released['TL']:
            self.btn_pressed_and_released['TL'] = False
            return True 
        return False
        # if self.leftBumperPressedAndReleased:
        #     self.leftBumperPressedAndReleased = False 
        #     return True 
        # return False

    # rightBumperPressed = False
    # rightBumperPressedAndReleased = False
    def getRightBumperPressedAndReleased(self):
        if self.btn_pressed_and_released['TR']:
            self.btn_pressed_and_released['TR'] = False 
            return True 
        return False
        # if self.rightBumperPressedAndReleased:
        #     self.rightBumperPressedAndReleased = False 
        #     return True 
        # return False

def main():
    """Process all events forever."""
    # jstest = JSTest()
    print("Processing all events")
    jstest = Controller()
    jstest.debugOutput = True
    while 1:
        jstest.process_events()


if __name__ == "__main__":
    # print("Initizialized controller")
    main()

print("Initialized Controller")