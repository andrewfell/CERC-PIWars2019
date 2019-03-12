from gpiozero import Robot, LineSensor
from time import sleep

robot = Robot(left=(8, 7),right=(21, 20))
left_sensor = LineSensor(27)
right_sensor= LineSensor(22)
#The above chosen to avoid GPIO pins used for UDS
speed = 0.4
def motor_speed():
    while True:
        left_detect = int(left_sensor.value)
        right_detect = int(right_sensor.value)
        ## This first bit manages what to do if both are true or false
        if left_detect == 1 and right_detect == 1:
            left_mot = 1
            right_mot = 1
        if left_detect == 0 and right_detect == 0:
            left_mot = 0
            right_mot = 0
        ##Left/right corrections
        if left_detect == 0 and right_detect == 1:          
            left_mot = -1
            right_mot = 1
        if left_detect == 1 and right_detect == 0:           
            right_mot = -1
            left_mot = 1
        #print(r-1)
        yield (right_mot * speed, left_mot * speed)

robot.source = motor_speed()

sleep(90)
robot.stop()
robot.source = None
robot.close()
left_sensor.close()
right_sensor.close()

# I've noticed that the actual piwars challenge uses a white line on black background. This program would need inverting to suit.


