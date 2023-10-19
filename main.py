import parameter
import yaml
import cv2 as cv
import numpy as np
import threading
import serailport

RED=3
GREEN=4
BLUE=5

with open("config.yaml", 'r') as file:
    config = yaml.load(file, Loader=yaml.FullLoader)

Vision_Mode = config["Vision_Mode"]

def open_camera(cam_id):
    cap = cv.VideoCapture(cam_id)
    cap.set(cv.CAP_PROP_FPS, 30)
    return cap

def main(cam_id):
    cap = open_camera(cam_id)

    while True:
        _, img = cap.read()
        img = cv.flip(img, -1)
        #模式切换1，2分别是识别物料和地标的模式位，3，4，5是不同的颜色
        if parameter.Mode.task_detect == 1:
          if parameter.Mode.color_detect == 3:
              Materail_detect(img,3)
          if parameter.Mode.color_detect == 4:
              Materail_detect(img,4)
          if parameter.Mode.color_detect == 5:
              Materail_detect(img,5)
        if parameter.Mode.task_detect == 2:
            Land_mark_Detect(img,GREEN)

        if parameter.Mode.task_detect == 6:
            Edge_Detect(img)
            
        if cv.waitKey(1) & 0xFF == ord('q'):
            break
    cap.release()
    if Vision_Mode:
        cv.destroyAllWindows()
    

def Materail_detect(img,color):

    Materail_Thresholds = config.get('Materail_Thresholds', {})

    lbc = Materail_Thresholds.get('lower_blue_contour', [])
    ubc = Materail_Thresholds.get('upper_blue_contour', [])
    lgc = Materail_Thresholds.get('lower_green_contour', [])
    ugc = Materail_Thresholds.get('upper_green_contour', [])
    lrc = Materail_Thresholds.get('lower_red_contour', [])
    urc = Materail_Thresholds.get('upper_red_contour', [])
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    if color is BLUE:
        mask = cv.inRange(hsv, tuple(lbc), tuple(ubc))
    elif color is GREEN:  
        mask = cv.inRange(hsv, tuple(lgc), tuple(ugc))
    elif color is RED:
        mask = cv.inRange(hsv, tuple(lrc), tuple(urc))
    if Vision_Mode:
        cv.imshow("mask",mask)
    contours, _ = cv.findContours(mask, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_perimeter = 0
    largest_contour = None
    
    # 遍历每个轮廓
    for cnt in contours:
        perimeter = cv.arcLength(cnt, True)
        if perimeter > max_perimeter:
            max_perimeter = perimeter
            largest_contour = cnt
    
    x, y, w, h = 0,0,0,0
        
    if largest_contour is not None:
        x, y, w, h = cv.boundingRect(largest_contour)

        if max_perimeter>config["min_contour"] and (x + w/2)>310:

            parameter.Object_Data.position_matrix[0] = [x, y]
            parameter.Object_Data.position_matrix[1] = [x, y + h]
            parameter.Object_Data.position_matrix[2] = [x + w, y + h]
            parameter.Object_Data.position_matrix[3] = [x + 2, y]

            center_x = int(x + w/2)
            center_y = int(y + h/2)
            #print(str((center_x,center_y))+"Catch")
            parameter.Object_Data.center = (center_x, center_y)
        else:
            x, y, w, h = 0,0,0,0
            parameter.Object_Data.position_matrix[0] = [x, y]
            parameter.Object_Data.position_matrix[1] = [x, y + h]
            parameter.Object_Data.position_matrix[2] = [x + w, y + h]
            parameter.Object_Data.position_matrix[3] = [x + 2, y]

            center_x = int(x + w/2)
            center_y = int(y + h/2)
            #print(center_x,center_y)
            parameter.Object_Data.center = (center_x, center_y)
            
    else:
        parameter.Object_Data.position_matrix[0] = [x, y]
        parameter.Object_Data.position_matrix[1] = [x, y + h]
        parameter.Object_Data.position_matrix[2] = [x + w, y + h]
        parameter.Object_Data.position_matrix[3] = [x + 2, y]

        center_x = int(x + w/2)
        center_y = int(y + h/2)
        parameter.Object_Data.center = (center_x, center_y)
    if Vision_Mode:
        cv.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
        cv.circle(img, parameter.Object_Data.center, 5, (0, 0, 0), -1)
        cv.imshow("materail_img",img)

def Land_mark_Detect(img, color):

    Landmark_Thresholds = config.get('Landmark_Thresholds', {})

    lbc_ = Landmark_Thresholds.get('lower_blue_circle', [])
    ubc_ = Landmark_Thresholds.get('upper_blue_circle', [])
    lgc_ = Landmark_Thresholds.get('lower_green_circle', [])
    ugc_ = Landmark_Thresholds.get('upper_green_circle', [])
    lr1c = Landmark_Thresholds.get('lower_red_1_circle', [])
    ur1c = Landmark_Thresholds.get('upper_red_1_circle', [])
    lr2c = Landmark_Thresholds.get('lower_red_2_circle', [])
    ur2c = Landmark_Thresholds.get('upper_red_2_circle', [])

    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)
    if color is BLUE:
        mask_blue = cv.inRange(hsv, tuple(lbc_), tuple(ubc_))
        res = cv.bitwise_and(img, img, mask=mask_blue)
    elif color is GREEN:
        mask_green = cv.inRange(hsv, tuple(lgc_), tuple(ugc_))
        res = cv.bitwise_and(img, img, mask=mask_green)
    elif color is RED:
        mask_red_1 = cv.inRange(hsv, tuple(lr1c), tuple(ur1c))
        mask_red_2 = cv.inRange(hsv, tuple(lr2c), tuple(ur2c))
        mask_red = cv.bitwise_or(mask_red_1,mask_red_2)
        res = cv.bitwise_and(img, img, mask=mask_red)

    # 将结果转换为灰度图像
    img_gray = cv.cvtColor(res, cv.COLOR_BGR2GRAY)
    img_gray = cv.medianBlur(img_gray, 5)
    # if Vision_Mode:
    #     cv.imshow("gray", img_gray)

    circles = cv.HoughCircles(img_gray, cv.HOUGH_GRADIENT_ALT, 1, 20,
                            param1=50, param2=0.8, minRadius=30, maxRadius=0)

    smallest_circle = None
    min_radius = config["min_radius"]

    if circles is not None:
        circles = np.uint16(np.around(circles))

        for cnt in circles[0, :]:
                radius = cnt[2]
                if radius < min_radius:
                    min_radius = radius
                    smallest_circle = cnt
        
        if Vision_Mode:
            cv.circle(img, (smallest_circle[0],smallest_circle[1]), smallest_circle[2], (0, 255, 0), 2)
        
        x, y, radius = smallest_circle[0], smallest_circle[1], smallest_circle[2]
        # 计算矩形的四个顶点坐标
        # 注意：以下left top可能会数据溢出，但是本项目数据溢出并不会造成严重后果
        
        left = x - radius
        right = x + radius
        top = y - radius
        bottom = y + radius
        parameter.Object_Data.position_matrix[0] = [left, top]
        parameter.Object_Data.position_matrix[3] = [right,top]
        parameter.Object_Data.position_matrix[2] = [right, bottom]
        parameter.Object_Data.position_matrix[1] = [left, bottom]
        parameter.Object_Data.center = (x, y)
        if Vision_Mode:
            cv.circle(img, parameter.Object_Data.center, 5, (0, 0, 0), -1)
            cv.imshow('Landmark_img', img)
    else:
        left = 0
        right = 0
        top = 0
        bottom = 0
        parameter.Object_Data.position_matrix[0] = [left, top]
        parameter.Object_Data.position_matrix[3] = [right,top]
        parameter.Object_Data.position_matrix[2] = [right, bottom]
        parameter.Object_Data.position_matrix[1] = [left, bottom]
        parameter.Object_Data.center = (0,0)
        if Vision_Mode:
            cv.imshow('Landmark_img', img)

def Edge_Detect(img):
    Edge_Thresholds = config.get('Edge_Thresholds', {})

    lower_contour_threshold = Edge_Thresholds.get('lower_contour', [])
    upper_contour_threshold = Edge_Thresholds.get('upper_contour', [])
    hsv = cv.cvtColor(img, cv.COLOR_BGR2HSV)

    mask_blue = cv.inRange(hsv, tuple(lower_contour_threshold), tuple(upper_contour_threshold))

    kernel = cv.getStructuringElement(cv.MORPH_RECT, (3, 3))  # 设置腐蚀和膨胀的核大小
    kernel2 = cv.getStructuringElement(cv.MORPH_RECT, (2, 2))  # 设置腐蚀和膨胀的核大小
    dilated = cv.dilate(mask_blue, kernel, iterations=2)  # 膨胀操作

    edges = cv.Canny(dilated,100,200)
    dilated_edges = cv.dilate(edges, kernel2, iterations=5)
 
    # 查找二进制图像中的轮廓
    contours, _ = cv.findContours(dilated_edges, cv.RETR_EXTERNAL, cv.CHAIN_APPROX_SIMPLE)
    max_perimeter = 0
    largest_contour = None
    # 遍历每个轮廓
    for cnt in contours:
        perimeter = cv.arcLength(cnt, True)
        if perimeter > max_perimeter:
            max_perimeter = perimeter
            largest_contour = cnt
    # 进行轮廓直线拟合

    if largest_contour is not None:
        
        [vx, vy, x, y] = cv.fitLine(largest_contour, cv.DIST_L2, 0, 0.01, 0.01)

        # 计算直线的起点和终点
        lefty = int((-x * vy / vx) + y)
        righty = int(((img.shape[1] - x) * vy / vx) + y)
        k = int(vy / vx *100)
        binary_complement = int_to_binary_complement(k)
        # 计算直线中点的坐标
        mid_x = int(x)
        mid_y = int(y)

        parameter.Object_Data.center = (mid_x, mid_y)
        parameter.Mode.color_detect = binary_complement
        print((mid_x,mid_y,k))
        if Vision_Mode:    
            cv.line(img, (0, lefty), (img.shape[1] - 1, righty), (0, 255, 0), 2)
            cv.circle(img, parameter.Object_Data.center, 5, (0, 0, 0), -1)   
    if Vision_Mode:    
        cv.imshow('Fitted Line', img)

def int_to_binary_complement(number):
    if number < -128 or number > 127:
        print("Invalid value")
        return 0
    # 将负数转换为其补码表示
    if number < 0:
        # 计算补码的绝对值
        complement_value = 256 + number  # 256是2^8
    else:
        complement_value = number
        
    return complement_value

if __name__ == "__main__":
    cam_id = config["cam_id"]
    serialport_mode = config["serialport_mode"]
    
    if serialport_mode:
        ser = serailport.serial_init()
        receive_thread = threading.Thread(target=serailport.receive_thread, args=(ser,))
        receive_thread.daemon = True  # 设置线程为守护线程，这样主程序退出时会自动结束线程
        receive_thread.start()

        if parameter.Mode.task_detect != 0:
            send_thread = threading.Thread(target=serailport.send_thread, args=(ser,))
            send_thread.daemon = True  # 设置线程为守护线程，这样主程序退出时会自动结束线程
            send_thread.start()
    
    main(cam_id)
