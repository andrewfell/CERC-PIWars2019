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
folder=green_barrel_source_dir
## Iterate for each picture
for img in os.listdir(folder):
    filepath = folder + '/' + img
    img = cv2.imread(filepath)
    img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
    #print(img.shape)
    #img = img[0:270, 0:399]
    cv2.imshow("img", np.hstack([img]))
    cv2.waitKey(0)
    img_down = img[round(img.shape[0]/2):img.shape[0],0:(img.shape[1]-1)]
    img_up = img[0:round(img.shape[0]/5),0:img.shape[1]]

    cv2.imshow("img", np.hstack([img_up]))
    cv2.waitKey(0)
    
    img_left = img[0:img.shape[1],0:round(img.shape[0]/2)]
    img_right = img[0:(img.shape[1]-1),round(img.shape[0]/2):img.shape[0]]
    
    # Red values #
    maskr1 = cv2.inRange(img, mask.lower_red1, mask.upper_red1)
    maskr2 = cv2.inRange(img, mask.lower_red2, mask.upper_red2)
    upper_pixr_cnt = (maskr1==255).sum() + (maskr2==255).sum()
    
    lower_maskr1 = cv2.inRange(img_down, mask.lower_red1, mask.upper_red1)
    lower_maskr2 = cv2.inRange(img_down, mask.lower_red2, mask.upper_red2)
    lower_pixr_cnt = (lower_maskr1==255).sum() + (lower_maskr2==255).sum()

    right_maskr1 = cv2.inRange(img_right, mask.lower_red1, mask.upper_red1)
    right_maskr2 = cv2.inRange(img_right, mask.lower_red2, mask.upper_red2)
    right_pixr_cnt = (right_maskr1==255).sum() + (right_maskr2==255).sum()
    
    left_maskr1 = cv2.inRange(img_left, mask.lower_red1, mask.upper_red1)
    left_maskr2 = cv2.inRange(img_left, mask.lower_red2, mask.upper_red2)
    left_pixr_cnt = (left_maskr1==255).sum() + (left_maskr2==255).sum()

    # Blue values #
    upper_maskb = cv2.inRange(img_up, mask.lower_blue, mask.upper_blue)
    upper_pixb_cnt = (upper_maskb==255).sum()
    
    lower_maskb = cv2.inRange(img_down, mask.lower_blue, mask.upper_blue)
    lower_pixb_cnt = (lower_maskb==255).sum()

    right_maskb = cv2.inRange(img_right, mask.lower_blue, mask.upper_blue)
    right_pixb_cnt = (right_maskb==255).sum()
    
    left_maskb = cv2.inRange(img_left, mask.lower_blue, mask.upper_blue)
    left_pixb_cnt = (left_maskb==255).sum()
    
    # Green values #
    upper_maskg = cv2.inRange(img_up, mask.lower_green, mask.upper_green)
    upper_pixg_cnt = (upper_maskg==255).sum()
    
    lower_maskg = cv2.inRange(img_down, mask.lower_green, mask.upper_green)
    lower_pixg_cnt = (lower_maskg==255).sum()

    right_maskg = cv2.inRange(img_right, mask.lower_green, mask.upper_green)
    right_pixg_cnt = (right_maskg==255).sum()
    
    left_maskg = cv2.inRange(img_left, mask.lower_green, mask.upper_green)
    left_pixg_cnt = (left_maskg==255).sum()

    # Yellow values #
    upper_masky = cv2.inRange(img_up, mask.lower_yellow, mask.upper_yellow)
    upper_pixy_cnt = (upper_masky==255).sum()
    
    lower_masky = cv2.inRange(img_down, mask.lower_yellow, mask.upper_yellow)
    lower_pixy_cnt = (lower_maskb==255).sum()

    right_masky = cv2.inRange(img_right, mask.lower_yellow, mask.upper_yellow)
    right_pixy_cnt = (right_maskb==255).sum()
    
    left_masky = cv2.inRange(img_left, mask.lower_yellow, mask.upper_yellow)
    left_pixy_cnt = (left_maskb==255).sum()
    
    if lower_pixg_cnt > upper_pixg_cnt or lower_pixr_cnt > upper_pixr_cnt:
        captured = True
    else:
        captured = False
    
    print("==========================================================")
    
    print("image = ",filepath)
    print("Threshold= ",threshhold)
    print("Captured = ",captured)
    
    print("========================GREEN=============================")
    print("lower_pixg = ",lower_pixg_cnt)
    print("upper_pixg = ",upper_pixg_cnt)
    print("right_pixg = ",right_pixg_cnt)
    print("left_pixg = ",left_pixg_cnt)
    
    print("========================RED===============================")
    print("lower_pixr = ",lower_pixr_cnt)
    print("upper_pixr = ",upper_pixr_cnt)
    print("right_pixr = ",right_pixr_cnt)
    print("left_pixr = ",left_pixr_cnt)
    
    print("========================BLUE==============================")
    print("lower_pixb = ",lower_pixb_cnt)
    print("upper_pixb = ",upper_pixb_cnt)
    print("right_pixb = ",right_pixb_cnt)
    print("left_pixb = ",left_pixb_cnt)
    
    print("========================YELLOW=============================")
    print("lower_pixy = ",lower_pixy_cnt)
    print("upper_pixy = ",upper_pixy_cnt)
    print("right_pixy = ",right_pixy_cnt)
    print("left_pixy = ",left_pixy_cnt)

    print("==========================================================")