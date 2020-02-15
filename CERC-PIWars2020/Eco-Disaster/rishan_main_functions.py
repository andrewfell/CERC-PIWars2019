# The robot must go in the following order: Red, Blue, Yellow and Green
# import the necessary packages
import numpy as np
import os
import cv2
import mask

captured = False
x_max = 400
y_max = 400
x_mod = x_max-130
y_mod = y_max-1
h_upper = 0
h_lower = 180
s_upper = 0
s_lower = 255
v_upper = 0
v_lower = 255
threshhold = 50 # for barrel
max_val = 40000

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


green_barrel_source_dir = "/home/pi/Pictures/green_barrel"
red_barrel_source_dir = "/home/pi/Pictures/red_barrel"

## Green barrel
myfolder=green_barrel_source_dir
## Iterate for each picture
for img in os.listdir(myfolder):
    myfilepath = myfolder + '/' + img
    img = cv2.imread(myfilepath)
    #print(img.shape)
    #img = img[0:270, 0:399]
    cv2.imshow("img", np.hstack([img]))
    cv2.waitKey(0)
    img_down = img[round(img.shape[0]/2):img.shape[0],0:(img.shape[1]-1)]
#     cv2.imshow("img_down", np.hstack([img_down]))
#     cv2.waitKey(0)
    img_up = img[0:round(img.shape[0]/2),0:img.shape[1]]
#     cv2.imshow("img_up", np.hstack([img_up]))
#     cv2.waitKey(0)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    img = cv2.GaussianBlur(img,(11,11),100) # The last value changes the amount of blur, in our case the highest

    maskr1 = cv2.inRange(img, mask.lower_red1, mask.upper_red1)
    maskr2 = cv2.inRange(img, mask.lower_red2, mask.upper_red2)
    upper_pixr_cnt = (maskr1==255).sum() + (maskr2==255).sum()
    
    lower_maskr1 = cv2.inRange(img_down, mask.lower_red1, mask.upper_red1)
    lower_maskr2 = cv2.inRange(img_down, mask.lower_red2, mask.upper_red2)
    lower_pixr_cnt = (lower_maskr1==255).sum() + (lower_maskr2==255).sum()
    
    maskb = cv2.inRange(img, mask.lower_blue, mask.upper_blue)
    pixb_cnt = (maskb==255).sum()
    
    upper_maskg = cv2.inRange(img_up, mask.lower_green, mask.upper_green)
    upper_pixg_cnt = (upper_maskg==255).sum()
    
    lower_maskg = cv2.inRange(img_down, mask.lower_green, mask.upper_green)
    lower_pixg_cnt = (lower_maskg==255).sum()
    
    masky = cv2.inRange(img, mask.lower_yellow, mask.upper_yellow)
    pixy_cnt = (masky==255).sum()
    
    if lower_pixg_cnt > upper_pixg_cnt or lower_pixr_cnt > upper_pixr_cnt:
        captured = True
    else:
        captured = False
        
    print ("==========================================")
    print ("filepath = ",myfilepath)
    print ("Threshold = ",threshhold)
    print ("pixr_up_cnt = ",upper_pixr_cnt)
    print ("pixr_down_cnt = ",lower_pixr_cnt)
    print ("pixg_up_cnt = ",upper_pixg_cnt)
    print ("pixg_down_cnt = ",lower_pixg_cnt)
    print ("pixb_cnt = ",pixb_cnt)
    print ("pixy_cnt = ",pixy_cnt)
    print ("is captured = ",captured)
    print("==========================================")
 
    ## If colour is greater than threshold (i.e. it is looking at it clearly
    ## and any of the distabnce is too less, i.e. it is either in the corner
    ## or head on to the colour that means it is done for that colour
    # Remove pictures afterwards.
    # show the imgs
    #cv2.imshow("img", np.hstack([img]))
    #cv2.waitKey(0)

