# USAGE
# python detect_color.py --image pokemon_games.png
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
threshhold = 300 #pixels
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
sl = 0.3
sl2 = 0.2

colours = ['red','green']
image_dest = "/home/pi/Pictures/colour.png"
camera.resolution = (200, 200)
print("centre")
centre_distance = CERCBot.calc_dist_cm(centre_trigger_pin, centre_echo_pin)
print("right")
right_distance = CERCBot.calc_dist_cm(right_trigger_pin, right_echo_pin)
#print("left")
#left_distance = CERCBot.calc_dist_cm(left_trigger_pin, left_echo_pin)

#Red:
lowerr = [10, 10, 40]
upperr = [50, 25, 200]
#Blue:
lowerb = [40, 10, 10]
upperb = [200, 56, 50]
#Green:
lowerg = [60, 127, 97]
upperg = [90, 160, 120]
#Yellow:
lowery = [65, 140, 190]
uppery = [90, 175, 220]

# create NumPy arrays from the boundaries
lowerr = np.array(lowerr, dtype = "uint8")
upperr = np.array(upperr, dtype = "uint8")
lowerg = np.array(lowerg, dtype = "uint8")
upperg = np.array(upperg, dtype = "uint8")
lowerb = np.array(lowerb, dtype = "uint8")
upperb = np.array(upperb, dtype = "uint8")
lowery = np.array(lowery, dtype = "uint8")
uppery = np.array(uppery, dtype = "uint8")
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
    
        camera.capture(image_dest,format='png')
    # Depending on colour, we need different masks
    # load the image
        image = cv2.imread(image_dest)
        
        if myColour == 'red':
            mask = cv2.inRange(image, lowerr, upperr)
        elif myColour == 'blue':
            mask = cv2.inRange(image, lowerb, upperb)
        elif myColour == 'green':
            mask = cv2.inRange(image, lowerg, upperg)
        else:
            mask = cv2.inRange(image, lowery, uppery)
        output = cv2.bitwise_and(image, image, mask = mask)
        
        row,col= mask.shape
        pix_cnt=0
        #millis = int(round(time.time() * 1000))
        #print ("millis ",millis)
        print("row = ",row," col = ",col)
        
        #for i in range(row):
        #    for j in range(col):
        #        if (mask[i,j]) == 255:
        #            pix_cnt += 1
        pix_cnt = (mask==255).sum()
        pix0_cnt = (mask==0).sum()
        print ("pix_cnt ",pix_cnt)
        print ("pix_cnt 0 ",pix0_cnt)
        print ("sum ",pix0_cnt+pix_cnt)
        
        #print ("pix_cnt = ",pix_cnt, " red = ",red, "green = ",green,"blue = ",blue)
        r = CERCBot.calc_dist_cm(right_trigger_pin, right_echo_pin)
        #l = CERCBot.calc_dist_cm(left_trigger_pin,left_echo_pin)
        l=20
        m = CERCBot.calc_dist_cm(centre_trigger_pin, centre_echo_pin)
        print(' l= ',l," m = ",m," r = ",r)
        if m < dis and r < dis and (pix_cnt <= threshhold):
            print('Turning back 1')
            burt_the_robot.backward(speed)
            print('Wait 1')
            sleep(sl2)
            print('Turning left 1')
            burt_the_robot.left(speed)
        if m < dis and l < dis  and (pix_cnt <= threshhold):
            
            print('Turning back 2')
            burt_the_robot.backward(speed)
            print('Wait 3')
            sleep(sl2)
            print('Turning right 1')
            burt_the_robot.right(speed)
        if  m < dis :
            if (pix_cnt > threshhold):
                colourDone = True
                led.on()
            print('Going back 3')
            burt_the_robot.backward(speed)
        elif r < dis:
            ## try adding curve here
            print('Turning back 4')
            burt_the_robot.backward(speed)
            sleep (sl2)
            print('Turning left 2')
            burt_the_robot.left(speed)
        elif l < dis:
            ## try adding curve here
            print('Turning back 5')
            burt_the_robot.backward(speed)
            sleep (sl2)
            print('Turning right 3')
            burt_the_robot.right(speed)
        else: 
            if  pix_cnt < threshhold:
                print('Turning left 3')
                burt_the_robot.left(speed) 
            else:
                print('Forward')
                burt_the_robot.forward(speed)
                #sleep(sl2)
        #print('Wait 8')
        sleep(sl)
        # Remove pictures afterwards.
        # show the images
        cv2.imshow("images", np.hstack([image, output]))
        cv2.waitKey(0)

            ##
burt_the_robot.stop()

