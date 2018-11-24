from time import sleep
import time
from gpiozero import Robot
import mypkg
import signal
import sys
trig_pin_l = 15
echo_pin_l = 14
echo_pin_m = 17
trig_pin_m = 4
trig_pin_r = 18
echo_pin_r = 23
mc_in1=8
mc_in2=7
##### Left Motor #####
mc_in3=21                                       
mc_in4=20
dis = 10
sp = 0.2
car = Robot(left=(mc_in1,mc_in2),right=(mc_in3,mc_in4))
car.stop()
log = open("log.txt","w")
def my_endfunc(sig, frame):
        print('You pressed Ctrl+C!')
        log.close()
        print("I AM HAPPY")
        sys.exit(0)
signal.signal(signal.SIGINT, my_endfunc)
while True:
    r = mypkg.calc_dist_cm(trig_pin_r, echo_pin_r)
    l = mypkg.calc_dist_cm(trig_pin_l, echo_pin_l)
    m = mypkg.calc_dist_cm(trig_pin_m, echo_pin_m)
    b = mypkg.compare(l,m,r)
    print(' l= ',l," m = ",m," r = ",r)
    log.write(time.asctime())
    log.write(' == ')
    log.write(str(l))
    log.write(' ')
    log.write(str(m))
    log.write(' ')
    log.write(str(r))
    log.write('\n')
    print(b)
    if m >= dis:
        print('Forward.')
        car.forward(speed=sp)
    else:
        if b == 3:
            car.right(speed=sp)
            print('Right')
        if b == 1:
           print('Left')
           car.left(speed=sp)
    sleep(0.3)

