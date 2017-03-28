#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC
* version: 20170328b
*
* By: Nicola Ferralis <feranick@hotmail.com>
*
***********************************************************
'''
print(__doc__)

import sys
sys.path.append('piRC_lib')

import piRC_gpio
from piRC_lib import *

from time import sleep
import random as rd

timeSleepSensor = 0.1
timeTransient0 = 0.05
timeTransient1 = 0.2
timeTransient2 = 0.5

webFolder = "/var/www/html/pirc/"
steerFile = "steerStatus.txt"
powerFile = "powerStatus.txt"

#************************************
''' Main initialization routine '''
#************************************

def main():
    
    #make sure motors are stopped
    fullStop()
    
    while True:
        l, r = irSensors()
        obstacleAvoidance(l,r)

        runManualControls()

#************************************
''' RunManualControls '''
#************************************
def runManualControls():
    with open(webFolder+powerFile, 'r') as f:
        powerStatus = f.readlines()[0]
    print(powerStatus)
    sleep(timeTransient0)
    with open(webFolder+steerFile, 'r') as f:
        steerStatus = f.readlines()[0]
    print(steerStatus)

    if powerStatus=='UP':
        runMotor(1,1)
    elif powerStatus=='DOWN':
        runMotor(1,-1)
    elif powerStatus=='STOP':
        runMotor(1,0)

    if steerStatus=='ZERO':
        runMotor(0,0)
    else:
        if steerStatus=='LEFT':
            runMotor(0,1)
        elif steerStatus=='RIGHT':
            runMotor(0,-1)
        with open(webFolder+steerFile, 'w') as f:
            f.write("ZERO")
        sleep(timeTransient1)
        print('\t',steerStatus)
        runMotor(0,0)

#************************************
''' Obstacle Avoidance '''
#************************************
def obstacleAvoidance(l,r):
    if l==0 & r!=0:                                #Right IR sensor detects an object
        print('Obstacle detected on Left',str(l))
        runMotor(0, 1)
        runMotor(1, 1)
        sleep(timeSleepSensor)
    elif r==0 & l!=0:                              #Left IR sensor detects an object
        print('Obstacle detected on Right',str(r))
        runMotor(0, -1)
        runMotor(1, 1)
        sleep(timeSleepSensor)
    elif r==0 & l==0:
        print('Obstacle detected in front',str(r),'BRAKE!')
        randomDirection = int(rd.uniform(-2,2))
        runMotor(0,randomDirection)
        runMotor(1, -1)
        sleep(timeTransient1)
        runMotor(0,-randomDirection)
        runMotor(1, 1)
        sleep(timeTransient2)
    runMotor(0, 0)

#************************************
''' Full Stop '''
#************************************
def fullStop():
    print('\nFULL STOP\n')
    with open(webFolder+steerFile, 'w') as f:
        f.write("ZERO")
    runMotor(0,0)
    with open(webFolder+powerFile, 'w') as f:
        f.write("STOP")
    runMotor(1,0)

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
