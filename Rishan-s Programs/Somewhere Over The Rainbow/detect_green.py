# USAGE
# python detect_color.py --image pokemon_games.png

# import the necessary packages
import numpy as np
import cv2

image_dest = "/home/pi/color.png"

##This is HSV .. we need two green filters
lower_green_hsv = [40, 10, 10]
upper_green_hsv = [80, 255, 255]

## convert into numpy array
lower_green_hsv = np.array(lower_green_hsv, dtype = "uint8")
upper_green_hsv = np.array(upper_green_hsv, dtype = "uint8")

## Take the image
image = cv2.imread(image_dest)
## Convert into HSV
image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

## Apply the two green filters
mask_green_hsv = cv2.inRange(image_hsv, lower_green_hsv, upper_green_hsv)
mask_green_hsv = np.array(mask_green_hsv)

## Total green pixels detected
green_pixel_hsv = (mask_green_hsv==255).sum()

print ("Number of green pixels using HSV = ", green_pixel_hsv)

##row,col,channel= image_hsv.shape
##print (" row  = ",row)
##print (" col  = ",col)
##for i in range(row):
   ##for j in range(col):
        ##print("PIXEL = ",image_hsv[i,j])
##
cv2.imshow("images", np.hstack([image_hsv, image_hsv]))
cv2.waitKey(0)
