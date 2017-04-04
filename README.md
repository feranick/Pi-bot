# Pi-bot (piRC)
Raspberry Pi Robots

Under development. More to come.

Hardware
=========
- robot: RC car with one motor for power, one motor for steering.
- controller: Raspberry PI zero w
- IR sensors:
    - 2 front left side break beam sensors 3mm LEDs (https://www.adafruit.com/products/2167)
    - 1 front GP2Y0A21YK0F Sharp IR Analog Distance Sensor 10-80cm

Communication
==============
HTML-PHP is used to write status for power, steer on file. 
Python script reads such files and send command to GPIO. 

Driving mode
=============
- kind of automated (tries to avoid obstacles)
- controlled via HTML

Requirements
=============
Since it uses Python3, it requires rpi.gpio package:

    sudo apt-get install python3-rpi.gpio

Use
===
Two versions of PiRC are provided:
- pirc_file: communication between PHP and python is done via shared file. auto and manual 
control take place within the same python script
- pirc_nofile: communication between PHP and python is done via shell. Auto control is, 
well, automated, in the background. Manual control is done via python script when the user 
is calling for an action.

To be working properly, a library folder piRC_lib needs to be copied inside the two main 
folders respectively:
- pirc_file
- pirc_nofile
