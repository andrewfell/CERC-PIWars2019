# USAGE
# python detect_color.py --image pokemon_games.png
# The robot must go in the following order: Red, Blue, Yellow and Green
# import the necessary packages
import numpy as np
import argparse
import cv2
from picamera import PiCamera
from time import sleep
from subprocess import call
from gpiozero import Robot
import time
# We'll use the distance sensor module in our CERCBot library (CERCBot.py)
import CERCBot

camera = PiCamera()
camera.rotation = 180
threshhold = 500
burt_the_robot = Robot(left=(20, 21), right=(7, 8))
left_echo_pin = 14
left_trigger_pin = 15
centre_echo_pin = 17
centre_trigger_pin = 4
right_echo_pin = 23
right_trigger_pin = 18
filecnt = 1
speed = 0.4
dis = 8
sl = 0.3
sl2 = 0.2

colours = ['red']
image_dest = "/home/pi/Pictures/colour.png"
camera.resolution = (200, 200)
print("centre")
centre_distance = CERCBot.calc_dist_cm(centre_trigger_pin, centre_echo_pin)
print("right")
right_distance = CERCBot.calc_dist_cm(right_trigger_pin, right_echo_pin)
#print("left")
#left_distance = CERCBot.calc_dist_cm(left_trigger_pin, left_echo_pin)

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
# In the specific order ('red','blue','yellow','green'), go to each zone
#and stop when it is less than 15cm away.
call(["rm", "/home/pi/Pictures.png"])
print("starting")
for k in range(len(colours)):
    colourDone = False
    myColour = colours[k]
    print('Finding colour',myColour)
    while colourDone == False:
        burt_the_robot.stop()
    # find the colors within the specified boundaries and apply
    # the mask
    
        camera.capture(image_dest,format='png')
    # load the image
        image = cv2.imread(image_dest)
        mask = cv2.inRange(image, lower, upper)
        output = cv2.bitwise_and(image, image, mask = mask)
        row,col,channel= output.shape
        red=0
        green=0
        blue=0
        #millis = int(round(time.time() * 1000))
        #print ("millis ",millis)
        for i in range(row):
            for j in range(col):
                red = red + output[i,j,2]
                green = green + output[i,j,1]
                blue = blue + output[i,j,0]
                
        #print ("millis ",millis)
        
        if myColour == 'red':
            myVal = red
        if myColour == 'blue':
            myVal = blue
        if myColour == 'green':
            myVal = green
        if myColour == 'yellow':
            myVal = yellow
            
        print ("myVal = ",myVal, " red = ",red, "green = ",green,"blue = ",blue)
        r = CERCBot.calc_dist_cm(right_trigger_pin, right_echo_pin)
        #l = CERCBot.calc_dist_cm(left_trigger_pin,left_echo_pin)
        l = 20
        m = CERCBot.calc_dist_cm(centre_trigger_pin, centre_echo_pin)
        print(' l= ',l," m = ",m," r = ",r)
        if m < dis and r < dis and (myVal <= threshhold):
            print('Turning back 1')
            backward(speed)
            print('Wait 1')
            sleep(sl2)
            print('Turning left 1')
            burt_the_robot.left(speed)
        if m < dis and l < dis  and (myVal <= threshhold):
            print('Turning back 2')
            burt_the_robot.backward(speed)
            print('Wait 3')
            sleep(sl2)
            print('Turning right 1')
            burt_the_robot.right(speed)
        if  m < dis :
            if (myVal > threshhold):
                colourDone = True
                ## Glow an LED
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
            ## When I write burt_the_robot.forward(speed), it actually does burt_the_robot.backward(speed)
            print('Turning back 5')
            burt_the_robot.backward(speed)
            sleep (sl2)
            print('Turning right 3')
            burt_the_robot.right(speed)
        else: 
            if  myVal < threshhold:
                print('Turning left 3')
                burt_the_robot.left(speed) 
            else:
                print('Forward')
                burt_the_robot.forward(speed)
                #sleep(sl2)

        #print('Wait 8')
        sleep(sl)
        print('Wait 9')
        #image_tg= "/home/pi/Pictures/" + str(filecnt) + "-" + str(red) + "-"+ str(green) + "-" + str(blue)  + "-" + str(l) + "-"  + str(m) + "-" + str(r) + "-" + ".png"
        #filecnt = filecnt + 1 
        #call(["mv", image_dest, image_tg])
        # Remove pictures afterwards.
        # show the images
        #cv2.imshow("images", np.hstack([image, output]))
        #cv2.waitKey(0)

            ##
burt_the_robot.stop()

