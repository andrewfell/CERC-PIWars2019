# The robot must go in the following order: Red, Blue, Yellow and Green
# import the necessary packages
import numpy as np
import cv2
from picamera import PiCamera
from time import sleep
from subprocess import call
from gpiozero import Robot, LED
import time
from bluedot import BlueDot
from signal import pause
# We'll use the distance sensor module in our CERCBot library (CERCBot.py)
import CERCBot

camera = PiCamera()
x_max = 400
y_max = 400
x_mod = x_max-130
y_mod = y_max-1
camera.resolution = (x_max, y_max)
threshhold = 50 #pixels
max_val = 40000
burt_the_robot = Robot(left=(8, 7), right=(21, 20))
left_echo_pin = 14
left_trigger_pin = 15
centre_echo_pin = 17
centre_trigger_pin = 4
right_echo_pin = 23
right_trigger_pin = 18
def my_endfunc(sig, frame):
        print('You pressed Ctrl+C!')
#        log.close()
        burt_the_robot.stop()
        sys.exit(0)

led = LED(2)
bd = BlueDot()
filecnt = 1
fwd_speed = 0.5
turn_speed_default = 0.5
turn_speed_fast = 0.6
dis = 8
dis_m = 11
sl = 0.3
counter = 0
colourDone = False

#Red:
lower_black = [330/2, (50*2.55), (50*2.55)]
upper_black = [360/2, (100*2.55), (100*2.55)]
lower_black2 = [0/2, (10*2.55), (10*2.55)]
upper_black2 = [20/2, (30*2.55), (70*2.55)]

#Red:
lower_red1 = [325/2, (55*2.55), (50*2.55)]
upper_red1 = [365/2, (100*2.55), (100*2.55)]

lower_red2 = [0/2, (55*2.55), (50*2.55)]
upper_red2 = [10/2, (80*2.55), (80*2.55)]
#Blue:
lower_blue = [61/2, (0*2.55), (60*2.55)]
upper_blue = [190/2, (50*2.55), (100*2.55)]
#Green:
lower_green = [55/2, (30*2.55), (30*2.55)]
upper_green = [60/2, (100*2.55), (100*2.55)]
#Yellow:
lower_yellow = [40/2, (30*2.55), (30*2.55)]
upper_yellow = [55/2, (100*2.55), (100*2.55)]

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
colours = ['red','blue','yellow','green']
img_dest = "/home/pi/colour.png"

def set_colour():
    global colourDone
    colourDone = True
    led.on()

def main_loop():
    global colourDone 
    print("centre")
    centre_distance = CERCBot.calc_dist_cm_v2(centre_trigger_pin, centre_echo_pin)
    print("right")
    right_distance = CERCBot.calc_dist_cm_v2(right_trigger_pin, right_echo_pin)
    print("left")
    left_distance = CERCBot.calc_dist_cm_v2(left_trigger_pin, left_echo_pin)
    # In the specific order ('red','blue','yellow','green'), go to each zone
    #and stop when it is less than 15cm away.
    led.off()
    print("starting")
    for k in range(len(colours)):
        direction = "left"
        colourDone = False
        got_pixel = False
        pic_on_left = False
              
        myColour = colours[k]
        led.off()
        filecnt = 1
        done = False
        turn_speed = turn_speed_fast
        while done == False:
            if colourDone == True:
                done = True
                burt_the_robot.backward(fwd_speed)
                sleep(sl)
                sleep(sl)
                sleep(sl)
                sleep(sl)
                print('Finished looking for colour')

            print('Finding colour',myColour)
            sleep_val = sl
            burt_the_robot.stop()
        # find the colors within the specified boundaries and apply
        # the mask
            camera.capture(img_dest,format='png')
        # Depending on colour, we need different masks
        # load the img
            img = cv2.imread(img_dest)
            #img = img[200:400, 0:400]
            img = img[0:x_mod, 0:y_mod]
            img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
            img = cv2.GaussianBlur(img,(11,11),100) # The last value changes the amount of blur, in our case the highest
            img_right = img[0:x_mod,0:round(y_mod/2)-1]
            img_left = img[0:x_mod,round(y_mod/2):y_mod]
            
            # Get how many red pixels in the image
            maskr_left = cv2.inRange(img_left, lower_red1, upper_red1) +  cv2.inRange(img_left, lower_red2, upper_red2)
            pixr_left_cnt = (maskr_left==255).sum()
            maskr_right = cv2.inRange(img_right, lower_red1, upper_red1) + cv2.inRange(img_right, lower_red2, upper_red2)
            pixr_right_cnt = (maskr_right==255).sum()
            pixr_cnt =  pixr_left_cnt + pixr_right_cnt
           
            # Get how many blue pixels in the image
            maskb_left = cv2.inRange(img_left, lower_blue, upper_blue)
            pixb_left_cnt = (maskb_left==255).sum() 
            maskb_right = cv2.inRange(img_right, lower_blue, upper_blue)
            pixb_right_cnt = (maskb_right==255).sum()
            pixb_cnt =  pixb_left_cnt + pixb_right_cnt
           
            
            # Get how many green pixels in the image
            maskg_left = cv2.inRange(img_left, lower_green, upper_green)
            pixg_left_cnt = (maskg_left==255).sum() 
            maskg_right = cv2.inRange(img_right, lower_green, upper_green)
            pixg_right_cnt = (maskg_right==255).sum()
            pixg_cnt =  pixg_left_cnt + pixg_right_cnt
            
            # Get how many gyello2 pixels in the image
            masky_left = cv2.inRange(img_left, lower_yellow, upper_yellow)
            pixy_left_cnt = (masky_left==255).sum() 
            masky_right = cv2.inRange(img_right, lower_yellow, upper_yellow)
            pixy_right_cnt = (masky_right==255).sum()
            pixy_cnt =  pixy_left_cnt + pixy_right_cnt

            # Now see pixels of which colour are the highest and assign thos evalues for use in the later
            # part of the program
            if ((pixr_cnt > pixb_cnt) and (pixr_cnt > pixg_cnt) and (pixr_cnt > pixy_cnt)) and (myColour == 'red'):
                print("Found Red Image")
                pix_left_cnt = pixr_left_cnt
                pix_right_cnt = pixr_right_cnt
                pix_cnt = pixr_cnt
            elif ((pixb_cnt > pixr_cnt) and (pixb_cnt > pixg_cnt) and (pixb_cnt > pixy_cnt)) and (myColour == 'blue'):
                print("Found Blue image")
                pix_left_cnt = pixb_left_cnt
                pix_right_cnt = pixb_right_cnt
                pix_cnt = pixb_cnt
            elif ((pixg_cnt > pixr_cnt) and (pixg_cnt > pixb_cnt) and (pixg_cnt > pixy_cnt)) and (myColour == 'green'):
                print("Found Green Image")
                pix_left_cnt = pixg_left_cnt
                pix_right_cnt = pixg_right_cnt
                pix_cnt = pixg_cnt
            elif ((pixy_cnt > pixr_cnt) and (pixy_cnt > pixg_cnt) and (pixy_cnt > pixb_cnt)) and (myColour == 'yellow'):
                print("Found Yellow Image")
                pix_left_cnt = pixy_left_cnt
                pix_right_cnt = pixy_right_cnt
                pix_cnt = pixy_cnt
            else:
                print("NO IMAGE FOUND")
                pix_left_cnt = 0
                pix_right_cnt = 0
                pix_cnt = 0
 
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
            if colourDone == False:
                if (pix_cnt > threshhold):
                  got_pixel = True
                  turn_speed = turn_speed_default
                  if pix_left_cnt > pix_right_cnt:
                    pic_on_left = True
                  else:
                    pic_on_left = False

                  print("pix_left_cnt = ",pix_left_cnt," pix_right_cnt = ",pix_right_cnt)
                  print("Going forward")
                  burt_the_robot.forward(fwd_speed)  
                else:
                    if (got_pixel): # that means turn towards the picture
                        print("got_pixel = ",got_pixel," pic_on_left = ",pic_on_left)
                        if (pic_on_left) and (l >= dis):
                            direction= "left"
                        else:
                            if (r >= dis ):
                                direction = "right"
                            else:
                                direction = "backward"
                    else:
                        if l < dis and r < dis:
                            direction = "backward"
                        else:
                            if l < dis and direction == "left":
                                direction = "right"    
                            if r < dis and direction == "right":
                                direction = "left"
                            if m < dis and direction == "forward":
                                direction = "backward"
                            
                            if  direction == "backward":
                                if l > dis:
                                    direction = "left"
                                elif r > dis:
                                    direction = "right"
                                elif m > dis:
                                    direction = "forward"
                                else:
                                    direction = "backward"
                          
                    got_pixel = False 
                    print("Changing direction to ",direction)
                    if direction == "left":
                        burt_the_robot.left(turn_speed)
                    elif direction == "right":
                        burt_the_robot.right(turn_speed)
                    elif direction == "forward":
                        burt_the_robot.forward(fwd_speed)
                    else:
                        burt_the_robot.backward(fwd_speed)

                sleep(sleep_val)
                image_tg= "/home/pi/Pictures/" + str(myColour) + "-" + str(filecnt) + "-" +  str(pix_cnt)  + "-" + str(l) + "-"  + str(m) + "-" + str(r) + "-" + ".png"
                filecnt = filecnt + 1 
                call(["cp", img_dest, image_tg])
                  # Remove pictures afterwards.
                # show the imgs
                #cv2.imshow("img", np.hstack([img, output]))
                #cv2.waitKey(0)

            ##
    burt_the_robot.stop()
    
def dpad(pos):
    global counter
    # pressed any button yet to change it by 1
    if pos.top:
        print("up") # If the position of the press is up, then print 'up' 
        set_colour() # and call the set_colour() function
    if pos.bottom:
        print("down") # If the position of the press is down, print 'down' 
        counter += 1 # and change 'counter' by 1 because we have now pressed
        # the bottom part of the button
        if counter <= 1:
            main_loop() # Call the main_loop function# If the 'counter' is greater than or less than 2, which
            # means we have pressed the bottom part of the button twice,
    # then break out of the 'if pos.bottom' loop so
bd.when_pressed = dpad
pause()
