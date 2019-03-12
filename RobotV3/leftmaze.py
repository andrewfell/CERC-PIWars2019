#Left Hand Wall Follower method of getting through a maze
#The Robot will follow the left-hand wall 
#Each time there is an opening on the left-hand side the robot will take that turning
#If it is a dead end the robot will turn around 180 degrees and look for the next left (this will be back along the original path, if there are no openings in the side path it has taken. 
#When the robot reaches a point where there is no wall on the right or in front, it has reached the end of the maze, so needs to stop.


#Motor program to drive forward, backward, left, right and spin
#UDS sensor program to look for gaps in maze, left, right and obstacles in front 
#Distance to obstacle vs speed (logic loop, where speed is inversely proportional to distance to obstacle)

from gpiozero import Robot, DistanceSensor
from time import sleep
import CERCBot
import random

burt_the_robot = Robot(left=(8, 7), right=(21, 20)) 
left_echo_pin = 14
left_trigger_pin = 15
centre_echo_pin = 17
centre_trigger_pin = 4
right_echo_pin = 23
right_trigger_pin = 18


threshold = 20 # made these a bit bigger
threshold2 = 25
dead_end = 0
fast = 0.7 # need to slow it down with Lipo battery!
slow = 0.6

def go_forwards(speed):
	burt_the_robot.forward(speed)
	print("Going forwards")


def go_backwards(speed):
	burt_the_robot.backward(speed)
	print("Going backwards")


def go_left(speed):
	burt_the_robot.left(speed)
	print("Turning Left")


def go_right(speed):
	burt_the_robot.right(speed)
	print("Turning Right")


try:
	while True:
	
		#take UDS readings
		left_distance = CERCBot.calc_dist_cm_v2(left_trigger_pin, left_echo_pin)  # updeted to "v2" as per Rishan/Alok's change
		centre_distance = CERCBot.calc_dist_cm_v2(centre_trigger_pin, centre_echo_pin)
		right_distance = CERCBot.calc_dist_cm_v2(right_trigger_pin, right_echo_pin)
		
		#print the results on the screen. Distance is in centimetres
		print(left_distance, centre_distance, right_distance)
	
	#look for left turns if way ahead is available	
		if left_distance > threshold and centre_distance > threshold and right_distance < threshold:
			go_left(fast)
		elif left_distance > threshold and centre_distance < threshold and right_distance < threshold:
			go_left(fast)

		#ANDY ADDED THIS: the robot needs to turn right when it sees a right hand turn. .
		elif left_distance < threshold and centre_distance < threshold and right_distance > threshold:
			go_right(fast)		
		elif left_distance < threshold and centre_distance > threshold and right_distance > threshold:
			go_right(fast)		



		elif left_distance > threshold and centre_distance < threshold and right_distance < threshold:
			go_left(fast)
		elif left_distance < threshold2 and centre_distance < threshold2 and right_distance < threshold2:
			print('Dead End')
			dead_end += 1
			go_right(slow)
			sleep(0.1)	
		elif left_distance > threshold and centre_distance < threshold and right_distance > threshold:
			if left_distance > right_distance:
				go_left(fast)
				sleep(0.5) # some sleep needed here
			else: 
				go_left(slow)
				sleep(0.5) # some sleep heeded here

		elif left_distance > threshold2 and centre_distance > threshold2 and right_distance > threshold2:
			go_forwards(fast)
			dead_end = 0
		elif left_distance < threshold2 or centre_distance < threshold2 or right_distance < threshold2:
			go_forwards(slow)

		if dead_end == 5:
			print("Can't get through - turning around!")
			if left_distance < right_distance :
				go_right(fast)
			else:
				go_left(fast)
			sleep(1)
			dead_end = 0


except Exception as excep:
	print(excep)
	burt_the_robot.stop()