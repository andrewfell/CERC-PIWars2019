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
x_max = 400
y_max = 400
x_mod = x_max-119
y_mod = y_max-1
camera.resolution = (x_max, y_max)
threshhold = 50 #pixels
max_val = 40000
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
dis_m = 11
sl = 0.3

#Red:
lower_red1 = [325/2, (50*2.55), (70*2.55)]
upper_red1 = [365/2, (100*2.55), (100*2.55)]
#Blue:
lower_blue = [175/2, (10*2.55), (70*2.55)]
upper_blue = [215/2, (40*2.55), (100*2.55)]
#Green:
lower_green = [60/2, (40*2.55), (25*2.55)]
upper_green = [85/2, (95*2.55), (100*2.55)]
#Yellow:
lower_yellow = [30/2, (40*2.55), (20*2.55)]
upper_yellow = [50/2, (90*2.55), (100*2.55)]

# create NumPy arrays from the boundaries
lower_red1 = np.array(lower_red1, dtype = "uint8")
upper_red1 = np.array(upper_red1, dtype = "uint8")
lower_green = np.array(lower_green, dtype = "uint8")
upper_green = np.array(upper_green, dtype = "uint8")
lower_blue = np.array(lower_blue, dtype = "uint8")
upper_blue = np.array(upper_blue, dtype = "uint8")
lower_yellow = np.array(lower_yellow, dtype = "uint8")
upper_yellow = np.array(upper_yellow, dtype = "uint8")
colours = ['red','blue','yellow','green']
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
    got_pixel = False
    pic_on_left = False
         
    myColour = colours[k]
    led.off()
    print('Finding colour',myColour)
    filecnt = 1
    while colourDone == False:
        sleep_val = sl
        speed_val = speed
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

        if myColour == 'red':
            mask_left = cv2.inRange(img_left, lower_red1, upper_red1)
            mask_right = cv2.inRange(img_right, lower_red1, upper_red1)
        elif myColour == 'blue':
            mask_left = cv2.inRange(img_left, lower_blue, upper_blue)
            mask_right = cv2.inRange(img_right, lower_blue, upper_blue)
        elif myColour == 'green':
            mask_left = cv2.inRange(img_left, lower_green, upper_green)
            mask_right = cv2.inRange(img_right, lower_green, upper_green)
        else:
            mask_left = cv2.inRange(img_left, lower_yellow, upper_yellow)
            mask_right = cv2.inRange(img_right, lower_yellow, upper_yellow)

        pix_left_cnt = (mask_left==255).sum()
        pix_right_cnt = (mask_right==255).sum()
        pix_cnt = pix_left_cnt + pix_right_cnt
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
          got_pixel = True
          if pix_left_cnt > pix_right_cnt:
            pic_on_left = True
          else:
            pic_on_left = False
          print("pix_left_cnt = ",pix_left_cnt," pix_right_cnt = ",pix_right_cnt)
          
          if (m <= dis_m) or ((pix_cnt > max_val) and (m <= dis_m or l <= dis_m or r < dis_m)):
              colourDone = True
              led.on()
              burt_the_robot.backward(speed_val)
              sleep(sleep_val)
              sleep(sleep_val)
          else:
            print("Going forward")
            sleep_val = 0.3
            speed_val = 0.4
            burt_the_robot.forward(speed_val)
            
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
                if l < dis and direction == "left":
                    direction = "right"    
                if r < dis and direction == "right":
                    direction = "left"
                if (m < dis or l < dis or r < dis) and direction == "forward":
                    direction = "backward"
            got_pixel = False 
            print("Changing direction to ",direction)
            if direction == "left":
                burt_the_robot.left(speed_val)
            elif direction == "right":
                burt_the_robot.right(speed_val)
            elif direction == "forward":
                burt_the_robot.forward(speed_val)
            else:
                burt_the_robot.backward(speed_val)

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

