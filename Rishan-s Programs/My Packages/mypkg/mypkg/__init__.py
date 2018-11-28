from gpiozero import InputDevice, OutputDevice, LED, Robot
from time import sleep, time
import numpy as np
import argparse
import cv2
from picamera import PiCamera
from subprocess import call

    
###########################################################
# Name
# arg1 = echo pin
# arg2 = trigger pin
# Description : what does it do 
###########################################################

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

def calculate_distance(duration):
    speed = 343
    distance = speed * duration / 2
    return distance
    

#################

def calc_dist_cm(trig_pin, echo_pin):
    duration = get_pulse_time(trig_pin, echo_pin)
    distance = calculate_distance(duration)
    distance_cm = distance*100
    dis_cm = int(distance_cm)
    #print(dis_cm, 'cm')
    return dis_cm

def uds_hit(trig_pin, echo_pin, uds_pin):
    uds_led = LED(uds_pin)
    ds_int = calc_dist_cm(trig_pin, echo_pin, uds_pin)
    my_val = 0
    if ds_int < 10 :
        uds_led.on()
        my_val = 1
    else:
        uds_led.off()
    return my_val

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

def my_endfunc(sig, frame):
        print('You pressed Ctrl+C!')
        log.close()
        sys.exit(0)






