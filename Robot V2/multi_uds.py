from time import sleep
import time
from gpiozero import Robot
import CERCBot
import signal
import sys
## These are UDS variables:
trig_pin_l = 15
echo_pin_l = 14
echo_pin_m = 17
trig_pin_m = 4
trig_pin_r = 18
echo_pin_r = 23
##### These are motor gpios 
mc_in1=7
mc_in2=8
mc_in3=20                                       
mc_in4=21
# Dis is the maximum distance for any actions for UDS
dis = 8
# sp is the speed of the motors
sp = 0.5
# sl is the amount of sleep in the program
sl = 0.1
car = Robot(left=(mc_in1,mc_in2),right=(mc_in3,mc_in4))
car.stop()
def my_endfunc(sig, frame):
        print('You pressed Ctrl+C!')
        car.stop()
        sys.exit(0)
signal.signal(signal.SIGINT, my_endfunc)
while True:                                                                     
    print("Getting Right")
    r = CERCBot.calc_dist_cm(trig_pin_r, echo_pin_r)
    print("Getting Left")
    l = CERCBot.calc_dist_cm(trig_pin_l, echo_pin_l)
    print('Got left')
    print("Getting Middle")
    m = CERCBot.calc_dist_cm(trig_pin_m, echo_pin_m)
    print("Comparing")
    def compare(a,b,c):
        if c >= b and c >= a:
            biggest = 3
        if b >= a and b >= c:
            biggest = 2
        if a >= b and a >= c:
            biggest = 1
        if a == b and a == c:
            biggest = 3
        return biggest
    compare(r,l,m)
    print(' l= ',l," m = ",m," r = ",r)
    if m > dis and l > dis and r > dis:
        car.forward(speed=sp)
        print('Forward')
    else:
        if l > dis and b == 1:
                car.left(speed=sp)
                print('Left')
        elif r > dis and b == 3:
                car.right(speed=sp)
                print('Right')
        else:
                while r < dis and l < dis:
                        r = CERCBot.calc_dist_cm(trig_pin_r, echo_pin_r)
                        l = CERCBot.calc_dist_cm(trig_pin_l, echo_pin_l)
                        print(' l= ',l," m = ",m," r = ",r)
                        car.backward(speed=sp)
                        print('Backward')
                        sleep(sl)
        
    sleep(sl)
