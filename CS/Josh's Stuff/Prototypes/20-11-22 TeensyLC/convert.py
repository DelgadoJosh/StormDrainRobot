len = 32
def convertToCharArr(number):
  arr = []
  for i in range(len):
    mod = number % 255 
    number //= 255 
    arr.append(mod)
  return arr 

def convertToNum(arr):
  num = 0
  for i in range(len-1, 0-1, -1):
    num *= 255
    num += arr[i] 
  return num
    
num = 1234 
arr = convertToCharArr(num) 
num = convertToNum(arr)

print(arr) 
print(num)