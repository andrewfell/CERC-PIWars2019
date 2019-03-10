import pygame
from gpiozero import Motor, AngularServo
from time import sleep

pygame.display.init()
pygame.joystick.init()
pygame.joystick.Joystick(0).init()

left_motor = Motor(8,7)
right_motor = Motor(21,20)
gun_motor = Motor(13,19)
laser = Motor(5,6)
servo = AngularServo(26, min_angle=-40, max_angle=45)
fire=45
retract=-40
servo.angle=retract
motors_on=False
gun_powder=1 #gun power it starts at


# Prints the joystick's name
JoyName = pygame.joystick.Joystick(0).get_name()
print ("Name of the joystick:")
print (JoyName)
# Gets the number of axes
#JoyAx = pygame.joystick.Joystick(0).get_numaxes()
#print ("Number of axis:")
#print (JoyAx)

while True:
        pygame.event.pump()
        #print(pygame.joystick.Joystick(0).get_axis(1))
        left_y = pygame.joystick.Joystick(0).get_axis(1)
        right_y = pygame.joystick.Joystick(0).get_axis(4)

        #print(left_y, right_y)
        
        #motor control
        if left_y > 0:
            left_motor.backward(abs(left_y))
        elif left_y < 0:
            left_motor.forward(abs(left_y))
        elif left_y == 0:
            left_motor.stop()

        if right_y > 0:
            right_motor.backward(abs(right_y))
        elif right_y < 0:
            right_motor.forward(abs(right_y))
        elif right_y == 0:
            right_motor.stop()

        if pygame.joystick.Joystick(0).get_button(13):
            laser.forward()
            print("Laser Sight On")
        if pygame.joystick.Joystick(0).get_button(14):
            laser.stop()
            print("Laser Sight Off")

        if pygame.joystick.Joystick(0).get_button(2):
            gun_motor.forward(gun_powder)
            print('Gun on')
            motors_on=True
        if pygame.joystick.Joystick(0).get_button(0):
            gun_motor.stop()
            print("Gun Off")
            motors_on=False

        if pygame.joystick.Joystick(0).get_button(3) and motors_on:
            gun_powder=gun_powder-0.1
            print("Reducing Gun Powder")
            if gun_powder < 0.5:
                gun_powder = 0.5
            gun_motor.forward(gun_powder)

        if pygame.joystick.Joystick(0).get_button(1) and motors_on:
            gun_powder=gun_powder+0.1
            print("Increasing Gun Powder")
            if gun_powder>1 :
                gun_powder = 1
            gun_motor.forward(gun_powder)


        if pygame.joystick.Joystick(0).get_button(7):
            if motors_on:
                servo.angle=fire
                print('Fire!')
                sleep(0.3)
                servo.angle=retract
    
