import json
import base64

data = {} 
PATH = "penguin.jpg"
PATH = "/home/teamblack/Desktop/TeamBlack/Github Repo/StormDrainRobot/CS/Josh's Stuff/Prototypes/20-11-09 JSON Attempt/penguin.jpg"
with open(PATH, mode='rb') as file:
    img = file.read() 
# data['img'] = base64.encodebytes(img).decode('utf-8')

# print(json.dumps(data))
print(type(img))

# Convert to base64 encoding and show start of data
jpg_as_text = base64.b64encode(img)
print(jpg_as_text[:80])

# Convert back to binary
jpg_original = base64.b64decode(jpg_as_text)

# Write to a file to show conversion worked
OUT_PATH = "testOut.jpg"
OUT_PATH = "/home/teamblack/Desktop/TeamBlack/Github Repo/StormDrainRobot/CS/Josh's Stuff/Prototypes/20-11-09 JSON Attempt/testOut2.jpg"
with open(OUT_PATH, 'wb') as f_output:
    f_output.write(jpg_original)




