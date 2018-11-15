from gpiozero import Robot
from time import sleep
##### Right Motor #####
mc_in1=8
mc_in2=7
##### Left Motor #####
mc_in3=21                                       
mc_in4=20
fast = 0.8
med = 0.5
slow=0.2

car = Robot(left=(mc_in1,mc_in2),right=(mc_in3,mc_in4))

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
    
car.forward(speed=med, curve_left=0.5)
sleep(1)
car.backward(speed=med, curve_right=0.5)
car.stop()