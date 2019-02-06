# USAGE
# python detect_color.py --image pokemon_games.png

# import the necessary packages
import numpy as np
import cv2

image_dest = "/home/pi/color.png"

##This is HSV .. we need two blue filters
lower_blue_hsv = [95, 10, 10]
upper_blue_hsv = [135, 255, 255]

## convert into numpy array
lower_blue_hsv = np.array(lower_blue_hsv, dtype = "uint8")
upper_blue_hsv = np.array(upper_blue_hsv, dtype = "uint8")

## Take the image
image = cv2.imread(image_dest)
## Convert into HSV
image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

## Apply the two blue filters
mask_blue_hsv = cv2.inRange(image_hsv, lower_blue_hsv, upper_blue_hsv)
mask_blue_hsv = np.array(mask_blue_hsv)


## Total blue pixels detected
blue_pixel_hsv = (mask_blue_hsv==255).sum()
print ("Number of blue pixels using HSV = ", blue_pixel_hsv)

##row,col,channel= image_hsv.shape
##print (" row  = ",row)
##print (" col  = ",col)
##for i in range(row):
   ##for j in range(col):
        ##print("PIXEL = ",image_hsv[i,j])
##
cv2.imshow("images", np.hstack([image_hsv, image_hsv]))
cv2.waitKey(0)
