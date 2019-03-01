# The robot must go in the following order: Red, Blue, Yellow and Green
# import the necessary packages
import numpy as np
import cv2
from picamera import PiCamera
from time import sleep
from subprocess import call
from gpiozero import Robot, LED
import time
# We'll use the distance sensor module in our CERCBot library (CERCBot.py)
import CERCBot

threshhold = 50 #pixels
burt_the_robot = Robot(left=(20, 21), right=(7, 8))
left_echo_pin = 14
left_trigger_pin = 15
centre_echo_pin = 17
centre_trigger_pin = 4
right_echo_pin = 23
right_trigger_pin = 18
led = LED(2)
filecnt = 1
speed = 0.4
dis = 12
sl = 0.4

colours = ['red']
img_dest = "/home/pi/color.png"
#Red:
lower_red1 = [320/2, (60/100)*255, (70/100)*255]
upper_red1 = [360/2, (75/100)*255, (100/100)*255]
lower_red2 = [320/2, (60/100)*255, (70/100)*255]
upper_red2 = [360/2, (75/100)*255, (100/100)*255]
#Blue:
lower_blue = [160/2, (10/100)*255, (30/100)*255]
upper_blue = [190/2, (20/100)*255, (50/100)*255]
#Green:
lower_green = [60/2, (70/100)*255, (40/100)*255]
upper_green = [90/2, (90/100)*255, (60/100)*255]
#Yellow:
lower_yellow = [27/2, (10/100)*255, (10/100)*255]
upper_yellow = [32/2, (255/100)*255, (255/100)*255]
# create NumPy arrays from the boundaries
lower_red1 = np.array(lower_red1, dtype = "uint8")
upper_red1 = np.array(upper_red1, dtype = "uint8")
lower_red2 = np.array(lower_red2, dtype = "uint8")
upper_red2 = np.array(upper_red2, dtype = "uint8")
lower_green = np.array(lower_green, dtype = "uint8")
upper_green = np.array(upper_green, dtype = "uint8")
lower_blue = np.array(lower_blue, dtype = "uint8")
upper_blue = np.array(upper_blue, dtype = "uint8")
lower_yellow = np.array(lower_yellow, dtype = "uint8")
upper_yellow = np.array(upper_yellow, dtype = "uint8")
# In the specific order ('red','blue','yellow','green'), go to each zone
#and stop when it is less than 15cm away.
led.off()
direction = "left"
print("starting")
for k in range(len(colours)):
    myColour = colours[k]
    print('Finding colour',myColour)
    filecnt = 1
    img = cv2.imread(img_dest)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    img = cv2.GaussianBlur(img,(11,11),100) # The last value changes the amount of blur, in our case the highest

    #row,col,channel= img.shape
    #for i in range(row):
    #    for j in range(col):
    #        print("PIX = ", img[i,j])
            
        
    #if myColour == 'red':
    maskr1 = cv2.inRange(img, lower_red1, upper_red1)
    maskr2 = cv2.inRange(img, lower_red2, upper_red2)
    pixr_cnt = (maskr1==255).sum() + (maskr2==255).sum()
    #elif myColour == 'blue':
    maskb = cv2.inRange(img, lower_blue, upper_blue)
    pixb_cnt = (maskb==255).sum()
    #elif myColour == 'green':
    maskg = cv2.inRange(img, lower_green, upper_green)
    pixg_cnt = (maskg==255).sum()
    #else:
    masky = cv2.inRange(img, lower_yellow, upper_yellow)
    pixy_cnt = (masky==255).sum()

    print ("pixr_cnt = ",pixr_cnt)
    print ("pixg_cnt = ",pixg_cnt)
    print ("pixb_cnt = ",pixb_cnt)
        
        ## If colour is greater than threshold (i.e. it is looking at it clearly
        ## and any of the distabnce is too less, i.e. it is either in the corner
        ## or head on to the colour that means it is done for that colour
            # Remove pictures afterwards.
        # show the imgs
        #cv2.imshow("img", np.hstack([img, output]))
        #cv2.waitKey(0)

            ##
