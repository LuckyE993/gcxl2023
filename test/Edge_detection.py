import numpy as np
import cv2 as cv
import matplotlib.pyplot as plt

# Callback function for the first trackbar
def min_threshold_callback(x):
    global min_threshold
    min_threshold = x
    update_canny()

# Callback function for the second trackbar
def max_threshold_callback(x):
    global max_threshold
    max_threshold = x
    update_canny()

# Function to update the Canny edge detection
def update_canny():
    edges = cv.Canny(img, min_threshold, max_threshold)
    cv.imshow('Edge Image', edges)
path = '/home/luckye/Desktop/test/BGR_COLOR.jpg'
img = cv.imread(path,cv.IMREAD_GRAYSCALE)
# Load the image
#img = cv.imread('Edge_detect2.jpeg', cv.IMREAD_GRAYSCALE)
assert img is not None, "file could not be read, check with os.path.exists()"

# Create a resizable window for the original image
cv.namedWindow('Original Image', cv.WINDOW_NORMAL)
cv.resizeWindow('Original Image', 400, 400)  # Adjust the window size as needed

# Create a resizable window for the edge image
cv.namedWindow('Edge Image', cv.WINDOW_NORMAL)
cv.resizeWindow('Edge Image', 400, 400)  # Adjust the window size as needed

# Initialize the thresholds
min_threshold = 100
max_threshold = 200

# Create trackbars for threshold values
cv.createTrackbar('Min Threshold', 'Edge Image', min_threshold, 500, min_threshold_callback)
cv.createTrackbar('Max Threshold', 'Edge Image', max_threshold, 500, max_threshold_callback)

# Initial Canny edge detection
update_canny()

# Display the original image
cv.imshow('Original Image', img)

# Wait for a key event and close the window when a key is pressed
cv.waitKey(0)
cv.destroyAllWindows()
