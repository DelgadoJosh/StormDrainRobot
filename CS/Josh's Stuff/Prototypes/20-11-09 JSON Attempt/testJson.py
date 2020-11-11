import json
import base64

data = {} 
with open('penguin.jpg', mode='rb') as file:
    img = file.read() 
# data['img'] = base64.encodebytes(img).decode('utf-8')

# print(json.dumps(data))

# Convert to base64 encoding and show start of data
jpg_as_text = base64.b64encode(img)
print(jpg_as_text[:80])

# Convert back to binary
jpg_original = base64.b64decode(jpg_as_text)

# Write to a file to show conversion worked
with open('testOut.jpg', 'wb') as f_output:
    f_output.write(jpg_original)




