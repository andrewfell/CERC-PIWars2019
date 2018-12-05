from gpiozero import Robot
from time import sleep

robot = Robot(left=(8, 7), right=(21, 20))


#this program tests that you have the GPIO mapping correct
#the gpiozero library is used
#the robot should first move forward, then spin right, then spin left, then go backwards.
#if this works as expected, your GPIO mapping and motor driver board wiring is correct

robot.forward()
sleep(0.5)
robot.right()
sleep(0.5)
robot.left()
sleep(0.5)
robot.backward()
sleep(0.5)
robot.stop()
