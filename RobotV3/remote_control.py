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
gun_powder=0.8

# Get a joystick
with ControllerResource(dead_zone=0.3, hot_zone=0.3) as joystick:
    # Loop until disconnected
    while joystick.connected:
        left_y = joystick.ly
        right_y = joystick.ry
        #presses = joystick.check.presess()
        #print(left_y, right_y)
        presses = joystick.check_presses()

        # If we had any presses, print the list of pressed buttons by standard name
        if joystick.has_presses:
            print(joystick.presses)

        #motor control
        if left_y < 0:
            left_motor.backward(abs(left_y))
        elif left_y > 0:
            left_motor.forward(left_y)
        elif left_y == 0:
            left_motor.stop()

        if right_y < 0:
            right_motor.backward(abs(right_y))
        elif right_y > 0:
            right_motor.forward(right_y)
        elif right_y == 0:
            right_motor.stop()


        if joystick.presses.dup:
            laser.forward()
        if joystick.presses.ddown:
            laser.stop()

        if joystick.presses.triangle:
            gun_motor.forward(gun_powder)
            print('Motors on')
            motors_on=True
        if joystick.presses.cross:
            gun_motor.stop()
            motors_on=False

        if joystick.presses.square and motors_on:
            gun_powder=gun_powder-0.1
            if gun_powder < 0.5:
                gun_powder = 0.5
            gun_motor.forward(gun_powder)

        if joystick.presses.circle and motors_on:
            gun_powder=gun_powder+0.1
            if gun_powder>1 :
                gun_powder = 1
            gun_motor.forward(gun_powder)


        if joystick.presses.r2:
            if motors_on:
                servo.angle=fire
                print('Fire!')
                sleep(0.3)
                servo.angle=retract
    
    print('joystick disconnected')        
