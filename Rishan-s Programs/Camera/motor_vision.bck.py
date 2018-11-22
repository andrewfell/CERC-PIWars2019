# import the necessary packages
from gpiozero import InputDevice, OutputDevice, LED
from time import sleep, time
import numpy as np
import argparse
import cv2
from picamera import PiCamera
from subprocess import call

## UDS tuff
trig = OutputDevice(4)
echo = InputDevice(17)
uds_led = LED(3)

## Camera stuff
camera = PiCamera()
image_dest = "/home/pi/My Projects/AI Python projects/opencv-python-color-detection/test.png"
camera.resolution = (200, 200)
camera_led = LED(2)

# construct the argument parse and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", help = "path to the image")
args = vars(ap.parse_args())

# loop over the boundaries
lower_r = [17, 15, 100]
upper_r = [50, 56, 200]

lower_g = [17, 0, 15]
upper_g = [50, 200, 56]

# create NumPy arrays from the boundaries
lower_r = np.array(lower_r, dtype = "uint8")
upper_r = np.array(upper_r, dtype = "uint8")

lower_g = np.array(lower_g, dtype = "uint8")
upper_g = np.array(upper_g, dtype = "uint8")

###############################
# Get the functions here
# UDS Functions
###############################
def get_pulse_time():
    trig.on()
    sleep(0.00001)
    trig.off()
    while echo.is_active == False:
            pulse_start = time()

    while echo.is_active == True:
            pulse_end = time()

    sleep(0.06)

    return pulse_end - pulse_start

def calculate_distance(duration):
    speed = 343
    distance = speed * duration / 2
    return distance

def uds_hit():
    duration = get_pulse_time()
    distance = calculate_distance(duration)
    distance_cm = distance*100
    ds_int = int(distance_cm)
    print(ds_int, 'cm')
    my_val = 0
    if ds_int < 10 :
        uds_led.on()
        my_val = 1
    else:
        uds_led.off()
    return my_val

###############################
# Get the functions here
# Camera functions
###############################
def get_red():
    camera.capture(image_dest,format='png')
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
       
    print ("red = ",red)
    call(["rm", image_dest])

    if red > 500 :
        camera_led.on()
        # go_forward
    else:
        camera_led.off()
    
# show the images
    cv2.imshow("images", np.hstack([image, output]))
    cv2.waitKey(0)
##
    return red

##################################################################################
# MAIN
##################################################################################
## Start with LEDs off
uds_led.off()
camera_led.off()
got_red = 0
###############################
# Check the status of UDS -
# Are we about to hit ?
###############################
about_to_hit = uds_hit()
# If yes, stop everything and
## make a decision - go back @? or turn left/right
## and skip everything else

# otherwise go ahea and look for red
if (about_to_hit == 0):
    got_red = get_red()
else:
    print("about to hit To be implemented ")
    ## call turn_left()
if (got_red == 1):
    print("To be implemented go forward")
    

