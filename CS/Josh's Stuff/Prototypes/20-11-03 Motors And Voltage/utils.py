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

def isFormatted(splitData):
    # Returns if data is in proper format
    # In this case it's two floats, separated by one space
    return  len(splitData) >= 2 and isFloat(splitData[0]) and isFloat(splitData[1])

def isInMargins(parsedData):
    return abs(parsedData[0]) <= 1 and abs(parsedData[1]) <= 1

def parse(data):
    # This will take the data, split it into a pair of elements needed
    # Returns None if it's not properly parsed
    splitData = data.split(DELIMITER)

    if (isFormatted(splitData)):
        parsedData = []
        parsedData.append(float(splitData[0])) 
        parsedData.append(float(splitData[1]))
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
    # Scrape off the begining 2 strings, and the end
    return byteData[2:len(byteData)-1]
