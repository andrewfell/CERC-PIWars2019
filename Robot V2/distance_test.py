#This program tests that you have the UDS GPIO mapping correct on your CERC Robot V2 chassis
#refer to GPIO pins allocations here: https://www.raspberrypi.org/documentation/usage/gpio/
#the 'DistanceSensor' class of the gpiozero library is used: https://gpiozero.readthedocs.io/en/stable/recipes.html#distance-sensor
#the robot should read the UDS sensors in the following order:  Left > Centre > Right
#then 

#first of all, import the DistanceSensor class from the 'gpiozero' library
from gpiozero import DistanceSensor
#then import the 'sleep' class from the 'time' library (so we can add pauses in our program)
from time import sleep

#define the name and pin mapping of each UDS.  This pin mapping should match the mapping in 
#https://github.com/andrewfell/CERC-PIWars2019/blob/master/Robot%20V2/RobotV2.md
left_sensor = DistanceSensor(echo=14, trigger=15)
centre_sensor = DistanceSensor(echo=17, trigger=4)
right_sensor = DistanceSensor(echo=18, trigger=23)

#begining looping forever
while True:
	#take a reading from the left UDS
	left_distance = left_sensor.distance * 100
	#take a reading from the centre UDS
	centre_distance = centre_sensor.distance * 100
	#take a reading from the centre UDS
	right_distance = right_sensor.distance * 100

	#print the results on the screen
	print(left_distance, centre_distance, right_distance)
	#wait a second between each scan
	sleep(1)
