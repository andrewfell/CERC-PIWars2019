#Import the libraries used in the program
from gpiozero import InputDevice, OutputDevice
from time import sleep, time

# Map the GPIO numbers to the motors
left_1_control = OutputDevice(8)
left_2_control = OutputDevice(7)

right_1_control = OutputDevice(21)
right_2_control = OutputDevice(20)

# Map the UDS trigger and echo pins
trig_left = OutputDevice(15)
echo_left = InputDevice(14)

trig_middle = OutputDevice(4)
echo_middle = InputDevice(17)

trig_right = OutputDevice(18)
echo_right = InputDevice(23)

#Define some constants to tune the program later
SOUND_CONSTANT = 353 * 50
UDS_PULSE_DURATION = 0.00001
UDS_LOOP_TIMEOUT = 5000
#offsets to account for the signals to/from pi to UDS
UDS_LEFT_OFFSET = 8
UDS_MIDDLE_OFFSET = 10
UDS_RIGHT_OFFSET = 8
#less than this distance on either side will make the robot change direction to move away from that side.
MIN_WALL_DISTANCE = 12
#less than this distance on the front will make the robot stop and turn 
FRONT_STOP_DISTANCE = 16
#less than this distance on either side or front will make the robot stop and give up
WALL_REALLY_CLOSE = 5
#this is the time it goes forward for before recalculating distance
FRONT_MOVE_TIME = 0.02
#these are the turn times for left and right adjustments to follow wall
RIGHT_ADJUST_TIME = 0.03
LEFT_ADJUST_TIME = 0.03
#these are the times for turning more or less 90 degrees.. this is on laminate floor.
LEFT_TURN_TIME = 0.4
RIGHT_TURN_TIME = 0.4
#these are the number of 90 degree turns after which the robot will stop.
MAX_TURNS_ALLOWED = 1

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
    
    # calculate distance of wall at left 
    def calc_distance_left(self):
        #Send the pulse 10microsec
        trig_left.on()
        sleep(UDS_PULSE_DURATION)
        trig_left.off()
        
        #Get the time from the clock.
        #There is a delay between the execution of pulse instruction
        # and the operatio of the UDS, so a calibrated approximate
        # offset is needed
        pulse_start = time()

        #Wait for the pulse to come back
        timeout = 0
        while echo_left.is_active == False:
            #Add timeout to avoid getting stuck.
            timeout=timeout+1
            if (timeout > UDS_LOOP_TIMEOUT):
               print("Error timeout UDS left start");
               return 1

        #record the time of pulse arrival
        pulse_end = time()
        timeout = 0
        while echo_left.is_active == True:
           pulse_end = time()
           timeout=timeout+1
           if (timeout > UDS_LOOP_TIMEOUT):
               print("Error timeout UDS left end");
               return 1
            
        #Calculate the distance from the pulse duration
        pulse = pulse_end - pulse_start
        self.left_distance = (SOUND_CONSTANT * pulse) - UDS_LEFT_OFFSET
        return 0

    # calculate distance of object in front of robot 
    def calc_distance_middle(self):
        trig_middle.on()
        sleep(UDS_PULSE_DURATION)
        trig_middle.off()
        pulse_start = time()
        timeout = 0
        while echo_middle.is_active == False:
           timeout=timeout+1
           if (timeout > UDS_LOOP_TIMEOUT):
               print("Error timeout UDS middle start");
               return 1
        pulse_end = time()
        timeout = 0
        while echo_middle.is_active == True:
           pulse_end = time()
           timeout=timeout+1
           if (timeout > UDS_LOOP_TIMEOUT):
               print("Error timeout UDS middle end");
               return 1
        pulse = pulse_end - pulse_start
        self.middle_distance = (SOUND_CONSTANT * pulse) - UDS_MIDDLE_OFFSET
        return 0

    # calculate distance of wall at right
    def calc_distance_right(self):
        trig_right.on()
        sleep(UDS_PULSE_DURATION)
        trig_right.off()
        pulse_start = time()
        timeout = 0
        while echo_right.is_active == False:
           timeout=timeout+1
           if (timeout > UDS_LOOP_TIMEOUT):
               print("Error timeout UDS right start");
               return 1
        pulse_end = time()
        timeout = 0
        while echo_right.is_active == True:
           pulse_end = time()
           timeout=timeout+1
           if (timeout > UDS_LOOP_TIMEOUT):
               print("Error timeout UDS right end");
               return 1
        pulse = pulse_end - pulse_start
        self.right_distance = (SOUND_CONSTANT * pulse) - UDS_RIGHT_OFFSET
        return 0

    # calculate distance left right and middle at the same time.
    def calc_distance(self):
        timeout = 0
        while(self.calc_distance_left() == 1):
           timeout = timeout+1 
        while(self.calc_distance_middle() == 1):
            timeout = timeout+1
        while(self.calc_distance_right() == 1):
            timeout = timeout+1
        if (timeout > 10):
            print("Too many UDS errors!")
            return 1
        return 0
    
#Create a robot object
myrobot = pirobot();

#taking the info to the log file so we can record what is happening
logfile = open("/home/pi/akshaye/logile.txt","w")
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
        if (left < MIN_WALL_DISTANCE and right > MIN_WALL_DISTANCE ):
            myrobot.turn_right(RIGHT_ADJUST_TIME)
        elif (right < MIN_WALL_DISTANCE and left > MIN_WALL_DISTANCE ):
            myrobot.turn_left(LEFT_ADJUST_TIME)
        elif (left < MIN_WALL_DISTANCE and right < MIN_WALL_DISTANCE ) or (left < WALL_REALLY_CLOSE or right < WALL_REALLY_CLOSE or middle < WALL_REALLY_CLOSE):
            myrobot.stop()

    #Stop the robot to turn.          
    myrobot.stop()
    logfile.write("stopped\n")
    logfile.flush()

    # Calculate distance again.  
    while (myrobot.calc_distance() == 1):
        logfile.write("Failed calc_distance\n")
    left = myrobot.left_distance
    middle = myrobot.middle_distance
    right = myrobot.right_distance
    logfile.write("%s,%s,%s\n" % (left,middle,right))

    #Turn the side where there is more space. need to watch out for the last turn
    if (left > right):
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
    if (left < MIN_WALL_DISTANCE and right > MIN_WALL_DISTANCE ):
        myrobot.turn_right(RIGHT_ADJUST_TIME)
    elif (right < MIN_WALL_DISTANCE and left > MIN_WALL_DISTANCE ):
        myrobot.turn_left(LEFT_ADJUST_TIME)
    elif (left < MIN_WALL_DISTANCE and right < MIN_WALL_DISTANCE ) or (left < WALL_REALLY_CLOSE or right < WALL_REALLY_CLOSE or middle < WALL_REALLY_CLOSE):
        myrobot.stop()

#We should be out of the maze now if all went well.
myrobot.stop()
logfile.close()



    







