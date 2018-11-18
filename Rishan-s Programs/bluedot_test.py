from bluedot import BlueDot
from gpiozero import Robot
from signal import pause
mc_in1=8
mc_in2=7
mc_in3=21                                       
mc_in4=20

bd = BlueDot()
robot = Robot(left=(mc_in1, mc_in2), right=(mc_in3, mc_in4))

def move(pos):
    if pos.top:
        robot.forward(pos.distance)
    elif pos.bottom:
        robot.backward(pos.distance)
    elif pos.left:
        robot.left(pos.distance)
    elif pos.right:
        robot.right(pos.distance)

def stop():
    robot.stop()

bd.when_pressed = move
bd.when_moved = move
bd.when_released = stop

pause()
