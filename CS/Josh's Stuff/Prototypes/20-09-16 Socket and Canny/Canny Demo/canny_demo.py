# My personal canny demo

import cv2 as cv 
import argparse 

max_low_threshold = 200
window_name = "Edge Map"
slider_title = "Min Threshold:"
ratio = 3
kernel_size = 3

# def CannyThreshold(source, source_gray, low_threshold):
def CannyThreshold(low_threshold):
  # Blurs the image
  img_blur = cv.blur(source_gray, (3, 3))

  # Runs the edge detection algorithm
  detected_edges = cv.Canny(img_blur, low_threshold, low_threshold*ratio, kernel_size)

  # The mask is on if there's an edge there
  mask = (detected_edges != 0)

  # Creates an output 
  output = source*(mask[:, :, None].astype(source.dtype))

  # return output
  cv.imshow(window_name, output)

parser = argparse.ArgumentParser(description="Code for Canny Edge Detector")
parser.add_argument("--input", help="Path to input image.", default="Crack1.jpg")
args = parser.parse_args()

source = cv.imread(cv.samples.findFile(args.input))
if source is None:
  print("Could not open or find the image: ", args.input)
  exit(0)

source_gray = cv.cvtColor(source, cv.COLOR_BGR2GRAY)

cv.namedWindow(window_name)
cv.createTrackbar(slider_title, window_name, 0, max_low_threshold, CannyThreshold)

CannyThreshold(0)
cv.waitKey()

