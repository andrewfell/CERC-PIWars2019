#This program tests that you have the UDS GPIO mapping correct on your CERC Robot V2 chassis
#refer to GPIO pins allocations here: https://www.raspberrypi.org/documentation/usage/gpio/

# then import the 'sleep' class from the 'time' library (so we can add pauses in our program)
from time import sleep

# We'll use the distance sensor module in our CERCBot library (CERCBot.py)
import CERCBot

#define the name and pin mapping of each UDS.  This pin mapping should match the mapping in 
#https://github.com/andrewfell/CERC-PIWars2019/blob/master/Robot%20V2/RobotV2.md
left_echo_pin = 14
left_trigger_pin = 15
centre_echo_pin = 17
centre_trigger_pin = 4
right_echo_pin = 23
right_trigger_pin = 18


#begin looping forever
while True:
	
	#take a reading from the left, centre and right Ultra Sound Distance Sensors
	left_distance = CERCBot.calc_dist_cm(left_trigger_pin, left_echo_pin)
	centre_distance = CERCBot.calc_dist_cm(centre_trigger_pin, centre_echo_pin)
	right_distance = CERCBot.calc_dist_cm(right_trigger_pin, right_echo_pin)

	# Print out the measurements
	print(left_distance, centre_distance, right_distance)

	#wait a second between each scan
	sleep(1)
