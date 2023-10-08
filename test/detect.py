import numpy as np
import cv2 as cv

Vision_Mode = True
DebugMode = False

frame_width = 640 / 2 # 获取宽度
frame_height = 480 / 2 # 获取高度
# Initial HSV threshold values
lower_blue_contour = np.array([102, 69, 0])
upper_blue_contour = np.array([147, 255, 255])

lower_green_contour = np.array([38, 92, 46])
upper_green_contour = np.array([82, 255, 255])

lower_red_1_contour = np.array([0, 43, 46])
upper_red_1_contour = np.array([10, 255, 255])

lower_red_2_contour = np.array([156, 43, 46])
upper_red_2_contour = np.array([180, 255, 255])

lower_blue_circle = np.array([90, 0, 0])
upper_blue_circle = np.array([150, 255, 255])
lower_green_circle = np.array([38, 0, 46])
upper_green_circle = np.array([82, 255, 255])
lower_red_1_circle = np.array([0, 0, 46])
upper_red_1_circle = np.array([15, 255, 255])
lower_red_2_circle = np.array([156, 0, 46])
upper_red_2_circle = np.array([180, 255, 255])

def detect_and_draw_circles(img_path,color):
    # Create a window to display trackbars   
    img = img_path
    # 读取图像
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    # Initial HSV threshold values
    

    if color is 'B':
        mask_blue = cv.inRange(hsv, lower_blue_circle, upper_blue_circle)
        res = cv.bitwise_and(img, img, mask=mask_blue)
    elif color is 'G':
        mask_green = cv.inRange(hsv, lower_green_circle, upper_green_circle)
        res = cv.bitwise_and(img, img, mask=mask_green)
    elif color is 'R':
        mask_red_1 = cv.inRange(hsv, lower_red_1_circle, upper_red_1_circle)
        mask_red_2 = cv.inRange(hsv, lower_red_2_circle, upper_red_2_circle)
        mask_red = cv.bitwise_or(mask_red_1,mask_red_2)
        res = cv.bitwise_and(img, img, mask=mask_red)
    #cv.imshow('detected circles', res)
     # 将结果转换为灰度图像
    img_gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
    
    img_gray = cv.medianBlur(img_gray, 5)
    #cv.imshow('detected circles', img_gray)q=
    if Vision_Mode:
        cimg = cv.cvtColor(img_gray, cv.COLOR_GRAY2BGR)
    circles = cv.HoughCircles(img_gray, cv.HOUGH_GRADIENT_ALT, 1, 20,
                              param1=50, param2=0.8, minRadius=30, maxRadius=0)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        all_centers = []

        for circle in circles[0, :]:
            center = (circle[0], circle[1])
            all_centers.append(center)
            # draw the outer circle
            if Vision_Mode:
                cv.circle(img, center, circle[2], (0, 255, 0), 2)
            # draw the center of the circle
            # cv.circle(cimg, center, 2, (0, 0, 255), 3)

        average_center = tuple(np.mean(all_centers, axis=0, dtype=np.int))
        if Vision_Mode:
            cv.circle(img, average_center, 5, (255, 0, 0), -1)
        print("center " + color + ": " + str(average_center))
        if Vision_Mode:
            cv.imshow('detected circles', img)
    else:
        print("Not detected.")
        if Vision_Mode:
            cv.imshow('detected circles', img)

def contour_detect(img_path,color):
    img = img_path
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    if color is 'B':
        mask = cv.inRange(hsv, lower_blue_contour, upper_blue_contour)
    elif color is 'G':  
        mask = cv.inRange(hsv, lower_green_contour, upper_green_contour)
    elif color is 'R':
        mask_red_1 = cv.inRange(hsv, lower_red_1_contour, upper_red_1_contour)
        mask_red_2 = cv.inRange(hsv, lower_red_2_contour, upper_red_2_contour)
        mask = cv.bitwise_or(mask_red_1,mask_red_2)

    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_perimeter = 0
    largest_contour =center= None

    # 遍历每个轮廓
    for cnt in contours:
        perimeter = cv.arcLength(cnt, True)
        if perimeter > max_perimeter:
            max_perimeter = perimeter
            largest_contour = cnt
    
    if largest_contour is not None:
        # 计算轮廓的中心坐标
        M = cv.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            center = (cx, cy)
        epsilon = 0.05 * max_perimeter
        approx = cv.approxPolyDP(largest_contour, epsilon, True)
        # 绘制近似的轮廓
        if Vision_Mode:
            img = cv.drawContours(img, [approx], -1, (0, 0, 255), 4)
            cv.circle(img, center, 5, (0, 255, 0), -1)
        print("Center "+color+": "+str(center))
    else:
        print("Not Detected.")
    if Vision_Mode:
        cv.imshow('Contours', img)

# 流程：
# 提前设置灰度-二值化阈值
# 原图像转HSV->提取对应颜色->与原图像相与获得颜色->转灰度图->腐蚀->寻找轮廓->筛选最大面积的轮廓
# ->多边形拟合(再议，或可以直接求中心)->求中心

if DebugMode:
    cv.namedWindow("Resulting_image")
    def update_threshold(value):
        global thresh_Debug
        thresh_Debug = cv.getTrackbarPos("Threshold 1", "Resulting_image")
    thresh_Debug = 0
    # Create trackbars for thresh_1 and thresh_2
    cv.createTrackbar("Threshold 1", "Resulting_image", thresh_Debug, 255, update_threshold)   
    
def contour_detect_v2(img_path,color):
    img = img_path
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    if color is 'B':
        mask = cv.inRange(hsv, lower_blue_contour, upper_blue_contour)
    elif color is 'G':  
        mask = cv.inRange(hsv, lower_green_contour, upper_green_contour)
    elif color is 'R':
        mask_red_1 = cv.inRange(hsv, lower_red_1_contour, upper_red_1_contour)
        mask_red_2 = cv.inRange(hsv, lower_red_2_contour, upper_red_2_contour)
        mask = cv.bitwise_or(mask_red_1,mask_red_2)

    res = cv.bitwise_and(img,img,mask = mask)
    if Vision_Mode:
        cv.imshow("inrange_res", res)

    imagegray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)

    if color is 'B':
        thresh = 60
    elif color is 'G':  
        thresh = 70
    elif color is 'R':
        thresh = 64

    if DebugMode:
        thresh = cv.getTrackbarPos("Threshold 1", "Resulting_image")

    _, imagethreshold = cv.threshold(imagegray, thresh, 255, cv.THRESH_BINARY)

    imagethreshold = cv.erode(imagethreshold, None, iterations=4)
    if Vision_Mode:
        cv.imshow("erode_res", imagethreshold)
    imagecontours, _ = cv.findContours(imagethreshold, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_NONE)

    max_perimeter = 0
    largest_contour =center= None

    # 遍历每个轮廓
    for cnt in imagecontours:
        perimeter = cv.arcLength(cnt, True)
        if perimeter > max_perimeter:
            max_perimeter = perimeter
            largest_contour = cnt
    if largest_contour is not None:
        M = cv.moments(largest_contour)
        if M["m00"] != 0:
            cx = int(M["m10"] / M["m00"])
            cy = int(M["m01"] / M["m00"])
            #center = (cx, cy)
            x_offset = cx - frame_width
            y_offset = cy - frame_height
            x_percentage_offset = (x_offset / frame_width) * 100
            y_percentage_offset = -(y_offset / frame_height) * 100
            center = (x_percentage_offset,y_percentage_offset)
            if Vision_Mode:
                cv.circle(img, (cx,cy), 5, (0, 255, 0), -1)

        epsilon = 0.01 * cv.arcLength(largest_contour, True)
        approximations = cv.approxPolyDP(largest_contour, epsilon, True)

        if Vision_Mode:
            cv.drawContours(img, [approximations], 0, (0,0,255), 3)
            cv.imshow("Resulting_image", img)
        print("Center "+color+": "+str(center))
    else:
        print("Not Detected.")
        if Vision_Mode:
            cv.imshow("Resulting_image", img)



                  
cap = cv.VideoCapture(0)
cap.set(cv.CAP_PROP_FPS, 30)

while True:
    # Capture frame-by-frame
    ret, img = cap.read()
    
    #detect_and_draw_circles(img,'G')
    contour_detect_v2(img,'B')

    if Vision_Mode:
        # 检查是否按下 'q' 键来退出循环
        if cv.waitKey(1) & 0xFF == ord('q'):
            break

# 释放摄像头资源和关闭窗口
cap.release()
if Vision_Mode:
    cv.destroyAllWindows()
