# USAGE
# python detect_color.py --image pokemon_games.png

# import the necessary packages
import numpy as np
import cv2

image_dest = "/home/pi/color.png"

## This is RGB filter
lower_rgb = [17, 15, 100]
upper_rgb = [50, 56, 200]

##This is HSV .. we need two Red filters
lower_red1_hsv = [0, 10, 10]
upper_red1_hsv = [40, 255, 255]
lower_red2_hsv = [160, 10, 10]
upper_red2_hsv = [180, 255, 255]

## convert into numpy array
lower_rgb = np.array(lower_rgb, dtype = "uint8")
upper_rgb = np.array(upper_rgb, dtype = "uint8")
lower_red1_hsv = np.array(lower_red1_hsv, dtype = "uint8")
upper_red1_hsv = np.array(upper_red1_hsv, dtype = "uint8")
lower_red2_hsv = np.array(lower_red2_hsv, dtype = "uint8")
upper_red2_hsv = np.array(upper_red2_hsv, dtype = "uint8")

## Take the image
image = cv2.imread(image_dest)
## Convert into HSV
image_hsv = cv2.cvtColor(image,cv2.COLOR_BGR2HSV)

## Apply the two red filters
mask_red1_hsv = cv2.inRange(image_hsv, lower_red1_hsv, upper_red1_hsv)
mask_red1_hsv = np.array(mask_red1_hsv)
mask_red2_hsv = cv2.inRange(image_hsv, lower_red2_hsv, upper_red2_hsv)
mask_red2_hsv = np.array(mask_red2_hsv)

## Also calculate in RGB
mask_rgb = cv2.inRange(image, lower_rgb, upper_rgb)
mask_rgb = np.array(mask_rgb)

## Total red pixels detected
red_pixel_hsv = (mask_red1_hsv==255).sum()+(mask_red2_hsv==255).sum()
print ("Number of red pixels using RGB = ", (mask_rgb==255).sum())
print ("Number of red pixels using HSV = ", red_pixel_hsv)

##row,col,channel= image_hsv.shape
##print (" row  = ",row)
##print (" col  = ",col)
##for i in range(row):
   ##for j in range(col):
        ##print("PIXEL = ",image_hsv[i,j])
##
cv2.imshow("images", np.hstack([image_hsv, image_hsv]))
cv2.waitKey(0)
