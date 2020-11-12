# The purpose of this is for support functions
# Parsing the data
DELIMITER = " "
LIGHTS_INDEX = 0
MOTOR_LEFT_INDEX = 1
MOTOR_RIGHT_INDEX = 2
SERVO_LEFT_INDEX = 3
SERVO_RIGHT_INDEX = 4

# The Float Values
FLOATS = [LIGHTS_INDEX, MOTOR_LEFT_INDEX, MOTOR_RIGHT_INDEX, SERVO_LEFT_INDEX, SERVO_RIGHT_INDEX]

# Defining the bounds of values intended
PERCENTAGES = [LIGHTS_INDEX, MOTOR_LEFT_INDEX, MOTOR_RIGHT_INDEX]
ANGLES = [SERVO_LEFT_INDEX, SERVO_RIGHT_INDEX]

data_len = len(PERCENTAGES) + len(ANGLES)

# This is the cheeseiest thing I'm doing and I'm almost ashamed
def isFloat(string):
    try:
        float(string)
        return True 
    except ValueError:
        return False

def isFormatted(splitData):
    # Returns if data is in proper format
    # In this case it's data_len floats, separated by one space
    isFormatted = False
    if len(splitData) >= data_len:
        isFormatted = True
        for i in FLOATS:
            if not isFloat(splitData[i]):
                isFormatted=  False
    return isFormatted

def isInMargins(parsedData):
    isInMargins = True
    for i in PERCENTAGES:
        if not (abs(parsedData[i]) <= 1):
            isInMargins = False

    for i in ANGLES:
        if not( parsedData[i] >= 0 and parsedData[i] <= MAX_ANGLE):
            isInMargins = False
    
    return isInMargins

def parse(data):
    # This will take the data, split it into a pair of elements needed
    # Returns None if it's not properly parsed
    splitData = data.split(DELIMITER)

    if (isFormatted(splitData)):
        parsedData = []
        for i in data_len:
            parsedData.append(float(splitData[i]))
            
        if (isInMargins(parsedData)):
            return parsedData 
        else:
            # print(f"{data} has bad values")
            return None
    else:
        # print(f"{data} is not formatted")
        return None

def cleanup(byteData):
    # Taking in a string of b'string'
    # Scrape off the begining 2 characters, and the end '
    return byteData[2:len(byteData)-1]
