import cv2
import numpy as np
# Function to update the threshold values based on trackbar positions
def update_threshold(value):
    global thresh_1
    thresh_1 = cv2.getTrackbarPos("Threshold 1", "Resulting_image")

    _, imagethreshold = cv2.threshold(imagegray, thresh_1, 255, cv2.THRESH_BINARY)
    cv2.imshow("Resulting_image", imagethreshold)

# Create a window for displaying the image
cv2.namedWindow("Resulting_image")
thresh_1 = 0
# Create trackbars for thresh_1 and thresh_2
cv2.createTrackbar("Threshold 1", "Resulting_image", thresh_1, 255, update_threshold)

# Read the image
imageread = cv2.imread('./dataset/raw_02.jpeg')

# Convert the input image to grayscale

hsv = cv2.cvtColor(imageread,cv2.COLOR_BGR2HSV)

lower_blue_contour = np.array([102, 69, 0])
upper_blue_contour = np.array([147, 255, 255])

mask = cv2.inRange(hsv, lower_blue_contour, upper_blue_contour)

res = cv2.bitwise_and(imageread,imageread,mask = mask)
imagegray = cv2.cvtColor(res, cv2.COLOR_BGR2GRAY)

cv2.imshow("res",res)

# Get the initial threshold values
#thresh_1 = cv2.getTrackbarPos("Threshold 1", "Resulting_image")
thresh_1 = 47

# Threshold the grayscale image
_, imagethreshold = cv2.threshold(imagegray, thresh_1, 255, cv2.THRESH_BINARY)
imagethreshold = cv2.erode(imagethreshold, None, iterations=4)
cv2.imshow("imgthresh",imagethreshold)
# Find contours in the thresholded image
imagecontours, _ = cv2.findContours(imagethreshold, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

max_perimeter = 0
largest_contour =center= None

# 遍历每个轮廓
for cnt in imagecontours:
    perimeter = cv2.arcLength(cnt, True)
    if perimeter > max_perimeter:
        max_perimeter = perimeter
        largest_contour = cnt

epsilon = 0.01 * cv2.arcLength(largest_contour, True)
approximations = cv2.approxPolyDP(largest_contour, epsilon, True)

cv2.drawContours(imageread, [approximations], 0, (0,0,255), 3)

i, j = approximations[0][0]
print((i,j))
if len(approximations) == 3:
    print(1)
    cv2.putText(imageread, "Triangle", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1, 0, 2)
elif len(approximations) == 4:
    print(4)
    cv2.putText(imageread, "Rectangle", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1, 0, 2)
elif len(approximations) == 5:
    print(1)
    cv2.putText(imageread, "Pentagon", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1, 0, 2)
elif 6 < len(approximations) < 15:
    print(15)
    cv2.putText(imageread, "Ellipse", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 0, 0),2)

else:
    print("cir")
    cv2.putText(imageread, "Circle", (i, j), cv2.FONT_HERSHEY_COMPLEX, 1,(255, 0, 0), 2)
        

# Display the resulting image
cv2.imshow("Resulting_image", imageread)

# # Check for the 'q' key to exit the loop
while True:
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release resources
cv2.destroyAllWindows()
