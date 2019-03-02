from approxeng.input.selectbinder import ControllerResource
from gpiozero import Motor, AngularServo
from time import sleep

left_motor = Motor(8,7)
right_motor = Motor(21,20)
gun_motor = Motor(13,19)
laser = Motor(5,6)
servo = AngularServo(26, min_angle=-40, max_angle=45)
fire=45
retract=-40
servo.angle=retract
motors_on=False
gun_powder=0.8  #start at 80% power

# Get a joystick
with ControllerResource(dead_zone=0.3, hot_zone=0.3) as joystick:
    # Loop until disconnected
    while joystick.connected:
        #get the positions of the left and right joystick.  control the robot like a tank.
        left_y = joystick.ly
        right_y = joystick.ry

        #Check to see if any buttons are pressed.
        presses = joystick.check_presses()

        # If we had any presses, print the list of pressed buttons by standard name
        if joystick.has_presses:
            print(joystick.presses)

        #motor control for the left motors
        if left_y < 0:
            left_motor.backward(abs(left_y))
        elif left_y > 0:
            left_motor.forward(left_y)
        elif left_y == 0:
            left_motor.stop()

        #motor control for the right motors
        if right_y < 0:
            right_motor.backward(abs(right_y))
        elif right_y > 0:
            right_motor.forward(right_y)
        elif right_y == 0:
            right_motor.stop()

        #if the 'DUP' button is pressed, turn on the laser
        #laser is connected to motor board, so using the motor control class
        #if 'DDown' button is pressed, turn off the laser
        if joystick.presses.dup:
            laser.forward()
        if joystick.presses.ddown:
            laser.stop()

        # If the triangle is pressed, turn on the gun motor and set the 'Motor_on' flag true
        if joystick.presses.triangle:
            gun_motor.forward(gun_powder)
            print('Motors on')
            motors_on=True
        #if the cross is pressed, turnd off the gun motor and set the 'Motor_on' flag to false.
        if joystick.presses.cross:
            gun_motor.stop()
            motors_on=False

        #pressing square slows the motors by 10%... do not let the speed try to go below 50%, otherwise gun will stall and accuracy is poor
        if joystick.presses.square and motors_on:
            gun_powder=gun_powder-0.1
            if gun_powder < 0.5:
                gun_powder = 0.5
            gun_motor.forward(gun_powder)
        #pressing circle speeds the motor up by 10%.. do no let the speed try to go over 100%
        if joystick.presses.circle and motors_on:
            gun_powder=gun_powder+0.1
            if gun_powder>1 :
                gun_powder = 1
            gun_motor.forward(gun_powder)

        #Pressing the R2 button fires the dart by moving the servo to push the dart into the motors
        #After 0.3 seconds the servo goes back to the 'retract' position. 
        if joystick.presses.r2:
            if motors_on:
                servo.angle=fire
                print('Fire!')
                sleep(0.3)
                servo.angle=retract
    
    #If the controller gets disconnected, exit the program.
    print('joystick disconnected')        
