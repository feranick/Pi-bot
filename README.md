# Pi-bot (piRC)
Raspberry Pi Robots

Hardware
=========
- robot: RC car with one motor for power, one motor for steering.
- controller: Raspberry PI zero w
- ADC controller: 4 channel 16bit, ADS1115 (Op. Voltage: 3.3V)
- Accelerometer: XYZ, ADXL345 (Op. Voltage: 3.3V)
- Stepper motor controller: Adafruit TB6612, 1.2A DC (Op. Voltage: 3.3V or 5V)
- Sensing the motor status requires a 1.5MOhm resistor to from the power motor leads to the ADS1115. 
- Sonars: 3 HC-SR04 (left, right, center, back); (Op. Voltage: 5V)
  Warning: the output operating voltage is 5V, while RPi accepts only up to 3.3V, so you need a voltage divider. 

- Deprecated IR sensors:
    - 2 front left side break beam sensors 3mm LEDs (https://www.adafruit.com/products/2167)
    - 1 front GP2Y0A21YK0F Sharp IR Analog Distance Sensor 10-80cm https://goo.gl/BiFYpK

Communication
==============
HTML-PHP is used to write status for power, steer on file. 
Python script reads such files and send command to GPIO. 

Driving mode
=============
- kind of automated (tries to avoid obstacles)
- controlled via HTML
- Partially autonomous through machine learning 

Requirements
=============
Since it uses Python3, it requires the following packages

    sudo apt-get install python3-rpi.gpio python3-dev python3-pip

You would then need to install two libraries for the ADC (ADS1115) and accelerometer (ADXL345)

    sudo pip3 install adafruit-adxl345 adafruit-ads1x15

Use
===
Three versions of PiRC are provided:
- piRC_ML: construct a learning profile using manual controls. Train the algorithm. Run as autonomous.
- piRC_file: communication between PHP and python is done via shared file. auto and manual 
control take place within the same python script
- piRC_nofile: communication between PHP and python is done via shell. Auto control is, 
well, automated, in the background. Manual control is done via python script when the user 
is calling for an action.

Utilities
==========
- (pirc_init): Initialize sensors and GPIO ports for full use with remote control.

To be working properly, a library file piRC_lib.py needs to be copied inside the three main 
folders respectively:
- piRC_file
- piRC_nofile
- piRC_ML
