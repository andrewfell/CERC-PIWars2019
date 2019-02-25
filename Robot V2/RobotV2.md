Code for Robot V2 platform.  Note GPIO mapping is currently as follows:

Purpose       |  Component name       | GPIO Pin
--------------|-----------------------|----------------
Trigger pin   | Front Left UDS        | 15 
Echo pin      | Front Left UDS        | 14
Trigger pin   | Front Middle UDS      | 4
Echo pin      | Front Middle UDS      | 17
Trigger pin   | Front Right UDS       | 18
Echo pin      | Front Right UDS       | 23
Trigger pin   | Side Left UDS         | xx 
Echo pin      | Side Left UDS         | xx
Trigger pin   | Side Right UDS        | xx
Echo pin      | Side Right UDS        | xx
Input 1       | Left motor            | 8
Input 2       | Left motor            | 7
Input 3       | Right motor           | 21
Input 4       | Right motor           | 20
Sensor OUT    | Right Line Sensor     | 27
Sensor OUT    | Left Line Sensor      | 22
Sensor OUT    | Mid-Right Line Sensor | 27
Sensor OUT    | Mid-Left Line Sensor  | 22
Input 1       | Nerf gun motor        | 13 (will update)
Input 2       | Nerf gun motor        | 19 (will update)
Input 4       | Gun Laser sight       | xx (will update)
Input 4       | Gun Laser signt       | xx (will update)
PWM           | Gun Fire servo        | 26


The GPIOZERO library is most useful for what we need (https://gpiozero.readthedocs.io/en/stable/index.html).  
Install this onto your RPI aacording to this page: https://gpiozero.readthedocs.io/en/stable/installing.html

Here is the pinout for the RPi connector: https://www.raspberrypi.org/documentation/usage/gpio/

Recommend starting with driving your robot's motors and reading the UDS sensors.  
Use the example code I have provided, which contain comments to explain how it works:
* motor_test.py
* distance_test.py
