#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC_manual
* version: 20170327a
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''
#print(__doc__)

import RPi.GPIO as GPIO
from time import sleep
import sys

GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)

#these need to be fixed for TB6612
GPIO.setup(5,GPIO.OUT)   #AIN1 motor input A
GPIO.setup(7,GPIO.OUT)   #AIN2 motor input B
#GPIO.setup(5,GPIO.OUT)   #PWNA motor input B (power) - analog
GPIO.setup(11,GPIO.OUT)  #BIN1 motor input A
GPIO.setup(13,GPIO.OUT)  #BIN2 motor input B
#GPIO.setup(14,GPIO.OUT)   #PWNA motor input B (power) - analog

GPIO.setwarnings(False)

timeSleepSensor = 0.1
timeTransient0 = 0.05
timeTransient1 = 0.2
timeTransient2 = 0.5

#************************************
''' Main initialization routine '''
#************************************
def main():
    runManualControls(sys.argv[1])


#************************************
''' Control Motors'''
#************************************
def runMotor(motor, state):
    if motor == 1:  # motor for powering vehicle
        in1 = 5
        in2 = 7
        #pwn = 3
    
    elif motor == 0:    # motor for steering
        in1 = 11
        in2 = 13
        #pwn = 6
    
    if state == -1:
        GPIO.output(in1,0)
        GPIO.output(in2,1)
    if state == 0:
        GPIO.output(in1,0)
        GPIO.output(in2,0)
    if state == 1:
        GPIO.output(in1,1)
        GPIO.output(in2,0)
    #full power
    #GPIO.output(pwn, 255)


#************************************
''' RunManualControls '''
#************************************
def runManualControls(status):
    print(status)
    if status=='UP':
        runMotor(1,1)
    elif status=='DOWN':
        runMotor(1,-1)
    elif status=='STOP':
        runMotor(1,0)
    elif status=='ZERO':
        runMotor(0,0)
    else:
        if status=='LEFT':
            runMotor(0,1)
        if status=='RIGHT':
            runMotor(0,-1)
        sleep(timeTransient1)
        runMotor(0,0)

    #with open(webFolder+steerFile, 'w') as f:
    #    f.write(status)
#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
