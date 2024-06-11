import cv2
import numpy
img = cv2.imread("C:\\Users\\praky\\Pictures\\Nitro\\Nitro_Wallpaper_01_3840x2400.jpg",0)
eroded_img = cv2.erode(img, kernel=numpy.ones((5,5),numpy.uint8), iterations=1)
dilated_img = cv2.dilate(img, kernel=numpy.ones((5,5),numpy.uint8), iterations=2)
cv2.imshow()
