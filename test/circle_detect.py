import cv2
import numpy as np


def update_threshold(x):
    pass

#接近精度
def update_approximation(x):
    pass


cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FPS, 30)

# 创建窗口
cv2.namedWindow('Elliptical Fit')

# Canny边缘检测的阈值
cv2.createTrackbar('Canny Threshold', 'Elliptical Fit', 0, 255, update_threshold)
initial_threshold = 100  # 设置初始阈值
cv2.setTrackbarPos('Canny Threshold', 'Elliptical Fit', initial_threshold)

# 多边形逼近的精度
cv2.createTrackbar('Approximation', 'Elliptical Fit', 1, 10, update_approximation)
initial_approximation = 1  # 设置初始逼近精度

while True:

    ret, frame = cap.read()

    canny_threshold = cv2.getTrackbarPos('Canny Threshold', 'Elliptical Fit')
    approximation = cv2.getTrackbarPos('Approximation', 'Elliptical Fit')

    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    edges = cv2.Canny(gray, canny_threshold, canny_threshold * 2, apertureSize=3)

    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # 遍历每个轮廓并拟合椭圆
    for contour in contours:
        if len(contour) >= 5:
            # 多边形逼近
            epsilon = approximation * 0.001 * cv2.arcLength(contour, True)
            approx = cv2.approxPolyDP(contour, epsilon, True)
            
            if len(approx) >= 5:
                ellipse = cv2.fitEllipse(approx)
                # 检查椭圆的尺寸信息是否有效
                if ellipse[1][0] >= 0 and ellipse[1][1] >= 0:
                    cv2.ellipse(frame, ellipse, (0, 255, 0), 2)

    # 显示结果
    cv2.imshow('Elliptical Fit', frame)

    # 检查是否按下 'q' 键来退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源和关闭窗口
cap.release()
cv2.destroyAllWindows()
