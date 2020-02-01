from picamera import PiCamera
from time import sleep
import numpy as np
import cv2

camera = PiCamera()
img_dest = "/home/pi/colour.png"
x_max = 400
y_max = 400
x_mod = x_max-130
y_mod = y_max-1
camera.resolution = (x_max, y_max)

#camera.start_preview()
#sleep(5)

camera.capture(img_dest,format='png')
img = cv2.imread(img_dest)
cv2.imshow("img", img) #np.hstack([img, output]))
cv2.waitKey(0)
img = img[0:x_mod, 0:y_mod]
cv2.imshow("img", img) #np.hstack([img, output]))
cv2.waitKey(0)
#camera.stop_preview()
