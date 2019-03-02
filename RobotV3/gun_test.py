from gpiozero import Motor, AngularServo

#then import the 'sleep' class from the 'time' library (so we can add pauses in our program)
from time import sleep

gun_motor = Motor(13,19)
laser = Motor(5,6)
servo = AngularServo(26, min_angle=-40, max_angle=50)
retract=-40
fire=50

print('laser on')
laser.forward()

print('servo back')
servo.angle=retract
sleep(0.5)
print('motors on')
gun_motor.forward(0.9)
sleep(5)

for x in range(5):
    print('fire ',x+1)
    servo.angle=fire
    sleep(0.5)
    print('retract')
    servo.angle=retract
    sleep(3)

gun_motor.stop()

print('laser off')
laser.stop()
