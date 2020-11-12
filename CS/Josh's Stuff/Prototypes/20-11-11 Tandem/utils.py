# The purpose of this is for support functions
# Parsing the data
DELIMITER = " "

# This is the cheeseiest thing I'm doing and I'm almost ashamed
def isFloat(string):
    try:
        float(string)
        return True 
    except ValueError:
        return False

data_len = 1
def isFormatted(splitData):
    # Returns if data is in proper format
    # In this case it's two floats, separated by one space
    # return  len(splitData) >= 2 and isFloat(splitData[0]) and isFloat(splitData[1])

    # In this case it's data_len floats, separated by one space
    if len(splitData) >= data_len:
        for i in range(data_len):
            if not isFloat(splitData[i]):
                return False
        return True 
    return False
    # return len(splitData) >= 1 and isFloat(splitData[0])

def isInMargins(parsedData):
    for i in data_len:
        if abs(parsedData[i]) > 1:
            return False
        return True
    # return abs(parsedData[0]) <= 1 #and abs(parsedData[1]) <= 1

def parse(data):
    # This will take the data, split it into a pair of elements needed
    # Returns None if it's not properly parsed
    splitData = data.split(DELIMITER)

    if (isFormatted(splitData)):
        parsedData = []
        for i in data_len:
            parsedData.append(float(splitData[i]))
        # parsedData.append(float(splitData[0])) 
        # parsedData.append(float(splitData[1]))
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
