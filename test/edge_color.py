import cv2
import numpy as np

# 读取图像
image = cv2.imread('dataset/Screenshot from 2023-10-03 15-35-29.png')

cv2.imshow("img",image)
# 将图像转换为灰度图
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

# 进行边缘检测，例如Canny边缘检测
edges = cv2.Canny(gray, threshold1=50, threshold2=150, apertureSize=3)

# 进行霍夫直线变换
lines = cv2.HoughLinesP(edges, 1, np.pi / 180, threshold=100, minLineLength=50, maxLineGap=5)

# 绘制检测到的直线
for line in lines:
    x1, y1, x2, y2 = line[0]
    cv2.line(image, (x1, y1), (x2, y2), (0, 0, 0), 2)
    # 计算直线的斜率
    if x2 - x1 != 0:  # 避免除以零的情况
        slope = (y2 - y1) / (x2 - x1)
    else:
        slope = float('inf')  # 处理斜率为无穷大的情况

    # 假设水平线的方程为 y = constant，这里使用图像的中心线作为水平线示例
    constant = image.shape[0] // 2  # 图像高度的一半，也可以根据实际情况替换为水平线的位置

    # 计算直线与水平线的交点横坐标
    if slope != 0:  # 避免斜率为零的情况
        x_intersection = (constant - y1) / slope
    else:
        x_intersection = x1  # 处理斜率为零的情况

    # 直线的偏差即为交点横坐标
    offset = x_intersection

    # 打印斜率和偏差
    print("直线斜率：", slope)
    print("直线偏差：", offset)
# 显示图像
cv2.imshow('Detected Lines', image)
cv2.waitKey(0)
cv2.destroyAllWindows()
