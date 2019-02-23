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

camera = PiCamera()
camera.rotation = 180
threshhold = 1000 #pixels
burt_the_robot = Robot(left=(20, 21), right=(7, 8))
left_echo_pin = 14
left_trigger_pin = 15
centre_echo_pin = 17
centre_trigger_pin = 4
right_echo_pin = 23
right_trigger_pin = 18
led = LED(2)
speed = 0.4
dis = 8
sl = 0.3

colours = ['red','green']
img_dest = "/home/pi/colour.png"
camera.resolution = (200, 200)
print("centre")
centre_distance = CERCBot.calc_dist_cm(centre_trigger_pin, centre_echo_pin)
print("right")
right_distance = CERCBot.calc_dist_cm(right_trigger_pin, right_echo_pin)
print("left")
left_distance = CERCBot.calc_dist_cm(left_trigger_pin, left_echo_pin)
#Red:
lower_red1 = [0, 10, 10]
upper_red1 = [40, 255, 255]
lower_red2 = [160, 10, 10]
upper_red2 = [180, 255, 255]
#Blue:
lower_blue = [95, 10, 10]
upper_blue = [135, 255, 255]
#Green:
lower_green = [40, 10, 10]
upper_green = [80, 255, 255]
#Yellow:
lower_yellow = [27, 10, 10]
upper_yellow = [32, 255, 255]
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
print("starting")
for k in range(len(colours)):
    colourDone = False
    myColour = colours[k]
    led.off()
    print('Finding colour',myColour)
    while colourDone == False:
        burt_the_robot.stop()
    # find the colors within the specified boundaries and apply
    # the mask
    
        camera.capture(img_dest,format='png')
    # Depending on colour, we need different masks
    # load the img
        img = cv2.imread(img_dest)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        img = cv2.GaussianBlur(img,(11,11),100) # The last value changes the amount of blur, in our case the highest
        
        if myColour == 'red':
            mask = cv2.inRange(img, lower_red1, upper_red1)
            mask2 = cv2.inRange(img, lower_red2, upper_red2)
            pix_cnt = (mask==255).sum() + (mask2==255).sum()
        elif myColour == 'blue':
             mask = cv2.inRange(img, lower_blue, upper_blue)
             pix_cnt = (mask==255).sum()
        elif myColour == 'green':
            mask = cv2.inRange(img, lower_green, upper_green)
            pix_cnt = (mask==255).sum()
        else:
            mask = cv2.inRange(img, lower_yellow, upper_yellow)
            pix_cnt = (mask==255).sum()

        output = cv2.bitwise_and(img, img, mask = mask)
        row,col= mask.shape
        print("row = ",row," col = ",col)
        print ("pix_cnt ",pix_cnt)

        r = CERCBot.calc_dist_cm(right_trigger_pin, right_echo_pin)
        l = CERCBot.calc_dist_cm(left_trigger_pin,left_echo_pin)
        #l=20
        m = CERCBot.calc_dist_cm(centre_trigger_pin, centre_echo_pin)
        print(' l= ',l," m = ",m," r = ",r)

        ## If colour is greater than threshold (i.e. it is looking at it clearly
        ## and any of the distabnce is too less, i.e. it is either in the corner
        ## or head on to the colour that means it is done for that colour
        if (pix_cnt > threshhold):
          if (m < dis or l < dis or r < dis):
              colourDone = True
              led.on()
              burt_the_robot.backward(speed)
          else:
              
            burt_the_robot.forward(speed)
        else:
        ## Turn left
          burt_the_robot.left(speed)

        sleep(sl)
        # Remove pictures afterwards.
        # show the imgs
        #cv2.imshow("img", np.hstack([img, output]))
        #cv2.waitKey(0)

            ##
burt_the_robot.stop()

