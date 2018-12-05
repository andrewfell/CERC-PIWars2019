Code for Robot V2 platform.  Note GPIO mapping is currently as follows:

Purpose       |  Component name     | GPIO Pin
--------------|---------------------|----------------
Trigger pin   | Left UDS            | 15 
Echo pin      | Left UDS            | 14
Trigger pin   | Middle UDS          | 4
Echo pin      | Middle UDS          | 17
Trigger pin   | Right UDS           | 18
Echo pin      | Right UDS           | 23
Input 1       | Left motor          | 8
Input 2       | Left motor          | 7
Input 3       | Right motor         | 21
Input 4       | Right motor         | 20

The GPIOZERO library is most useful for what we need (https://gpiozero.readthedocs.io/en/stable/index.html).  
Install this onto your RPI aacording to this page: https://gpiozero.readthedocs.io/en/stable/installing.html

Recommend starting with driving your robot's motors.  Use the 


