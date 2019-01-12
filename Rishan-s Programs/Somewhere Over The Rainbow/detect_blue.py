# USAGE
# python detect_color.py --image pokemon_games.png

# import the necessary packages
import numpy as np
import argparse
import cv2
from picamera import PiCamera
from time import sleep
from subprocess import call

camera = PiCamera()
camera.rotation = 180
image_dest = "/home/pi/colour.png"
camera.resolution = (200, 200)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

# define the list of boundaries
boundaries = [
	([17, 15, 100], [50, 56, 200])
]

# loop over the boundaries
lower = [17, 15, 100]
upper = [50, 56, 200]
# create NumPy arrays from the boundaries
lower = np.array(lower, dtype = "uint8")
upper = np.array(upper, dtype = "uint8")
while True:
# find the colors within the specified boundaries and apply
# the mask
    camera.capture(image_dest,format='png')


# load the image
#image = cv2.imread(args["image"])
#image = cv2.imread("/home/pi/My Projects/AI Python projects/opencv-python-color-detection/pokemon_games.png")
    image = cv2.imread(image_dest)


    mask = cv2.inRange(image, lower, upper)
    output = cv2.bitwise_and(image, image, mask = mask)

    row,col,channel= output.shape
    print (" row  = ",row)
    print (" col  = ",col)
    red=0
    green=0
    blue=0
    for i in range(row):
        for j in range(col):
            #print (output[i,j,2])
            red = red + output[i,j,2]
            green = green + output[i,j,1]
            blue = blue + output[i,j,0]
            
    print ("red = ",red)
    print ("green = ",green)
    print ("blue = ",blue)
    ru = red/(red + green + blue + 1)
    gu = green/(red + green + blue + 1)
    bu = blue/(red + green + blue + 1)

    print ("ru = ",ru)
    print ("gu = ",gu)
    print ("bu = ",bu)
    if blue < 5000:
        print('Turning left')
    else:
        print('Forward')
    call(["rm", image_dest])

    # show the images
    cv2.imshow("images", np.hstack([image, output]))
    cv2.waitKey(0)

	##
