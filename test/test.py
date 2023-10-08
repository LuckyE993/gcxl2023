import cv2 as cv
import numpy as np

# Function to update the HSV values when trackbars are moved
def update_hsv_values(x):
    global lower_blue, upper_blue, erode_value, dilate_value
    lower_blue[0] = cv.getTrackbarPos('Hue Lower', 'Trackbars')
    upper_blue[0] = cv.getTrackbarPos('Hue Upper', 'Trackbars')
    lower_blue[1] = cv.getTrackbarPos('Saturation Lower', 'Trackbars')
    upper_blue[1] = cv.getTrackbarPos('Saturation Upper', 'Trackbars')
    lower_blue[2] = cv.getTrackbarPos('Value Lower', 'Trackbars')
    upper_blue[2] = cv.getTrackbarPos('Value Upper', 'Trackbars')
    erode_value = cv.getTrackbarPos('Erode', 'Trackbars')
    dilate_value = cv.getTrackbarPos('Dilate', 'Trackbars')

    # Apply the updated HSV values to the thresholding
    mask = cv.inRange(hsv, lower_blue, upper_blue)
    # Apply morphological operations
    mask = cv.erode(mask, None, iterations=erode_value)
    mask = cv.dilate(mask, None, iterations=dilate_value)
    
    # Find contours and draw them on the original image
    contours, hierachy = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    # res = cv.bitwise_and(img, img, mask=mask)
    res = cv.drawContours(img.copy(), contours, -1, (255,0, 0), 4)
    
    # Show the result
    cv.imshow('res', res)
path = '/home/luckye/Desktop/test/color_1.jpg'
img = cv.imread(path)
hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

# Initial HSV threshold values
lower_blue = np.array([102, 69, 0])
upper_blue = np.array([147, 255, 255])

lower_green = np.array([38, 92, 46])
upper_green = np.array([82, 255, 255])

lower_red_1 = np.array([0, 43, 46])
upper_red_1 = np.array([10, 255, 255])

lower_red_2 = np.array([156, 43, 46])
upper_red_2 = np.array([180, 255, 255])


# Initial values for erode and dilate
erode_value = 0
dilate_value = 0


# Create a window to display trackbars
cv.namedWindow('Trackbars')

# Create trackbars for adjusting HSV values
cv.createTrackbar('Hue Lower', 'Trackbars', lower_blue[0], 179, update_hsv_values)
cv.createTrackbar('Hue Upper', 'Trackbars', upper_blue[0], 179, update_hsv_values)
cv.createTrackbar('Saturation Lower', 'Trackbars', lower_blue[1], 255, update_hsv_values)
cv.createTrackbar('Saturation Upper', 'Trackbars', upper_blue[1], 255, update_hsv_values)
cv.createTrackbar('Value Lower', 'Trackbars', lower_blue[2], 255, update_hsv_values)
cv.createTrackbar('Value Upper', 'Trackbars', upper_blue[2], 255, update_hsv_values)
cv.createTrackbar('Erode', 'Trackbars', erode_value, 10, update_hsv_values)
cv.createTrackbar('Dilate', 'Trackbars', dilate_value, 10, update_hsv_values)


#Initialize the mask and result using the initial HSV values
mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
res = cv.bitwise_and(img, img, mask=mask_blue)
median = cv.medianBlur(mask_blue, 9)
mask_blue = cv.erode(mask_blue, None, iterations=4)  #腐蚀操作    
mask_blue = cv.dilate(mask_blue, None, iterations=8)  #膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
contours_blue, hierachy = cv.findContours(mask_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
res = cv.drawContours(img, contours_blue, -1,(0,0,0), 4)
moments = cv.moments(contours_blue[0])
# Calculate the centroid (barycenter) coordinates
centroid_x = int(moments["m10"] / moments["m00"])
centroid_y = int(moments["m01"] / moments["m00"])
cv.circle(img, (centroid_x, centroid_y), 10, (255, 0, 0), -1)
print("Blue: "+' ('+str(centroid_x)+','+str(centroid_y)+')') # 输出各个中心点

#Initialize the mask and result using the initial HSV values
mask_green = cv.inRange(hsv, lower_green, upper_green)
res = cv.bitwise_and(img, img, mask=mask_green)
median = cv.medianBlur(mask_green, 9)
mask_green = cv.erode(mask_green, None, iterations=0)  #腐蚀操作    
mask_green = cv.dilate(mask_green, None, iterations=0)  #膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
contours_green, hierachy = cv.findContours(mask_green, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
#contours_green = max(contours_green, key=lambda x: len(x))
res = cv.drawContours(img, contours_green, -1,(0,255,0), 4)
moments = cv.moments(contours_green[0])
# Calculate the centroid (barycenter) coordinates
centroid_x = int(moments["m10"] / moments["m00"])
centroid_y = int(moments["m01"] / moments["m00"])
cv.circle(img, (centroid_x, centroid_y), 10, (0, 255, 0), -1)
print("Green: "+' ('+str(centroid_x)+','+str(centroid_y)+')') # 输出各个中心点


#Initialize the mask and result using the initial HSV values
#mask_red_1 = cv.inRange(hsv, lower_red_1, upper_red_1)
#mask_red_2 = cv.inRange(hsv, lower_red_2, upper_red_2)
mask_red = cv.inRange(hsv, lower_red_2, upper_red_2)
#mask_red = cv.bitwise_or(mask_red_1,mask_red_2)
res = cv.bitwise_and(img, img, mask=mask_red)
median = cv.medianBlur(mask_red, 9)
mask_red = cv.erode(mask_red, None, iterations=2)  #腐蚀操作    
mask_red = cv.dilate(mask_red, None, iterations=5)  #膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
contours_red, hierachy = cv.findContours(mask_red, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
res = cv.drawContours(img, contours_red, -1,(0,0,255), 4)

longest_contour = max(contours_red, key=lambda x: len(x))
moments = cv.moments(longest_contour)
# Calculate the centroid (barycenter) coordinates
centroid_x = int(moments["m10"] / moments["m00"])
centroid_y = int(moments["m01"] / moments["m00"])
cv.circle(img, (centroid_x, centroid_y), 10, (0, 0, 255), -1)
print("Red: "+' ('+str(centroid_x)+','+str(centroid_y)+')') # 输出各个中心点

cv.imshow('img', img)

cv.waitKey(0)
cv.destroyAllWindows()
