# The robot must go in the following order: Red, Blue, Yellow and Green
# import the necessary packages
import os
import numpy as np
import cv2
from time import sleep
from subprocess import call
import time
# We'll use the distance sensor module in our CERCBot library (CERCBot.py)

threshhold = 100 #pixels
left_echo_pin = 14
left_trigger_pin = 15
centre_echo_pin = 17
centre_trigger_pin = 4
right_echo_pin = 23
right_trigger_pin = 18
filecnt = 1
speed = 0.4
dis = 11
sl = 0.4
#Red:
lower_black = [330/2, (50*2.55), (50*2.55)]
upper_black = [360/2, (100*2.55), (100*2.55)]
lower_black2 = [0/2, (10*2.55), (10*2.55)]
upper_black2 = [20/2, (30*2.55), (70*2.55)]

#Red:
lower_red1 = [325/2, (55*2.55), (50*2.55)]
upper_red1 = [365/2, (100*2.55), (100*2.55)]

lower_red2 = [0/2, (55*2.55), (50*2.55)]
upper_red2 = [20/2, (80*2.55), (80*2.55)]
#Blue:
lower_blue = [140/2, (0*2.55), (60*2.55)]
upper_blue = [200/2, (50.55), (100*2.55)]
#Green:
lower_green = [40/2, (40*2.55), (30*2.55)]
upper_green = [100/2, (100*2.55), (100*2.55)]
#Yellow:
lower_yellow = [30/2, (60*2.55), (60*2.55)]
upper_yellow = [58/2, (100*2.55), (100*2.55)]

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

colours = ['red','yellow']
img_dest = "/home/pi/color.png"
# In the specific order ('red','blue','yellow','green'), go to each zone
#and stop when it is less than 15cm away.
direction = "left"
print("starting")
def get_bigger(x,y):
    if x > y:
        return x
    else:
        return y
def get_lower(x,y):
    if x < y:
        return x
    else:
        return y
def is_black(h,s,v):
    black = False
    black2 = False
    if h >= lower_black[0] and h <= upper_black[0]:
        if s >= lower_black[1] and s <= upper_black[1]:
            if v >= lower_black[2] and v <= upper_black[2]:
                black = True
    if h >= lower_black2[0] and h <= upper_black2[0]:
        if s >= lower_black2[1] and s <= upper_black2[1]:
            if v >= lower_black2[2] and v <= upper_black2[2]:
                black2 = True

    return (black or black2)

h_upper = 0
h_lower = 180
s_upper = 0
s_lower = 255
v_upper = 0
v_lower = 255
myfolder = './red'
for k in range(len(colours)):
    myColour = colours[k]
    myfolder = './' + myColour
    for img_dest in os.listdir(myfolder):
        myfilepath = myfolder + '/' + img_dest
        print('Finding colour',myColour, " in ",myfilepath)
        img = cv2.imread(myfilepath)
        img = img[0:270, 0:399]
        #cv2.imshow("img", np.hstack([img]))
        #cv2.waitKey(0)
        img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
        img = cv2.GaussianBlur(img,(11,11),100) # The last value changes the amount of blur, in our case the highest
    
    #    row,col,channel = img.shape
    #    for i in range(row):
    #       for j in range(col):
    #            h_upper = get_bigger(h_upper,img[i,j][0])
    #            h_lower = get_lower(h_lower,img[i,j][0])
    #            s_upper = get_bigger(s_upper,img[i,j][1])
    #            s_lower = get_lower(s_lower,img[i,j][1])
    #            v_upper = get_bigger(v_upper,img[i,j][2])
    #            v_lower = get_lower(v_lower,img[i,j][2])
                
        #Create the masks    
        #if myColour == 'red':
        maskr1 = cv2.inRange(img, lower_red1, upper_red1)
        maskr2 = cv2.inRange(img, lower_red2, upper_red2)
        #row,col = maskr.shape
        #for i in range(row):
        #    for j in range(col):
        #        print("PIX = ", maskr[i,j])
       
        pixr_cnt = (maskr1==255).sum()  + (maskr2==255).sum() 
        #elif myColour == 'blue':
        maskb = cv2.inRange(img, lower_blue, upper_blue)
        pixb_cnt = (maskb==255).sum()
        #elif myColour == 'green':
        maskg = cv2.inRange(img, lower_green, upper_green)
        pixg_cnt = (maskg==255).sum()
        #else:
        masky = cv2.inRange(img, lower_yellow, upper_yellow)
        pixy_cnt = (masky==255).sum()
        print("==========================================")
        print("folder = ",myfolder," image = ",img_dest)
        print ("pixr_cnt = ",pixr_cnt)
        print ("pixg_cnt = ",pixg_cnt)
        print ("pixb_cnt = ",pixb_cnt)
        print ("pixy_cnt = ",pixy_cnt)
        print ("h_u = ",h_upper," h_l = ",h_lower)        
        print ("s_u = ",s_upper," s_l = ",s_lower)        
        print ("v_u = ",v_upper," v_l = ",v_lower)        
        print("==========================================")
        ## If colour is greater than threshold (i.e. it is looking at it clearly
        ## and any of the distabnce is too less, i.e. it is either in the corner
        ## or head on to the colour that means it is done for that colour
        # Remove pictures afterwards.
        # show the imgs
        #cv2.imshow("img", np.hstack([img]))
        #cv2.waitKey(0)

                ##
