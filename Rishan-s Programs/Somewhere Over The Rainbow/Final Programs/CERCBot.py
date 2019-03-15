
# CERCBot library by Rishthefish
# Nice work, Rishan!

# The libraries that we require are imported at the beginning of the program
# From gpiozero, we only need InputDevice and OutputDevice rather than the DistanceSensor module (which appears to output lots of errors!).
# https://gpiozero.readthedocs.io/en/stable/api_input.html#inputdevice
# https://gpiozero.readthedocs.io/en/stable/api_output.html#outputdevice
from gpiozero import InputDevice, OutputDevice
import RPi.GPIO as GPIO

# The time library is used for the sleep command
from time import sleep, time

#  I have commented out these libraries for now.. Maybe we'll use them later with the camera
#import numpy as np
#import argparse
#import cv2
#from picamera import PiCamera
#from subprocess import call

    
###########################################################
# Name
# arg1 = echo pin
# arg2 = trigger pin
# Description : what does it do 
###########################################################


# This function meausres the time between the ultrasound pulse being sent out and the echo signal that returns
def get_pulse_time(trig_pin, echo_pin):
    ###### Add your echo and trig pin as an argument 
    trig = OutputDevice(trig_pin)
    echo = InputDevice(echo_pin)
    trig.on()
    sleep(0.00001)
    trig.off()
    pulse_start = time()
    while echo.is_active == False:
            pulse_start = time()
    pulse_end = time()        
    while echo.is_active == True:
            pulse_end = time()
    
    return pulse_end - pulse_start
# This is another implementation of get_pulse_time() which makes use of the RPi.GPIO library
# This is needed because Rishan's robot faced problems with get_pulse_time. The problem is explained in detail 
# in issue #4

def get_pulse_time_v2(trig_pin, echo_pin):
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)

    GPIO.setup(trig_pin, GPIO.OUT)
    GPIO.setup(echo_pin, GPIO.IN)
    cnt1 = 0
    cnt2 = 0

    GPIO.output(trig_pin, True)
    sleep(0.00001)
    GPIO.output(trig_pin, False)

    start = time()
    while GPIO.input(echo_pin) == 0:
        start = time()
        cnt1 += 1
        if cnt1 > 1000:
            break

    stop = time()
    while GPIO.input(echo_pin) == 1:
        stop = time()
        cnt2 += 1
        if cnt2 > 1000:
            break

    return (stop - start)

# The distance is calculated by dividing the speed of sound by the time is took for the pulse to return
# Divide by 2 because we only want the distance from the robot to the wall, not the total distance from the robot
# to the wall and back again
def calculate_distance(duration):
    speed = 343
    distance = speed * duration / 2
    return distance
    

# This function uses both of the above functions, then return the result (in cms) to the main program.
def calc_dist_cm(trig_pin, echo_pin):
    duration = get_pulse_time(trig_pin, echo_pin)
    distance = calculate_distance(duration)
    distance_cm = distance*100
    dis_cm = int(distance_cm)
    # If the measured distance is greater than 70cm, then set the distance to 70cm.  
    # Otherwise the measurement is noisy and it can make the robot make incorrect decisions on which way to turn.
    if dis_cm > 70:
        dis_cm = 70
    #print(dis_cm, 'cm')  << Have removed this as the distance is reported in the main program
    return dis_cm

# The following function makes use of get_pulse_time_v2()

def calc_dist_cm_v2(trig_pin, echo_pin):
    duration = get_pulse_time_v2(trig_pin, echo_pin)
    distance = calculate_distance(duration)
    distance_cm = distance*100
    dis_cm = int(distance_cm)
    # If the measured distance is greater than 150cm, then set the distance to 150cm.  
    # Otherwise the measurement is noisy and it can make the robot make incorrect decisions on which way to turn.
    if dis_cm > 150:
        dis_cm = 150
    #print(dis_cm, 'cm')  << Have removed this as the distance is reported in the main program
    return dis_cm


# This function is not required because the Robot needs to action this in the main program but turning left or right.
# def uds_hit(trig_pin, echo_pin, uds_pin):
#     uds_led = LED(uds_pin)
#     ds_int = calc_dist_cm(trig_pin, echo_pin, uds_pin)
#     my_val = 0
#     if ds_int < 10 :
#         uds_led.on()
#         my_val = 1
#     else:
#         uds_led.off()
#     return my_val


#  this is better done in the main program, so it's not really needed here.
def compare(a,b,c):
    if c >= b and c >= a:
#        biggest_val = c
        biggest = 3
    if b >= a and b >= c:
#        biggest_val = b
        biggest = 2
    if a >= b and a >= c:
#        biggest_val = a
        biggest = 1
    if a == b and a == c:
#        biggest_val = c
        biggest = 3
    return biggest


#  We don't need this,  you can use "Try" and "Except" to stop the robot when you press ctrl-C.
#def my_endfunc(sig, frame):
#        print('You pressed Ctrl+C!')
#        log.close()
#        sys.exit(0)
