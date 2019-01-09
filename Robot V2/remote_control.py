from approxeng.input.selectbinder import ControllerResource
from gpiozero import Motor
from time import sleep

left_motor = Motor(8,7)
right_motor = Motor(21,20)

# Get a joystick
with ControllerResource(dead_zone=0.1, hot_zone=0.2) as joystick:
    # Loop until disconnected
    while joystick.connected:
        left_y = joystick.ly
        right_y = joystick.ry
        #print(left_y, right_y)

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
