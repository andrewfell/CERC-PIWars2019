# USAGE
# python detect_color.py --image pokemon_games.png

# import the necessary packages
import numpy as np
import cv2

image_dest = "/home/pi/color.png"
 
##This is HSV .. we need two yellow filters
lower_yellow_hsv = [27, 10, 10]
upper_yellow_hsv = [32, 255, 255]

## convert into numpy array
lower_yellow_hsv = np.array(lower_yellow_hsv, dtype = "uint8")
upper_yellow_hsv = np.array(upper_yellow_hsv, dtype = "uint8")

## Take the image
image = cv2.imread(image_dest)
## Convert into HSV
image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

## Apply the two yellow filters
mask_yellow_hsv = cv2.inRange(image_hsv, lower_yellow_hsv, upper_yellow_hsv)
mask_yellow_hsv = np.array(mask_yellow_hsv)

## Total yellow pixels detected
yellow_pixel_hsv = (mask_yellow_hsv==255).sum()
print ("Number of yellow pixels using HSV = ", yellow_pixel_hsv)

##row,col,channel= image_hsv.shape
##print (" row  = ",row)
##print (" col  = ",col)
##for i in range(row):
   ##for j in range(col):
        ##print("PIXEL = ",image_hsv[i,j])
##
cv2.imshow("images", np.hstack([image_hsv, image_hsv]))
cv2.waitKey(0)
