
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


threshold = 20
threshold2 = 25
dead_end = 0
fast = 0.7
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
		left_distance = CERCBot.calc_dist_cm_v2(left_trigger_pin, left_echo_pin)
		centre_distance = CERCBot.calc_dist_cm_v2(centre_trigger_pin, centre_echo_pin)
		right_distance = CERCBot.calc_dist_cm_v2(right_trigger_pin, right_echo_pin)
		
		#print the results on the screen. Distance is in centimetres
		print(left_distance, centre_distance, right_distance)

		if left_distance < threshold and centre_distance > threshold and right_distance > threshold:
			go_right(fast)
		elif left_distance < threshold and centre_distance < threshold and right_distance > threshold:
			go_right(fast)
		
		elif left_distance > threshold and centre_distance > threshold and right_distance < threshold:
			go_left(fast)
		elif left_distance > threshold and centre_distance < threshold and right_distance < threshold:
			go_left(fast)

		elif left_distance < threshold2 and centre_distance < threshold2 and right_distance < threshold2:
			print('Dead End')
			dead_end += 1
			go_backwards(slow)
			sleep(0.1)
			if left_distance < right_distance :
				go_right(fast)
			else:
				go_left(fast)
			sleep(0.5)
			if left_distance < right_distance :
				go_right(fast)
			else:
				go_left(fast)
			sleep(0.5)


		elif left_distance > threshold and centre_distance < threshold and right_distance > threshold:
			if left_distance < right_distance:
				go_right(fast)
			else:
				go_left(fast)

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
