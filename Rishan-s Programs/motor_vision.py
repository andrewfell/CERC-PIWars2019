# import the necessary packages
from gpiozero import InputDevice, OutputDevice, LED, Robot
from time import sleep, time
import numpy as np
import argparse
import cv2
from picamera import PiCamera
from subprocess import call
import mypkg

fast = 0.8
mid = 0.5
slow=0.2
trig_pin = 4
echo_pin = 17
uds_pin = 3
camera_pin = 2
mc_in1=8
mc_in2=7
mc_in3=21                                       
mc_in4=20
res_l = 200
res_h = 200


camera = PiCamera()
camera.resolution = (res_l, res_h)

car = Robot(left=(mc_in1,mc_in2),right=(mc_in3,mc_in4))

image_dest = "/home/pi/My Projects/Robot Project/opencv-python-color-detection/test.png"
lower_g = [17, 0, 15]
upper_g = [50, 200, 56]
lower_g = np.array(lower_g, dtype = "uint8")
upper_g = np.array(upper_g, dtype = "uint8")

def get_red(image_dest, numpix, pin, res_l, res_h):
    
    lower_r = [17, 15, 100]
    upper_r = [50, 56, 200]
    lower_r = np.array(lower_r, dtype = "uint8")
    upper_r = np.array(upper_r, dtype = "uint8")
    
    camera_led = LED(pin)
    camera.capture(image_dest,format='png')
    print("Camera has taken picture")
    image = cv2.imread(image_dest)

    mask = cv2.inRange(image, lower_r, upper_r)
    output = cv2.bitwise_and(image, image, mask = mask)

    row,col,channel= output.shape
    print (" row  = ",row)
    print (" col  = ",col)
    red = 0
    for i in range(row):
        for j in range(col):
            red = red + output[i,j,2]
       
    print ("calculated red = ",red)
    call(["rm", image_dest])

    if red > numpix :
        camera_led.on()
        # go_forward
    else:
        camera_led.off()
    return red

    
def left(motor_speed): 
    print("LEFT with speed factor", motor_speed)
    car.left(speed=motor_speed)
    
def right(motor_speed):
    print("RIGHT with speed factor", motor_speed)
    car.right(speed=motor_speed)
    
def forward(motor_speed):
    print("FORWARD with speed factor", motor_speed)
    car.forward(speed=motor_speed)
    
def backward(motor_speed):
    print("BACKWARD with speed factor", motor_speed)
    car.backward(speed=motor_speed)
def stop():
    print("STOPPING ALL MOTORS")
    car.stop()
    
##################################################################################
# MAIN
##################################################################################
got_red = 0
about_to_hit = mypkg.uds_hit(trig_pin, echo_pin, uds_pin)
# otherwise go ahea and look for red
#if (about_to_hit == 0):
#    got_red = mypkg.get_red(image_dest, 200, camera_pin, res_l , res_h)
#else:
#    print("about to hit To be implemented ")
#    ## call turn_left()
#if (got_red == 1):
#    print("To be implemented go forward")
# While red = 0, then keep turning left, else, stop then go forward until 10 cm away from the wall. #####
while True:
    about_to_hit = mypkg.uds_hit(trig_pin, echo_pin, uds_pin)
    got_red = get_red(image_dest, 200, camera_pin, res_l , res_h)
    print("about_to_hit = ", about_to_hit)
    print("got_red = ", got_red)
    ## Now that we know we have a red or we are going to hit
    if (about_to_hit):
        ## Stop !! What are you thinking ?
        stop()
        print("SSSSSTTTOOOOOPPPPPPPP")
    else:
        ## Now that nobody is there .. what are you waiting for ??
        ## Check red and ,...go !
        if (got_red):
            ## Go forward
            forward(motor_speed=mid)
        else:    
            left(motor_speed=mid)
    sleep(1)
        