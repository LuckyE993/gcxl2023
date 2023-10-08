import numpy as np
import cv2 as cv
img = cv.imread('/home/luckye/Downloads/dataset/dataset_2.jpeg', cv.IMREAD_GRAYSCALE)
#img = cv.resize(img,(640,640))
img = cv.resize(img,None,fx=0.5, fy=0.5, interpolation = cv.INTER_CUBIC)
img = cv.medianBlur(img,5)
cimg = cv.cvtColor(img,cv.COLOR_GRAY2BGR)
circles = cv.HoughCircles(img,cv. HOUGH_GRADIENT_ALT,1,20,
                            param1=50,param2=0.9,minRadius=0,maxRadius=0)
circles = np.uint16(np.around(circles))
for i in circles[0,:]:
    # draw the outer circle
    cv.circle(cimg,(i[0],i[1]),i[2],(0,255,0),2)
    # draw the center of the circle
    cv.circle(cimg,(i[0],i[1]),2,(0,0,255),3)
cv.imshow('detected circles',cimg)
height, width = img.shape[:2]
print(height,width)

cv.waitKey(0)
cv.destroyAllWindows()