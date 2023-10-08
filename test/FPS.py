import numpy as np
import cv2 as cv
cap = cv.VideoCapture(0)
#cap.set(cv.CAP_PROP_FOURCC, cv.VideoWriter_fourcc('M', 'J', 'P', 'G'))
cap.set(cv.CAP_PROP_FPS, 30)

count = 0

if not cap.isOpened():
 print("Cannot open camera")
 exit()
while True:
    # Capture frame-by-frame
    ret, img = cap.read()
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


    # # Create a window to display trackbars
    # cv.namedWindow('Trackbars')

    # # Create trackbars for adjusting HSV values
    # cv.createTrackbar('Hue Lower', 'Trackbars', lower_green[0], 179, update_hsv_values)
    # cv.createTrackbar('Hue Upper', 'Trackbars', upper_green[0], 179, update_hsv_values)
    # cv.createTrackbar('Saturation Lower', 'Trackbars', lower_green[1], 255, update_hsv_values)
    # cv.createTrackbar('Saturation Upper', 'Trackbars', upper_green[1], 255, update_hsv_values)
    # cv.createTrackbar('Value Lower', 'Trackbars', lower_blue[2], 255, update_hsv_values)
    # cv.createTrackbar('Value Upper', 'Trackbars', upper_green[2], 255, update_hsv_values)
    # cv.createTrackbar('Erode', 'Trackbars', erode_value, 10, update_hsv_values)
    # cv.createTrackbar('Dilate', 'Trackbars', dilate_value, 10, update_hsv_values)


    #Initialize the mask and result using the initial HSV values
    mask_blue = cv.inRange(hsv, lower_blue, upper_blue)
    res = cv.bitwise_and(img, img, mask=mask_blue)
    median = cv.medianBlur(mask_blue, 9)
    mask_blue = cv.erode(mask_blue, None, iterations=2)  #腐蚀操作    
    mask_blue = cv.dilate(mask_blue, None, iterations=8)  #膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    contours_blue, hierachy = cv.findContours(mask_blue, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    res = cv.drawContours(img, contours_blue, -1,(255,0,0), 4)
    moments = cv.moments(contours_blue[0])
    # Calculate the centroid (barycenter) coordinates
    centroid_x_b = int(moments["m10"] / moments["m00"])
    centroid_y_b = int(moments["m01"] / moments["m00"])
    cv.circle(img, (centroid_x_b, centroid_y_b), 10, (255, 0, 0), -1)
    if count > 10:
        print("Blue: "+' ('+str(centroid_x_b)+','+str(centroid_y_b)+')') # 输出各个中心点

    #Initialize the mask and result using the initial HSV values
    mask_green = cv.inRange(hsv, lower_green, upper_green)
    res = cv.bitwise_and(img, img, mask=mask_green)
    median = cv.medianBlur(mask_green, 9)
    mask_green = cv.erode(mask_green, None, iterations=0)  #腐蚀操作    
    mask_green = cv.dilate(mask_green, None, iterations=3)  #膨胀操作，其实先腐蚀再膨胀的效果是开运算，去除噪点
    contours_green, hierachy = cv.findContours(mask_green, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)
    #contours_green = max(contours_green, key=lambda x: len(x))
    res = cv.drawContours(img, contours_green, -1,(0,255,0), 4)
    moments = cv.moments(contours_green[0])
    # Calculate the centroid (barycenter) coordinates

    centroid_x_g = int(moments["m10"] / moments["m00"])
    centroid_y_g = int(moments["m01"] / moments["m00"])
    cv.circle(img, (centroid_x_g, centroid_y_g), 10, (0, 255, 0), -1)
    if count > 10:
        print("Green: "+' ('+str(centroid_x_g)+','+str(centroid_y_g)+')') # 输出各个中心点
            

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
    centroid_x_r = int(moments["m10"] / moments["m00"])
    centroid_y_r = int(moments["m01"] / moments["m00"])
    cv.circle(img, (centroid_x_r, centroid_y_r), 10, (0, 0, 255), -1)
    if count > 10:
       count = 0
       print("Red: "+' ('+str(centroid_x_r)+','+str(centroid_y_r)+')') # 输出各个中心点

    cv.imshow('img', img)


    
    count+=1


    if cv.waitKey(1) == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv.destroyAllWindows()


