#!/usr/bin/env python3
# -*- coding: utf-8 -*-
'''
**********************************************************
*
* PiRC - auto
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

#************************************
''' Main initialization routine '''
#************************************

def main():
    
    #make sure motors are stopped
    fullStop()
    
    while True:
        l, r = irSensors()
        obstacleAvoidance(l,r)

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
    runMotor(0,0)
    runMotor(1,0)

#************************************
''' Main initialization routine '''
#************************************
if __name__ == "__main__":
    sys.exit(main())
