#This program tests that you have the motor GPIO mapping correct on your CERC Robot V2 chassis
#refer to GPIO pins allocations here: https://www.raspberrypi.org/documentation/usage/gpio/
#the 'robot' class of the gpiozero library is used below: https://gpiozero.readthedocs.io/en/stable/recipes.html#robot
#the robot should first move forward, then spin right, then spin left, then go backwards.
#if this works as expected, your GPIO mapping and motor driver board wiring is correct


#first of all, import the Robot class from the 'gpiozero' library
from gpiozero import Robot
#then import the 'sleep' class from the 'time' library (so we can add pauses in our program)
from time import sleep

#define a robot (it's called Burt! :-) ), with the GPIO pin mapping as per the GPIO in the RobotV2.md file
burt_the_robot = Robot(left=(8, 7), right=(21, 20)) # dont change this pin mapping, otherwise your robot will be different to the others!


burt_the_robot.forward() #go forward indefinitely
sleep(0.5) # sleep for 0.5seconds
burt_the_robot.right()  #spin right indefinitely
sleep(0.5) #sleep for 0.5seconds
burt_the_robot.left() #spin left indefinitely
sleep(0.5) #sleep for 0.5seconds
burt_the_robot.backward() #go backwards indefinitely
sleep(0.5) #sleep for 0.5seconds
burt_the_robot.stop() #stop!
