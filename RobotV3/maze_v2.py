#Import the libraries used in the program
from gpiozero import InputDevice, OutputDevice
from time import sleep, time 
import CERCBot

# Map the GPIO numbers to the motors
left_1_control = OutputDevice(8)
left_2_control = OutputDevice(7)

right_1_control = OutputDevice(21)
right_2_control = OutputDevice(20)

#less than this distance on either side will make the robot change direction to move away from that side.
MIN_WALL_DISTANCE = 20
MAX_WALL_DISTANCE = 25
#less than this distance on the front will make the robot stop and turn 
FRONT_STOP_DISTANCE = 37
#this is the time it goes forward for before recalculating distance
FRONT_MOVE_TIME = 0.07
#these are the turn times for left and right adjustments to follow wall
RIGHT_ADJUST_TIME = 0.03
LEFT_ADJUST_TIME = 0.03
#these are the times for turning more or less 90 degrees.. this is on laminate floor.
LEFT_TURN_TIME = 0.41
RIGHT_TURN_TIME = 0.41
#these are the number of 90 degree turns after which the robot will stop.
MAX_TURNS_ALLOWED = 8

# Make a robot class to contain all the robot functions
class pirobot:

    # Create the robot functions

    # Initialize function for the robot.
    def __init__(self):
        #turn the motors off
        left_1_control.off()
        left_2_control.off() 
        right_1_control.off()
        right_2_control.off()
        #Initialize variables
        self.left_distance = 0
        self.middle_distance = 0
        self.right_distance = 0

    #Stop the robot motors
    def stop(self):
        left_1_control.off()
        left_2_control.off() 
        right_1_control.off()
        right_2_control.off()
        return

    #Move the robot forward for ever or for some time
    def move_forward(self,duration=0):
        left_1_control.on()
        left_2_control.off() 
        right_1_control.on()
        right_2_control.off()
        if duration != 0:
            sleep(duration)
            self.stop()
        return

    #Move the robot backward for ever or for some time... not used for now
    def move_back(self,duration=0):
        left_1_control.off()
        left_2_control.on() 
        right_1_control.off()
        right_2_control.on()
        if duration != 0:
            sleep(duration)
            self.stop()
        return

    #Turn the robot left for ever or for some time
    def turn_left(self,duration=0):
        left_1_control.off()
        left_2_control.on() 
        right_1_control.on()
        right_2_control.off()
        if duration != 0:
            sleep(duration)
            self.stop()
        return

    #Turn the robot right for ever or for some time
    def turn_right(self,duration=0):
        left_1_control.on()
        left_2_control.off() 
        right_1_control.off()
        right_2_control.on()
        if duration != 0:
            sleep(duration)
            self.stop()
        return

    # calculate distance of all UDS
    def calc_distance(self):
        self.left_distance = CERCBot.calc_dist_cm_v2(15, 14)
        self.middle_distance = CERCBot.calc_dist_cm_v2(4, 17)
        self.right_distance = CERCBot.calc_dist_cm_v2(18, 23)
        return 0

#Create a robot object
myrobot = pirobot();

#taking the info to the log file so we can record what is happening
logfile = open("/home/pi/CERCBot/logs/maze_logfile.txt","w")
logfile.write("sleeping for some time before starting\n")
sleep(2)
logfile.write("Starting program\n")

# only alowed to take limited number of turns
turns = 0
while(turns < MAX_TURNS_ALLOWED ):
    #Just a number to get it in the loop for the first time
    middle = FRONT_STOP_DISTANCE + 1

    #Keep going forward till distance in front is quite low
    while (middle > FRONT_STOP_DISTANCE):
        myrobot.move_forward(FRONT_MOVE_TIME)
        while (myrobot.calc_distance() == 1):
            logfile.write("Error: failed calc_distance\n")
        left = myrobot.left_distance
        middle = myrobot.middle_distance
        right = myrobot.right_distance
        logfile.write("%s,%s,%s\n" % (left,middle,right))
        logfile.flush()
        #Keep adjusting to appropriate distance from wall
        if (left < right):
            if (left < MIN_WALL_DISTANCE):
                myrobot.turn_right(RIGHT_ADJUST_TIME)
                logfile.write("right_adjust left wall follow\n")
            elif (left > MAX_WALL_DISTANCE):
                myrobot.turn_left(LEFT_ADJUST_TIME)
                logfile.write("left_adjust left wall follow\n")
        elif (left > right):
            if (right < MIN_WALL_DISTANCE):
                myrobot.turn_left(LEFT_ADJUST_TIME)
                logfile.write("left_adjust right wall follow\n")
            elif (right > MAX_WALL_DISTANCE):
                myrobot.turn_right(RIGHT_ADJUST_TIME)
                logfile.write("right_adjust right wall follow\n")

    #Stop the robot to turn.          
    #myrobot.stop()
    #logfile.write("stopped\n")
    #logfile.flush()

    # Calculate distance again.  
    #while (myrobot.calc_distance() == 1):
    #    logfile.write("Failed calc_distance\n")
    #left = myrobot.left_distance
    #middle = myrobot.middle_distance
    #right = myrobot.right_distance
    #logfile.write("%s,%s,%s\n" % (left,middle,right))

    #Turn the side where there is more space. need to watch out for the last turn
    if (left > right and turns < 7):
        myrobot.turn_left(LEFT_TURN_TIME)
        logfile.write("turned left\n")
    else:
        myrobot.turn_right(RIGHT_TURN_TIME)
        logfile.write("turned right\n")

    turns = turns + 1
    logfile.flush()

#All turns finished. Just keep going till you find an obstacle
middle = FRONT_STOP_DISTANCE + 1
while (middle > FRONT_STOP_DISTANCE):
    myrobot.move_forward(FRONT_MOVE_TIME)
    while (myrobot.calc_distance() == 1):
        logfile.write("Error: failed calc_distance\n")
    left = myrobot.left_distance
    middle = myrobot.middle_distance
    right = myrobot.right_distance
    logfile.write("%s,%s,%s\n" % (left,middle,right))
    logfile.flush()
    #Keep adjusting to appropriate distance from wall
    if (left < right):
        if (left < MIN_WALL_DISTANCE):
            myrobot.turn_right(RIGHT_ADJUST_TIME)
            logfile.write("right_adjust left wall follow\n")
        elif (left > MAX_WALL_DISTANCE):
            myrobot.turn_left(LEFT_ADJUST_TIME)
            logfile.write("left_adjust left wall follow\n")
    elif (left > right):
        if (right < MIN_WALL_DISTANCE):
            myrobot.turn_left(LEFT_ADJUST_TIME)
            logfile.write("left_adjust right wall follow\n")
        elif (right > MAX_WALL_DISTANCE):
            myrobot.turn_right(RIGHT_ADJUST_TIME)
            logfile.write("right_adjust right wall follow\n")

#We should be out of the maze now if all went well.
myrobot.stop()
logfile.write("stopped at end of maze\n")
logfile.close()



    







