import cv2
import numpy as np

# 创建回调函数，用于Trackbar的调整
def update_dp(x):
    pass

def update_minDist(x):
    pass

def update_param1(x):
    pass

def update_param2(x):
    pass

def update_minRadius(x):
    pass

def update_maxRadius(x):
    pass

# 打开摄像头
cap = cv2.VideoCapture(2)
cap.set(cv2.CAP_PROP_FPS, 30)

# 创建窗口
cv2.namedWindow('Target Detection')

# 创建Trackbar，用于调整靶心检测的参数
cv2.createTrackbar('dp', 'Target Detection', 1, 10, update_dp)
cv2.createTrackbar('minDist', 'Target Detection', 10, 200, update_minDist)
cv2.createTrackbar('param1', 'Target Detection', 10, 200, update_param1)
cv2.createTrackbar('param2', 'Target Detection', 10, 200, update_param2)
cv2.createTrackbar('minRadius', 'Target Detection', 1, 100, update_minRadius)
cv2.createTrackbar('maxRadius', 'Target Detection', 100, 300, update_maxRadius)

while True:
    # 读取视频帧
    ret, frame = cap.read()

    # 将图像转换为灰度
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # 显示灰度图像以进行调试
    cv2.imshow('Gray Image', gray)

    # 使用Canny边缘检测进行预处理
    edges = cv2.Canny(gray, 50, 150, apertureSize=3)

    # 获取Trackbar的当前值
    dp = cv2.getTrackbarPos('dp', 'Target Detection')
    minDist = cv2.getTrackbarPos('minDist', 'Target Detection')
    param1 = cv2.getTrackbarPos('param1', 'Target Detection')
    param2 = cv2.getTrackbarPos('param2', 'Target Detection')
    minRadius = cv2.getTrackbarPos('minRadius', 'Target Detection')
    maxRadius = cv2.getTrackbarPos('maxRadius', 'Target Detection')

    # 执行霍夫圆检测
    circles = cv2.HoughCircles(edges, cv2.HOUGH_GRADIENT, dp=dp, minDist=minDist, param1=param1, param2=param2, minRadius=minRadius, maxRadius=maxRadius)

    if circles is not None:
        circles = np.uint16(np.around(circles))
        for circle in circles[0, :]:
            # 提取圆的中心坐标和半径
            center = (circle[0], circle[1])
            radius = circle[2]
            # 绘制圆
            cv2.circle(frame, center, radius, (0, 255, 0), 2)

    # 显示结果
    cv2.imshow('Target Detection', frame)

    # 检查是否按下 'q' 键来退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源和关闭窗口
cap.release()
cv2.destroyAllWindows()
