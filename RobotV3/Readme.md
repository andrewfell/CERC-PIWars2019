Code for Robot V3 platform.  Note GPIO mapping is currently as follows:

Purpose       |  Component name       | GPIO Pin
--------------|-----------------------|----------------
Trigger pin   | Left UDS              | 15 
Echo pin      | Left UDS              | 14
Trigger pin   | Middle UDS            | 4
Echo pin      | Middle UDS            | 17
Trigger pin   | Right UDS             | 18
Echo pin      | Right UDS             | 23
Input 1       | Left motor            | 8
Input 2       | Left motor            | 7
Input 3       | Right motor           | 21
Input 4       | Right motor           | 20
Sensor OUT    | Right Line Sensor     | 27
Sensor OUT    | Left Line Sensor      | 22
Sensor OUT    | Mid-Right Line Sensor | 27
Sensor OUT    | Mid-Left Line Sensor  | 22
Input 1       | Nerf gun motor        | 13 
Input 2       | Nerf gun motor        | 19 
Input 3       | Gun Laser sight       | 5
Input 4       | Gun Laser signt       | 6
PWM           | Gun Fire servo        | 26


The GPIOZERO library is most useful for what we need (https://gpiozero.readthedocs.io/en/stable/index.html).  
Install this onto your RPI aacording to this page: https://gpiozero.readthedocs.io/en/stable/installing.html

Here is the pinout for the RPi connector: https://www.raspberrypi.org/documentation/usage/gpio/

Test code below:
* CERCBot.py (main library as per latest modification in RobotV2 directory)
* motor_test.py (code from V2 robot still current)
* distance_test.py  (code from V2 robot still current)
* gun_test.py (starts up the laser sight, starts the motors and then fires 5 darts)

For the remote control tasks, we have bluetooth paired a Playstation3 controller for bluetooth pairing of the PS3 - see here: https://approxeng.github.io/approxeng.input/api/dualshock3.html#pairing
Then the PS3 is read usin the pygame function - see remote_control.py ..  ref material here: https://www.pygame.org/docs/ref/joystick.html

