import cv2 as cv
cap = cv.VideoCapture(0)

cap.set(cv.CAP_PROP_FPS, 30)


while True:

    ret, frame = cap.read()
        # 显示结果
    cv.imshow('Elliptical Fit', frame)

    # 检查是否按下 'q' 键来退出循环
    if cv.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源和关闭窗口
cap.release()
cv.destroyAllWindows()