# The robot must go in the following order: Red, Blue, Yellow and Green
# import the necessary packages
import numpy as np
import cv2
from time import sleep
from subprocess import call
import time
b_l_1=10



h_upper = 0
h_lower = 180
s_upper = 0
s_lower = 255
v_upper = 0
v_lower = 255
a = 110/100
b = a*255
print ("a = ",a)
print ("b = ",b)

#Red:
lower_black = [340/2, (10*255)/100, (10*255)/100]
upper_black = [360/2, (30*255)/100, (60*255)/100]
lower_black2 = [0/2, (10*255)/100, (10*255)/100]
upper_black2 = [20/2, (30*255)/100, (70*255)/100]

#Red:
lower_red1 = [335/2, (70/100)*255, (70/100)*255]
upper_red1 = [365/2, (110/100)*255, (110/100)*255]
#Blue:
lower_blue = [175/2, (40*255)/100, (70*255)/100]
upper_blue = [215/2, (90*255)/100, (120*255)/100]
#Green:
lower_green = [75/2, (20*255)/100, (40*255)/100]
upper_green = [115/2, (100*255)/100, (110*255)/100]
#Yellow:
lower_yellow = [40/2, (20*255)/100, (70*255)/100]
upper_yellow = [65/2, (90*255)/100, (110*255)/100]
# create NumPy arrays from the boundaries
lower_red1 = np.array(lower_red1, dtype = "uint8")
upper_red1 = np.array(upper_red1, dtype = "uint8")
lower_green = np.array(lower_green, dtype = "uint8")
upper_green = np.array(upper_green, dtype = "uint8")
lower_blue = np.array(lower_blue, dtype = "uint8")
upper_blue = np.array(upper_blue, dtype = "uint8")
lower_yellow = np.array(lower_yellow, dtype = "uint8")
upper_yellow = np.array(upper_yellow, dtype = "uint8")

colours = ['red']
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

for k in range(len(colours)):
    myColour = colours[k]
    print('Finding colour',myColour)
    filecnt = 1
    img = cv2.imread(img_dest)
    img = img[0:310, 0:399]
    cv2.imshow("img", np.hstack([img]))
    cv2.waitKey(0)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #img = cv2.GaussianBlur(img,(11,11),100) # The last value changes the amount of blur, in our case the highest
    
    row,col,channel = img.shape
    print("lower_red1[0] = ",lower_red1[0]," lower_red1[1] = ",lower_red1[1]," lower_red1[2] = ",lower_red1[2] ) 
    print("upper_red1[0] = ",upper_red1[0]," upper_red1[1] = ",upper_red1[1]," upper_red1[2] = ",upper_red1[2] ) 
    for i in range(row):
       for j in range(col):
            #if is_black(img[i,j][0],img[i,j][1],img[i,j][2]) == False:
            if img[i,j][0] > lower_red1[0] and img[i,j][0] < lower_red1[0]:
                if img[i,j][1] > lower_red1[1] and img[i,j][1] < lower_red1[1]:
                    print("PIX1 = ", img[i,j]) 
                    if img[i,j][2] > lower_red1[2] and img[i,j][2] < lower_red1[2]:
                        print("PIX = ", img[i,j])    
            h_upper = get_bigger(h_upper,img[i,j][0])
            h_lower = get_lower(h_lower,img[i,j][0])
            s_upper = get_bigger(s_upper,img[i,j][1])
            s_lower = get_lower(s_lower,img[i,j][1])
            v_upper = get_bigger(v_upper,img[i,j][2])
            v_lower = get_lower(v_lower,img[i,j][2])
            
    #Create the masks    
    #if myColour == 'red':
    maskr1 = cv2.inRange(img, lower_red1, upper_red1)
    #row,col = maskr1.shape
    #for i in range(row):
    #    for j in range(col):
    #        print("PIX = ", maskr1[i,j])
   
    pixr_cnt = (maskr1==255).sum() 
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
    print ("pixy_cnt = ",pixy_cnt)
    print ("h_u = ",h_upper," h_l = ",h_lower)        
    print ("s_u = ",s_upper," s_l = ",s_lower)        
    print ("v_u = ",v_upper," v_l = ",v_lower)        
        ## If colour is greater than threshold (i.e. it is looking at it clearly
        ## and any of the distabnce is too less, i.e. it is either in the corner
        ## or head on to the colour that means it is done for that colour
            # Remove pictures afterwards.
        # show the imgs
    #cv2.imshow("img", np.hstack([img]))
    #cv2.waitKey(0)

            ##
