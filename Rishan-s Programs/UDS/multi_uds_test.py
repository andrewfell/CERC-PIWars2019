from time import sleep
from gpiozero import Robot
import mypkg
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
car = Robot(left=(mc_in1,mc_in2),right=(mc_in3,mc_in4))
def left(): 
    car.left()
def right():
    car.right()
def forward():
    car.forward()
def backward():
    car.backward()
while True:
    r = mypkg.calc_dist_cm(trig_pin_r, echo_pin_r)
    l = mypkg.calc_dist_cm(trig_pin_l, echo_pin_l)
    m = mypkg.calc_dist_cm(trig_pin_m, echo_pin_m)
    b = mypkg.compare(l,m,r)
    print(' l= ',l," m = ",m," r = ",r)
    print(b)
    if b == 1:
        print('Turning Left.')
        left() 
    if b == 2:
        print('Going forward')
        forward()
    if b == 3:
        print('Turning Right.')
        right()
    sleep(0.3)




