# The purpose of this is for support functions
# Parsing the data
DELIMITER = " "
LIGHTS_INDEX = 0
MOTOR_LEFT_INDEX = 1
MOTOR_RIGHT_INDEX = 2
SERVO_HORIZONTAL_INDEX = 3
SERVO_VERTICAL_INDEX = 4
ATTACHMENT_INDEX = 5

# The Float Values
FLOATS = [LIGHTS_INDEX, MOTOR_LEFT_INDEX, MOTOR_RIGHT_INDEX, SERVO_HORIZONTAL_INDEX, SERVO_VERTICAL_INDEX, ATTACHMENT_INDEX]

# Defining the bounds of values intended
POSITIVE_PERCENTAGES = [LIGHTS_INDEX, ATTACHMENT_INDEX]
PERCENTAGES = [MOTOR_LEFT_INDEX, MOTOR_RIGHT_INDEX]
HORIZONTAL_ANGLES = [SERVO_HORIZONTAL_INDEX]  # In the future, may want to make vertical index have custom bounds
VERTICAL_ANGLES = [SERVO_VERTICAL_INDEX]

MAX_HORIZONTAL_ANGLE = 180
MAX_VERTICAL_ANGLE = 90

data_len = len(POSITIVE_PERCENTAGES) + len(PERCENTAGES) + len(HORIZONTAL_ANGLES) + len(VERTICAL_ANGLES)

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
    for i in POSITIVE_PERCENTAGES:
        if not (parsedData[i] >= 0 and parsedData[i] <= 1):
            isInMargins = False

    for i in PERCENTAGES:
        if not (abs(parsedData[i]) <= 1):
            isInMargins = False

    for i in HORIZONTAL_ANGLES:
        if not( parsedData[i] >= 0 and parsedData[i] <= MAX_HORIZONTAL_ANGLE):
            isInMargins = False
    
    for i in VERTICAL_ANGLES:
        if not( parsedData[i] >= 0 and parsedData[i] <= MAX_VERTICAL_ANGLE):
            isInMargins = False
    
    return isInMargins

def parse(data):
    # This will take the data, split it into a pair of elements needed
    # Returns None if it's not properly parsed
    splitData = data.split(DELIMITER)

    if (isFormatted(splitData)):
        parsedData = []
        for i in range(data_len):
            parsedData.append(float(splitData[i]))

        if (isInMargins(parsedData)):
            return parsedData 
        else:
            # print(f"{data} has bad values")
            return None
    else:
        # print(f"{data} is not formatted")
        return None

def parseTitle(data):
    try:
        splitData = data.split("|")
        command = splitData[0]

        if command == 'NAME':
            pipe_name = splitData[1]

            datetimenow = splitData[2]
            date_split = str(datetimenow).split(" ")
            date = date_split[0]
            timeStartedRunString = date_split[1]
            timeStartedRunString = timeStartedRunString.replace('.', " ")
            timeStartedRunString = timeStartedRunString.split(" ")[0]  # Throwing away the milliseconds
            timeStartedRunString = timeStartedRunString.replace(":", "-")
            name = date + "_" + timeStartedRunString

            splitData[0] = pipe_name
            splitData[1] = name
            return splitData
    except: 
        return None

def cleanup(byteData):
    # Taking in a string of b'string'
    # Scrape off the begining 2 characters, and the end '
    return byteData[2:len(byteData)-1]
