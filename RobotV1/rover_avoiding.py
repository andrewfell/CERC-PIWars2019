# CERC Wall avoiding (sort of) Robot
# Uses RaspirobotV3 board and software 

from rrb3 import *
import time, random

BATTERY_VOLTS = 7
MOTOR_VOLTS = 6

rr = RRB3(BATTERY_VOLTS, MOTOR_VOLTS)



for n in range(5):
    rr.set_led1(0)
    rr.set_led2(0)
    time.sleep(0.5)
    rr.set_led1(1)
    rr.set_led2(1)
    time.sleep(0.5)

threshold = 40
threshold2 = 60

forward_speed = 0.6  #1 is 100% (full speed), 0 is 0%
turning_speed = 0.5 #turn at half speed

def measure_distance(): # Takes a rolling average of 2, to avoid spurious measurements
    dist = []
    for n in range(2):
        distance = rr.get_distance()
        dist.append(distance)
    distance_ave = sum(dist)/len(dist)
    print(distance_ave)
    return distance_ave
    


try:
    while True:
        distance = measure_distance()
        if distance < threshold :
            if random.randint(1, 2) == 1:
                while distance < threshold2:
                    rr.left(0, turning_speed) 
                    distance = measure_distance()
            else:
                while distance < threshold2:
                    rr.right(0, turning_speed) 
                    distance = measure_distance()                
        else:
            rr.forward(0, forward_speed)

finally:
    print("Exiting")
    rr.cleanup()
