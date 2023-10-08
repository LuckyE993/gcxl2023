import cv2
from pyzbar.pyzbar import decode
import numpy as np

# 打开摄像头
cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FPS, 30)
while True:
    # 读取视频帧
    ret, frame = cap.read()


    decoded_objects = decode(frame)


    for obj in decoded_objects:
        points = obj.polygon
        if len(points) > 4:
            hull = cv2.convexHull(np.array([point for point in points], dtype=np.float32))
            cv2.polylines(frame, [hull], True, (0, 255, 0), 2)
        else:
            cv2.polylines(frame, [np.array(points, dtype=np.int32)], True, (0, 255, 0), 2)


        qr_code_data = obj.data.decode('utf-8')
        cv2.putText(frame, qr_code_data, (obj.rect.left, obj.rect.top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)


    cv2.imshow('QR Code ', frame)

    # 检查是否按下 'q' 键来退出循环
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 释放摄像头资源和关闭窗口
cap.release()
cv2.destroyAllWindows()
