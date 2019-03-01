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
dis = 8
dis_m = 15
sl = 0.3
#Red:
lower_red1 = [320/2, (60*255)/100, (50*255)/100]
upper_red1 = [370/2, (85*255)/100, (90*255)/100]
lower_red2 = [320/2, (60*255)/100, (50*255)/100]
upper_red2 = [370/2, (85*255)/100, (90*255)/100]
#Blue:
lower_blue = [180/2, (10*255)/100, (40*255)/100]
upper_blue = [250/2, (60*255)/100, (80*255)/100]
#Green:
lower_green = [70/2, (40*255)/100, (40*255)/100]
upper_green = [90/2, (70*255)/100, (70*255)/100]
#Yellow:
lower_yellow = [40/2, (40*255)/100, (70*255)/100]
upper_yellow = [60/2, (60*255)/100, (100*255)/100]
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
colours = ['blue']
img_dest = "/home/pi/colour.png"
camera.resolution = (400, 400)
print("centre")
centre_distance = CERCBot.calc_dist_cm_v2(centre_trigger_pin, centre_echo_pin)
print("right")
right_distance = CERCBot.calc_dist_cm_v2(right_trigger_pin, right_echo_pin)
print("left")
left_distance = CERCBot.calc_dist_cm_v2(left_trigger_pin, left_echo_pin)
# In the specific order ('red','blue','yellow','green'), go to each zone
#and stop when it is less than 15cm away.
led.off()
direction = "left"
print("starting")
for k in range(len(colours)):
    colourDone = False
    myColour = colours[k]
    led.off()
    print('Finding colour',myColour)
    filecnt = 1
    while colourDone == False:
        
        burt_the_robot.stop()
    # find the colors within the specified boundaries and apply
    # the mask
    
        camera.capture(img_dest,format='png')
    # Depending on colour, we need different masks
    # load the img
        img = cv2.imread(img_dest)
        #img = img[100:400, 0:400]
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

        #output = cv2.bitwise_and(img, img, mask = mask)
        #row,col= mask.shape
        #print("row = ",row," col = ",col)
        #print ("pix_cnt ",pix_cnt)
        
        #print ("pix_cnt = ",pix_cnt, " red = ",red, "green = ",green,"blue = ",blue)
        r = CERCBot.calc_dist_cm_v2(right_trigger_pin, right_echo_pin)
        l = CERCBot.calc_dist_cm_v2(left_trigger_pin,left_echo_pin)
        m = CERCBot.calc_dist_cm_v2(centre_trigger_pin, centre_echo_pin)
        print(' l= ',l," m = ",m," r = ",r," pix_cnt = ",pix_cnt," threshold = ",threshhold)

        ## If colour is greater than threshold (i.e. it is looking at it clearly
        ## and any of the distabnce is too less, i.e. it is either in the corner
        ## or head on to the colour that means it is done for that colour
        if (pix_cnt > threshhold):
          if (m <= dis_m):
              colourDone = True
              led.on()
              burt_the_robot.backward(speed)
          else:
            print("Going forward")
            burt_the_robot.forward(speed)
        else:
        ## Turn left
            if l < dis and direction == "left":
                direction = "right"    
            if r < dis and direction == "right":
                direction = "left"
            if m < dis and direction == "forward":
                direction = "backward"

            print("Changing direction to ",direction)
            if direction == "left":
                burt_the_robot.left(speed)
            elif direction == "right":
                burt_the_robot.right(speed)
            elif direction == "forward":
                burt_the_robot.forward(speed)
            else:
                burt_the_robot.backward(speed)

        sleep(sl)
        image_tg= "/home/pi/Pictures/" + str(filecnt) + "-" +  str(pix_cnt)  + "-" + str(l) + "-"  + str(m) + "-" + str(r) + "-" + ".png"
        filecnt = filecnt + 1 
        call(["cp", img_dest, image_tg])
          # Remove pictures afterwards.
        # show the imgs
        #cv2.imshow("img", np.hstack([img, output]))
        #cv2.waitKey(0)

            ##
burt_the_robot.stop()

