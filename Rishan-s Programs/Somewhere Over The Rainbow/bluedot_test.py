from bluedot import BlueDot
from time import sleep
from signal import pause

bd = BlueDot()
colourDone = False

def set_colour():
    global colourDone
    colourDone = True
    print('Finished looking for colours')

def main_loop():
    print('Entering while loop')
    while colourDone == False:
        print('Looking for colours')
        sleep(0.5)

def dpad(pos):
    if pos.top:
        print("up")
        set_colour()
    if pos.bottom:
        print("down")
        main_loop()
    
        
bd.when_pressed = dpad

pause()
