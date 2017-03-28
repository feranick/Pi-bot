# Pi-bot (piRC)
Raspberry Pi Robots

Under development. More to come.

Hardware
=========
- robot: RC car with one motor for power, one motor for steering.
- controller: Raspberry PI zero w

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


