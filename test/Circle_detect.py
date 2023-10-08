import numpy as np
import cv2 as cv
img = cv.imread('BGR_COLOR.jpg',cv.IMREAD_UNCHANGED)
gray = 	cv.cvtColor(img,cv.COLOR_BGR2GRAY)
cv.imshow('IMG',img)
cv.imshow('GRAY',gray)
cv.waitKey(0)
cv.destroyAllWindows()