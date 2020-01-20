from bluedot import BlueDot
from time import sleep
from signal import pause

bd = BlueDot()
colourDone = False
counter = 0 # Set variable 'counter' to 0 because we have not
colours = ['red','green','blue','yellow']

def set_colour():
    global colourDone
    colourDone = True
    print('Finished looking for colour')

def main_loop():
    global colourDone
    print('Entering while loop')
    for i in range(len(colours)):
        colourDone = False
        while colourDone == False:
            print(colours[i])
            sleep(0.5)

def dpad(pos):
    global counter
    # pressed any button yet to change it by 1
    if pos.top:
        print("up") # If the position of the press is up, then print 'up' 
        set_colour() # and call the set_colour() function
    if pos.bottom:
        print("down") # If the position of the press is down, print 'down' 
        counter += 1 # and change 'counter' by 1 because we have now pressed
        # the bottom part of the button
        if counter <= 1:
            main_loop() # Call the main_loop function# If the 'counter' is greater than or less than 2, which
            # means we have pressed the bottom part of the button twice,
    # then break out of the 'if pos.bottom' loop so
bd.when_pressed = dpad
pause()
