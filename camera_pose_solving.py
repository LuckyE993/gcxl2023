import cv2
import yaml
import parameter as param
import numpy as np

# 从YAML文件中读取数据
with open("pnp_params.yaml", 'r') as file:
    params = yaml.load(file, Loader=yaml.FullLoader)

camera_matrix = np.array(params["camera_matrix"], dtype=np.float32)
dist_coeffs = np.array(params["dist_coeffs"], dtype=np.float32)
# image_points = np.array(params["image_points"], dtype=np.float32)
image_points = param.Object_Data.position_matrix

if param.Mode.axis_detect == 1:
    object_points = np.array(params["material_points"], dtype=np.float32)
if param.Mode.axis_detect == 2:
    object_points = np.array(params["landmark_points"], dtype=np.float32)

print(object_points)

# 进行PnP解算
retval, rvec, tvec = cv2.solvePnP(object_points, image_points, camera_matrix, dist_coeffs)

tx, ty, tz = tvec

# # # 输出结果
# print("Rotation Vector (rvec):")
# print(rvec)
# print("\nTranslation Vector (tvec):")
# print(tvec)
